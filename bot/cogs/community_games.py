import discord
from discord.ext import commands

import UserUtils
import decorators
from log import LoggerFactory

log = LoggerFactory.get_logger(__name__)


class CommunityGames(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.file_repository.create_player_file_if_doesnt_exist()

    # TODO Mor: Add tests
    @commands.command(help="Reset all and open team registration", name="open", description='1')
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def open_registration_command(self, ctx):
        if self.client.global_variables.registration_opened:
            log.debug("Registration is already open")
            await ctx.send(ctx.author.mention + " Registrations are already opened")
            return
        log.debug("Empty global variable [bench]")
        self.client.global_variables.bench = list()

        self.client.global_variables.registration_opened = True
        log.info("Activated registration for community games")
        await ctx.send(ctx.author.mention + " Registrations are open")

    @commands.command(help="Close team registration", name="close", description='2')
    @decorators.is_admin
    @decorators.only_allowed_channels
    @decorators.is_registration_open
    async def close_registration_command(self, ctx):
        log.debug("Closed registration for community games")
        self.client.global_variables.registration_opened = False
        await ctx.send(ctx.author.mention + " Registrations are closed")

    # TODO Mor: Add tests
    @commands.command(help="Add a player to the bench", name="addToBench", description='3')
    @decorators.is_admin
    @decorators.only_allowed_channels
    @decorators.is_registration_open
    async def add_to_bench_command(self, ctx, user: discord.Member):
        log.info("Adding %s to bench...", UserUtils.get_nick_or_name(user))
        self.client.global_variables.bench.append(user)
        user_name = UserUtils.get_nick_or_name(user)
        await ctx.send(ctx.author.mention + " User `" + user_name + "` has been added to the bench")

    @commands.command(help="Remove a player from the bench", name="removeFromBench", description='4')
    @decorators.is_admin
    @decorators.only_allowed_channels
    @decorators.is_registration_open
    async def remove_from_bench_command(self, ctx, user: discord.Member):
        log.info("Removing %s from bench...", user.name)
        if user in self.client.global_variables.bench:
            self.client.global_variables.bench.remove(user)
            await ctx.send(ctx.author.mention + " User `" + user.name + "` has been removed from the bench")
        else:
            await ctx.send(ctx.author.mention + " User `" + user.name + "` is not in the bench")

    @commands.command(help="Show a list of players in bench", name="showBench", description='5')
    @decorators.only_allowed_channels
    async def show_bench_command(self, ctx):
        embed = await self.generate_members_in_bench_msg(self.client.global_variables.bench)
        await ctx.send(embed=embed)

    @staticmethod
    async def generate_members_in_bench_msg(bench):
        member_names = '\n'.join([UserUtils.get_nick_or_name(m) for m in bench])
        return discord.Embed(title="{} member(s) in {}".format(len(bench), "Bench"),
                             description=member_names,
                             color=discord.Color.blue())


def setup(client):
    client.add_cog(CommunityGames(client))
