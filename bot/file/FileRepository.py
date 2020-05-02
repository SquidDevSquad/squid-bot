import os

import Config


def write_player_data_to_file(userId, ingameName):
    playerListFile = open("./files/playerlist.txt", "a")
    playerListFile.write(str(userId) + "=" + ingameName + "\n")
    playerListFile.close()


def user_exists_in_file(userId):
    playerListFile = open("./files/playerlist.txt", "r")
    for line in playerListFile:
        lineArray = line.split('=')
        if lineArray[0] == userId:
            playerListFile.close()
            return True
    playerListFile.close()
    return False


def get_ingame_name_by_id(userId):
    playerListFile = open("./files/playerlist.txt", "r")
    for line in playerListFile:
        lineArray = line.split('=')
        if lineArray[0] == str(userId):
            playerListFile.close()
            return lineArray[1].rstrip()
    playerListFile.close()
    return ''


def delete_user_in_file(userId):
    with open("./files/playerlist.txt", 'r') as f:
        lines = f.readlines()
    with open("./files/playerlist.txt", 'w') as f:
        for line in lines:
            lineArray = line.split('=')
            if lineArray[0] != str(userId):
                f.write(line)


def create_playerfile_if_doesnt_exist():
    if not os.path.exists('./files/playerlist.txt'):
        os.open('./files/playerlist.txt', os.O_RDWR | os.O_CREAT)


def create_mapfile_if_doesnt_exist():
    if not os.path.exists('./files/maplist.txt'):
        os.open('./files/maplist.txt', os.O_RDWR | os.O_CREAT)


def can_operate_in_channel(currentChannel, allowedChannel):
    if currentChannel in allowedChannel:
        return True
    return False


def is_map_already_registered(mapName):
    mapfile = open("./files/maplist.txt", "r")
    for line in mapfile:
        if line.rstrip() == mapName:
            mapfile.close()
            return True
    mapfile.close()
    return False


def add_map_to_file(mapName):
    mapfile = open("./files/maplist.txt", "a")
    mapfile.write(mapName + "\n")
    mapfile.close()


def get_maps_from_file():
    mapfile = open("./files/maplist.txt", "r")
    maps = list()
    for line in mapfile:
        maps.append(line.rstrip())
    mapfile.close()
    return maps


def remove_map_from_list(mapName):
    with open("./files/maplist.txt", 'r') as f:
        lines = f.readlines()
    with open("./files/maplist.txt", 'w') as f:
        for line in lines:
            if line.strip("\n") != mapName:
                f.write(line)


def is_admin(userId):
    return userId in Config.ALLOWED_USER_TO_ADMIN_COMMANDS
