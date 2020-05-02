from random import randint

import discord
from discord.ext import commands

import file.GlobaleVariables as GlobaleVariables
from file.FileRepository import *


class CommunityGamesMapGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        create_mapfile_if_doesnt_exist()

    @commands.command(name="addMap")
    async def add_map_command(self, ctx, mapName):
        if not is_admin(ctx.author.id):
            await ctx.send('You don\'t have the permissions to use this command')
            return
        if is_map_already_registered(mapName):
            await ctx.send(ctx.author.mention + " the map " + mapName + " is already registered.")
            return
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return

        add_map_to_file(mapName)
        await ctx.send(ctx.author.mention + mapName + " was registered to the pool.")
    
    @commands.command(name="getMaps")
    async def get_maps_command(self, ctx):
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        maps = get_maps_from_file()

        if len(maps) == 0:
            await ctx.send('No maps to show')
            return

        embed = discord.Embed(title="Maps", color=0x12ff32)
        for x in range(0, len(maps)):
            embed.add_field(name="Map " + str(x + 1) + ":", value=maps[x])
        await ctx.send(embed=embed)

    @commands.command(name="getRandomMap")
    async def get_random_map_command(self, ctx):
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        maps = get_maps_from_file()

        if (len(maps) == len(GlobaleVariables.usedMaps)):
            await ctx.send("All maps are used up. You need to reset the maps first")
            return

        map = self.get_random_map(maps)
        while map in GlobaleVariables.usedMaps:
            map = self.get_random_map(maps)
        GlobaleVariables.usedMaps.append(map)
        await ctx.send(map)
    
    @commands.command(name="resetMaps")
    async def reset_maps_command(self, ctx):
        if not is_admin(ctx.author.id):
            await ctx.send('You don\'t have the permissions to use this command')
            return
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        del GlobaleVariables.usedMaps[:]
    
    @commands.command(name="getUsedMaps")
    async def get_used_maps_command(self, ctx):
        if not is_admin(ctx.author.id):
            await ctx.send('You don\'t have the permissions to use this command')
            return
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        await ctx.send(GlobaleVariables.usedMaps)
    
    @commands.command(name="removeMap")
    async def remove_map_command(self, ctx, mapName):
        if not is_admin(ctx.author.id):
            await ctx.send('You don\'t have the permissions to use this command')
            return
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        remove_map_from_list(mapName)
        GlobaleVariables.usedMaps.remove(mapName)
        await ctx.send(ctx.author.mention + " " + mapName + " got removed from the list")
        
    
    def get_random_map(self, maps):
        randomIndex = randint(0, len(maps) - 1)
        return maps[randomIndex]

def setup(client):
    client.add_cog(CommunityGamesMapGenerator(client))