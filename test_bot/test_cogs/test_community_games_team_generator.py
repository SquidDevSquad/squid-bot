import asyncio
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import Mock

import Config as Config
from cogs import community_games_team_generator
from utils import ListUtils, UserUtils, TestUtils


async def async_magic():
    pass


MagicMock.__await__ = lambda x: async_magic().__await__()


def verify_benched_players_play(benched_players, team0, team1):
    for benched_player in benched_players:
        player_id = benched_player.id
        if not ListUtils.find_by_id(player_id, team0) and not ListUtils.find_by_id(player_id, team1):
            return False
    return True


def verify_bench_does_not_contain_players(bench, team0, team1):
    for benched_player in bench:
        player_id = benched_player.id
        if ListUtils.find_by_id(player_id, team0) or ListUtils.find_by_id(player_id, team1):
            return False
    return True


ctx_mock = MagicMock()


class TestCommunityGamesTeamGenerator(TestCase):

    def setUp(self) -> None:
        ctx_mock.author.id = Config.ADMIN_IDS[0]
        super().setUp()

    def test_generate_teams_command_no_allowed_channels(self):
        ctx_mock.message.channel.id = "Some channel"
        Config.ALLOWED_TEXT_CHANNEL_IDS = []
        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(None)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        self.assertTrue(ctx_mock.send.called)
        self.assertEqual('Not allowed to operate on this channel', ctx_mock.send.call_args[0][0])

    def test_generate_team_less_than_12_players(self):
        Config.ALLOWED_TEXT_CHANNEL_IDS = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL_ID
        voice_channel_mock.members = TestUtils.generate_mock_players_list(11)

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"
        # ctx_mock.guild.voice_channels = [voice_channel_mock]

        client_mock = Mock()
        client_mock.global_variables.bench = list()
        client_mock.get_channel.return_value = voice_channel_mock
        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(client_mock)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        self.assertTrue(ctx_mock.send.called)
        self.assertEqual('@Kane Not enough players for 2 teams. Currently have: 11. At least 12 players needed.',
                         ctx_mock.send.call_args[0][0])

    def test_generate_teams_exactly_12_players(self):
        Config.ALLOWED_TEXT_CHANNEL_IDS = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL_ID
        voice_channel_mock.members = TestUtils.generate_mock_players_list(12)

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"

        client_mock = Mock()
        client_mock.global_variables.bench = list()
        client_mock.get_channel.return_value = voice_channel_mock

        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(client_mock)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        self.assertEqual(6, len(client_mock.global_variables.teams[0]))
        self.assertEqual(6, len(client_mock.global_variables.teams[1]))
        self.assertFalse(ListUtils.contains_duplicates(client_mock.global_variables.teams[0]))
        self.assertFalse(ListUtils.contains_duplicates(client_mock.global_variables.teams[1]))
        self.assertEqual(0, len(voice_channel_mock.members))

    def test_generate_teams_more_than_12_players(self):
        Config.ALLOWED_TEXT_CHANNEL_IDS = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL_ID
        voice_channel_mock.members = TestUtils.generate_mock_players_list(22)

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"

        client_mock = Mock()
        client_mock.global_variables.bench = list()
        client_mock.get_channel.return_value = voice_channel_mock

        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(client_mock)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        self.assertEqual(6, len(client_mock.global_variables.teams[0]))
        self.assertEqual(6, len(client_mock.global_variables.teams[1]))
        self.assertEqual(10, len(client_mock.global_variables.bench))
        self.assertFalse(ListUtils.contains_duplicates(client_mock.global_variables.teams[0]))
        self.assertFalse(ListUtils.contains_duplicates(client_mock.global_variables.teams[1]))
        self.assertFalse(ListUtils.contains_duplicates(client_mock.global_variables.bench))
        self.assertEqual(0, len(voice_channel_mock.members))

    def test_generate_teams_from_bench(self):
        Config.ALLOWED_TEXT_CHANNEL_IDS = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL_ID
        voice_channel_mock.members = TestUtils.generate_mock_players_list(22)

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"

        client_mock = Mock()
        client_mock.get_channel.return_value = voice_channel_mock
        benched_players = TestUtils.generate_mock_players_list(5)
        client_mock.global_variables.bench = benched_players.copy()

        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(client_mock)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        team0 = client_mock.global_variables.teams[0]
        team1 = client_mock.global_variables.teams[1]
        bench = client_mock.global_variables.bench
        self.assertEqual(6, len(team0))
        self.assertEqual(6, len(team1))
        self.assertEqual(10, len(bench))
        self.assertTrue(verify_benched_players_play(benched_players, team0, team1))
        self.assertTrue(verify_bench_does_not_contain_players(bench, team0, team1))
        self.assertFalse(ListUtils.contains_duplicates(team0))
        self.assertFalse(ListUtils.contains_duplicates(team1))
        self.assertFalse(ListUtils.contains_duplicates(bench))
        self.assertEqual(0, len(voice_channel_mock.members))

    def test_generate_teams_with_spectators(self):
        Config.ALLOWED_TEXT_CHANNEL_IDS = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL_ID
        online_players = TestUtils.generate_mock_players_list(15)
        idle_players = TestUtils.generate_mock_players_list(10, UserUtils.IDLE)
        all_players = list()
        all_players.extend(online_players)
        all_players.extend(idle_players)
        voice_channel_mock.members = all_players

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"

        client_mock = Mock()
        client_mock.get_channel.return_value = voice_channel_mock
        client_mock.global_variables.bench = list()

        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(client_mock)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        team0 = client_mock.global_variables.teams[0]
        team1 = client_mock.global_variables.teams[1]

        bench = client_mock.global_variables.bench
        spectators = client_mock.global_variables.spectators
        self.assertEqual(6, len(team0))
        self.assertEqual(6, len(team1))
        self.assertEqual(3, len(bench))
        self.assertEqual(10, len(spectators))
        self.assertTrue(verify_bench_does_not_contain_players(bench, team0, team1))
        self.assertFalse(ListUtils.contains_duplicates(team0))
        self.assertFalse(ListUtils.contains_duplicates(team1))
        self.assertFalse(ListUtils.contains_duplicates(bench))
        self.assertEqual(0, len(voice_channel_mock.members))
