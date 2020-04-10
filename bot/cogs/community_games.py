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
        if not is_admin(ctx.author.id):
            await ctx.send('You don\'t have the permissions to use this command')
            return
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
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
        if not is_admin(ctx.author.id):
            await ctx.send('You don\'t have the permissions to use this command')
            return
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        if not GlobaleVariables.registrationOpened:
            await ctx.send(ctx.author.mention + ' Registrations are already closed')
            return
        GlobaleVariables.registrationOpened = False
        await ctx.send(ctx.author.mention + ' Registrations are closed')

    @commands.command(name="register")
    async def register_player_name_command(self, ctx, ingameName):
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        userId = ctx.author.id
        if (user_exists_in_file(userId)):
            registeredName = get_ingame_name_by_id(userId)
            await ctx.send(ctx.author.mention + ' You are already registerd with the name ' + registeredName)
            return
        
        write_player_data_to_file(userId, ingameName)
        await ctx.send('Successfully registered ' + ctx.author.mention + ' with username ' + ingameName)


    @commands.command(name="add")
    async def add_participant_command(self, ctx):
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return

        if not GlobaleVariables.registrationOpened:
            await ctx.send(ctx.author.mention + ' Registrations are not opened yet')
            return

        playerName = get_ingame_name_by_id(ctx.author.id)

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
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        ingameName = get_ingame_name_by_id(ctx.author.id)

        if ingameName in GlobaleVariables.playersList:
            GlobaleVariables.playersList.remove(ingameName)
        if ingameName in GlobaleVariables.bench:
            GlobaleVariables.bench.remove(ingameName)
        if ingameName in GlobaleVariables.playersAllowedToPlayer:
            GlobaleVariables.playersAllowedToPlayer.remove(ingameName)

        await ctx.send(ctx.author.mention + ' Removed you from the list of participants')

    @commands.command(name="participants")
    async def show_participants_command(self, ctx):
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        embed = discord.Embed(title="Participants", color=0x00ff00)
        for x in range(0, len(GlobaleVariables.playersList)):
            embed.add_field(name="Player " + str(x + 1) + ":", value=GlobaleVariables.playersList[x], inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name="addUser")
    async def add_user_command(self, ctx, user : discord.User):
        if not is_admin(ctx.author.id):
            await ctx.send('You don\'t have the permissions to use this command')
            return
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return

        if not GlobaleVariables.registrationOpened:
            await ctx.send(ctx.author.mention + ' Registrations are not opened yet')
            return
        

        userId = user.id
        playerName = get_ingame_name_by_id(userId)
        if not playerName:
            await ctx.send(ctx.author.mention + ' You are not registered with an ingame character. Please use the `' + Config.COMMAND_PREFIX + 'register USERNAME` command.')
            return

        if playerName in GlobaleVariables.bench or playerName in GlobaleVariables.playersList:
            await ctx.send(ctx.author.mention + ' You are already registered for the community games')
            return
        
        GlobaleVariables.playersList.append(playerName)

        await ctx.send(ctx.author.mention + ' You registered ' + user.name + ' for the community games')
    
    @commands.command(name="removeUser")
    async def remove_user_command(self, ctx, user : discord.User):
        if not is_admin(ctx.author.id):
            await ctx.send('You don\'t have the permissions to use this command')
            return
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        
        ingameName = get_ingame_name_by_id(user.id)

        if ingameName in GlobaleVariables.playersList:
            GlobaleVariables.playersList.remove(ingameName)
        if ingameName in GlobaleVariables.bench:
            GlobaleVariables.bench.remove(ingameName)
        if ingameName in GlobaleVariables.playersAllowedToPlayer:
            GlobaleVariables.playersAllowedToPlayer.remove(ingameName)
        
        await ctx.send(ctx.author.mention + ' Removed ' + user.name +' from the list of participants')

    @commands.command(name="registerUser")
    async def register_user_command(self, ctx, user : discord.User, ingameName):
        if not is_admin(ctx.author.id):
            await ctx.send('You don\'t have the permissions to use this command')
            return
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        userId = user.id
        if (user_exists_in_file(userId)):
            registeredName = get_ingame_name_by_id(userId)
            await ctx.send(ctx.author.mention + ' You are already registerd with the name ' + registeredName)
            return
        
        write_player_data_to_file(userId, ingameName)
        await ctx.send('Successfully registered ' + user.name + ' with username ' + ingameName)


def setup(client):
    client.add_cog(CommunityGames(client))