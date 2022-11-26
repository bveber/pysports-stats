import mock
import os
import pandas as pd
import pytest
from flexmock import flexmock
from sports import utils
from sports.nhl.constants import SEASON_PAGE_URL
from sports.nhl.teams import Team, Teams
from ..utils import read_file


MONTH = 1
YEAR = 2022
TEAM = "MIN"


def mock_pyquery(url):
    if "NHL_%s.html" % YEAR in url:
        return read_file("NHL_%s.html" % YEAR, "nhl", "teams")
    return None


def mock_request(url):
    class MockRequest:
        def __init__(self, html_contents, status_code=200):
            self.status_code = status_code
            self.html_contents = html_contents
            self.text = html_contents

    if str(YEAR) in url:
        return MockRequest("good")
    else:
        return MockRequest("bad", status_code=404)


class MockDateTime:
    def __init__(self, year, month):
        self.year = year
        self.month = month


class TestNHLIntegration:
    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            "abbreviation": "MIN",
            "average_age": 29.4,
            "games_played": 82,
            "goals_against": 249,
            "goals_for": 305,
            "losses": 22,
            "name": "Minnesota Wild",
            "overtime_losses": 7,
            "pdo_at_even_strength": 101.9,
            "penalty_killing_percentage": 76.14,
            "points": 113,
            "points_percentage": 0.689,
            "power_play_goals": 53,
            "power_play_goals_against": 63,
            "power_play_opportunities": 258,
            "power_play_opportunities_against": 264,
            "power_play_percentage": 20.54,
            "rank": 5,
            "save_percentage": 0.903,
            "shooting_percentage": 11.4,
            "short_handed_goals": 2,
            "short_handed_goals_against": 5,
            "shots_against": 2577,
            "shots_on_goal": 2666,
            "simple_rating_system": 0.68,
            "strength_of_schedule": -0.02,
            "total_goals_per_game": 3.72,
            "wins": 53,
        }
        self.abbreviations = [
            "FLA",
            "COL",
            "CAR",
            "TOR",
            "MIN",
            "CGY",
            "TBL",
            "NYR",
            "STL",
            "BOS",
            "EDM",
            "PIT",
            "WSH",
            "LAK",
            "DAL",
            "NSH",
            "VEG",
            "VAN",
            "WPG",
            "NYI",
            "CBJ",
            "SJS",
            "ANA",
            "BUF",
            "DET",
            "OTT",
            "CHI",
            "NJD",
            "PHI",
            "SEA",
            "ARI",
            "MTL",
        ]

        flexmock(utils).should_receive("_todays_date").and_return(
            MockDateTime(YEAR, MONTH)
        )

        self.teams = Teams()

    def test_nhl_integration_returns_correct_number_of_teams(self):
        assert len(self.teams) == len(self.abbreviations)

    def test_nhl_integration_returns_correct_attributes_for_team(self):
        team = self.teams(TEAM)

        for attribute, value in self.results.items():
            assert getattr(team, attribute) == value

    def test_nhl_integration_returns_correct_team_abbreviations(self):
        for team in self.teams:
            assert team.abbreviation in self.abbreviations

    def test_nhl_integration_dataframe_returns_dataframe(self):
        df = pd.DataFrame([self.results], index=[TEAM])

        team = self.teams(TEAM)
        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected one above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, team.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_nhl_integration_all_teams_dataframe_returns_dataframe(self):
        result = self.teams.dataframes.drop_duplicates(keep=False)

        assert len(result) == len(self.abbreviations)
        assert set(result.columns.values) == set(self.results.keys())

    def test_nhl_invalid_team_name_raises_value_error(self):
        with pytest.raises(ValueError):
            self.teams("INVALID_NAME")

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_nhl_empty_page_returns_no_teams(self, *args, **kwargs):
        flexmock(utils).should_receive("_no_data_found").once()
        flexmock(utils).should_receive("_get_stats_table").and_return(None)

        teams = Teams()

        assert len(teams) == 0

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_pulling_team_directly(self, *args, **kwargs):
        team = Team(TEAM)

        for attribute, value in self.results.items():
            assert getattr(team, attribute) == value

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_team_string_representation(self, *args, **kwargs):
        team = Team(TEAM)

        assert team.__repr__() == "Minnesota Wild (MIN) - 2022"

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_teams_string_representation(self, *args, **kwargs):
        expected = """Florida Panthers (FLA)
Colorado Avalanche (COL)
Carolina Hurricanes (CAR)
Toronto Maple Leafs (TOR)
Minnesota Wild (MIN)
Calgary Flames (CGY)
Tampa Bay Lightning (TBL)
New York Rangers (NYR)
St. Louis Blues (STL)
Boston Bruins (BOS)
Edmonton Oilers (EDM)
Pittsburgh Penguins (PIT)
Washington Capitals (WSH)
Los Angeles Kings (LAK)
Dallas Stars (DAL)
Nashville Predators (NSH)
Vegas Golden Knights (VEG)
Vancouver Canucks (VAN)
Winnipeg Jets (WPG)
New York Islanders (NYI)
Columbus Blue Jackets (CBJ)
San Jose Sharks (SJS)
Anaheim Ducks (ANA)
Buffalo Sabres (BUF)
Detroit Red Wings (DET)
Ottawa Senators (OTT)
Chicago Blackhawks (CHI)
New Jersey Devils (NJD)
Philadelphia Flyers (PHI)
Seattle Kraken (SEA)
Arizona Coyotes (ARI)
Montreal Canadiens (MTL)"""

        teams = Teams()

        assert teams.__repr__() == expected
