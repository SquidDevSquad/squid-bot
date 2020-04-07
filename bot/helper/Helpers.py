import os

def write_player_data_to_file(name, ingameName):
    playerListFile = open("./files/playerlist.txt", "a")
    playerListFile.write(name + "=" + ingameName + "\n")
    playerListFile.close()

def user_exists_in_file(name):
    playerListFile = open("./files/playerlist.txt", "r")
    for line in playerListFile:
        lineArray = line.split('=')
        if lineArray[0] == name:
            playerListFile.close()
            return True
    playerListFile.close()
    return False

def get_ingame_name_by_user(name):
    playerListFile = open("./files/playerlist.txt", "r")
    for line in playerListFile:
        lineArray = line.split('=')
        if lineArray[0] == name:
            playerListFile.close()
            return lineArray[1]
    playerListFile.close()
    return ''

def create_playerfile_if_doesnt_exist():
    if not os.path.exists('./files/playerlist.txt'):
        os.mknod('./files/playerlist.txt')

def can_operate_in_channel(currentChannel, allowedChannel):
    if currentChannel in allowedChannel:
        return True
    return False
