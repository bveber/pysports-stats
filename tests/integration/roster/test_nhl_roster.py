import mock
import os
import pandas as pd
import pytest
from flexmock import flexmock
from sports import utils
from sports.nhl.roster import Player, Roster
from sports.nhl.teams import Team
from ..utils import read_file


PLAYER_YEAR_INDEX = "2021-22"
ROSTER_YEAR = "2022"
TEAM = "MIN"


def mock_pyquery(url):
    if "BAD" in url or "bad" in url:
        return None
    if "kapriki01" in url:
        return read_file("kapriki01.html", "nhl", "roster")
    if "kahkoka01" in url:
        return read_file("kahkoka01.html", "nhl", "roster")
    if "MIN" in url:
        return read_file("MIN-2022.html", "nhl", "roster")
    return None


def mock_request(url):
    class MockRequest:
        def __init__(self, html_contents, status_code=200):
            self.status_code = status_code
            self.html_contents = html_contents
            self.text = html_contents

    if str(ROSTER_YEAR) in url:
        return MockRequest("good")
    else:
        return MockRequest("bad", status_code=404)


class TestNHLPlayer:
    def setup_method(self):
        self.skater_results_career = {
            "adjusted_assists": 138,
            "adjusted_goals": 132,
            "adjusted_goals_against_average": None,
            "adjusted_goals_created": 110,
            "adjusted_points": 270,
            "age": None,
            "assists": 51,
            "average_time_on_ice": "19:02",
            "blocks_at_even_strength": 29,
            "corsi_against": 2157.0,
            "corsi_for": 3261.0,
            "corsi_for_percentage": 60.2,
            "defensive_point_shares": 3.7,
            "defensive_zone_start_percentage": 28.0,
            "even_strength_assists": 69,
            "even_strength_goals": 57,
            "even_strength_goals_allowed": None,
            "even_strength_save_percentage": None,
            "even_strength_shots_faced": None,
            "faceoff_losses": 14,
            "faceoff_percentage": 23.5,
            "faceoff_wins": 4,
            "fenwick_against": 1619,
            "fenwick_for": 2478,
            "fenwick_for_percentage": 60.5,
            "game_winning_goals": 10,
            "games_played": 82,
            "giveaways": 63,
            "goal_against_percentage_relative": None,
            "goalie_point_shares": None,
            "goals": 45,
            "goals_against": None,
            "goals_against_average": None,
            "goals_against_on_ice": 126,
            "goals_created": 72,
            "goals_for_on_ice": 225,
            "goals_saved_above_average": None,
            "height": "5-10",
            "hits_at_even_strength": 62,
            "league": "NHL",
            "losses": None,
            "minutes": None,
            "name": "Kirill Kaprizov",
            "offensive_point_shares": 18.0,
            "offensive_zone_start_percentage": 72.0,
            "pdo": 102.0,
            "penalties_in_minutes": 63,
            "player_id": "kapriki01",
            "plus_minus": 32,
            "point_shares": 21.6,
            "points": 95,
            "power_play_assists": 26,
            "power_play_goals": 27,
            "power_play_goals_against_on_ice": 1,
            "power_play_goals_allowed": None,
            "power_play_goals_for_on_ice": 69,
            "power_play_save_percentage": None,
            "power_play_shots_faced": None,
            "quality_start_percentage": None,
            "quality_starts": None,
            "really_bad_starts": None,
            "relative_corsi_for_percentage": 15.9,
            "relative_fenwick_for_percentage": 15.7,
            "save_percentage": None,
            "save_percentage_on_ice": None,
            "saves": None,
            "season": "Career",
            "shooting_percentage": 16.2,
            "shooting_percentage_on_ice": 12.4,
            "shootout_attempts": 9,
            "shootout_goals": 4,
            "shootout_misses": 5,
            "shootout_percentage": 44.4,
            "short_handed_assists": 0,
            "short_handed_goals": 0,
            "short_handed_goals_allowed": None,
            "short_handed_save_percentage": None,
            "short_handed_shots_faced": None,
            "shots_against": None,
            "shots_on_goal": 276,
            "shutouts": None,
            "takeaways": 52,
            "team_abbreviation": None,
            "ties_plus_overtime_loss": None,
            "time_on_ice": 2930,
            "time_on_ice_even_strength": 2930.4,
            "total_goals_against_on_ice": 126,
            "total_goals_for_on_ice": 225,
            "total_shots": 491,
            "weight": 202,
            "wins": None,
        }

        self.skater_results_year = {
            "adjusted_assists": 58,
            "adjusted_goals": 46,
            "adjusted_goals_against_average": None,
            "adjusted_goals_created": 41,
            "adjusted_points": 104,
            "age": 24.0,
            "assists": 61,
            "average_time_on_ice": "19:06",
            "blocks_at_even_strength": 29,
            "corsi_against": 1144.0,
            "corsi_for": 1771.0,
            "corsi_for_percentage": 60.8,
            "defensive_point_shares": 2.0,
            "defensive_zone_start_percentage": 27.9,
            "even_strength_assists": 44,
            "even_strength_goals": 33,
            "even_strength_goals_allowed": None,
            "even_strength_save_percentage": None,
            "even_strength_shots_faced": None,
            "faceoff_losses": 4,
            "faceoff_percentage": 55.6,
            "faceoff_wins": 5,
            "fenwick_against": 875,
            "fenwick_for": 1326,
            "fenwick_for_percentage": 60.2,
            "game_winning_goals": 5,
            "games_played": 81,
            "giveaways": 72,
            "goal_against_percentage_relative": None,
            "goalie_point_shares": None,
            "goals": 47,
            "goals_against": None,
            "goals_against_average": None,
            "goals_against_on_ice": 69,
            "goals_created": 42,
            "goals_for_on_ice": 135,
            "goals_saved_above_average": None,
            "height": "5-10",
            "hits_at_even_strength": 73,
            "league": "NHL",
            "losses": None,
            "minutes": None,
            "name": "Kirill Kaprizov",
            "offensive_point_shares": 10.7,
            "offensive_zone_start_percentage": 72.1,
            "pdo": 103.3,
            "penalties_in_minutes": 34,
            "player_id": "kapriki01",
            "plus_minus": 27,
            "point_shares": 12.8,
            "points": 108,
            "power_play_assists": 17,
            "power_play_goals": 14,
            "power_play_goals_against_on_ice": 1,
            "power_play_goals_allowed": None,
            "power_play_goals_for_on_ice": 40,
            "power_play_save_percentage": None,
            "power_play_shots_faced": None,
            "quality_start_percentage": None,
            "quality_starts": None,
            "really_bad_starts": None,
            "relative_corsi_for_percentage": 14.9,
            "relative_fenwick_for_percentage": 14.1,
            "save_percentage": None,
            "save_percentage_on_ice": None,
            "saves": None,
            "season": "2021-22",
            "shooting_percentage": 16.3,
            "shooting_percentage_on_ice": 13.8,
            "shootout_attempts": 6,
            "shootout_goals": 2,
            "shootout_misses": 4,
            "shootout_percentage": 33.3,
            "short_handed_assists": 0,
            "short_handed_goals": 0,
            "short_handed_goals_allowed": None,
            "short_handed_save_percentage": None,
            "short_handed_shots_faced": None,
            "shots_against": None,
            "shots_on_goal": 289,
            "shutouts": None,
            "takeaways": 57,
            "team_abbreviation": "MIN",
            "ties_plus_overtime_loss": None,
            "time_on_ice": 1548,
            "time_on_ice_even_strength": 1547.7,
            "total_goals_against_on_ice": 69,
            "total_goals_for_on_ice": 135,
            "total_shots": 515,
            "weight": 202,
            "wins": None,
        }

        self.goalie_results_career = {
            "adjusted_assists": None,
            "adjusted_goals": None,
            "adjusted_goals_against_average": 3.08,
            "adjusted_goals_created": None,
            "adjusted_points": None,
            "age": None,
            "assists": 1,
            "average_time_on_ice": None,
            "blocks_at_even_strength": None,
            "corsi_against": None,
            "corsi_for": None,
            "corsi_for_percentage": None,
            "defensive_point_shares": None,
            "defensive_zone_start_percentage": None,
            "even_strength_assists": None,
            "even_strength_goals": None,
            "even_strength_goals_allowed": 147,
            "even_strength_save_percentage": 0.915,
            "even_strength_shots_faced": 1720,
            "faceoff_losses": None,
            "faceoff_percentage": None,
            "faceoff_wins": None,
            "fenwick_against": None,
            "fenwick_for": None,
            "fenwick_for_percentage": None,
            "game_winning_goals": None,
            "games_played": None,
            "giveaways": None,
            "goal_against_percentage_relative": 101.0,
            "goalie_point_shares": 8.9,
            "goals": 0,
            "goals_against": 149,
            "goals_against_average": 2.88,
            "goals_against_on_ice": None,
            "goals_created": None,
            "goals_for_on_ice": None,
            "goals_saved_above_average": -2.1,
            "height": "6-2",
            "hits_at_even_strength": None,
            "league": "NHL",
            "losses": 17,
            "minutes": 3099,
            "name": "Kaapo Kahkonen",
            "offensive_point_shares": None,
            "offensive_zone_start_percentage": None,
            "pdo": None,
            "penalties_in_minutes": 4,
            "player_id": "kahkoka01",
            "plus_minus": None,
            "point_shares": None,
            "points": 1,
            "power_play_assists": None,
            "power_play_goals": None,
            "power_play_goals_against_on_ice": None,
            "power_play_goals_allowed": 47,
            "power_play_goals_for_on_ice": None,
            "power_play_save_percentage": 0.855,
            "power_play_shots_faced": 324,
            "quality_start_percentage": 0.549,
            "quality_starts": 28,
            "really_bad_starts": 10,
            "relative_corsi_for_percentage": None,
            "relative_fenwick_for_percentage": None,
            "save_percentage": 0.907,
            "save_percentage_on_ice": None,
            "saves": 1449,
            "season": "Career",
            "shooting_percentage": None,
            "shooting_percentage_on_ice": None,
            "shootout_attempts": None,
            "shootout_goals": None,
            "shootout_misses": None,
            "shootout_percentage": None,
            "short_handed_assists": None,
            "short_handed_goals": None,
            "short_handed_goals_allowed": 5,
            "short_handed_save_percentage": 0.918,
            "short_handed_shots_faced": 61,
            "shots_against": 1598,
            "shots_on_goal": None,
            "shutouts": 2,
            "takeaways": None,
            "team_abbreviation": None,
            "ties_plus_overtime_loss": 4,
            "time_on_ice": None,
            "time_on_ice_even_strength": None,
            "total_goals_against_on_ice": None,
            "total_goals_for_on_ice": None,
            "total_shots": None,
            "weight": 215,
            "wins": 31,
        }

        self.goalie_results_year = {
            "adjusted_assists": None,
            "adjusted_goals": None,
            "adjusted_goals_against_average": 2.96,
            "adjusted_goals_created": None,
            "adjusted_points": None,
            "age": 25.0,
            "assists": 1,
            "average_time_on_ice": None,
            "blocks_at_even_strength": None,
            "corsi_against": None,
            "corsi_for": None,
            "corsi_for_percentage": None,
            "defensive_point_shares": None,
            "defensive_zone_start_percentage": None,
            "even_strength_assists": None,
            "even_strength_goals": None,
            "even_strength_goals_allowed": 67,
            "even_strength_save_percentage": 0.921,
            "even_strength_shots_faced": 847,
            "faceoff_losses": None,
            "faceoff_percentage": None,
            "faceoff_wins": None,
            "fenwick_against": None,
            "fenwick_for": None,
            "fenwick_for_percentage": None,
            "game_winning_goals": None,
            "games_played": None,
            "giveaways": None,
            "goal_against_percentage_relative": 95.0,
            "goalie_point_shares": 6.4,
            "goals": 0,
            "goals_against": 93,
            "goals_against_average": 2.87,
            "goals_against_on_ice": None,
            "goals_created": None,
            "goals_for_on_ice": None,
            "goals_saved_above_average": 5.2,
            "height": "6-2",
            "hits_at_even_strength": None,
            "league": "NHL",
            "losses": 14,
            "minutes": 1947,
            "name": "Kaapo Kahkonen",
            "offensive_point_shares": None,
            "offensive_zone_start_percentage": None,
            "pdo": None,
            "penalties_in_minutes": 2,
            "player_id": "kahkoka01",
            "plus_minus": None,
            "point_shares": None,
            "points": 1,
            "power_play_assists": None,
            "power_play_goals": None,
            "power_play_goals_against_on_ice": None,
            "power_play_goals_allowed": 24,
            "power_play_goals_for_on_ice": None,
            "power_play_save_percentage": 0.862,
            "power_play_shots_faced": 174,
            "quality_start_percentage": 0.667,
            "quality_starts": 22,
            "really_bad_starts": 6,
            "relative_corsi_for_percentage": None,
            "relative_fenwick_for_percentage": None,
            "save_percentage": 0.912,
            "save_percentage_on_ice": None,
            "saves": 963,
            "season": "2021-22",
            "shooting_percentage": None,
            "shooting_percentage_on_ice": None,
            "shootout_attempts": None,
            "shootout_goals": None,
            "shootout_misses": None,
            "shootout_percentage": None,
            "short_handed_assists": None,
            "short_handed_goals": None,
            "short_handed_goals_allowed": 2,
            "short_handed_save_percentage": 0.935,
            "short_handed_shots_faced": 31,
            "shots_against": 1056,
            "shots_on_goal": None,
            "shutouts": 0,
            "takeaways": None,
            "team_abbreviation": "TOT",
            "ties_plus_overtime_loss": 4,
            "time_on_ice": None,
            "time_on_ice_even_strength": None,
            "total_goals_against_on_ice": None,
            "total_goals_for_on_ice": None,
            "total_shots": None,
            "weight": 215,
            "wins": 14,
        }

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_nhl_skater_returns_requested_career_stats(self, *args, **kwargs):
        # Request the career stats
        player = Player("kapriki01")
        player = player("")

        for attribute, value in self.skater_results_career.items():
            assert getattr(player, attribute) == value

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_nhl_skater_returns_player_season_stats(self, *args, **kwargs):
        # Request the 2017 stats
        player = Player("kapriki01")
        player = player(PLAYER_YEAR_INDEX)

        for attribute, value in self.skater_results_year.items():
            assert getattr(player, attribute) == value

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_nhl_goalie_returns_requested_career_stats(self, *args, **kwargs):
        # Request the career stats
        player = Player("kahkoka01")
        player = player("")

        for attribute, value in self.goalie_results_career.items():
            assert getattr(player, attribute) == value

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_nhl_goalie_returns_player_season_stats(self, *args, **kwargs):
        # Request the 2017 stats
        player = Player("kahkoka01")
        player = player(PLAYER_YEAR_INDEX)

        for attribute, value in self.goalie_results_year.items():
            assert getattr(player, attribute) == value

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_dataframe_returns_dataframe(self, *args, **kwargs):
        dataframe = [
            {
                "adjusted_assists": 36,
                "adjusted_goals": 41,
                "adjusted_goals_against_average": None,
                "adjusted_goals_created": 32,
                "adjusted_points": 77,
                "age": 23.0,
                "assists": 24,
                "average_time_on_ice": "18:18",
                "blocks_at_even_strength": 18,
                "corsi_against": 759.0,
                "corsi_for": 1059.0,
                "corsi_for_percentage": 58.3,
                "defensive_point_shares": 1.3,
                "defensive_zone_start_percentage": 30.2,
                "even_strength_assists": 19,
                "even_strength_goals": 19,
                "even_strength_goals_allowed": None,
                "even_strength_save_percentage": None,
                "even_strength_shots_faced": None,
                "faceoff_losses": 21,
                "faceoff_percentage": 12.5,
                "faceoff_wins": 3,
                "fenwick_against": 565,
                "fenwick_for": 819,
                "fenwick_for_percentage": 59.2,
                "game_winning_goals": 3,
                "games_played": 55,
                "giveaways": 35,
                "goal_against_percentage_relative": None,
                "goalie_point_shares": None,
                "goals": 27,
                "goals_against": None,
                "goals_against_average": None,
                "goals_against_on_ice": 39,
                "goals_created": 22,
                "goals_for_on_ice": 65,
                "goals_saved_above_average": None,
                "height": "5-10",
                "hits_at_even_strength": 29,
                "league": "NHL",
                "losses": None,
                "minutes": None,
                "name": "Kirill Kaprizov",
                "offensive_point_shares": 5.4,
                "offensive_zone_start_percentage": 69.8,
                "pdo": 101.7,
                "penalties_in_minutes": 16,
                "player_id": "kapriki01",
                "plus_minus": 10,
                "point_shares": 6.7,
                "points": 51,
                "power_play_assists": 5,
                "power_play_goals": 8,
                "power_play_goals_against_on_ice": 0,
                "power_play_goals_allowed": None,
                "power_play_goals_for_on_ice": 17,
                "power_play_save_percentage": None,
                "power_play_shots_faced": None,
                "quality_start_percentage": None,
                "quality_starts": None,
                "really_bad_starts": None,
                "relative_corsi_for_percentage": 16.2,
                "relative_fenwick_for_percentage": 16.0,
                "save_percentage": None,
                "save_percentage_on_ice": None,
                "saves": None,
                "season": "2020-21",
                "shooting_percentage": 17.2,
                "shooting_percentage_on_ice": 11.1,
                "shootout_attempts": 1,
                "shootout_goals": 0,
                "shootout_misses": 1,
                "shootout_percentage": 0.0,
                "short_handed_assists": 0,
                "short_handed_goals": 0,
                "short_handed_goals_allowed": None,
                "short_handed_save_percentage": None,
                "short_handed_shots_faced": None,
                "shots_against": None,
                "shots_on_goal": 157,
                "shutouts": None,
                "takeaways": 27,
                "team_abbreviation": "MIN",
                "ties_plus_overtime_loss": None,
                "time_on_ice": 1006,
                "time_on_ice_even_strength": 1006.4,
                "total_goals_against_on_ice": 39,
                "total_goals_for_on_ice": 65,
                "total_shots": 280,
                "weight": 202,
                "wins": None,
            },
            {
                "adjusted_assists": 58,
                "adjusted_goals": 46,
                "adjusted_goals_against_average": None,
                "adjusted_goals_created": 41,
                "adjusted_points": 104,
                "age": 24.0,
                "assists": 61,
                "average_time_on_ice": "19:06",
                "blocks_at_even_strength": 29,
                "corsi_against": 1144.0,
                "corsi_for": 1771.0,
                "corsi_for_percentage": 60.8,
                "defensive_point_shares": 2.0,
                "defensive_zone_start_percentage": 27.9,
                "even_strength_assists": 44,
                "even_strength_goals": 33,
                "even_strength_goals_allowed": None,
                "even_strength_save_percentage": None,
                "even_strength_shots_faced": None,
                "faceoff_losses": 4,
                "faceoff_percentage": 55.6,
                "faceoff_wins": 5,
                "fenwick_against": 875,
                "fenwick_for": 1326,
                "fenwick_for_percentage": 60.2,
                "game_winning_goals": 5,
                "games_played": 81,
                "giveaways": 72,
                "goal_against_percentage_relative": None,
                "goalie_point_shares": None,
                "goals": 47,
                "goals_against": None,
                "goals_against_average": None,
                "goals_against_on_ice": 69,
                "goals_created": 42,
                "goals_for_on_ice": 135,
                "goals_saved_above_average": None,
                "height": "5-10",
                "hits_at_even_strength": 73,
                "league": "NHL",
                "losses": None,
                "minutes": None,
                "name": "Kirill Kaprizov",
                "offensive_point_shares": 10.7,
                "offensive_zone_start_percentage": 72.1,
                "pdo": 103.3,
                "penalties_in_minutes": 34,
                "player_id": "kapriki01",
                "plus_minus": 27,
                "point_shares": 12.8,
                "points": 108,
                "power_play_assists": 17,
                "power_play_goals": 14,
                "power_play_goals_against_on_ice": 1,
                "power_play_goals_allowed": None,
                "power_play_goals_for_on_ice": 40,
                "power_play_save_percentage": None,
                "power_play_shots_faced": None,
                "quality_start_percentage": None,
                "quality_starts": None,
                "really_bad_starts": None,
                "relative_corsi_for_percentage": 14.9,
                "relative_fenwick_for_percentage": 14.1,
                "save_percentage": None,
                "save_percentage_on_ice": None,
                "saves": None,
                "season": "2021-22",
                "shooting_percentage": 16.3,
                "shooting_percentage_on_ice": 13.8,
                "shootout_attempts": 6,
                "shootout_goals": 2,
                "shootout_misses": 4,
                "shootout_percentage": 33.3,
                "short_handed_assists": 0,
                "short_handed_goals": 0,
                "short_handed_goals_allowed": None,
                "short_handed_save_percentage": None,
                "short_handed_shots_faced": None,
                "shots_against": None,
                "shots_on_goal": 289,
                "shutouts": None,
                "takeaways": 57,
                "team_abbreviation": "MIN",
                "ties_plus_overtime_loss": None,
                "time_on_ice": 1548,
                "time_on_ice_even_strength": 1547.7,
                "total_goals_against_on_ice": 69,
                "total_goals_for_on_ice": 135,
                "total_shots": 515,
                "weight": 202,
                "wins": None,
            },
            {
                "adjusted_assists": 44,
                "adjusted_goals": 45,
                "adjusted_goals_against_average": None,
                "adjusted_goals_created": 37,
                "adjusted_points": 89,
                "age": 25.0,
                "assists": 10,
                "average_time_on_ice": "20:54",
                "blocks_at_even_strength": 7,
                "corsi_against": 254.0,
                "corsi_for": 431.0,
                "corsi_for_percentage": 62.9,
                "defensive_point_shares": 0.4,
                "defensive_zone_start_percentage": 21.8,
                "even_strength_assists": 6,
                "even_strength_goals": 5,
                "even_strength_goals_allowed": None,
                "even_strength_save_percentage": None,
                "even_strength_shots_faced": None,
                "faceoff_losses": 1,
                "faceoff_percentage": 0.0,
                "faceoff_wins": 0,
                "fenwick_against": 179,
                "fenwick_for": 333,
                "fenwick_for_percentage": 65.0,
                "game_winning_goals": 2,
                "games_played": 18,
                "giveaways": 11,
                "goal_against_percentage_relative": None,
                "goalie_point_shares": None,
                "goals": 10,
                "goals_against": None,
                "goals_against_average": None,
                "goals_against_on_ice": 18,
                "goals_created": 8,
                "goals_for_on_ice": 25,
                "goals_saved_above_average": None,
                "height": "5-10",
                "hits_at_even_strength": 15,
                "league": "NHL",
                "losses": None,
                "minutes": None,
                "name": "Kirill Kaprizov",
                "offensive_point_shares": 1.8,
                "offensive_zone_start_percentage": 78.2,
                "pdo": 96.4,
                "penalties_in_minutes": 13,
                "player_id": "kapriki01",
                "plus_minus": -5,
                "point_shares": 2.2,
                "points": 20,
                "power_play_assists": 4,
                "power_play_goals": 5,
                "power_play_goals_against_on_ice": 0,
                "power_play_goals_allowed": None,
                "power_play_goals_for_on_ice": 12,
                "power_play_save_percentage": None,
                "power_play_shots_faced": None,
                "quality_start_percentage": None,
                "quality_starts": None,
                "really_bad_starts": None,
                "relative_corsi_for_percentage": 19.4,
                "relative_fenwick_for_percentage": 22.0,
                "save_percentage": None,
                "save_percentage_on_ice": None,
                "saves": None,
                "season": "2022-23",
                "shooting_percentage": 13.9,
                "shooting_percentage_on_ice": 10.4,
                "shootout_attempts": 2,
                "shootout_goals": 2,
                "shootout_misses": 0,
                "shootout_percentage": 100.0,
                "short_handed_assists": 0,
                "short_handed_goals": 0,
                "short_handed_goals_allowed": None,
                "short_handed_save_percentage": None,
                "short_handed_shots_faced": None,
                "shots_against": None,
                "shots_on_goal": 72,
                "shutouts": None,
                "takeaways": 13,
                "team_abbreviation": "MIN",
                "ties_plus_overtime_loss": None,
                "time_on_ice": 376,
                "time_on_ice_even_strength": 376.3,
                "total_goals_against_on_ice": 18,
                "total_goals_for_on_ice": 25,
                "total_shots": 127,
                "weight": 202,
                "wins": None,
            },
            {
                "adjusted_assists": 138,
                "adjusted_goals": 132,
                "adjusted_goals_against_average": None,
                "adjusted_goals_created": 110,
                "adjusted_points": 270,
                "age": None,
                "assists": 51,
                "average_time_on_ice": "19:02",
                "blocks_at_even_strength": 29,
                "corsi_against": 2157.0,
                "corsi_for": 3261.0,
                "corsi_for_percentage": 60.2,
                "defensive_point_shares": 3.7,
                "defensive_zone_start_percentage": 28.0,
                "even_strength_assists": 69,
                "even_strength_goals": 57,
                "even_strength_goals_allowed": None,
                "even_strength_save_percentage": None,
                "even_strength_shots_faced": None,
                "faceoff_losses": 14,
                "faceoff_percentage": 23.5,
                "faceoff_wins": 4,
                "fenwick_against": 1619,
                "fenwick_for": 2478,
                "fenwick_for_percentage": 60.5,
                "game_winning_goals": 10,
                "games_played": 82,
                "giveaways": 63,
                "goal_against_percentage_relative": None,
                "goalie_point_shares": None,
                "goals": 45,
                "goals_against": None,
                "goals_against_average": None,
                "goals_against_on_ice": 126,
                "goals_created": 72,
                "goals_for_on_ice": 225,
                "goals_saved_above_average": None,
                "height": "5-10",
                "hits_at_even_strength": 62,
                "league": "NHL",
                "losses": None,
                "minutes": None,
                "name": "Kirill Kaprizov",
                "offensive_point_shares": 18.0,
                "offensive_zone_start_percentage": 72.0,
                "pdo": 102.0,
                "penalties_in_minutes": 63,
                "player_id": "kapriki01",
                "plus_minus": 32,
                "point_shares": 21.6,
                "points": 95,
                "power_play_assists": 26,
                "power_play_goals": 27,
                "power_play_goals_against_on_ice": 1,
                "power_play_goals_allowed": None,
                "power_play_goals_for_on_ice": 69,
                "power_play_save_percentage": None,
                "power_play_shots_faced": None,
                "quality_start_percentage": None,
                "quality_starts": None,
                "really_bad_starts": None,
                "relative_corsi_for_percentage": 15.9,
                "relative_fenwick_for_percentage": 15.7,
                "save_percentage": None,
                "save_percentage_on_ice": None,
                "saves": None,
                "season": "Career",
                "shooting_percentage": 16.2,
                "shooting_percentage_on_ice": 12.4,
                "shootout_attempts": 9,
                "shootout_goals": 4,
                "shootout_misses": 5,
                "shootout_percentage": 44.4,
                "short_handed_assists": 0,
                "short_handed_goals": 0,
                "short_handed_goals_allowed": None,
                "short_handed_save_percentage": None,
                "short_handed_shots_faced": None,
                "shots_against": None,
                "shots_on_goal": 276,
                "shutouts": None,
                "takeaways": 52,
                "team_abbreviation": None,
                "ties_plus_overtime_loss": None,
                "time_on_ice": 2930,
                "time_on_ice_even_strength": 2930.4,
                "total_goals_against_on_ice": 126,
                "total_goals_for_on_ice": 225,
                "total_shots": 491,
                "weight": 202,
                "wins": None,
            },
        ]
        indices = ["2020-21", "2021-22", "2022-23", "Career"]

        df = pd.DataFrame(dataframe, index=indices)
        player = Player("kapriki01")

        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected on above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, player.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_nhl_404_returns_none_with_no_errors(self, *args, **kwargs):
        player = Player("bad")

        assert player.name is None
        assert player.dataframe is None

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_nhl_404_returns_none_for_different_season(self, *args, **kwargs):
        player = Player("bad")

        assert player.name is None
        assert player.dataframe is None

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_nhl_player_string_representation(self, *args, **kwargs):
        player = Player("kapriki01")

        assert player.__repr__() == "Kirill Kaprizov (kapriki01)"


