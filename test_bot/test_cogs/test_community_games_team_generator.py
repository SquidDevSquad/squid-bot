import asyncio
from unittest import TestCase
from unittest.mock import MagicMock

import Config as Config
import UserUtils
from cogs import community_games_team_generator


async def async_magic():
    pass


MagicMock.__await__ = lambda x: async_magic().__await__()


def generate_players_list(length):
    players = list()
    for i in range(length):
        player = MagicMock()
        player.nick = None
        player.id = i
        player.name = "player" + str(i)
        players.append(player)
    return players


def contains_duplicates(lst):
    if len(lst) == len(set(lst)):
        return False
    else:
        return True


def verify_benched_players_play(benched_players, team0, team1):
    for benched_player in benched_players:
        player_id = benched_player.id
        if not UserUtils.find(player_id, team0) and not UserUtils.find(player_id, team1):
            return False
    return True


def verify_bench_does_not_contain_players(bench, team0, team1):
    for benched_player in bench:
        player_id = benched_player.id
        if UserUtils.find(player_id, team0) or UserUtils.find(player_id, team1):
            return False
    return True


ctx_mock = MagicMock()


class TestCommunityGamesTeamGenerator(TestCase):

    def setUp(self) -> None:
        ctx_mock.author.id = Config.ALLOWED_USER_TO_ADMIN_COMMANDS[0]
        super().setUp()

    def test_generate_teams_command_no_allowed_channels(self):
        ctx_mock.message.channel.id = "Some channel"
        Config.ALLOWED_CHANNEL = []
        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(None)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        self.assertTrue(ctx_mock.send.called)
        self.assertEqual('Not allowed to operate on this channel', ctx_mock.send.call_args[0][0])

    def test_generate_team_less_than_12_players(self):
        Config.ALLOWED_CHANNEL = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL
        voice_channel_mock.members = generate_players_list(11)

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"
        ctx_mock.guild.voice_channels = [voice_channel_mock]

        client_mock = MagicMock()
        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(client_mock)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        self.assertTrue(ctx_mock.send.called)
        self.assertEqual('@Kane Not enough players for 2 teams. Currently have: 11. At least 12 players needed.',
                         ctx_mock.send.call_args[0][0])

    def test_generate_teams_exactly_12_players(self):
        Config.ALLOWED_CHANNEL = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL
        voice_channel_mock.members = generate_players_list(12)

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"
        ctx_mock.guild.voice_channels = [voice_channel_mock]

        client_mock = MagicMock()
        client_mock.global_variables.teams = list()
        client_mock.global_variables.teams.append(list())
        client_mock.global_variables.teams.append(list())
        client_mock.global_variables.bench = list()

        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(client_mock)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        self.assertEqual(6, len(client_mock.global_variables.teams[0]))
        self.assertEqual(6, len(client_mock.global_variables.teams[1]))
        self.assertFalse(contains_duplicates(client_mock.global_variables.teams[0]))
        self.assertFalse(contains_duplicates(client_mock.global_variables.teams[1]))
        self.assertEqual(0, len(voice_channel_mock.members))

    def test_generate_teams_more_than_12_players(self):
        Config.ALLOWED_CHANNEL = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL
        voice_channel_mock.members = generate_players_list(22)

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"
        ctx_mock.guild.voice_channels = [voice_channel_mock]

        client_mock = MagicMock()
        client_mock.global_variables.teams = list()
        client_mock.global_variables.teams.append(list())
        client_mock.global_variables.teams.append(list())
        client_mock.global_variables.bench = list()

        comm_games_team_generator = community_games_team_generator.CommunityGamesTeamGenerator(client_mock)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(comm_games_team_generator.generate_teams_command(comm_games_team_generator, ctx_mock))
        self.assertEqual(6, len(client_mock.global_variables.teams[0]))
        self.assertEqual(6, len(client_mock.global_variables.teams[1]))
        self.assertEqual(10, len(client_mock.global_variables.bench))
        self.assertFalse(contains_duplicates(client_mock.global_variables.teams[0]))
        self.assertFalse(contains_duplicates(client_mock.global_variables.teams[1]))
        self.assertFalse(contains_duplicates(client_mock.global_variables.bench))
        self.assertEqual(0, len(voice_channel_mock.members))

    def test_generate_teams_from_bench(self):
        Config.ALLOWED_CHANNEL = ["Community Games"]

        voice_channel_mock = MagicMock()
        voice_channel_mock.id = Config.COMMUNITY_GAMES_VOICE_CHANNEL
        voice_channel_mock.members = generate_players_list(22)

        ctx_mock.message.channel.id = "Community Games"
        ctx_mock.author.mention = "@Kane"
        ctx_mock.guild.voice_channels = [voice_channel_mock]

        client_mock = MagicMock()
        client_mock.global_variables.teams = list()
        client_mock.global_variables.teams.append(list())
        client_mock.global_variables.teams.append(list())
        benched_players = generate_players_list(5)
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
        self.assertFalse(contains_duplicates(team0))
        self.assertFalse(contains_duplicates(team1))
        self.assertFalse(contains_duplicates(bench))
        self.assertEqual(0, len(voice_channel_mock.members))
