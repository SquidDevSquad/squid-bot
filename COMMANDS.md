# Commands

| Permission | Description |
| -- | -- |
| User | Standard user (everyone) |
| Admin | All user who are entered in the ALLOWED_USER_TO_ADMIN_COMMANDS configuration |

## Standard Comamnds
| Command | Description | Permissions |
|--|--|--|
| load [cog] | Loads a certain Cog (Extension) |
| unload [cog] | Unloads a certain Cog (Extension) |
| reload [cog] | Unloads a certain Cog (Extension) |

## Community Games
| Command | Description | Permissions |
|--|--|--|
| open  | Opens the registration for the community games | Admin |
| close | Closes the registration for the community games | Admin |
| add | Adds the current user to the pool of players for the community games | User |
| remove | Removes the current player from the pool of players for the community games | User |
| participants | Shows a list of all registered users for the community games | User |
| register [ingameName] | Register player to list | User |

## Team Generator
| Command | Description | Permissions |
|--|--|--|
| generateTeams | Generates 2 random teams à 6 player | User |

## Map Generator
| Command | Description | Permissions |
|--|--|--|
| addMap [mapName]| Adds a map to the map pool | Admin |
| removeMap [mapName] | Removes a map from the pool | Admin |
| getMaps | Displays all configured maps | User |
| getRandomMap | Gets a random map | User |
| getUsedMaps | Shows all maps which were already used | Admin |
| resetMaps | Resets the used maps | Admin |