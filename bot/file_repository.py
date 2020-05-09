import os

from log import LoggerFactory

log = LoggerFactory.get_logger(__name__)


class FileRepository:
    def __init__(self):
        self.player_list_file_path = "./files/playerlist.txt"
        self.map_list_file_path = "./files/maplist.txt"

    def write_player_data_to_file(self, user_id, in_game_name):
        with open(self.player_list_file_path, "a") as file:
            log.debug("Write " + str(user_id) + "=" + in_game_name)
            file.write(str(user_id) + "=" + in_game_name + "\n")

    def user_exists_in_file(self, user_id):
        with open(self.player_list_file_path, "r") as file:
            for line in file:
                line_array = line.split("=")
                if int(line_array[0]) == user_id:
                    log.debug("Found user by id: " + str(user_id))
                    return True
        log.debug("Couldn't find user by id: " + str(user_id))
        return False

    def get_in_game_name_by_id(self, user_id):
        with open(self.player_list_file_path, "r") as file:
            log.debug("Try to find user by id: " + str(user_id))
            for line in file:
                line_array = line.split("=")
                if int(line_array[0]) == user_id:
                    log.debug(
                        "Found user with id: "
                        + str(user_id)
                        + " = "
                        + line_array[1].rstrip()
                    )
                    return line_array[1].rstrip()
        log.debug("Couldn't find user by id: " + str(user_id))
        return ""

    def delete_user_in_file(self, user_id):
        with open(self.player_list_file_path, "r") as f:
            log.debug("Read all lines of player file")
            lines = f.readlines()
        with open(self.player_list_file_path, "w") as f:
            for line in lines:
                line_array = line.split("=")
                if int(line_array[0]) != user_id:
                    log.debug("Writing entry to delete")
                    f.write(line)

    def create_player_file_if_doesnt_exist(self):
        if not os.path.exists(self.player_list_file_path):
            log.debug("Creating player file")
            os.open(self.player_list_file_path, os.O_RDWR | os.O_CREAT)

    def create_map_file_if_doesnt_exist(self):
        if not os.path.exists(self.map_list_file_path):
            log.debug("Creating map file")
            os.open(self.map_list_file_path, os.O_RDWR | os.O_CREAT)

    def add_map_to_file(self, map_name):
        with open(self.map_list_file_path, "a") as file:
            log.debug("Write map to file: " + map_name)
            file.write(map_name + "\n")

    def get_maps_from_file(self):
        with open(self.map_list_file_path, "r") as file:
            maps = list()
            for line in file:
                maps.append(line.rstrip())
            return maps

    def is_map_already_registered(self, map_name):
        with open(self.map_list_file_path, "r") as file:
            for line in file:
                if line.rstrip() == map_name:
                    log.debug("Found map")
                    return True
            log.debug("Couldn't find map")
            return False

    def remove_map_from_list(self, map_name):
        with open(self.map_list_file_path, "r") as f:
            log.debug("Read all lines of map file")
            lines = f.readlines()
        with open(self.map_list_file_path, "w") as f:
            for line in lines:
                if line.strip("\n") != map_name:
                    log.debug("Add map again")
                    f.write(line)
