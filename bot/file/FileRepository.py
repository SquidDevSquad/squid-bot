import os

import Config

player_list_file_path = "./files/playerlist.txt"
map_list_file_path = './files/maplist.txt'


def write_player_data_to_file(user_id, in_game_name):
    player_list_file = open(player_list_file_path, "a")
    player_list_file.write(str(user_id) + "=" + in_game_name + "\n")
    player_list_file.close()


def user_exists_in_file(user_id):
    player_list_file = open(player_list_file_path, "r")
    for line in player_list_file:
        line_array = line.split('=')
        if int(line_array[0]) == user_id:
            player_list_file.close()
            return True
    player_list_file.close()
    return False


def get_in_game_name_by_id(user_id):
    player_list_file = open(player_list_file_path, "r")
    for line in player_list_file:
        line_array = line.split('=')
        if line_array[0] == str(user_id):
            player_list_file.close()
            return line_array[1].rstrip()
    player_list_file.close()
    return ''


def delete_user_in_file(user_id):
    with open(player_list_file_path, 'r') as f:
        lines = f.readlines()
    with open(player_list_file_path, 'w') as f:
        for line in lines:
            line_array = line.split('=')
            if line_array[0] != str(user_id):
                f.write(line)


def create_player_file_if_doesnt_exist():
    if not os.path.exists(player_list_file_path):
        os.open(player_list_file_path, os.O_RDWR | os.O_CREAT)


def create_map_file_if_doesnt_exist():
    if not os.path.exists(map_list_file_path):
        os.open(map_list_file_path, os.O_RDWR | os.O_CREAT)


def can_operate_in_channel(current_channel, allowed_channel):
    if current_channel in allowed_channel:
        return True
    return False


def is_map_already_registered(map_name):
    map_file = open(map_list_file_path, "r")
    for line in map_file:
        if line.rstrip() == map_name:
            map_file.close()
            return True
    map_file.close()
    return False


def add_map_to_file(map_name):
    map_file = open(map_list_file_path, "a")
    map_file.write(map_name + "\n")
    map_file.close()


def get_maps_from_file():
    map_file = open(map_list_file_path, "r")
    maps = list()
    for line in map_file:
        maps.append(line.rstrip())
    map_file.close()
    return maps


def remove_map_from_list(map_name):
    with open(map_list_file_path, 'r') as f:
        lines = f.readlines()
    with open(map_list_file_path, 'w') as f:
        for line in lines:
            if line.strip("\n") != map_name:
                f.write(line)


def is_admin(user_id):
    return user_id in Config.ALLOWED_USER_TO_ADMIN_COMMANDS
