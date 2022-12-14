import mock
import os
import pandas as pd
import pytest
from flexmock import flexmock
from sports import utils
from sports.ncaaf.conferences import Conferences
from sports.ncaaf.constants import (
    OFFENSIVE_STATS_URL,
    DEFENSIVE_STATS_URL,
    SEASON_PAGE_URL,
    CONFERENCE_DICT,
)
from sports.ncaaf.teams import Team, Teams
from ..utils import read_file


MONTH = 9
YEAR = 2021
TEAM = "PURDUE"


def mock_pyquery(url):
    if url == OFFENSIVE_STATS_URL % YEAR:
        return read_file("2021-team-offense.html", "ncaaf", "teams")
    if url == DEFENSIVE_STATS_URL % YEAR:
        return read_file("2021-team-defense.html", "ncaaf", "teams")
    if url == SEASON_PAGE_URL % YEAR:
        return read_file("2021-standings.html", "ncaaf", "teams")
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


@pytest.fixture(scope="session")
@mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
def teams(*args, **kwargs):

    flexmock(utils).should_receive("_todays_date").and_return(MockDateTime(YEAR, MONTH))

    return Teams(YEAR)


@pytest.fixture(scope="session")
@mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
def team(*args, **kwargs):

    flexmock(utils).should_receive("_todays_date").and_return(MockDateTime(YEAR, MONTH))

    return Team(TEAM)


