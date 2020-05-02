import discord

import Config

import helper.GlobaleVariables as GlobaleVariables
from helper.Helpers import *

from discord.ext import commands
from random import randrange
from random import randint

class CommunityGamesTeamGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="generateTeams")
    async def generate_teams_command(self, ctx):
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return

        if len(GlobaleVariables.playersList) < 12:
            await ctx.send(ctx.author.mention + ' Not enough player for 2 teams')
            return
        
        del GlobaleVariables.alreadyUsedIndex[:]
        del GlobaleVariables.teams[:]

        self.fill_players_allowed_to_play()

        numberOfPlayersAllowed = len(GlobaleVariables.playersAllowedToPlay)
        if numberOfPlayersAllowed < 12:
            await ctx.send('NO U')
            return

        self.generate_teams()
        await ctx.send(embed=self.generate_team_embed_message(1, GlobaleVariables.teams[0]))
        await ctx.send(embed=self.generate_team_embed_message(2, GlobaleVariables.teams[1]))

            
    def generate_team(self):
        numberOfPlayers = len(GlobaleVariables.playersAllowedToPlay)
        team = list()
        x = 0
        while (x < 6):
            playerIndex = randrange(numberOfPlayers)
            if playerIndex in GlobaleVariables.alreadyUsedIndex:
                continue
            GlobaleVariables.alreadyUsedIndex.append(playerIndex)
            team.append(GlobaleVariables.playersAllowedToPlay[playerIndex])
            x += 1
        return team
    
    def generate_teams(self):
        for x in range(0, 2):
            GlobaleVariables.teams.append(self.generate_team())
    
    def generate_team_embed_message(self, numberOfTeam, team):
        embed = discord.Embed(title="Team " + str(numberOfTeam), color=0x00ff00)
        for x in range(0, len(team)):
            embed.add_field(name="Player " + str(x + 1) + ":", value=team[x], inline=True)
        return embed
    
    def fill_players_allowed_to_play(self):
        if (len(GlobaleVariables.bench) > 0):
            # Get amount of player who have to get benched
            playersToBench = len(GlobaleVariables.bench)

            if len(GlobaleVariables.playersAllowedToPlay) < 12:
                print('Less than 12 players')
                missingPlayer = 12 - len(GlobaleVariables.playersAllowedToPlay)
                playersToBench = playersToBench - missingPlayer

            tempBench = list()
            tempUsedIndex = list()

            x = 0
            while x < playersToBench:
                playerIndexToRemove = randint(0, len(GlobaleVariables.playersAllowedToPlay) - 1)                

                # Redraw if user is already in temp bench
                if playerIndexToRemove in tempUsedIndex:
                    print('Index already used')
                    continue;
                
                playerName = GlobaleVariables.playersAllowedToPlay[playerIndexToRemove]

                if not playerName in GlobaleVariables.playersList:
                    print('Player not registered anymore')
                    continue;

                # Add index to used indexes
                tempUsedIndex.append(playerIndexToRemove)
                # Add player to the temporary bench list
                tempBench.append(GlobaleVariables.playersAllowedToPlay[playerIndexToRemove])
                x = x + 1

            # Empty list of benched players
            del GlobaleVariables.bench[:]
            # Removed all indexes which were used
            del tempUsedIndex[:]
            # Empty list of player who are allowed to play
            del GlobaleVariables.playersAllowedToPlay[:]

            playersAllowedToPlayAmount = len(GlobaleVariables.playersList) - len(tempBench)

            x = 0
            while x < playersAllowedToPlayAmount:
                allowedToPlayIndex = randint(0, len(GlobaleVariables.playersList) - 1)
                if allowedToPlayIndex in tempUsedIndex:
                    continue
                
                playerName = GlobaleVariables.playersList[allowedToPlayIndex]
                if playerName in GlobaleVariables.bench:
                    continue
                
                tempUsedIndex.append(allowedToPlayIndex)
                GlobaleVariables.playersAllowedToPlay.append(playerName)
                x = x + 1
            

            for benched in tempBench:
                GlobaleVariables.bench.append(benched)
            
            del tempBench[:]

        else:
            playersToBench = len(GlobaleVariables.playersList) - 12
            usedIndex = list()
            x = 0
            while (x < playersToBench):
                playerToRemoveIndex = randrange(playersToBench)
                if playerToRemoveIndex in usedIndex:
                    continue
                GlobaleVariables.bench.append(GlobaleVariables.playersList[playerToRemoveIndex])
                usedIndex.append(playerToRemoveIndex)
                x += 1
            for x in range(0, len(GlobaleVariables.playersList)):
                if x in usedIndex:
                    continue
                GlobaleVariables.playersAllowedToPlay.append(GlobaleVariables.playersList[x])


def setup(client):
    client.add_cog(CommunityGamesTeamGenerator(client))