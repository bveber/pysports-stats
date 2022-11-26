from mock import patch
from os import path
from sports.fb.team import Team
from ..utils import read_file


def mock_pyquery(url):
    if "361ca564" in url:
        return read_file("tottenham-hotspur-2022-2023.html", "fb", "team")
    return None


class TestFBTeam:
    def setup_method(self):
        self.results = {
            "away_draws": 2,
            "away_games": 7,
            "away_losses": 2,
            "away_points": 11,
            "away_record": "3-2-2",
            "away_wins": 3,
            "country": "England",
            "expected_goal_difference": 7.6,
            "expected_goals": 24.1,
            "expected_goals_against": 16.5,
            "gender": "Male",
            "goal_difference": 10,
            "goals_against": 21,
            "goals_scored": 31,
            "home_draws": 0,
            "home_games": 8,
            "home_losses": 2,
            "home_points": 18,
            "home_record": "6-0-2",
            "home_wins": 6,
            "league": "Premier League",
            "manager": "Antonio Conte",
            "name": "Tottenham Hotspur",
            "points": 29,
            "position": 4,
            "record": "9-2-4",
            "season": "2022-2023",
        }

    @patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_fb_team_returns_correct_attributes(self, *args, **kwargs):
        tottenham = Team("Tottenham Hotspur")

        for attribute, value in self.results.items():
            assert getattr(tottenham, attribute) == value

    @patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_team_name(self, *args, **kwargs):
        team = Team("Tottenham Hotspur")

        assert team.__repr__() == "Tottenham Hotspur (361ca564) - 2022-2023"
