import discord

import Config
import helper.GlobaleVariables as GlobaleVariables
from helper.Helpers import *

from discord.ext import commands

class CommunityGames(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        create_playerfile_if_doesnt_exist()

    @commands.command(name="open")
    async def open_registration_command(self, ctx):
        if GlobaleVariables.registrationOpened:
            await ctx.send(ctx.author.mention + ' Registrations are already opened')
            return
        
        del GlobaleVariables.playersList[:]
        del GlobaleVariables.bench[:]
        del GlobaleVariables.teams[:]
        del GlobaleVariables.playersAllowedToPlayer[:]
        del GlobaleVariables.alreadyUsedIndex[:]

        GlobaleVariables.registrationOpened = True
        await ctx.send(ctx.author.mention + ' Registrations are opened')

    @commands.command(name="close")
    async def close_registration_command(self, ctx):
        if not GlobaleVariables.registrationOpened:
            await ctx.send(ctx.author.mention + ' Registrations are already closed')
            return
        GlobaleVariables.registrationOpened = False
        await ctx.send(ctx.author.mention + ' Registrations are closed')

    @commands.command(name="register")
    async def register_player_name_command(self, ctx, ingameName):
        if (user_exists_in_file(ctx.author.name)):
            registeredName = get_ingame_name_by_user(ctx.author.name)
            await ctx.send(ctx.author.mention + ' You are already registerd with the name ' + registeredName)
            return
        write_player_data_to_file(ctx.author.name, ingameName)
        await ctx.send('Successfully registered ' + ctx.author.mention + ' with username ' + ingameName)


    @commands.command(name="add")
    async def add_participant_command(self, ctx):
        if not GlobaleVariables.registrationOpened:
            await ctx.send(ctx.author.mention + ' Registrations are not opened yet')
            return

        playerName = get_ingame_name_by_user(ctx.author.name)

        if not playerName:
            await ctx.send(ctx.author.mention + ' You are not registered with an ingame character. Please use the `' + Config.COMMAND_PREFIX + 'register USERNAME` command.')
            return

        if playerName in GlobaleVariables.bench or playerName in GlobaleVariables.playersList:
            await ctx.send(ctx.author.mention + ' You are already registered for the community games')
            return
        
        GlobaleVariables.playersList.append(playerName)

        await ctx.send(ctx.author.mention + ' You are now registered for the community games')
    
    @commands.command(name="remove")
    async def remove_participant_command(self, ctx):
        ingameName = get_ingame_name_by_user(ctx.author.name)

        if ingameName in GlobaleVariables.playersList:
            GlobaleVariables.playersList.remove(ingameName)
        if ingameName in GlobaleVariables.bench:
            GlobaleVariables.bench.remove(ingameName)
        if ingameName in GlobaleVariables.playersAllowedToPlayer:
            GlobaleVariables.playersAllowedToPlayer.remove(ingameName)

        await ctx.send(ctx.author.mention + ' Removed you from the list of participants')

    @commands.command(name="participants")
    async def show_participants_command(self, ctx):
        embed = discord.Embed(title="Participants", color=0x00ff00)
        for x in range(0, len(GlobaleVariables.playersList)):
            embed.add_field(name="Player " + str(x + 1) + ":", value=GlobaleVariables.playersList[x], inline=True)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(reaction.emoji)
    



def setup(client):
    client.add_cog(CommunityGames(client))