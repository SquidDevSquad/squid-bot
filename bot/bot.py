import os

from discord.ext import commands
import Config
from log import LoggerFactory

import decorators
import globale_variables
import file_repository

log = LoggerFactory.get_logger(__name__)

client = commands.Bot(command_prefix=Config.COMMAND_PREFIX)

client.globale_variables = globale_variables.GlobaleVariables()
client.file_repository = file_repository.FileRepository()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        log.info('Load: ' + filename)
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    log.info("Bot started")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please fill in all required arguments')
        return


@client.command(help="Loads an extension")
@decorators.is_admin
async def load(ctx, extension):
    log.info('Load: ' + extension)
    client.load_extension(f'cogs.{extension}')


@client.command(help="Unloads an extension")
@decorators.is_admin
async def unload(ctx, extension):
    log.info('Unload: ' + extension)
    client.unload_extension(f'cogs.{extension}')


@client.command(help="Reloads an extension")
@decorators.is_admin
async def reload(ctx, extension):
    log.info('Reload: ' + extension)
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


client.run(Config.DISCORD_TOKEN)
