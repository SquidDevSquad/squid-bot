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

## Team Generator
| Command | Description | Permissions |
|--|--|--|
| generateTeams | Generates 2 random teams of 6 players each, auto-adding to bench players who were not chosen. Players in bench have higher priority in next generation | Admin |

## Map Generator
| Command | Description | Permissions |
|--|--|--|
| addMap [mapName]| Adds a map to the map pool | Admin |
| removeMap [mapName] | Removes a map from the pool | Admin |
| getMaps | Displays all configured maps | User |
| getRandomMap | Gets a random map | User |
| getUsedMaps | Shows all maps which were already used | Admin |
| resetMaps | Resets the used maps | Admin |

## Giveaway
| Command | Description | Permissions |
|--|--|--|
| getGiveawayUser | Saves all user who are in the configured voice channel | Admin |
| getGiveawayWinner | Draws a random user from the giveaway list | Admin |