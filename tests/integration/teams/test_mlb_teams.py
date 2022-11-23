import mock
import os
import pandas as pd
import pytest
from flexmock import flexmock
from sportsipy import utils
from sportsipy.mlb.constants import STANDINGS_URL, TEAM_STATS_URL
from sportsipy.mlb.teams import Team, Teams
from ..utils import read_file


MONTH = 4
YEAR = 2022
TEAM = 'HOU'


def mock_pyquery(url):
    if 'standings' in url:
        return read_file('2022-standings.shtml', 'mlb', 'teams')
    if 'overall' in url:
        return read_file('2022-overall.html', 'mlb', 'teams')
    if 'pitching' in url:
        return read_file('2022-pitching.html', 'mlb', 'teams')
    if 'batting' in url:
        return read_file('2022-batting.html', 'mlb', 'teams')
    if 'HOU/2022' in url:
        return read_file('HOU-2022.shtml', 'mlb', 'teams')
    if 'MLB/2022' in url:
        return read_file('2022.html', 'mlb', 'teams')
    return None


def mock_request(url):
    class MockRequest:
        def __init__(self, html_contents, status_code=200):
            self.status_code = status_code
            self.html_contents = html_contents
            self.text = html_contents

    if str(YEAR) in url:
        return MockRequest('good')
    else:
        return MockRequest('bad', status_code=404)


class MockDateTime:
    def __init__(self, year, month):
        self.year = year
        self.month = month


