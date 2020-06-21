# Changelog
## Version 1.4.0
* Add spectator filtering by status
* Add rank emojis to players in list (Based on Discord role)
* Add average team SR calculation (Based on Discord role)

Other changes:
* Add `gt` alias for `generateTeams` command
* Fix sorting of commands in `help` command embed
* Add bench list printing after add/remove


## Version 1.3.0
## 2020-06-17
**Major release**:
* Refactor team generation to work with voice channel members without relying on files
* Add auto-bench priority mechanism
* Remove lots of unneeded code

## Version 1.2.0
## 2020-05-09
- Nothing new added.
- Refactored the code a lot.

## Version 1.1.2
## 2020-05-03
### Added
* Unit tests
* Logging infrastructure
### Fixed
- Bug of duplicate registered user

## Version 1.1.0
## 2020-04-10
### Added
- Added the giveaway module 
- You can now configure a specific voice channel where giveaways happen

## Version 1.0.0
## 2020-04-10
### Added
- Added more user commands for admins

### Changed
- Changed user identification from name to user id
- 

## 2020-04-09
### Added
- Added a permission system
- Added possibility to configure user ids in the config who has admin rights
- Added random map generator + commands

## 2020-04-07
### Added
- Added possibility to configure allowed channel
- Added description for the configuration int the Readme

## 2020-04-06
### Added
- Added Bot to repo
- Added configuration file

### Changed
- Cleanup the bot code (use Cogs)