import os
import discord
from discord.ext import commands

import Config

client = commands.Bot(command_prefix = Config.COMMAND_PREFIX)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print('Load: ' + filename)
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print("Bot started")

@client.command(description="Loads an extension")
async def load(ctx, extension):
    print('Load: ' + extension)
    client.load_extension(f'cogs.{extension}')

@client.command(description="Unloads an extension")
async def unload(ctx, extension):
    print('Unload: ' + extension)
    client.unload_extension(f'cogs.{extension}')

@client.command(description="Reloads an extension")
async def reload(ctx, extension):
    print('Reload: ' + extension)
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

client.run(Config.DISCORD_TOKEN)