import asyncio
import time
from unittest import TestCase
from unittest.mock import MagicMock

import Config
from cogs import giveaway
from utils import TestUtils


async def async_magic():
    pass


MagicMock.__await__ = lambda x: async_magic().__await__()

ctx_mock = MagicMock()

current_milli_time = lambda: int(round(time.time() * 1000))


def time_elapsed(start_time):
    return current_milli_time() - start_time > 10_000


class TestGiveaway(TestCase):

    def setUp(self) -> None:
        ctx_mock.author.id = Config.ADMIN_IDS[0]
        super().setUp()

    def test_giveaway_command_no_prev_winners(self):
        Config.ALLOWED_TEXT_CHANNEL_IDS = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL_ID
        voice_channel_mock.members = TestUtils.generate_mock_players_list(10)

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"

        client_mock = MagicMock()
        client_mock.global_variables.giveaway_winners = []
        client_mock.get_channel.return_value = voice_channel_mock

        giveaway_command = giveaway.Giveaway(client_mock)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(giveaway_command.giveaway_command(giveaway_command, ctx_mock))

        winners = client_mock.global_variables.giveaway_winners

        self.assertIsNotNone(winners)
        self.assertTrue('Winners list was expected to be non-empty', winners)
        self.assertEqual(1, len(winners))

        self.assertTrue(ctx_mock.send.called)
        self.assertIsNotNone(ctx_mock.send.call_args[1]['embed'].description)

    def test_giveaway_command_with_prev_winners(self):
        Config.ALLOWED_TEXT_CHANNEL_IDS = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL_ID
        voice_channel_mock.members = TestUtils.generate_mock_players_list(10)

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"

        client_mock = MagicMock()
        client_mock.global_variables.giveaway_winners = [voice_channel_mock.members[0]]
        client_mock.get_channel.return_value = voice_channel_mock

        giveaway_command = giveaway.Giveaway(client_mock)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(giveaway_command.giveaway_command(giveaway_command, ctx_mock))

        winners = client_mock.global_variables.giveaway_winners

        self.assertIsNotNone(winners)
        self.assertTrue('Winners list was expected to be non-empty', winners)
        self.assertEqual(2, len(winners))
        self.assertTrue(voice_channel_mock.members[0] in winners)

        self.assertTrue(ctx_mock.send.called)
        self.assertIsNotNone(ctx_mock.send.call_args[1]['embed'].description)

    def test_giveaway_call_until_all_are_winners(self):
        Config.ALLOWED_TEXT_CHANNEL_IDS = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL_ID
        voice_channel_mock.members = TestUtils.generate_mock_players_list(10)

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"

        client_mock = MagicMock()
        client_mock.global_variables.giveaway_winners = []
        winners = client_mock.global_variables.giveaway_winners
        client_mock.get_channel.return_value = voice_channel_mock

        giveaway_command = giveaway.Giveaway(client_mock)

        start_time = current_milli_time()
        while time_elapsed(start_time) or len(winners) < len(voice_channel_mock.members):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(giveaway_command.giveaway_command(giveaway_command, ctx_mock))

            self.assertIsNotNone(winners)
            self.assertTrue('Winners list was expected to be non-empty', winners)

            self.assertTrue(ctx_mock.send.called)
            self.assertIsNotNone(ctx_mock.send.call_args[1]['embed'].description)
        self.assertEqual(len(winners), len(voice_channel_mock.members))
