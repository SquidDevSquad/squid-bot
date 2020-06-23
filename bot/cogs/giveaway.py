import discord
from discord.ext import commands

import Config
import decorators
from log import LoggerFactory
from utils import ListUtils
from utils import UserUtils

# from utils import TestUtils

log = LoggerFactory.get_logger(__name__)

funny_declare_msgs = [
    "This time it's for sure ... {} !",
    "{} feels like it's your lucky day !",
    "This game is already in your pocket {}",
    "You got this {} ! gg ez",
    "Aaaaaaand is it {} ??? is it ?",
    "I can just feel it's gonna be {} !",
    "Always lucky {}",
    "Crossing my fingers for you {} !",
    "I got a feeling the dice is on your side {} !",
    "Lady luck has a thing for you {}"
]

giveaway_title = "<:happysquid:589960594510184496> Squid Squad Community Games Giveaway " \
                 "<:happysquid:589960594510184496> "

giveaway_desc = "{} \n {} \n\n\nAnd the winner is ... {} ! \n Congratulations !!! 🥳 🥳 🥳"


# TODO Mor: Add tests
class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="giveaway")
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def get_giveaway_winner_command(self, ctx):
        winners = self.client.global_variables.giveaway_winners
        channel = self.client.get_channel(Config.GIVEAWAY_VOICE_CHANNEL_ID)
        channel_members = channel.members

        # channel_members = TestUtils.generate_players_list(14)
        # spectators = TestUtils.generate_players_list(3, UserUtils.IDLE)
        # channel_members.extend(spectators)

        prev_winners_msg = self.generate_prev_winners_msg(winners)
        contenders = ListUtils.remove_sub_list(channel_members, winners)
        if not contenders:
            await ctx.send(embed=discord.Embed(title=giveaway_title,
                                               description=prev_winners_msg + '\n' + "No contenders!",
                                               color=discord.Color.blue()))
            return

        player_lottery_msg = self.generate_players_lottery_msg(self, contenders)

        random_index = ListUtils.get_rand_index(contenders)
        new_winner = contenders[random_index]
        winners.append(new_winner)
        await ctx.send(embed=discord.Embed(title=giveaway_title,
                                           description=giveaway_desc.format(prev_winners_msg, player_lottery_msg,
                                                                            new_winner.mention),
                                           # description=prev_winners_msg + '\n' +
                                           #             player_lottery_msg + "\n\n\nAnd the winner is ... " +
                                           #             new_winner.mention + "!" + "\n Congratulations !!! 🥳 🥳 🥳",
                                           color=discord.Color.blue()))

    @staticmethod
    def generate_players_lottery_msg(self, players):
        return 'Contenders:\n' + '\n'.join(
            [self.get_rand_declare_msg().format(UserUtils.get_nick_or_name(player)) for
             player in players])

    @staticmethod
    def generate_prev_winners_msg(winners):
        if not winners:
            return ''

        return 'Previous giveaway winners:\n' + '\n'.join(
            [UserUtils.get_nick_or_name(winner) for
             winner in winners]) + '\n'

    @staticmethod
    def get_rand_declare_msg():
        index = ListUtils.get_rand_index(funny_declare_msgs)
        return funny_declare_msgs[index]


def setup(client):
    client.add_cog(Giveaway(client))
