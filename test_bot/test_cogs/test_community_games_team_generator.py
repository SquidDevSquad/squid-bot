import asyncio
from unittest import TestCase
from unittest.mock import MagicMock

import Config as Config
from cogs import community_games_team_generator


async def async_magic():
    pass


MagicMock.__await__ = lambda x: async_magic().__await__()


class TestCommunityGamesTeamGenerator(TestCase):
    def test_generate_teams_command_no_allowed_channels(self):
        ctx_mock = MagicMock()
        ctx_mock.message.channel.id = "Some channel"
        Config.ALLOWED_CHANNEL = []
        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(None)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        self.assertTrue(ctx_mock.send.called)
        self.assertEqual('Not allowed to operate on this channel', ctx_mock.send.call_args[0][0])

    def test_generate_team(self):
        self.fail()

    def test_generate_teams(self):
        self.fail()

    def test_generate_team_embed_message(self):
        self.fail()

    def test_fill_players_allowed_to_play(self):
        self.fail()
