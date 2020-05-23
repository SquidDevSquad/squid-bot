from random import randint
from random import randrange

import discord
from discord.ext import commands

import decorators
from log import LoggerFactory

log = LoggerFactory.get_logger(__name__)


class CommunityGamesTeamGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="generateTeams")
    @decorators.only_allowed_channels
    async def generate_teams_command(self, ctx):
        log.info("Generating teams...")

        number_of_players = len(self.client.global_variables.players_list)

        log.info("Current amount of players: " + str(number_of_players))

        if number_of_players < 12:
            error_msg = get_not_enough_players_msg(number_of_players)
            log.error(error_msg)
            await ctx.send(ctx.author.mention + error_msg)
            return

        log.debug("Delete globale variable [already_used_index]")
        del self.client.global_variables.already_used_index[:]
        log.debug("Delete globale variable [teams]")
        del self.client.global_variables.teams[:]

        self.fill_players_allowed_to_play()

        number_of_players_allowed = len(
            self.client.global_variables.players_allowed_to_play
        )
        if number_of_players_allowed < 12:
            error_msg = get_not_enough_players_msg(number_of_players_allowed)
            await ctx.send(error_msg)
            return

        self.generate_teams()
        await ctx.send(
            embed=self.generate_team_embed_message(
                1, self.client.global_variables.teams[0]
            )
        )
        await ctx.send(
            embed=self.generate_team_embed_message(
                2, self.client.global_variables.teams[1]
            )
        )

    def generate_team(self):
        log.debug("Start generating teams")
        number_of_players = len(self.client.global_variables.players_allowed_to_play)
        team = list()
        x = 0
        while x < 6:
            player_index = randrange(number_of_players)
            if player_index in self.client.global_variables.already_used_index:
                log.debug("Index already used")
                continue
            self.client.global_variables.already_used_index.append(player_index)
            log.debug(
                "Add player to the team: "
                + self.client.global_variables.players_allowed_to_play[player_index]
            )
            team.append(
                self.client.global_variables.players_allowed_to_play[player_index]
            )
            x += 1
        return team

    def generate_teams(self):
        for x in range(0, 2):
            self.client.global_variables.teams.append(self.generate_team())


    def generate_team_embed_message(self, number_of_team, team):
        embed = discord.Embed(title="Team " + str(number_of_team), color=0x00FF00)
        for x in range(0, len(team)):
            embed.add_field(
                name="Player " + str(x + 1) + ":", value=team[x], inline=True
            )
        return embed

    def fill_players_allowed_to_play(self):
        log.debug("Start filling allowed players")
        if len(self.client.global_variables.bench) > 0:
            log.debug("Already benched players")
            # Get amount of player who have to get benched
            players_to_bench = len(self.client.global_variables.bench)
            log.debug("Amount of player to bench: " + str(players_to_bench))

            if len(self.client.global_variables.players_allowed_to_play) < 12:
                log.debug("Less than 12 players")
                missing_player = 12 - len(
                    self.client.global_variables.players_allowed_to_play
                )
                log.debug("Amount of missing player: " + str(missing_player))
                players_to_bench = players_to_bench - missing_player
                log.debug("New amount of player to bench: " + str(players_to_bench))

            log.debug("Create temp bench")
            temp_bench = list()
            log.debug("Create temp used index")
            temp_used_index = list()

            log.debug("Start filling temp bench")
            x = 0
            while x < players_to_bench:
                player_index_to_remove = randint(
                    0, len(self.client.global_variables.players_allowed_to_play) - 1
                )
                log.debug("Try to bench player index: " + str(player_index_to_remove))
                # Redraw if user is already in temp bench
                if player_index_to_remove in temp_used_index:
                    log.debug("Index already used")
                    continue

                player_name = self.client.global_variables.players_allowed_to_play[
                    player_index_to_remove
                ]

                if player_name not in self.client.global_variables.players_list:
                    log.debug("Player not registered anymore: " + player_name)
                    continue

                # Add index to used indexes
                log.debug("Add player index to temp used index")
                temp_used_index.append(player_index_to_remove)
                # Add player to the temporary bench list
                log.debug("Add player name to temp bench")
                temp_bench.append(
                    self.client.global_variables.players_allowed_to_play[
                        player_index_to_remove
                    ]
                )
                x = x + 1

            # Empty list of benched players
            log.debug("Empty globale variable [bench]")
            del self.client.global_variables.bench[:]
            # Removed all indexes which were used
            log.debug("Empty variable [temp_used_index]")
            del temp_used_index[:]
            # Empty list of player who are allowed to play
            log.debug("Empty globale variable [players_allowed_to_play]")
            del self.client.global_variables.players_allowed_to_play[:]

            players_allowed_to_play_amount = len(
                self.client.global_variables.players_list
            ) - len(temp_bench)
            log.debug(
                "Amount of players allowed to play: "
                + str(players_allowed_to_play_amount)
            )

            log.debug("Start filling allowed player")
            x = 0
            while x < players_allowed_to_play_amount:
                allowed_to_play_index = randint(
                    0, len(self.client.global_variables.players_list) - 1
                )
                log.debug("Try to add player index: " + str(allowed_to_play_index))
                if allowed_to_play_index in temp_used_index:
                    log.debug("Index already used")
                    continue

                player_name = self.client.global_variables.players_list[
                    allowed_to_play_index
                ]
                if player_name in self.client.global_variables.bench:
                    log.debug("Player already benched")
                    continue

                log.debug("Add player index to temp used index")
                temp_used_index.append(allowed_to_play_index)
                log.debug("Add player to the allowed to play list: " + player_name)
                self.client.global_variables.players_allowed_to_play.append(player_name)
                x = x + 1

            log.debug("Fill in benched with temp_bench")
            for benched in temp_bench:
                self.client.global_variables.bench.append(benched)

            log.debug("Empty variable [temp_bench]")
            del temp_bench[:]

        else:
            log.debug("No benched player")
            players_to_bench = len(self.client.global_variables.players_list) - 12
            log.debug("Amount of player to bench: " + str(players_to_bench))
            used_index = list()
            x = 0
            log.debug("Start benching player")
            while x < players_to_bench:
                player_to_remove_index = randrange(players_to_bench)
                if player_to_remove_index in used_index:
                    log.debug("Index already used")
                    continue
                self.client.global_variables.bench.append(
                    self.client.global_variables.players_list[player_to_remove_index]
                )
                used_index.append(player_to_remove_index)
                x += 1
            log.debug("Start adding allowed player")
            for x in range(0, len(self.client.global_variables.players_list)):
                if x in used_index:
                    log.debug("Index already used")
                    continue
                self.client.global_variables.players_allowed_to_play.append(
                    self.client.global_variables.players_list[x]
                )


def setup(client):
    client.add_cog(CommunityGamesTeamGenerator(client))


def get_not_enough_players_msg(current_number_of_players):
    return (
        " Not enough players for 2 teams. Currently have: {currentNumberOfPlayers}. "
        "At least 12 players needed.".format(
            currentNumberOfPlayers=current_number_of_players
        )
    )
