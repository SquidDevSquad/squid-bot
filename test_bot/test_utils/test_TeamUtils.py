from unittest import TestCase
from unittest.mock import MagicMock

from unittest_data_provider import data_provider

from utils import TeamUtils, TestUtils

role_to_sr_map = lambda: (
    ("Silver 1500+ sr", 1500),
    ("Gold 2000+ sr", 2000),
    ("Platinum 2500+ sr", 2500),
    ("Diamond 3000+ sr", 3000),
    ("Master 3500+ sr", 3500),
    ("GrandMaster 4000+ sr", 4000),
    ("No SR", 0)
)


class Test(TestCase):
    @data_provider(role_to_sr_map)
    def test_get_player_sr(self, sr_role, expected_sr):
        player_mock = MagicMock()
        player_mock.roles = list()
        role = MagicMock()
        role.name = sr_role
        player_mock.roles.append(role)
        sr = TeamUtils.get_player_sr(player_mock)
        self.assertEqual(expected_sr, sr)

    def test_get_team_avg_sr(self):
        players_list = TestUtils.generate_mock_players_list(6)
        expected_sr_total = 0
        for p in players_list:
            sr = TeamUtils.get_player_sr(p)
            expected_sr_total = expected_sr_total + sr

        expected_avg = int(expected_sr_total / 6)
        avg_sr = TeamUtils.get_team_avg_sr(players_list)
        self.assertEqual(expected_avg, avg_sr)
