import json
from unittest.mock import AsyncMock, patch

import test_logger
from aiohttp import WSMsgType
from aiohttp.test_utils import AioHTTPTestCase
from bug.game_bug import GameBug
from bug.utils_bug import insert_game_to_db_bughouse
from const import ABANDON, ABORTED, FLAG, RATED, RESIGN, STARTED
from game import Game
from glicko2.glicko2 import new_default_perf_map
from mongomock_motor import AsyncMongoMockClient
from newid import id8
from pychess_global_app_state_utils import get_app_state
from user import User
from utils import insert_game_to_db
from variants import VARIANTS
from wsr import process_message

from server import make_app

test_logger.init_test_logger()


class RoundEndAuthorizationTestCase(AioHTTPTestCase):
    async def get_application(self):
        return make_app(db_client=AsyncMongoMockClient(tz_aware=True))

    async def tearDownAsync(self):
        await self.client.close()

    async def new_game(self, *, bughouse=False, anonymous_player=False):
        state = get_app_state(self.app)
        players = [
            User(
                state,
                username=f"end-player-{seat}",
                anon=anonymous_player and seat == 0,
                perfs=new_default_perf_map(VARIANTS),
            )
            for seat in range(4 if bughouse else 2)
        ]
        for player in players:
            state.users[player.username] = player
        if bughouse:
            game = GameBug(state, id8(), "bughouse", "", *players, rated=RATED)
            self.addAsyncCleanup(game.gameClocks.cancel_stopwatches)
            await insert_game_to_db_bughouse(game, state)
        else:
            game = Game(state, id8(), "chess", "", *players, rated=RATED)
            self.addAsyncCleanup(game.stopwatch.cancel)
            await insert_game_to_db(game, state)
        state.games[game.id] = game
        # Keep abort eligible while also exercising an ongoing game.
        if bughouse:
            await game.play_move("e2e4", clocks=[60000, 60000], clocks_b=[60000, 60000])
            await game._persist_queue.join()
        else:
            await game.play_move("e2e4")
        return state, game, players

    async def test_spectators_cannot_end_games_or_trigger_game_end_side_effects(self):
        for bughouse in (False, True):
            for anonymous in (False, True):
                with self.subTest(bughouse=bughouse, anonymous=anonymous):
                    state, game, players = await self.new_game(bughouse=bughouse)
                    spectator = User(state, username="end-spectator", anon=anonymous)
                    game.spectators.add(spectator)
                    before = await state.db.game.find_one({"_id": game.id})
                    perfs_before = json.dumps([player.perfs for player in players], sort_keys=True)
                    ws = AsyncMock()
                    with (
                        patch.object(game, "game_ended", wraps=game.game_ended) as end,
                        patch("wsr.round_broadcast", new=AsyncMock()) as broadcast,
                        patch("bug.wsr_bug.round_broadcast", new=AsyncMock()) as bug_broadcast,
                    ):
                        for control in ("resign", "abandon", "abort", "flag"):
                            await process_message(
                                state, spectator, ws, {"type": control, "gameId": game.id}, game
                            )
                            self.assertEqual(game.status, STARTED)
                            self.assertEqual(game.result, "*")
                        end.assert_not_awaited()
                        broadcast.assert_not_awaited()
                        bug_broadcast.assert_not_awaited()
                    ws.send_str.assert_not_awaited()
                    self.assertEqual(await state.db.game.find_one({"_id": game.id}), before)
                    self.assertEqual(
                        json.dumps([player.perfs for player in players], sort_keys=True),
                        perfs_before,
                    )
                    if bughouse:
                        self.assertIsNone(game.resign_offer)

    async def test_cookie_free_spectator_socket_cannot_end_games(self):
        for bughouse in (False, True):
            with self.subTest(bughouse=bughouse):
                state, game, _players = await self.new_game(bughouse=bughouse)
                before = await state.db.game.find_one({"_id": game.id})
                self.client.session.cookie_jar.clear()
                origin = str(self.client.make_url("/")).rstrip("/")
                async with self.client.ws_connect(
                    f"/wsr/{game.id}", headers={"Origin": origin}
                ) as ws:
                    while True:
                        message = await ws.receive_json(timeout=2)
                        if message["type"] == "game_user_connected":
                            spectator = state.users[message["username"]]
                            break
                    self.assertTrue(spectator.anon)
                    self.assertFalse(game.is_player(spectator))
                    self.assertIn(spectator, game.spectators)
                    for control in ("resign", "abandon", "abort", "flag"):
                        await ws.send_json({"type": control, "gameId": game.id})
                    # The echoed ping is a barrier: all four control messages were processed.
                    await ws.send_str("/n")
                    while True:
                        response = await ws.receive(timeout=2)
                        self.assertEqual(response.type, WSMsgType.TEXT)
                        if response.data == "/n":
                            break
                        self.assertNotEqual(json.loads(response.data)["type"], "gameEnd")
                    self.assertEqual(game.status, STARTED)
                    self.assertEqual(game.result, "*")
                    self.assertEqual(await state.db.game.find_one({"_id": game.id}), before)

    async def test_each_player_can_still_end_their_game(self):
        for anonymous in (False, True):
            for seat in (0, 1):
                for control, status in (
                    ("resign", RESIGN),
                    ("abandon", ABANDON),
                    ("abort", ABORTED),
                ):
                    with self.subTest(anonymous=anonymous, seat=seat, control=control):
                        state, game, players = await self.new_game(anonymous_player=anonymous)
                        with patch.object(game, "save_game", new=AsyncMock()) as save:
                            await process_message(
                                state,
                                players[seat],
                                AsyncMock(),
                                {"type": control, "gameId": game.id},
                                game,
                            )
                        self.assertEqual(game.status, status)
                        expected = "*" if control == "abort" else ("0-1" if seat == 0 else "1-0")
                        self.assertEqual(game.result, expected)
                        save.assert_awaited_once()

    async def test_all_four_bughouse_players_can_still_end_their_game(self):
        for seat in range(4):
            for control, status in (
                ("resign", RESIGN),
                ("abandon", ABANDON),
                ("abort", ABORTED),
                ("flag", FLAG),
            ):
                with self.subTest(seat=seat, control=control):
                    state, game, players = await self.new_game(bughouse=True)
                    player = players[seat]
                    with patch.object(game, "save_game", new=AsyncMock()) as save:
                        await process_message(
                            state, player, AsyncMock(), {"type": control, "gameId": game.id}, game
                        )
                        if control == "resign":
                            self.assertEqual(game.status, STARTED)
                            partner = state.users[game.partner_of(player.username)]
                            await process_message(
                                state,
                                partner,
                                AsyncMock(),
                                {"type": control, "gameId": game.id},
                                game,
                            )
                    self.assertEqual(game.status, status)
                    expected = "*" if control == "abort" else ("0-1" if seat in (0, 3) else "1-0")
                    self.assertEqual(game.result, expected)
                    save.assert_awaited_once()
