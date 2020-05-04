from random import randint

from discord.ext import commands

import decorators
from log import LoggerFactory

log = LoggerFactory.get_logger(__name__)


class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="getGiveawayUser")
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def get_giveaway_user_command(self, ctx):
        channel = self.client.get_channel(Config.GIVEAWAY_VOICE_CHANNEL)
        channel_members = channel.members
        log.debug('Empty the list of participants')
        del self.client.global_variables.user_for_giveaway[:]

        log.debug('Add user to [user_for_giveaway]')
        for member in channel_members:
            self.client.global_variables.user_for_giveaway.append(member.id)

        await ctx.send('Loaded ' + str(len(self.client.global_variables.user_for_giveaway)) + ' user for the giveaway')

    @commands.command(name="getGiveawayWinner")
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def get_giveaway_winner_command(self, ctx):
        # get a random number between 0 and the amount of user -1
        random_index = randint(0, len(self.client.global_variables.user_for_giveaway) - 1)
        # create a user object out of the drawn id
        user = self.client.get_user(self.client.global_variables.user_for_giveaway[random_index])
        # remove the player from the giveaway list
        self.client.global_variables.user_for_giveaway.remove(
            self.client.global_variables.user_for_giveaway[random_index])
        # announce the winner
        await ctx.send(user.mention + ' Won!')


def setup(client):
    client.add_cog(Giveaway(client))