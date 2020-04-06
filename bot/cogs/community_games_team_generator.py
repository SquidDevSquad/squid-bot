import discord

import helper.GlobaleVariables as GlobaleVariables

from discord.ext import commands

class CommunityGamesTeamGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="test")
    async def test_command(self, ctx):
        if GlobaleVariables.registrationOpened:
            await ctx.send(ctx.author.mention + " Registrations open you can register now")
        else:
            await ctx.send(ctx.author.mention + " Registrations closed you can't register now")
        

def setup(client):
    client.add_cog(CommunityGamesTeamGenerator(client))