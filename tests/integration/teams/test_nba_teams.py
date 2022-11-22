import mock
import os
import pandas as pd
import pytest
from flexmock import flexmock
from sportsipy import utils
from sportsipy.nba.constants import SEASON_PAGE_URL
from sportsipy.nba.teams import Team, Teams
from ..utils import read_file


MONTH = 1
YEAR = 2022


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


def mock_pyquery(url):
    if 'DEN' in url:
        return read_file('DEN_2022.html', 'nba', 'teams')
    if '2022' in url:
        return read_file('NBA_2022.html', 'nba', 'teams')
    else:
        return None


class MockDateTime:
    def __init__(self, year, month):
        self.year = year
        self.month = month


class TestNBAIntegration:
    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            'abbreviation': 'DEN',
            'assists': 2279,
            'blocks': 305,
            'defensive_rebounds': 2865,
            'field_goal_attempts': 7079,
            'field_goal_percentage': 0.483,
            'field_goals': 3416,
            'free_throw_attempts': 1725,
            'free_throw_percentage': 0.795,
            'free_throws': 1372,
            'games_played': 82,
            'minutes_played': 19805,
            'name': 'Denver Nuggets',
            'offensive_rebounds': 752,
            'opp_assists': 2082,
            'opp_blocks': 392,
            'opp_defensive_rebounds': 2680,
            'opp_field_goal_attempts': 7168,
            'opp_field_goal_percentage': 0.47,
            'opp_field_goals': 3367,
            'opp_free_throw_attempts': 1783,
            'opp_free_throw_percentage': 0.757,
            'opp_free_throws': 1349,
            'opp_offensive_rebounds': 795,
            'opp_personal_fouls': 1632,
            'opp_points': 9054,
            'opp_steals': 649,
            'opp_three_point_field_goal_attempts': 2806,
            'opp_three_point_field_goal_percentage': 0.346,
            'opp_three_point_field_goals': 971,
            'opp_total_rebounds': 3475,
            'opp_turnovers': 1051,
            'opp_two_point_field_goal_attempts': 4362,
            'opp_two_point_field_goal_percentage': 0.549,
            'opp_two_point_field_goals': 2396,
            'personal_fouls': 1639,
            'points': 9243,
            'rank': 10,
            'steals': 592,
            'three_point_field_goal_attempts': 2944,
            'three_point_field_goal_percentage': 0.353,
            'three_point_field_goals': 1039,
            'total_rebounds': 3617,
            'turnovers': 1189,
            'two_point_field_goal_attempts': 4135,
            'two_point_field_goal_percentage': 0.575,
            'two_point_field_goals': 2377
        }
        self.abbreviations = [
            'BOS', 'CLE', 'TOR', 'WAS', 'ATL', 'MIL', 'IND', 'CHI', 'MIA',
            'DET', 'CHO', 'NYK', 'ORL', 'PHI', 'BRK', 'GSW', 'SAS', 'HOU',
            'LAC', 'UTA', 'OKC', 'MEM', 'POR', 'DEN', 'NOP', 'DAL', 'SAC',
            'MIN', 'LAL', 'PHO'
        ]
        flexmock(utils) \
            .should_receive('_todays_date') \
            .and_return(MockDateTime(YEAR, MONTH))

        self.teams = Teams()

    def test_nba_integration_returns_correct_number_of_teams(self):
        assert len(self.teams) == len(self.abbreviations)

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nba_integration_returns_correct_attributes_for_team(self, *args, **kwargs):
        den = self.teams('DEN')

        for attribute, value in self.results.items():
            assert getattr(den, attribute) == value

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nba_integration_returns_correct_team_abbreviations(self, *args, **kwargs):
        for team in self.teams:
            assert team.abbreviation in self.abbreviations

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nba_integration_dataframe_returns_dataframe(self, *args, **kwargs):
        df = pd.DataFrame([self.results], index=['DEN'])

        den = self.teams('DEN')
        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected one above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, den.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_nba_integration_all_teams_dataframe_returns_dataframe(self):
        result = self.teams.dataframes.drop_duplicates(keep=False)

        assert len(result) == len(self.abbreviations)
        assert set(result.columns.values) == set(self.results.keys())

    def test_nba_invalid_team_name_raises_value_error(self):
        with pytest.raises(ValueError):
            self.teams('INVALID_NAME')

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nba_empty_page_returns_no_teams(self, *args, **kwargs):
        flexmock(utils) \
            .should_receive('_no_data_found') \
            .once()
        flexmock(utils) \
            .should_receive('_get_stats_table') \
            .and_return(None)

        teams = Teams()

        assert len(teams) == 0

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_pulling_team_directly(self, *args, **kwargs):
        den = Team('DEN')

        for attribute, value in self.results.items():
            assert getattr(den, attribute) == value

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_team_string_representation(self, *args, **kwargs):
        den = Team('DEN')

        assert den.__repr__() == 'Denver Nuggets (DEN) - 2022'

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_teams_string_representation(self, *args, **kwargs):
        expected = """Minnesota Timberwolves (MIN)
Memphis Grizzlies (MEM)
Milwaukee Bucks (MIL)
Charlotte Hornets (CHO)
Phoenix Suns (PHO)
Atlanta Hawks (ATL)
Utah Jazz (UTA)
San Antonio Spurs (SAS)
Brooklyn Nets (BRK)
Denver Nuggets (DEN)
Los Angeles Lakers (LAL)
Boston Celtics (BOS)
Chicago Bulls (CHI)
Indiana Pacers (IND)
Golden State Warriors (GSW)
Sacramento Kings (SAC)
Miami Heat (MIA)
Philadelphia 76ers (PHI)
Houston Rockets (HOU)
Toronto Raptors (TOR)
New Orleans Pelicans (NOP)
Washington Wizards (WAS)
Los Angeles Clippers (LAC)
Dallas Mavericks (DAL)
Cleveland Cavaliers (CLE)
New York Knicks (NYK)
Portland Trail Blazers (POR)
Detroit Pistons (DET)
Orlando Magic (ORL)
Oklahoma City Thunder (OKC)"""

        teams = Teams()
        assert teams.__repr__() == expected
