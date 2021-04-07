import string

import discord
from discord.ext import commands

import decorators
from utils import ListUtils

filtered_maps = ['TUTORIAL', 'PRACTICE RANGE', 'ESTÁDIO DAS RÃS', 'VPP GREEN ROOM', 'JUNKENSTEIN\'S REVENGE',
                 'ECOPOINT: ANTARCTICA', 'HORIZON LUNAR COLONY', 'NECROPOLIS', 'BLACK FOREST', 'NEPAL SANCTUM',
                 'CASTILLO', 'SYDNEY HARBOUR ARENA', 'AYUTTHAYA', 'CHÂTEAU GUILLARD', 'PETRA', 'BUSAN STADIUM',
                 ]


def from_json():
    maps = list()
    for i in range(len(maps_json)):
        maps_name = string.capwords(maps_json[i]['name']['en_US'])
        icon_url = maps_json[i]['icon']
        if maps_name.upper() not in filtered_maps:
            maps.append(Map(maps_name, icon_url))
    return ListUtils.remove_duplicates(maps)


# maps_json = requests.get('https://api.overwatchleague.com/maps').json()
maps_json = [
    {
        "guid": "guid",
        "name": {
            "en_US": "Anubis"
        },
        "gameModes": [
            {
                "Id": "string",
                "Name": "string",
                "Key": {
                    "href": "string"
                }
            }
        ],
        "id": "string",
        "icon": "",
        "thumbnail": "string",
        "type": "string"
    }
]


class CommunityGamesMapGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.maps = from_json()

    # TODO Mor: Add tests
    @commands.command(name="getRandomMap", aliases=["grm"], description='1', help='(alias: grm)')
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def get_random_map_command(self, ctx):
        used_maps = self.client.global_variables.used_maps
        if len(self.maps) == len(used_maps):
            await ctx.send(ctx.author.mention + " All maps are used up. You need to reset the maps first")
            return

        random_map = self.get_random_map(self.maps)
        while random_map in used_maps:
            random_map = self.get_random_map(self.maps)
        used_maps.append(random_map)

        embed = discord.Embed(title=random_map.name)
        embed.set_image(url=random_map.icon)
        await ctx.send(embed=embed)

    @commands.command(name="resetUsedMaps", description='2')
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def reset_used_maps_command(self, ctx):
        del self.client.global_variables.used_maps[:]
        await ctx.send(ctx.author.mention + " Used maps list has been reset")

    @commands.command(name="getUsedMaps", description='3')
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def get_used_maps_command(self, ctx):
        await ctx.send(embed=ListUtils.get_embed(self.client.global_variables.used_maps, 'Used Maps'))

    @commands.command(name="removeUsedMap", description='4')
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def remove_map_command(self, ctx, map_name):
        used_maps = self.client.global_variables.used_maps
        map_to_remove = Map.from_name(map_name)
        if map_to_remove not in used_maps:
            await ctx.send(ctx.author.mention + " The map `" + map_name + "` is not in the used maps list")
            return

        used_maps.remove(map_to_remove)
        await ctx.send(ctx.author.mention + " The map `" + map_name + "` was removed from the used maps list")
        await ctx.send(embed=ListUtils.get_embed(used_maps, "Used Maps"))

    @staticmethod
    def get_random_map(maps):
        rand_index = ListUtils.get_rand_index(maps)
        return maps[rand_index]


class Map:
    def __init__(self, name, icon):
        self.name = name
        default_icon = 'https://i.ibb.co/SVYx1Ms/db9-1.jpg'
        self.icon = default_icon if not icon else icon

    @classmethod
    def from_name(cls, name):
        cls.name = name
        return cls(name, '')

    def __key(self):
        return self.name

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Map):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self) -> str:
        return self.name


def setup(client):
    client.add_cog(CommunityGamesMapGenerator(client))
