import mock
import pandas as pd
from flexmock import flexmock
from os import path
from pyquery import PyQuery as pq
from sports.fb.roster import Roster
from ..utils import read_file


EXPECTED_NUM_PLAYERS = 25


def mock_pyquery(url):
    if "361ca564" in url:
        return read_file("tottenham-hotspur-2022-2023.html", "fb", "roster")
    return None


class TestFBRoster:
    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            "name": "Harry Kane",
            "player_id": "21a66f6a",
            "nationality": "England",
            "position": "FW",
            "age": 29,
            "matches_played": 15,
            "starts": 15,
            "minutes": 1335,
            "goals": 12,
            "assists": 1,
            "penalty_kicks": 2,
            "penalty_kick_attempts": 3,
            "yellow_cards": 4,
            "red_cards": 0,
            "goals_per_90": 0.81,
            "assists_per_90": 0.07,
            "goals_and_assists_per_90": 0.88,
            "goals_non_penalty_per_90": 0.67,
            "goals_and_assists_non_penalty_per_90": 0.74,
            "expected_goals": 9.4,
            "expected_goals_non_penalty": 7.1,
            "expected_assists": 2.4,
            "expected_goals_per_90": 0.64,
            "expected_assists_per_90": 0.16,
            "expected_goals_and_assists_per_90": 0.8,
            "expected_goals_non_penalty_per_90": 0.48,
            "expected_goals_and_assists_non_penalty_per_90": 0.64,
            "own_goals": 0,
            "goals_against": None,
            "own_goals_against": None,
            "goals_against_per_90": None,
            "shots_on_target_against": None,
            "saves": None,
            "save_percentage": None,
            "wins": None,
            "draws": None,
            "losses": None,
            "clean_sheets": None,
            "clean_sheet_percentage": None,
            "penalty_kicks_attempted": None,
            "penalty_kicks_allowed": None,
            "penalty_kicks_saved": None,
            "penalty_kicks_missed": None,
            "free_kick_goals_against": None,
            "corner_kick_goals_against": None,
            "post_shot_expected_goals": None,
            "post_shot_expected_goals_per_shot": None,
            "post_shot_expected_goals_minus_allowed": None,
            "launches_completed": None,
            "launches_attempted": None,
            "launch_completion_percentage": None,
            "keeper_passes_attempted": None,
            "throws_attempted": None,
            "launch_percentage": None,
            "average_keeper_pass_length": None,
            "goal_kicks_attempted": None,
            "goal_kick_launch_percentage": None,
            "average_goal_kick_length": None,
            "opponent_cross_attempts": None,
            "opponent_cross_stops": None,
            "opponent_cross_stop_percentage": None,
            "keeper_actions_outside_penalty_area": None,
            "keeper_actions_outside_penalty_area_per_90": None,
            "average_keeper_action_outside_penalty_distance": None,
            "shots": 52,
            "shots_on_target": 24,
            "free_kick_shots": 0,
            "shots_on_target_percentage": 46.2,
            "shots_per_90": 3.51,
            "shots_on_target_per_90": 1.62,
            "goals_per_shot": 0.19,
            "goals_per_shot_on_target": 0.42,
            "expected_goals_non_penalty_per_shot": 0.14,
            "goals_minus_expected": 2.6,
            "non_penalty_minus_expected_non_penalty": 2.9,
            "assists_minus_expected": -1.4,
            "key_passes": 28,
            "passes_completed": 258,
            "passes_attempted": 366,
            "pass_completion": 70.5,
            "short_passes_completed": 124,
            "short_passes_attempted": 156,
            "short_pass_completion": 79.5,
            "medium_passes_completed": 88,
            "medium_passes_attempted": 117,
            "medium_pass_completion": 75.2,
            "long_passes_completed": 39,
            "long_passes_attempted": 57,
            "long_pass_completion": 68.4,
            "left_foot_passes": None,
            "right_foot_passes": None,
            "free_kick_passes": 5,
            "through_balls": 3,
            "corner_kicks": 0,
            "throw_ins": 13,
            "final_third_passes": 41,
            "penalty_area_passes": 22,
            "penalty_area_crosses": 4,
            "minutes_per_match": 89,
            "minutes_played_percentage": 98.9,
            "nineties_played": 14.8,
            "minutes_per_start": 89,
            "subs": 0,
            "minutes_per_sub": None,
            "unused_sub": 0,
            "points_per_match": 1.93,
            "goals_scored_on_pitch": 31,
            "goals_against_on_pitch": 20,
            "goal_difference_on_pitch": 11,
            "goal_difference_on_pitch_per_90": 0.74,
            "net_difference_on_pitch_per_90": 6.74,
            "expected_goals_on_pitch": 23.9,
            "expected_goals_against_on_pitch": 16.3,
            "expected_goal_difference": 7.6,
            "expected_goal_difference_per_90": 0.51,
            "net_expected_goal_difference_per_90": 0.81,
            "soft_reds": 0,
            "fouls_committed": 10,
            "fouls_drawn": 21,
            "offsides": 3,
            "crosses": 19,
            "tackles_won": 4,
            "interceptions": 1,
            "penalty_kicks_won": 1,
            "penalty_kicks_conceded": 0,
            "successful_dribbles": 13,
            "attempted_dribbles": 44,
            "dribble_success_rate": 29.5,
            "players_dribbled_past": None,
            "nutmegs": None,
            "dribblers_tackled": 1,
            "dribblers_contested": 5,
            "tackle_percentage": 20.0,
            "times_dribbled_past": 4,
        }
        self.keeper = {
            "name": "Hugo Lloris",
            "player_id": "8f62b6ee",
            "nationality": "France",
            "position": "GK",
            "age": 35,
            "matches_played": 15,
            "starts": 15,
            "minutes": 1350,
            "goals": 0,
            "assists": 0,
            "penalty_kicks": 0,
            "penalty_kick_attempts": 0,
            "yellow_cards": 0,
            "red_cards": 0,
            "goals_per_90": 0.0,
            "assists_per_90": 0.0,
            "goals_and_assists_per_90": 0.0,
            "goals_non_penalty_per_90": 0.0,
            "goals_and_assists_non_penalty_per_90": 0.0,
            "expected_goals": 0.0,
            "expected_goals_non_penalty": 0.0,
            "expected_assists": 0.0,
            "expected_goals_per_90": 0.0,
            "expected_assists_per_90": 0.0,
            "expected_goals_and_assists_per_90": 0.0,
            "expected_goals_non_penalty_per_90": 0.0,
            "expected_goals_and_assists_non_penalty_per_90": 0.0,
            "own_goals": 0,
            "goals_against": 21,
            "own_goals_against": 0,
            "goals_against_per_90": 1.4,
            "shots_on_target_against": 66,
            "saves": 45,
            "save_percentage": 69.7,
            "wins": 9,
            "draws": 2,
            "losses": 4,
            "clean_sheets": 4,
            "clean_sheet_percentage": 26.7,
            "penalty_kicks_attempted": 1,
            "penalty_kicks_allowed": 1,
            "penalty_kicks_saved": 0,
            "penalty_kicks_missed": 0,
            "free_kick_goals_against": 0,
            "corner_kick_goals_against": 2,
            "post_shot_expected_goals": 18.1,
            "post_shot_expected_goals_per_shot": 0.26,
            "post_shot_expected_goals_minus_allowed": -2.9,
            "launches_completed": 49,
            "launches_attempted": 123,
            "launch_completion_percentage": 39.8,
            "keeper_passes_attempted": 323,
            "throws_attempted": 65,
            "launch_percentage": 30.3,
            "average_keeper_pass_length": 31.1,
            "goal_kicks_attempted": 119,
            "goal_kick_launch_percentage": 21.0,
            "average_goal_kick_length": 24.3,
            "opponent_cross_attempts": 186,
            "opponent_cross_stops": 12,
            "opponent_cross_stop_percentage": 6.5,
            "keeper_actions_outside_penalty_area": 20,
            "keeper_actions_outside_penalty_area_per_90": 1.33,
            "average_keeper_action_outside_penalty_distance": 14.4,
            "shots": 0,
            "shots_on_target": 0,
            "free_kick_shots": 0,
            "shots_on_target_percentage": None,
            "shots_per_90": 0.0,
            "shots_on_target_per_90": 0.0,
            "goals_per_shot": None,
            "goals_per_shot_on_target": None,
            "expected_goals_non_penalty_per_shot": None,
            "goals_minus_expected": 0.0,
            "non_penalty_minus_expected_non_penalty": 0.0,
            "assists_minus_expected": 0.0,
            "key_passes": 0,
            "passes_completed": 356,
            "passes_attempted": 444,
            "pass_completion": 80.2,
            "short_passes_completed": 108,
            "short_passes_attempted": 110,
            "short_pass_completion": 98.2,
            "medium_passes_completed": 150,
            "medium_passes_attempted": 150,
            "medium_pass_completion": 100.0,
            "long_passes_completed": 98,
            "long_passes_attempted": 181,
            "long_pass_completion": 54.1,
            "left_foot_passes": None,
            "right_foot_passes": None,
            "free_kick_passes": 9,
            "through_balls": 0,
            "corner_kicks": 0,
            "throw_ins": 0,
            "final_third_passes": 7,
            "penalty_area_passes": 0,
            "penalty_area_crosses": 0,
            "minutes_per_match": 90,
            "minutes_played_percentage": 100.0,
            "nineties_played": 15.0,
            "minutes_per_start": 90,
            "subs": 0,
            "minutes_per_sub": None,
            "unused_sub": 0,
            "points_per_match": 1.93,
            "goals_scored_on_pitch": 31,
            "goals_against_on_pitch": 21,
            "goal_difference_on_pitch": 10,
            "goal_difference_on_pitch_per_90": 0.67,
            "net_difference_on_pitch_per_90": None,
            "expected_goals_on_pitch": 24.1,
            "expected_goals_against_on_pitch": 16.5,
            "expected_goal_difference": 7.6,
            "expected_goal_difference_per_90": 0.5,
            "net_expected_goal_difference_per_90": None,
            "soft_reds": 0,
            "fouls_committed": 0,
            "fouls_drawn": 2,
            "offsides": 0,
            "crosses": 0,
            "tackles_won": 1,
            "interceptions": 0,
            "penalty_kicks_won": 0,
            "penalty_kicks_conceded": 0,
            "successful_dribbles": 0,
            "attempted_dribbles": 0,
            "dribble_success_rate": None,
            "players_dribbled_past": None,
            "nutmegs": None,
            "dribblers_tackled": 1,
            "dribblers_contested": 1,
            "tackle_percentage": 100.0,
            "times_dribbled_past": 0,
        }

        self.roster = Roster("Tottenham Hotspur")

    def test_outfield_player_roster_returns_expected_stats(self):
        harry_kane = self.roster("Harry Kane")

        for attribute, value in self.results.items():
            assert getattr(harry_kane, attribute) == value

    def test_keeper_player_roster_returns_expected_stats(self):
        hugo_lloris = self.roster("Hugo Lloris")

        for attribute, value in self.keeper.items():
            assert getattr(hugo_lloris, attribute) == value

    def test_outfield_player_id_returns_expected_player(self):
        harry_kane = self.roster("21a66f6a")

        for attribute, value in self.results.items():
            assert getattr(harry_kane, attribute) == value

    def test_number_of_players_returns_expected(self):
        for count, player in enumerate(self.roster):
            pass

        assert count + 1 == EXPECTED_NUM_PLAYERS

    def test_roster_len_returns_expected_roster_size(self):
        assert len(self.roster) == EXPECTED_NUM_PLAYERS

    def test_fb_roster_dataframe_returns_dataframe(self):
        df = pd.DataFrame([self.results], index=["21a66f6a"])

        harry_kane = self.roster("Harry Kane")
        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected on above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, harry_kane.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_fb_invalid_tables_returns_nothing(self, *args, **kwargs):
        roster = Roster("Tottenham Hotspur")
        stats = roster._pull_stats(pq("<div></div>"))

        assert stats == {}

    def test_fb_roster_string_representation(self):
        expected = """Hugo Lloris (8f62b6ee)
Harry Kane (21a66f6a)
Eric Dier (ac861941)
Pierre Højbjerg (8b04d6c1)
Rodrigo Bentancur (3b8674e6)
Son Heung-min (92e7e919)
Ben Davies (44781702)
Emerson (df8b52a5)
Ivan Perišić (6fe90922)
Ryan Sessegnon (6aa3e78b)
Cristian Romero (a3d94a58)
Dejan Kulusevski (df3cda47)
Clément Lenglet (4f28a6ff)
Yves Bissouma (6c203af0)
Davinson Sánchez (da7b447d)
Richarlison (fa031b34)
Matt Doherty (d557d734)
Oliver Skipp (6250083a)
Lucas Moura (2b622f01)
Bryan (7b5ab7f2)
Djed Spence (9bc9a519)
Fraser Forster (c3e39f12)
Pape Matar Sarr (feb5d972)
Japhet Tanganga (e9971f2d)
Harvey White (4d90ce8c)"""
        # repr encoded to deal with string equality bug with latin letters

        assert self.roster.__repr__() == expected

    def test_fb_player_string_representation(self):
        player = self.roster("Harry Kane")

        assert player.__repr__() == "Harry Kane (21a66f6a)"
