# bot.py
import os

import discord

from random import randrange
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='!')

#playersList = ['angel', 'lightning', 'salti', 'aspect', 'blaid', 'deleted', 'djmanush', 'fresh', 'ice', 'grisly', 'loneWolf', 'lily', 'humid', 'ZBR', 'nyxii', 'sj', 'Seyuna']
playersList = list()
playersAllowedToPlay = list()
alreadyUsedIndex = list()

# Initialize lists of teams
teams = list()
bench = list()

registrationOpened = False

@client.event
async def on_ready():
    print("Bot started")

@client.command(name='open', help='Opens registration for players')
async def open_registration_command(ctx):
    global registrationOpened

    if registrationOpened:
        await ctx.send('Registration already opened')
        return
    
    registrationOpened = True
    await ctx.send('Registration for the community games are opened!\nIf you want to participate please use the !add command')
    

@client.command(name='close', help='Closes registration for players')
async def start_registration_command(ctx):
    global registrationOpened
    if not registrationOpened:
        await ctx.send('Registration already closed')
        return
    
    registrationOpened = False
    await ctx.send('Registrations closed')

@client.command(name='register', help='Registeres player with ingame name')
async def register_player_command(ctx, name):
    if player_already_in_list(ctx.author.name):
        await ctx.send('Player already registered')
        return
    playerNamesFile=open("playerlist.txt","a")
    playerNamesFile.write(ctx.author.name + "=" + name + '\n')
    playerNamesFile.close()
    await ctx.send('Player registered')


@client.command(name='add', help='Add the user to the players list')
async def add_player_command(ctx):

    if not registrationOpened:
        await ctx.send('Registration is not opened')
        return

    name = ctx.author.name

    if not player_already_in_list(name):
        await ctx.send('Your name is not in the list yet. Please use the !register command like `!register ingamename`.')
        return

    ingameName = get_ingame_name_by_name(name)

    if len(bench) > 0 and ingameName not in playersList and ingameName not in bench and ingameName not in playersAllowedToPlay:
        bench.append(ingameName)
        await ctx.send('Player added to the bench')

    # Check if player is already in the list
    if ingameName in playersList:
        await ctx.send('Player already in list')
        return

    # Add player to the list of possible candidates
    playersList.append(ingameName)
    await ctx.send('Added player ' + ingameName + ' to the list')

@client.command(name='remove', help='Remove user from players list')
async def remove_player_command(ctx):
    name = ctx.author.name
    ingameName = get_ingame_name_by_name(name)
    # Remove player from list
    if  ingameName in playersList:
        playersList.remove(ingameName)
    if ingameName in bench:
        bench.remove(ingameName)
    if ingameName in playersAllowedToPlay:
        playersAllowedToPlay.remove(ingameName)
    
    await ctx.send('Removed player ' + ingameName + ' from list')

@client.command(name='participants', help='Lists all registered players')
async def list_player_command(ctx):
    print(playersList)
    embed = discord.Embed(title="Participants", color=0x00ff00)
    for x in range(0, len(playersList)):
        embed.add_field(name="Player " + str(x + 1) + ":", value=playersList[x], inline=True)
    await ctx.send(embed=embed)

@client.command(name='generateTeams', help='Generates 2 Teams a 6 player')
async def generate_teams_command(ctx):
    if len(playersList) < 12:
        await ctx.send('Not enough player')
        return

    del alreadyUsedIndex[:]
    del teams[:]
    fill_players_allowed_to_play()
    generate_teams()

    embedTeam1 = generate_embed_message("1", teams[0])
    embedTeam2 = generate_embed_message("2", teams[1])

    await ctx.send(embed=embedTeam1)
    await ctx.send(embed=embedTeam2)

@client.command(name='bench', help='Shows benched players')
async def show_benched_player_command(ctx):
    embed = discord.Embed(title="Benched Players", color=0x00ff00)

    for x in range(0, len(bench)):
        embed.add_field(name="Player " + str(x + 1) + ":", value=bench[x], inline=True)
    await ctx.send(embed=embed)

def generate_embed_message(teamNumber, team):
    embed = discord.Embed(title="Team " + teamNumber, color=0x00ff00)
    for x in range(0, len(team)):
        embed.add_field(name="Player " + str(x + 1) + ":", value=team[x], inline=True)

    return embed

def generate_teams():
    for x in range(0, 2):
        teams.append(generate_team())
    #bench = generate_bench()

def fill_players_allowed_to_play():
    if (len(bench) > 0):
        playerToBench = len(bench)
        print(playerToBench)
        tempBench = list()

        for benched in range(0, playerToBench):
            playerIndexToRemove = randrange(len(playersAllowedToPlay))
            # Add player to a temporary list
            tempBench.append(playersAllowedToPlay[playerIndexToRemove])
            playersAllowedToPlay.remove(playersAllowedToPlay[playerIndexToRemove])
        
        for i in range(0, playerToBench):
            playersAllowedToPlay.append(bench[i])
        
        del bench[:]

        for x in range(0, len(tempBench)):
            bench.append(tempBench[x])
        
        del tempBench[:]
    else:
        playersToBench = len(playersList) - 12
        usedIndex = list()
        x = 0
        while (x < playersToBench):
            playerToRemoveIndex = randrange(playersToBench)
            if playerToRemoveIndex in usedIndex:
                continue
            bench.append(playersList[playerToRemoveIndex])
            usedIndex.append(playerToRemoveIndex)
            x += 1
        
        for x in range(0, len(playersList)):
            if x in usedIndex:
                continue
            playersAllowedToPlay.append(playersList[x])
   

def generate_team():
    numberOfPlayers = len(playersAllowedToPlay)
    team = list()
    x = 0
    while(x < 6):
        playerIndex = randrange(numberOfPlayers)
        if playerIndex in alreadyUsedIndex:
            continue
        alreadyUsedIndex.append(playerIndex)
        team.append(playersAllowedToPlay[playerIndex])
        x += 1
    
    return team

def generate_bench():
    numberOfPlayers = len(playersList)
    numberOfBenchedPlayers = numberOfPlayers - 12
    x = 0
    # generate bench
    while (x < numberOfBenchedPlayers):
        playerIndex = randrange(numberOfPlayers)
        if playerIndex in alreadyUsedIndex:
            continue
        alreadyUsedIndex.append(playerIndex)
        bench.append(playersList[playerIndex])
        x += 1

def had_benched_player():
    if len(bench) > 0:
        return true
    else:
        return false
    
def player_already_in_list(name):
    playerListFile = open("playerlist.txt", "r")
    for line in playerListFile:
        lineArray = line.split('=')
        if lineArray[0] == name:
            playerListFile.close()
            return True
    playerListFile.close()
    return False

def get_ingame_name_by_name(name):
    playerListFile = open("playerlist.txt", "r")
    for line in playerListFile:
        lineArray = line.split('=')
        if lineArray[0] == name:
            playerListFile.close()
            return lineArray[1].rstrip()
    playerListFile.close()
    return ''

client.run(TOKEN)