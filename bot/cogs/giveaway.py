from random import randint

import discord
from discord.ext import commands

import Config
import decorators
from log import LoggerFactory
from utils import ListUtils

log = LoggerFactory.get_logger(__name__)


# TODO Mor: Add tests
class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    # TODO Mor: Remove this and docs
    # @commands.command(name="getGiveawayUser")
    # @decorators.is_admin
    # @decorators.only_allowed_channels
    # async def get_giveaway_user_command(self, ctx):
    #
    #     log.debug("Empty the list of participants")
    #     del self.client.global_variables.user_for_giveaway[:]
    #
    #     log.debug("Add user to [user_for_giveaway]")
    #     for member in channel_members:
    #         self.client.global_variables.user_for_giveaway.append(member.id)
    #
    #     await ctx.send(
    #         "Loaded "
    #         + str(len(self.client.global_variables.user_for_giveaway))
    #         + " users for the giveaway"
    #     )

    @commands.command(name="getGiveawayWinner")
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def get_giveaway_winner_command(self, ctx):
        winners = self.client.global_variables.giveaway_winners
        channel = self.client.get_channel(Config.GIVEAWAY_VOICE_CHANNEL_ID)
        channel_members = channel.members
        contenders = ListUtils.remove_sub_list(channel_members, winners)
        if not contenders:
            await ctx.send(embed=discord.Embed(title="Squid Squad Community Games Giveaway",
                                               description="No contenders!",
                                               color=discord.Color.blue()))
            return

        random_index = randint(0, len(contenders) - 1)

        new_winner = contenders[random_index]
        winners.append(new_winner)
        await ctx.send(embed=discord.Embed(title="Squid Squad Community Games Giveaway",
                                           description="And the winner is ... " + new_winner.mention + "!",
                                           color=discord.Color.blue()))


def setup(client):
    client.add_cog(Giveaway(client))
