from random import randrange
from unittest.mock import MagicMock

from utils import UserUtils


class TestPlayer:
    def __init__(self, player_id, player_status, player_name):
        self.nick = None
        self.id = player_id
        self.name = player_name
        self.status = PlayerStatus(player_status)
        self.roles = [PlayerRole()]
        self.mention = '@' + player_name

    def __key(self):
        return self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, TestPlayer):
            return self.__key() == other.__key()
        return NotImplemented


class PlayerStatus:
    def __init__(self, value):
        self.value = value


class PlayerRole:
    def __init__(self):
        emoji_map = UserUtils.sr_role_2_emoji_map
        role_index = randrange(emoji_map.__len__())
        role_key = list(emoji_map.keys())[role_index]
        self.name = role_key


def generate_players_list(length, status=UserUtils.ONLINE):
    players = list()
    for i in range(length):
        player = TestPlayer(str(i) + "_" + status, status, "playerName" + str(i) + "_" + status)
        players.append(player)
    return players


def generate_mock_players_list(length, status=UserUtils.ONLINE):
    players = list()
    for i in range(length):
        player = MagicMock()
        player.nick = None
        player.id = str(i) + status
        player.name = "player" + str(i)
        player.status.value = status
        player.roles = [PlayerRole()]
        player.__str__ = to_str
        players.append(player)
    return players


def to_str(self):
    return self.name
