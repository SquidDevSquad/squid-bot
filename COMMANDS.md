# Commands

| Permission | Description |
| -- | -- |
| User | Standard user (everyone) |
| Admin | All user who are entered in the ALLOWED_USER_TO_ADMIN_COMMANDS configuration |

## Standard Comamnds
| Command | Description | Permissions |
|--|--|--|
| load [cog] | Loads a certain Cog (Extension) | Admin
| unload [cog] | Unloads a certain Cog (Extension) | Admin
| reload [cog] | Unloads a certain Cog (Extension) | Admin

## Community Games
| Command | Description | Permissions |
|--|--|--|
| open  | Opens the registration for the community games | Admin |
| close | Closes the registration for the community games | Admin |
| addToBench @[playerName] | Adds a player to the bench | Admin | 
| removeFromBench @[playerName] | Remove a player from the bench | Admin |
| showBench | Displays the list of players currently in bench | User |
| clear | Clears all messages in current channel | Admin | 

## Team Generator
| Command | Alias | Description | Permissions |
|--|--|--|--|
| generateTeams | gt | Generates 2 random teams of 6 players each, auto-adding to bench players who were not chosen. Players in bench have higher priority in next generation. Generation is made with players who have set **online** status on Discord. Players with other statuses are considered spectators | Admin |

## Map Generator
| Command | Alias | Description | Permissions |
|--|--|--|--|
| getRandomMap | grm | Gets a random map | User |
| getUsedMaps | - | Shows all maps which were already used | Admin |
| resetUsedMaps | - | Resets the used maps | Admin |

## Giveaway
| Command | Description | Permissions |
|--|--|--|
| giveaway | Draws a random user from the giveaway list | Admin |