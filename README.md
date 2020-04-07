# squid-bot

## Commands

| Command  | Description  |
|---|---|
| !open  | Opens the registration for the community games  |
| !close  | Closes the registration for the community games  |
| !add  | Adds the current user to the pool of players for the community games  |
| !remove  | Removes the current player from the pool of players for the community games  |
| !participants | Shows a list of all registered users for the community games |
| !generateTeams | Generates 2 teams à 6 players |

## Configuration
| Config | Description |
|---|---|
| DISCORD_TOKEN | The token needed to contact your bot |
| COMMAND_PREFIX | Needs to be at the beginning of every command |
| ALLOWED_CHANNEL | Names of the allowed channel |

## How to install

Create a copy of the `Config.py.template` file and rename it to `Config.py`. Afterwards open it and insert your Bot token to the `DISCORD_TOKEN` constant. Now decide which prefix the commands should have and fill it in the `COMMAND_PREFIX` constant.

### Docker
If you are using Docker to test or use the bot, you should first build the image with the following command:  
`docker build -t discord-bot .`  
When the image is built you can start the container with  
`docker run --rm -v $PWD/bot:/app/ -it discord-bot bash`  
If you are on Windows you need to adjust the path to the bot folder. But i recommend to use WSL on Windows.
