import os
from os.path import splitext

import discord
from discord.ext import commands

import Config
import decorators
import global_variables
from commands.MyHelpCommand import MyHelpCommand
from log import LoggerFactory

log = LoggerFactory.get_logger(__name__)

intents = discord.Intents(messages=True, members=True, presences=True, guilds=True)
help_command = MyHelpCommand()
client = commands.Bot(command_prefix=Config.COMMAND_PREFIX, help_command=help_command, intents=intents)

client.global_variables = global_variables.GlobalVariables()

for filename in os.listdir(os.getcwd() + "/bot/cogs"):
    file = splitext(filename)
    if file[1] == ".py":
        log.info("Load: " + file[0])
        client.load_extension(f"cogs.{file[0]}")


@client.event
async def on_ready():
    log.info("Squid-Bot started :)")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please fill in all required arguments")
        return


@client.command(help="Loads an extension")
@decorators.is_admin
async def load(ctx, extension):
    log.info("Load: " + extension)
    client.load_extension(f"cogs.{extension}")


@client.command(help="Unloads an extension")
@decorators.is_admin
async def unload(ctx, extension):
    log.info("Unload: " + extension)
    client.unload_extension(f"cogs.{extension}")


@client.command(help="Reloads an extension")
@decorators.is_admin
async def reload(ctx, extension):
    log.info("Reload: " + extension)
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")


token = os.environ['BOT_TOKEN']
client.run(token)
