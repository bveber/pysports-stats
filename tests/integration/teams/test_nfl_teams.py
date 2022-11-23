import mock
import os
import pandas as pd
import pytest
from flexmock import flexmock
from sports import utils
from sports.constants import LOSS
from sports.nfl.constants import LOST_WILD_CARD, SEASON_PAGE_URL
from sports.nfl.teams import Team, Teams
from ..utils import read_file
from pyquery import PyQuery as pq


MONTH = 9
YEAR = 2017

SEASON_PAGE = 'tests/integration/teams/nfl/2017.html'

def mock_pyquery(url):
    if 'years/2017/' in url:
        return read_file('2017.html', 'nfl', 'teams')
    if 'kan' in url:
        return read_file('kan-2017.html', 'nfl', 'teams')
    return read_file('kan-2017.html', 'nfl', 'teams')


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


class MockSchedule:
    def __init__(self, abbreviation, year):
        self.result = LOSS
        self.week = 18

    def __getitem__(self, index):
        return self


class TestNFLIntegration:
    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            'rank': 6,
            'abbreviation': 'KAN',
            'name': 'Kansas City Chiefs',
            'wins': 10,
            'losses': 6,
            'win_percentage': .625,
            'post_season_result': LOST_WILD_CARD,
            'games_played': 16,
            'points_for': 415,
            'points_against': 339,
            'points_difference': 76,
            'margin_of_victory': 4.8,
            'strength_of_schedule': -1.3,
            'simple_rating_system': 3.4,
            'offensive_simple_rating_system': 3.8,
            'defensive_simple_rating_system': -0.3,
            'yards': 6007,
            'plays': 985,
            'yards_per_play': 6.1,
            'turnovers': 11,
            'fumbles': 3,
            'first_downs': 322,
            'pass_completions': 363,
            'pass_attempts': 543,
            'pass_yards': 4104,
            'pass_touchdowns': 26,
            'interceptions': 8,
            'pass_net_yards_per_attempt': 7.1,
            'pass_first_downs': 198,
            'rush_attempts': 405,
            'rush_yards': 1903,
            'rush_touchdowns': 12,
            'rush_yards_per_attempt': 4.7,
            'rush_first_downs': 95,
            'penalties': 118,
            'yards_from_penalties': 1044,
            'first_downs_from_penalties': 29,
            'percent_drives_with_points': 44.9,
            'percent_drives_with_turnovers': 6.3,
            'points_contributed_by_offense': -22.58
        }
        self.abbreviations = [
            'RAM', 'NWE', 'PHI', 'NOR', 'JAX', 'KAN', 'DET', 'PIT', 'RAV',
            'MIN', 'SEA', 'CAR', 'SDG', 'DAL', 'ATL', 'WAS', 'HTX', 'TAM',
            'OTI', 'SFO', 'GNB', 'BUF', 'RAI', 'NYJ', 'CRD', 'CIN', 'DEN',
            'MIA', 'CHI', 'CLT', 'NYG', 'CLE'
        ]
        flexmock(utils) \
            .should_receive('_todays_date') \
            .and_return(MockDateTime(YEAR, MONTH))

        self.teams = Teams(season_page = SEASON_PAGE)

    def test_nfl_integration_returns_correct_number_of_teams(self):
        assert len(self.teams) == len(self.abbreviations)

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_integration_returns_correct_attributes_for_team(self, *args, **kwargs):
        kansas = self.teams('KAN')

        for attribute, value in self.results.items():
            assert getattr(kansas, attribute) == value

    def test_nfl_integration_returns_correct_team_abbreviations(self):
        for team in self.teams:
            assert team.abbreviation in self.abbreviations

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_integration_dataframe_returns_dataframe(self, *args, **kwargs):
        df = pd.DataFrame([self.results], index=['KAN'])

        kansas = self.teams('KAN')
        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected one above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, kansas.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_integration_all_teams_dataframe_returns_dataframe(self, *args, **kwargs):
        result = self.teams.dataframes.drop_duplicates(keep=False)

        assert len(result) == len(self.abbreviations)
        assert set(result.columns.values) == set(self.results.keys())

    def test_nfl_invalid_team_name_raises_value_error(self):
        with pytest.raises(ValueError):
            self.teams('INVALID_NAME')

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_empty_page_returns_no_teams(self, *args, **kwargs):
        flexmock(utils) \
            .should_receive('_no_data_found') \
            .once()
        flexmock(utils) \
            .should_receive('_get_stats_table') \
            .and_return(None)

        teams = Teams()

        assert len(teams) == 0

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_pulling_team_directly(self, *args, **kwargs):
        schedule = MockSchedule(None, None)

        flexmock(Team) \
            .should_receive('schedule') \
            .and_return(schedule)

        kansas = Team('KAN')

        for attribute, value in self.results.items():
            assert getattr(kansas, attribute) == value

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_team_string_representation(self, *args, **kwargs):
        kansas = Team('KAN')

        assert kansas.__repr__() == 'Kansas City Chiefs (KAN) - 2017'

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_teams_string_representation(self, *args, **kwargs):
        expected = """Los Angeles Rams (RAM)
New England Patriots (NWE)
Philadelphia Eagles (PHI)
New Orleans Saints (NOR)
Jacksonville Jaguars (JAX)
Kansas City Chiefs (KAN)
Detroit Lions (DET)
Pittsburgh Steelers (PIT)
Baltimore Ravens (RAV)
Minnesota Vikings (MIN)
Seattle Seahawks (SEA)
Carolina Panthers (CAR)
Los Angeles Chargers (SDG)
Dallas Cowboys (DAL)
Atlanta Falcons (ATL)
Washington Redskins (WAS)
Houston Texans (HTX)
Tampa Bay Buccaneers (TAM)
Tennessee Titans (OTI)
San Francisco 49ers (SFO)
Green Bay Packers (GNB)
Buffalo Bills (BUF)
Oakland Raiders (RAI)
New York Jets (NYJ)
Arizona Cardinals (CRD)
Cincinnati Bengals (CIN)
Denver Broncos (DEN)
Miami Dolphins (MIA)
Chicago Bears (CHI)
Indianapolis Colts (CLT)
New York Giants (NYG)
Cleveland Browns (CLE)"""

        teams = Teams()

        assert teams.__repr__() == expected


class TestNFLIntegrationInvalidYear:
    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    @mock.patch('requests.head', side_effect=mock_request)
    def test_invalid_default_year_reverts_to_previous_year(self,
                                                           *args,
                                                           **kwargs):
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return(2018)

        teams = Teams(season_page=SEASON_PAGE)

        for team in teams:
            assert team._year == '2017'
