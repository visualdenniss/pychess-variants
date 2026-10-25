from newid import id8
from pychess_global_app_state_utils import get_app_state
from tournament.auto_play_tournament import ArenaTestTournament
from tournament.tournament import upsert_tournament_to_db
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
