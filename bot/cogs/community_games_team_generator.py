from random import randrange

import discord
from discord.ext import commands

import Config
import decorators
from log import LoggerFactory
from utils import ListUtils
from utils import UserUtils

log = LoggerFactory.get_logger(__name__)


class CommunityGamesTeamGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="generateTeams", aliases=["gt"])
    @decorators.is_admin
    @decorators.only_allowed_channels
    @decorators.is_registration_open
    async def generate_teams_command(self, ctx):
        self.client.global_variables.teams = list()
        self.client.global_variables.spectators = list()
        teams = self.client.global_variables.teams
        teams.append(list())
        teams.append(list())

        bench = self.client.global_variables.bench

        log.info("Generating teams...")
        voice_channel = ListUtils.find_by_id(Config.COMMUNITY_GAMES_VOICE_CHANNEL, ctx.guild.voice_channels)
        members = voice_channel.members

        self.client.global_variables.spectators = UserUtils.filter_spectators(members)
        spectators = self.client.global_variables.spectators
        log.info("Spectator players:%s", UserUtils.print_players(spectators))

        log.debug("Removing spectators: %s from player pool: %s", UserUtils.print_players(spectators),
                  UserUtils.print_players(members))
        UserUtils.remove_players_from_list(spectators, members)
        log.debug("Player pool after removing spectators: %s", UserUtils.print_players(members))

        log.debug("Removing spectators: %s from player bench: %s", UserUtils.print_players(spectators),
                  UserUtils.print_players(bench))
        UserUtils.remove_players_from_list(spectators, bench)
        log.debug("Bench pool after removing spectators: %s", UserUtils.print_players(bench))

        num_of_players = len(members)

        await ctx.send(embed=(UserUtils.generate_player_list_embed(members, voice_channel.name)))
        if spectators:
            await ctx.send(embed=UserUtils.generate_player_list_embed(spectators, "Spectators"))

        log.info("Current number of players: " + str(num_of_players))

        if num_of_players < 12:
            error_msg = self.get_not_enough_players_msg(num_of_players)
            log.error(error_msg)
            await ctx.send(ctx.author.mention + error_msg)
            return

        UserUtils.remove_players_from_list(bench, members)
        log.info("Adding previously benched players to teams:%s", UserUtils.print_players(bench))
        self.generate_teams(bench)
        log.info("Adding players from players pool to teams:%s", UserUtils.print_players(members))
        self.generate_teams(members)

        log.info("Adding unselected players to bench:%s", UserUtils.print_players(members))
        ListUtils.add_to_list(bench, members)
        bench = ListUtils.remove_duplicates(bench)
        members.clear()

        team0 = teams[0]
        team1 = teams[1]

        log.info("Teams generated are: "
                 "\n Team 1: %s "
                 "\n Team 2: %s",
                 UserUtils.print_players(team0),
                 UserUtils.print_players(team1)
                 )

        await ctx.send(embed=self.generate_team_embed_message(1, team0))
        await ctx.send(embed=self.generate_team_embed_message(2, team1))
        await ctx.send(embed=UserUtils.generate_player_list_embed(bench, "Bench"))

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
            "At least 12 players needed.".format(currentNumberOfPlayers=current_number_of_players)
        )


def setup(client):
    client.add_cog(CommunityGamesTeamGenerator(client))
