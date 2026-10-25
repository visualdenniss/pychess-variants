from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from const import DRAW, T_FINISHED
from newid import id8
from pychess_global_app_state_utils import get_app_state
from tournament.auto_play_tournament import ArenaTestTournament
from tournament.tournament import GameData, upsert_tournament_to_db
from tournament_test_base import TournamentTestCase


class ArenaPairingTestCase(TournamentTestCase):
    async def make_tournament(self, nb_players):
        app_state = get_app_state(self.app)
        self.tournament = ArenaTestTournament(app_state, id8(), variant="asean", with_clock=False)
        app_state.tournaments[self.tournament.id] = self.tournament
        await upsert_tournament_to_db(self.tournament, app_state)
        await self.tournament.join_players(nb_players, rating=1500)
        players = list(self.tournament.players)
        for rank, player in enumerate(players, start=1):
            player_data = self.tournament.player_data_by_name(player.username)
            assert player_data is not None
            self.tournament.set_leaderboard_score_by_username(
                player.username,
                self.tournament.compose_leaderboard_score(nb_players - rank, player_data),
            )
        return players

    def assert_pairing(self, waiting_players, expected):
        pairing = self.tournament.create_pairing(waiting_players)
        self.assertEqual(
            {frozenset((white.username, black.username)) for white, black in pairing},
            {frozenset((a.username, b.username)) for a, b in expected},
        )

    async def test_pairs_nearby_ranks(self):
        players = await self.make_tournament(4)
        for waiting in (players, players[::-1]):
            with self.subTest(waiting=[player.username for player in waiting]):
                self.assert_pairing(waiting, [(players[0], players[1]), (players[2], players[3])])

    async def test_pairs_leaders_with_each_other_when_lower_ranks_are_waiting(self):
        players = await self.make_tournament(17)
        self.assert_pairing(
            [players[0], players[2], players[14], players[16]],
            [(players[0], players[2]), (players[14], players[16])],
        )

    async def test_maximizes_pair_count_before_minimizing_distance(self):
        players = await self.make_tournament(4)
        # The closest pair (ranks 1 and 2) would leave ranks 3 and 4 unable to play.
        player_data = self.tournament.player_data_by_name(players[2].username)
        assert player_data is not None
        player_data.prev_opp = players[3].username
        self.assert_pairing(players, [(players[0], players[2]), (players[1], players[3])])

    async def test_rank_weighting_scales_gradually(self):
        players = await self.make_tournament(4)
        for player, rating in zip(players, (1000, 2250, 1000, 2250)):
            self.tournament.players[player].rating = rating
        # Lichess's gradual rank factors favor adjacent ranks here. Rounding the
        # fraction before multiplying instead pairs the two equal-rating groups.
        self.assert_pairing(players, [(players[0], players[1]), (players[2], players[3])])

    async def record_colors(self, players, colors):
        games = []
        date = datetime.now(UTC)
        for index, color in enumerate(colors):
            white, black = players if color == "W" else players[::-1]
            game = GameData(
                id8(),
                white.username,
                "1500",
                black.username,
                "1500",
                "1/2-1/2",
                date + timedelta(seconds=index),
                False,
                False,
                status=DRAW,
                ply=20,
            )
            self.tournament.update_players(game)
            games.append(game)
        return games

    async def test_color_streak_resets_when_color_changes(self):
        players = await self.make_tournament(2)
        for colors, expected in (("WWW", (3, 3)), ("B", (-1, 2)), ("BB", (-3, 0)), ("W", (1, 1))):
            await self.record_colors(players, colors)
            white_data, black_data = (self.tournament.players[player] for player in players)
            self.assertEqual((white_data.color_streak, white_data.color_balance), expected)
            self.assertEqual(
                (black_data.color_streak, black_data.color_balance),
                tuple(-value for value in expected),
            )

    async def test_same_color_streaks_block_pairing_even_with_balanced_totals(self):
        players = await self.make_tournament(4)
        for streaks in ((3, 3), (-3, -3), (3, 4), (-4, -3)):
            with self.subTest(streaks=streaks):
                for player, streak in zip(players[:2], streaks):
                    self.tournament.players[player].color_streak = streak
                self.assert_pairing(players, [(players[0], players[2]), (players[1], players[3])])

    async def test_total_color_imbalance_does_not_block_short_streaks(self):
        players = await self.make_tournament(4)
        for balance in (3, -3):
            with self.subTest(balance=balance):
                for player in players[:2]:
                    data = self.tournament.players[player]
                    data.color_balance = balance
                    data.color_streak = 1 if balance > 0 else -1
                self.assert_pairing(players, [(players[0], players[1]), (players[2], players[3])])

    async def test_color_assignment_prioritizes_streak_then_balance(self):
        players = await self.make_tournament(2)
        cases = (
            ((2, 2), (3, 1), 0),
            ((-2, -2), (-1, -3), 0),
            ((2, 2), (2, 0), 1),
            ((-2, -2), (-2, 0), 0),
        )
        for a, b, white_index in cases:
            with self.subTest(a=a, b=b):
                for player, history in zip(players, (a, b)):
                    data = self.tournament.players[player]
                    data.color_streak, data.color_balance = history
                self.assertEqual(
                    self.tournament.create_pairing(players),
                    [(players[white_index], players[1 - white_index])],
                )

    async def test_equal_color_histories_use_random_color(self):
        players = await self.make_tournament(2)
        for first_gets_white in (True, False):
            with patch("tournament.arena.random.choice", return_value=first_gets_white):
                white_index = 0 if first_gets_white else 1
                self.assertEqual(
                    self.tournament.create_pairing(players),
                    [(players[white_index], players[1 - white_index])],
                )

    async def test_two_waiting_players_respect_color_streaks_except_in_duel(self):
        players = await self.make_tournament(4)
        await self.tournament.create_games([(players[2], players[3])])
        for player in players[:2]:
            self.tournament.players[player].color_streak = 3
        self.assertEqual(self.tournament.create_pairing(players[:2]), [])
        self.tournament.ongoing_games.clear()
        self.assert_pairing(players[:2], [(players[0], players[1])])

    async def test_reload_restores_color_streak_from_pairing_history(self):
        players = await self.make_tournament(2)
        games = await self.record_colors(players, "WWWBBB")
        for game in games:
            await self.tournament.db_update_pairing(game)
        self.tournament.status = T_FINISHED
        app_state = get_app_state(self.app)
        await upsert_tournament_to_db(self.tournament, app_state)
        _, reloaded = await self.reload_tournament(app_state.db_client, self.tournament.id)
        for player, streak in zip(players, (-3, 3)):
            data = reloaded.player_data_by_name(player.username)
            self.assertIsNotNone(data)
            self.assertEqual((data.color_streak, data.color_balance), (streak, 0))
