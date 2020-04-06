import discord

import helper.GlobaleVariables as GlobaleVariables

from discord.ext import commands
from random import randrange

class CommunityGamesTeamGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="test")
    async def test_command(self, ctx):
        if GlobaleVariables.registrationOpened:
            await ctx.send(ctx.author.mention + " Registrations open you can register now")
        else:
            await ctx.send(ctx.author.mention + " Registrations closed you can't register now")

    @commands.command(name="generateTeams")
    async def generate_teams_command(self, ctx):
        if len(GlobaleVariables.playersList) < 12:
            await ctx.send(ctx.author.mention + ' Not enough player for 2 teams')
            return
        
        del GlobaleVariables.alreadyUsedIndex[:]
        del GlobaleVariables.teams[:]

        self.fill_players_allowed_to_play()
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
        print(team)
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
            playerToBench = len(GlobaleVariables.bench)
            tempBench = list()

            for benched in range(0, playerToBench):
                playerIndexToRemove = randrange(len(GlobaleVariables.playersAllowedToPlay))
                tempBench.append(GlobaleVariables.playersAllowedToPlay[playerIndexToRemove])
            
            for i in range(0, playerToBench):
                GlobaleVariables.playersAllowedToPlay.append(GlobaleVariables.bench[i])
            
            del GlobaleVariables.bench[:]

            for x in range(0, len(tempBench)):
                GlobaleVariables.bench.append(tempBench[x])
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