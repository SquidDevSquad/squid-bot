import discord
from discord.ext import commands

import Config as Config
import decorators
from log import LoggerFactory

log = LoggerFactory.get_logger(__name__)


class CommunityGames(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.file_repository.create_player_file_if_doesnt_exist()

    @commands.command(name="open")
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def open_registration_command(self, ctx):
        if self.client.global_variables.registration_opened:
            log.debug('Registration is already open')
            await ctx.send(ctx.author.mention + ' Registrations are already opened')
            return

        log.debug('Empty global variable [players_list]')
        del self.client.global_variables.players_list[:]
        log.debug('Empty global variable [bench]')
        del self.client.global_variables.bench[:]
        log.debug('Empty global variable [teams]')
        del self.client.global_variables.teams[:]
        log.debug('Empty global variable [players_allowed_to_play]')
        del self.client.global_variables.players_allowed_to_play[:]
        log.debug('Empty global variable [already_used_index]')
        del self.client.global_variables.already_used_index[:]

        self.client.global_variables.registration_opened = True
        log.info('Activated registration for community games')
        await ctx.send(ctx.author.mention + ' Registrations are opened')

    @commands.command(name="close")
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def close_registration_command(self, ctx):
        if not self.client.global_variables.registration_opened:
            log.debug('Registration is already closed')
            await ctx.send(ctx.author.mention + ' Registrations are already closed')
            return
        log.debug('Closed registration for community games')
        self.client.global_variables.registration_opened = False
        await ctx.send(ctx.author.mention + ' Registrations are closed')

    @commands.command(name="register")
    @decorators.only_allowed_channels
    async def register_player_name_command(self, ctx, in_game_name):
        user_id = ctx.author.id
        log.debug('Try register user with id: ' + str(user_id))
        if self.client.file_repository.user_exists_in_file(user_id):
            registered_name = self.client.file_repository.get_in_game_name_by_id(user_id)
            log.debug('User already registered with name: ' + registered_name)
            await ctx.send(ctx.author.mention + ' You are already registered with the name: ' + registered_name)
            return

        log.debug('Try to add player to file')
        self.client.file_repository.write_player_data_to_file(user_id, in_game_name)
        await ctx.send('Successfully registered ' + ctx.author.mention + ' with username: ' + in_game_name)

    @commands.command(name="add")
    @decorators.only_allowed_channels
    async def add_participant_command(self, ctx):
        if not self.client.global_variables.registration_opened:
            log.debug('Registrations are not opened')
            await ctx.send(ctx.author.mention + ' Registrations are not opened yet')
            return

        player_name = self.client.file_repository.get_in_game_name_by_id(ctx.author.id)
        log.debug('Player to add: ' + player_name)
        if not player_name:
            log.debug('Player not registered')
            await ctx.send(
                ctx.author.mention + ' You are not registered with an in-game character. Please use the `' +
                Config.COMMAND_PREFIX + 'register USERNAME` command.')
            return

        if player_name in self.client.global_variables.bench or \
                player_name in self.client.global_variables.players_list:
            log.debug('Player already registered')
            await ctx.send(ctx.author.mention + ' You are already registered for the community games')
            return

        # If first teams were generated already, add to bench as well
        log.debug('Check if player are already on bench')
        if len(self.client.global_variables.bench) > 0:
            log.debug('Add player to bench')
            self.client.global_variables.bench.append(player_name)

        log.debug('Add player to [players_list]')
        self.client.global_variables.players_list.append(player_name)

        await ctx.send(ctx.author.mention + ' You are now registered for the community games')

    @commands.command(name="remove")
    @decorators.only_allowed_channels
    async def remove_participant_command(self, ctx):
        in_game_name = self.client.file_repository.get_in_game_name_by_id(ctx.author.id)

        if in_game_name in self.client.global_variables.players_list:
            log.debug('Remove player from the players list')
            self.client.global_variables.players_list.remove(in_game_name)
        if in_game_name in self.client.global_variables.bench:
            log.debug('Remove player from the bench')
            self.client.global_variables.bench.remove(in_game_name)
        if in_game_name in self.client.global_variables.players_allowed_to_play:
            log.debug('Remove player from the allowed to play list')
            self.client.global_variables.players_allowed_to_play.remove(in_game_name)

        await ctx.send(ctx.author.mention + ' Removed you from the list of participants')

    @commands.command(name="participants")
    @decorators.only_allowed_channels
    async def show_participants_command(self, ctx):
        embed = discord.Embed(title="Participants", color=0x00ff00)
        for x in range(0, len(self.client.global_variables.players_list)):
            embed.add_field(name="Player " + str(x + 1) + ":", value=self.client.global_variables.players_list[x],
                            inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="addUser")
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def add_user_command(self, ctx, user: discord.User):
        if not self.client.global_variables.registration_opened:
            log.debug('Registrations are not opened')
            await ctx.send(ctx.author.mention + ' Registrations are not opened yet')
            return

        user_id = user.id
        in_game_name = self.client.file_repository.get_in_game_name_by_id(user_id)

        if not in_game_name:
            log.debug('Player not registered')
            await ctx.send(
                ctx.author.mention + ' The player is not registered with an ingame character. Please use the `' +
                Config.COMMAND_PREFIX + 'register USERNAME` command.')
            return

        if in_game_name in self.client.global_variables.bench or in_game_name in self.client.global_variables.players_list:
            log.debug('The player is already registered')
            await ctx.send(ctx.author.mention + ' Player already registered for the community games')
            return

        log.debug('Add player to the players list')
        self.client.global_variables.players_list.append(in_game_name)

        # If first teams were generated already, add to bench as well
        log.debug('Check if player are already on bench')
        if len(self.client.global_variables.bench) > 0:
            log.debug('Add player to bench')
            self.client.global_variables.bench.append(in_game_name)

        await ctx.send(ctx.author.mention + ' You registered ' + in_game_name + ' for the community games')

    @commands.command(name="removeUser")
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def remove_user_command(self, ctx, user: discord.User):
        in_game_name = self.client.file_repository.get_in_game_name_by_id(user.id)

        if in_game_name in self.client.global_variables.players_list:
            log.debug('Remove player from the players list')
            self.client.global_variables.players_list.remove(in_game_name)
        if in_game_name in self.client.global_variables.bench:
            log.debug('Remove player from the bench')
            self.client.global_variables.bench.remove(in_game_name)
        if in_game_name in self.client.global_variables.players_allowed_to_play:
            log.debug('Remove player from the allowed to play list')
            self.client.global_variables.players_allowed_to_play.remove(in_game_name)

        await ctx.send(ctx.author.mention + ' Removed ' + in_game_name + ' from the list of participants')

    @commands.command(name="registerUser")
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def register_user_command(self, ctx, user: discord.User, in_game_name):
        user_id = user.id
        if self.client.file_repository.user_exists_in_file(user_id):
            registered_name = self.client.file_repository.get_in_game_name_by_id(user_id)
            log.debug('User already registered with name: ' + registered_name)
            await ctx.send(ctx.author.mention + ' The player is already registered with the name: ' + registered_name)
            return

        self.client.file_repository.write_player_data_to_file(user_id, in_game_name)
        await ctx.send('Successfully registered ' + in_game_name + ' with username ' + in_game_name)

    @commands.command(name="deleteUser")
    @decorators.is_admin
    @decorators.only_allowed_channels
    async def delete_user_command(self, ctx, user: discord.User):
        user_id = user.id
        self.client.file_repository.delete_user_in_file(user_id)
        await ctx.send(ctx.author.mention + ' Successfully removed ' + user.name + ' from the list')


def setup(client):
    client.add_cog(CommunityGames(client))