class TestNHLRoster:
    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_roster_class_pulls_all_player_stats(self, *args, **kwargs):
        flexmock(utils).should_receive("_find_year_for_season").and_return(ROSTER_YEAR)
        roster = Roster(TEAM)

        assert len(roster.players) == 37

        roster_players = [player.name for player in roster.players]
        for player in ["Kirill Kaprizov", "Kaapo Kahkonen"]:
            assert player in roster_players

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_bad_url_raises_value_error(self, *args, **kwargs):
        with pytest.raises(ValueError):
            roster = Roster("bad")

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_roster_from_team_class(self, *args, **kwargs):
        flexmock(Team).should_receive("_parse_team_data").and_return(None)
        team = Team(team_data=None, rank=1, year=ROSTER_YEAR)
        mock_abbreviation = mock.PropertyMock(return_value=TEAM)
        type(team)._abbreviation = mock_abbreviation

        assert len(team.roster.players) == 37

        roster_players = [player.name for player in team.roster.players]
        for player in ["Kirill Kaprizov", "Kaapo Kahkonen"]:
            assert player in roster_players
        type(team)._abbreviation = None

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_roster_class_with_slim_parameter(self, *args, **kwargs):
        flexmock(utils).should_receive("_find_year_for_season").and_return(ROSTER_YEAR)
        roster = Roster(TEAM, slim=True)

        assert len(roster.players) == 37

        assert roster.players == {
            "addisca01": "Calen Addison",
            "beckmad01": "Adam Beckman",
            "bennjo01": "Jordie Benn",
            "bjugsni01": "Nick Bjugstad",
            "boldyma01": "Matt Boldy",
            "brodijo01": "Jonas Brodin",
            "chaffmi01": "Mitchell Chaffee",
            "cramajo01": "Joseph Cramarossa",
            "deslani01": "Nicolas Deslauriers",
            "dewarco01": "Connor Dewar",
            "duhaibr01": "Brandon Duhaime",
            "dumbama01": "Mathew Dumba",
            "eriksjo02": "Joel Eriksson Ek",
            "fialake01": "Kevin Fiala",
            "fleurma01": "Marc-Andre Fleury",
            "foligma01": "Marcus Foligno",
            "gaudrfr01": "Frederick Gaudreau",
            "goligal01": "Alex Goligoski",
            "greenjo02": "Jordan Greenway",
            "hartmry01": "Ryan Hartman",
            "jostty01": "Tyson Jost",
            "kahkoka01": "Kaapo Kahkonen",
            "kapriki01": "Kirill Kaprizov",
            "kulikdm01": "Dmitry Kulikov",
            "lizotjo01": "Jon Lizotte",
            "mermida01": "Dakota Mermis",
            "merrijo01": "Jonathon Merrill",
            "middlja01": "Jacob Middleton",
            "pitlire01": "Rem Pitlick",
            "raskvi01": "Victor Rask",
            "rauky01": "Kyle Rau",
            "rossima01": "Marco Rossi",
            "shawma01": "Mason Shaw",
            "spurgja01": "Jared Spurgeon",
            "sturmni01": "Nico Sturm",
            "talboca01": "Cam Talbot",
            "zuccama01": "Mats Zuccarello",
        }

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_roster_class_string_representation(self, *args, **kwargs):
        expected = """None (addisca01)
None (beckmad01)
None (bennjo01)
None (bjugsni01)
None (boldyma01)
None (brodijo01)
None (chaffmi01)
None (cramajo01)
None (deslani01)
None (dewarco01)
None (duhaibr01)
None (dumbama01)
None (eriksjo02)
None (fialake01)
None (fleurma01)
None (foligma01)
None (gaudrfr01)
None (goligal01)
None (greenjo02)
None (hartmry01)
None (jostty01)
Kaapo Kahkonen (kahkoka01)
Kirill Kaprizov (kapriki01)
None (kulikdm01)
None (lizotjo01)
None (mermida01)
None (merrijo01)
None (middlja01)
None (pitlire01)
None (raskvi01)
None (rauky01)
None (rossima01)
None (shawma01)
None (spurgja01)
None (sturmni01)
None (talboca01)
None (zuccama01)"""

        flexmock(utils).should_receive("_find_year_for_season").and_return(ROSTER_YEAR)
        roster = Roster(TEAM)

        assert roster.__repr__() == expected

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_coach(self, *args, **kwargs):
        assert "Dean Evason" == Roster(TEAM, year=ROSTER_YEAR).coach
