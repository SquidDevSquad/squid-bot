from random import randrange

import discord
from discord.ext import commands

import Config as Config
import UserUtils
import decorators
from log import LoggerFactory

log = LoggerFactory.get_logger(__name__)


class CommunityGamesTeamGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="generateTeams")
    @decorators.is_admin
    @decorators.only_allowed_channels
    @decorators.is_registration_open
    async def generate_teams_command(self, ctx):
        log.debug("Empty global variable [teams]")
        self.client.global_variables.teams = list()
        self.client.global_variables.teams.append(list())
        self.client.global_variables.teams.append(list())

        log.info("Generating teams...")
        voice_channel = await self.find_community_games_voice_channel(ctx)
        members = voice_channel.members
        num_of_players = len(members)
        embed = await self.generate_members_in_channel_msg(members, num_of_players, voice_channel.name)
        await ctx.send(embed=embed)

        log.info("Current number of players: " + str(num_of_players))

        if num_of_players < 12:
            error_msg = self.get_not_enough_players_msg(num_of_players)
            log.error(error_msg)
            await ctx.send(ctx.author.mention + error_msg)
            return

        bench = self.client.global_variables.bench
        self.remove_benched_players_from_general_list(bench, members)
        log.info("Adding previously benched players to teams:%s", UserUtils.print_players(bench))
        self.generate_teams(bench)
        log.info("Adding players from players pool to teams:%s", UserUtils.print_players(members))
        self.generate_teams(members)

        log.info("Adding unselected players to bench:%s", UserUtils.print_players(members))
        self.add_remaining_players_to_bench(members)
        members.clear()

        team0 = self.client.global_variables.teams[0]
        team1 = self.client.global_variables.teams[1]

        log.info("Teams generated are: "
                 "\n Team 1: %s "
                 "\n Team 2: %s",
                 UserUtils.print_players(team0),
                 UserUtils.print_players(team1)
                 )

        await ctx.send(embed=self.generate_team_embed_message(1, team0))
        await ctx.send(embed=self.generate_team_embed_message(2, team1))

    @staticmethod
    async def find_community_games_voice_channel(ctx):
        return filter(is_community_games_channel, ctx.guild.voice_channels).__next__()

    @staticmethod
    async def generate_members_in_channel_msg(members, num_of_players, voice_channel_name):
        member_names = '\n'.join([UserUtils.get_nick_or_name(m) for m in members])
        return discord.Embed(title="{} member(s) in {}".format(num_of_players, voice_channel_name),
                             description=member_names,
                             color=discord.Color.blue())

    @staticmethod
    def generate_team(members, team):
        while len(members) > 0 and len(team) < 6:
            player_index = randrange(len(members))
            member = members[player_index]
            team.append(member)
            members.remove(member)

    def generate_teams(self, players):
        if len(players) > 0:
            for x in range(2):
                self.generate_team(players, self.client.global_variables.teams[x])

    @staticmethod
    def generate_team_embed_message(number_of_team, team):
        embed = discord.Embed(title="Team " + str(number_of_team), color=0x00FF00)
        for x in range(0, len(team)):
            player = team[x]
            embed.add_field(name="Player " + str(x + 1) + ":", value=UserUtils.get_nick_or_name(player), inline=True)
        return embed

    @staticmethod
    def get_not_enough_players_msg(current_number_of_players):
        return (
            " Not enough players for 2 teams. Currently have: {currentNumberOfPlayers}. "
            "At least 12 players needed.".format(
                currentNumberOfPlayers=current_number_of_players
            )
        )

    def add_remaining_players_to_bench(self, members):
        bench_list = self.client.global_variables.bench
        bench_list.extend(members)
        self.client.global_variables.bench = self.remove_duplicates_from_list(bench_list)

    @staticmethod
    def remove_duplicates_from_list(lst):
        return list(dict.fromkeys(lst))

    @staticmethod
    def remove_benched_players_from_general_list(bench, members):
        for benched_player in bench:
            for player in members:
                if benched_player.id == player.id:
                    members.remove(player)
                    break


def setup(client):
    client.add_cog(CommunityGamesTeamGenerator(client))


def is_community_games_channel(voice_channel):
    return voice_channel.id == Config.COMMUNITY_GAMES_VOICE_CHANNEL
