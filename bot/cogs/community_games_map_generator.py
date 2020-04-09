import discord

from discord.ext import commands
from helper.Helpers import *
from random import randrange
import helper.GlobaleVariables as GlobaleVariables

class CommunityGamesMapGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        create_mapfile_if_doesnt_exist()

    @commands.command(name="addMap")
    async def add_map_command(self, ctx, mapName):
        print(mapName)
        if is_map_already_registered(mapName):
            await ctx.send(ctx.author.mention + " the map " + mapName + " is already registered.")
            return
        add_map_to_file(mapName)
    
    @commands.command(name="getMaps")
    async def get_maps_command(self, ctx):
        maps = get_maps_from_file()
        print(maps)

        if len(maps) == 0:
            await ctx.send('No maps to show')
            return

        embed = discord.Embed(title="Maps", color=0x12ff32)
        for x in range(0, len(maps)):
            embed.add_field(name="Map " + str(x + 1) + ":", value=maps[x])
        await ctx.send(embed=embed)

    @commands.command(name="getRandomMap")
    async def get_random_map_command(self, ctx):
        maps = get_maps_from_file()

        print(len(maps))
        print(len(GlobaleVariables.usedMaps))

        if (len(maps) == len(GlobaleVariables.usedMaps)):
            await ctx.send("All maps are used up. You need to reset the maps first")
            return
        
        map = self.get_random_map(maps)
        while map in GlobaleVariables.usedMaps:
            map = self.get_random_map(maps)
        GlobaleVariables.usedMaps.append(map)
        print(GlobaleVariables.usedMaps)
        await ctx.send(map)
        
    
    def get_random_map(self, maps):
        randomIndex = randrange(0, len(maps) - 1)
        return maps[randomIndex]

        
    
    



def setup(client):
    client.add_cog(CommunityGamesMapGenerator(client))