from random import randint

import discord
from discord.ext import commands

import decorators


class CommunityGamesMapGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.file_repository.create_map_file_if_doesnt_exist()

    @commands.command(name="addMap", description='1')
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def add_map_command(self, ctx, map_name):
        self.client.file_repository.add_map_to_file(map_name)
        await ctx.send(
            ctx.author.mention + " " + map_name + " was registered to the pool."
        )

    @commands.command(name="getMaps", description='2')
    @decorators.only_allowed_channels
    async def get_maps_command(self, ctx):
        maps = self.client.file_repository.get_maps_from_file()

        if len(maps) == 0:
            await ctx.send("No maps to show")
            return

        embed = discord.Embed(title="Maps", color=0x12FF32)
        for x in range(0, len(maps)):
            embed.add_field(name="Map " + str(x + 1) + ":", value=maps[x])
        await ctx.send(embed=embed)

    @commands.command(name="getRandomMap", description='3')
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def get_random_map_command(self, ctx):
        maps = self.client.file_repository.get_maps_from_file()

        if len(maps) == len(self.client.global_variables.used_maps):
            await ctx.send("All maps are used up. You need to reset the maps first")
            return

        random_map = self.get_random_map(maps)
        while random_map in self.client.global_variables.used_maps:
            random_map = self.get_random_map(maps)
        self.client.global_variables.used_maps.append(random_map)
        await ctx.send(random_map)

    @commands.command(name="resetMaps", description='4')
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def reset_maps_command(self, ctx):
        del self.client.global_variables.used_maps[:]

    @commands.command(name="getUsedMaps", description='5')
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def get_used_maps_command(self, ctx):
        await ctx.send(self.client.global_variables.used_maps)

    @commands.command(name="removeMap", description='6')
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def remove_map_command(self, ctx, map_name):
        self.client.file_repository.remove_map_from_list(map_name)
        self.client.global_variables.used_maps.remove(map_name)
        await ctx.send(
            ctx.author.mention + " " + map_name + " got removed from the list"
        )

    @staticmethod
    def get_random_map(maps):
        random_index = randint(0, len(maps) - 1)
        return maps[random_index]


def setup(client):
    client.add_cog(CommunityGamesMapGenerator(client))
