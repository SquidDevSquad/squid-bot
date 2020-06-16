from random import randrange

import discord
from discord.ext import commands

import Config as Config
import UserUtils
import decorators
from log import LoggerFactory

log = LoggerFactory.get_logger(__name__)


def print_players(players):
    if len(players) > 0:
        return ",".join([x.name for x in players])


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

        log.info("Current amount of players: " + str(num_of_players))

        if num_of_players < 12:
            error_msg = self.get_not_enough_players_msg(num_of_players)
            log.error(error_msg)
            await ctx.send(ctx.author.mention + error_msg)
            return

        bench = self.client.global_variables.bench
        self.remove_benched_players_from_general_list(bench, members)
        log.info("Adding previously benched players to teams:%s", print_players(bench))
        self.generate_teams(bench)
        log.info("Adding players from players pool to teams:%s", print_players(members))
        self.generate_teams(members)

        log.info("Adding unselected players to bench:%s", print_players(members))
        self.add_remaining_players_to_bench(members)
        members.clear()

        team0 = self.client.global_variables.teams[0]
        team1 = self.client.global_variables.teams[1]

        log.info("Teams generated are: "
                 "\n Team 1: %s "
                 "\n Team 2: %s",
                 print_players(team0),
                 print_players(team1)
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
            if player.nick is not None:
                player_name = player.nick
            else:
                player_name = player.name

            embed.add_field(
                name="Player " + str(x + 1) + ":", value=player_name, inline=True
            )
        return embed

    # def fill_players_allowed_to_play(self):
    #     log.debug("Start filling allowed players")
    #     if len(self.client.global_variables.bench) > 0:
    #         log.debug("Already benched players")
    #         # Get amount of player who have to get benched
    #         players_to_bench = len(self.client.global_variables.bench)
    #         log.debug("Amount of player to bench: " + str(players_to_bench))
    #
    #         if len(self.client.global_variables.players_allowed_to_play) < 12:
    #             log.debug("Less than 12 players")
    #             missing_player = 12 - len(
    #                 self.client.global_variables.players_allowed_to_play
    #             )
    #             log.debug("Amount of missing player: " + str(missing_player))
    #             players_to_bench = players_to_bench - missing_player
    #             log.debug("New amount of player to bench: " + str(players_to_bench))
    #
    #         log.debug("Create temp bench")
    #         temp_bench = list()
    #         log.debug("Create temp used index")
    #         temp_used_index = list()
    #
    #         log.debug("Start filling temp bench")
    #         x = 0
    #         while x < players_to_bench:
    #             player_index_to_remove = randint(
    #                 0, len(self.client.global_variables.players_allowed_to_play) - 1
    #             )
    #             log.debug("Try to bench player index: " + str(player_index_to_remove))
    #             # Redraw if user is already in temp bench
    #             if player_index_to_remove in temp_used_index:
    #                 log.debug("Index already used")
    #                 continue
    #
    #             player_name = self.client.global_variables.players_allowed_to_play[
    #                 player_index_to_remove
    #             ]
    #
    #             if player_name not in self.client.global_variables.players_list:
    #                 log.debug("Player not registered anymore: " + player_name)
    #                 continue
    #
    #             # Add index to used indexes
    #             log.debug("Add player index to temp used index")
    #             temp_used_index.append(player_index_to_remove)
    #             # Add player to the temporary bench list
    #             log.debug("Add player name to temp bench")
    #             temp_bench.append(
    #                 self.client.global_variables.players_allowed_to_play[
    #                     player_index_to_remove
    #                 ]
    #             )
    #             x = x + 1
    #
    #         # Empty list of benched players
    #         log.debug("Empty global variable [bench]")
    #         del self.client.global_variables.bench[:]
    #         # Removed all indexes which were used
    #         log.debug("Empty variable [temp_used_index]")
    #         del temp_used_index[:]
    #         # Empty list of player who are allowed to play
    #         log.debug("Empty global variable [players_allowed_to_play]")
    #         del self.client.global_variables.players_allowed_to_play[:]
    #
    #         players_allowed_to_play_amount = len(
    #             self.client.global_variables.players_list
    #         ) - len(temp_bench)
    #         log.debug(
    #             "Amount of players allowed to play: "
    #             + str(players_allowed_to_play_amount)
    #         )
    #
    #         log.debug("Start filling allowed player")
    #         x = 0
    #         while x < players_allowed_to_play_amount:
    #             allowed_to_play_index = randint(
    #                 0, len(self.client.global_variables.players_list) - 1
    #             )
    #             log.debug("Try to add player index: " + str(allowed_to_play_index))
    #             if allowed_to_play_index in temp_used_index:
    #                 log.debug("Index already used")
    #                 continue
    #
    #             player_name = self.client.global_variables.players_list[
    #                 allowed_to_play_index
    #             ]
    #             if player_name in self.client.global_variables.bench:
    #                 log.debug("Player already benched")
    #                 continue
    #
    #             log.debug("Add player index to temp used index")
    #             temp_used_index.append(allowed_to_play_index)
    #             log.debug("Add player to the allowed to play list: " + player_name)
    #             self.client.global_variables.players_allowed_to_play.append(player_name)
    #             x = x + 1
    #
    #         log.debug("Fill in benched with temp_bench")
    #         for benched in temp_bench:
    #             self.client.global_variables.bench.append(benched)
    #
    #         log.debug("Empty variable [temp_bench]")
    #         del temp_bench[:]
    #
    #     else:
    #         log.debug("No benched player")
    #         players_to_bench = len(self.client.global_variables.players_list) - 12
    #         log.debug("Amount of player to bench: " + str(players_to_bench))
    #         used_index = list()
    #         x = 0
    #         log.debug("Start benching player")
    #         while x < players_to_bench:
    #             player_to_remove_index = randrange(players_to_bench)
    #             if player_to_remove_index in used_index:
    #                 log.debug("Index already used")
    #                 continue
    #             self.client.global_variables.bench.append(
    #                 self.client.global_variables.players_list[player_to_remove_index]
    #             )
    #             used_index.append(player_to_remove_index)
    #             x += 1
    #         log.debug("Start adding allowed player")
    #         for x in range(0, len(self.client.global_variables.players_list)):
    #             if x in used_index:
    #                 log.debug("Index already used")
    #                 continue
    #             self.client.global_variables.players_allowed_to_play.append(
    #                 self.client.global_variables.players_list[x]
    #             )

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