class TestNCAAFIntegration:
    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            "abbreviation": "PURDUE",
            "conference": "big-ten",
            "conference_losses": 3,
            "conference_win_percentage": 0.667,
            "conference_wins": 6,
            "first_downs": 24.0,
            "opponents_first_downs": 18.4,
            "first_downs_from_penalties": 1.9,
            "opponents_first_downs_from_penalties": 1.6,
            "fumbles_lost": 0.5,
            "opponents_fumbles_lost": 0.3,
            "games": 13,
            "interceptions": 0.9,
            "opponents_interceptions": 1.0,
            "losses": 4,
            "name": "Purdue",
            "pass_attempts": 44.3,
            "opponents_pass_attempts": 28.8,
            "pass_completion_percentage": 70.7,
            "opponents_pass_completion_percentage": 59.4,
            "pass_completions": 31.3,
            "opponents_pass_completions": 17.1,
            "pass_first_downs": 17.1,
            "opponents_pass_first_downs": 8.5,
            "pass_touchdowns": 2.7,
            "opponents_pass_touchdowns": 1.4,
            "pass_yards": 355.4,
            "opponents_pass_yards": 208.7,
            "penalties": 4.5,
            "opponents_penalties": 5.9,
            "plays": 74.0,
            "opponents_plays": 65.3,
            "points_against_per_game": 22.4,
            "points_per_game": 29.1,
            "rush_attempts": 29.7,
            "opponents_rush_attempts": 36.5,
            "rush_first_downs": 5.1,
            "opponents_rush_first_downs": 8.3,
            "rush_touchdowns": 0.5,
            "opponents_rush_touchdowns": 1.4,
            "rush_yards": 84.8,
            "opponents_rush_yards": 159.4,
            "rush_yards_per_attempt": 2.9,
            "opponents_rush_yards_per_attempt": 4.4,
            "simple_rating_system": 10.58,
            "strength_of_schedule": 5.81,
            "turnovers": 1.5,
            "opponents_turnovers": 1.3,
            "win_percentage": 0.692,
            "wins": 9,
            "yards": 440.2,
            "opponents_yards": 368.1,
            "yards_from_penalties": 42.8,
            "opponents_yards_from_penalties": 53.8,
            "yards_per_play": 5.9,
            "opponents_yards_per_play": 5.6,
        }
        self.schools = [
            "Wake Forest",
            "Clemson",
            "North Carolina State",
            "Louisville",
            "Florida State",
            "Boston College",
            "Syracuse",
            "Pitt",
            "Miami (FL)",
            "Virginia",
            "Virginia Tech",
            "North Carolina",
            "Georgia Tech",
            "Duke",
            "Cincinnati",
            "Houston",
            "UCF",
            "East Carolina",
            "Tulsa",
            "SMU",
            "Memphis",
            "Navy",
            "Temple",
            "South Florida",
            "Tulane",
            "Baylor",
            "Oklahoma State",
            "Oklahoma",
            "Iowa State",
            "Kansas State",
            "West Virginia",
            "Texas Tech",
            "Texas",
            "Texas Christian",
            "Kansas",
            "Michigan",
            "Ohio State",
            "Michigan State",
            "Penn State",
            "Maryland",
            "Rutgers",
            "Indiana",
            "Iowa",
            "Minnesota",
            "Purdue",
            "Wisconsin",
            "Illinois",
            "Nebraska",
            "Northwestern",
            "Western Kentucky",
            "Marshall",
            "Old Dominion",
            "Middle Tennessee State",
            "Charlotte",
            "Florida Atlantic",
            "Florida International",
            "UTSA",
            "UAB",
            "North Texas",
            "UTEP",
            "Rice",
            "Louisiana Tech",
            "Southern Mississippi",
            "Notre Dame",
            "New Mexico State",
            "Liberty",
            "Massachusetts",
            "Connecticut",
            "Army",
            "BYU",
            "Kent State",
            "Miami (OH)",
            "Ohio",
            "Bowling Green",
            "Buffalo",
            "Akron",
            "Northern Illinois",
            "Central Michigan",
            "Toledo",
            "Western Michigan",
            "Eastern Michigan",
            "Ball State",
            "Utah State",
            "Air Force",
            "Boise State",
            "Wyoming",
            "Colorado State",
            "New Mexico",
            "San Diego State",
            "Fresno State",
            "Nevada",
            "Hawaii",
            "San Jose State",
            "Nevada-Las Vegas",
            "Oregon",
            "Washington State",
            "Oregon State",
            "California",
            "Washington",
            "Stanford",
            "Utah",
            "UCLA",
            "Arizona State",
            "Colorado",
            "USC",
            "Arizona",
            "Georgia",
            "Kentucky",
            "Tennessee",
            "South Carolina",
            "Missouri",
            "Florida",
            "Vanderbilt",
            "Alabama",
            "Ole Miss",
            "Arkansas",
            "Texas A&M",
            "Mississippi State",
            "Auburn",
            "LSU",
            "Appalachian State",
            "Coastal Carolina",
            "Georgia State",
            "Troy",
            "Georgia Southern",
            "Louisiana",
            "Texas State",
            "South Alabama",
            "Louisiana-Monroe",
            "Arkansas State",
        ]

    def test_ncaaf_integration_returns_correct_number_of_teams(self, teams):
        assert len(teams) == len(self.schools)

    def test_ncaaf_integration_returns_correct_attributes_for_team(self, teams):
        team = teams(TEAM)

        for attribute, value in self.results.items():
            assert getattr(team, attribute) == value

    def test_ncaaf_integration_returns_correct_team_abbreviations(self, teams):
        for team in teams:
            assert team.name in self.schools

    def test_ncaaf_integration_dataframe_returns_dataframe(self, team):
        df = pd.DataFrame([self.results], index=[TEAM])

        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected one above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, team.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_ncaaf_integration_all_teams_dataframe_returns_dataframe(self, teams):
        result = teams.dataframes.drop_duplicates(keep=False)

        assert len(result) == len(self.schools)
        assert set(result.columns.values) == set(self.results.keys())

    def test_ncaaf_invalid_team_name_raises_value_error(self, teams):
        with pytest.raises(ValueError):
            teams("INVALID_NAME")

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_ncaaf_empty_page_returns_no_teams(self, *args, **kwargs):
        flexmock(utils).should_receive("_no_data_found").once()
        flexmock(utils).should_receive("_get_stats_table").and_return(None)

        teams = Teams()

        assert len(teams) == 0

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_ncaab_no_conference_info_skips_team(self, *args, **kwargs):
        flexmock(utils).should_receive("_todays_date").and_return(
            MockDateTime(YEAR, MONTH)
        )
        flexmock(Conferences).should_receive("team_conference").and_return({})
        flexmock(Conferences).should_receive("_find_conferences").and_return(None)

        teams = Teams(recompute_conferences=True)

        assert len(teams) == 0

    def test_use_conferences_from_constants(self, teams):
        assert teams._conferences_dict == CONFERENCE_DICT

    def test_pulling_team_directly(self, team):

        for attribute, value in self.results.items():
            assert getattr(team, attribute) == value

    def test_team_string_representation(self, team):

        assert team.__repr__() == "Purdue (PURDUE) - 2021"

    def test_teams_string_representation(self, teams):
        expected = """Wake Forest (WAKE-FOREST)
Clemson (CLEMSON)
North Carolina State (NORTH-CAROLINA-STATE)
Louisville (LOUISVILLE)
Florida State (FLORIDA-STATE)
Boston College (BOSTON-COLLEGE)
Syracuse (SYRACUSE)
Pitt (PITTSBURGH)
Miami (FL) (MIAMI-FL)
Virginia (VIRGINIA)
Virginia Tech (VIRGINIA-TECH)
North Carolina (NORTH-CAROLINA)
Georgia Tech (GEORGIA-TECH)
Duke (DUKE)
Cincinnati (CINCINNATI)
Houston (HOUSTON)
UCF (CENTRAL-FLORIDA)
East Carolina (EAST-CAROLINA)
Tulsa (TULSA)
SMU (SOUTHERN-METHODIST)
Memphis (MEMPHIS)
Navy (NAVY)
Temple (TEMPLE)
South Florida (SOUTH-FLORIDA)
Tulane (TULANE)
Baylor (BAYLOR)
Oklahoma State (OKLAHOMA-STATE)
Oklahoma (OKLAHOMA)
Iowa State (IOWA-STATE)
Kansas State (KANSAS-STATE)
West Virginia (WEST-VIRGINIA)
Texas Tech (TEXAS-TECH)
Texas (TEXAS)
Texas Christian (TEXAS-CHRISTIAN)
Kansas (KANSAS)
Michigan (MICHIGAN)
Ohio State (OHIO-STATE)
Michigan State (MICHIGAN-STATE)
Penn State (PENN-STATE)
Maryland (MARYLAND)
Rutgers (RUTGERS)
Indiana (INDIANA)
Iowa (IOWA)
Minnesota (MINNESOTA)
Purdue (PURDUE)
Wisconsin (WISCONSIN)
Illinois (ILLINOIS)
Nebraska (NEBRASKA)
Northwestern (NORTHWESTERN)
Western Kentucky (WESTERN-KENTUCKY)
Marshall (MARSHALL)
Old Dominion (OLD-DOMINION)
Middle Tennessee State (MIDDLE-TENNESSEE-STATE)
Charlotte (CHARLOTTE)
Florida Atlantic (FLORIDA-ATLANTIC)
Florida International (FLORIDA-INTERNATIONAL)
UTSA (TEXAS-SAN-ANTONIO)
UAB (ALABAMA-BIRMINGHAM)
North Texas (NORTH-TEXAS)
UTEP (TEXAS-EL-PASO)
Rice (RICE)
Louisiana Tech (LOUISIANA-TECH)
Southern Mississippi (SOUTHERN-MISSISSIPPI)
Notre Dame (NOTRE-DAME)
New Mexico State (NEW-MEXICO-STATE)
Liberty (LIBERTY)
Massachusetts (MASSACHUSETTS)
Connecticut (CONNECTICUT)
Army (ARMY)
BYU (BRIGHAM-YOUNG)
Kent State (KENT-STATE)
Miami (OH) (MIAMI-OH)
Ohio (OHIO)
Bowling Green (BOWLING-GREEN-STATE)
Buffalo (BUFFALO)
Akron (AKRON)
Northern Illinois (NORTHERN-ILLINOIS)
Central Michigan (CENTRAL-MICHIGAN)
Toledo (TOLEDO)
Western Michigan (WESTERN-MICHIGAN)
Eastern Michigan (EASTERN-MICHIGAN)
Ball State (BALL-STATE)
Utah State (UTAH-STATE)
Air Force (AIR-FORCE)
Boise State (BOISE-STATE)
Wyoming (WYOMING)
Colorado State (COLORADO-STATE)
New Mexico (NEW-MEXICO)
San Diego State (SAN-DIEGO-STATE)
Fresno State (FRESNO-STATE)
Nevada (NEVADA)
Hawaii (HAWAII)
San Jose State (SAN-JOSE-STATE)
Nevada-Las Vegas (NEVADA-LAS-VEGAS)
Oregon (OREGON)
Washington State (WASHINGTON-STATE)
Oregon State (OREGON-STATE)
California (CALIFORNIA)
Washington (WASHINGTON)
Stanford (STANFORD)
Utah (UTAH)
UCLA (UCLA)
Arizona State (ARIZONA-STATE)
Colorado (COLORADO)
USC (SOUTHERN-CALIFORNIA)
Arizona (ARIZONA)
Georgia (GEORGIA)
Kentucky (KENTUCKY)
Tennessee (TENNESSEE)
South Carolina (SOUTH-CAROLINA)
Missouri (MISSOURI)
Florida (FLORIDA)
Vanderbilt (VANDERBILT)
Alabama (ALABAMA)
Ole Miss (MISSISSIPPI)
Arkansas (ARKANSAS)
Texas A&M (TEXAS-AM)
Mississippi State (MISSISSIPPI-STATE)
Auburn (AUBURN)
LSU (LOUISIANA-STATE)
Appalachian State (APPALACHIAN-STATE)
Coastal Carolina (COASTAL-CAROLINA)
Georgia State (GEORGIA-STATE)
Troy (TROY)
Georgia Southern (GEORGIA-SOUTHERN)
Louisiana (LOUISIANA-LAFAYETTE)
Texas State (TEXAS-STATE)
South Alabama (SOUTH-ALABAMA)
Louisiana-Monroe (LOUISIANA-MONROE)
Arkansas State (ARKANSAS-STATE)"""

        assert teams.__repr__() == expected
