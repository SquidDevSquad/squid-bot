# TODO Mor: Add tests
from utils import UserUtils

role_to_sr_map = {
    "Silver 1500+ sr": 1500,
    "Gold 2000+ sr": 2000,
    "Platinum 2500+ sr": 2500,
    "Diamond 3000+ sr": 3000,
    "Master 3500+ sr": 3500,
    "GrandMaster 4000+ sr": 4000,
    "No SR": 0
}


def get_player_sr(player):
    sr_role = UserUtils.find_sr_role(player.roles)
    return role_to_sr_map[sr_role]


def get_team_avg_sr(team):
    sr_total = 0
    for p in team:
        sr_total = sr_total + get_player_sr(p)
    return int(sr_total / 6)
