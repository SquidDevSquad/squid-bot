import asyncio
from unittest import TestCase
from unittest.mock import MagicMock

import Config as Config
from cogs import community_games_team_generator


async def async_magic():
    pass


MagicMock.__await__ = lambda x: async_magic().__await__()


def generate_players_list(length):
    players_list = []
    for i in range(length):
        players_list.append("player" + str(i))
    return players_list


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

    def test_generate_team_less_than_12_players(self):
        ctx_mock = MagicMock()
        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"
        Config.ALLOWED_CHANNEL = ["Community Games"]
        client_mock = MagicMock()
        client_mock.global_variables.players_list = generate_players_list(11)
        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(client_mock)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        self.assertTrue(ctx_mock.send.called)
        self.assertEqual('@Kane Not enough players for 2 teams. Currently have: 11. At least 12 players needed.',
                         ctx_mock.send.call_args[0][0])

    def test_generate_teams(self):
        self.fail()

    def test_generate_team_embed_message(self):
        self.fail()

    def test_fill_players_allowed_to_play(self):
        self.fail()
