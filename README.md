# squid-bot

## Configuration
| Config | Description |
|---|---|
| COMMAND_PREFIX | Needs to be at the beginning of every command |
| ALLOWED_CHANNEL | IDs of the allowed channel |
| ALLOWED_USER_TO_ADMIN_COMMANDS | IDs of the users who are allowed to use admin commands |

### Configure
#### Admin permissions:
In your `Config.py` insert the Discord IDs of wanted admin users to `ALLOWED_USER_TO_ADMIN_COMMANDS` list
#### Permitted voice channels:
In your `Config.py` insert the Discord IDs of wanted voice channels to `COMMUNITY_GAMES_VOICE_CHANNEL` and `GIVEAWAY_VOICE_CHANNEL` 

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