class TestMLBIntegration:
    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            'abbreviation': 'HOU',
            'at_bats': 5409,
            'average_batter_age': 29.3,
            'average_pitcher_age': 29.4,
            'away_losses': 30,
            'away_record': '51-30',
            'away_wins': 51,
            'balks': 6,
            'bases_on_balls': 528,
            'bases_on_walks_given': 458,
            'bases_on_walks_given_per_nine_innings': 2.9,
            'batters_faced': 5856,
            'batting_average': 0.248,
            'complete_game_shutouts': 1,
            'complete_games': 3,
            'doubles': 284,
            'earned_runs_against': 2.9,
            'earned_runs_against_plus': 134,
            'extra_inning_losses': 6,
            'extra_inning_record': '5-6',
            'extra_inning_wins': 5,
            'fielding_independent_pitching': 3.28,
            'games': 162,
            'games_finished': 159,
            'grounded_into_double_plays': 118,
            'hit_pitcher': 60,
            'hits': 1341,
            'hits_allowed': 1121,
            'hits_per_nine_innings': 7.0,
            'home_losses': 26,
            'home_record': '55-26',
            'home_runs': 214,
            'home_runs_against': 134,
            'home_runs_per_nine_innings': 0.8,
            'home_wins': 55,
            'innings_pitched': 1445.1,
            'intentional_bases_on_balls': 18,
            'interleague_record': '12-8',
            'last_ten_games_record': '7-3',
            'last_thirty_games_record': '21-9',
            'last_twenty_games_record': '14-6',
            'league': None,
            'losses': 56,
            'losses_last_ten_games': 3,
            'losses_last_thirty_games': 9,
            'losses_last_twenty_games': 6,
            'losses_vs_left_handed_pitchers': 12,
            'losses_vs_right_handed_pitchers': 44,
            'losses_vs_teams_over_500': 27,
            'losses_vs_teams_under_500': 29,
            'luck': 0,
            'name': 'Houston Astros',
            'number_of_pitchers': 22,
            'number_players_used': 45,
            'on_base_percentage': 0.319,
            'on_base_plus_slugging_percentage': 0.743,
            'on_base_plus_slugging_percentage_plus': 111,
            'opposing_runners_left_on_base': 1017,
            'plate_appearances': 6054,
            'pythagorean_win_loss': '106-56',
            'rank': 2,
            'record_vs_left_handed_pitchers': '42-12',
            'record_vs_right_handed_pitchers': '64-44',
            'record_vs_teams_over_500': '42-27',
            'record_vs_teams_under_500': '64-29',
            'run_difference': 1.4,
            'runners_left_on_base': 1068,
            'runs': 4.5,
            'runs_against': 3.2,
            'runs_allowed_per_game': 3.2,
            'runs_batted_in': 715,
            'sacrifice_flies': 42,
            'sacrifice_hits': 9,
            'saves': 53,
            'shutouts': 18,
            'simple_rating_system': 1.3,
            'single_run_losses': 16,
            'single_run_record': '28-16',
            'single_run_wins': 28,
            'slugging_percentage': 0.424,
            'stolen_bases': 83,
            'streak': 'W 2',
            'strength_of_schedule': -0.1,
            'strikeouts': 1524,
            'strikeouts_per_base_on_balls': 3.33,
            'strikeouts_per_nine_innings': 9.5,
            'times_caught_stealing': 22,
            'times_hit_by_pitch': 60,
            'times_struck_out': 1179,
            'total_bases': 2293,
            'total_runs': 737,
            'triples': 13,
            'whip': 1.092,
            'wild_pitches': 56,
            'win_percentage': 0.654,
            'wins': 106,
            'wins_last_ten_games': 7,
            'wins_last_thirty_games': 21,
            'wins_last_twenty_games': 14,
            'wins_vs_left_handed_pitchers': 42,
            'wins_vs_right_handed_pitchers': 64,
            'wins_vs_teams_over_500': 42,
            'wins_vs_teams_under_500': 64
        }
        self.abbreviations = [
            'LAD',
            'HOU',
            'ATL',
            'NYM',
            'NYY',
            'STL',
            'CLE',
            'TOR',
            'SEA',
            'SDP',
            'PHI',
            'MIL',
            'TBR',
            'BAL',
            'CHW',
            'SFG',
            'MIN',
            'BOS',
            'CHC',
            'ARI',
            'LAA',
            'MIA',
            'TEX',
            'COL',
            'DET',
            'KCR',
            'PIT',
            'CIN',
            'OAK',
            'WSN'
        ]

        flexmock(utils) \
            .should_receive('_todays_date') \
            .and_return(MockDateTime(YEAR, MONTH))

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_mlb_integration_returns_correct_number_of_teams(self, *args,
                                                             **kwargs):
        teams = Teams(YEAR)

        assert len(teams) == len(self.abbreviations)

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_mlb_integration_returns_correct_attributes_for_team(self,
                                                                 *args,
                                                                 **kwargs):
        teams = Teams(YEAR)

        team = teams(TEAM)

        for attribute, value in self.results.items():
            assert getattr(team, attribute) == value

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_mlb_integration_returns_correct_team_abbreviations(self,
                                                                *args,
                                                                **kwargs):
        teams = Teams(YEAR)

        for team in teams:
            assert team.abbreviation in self.abbreviations

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_mlb_integration_dataframe_returns_dataframe(self, *args,
                                                         **kwargs):
        teams = Teams(YEAR)
        df = pd.DataFrame([self.results], index=[TEAM])

        houston = teams(TEAM)
        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected one above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, houston.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_mlb_integration_all_teams_dataframe_returns_dataframe(self,
                                                                   *args,
                                                                   **kwargs):
        teams = Teams(YEAR)
        result = teams.dataframes.drop_duplicates(keep=False)

        assert len(result) == len(self.abbreviations)
        assert set(result.columns.values) == set(self.results.keys())

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_pulling_team_directly(self, *args, **kwargs):
        hou = Team(TEAM)

        for attribute, value in self.results.items():
            assert getattr(hou, attribute) == value

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_mlb_invalid_team_name_raises_value_error(self, *args, **kwargs):
        teams = Teams(YEAR)

        with pytest.raises(ValueError):
            teams('INVALID_NAME')

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_mlb_empty_page_returns_no_teams(self, *args, **kwargs):
        flexmock(utils) \
            .should_receive('_no_data_found') \
            .once()
        flexmock(utils) \
            .should_receive('_get_stats_table') \
            .and_return(None)

        teams = Teams(YEAR)

        assert len(teams) == 0

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_mlb_team_string_representation(self, *args, **kwargs):
        hou = Team(TEAM)

        assert hou.__repr__() == 'Houston Astros (HOU) - 2022'

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_mlb_teams_string_representation(self, *args, **kwargs):
        expected = """Los Angeles Dodgers (LAD)
Houston Astros (HOU)
Atlanta Braves (ATL)
New York Mets (NYM)
New York Yankees (NYY)
St. Louis Cardinals (STL)
Cleveland Guardians (CLE)
Toronto Blue Jays (TOR)
Seattle Mariners (SEA)
San Diego Padres (SDP)
Philadelphia Phillies (PHI)
Milwaukee Brewers (MIL)
Tampa Bay Rays (TBR)
Baltimore Orioles (BAL)
Chicago White Sox (CHW)
San Francisco Giants (SFG)
Minnesota Twins (MIN)
Boston Red Sox (BOS)
Chicago Cubs (CHC)
Arizona Diamondbacks (ARI)
Los Angeles Angels (LAA)
Miami Marlins (MIA)
Texas Rangers (TEX)
Colorado Rockies (COL)
Detroit Tigers (DET)
Kansas City Royals (KCR)
Pittsburgh Pirates (PIT)
Cincinnati Reds (CIN)
Oakland Athletics (OAK)
Washington Nationals (WSN)"""

        teams = Teams()

        assert teams.__repr__() == expected
