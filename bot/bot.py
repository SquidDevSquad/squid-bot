from discord.ext import commands

from file.FileRepository import *
from log import LoggerFactory

log = LoggerFactory.get_logger(__name__)

client = commands.Bot(command_prefix=Config.COMMAND_PREFIX)

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

@client.command(description="Loads an extension")
async def load(ctx, extension):
    if not is_admin(ctx.author.id):
        await ctx.send('You don\'t have the permissions to use this command')
        return
    log.info('Load: ' + extension)
    client.load_extension(f'cogs.{extension}')

@client.command(description="Unloads an extension")
async def unload(ctx, extension):
    if not is_admin(ctx.author.id):
        await ctx.send('You don\'t have the permissions to use this command')
        return
    log.info('Unload: ' + extension)
    client.unload_extension(f'cogs.{extension}')

@client.command(description="Reloads an extension")
async def reload(ctx, extension):
    if not is_admin(ctx.author.id):
        await ctx.send('You don\'t have the permissions to use this command')
        return
    log.info('Reload: ' + extension)
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

client.run(Config.DISCORD_TOKEN)