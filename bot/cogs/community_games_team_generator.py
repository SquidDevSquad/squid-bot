from random import randint
from random import randrange

import discord
from discord.ext import commands

import GlobalVariables as GlobalVariables
from file.FileRepository import *
from log import LoggerFactory

log = LoggerFactory.get_logger(__name__)


class CommunityGamesTeamGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="generateTeams")
    async def generate_teams_command(self, ctx):
        log.info('Generating teams...')
        channel = ctx.message.channel.id
        log.info('Current channels are:%s. Allowed Channels are:%s', channel, Config.ALLOWED_CHANNEL)
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            log.error("Cannot generate teams in any of the current channels. Aborting.")
            await ctx.send('Not allowed to operate on this channel')
            return

        number_of_players = len(GlobalVariables.playersList)

        if number_of_players < 12:
            error_msg = get_not_enough_players_msg(number_of_players)
            log.error(error_msg)
            await ctx.send(ctx.author.mention + error_msg)
            return

        del GlobalVariables.alreadyUsedIndex[:]
        del GlobalVariables.teams[:]

        self.fill_players_allowed_to_play()

        number_of_players_allowed = len(GlobalVariables.playersAllowedToPlay)
        if number_of_players_allowed < 12:
            error_msg = get_not_enough_players_msg(number_of_players_allowed)
            await ctx.send(error_msg)
            return

        self.generate_teams()
        await ctx.send(embed=self.generate_team_embed_message(1, GlobalVariables.teams[0]))
        await ctx.send(embed=self.generate_team_embed_message(2, GlobalVariables.teams[1]))

    def generate_team(self):
        number_of_players = len(GlobalVariables.playersAllowedToPlay)
        team = list()
        x = 0
        while x < 6:
            player_index = randrange(number_of_players)
            if player_index in GlobalVariables.alreadyUsedIndex:
                continue
            GlobalVariables.alreadyUsedIndex.append(player_index)
            team.append(GlobalVariables.playersAllowedToPlay[player_index])
            x += 1
        return team

    def generate_teams(self):
        for x in range(0, 2):
            GlobalVariables.teams.append(self.generate_team())

    def generate_team_embed_message(self, number_of_team, team):
        embed = discord.Embed(title="Team " + str(number_of_team), color=0x00ff00)
        for x in range(0, len(team)):
            embed.add_field(name="Player " + str(x + 1) + ":", value=team[x], inline=True)
        return embed

    def fill_players_allowed_to_play(self):
        if (len(GlobalVariables.bench) > 0):
            # Get amount of player who have to get benched
            playersToBench = len(GlobalVariables.bench)

            if len(GlobalVariables.playersAllowedToPlay) < 12:
                print('Less than 12 players')
                missingPlayer = 12 - len(GlobalVariables.playersAllowedToPlay)
                playersToBench = playersToBench - missingPlayer

            tempBench = list()
            tempUsedIndex = list()

            x = 0
            while x < playersToBench:
                playerIndexToRemove = randint(0, len(GlobalVariables.playersAllowedToPlay) - 1)

                # Redraw if user is already in temp bench
                if playerIndexToRemove in tempUsedIndex:
                    print('Index already used')
                    continue;

                playerName = GlobalVariables.playersAllowedToPlay[playerIndexToRemove]

                if not playerName in GlobalVariables.playersList:
                    print('Player not registered anymore')
                    continue;

                # Add index to used indexes
                tempUsedIndex.append(playerIndexToRemove)
                # Add player to the temporary bench list
                tempBench.append(GlobalVariables.playersAllowedToPlay[playerIndexToRemove])
                x = x + 1

            # Empty list of benched players
            del GlobalVariables.bench[:]
            # Removed all indexes which were used
            del tempUsedIndex[:]
            # Empty list of player who are allowed to play
            del GlobalVariables.playersAllowedToPlay[:]

            playersAllowedToPlayAmount = len(GlobalVariables.playersList) - len(tempBench)

            x = 0
            while x < playersAllowedToPlayAmount:
                allowedToPlayIndex = randint(0, len(GlobalVariables.playersList) - 1)
                if allowedToPlayIndex in tempUsedIndex:
                    continue

                playerName = GlobalVariables.playersList[allowedToPlayIndex]
                if playerName in GlobalVariables.bench:
                    continue

                tempUsedIndex.append(allowedToPlayIndex)
                GlobalVariables.playersAllowedToPlay.append(playerName)
                x = x + 1

            for benched in tempBench:
                GlobalVariables.bench.append(benched)

            del tempBench[:]

        else:
            playersToBench = len(GlobalVariables.playersList) - 12
            usedIndex = list()
            x = 0
            while (x < playersToBench):
                playerToRemoveIndex = randrange(playersToBench)
                if playerToRemoveIndex in usedIndex:
                    continue
                GlobalVariables.bench.append(GlobalVariables.playersList[playerToRemoveIndex])
                usedIndex.append(playerToRemoveIndex)
                x += 1
            for x in range(0, len(GlobalVariables.playersList)):
                if x in usedIndex:
                    continue
                GlobalVariables.playersAllowedToPlay.append(GlobalVariables.playersList[x])


def setup(client):
    client.add_cog(CommunityGamesTeamGenerator(client))


def get_not_enough_players_msg(current_number_of_players):
    return ' Not enough players for 2 teams. Currently have: {currentNumberOfPlayers}. ' \
           'At least 12 players needed.'.format(currentNumberOfPlayers=current_number_of_players)
