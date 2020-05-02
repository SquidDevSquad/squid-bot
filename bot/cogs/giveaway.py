from random import randint

from discord.ext import commands

import file.GlobaleVariables as GlobaleVariables
from file.FileRepository import *


class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="getGiveawayUser")
    async def get_giveaway_user_command(self, ctx):
        if not is_admin(ctx.author.id):
            await ctx.send('You don\'t have the permissions to use this command')
            return
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        channel = self.client.get_channel(Config.GIVEAWAY_VOICE_CHANNEL)
        channel_members = channel.members
        del GlobaleVariables.userForGiveaway[:]

        for member in channel_members:
            GlobaleVariables.userForGiveaway.append(member.id)
        
        await ctx.send('Loaded ' + str(len(GlobaleVariables.userForGiveaway)) + ' user for the giveaway')
    
    @commands.command(name="getGiveawayWinner")
    async def get_giveaway_winner_command(self, ctx):
        if not is_admin(ctx.author.id):
            await ctx.send('You don\'t have the permissions to use this command')
            return
        channel = ctx.message.channel.id
        if not can_operate_in_channel(channel, Config.ALLOWED_CHANNEL):
            await ctx.send('Not allowed to operate here')
            return
        # get a random number between 0 and the amount of user -1
        randomIndex = randint(0, len(GlobaleVariables.userForGiveaway) - 1)
        # create a user object out of the drawn id
        user = self.client.get_user(GlobaleVariables.userForGiveaway[randomIndex])
        # remove the player from the giveaway list
        GlobaleVariables.userForGiveaway.remove(GlobaleVariables.userForGiveaway[randomIndex])
        # announce the winner
        await ctx.send(user.mention + ' Won!')
        




def setup(client):
    client.add_cog(Giveaway(client))