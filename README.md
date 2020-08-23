# squid-bot
This Discord bot has the following features:
#### Overwatch Team Generation
 Generates Overwatch 6v6 teams out of a selected Discord voice channel, taking into consideration the following:
 * Only users who are in status `online` on Discord are selected for team generation, others are considered spectators.
 * If there are more than 12 users in the voice channel, the remainder who are not selected are auto-benched. This means they are mandatory to be selected in the following generation (There are `add/removeFromBench` commands for adjustments)
 * Overwatch skill rating is displayed with appropriately emoji's and the average of team skill rating is calculated and presented after team generation (this relies on Discord roles)
    
#### Overwatch Map Generation

* Generates a random Overwatch map and displays an appropriate title and image.
* Marks the generated map in order to avoid repeating the same map in a single run.

#### Giveaway Lottery

* Randomly selects a winner for a giveaway lotter out of a selected voice channel, displaying a designed message.
* Marks the winner in order to void repeating the same winner ina single run (allows for repeated lotteries without restart)

## Config.py Configuration
| Config | Description |
|---|---|
| COMMAND_PREFIX | The prefix to use at the beginning of every command |
| ADMIN_IDS | Discord IDs of the users who are allowed to use admin commands |
| ALLOWED_TEXT_CHANNEL_IDS | Discord IDs of the allowed text channels |
| GIVEAWAY_VOICE_CHANNEL_ID | Discord channel ID for the giveaway lottery |
| COMMUNITY_GAMES_VOICE_CHANNEL_ID | Discord channel ID for the team generation |

### How To Run?

In command line or your preferred IDE: `python bot/bot.py BOT_TOKEN=<your_bot_token>`

### Docker
If you are using Docker to test or use the bot, you should first build the image with the following command:  
`docker build -t discord-bot .`  
When the image is built you can start the container with  
`docker run --rm -v $PWD/bot:/app/ -it discord-bot bash`  
If you are on Windows you need to adjust the path to the bot folder. But i recommend to use WSL on Windows.

## How to use?
See the list of [Commands](COMMANDS.md)