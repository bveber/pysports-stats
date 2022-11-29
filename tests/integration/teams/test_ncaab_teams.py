import mock
import os
import pandas as pd
import pytest
from flexmock import flexmock
from sports import utils
from sports.ncaab.conferences import Conferences
from sports.ncaab.constants import (
    ADVANCED_OPPONENT_STATS_URL,
    ADVANCED_STATS_URL,
    BASIC_OPPONENT_STATS_URL,
    BASIC_STATS_URL,
    CONFERENCE_URL,
    CONFERENCE_DICT,
)
from sports.ncaab.teams import Team, Teams
from ..utils import read_file


MONTH = 1
YEAR = 2022
MOCK_CONFERENCE_DICT = {"purdue": "big-ten"}
TEAM = "PURDUE"


def mock_pyquery(url):
    if "-advanced-school-stats" in url:
        return read_file("2022-advanced-school-stats.html", "ncaab", "teams")
    if "-school-stats" in url:
        return read_file("2022-school-stats.html", "ncaab", "teams")
    if "-advanced-opponent-stats" in url:
        return read_file("2022-advanced-opponent-stats.html", "ncaab", "teams")
    if "-opponent-stats" in url:
        return read_file("2022-opponent-stats.html", "ncaab", "teams")
    if "purdue" in url:
        return read_file("2022-purdue.html", "ncaab", "teams")
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


class TestNCAABIntegration:
    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            "abbreviation": "PURDUE",
            "assist_percentage": 58.6,
            "assists": 601,
            "away_losses": 5,
            "away_wins": 5,
            "block_percentage": 9.7,
            "blocks": 128,
            "conference": "big-ten",
            "conference_losses": 6,
            "conference_wins": 14,
            "defensive_rebounds": 1019,
            "effective_field_goal_percentage": 0.565,
            "field_goal_attempts": 2094,
            "field_goal_percentage": 0.49,
            "field_goals": 1026,
            "free_throw_attempt_rate": 0.382,
            "free_throw_attempts": 800,
            "free_throw_percentage": 0.711,
            "free_throws": 569,
            "free_throws_per_field_goal_attempt": 0.272,
            "games_played": 37,
            "home_losses": 1,
            "home_wins": 16,
            "losses": 8,
            "minutes_played": 1495,
            "name": "Purdue",
            "net_rating": None,
            "offensive_rating": 117.8,
            "offensive_rebound_percentage": 35.2,
            "offensive_rebounds": 412,
            "opp_assist_percentage": 53.3,
            "opp_assists": 503,
            "opp_block_percentage": 7.1,
            "opp_blocks": 90,
            "opp_defensive_rebounds": 758,
            "opp_effective_field_goal_percentage": 0.491,
            "opp_field_goal_attempts": 2225,
            "opp_field_goal_percentage": 0.424,
            "opp_field_goals": 943,
            "opp_free_throw_attempt_rate": 0.216,
            "opp_free_throw_attempts": 480,
            "opp_free_throw_percentage": 0.721,
            "opp_free_throws": 346,
            "opp_free_throws_per_field_goal_attempt": 0.156,
            "opp_offensive_rating": None,
            "opp_offensive_rebound_percentage": 23.8,
            "opp_offensive_rebounds": 318,
            "opp_personal_fouls": 716,
            "opp_points": 2532,
            "opp_steal_percentage": 8.8,
            "opp_steals": 220,
            "opp_three_point_attempt_rate": 0.406,
            "opp_three_point_field_goal_attempts": 903,
            "opp_three_point_field_goal_percentage": 0.332,
            "opp_three_point_field_goals": 300,
            "opp_two_point_field_goal_attempts": 1322,
            "opp_two_point_field_goal_percentage": 0.486,
            "opp_two_point_field_goals": 643,
            "opp_total_rebound_percentage": 42.9,
            "opp_total_rebounds": 1076,
            "opp_true_shooting_percentage": 0.516,
            "opp_turnover_percentage": 12.5,
            "opp_turnovers": 351,
            "pace": 66.7,
            "personal_fouls": 535,
            "points": 2936,
            "simple_rating_system": 19.15,
            "steal_percentage": 6.9,
            "steals": 172,
            "strength_of_schedule": 8.23,
            "three_point_attempt_rate": 0.392,
            "three_point_field_goal_attempts": 820,
            "three_point_field_goal_percentage": 0.384,
            "three_point_field_goals": 315,
            "two_point_field_goal_attempts": 1274,
            "two_point_field_goal_percentage": 0.558,
            "two_point_field_goals": 711,
            "total_rebound_percentage": 57.1,
            "total_rebounds": 1431,
            "true_shooting_percentage": 0.593,
            "turnover_percentage": 15.0,
            "turnovers": 436,
            "win_percentage": 0.784,
            "wins": 29,
        }
        self.abbreviations = [
            "ABILENE-CHRISTIAN",
            "AIR-FORCE",
            "AKRON",
            "ALABAMA",
            "ALABAMA-AM",
            "ALABAMA-STATE",
            "ALBANY-NY",
            "ALCORN-STATE",
            "AMERICAN",
            "APPALACHIAN-STATE",
            "ARIZONA",
            "ARIZONA-STATE",
            "ARKANSAS",
            "ARKANSAS-STATE",
            "ARKANSAS-PINE-BLUFF",
            "ARMY",
            "AUBURN",
            "AUSTIN-PEAY",
            "BALL-STATE",
            "BAYLOR",
            "BELLARMINE",
            "BELMONT",
            "BETHUNE-COOKMAN",
            "BINGHAMTON",
            "BOISE-STATE",
            "BOSTON-COLLEGE",
            "BOSTON-UNIVERSITY",
            "BOWLING-GREEN-STATE",
            "BRADLEY",
            "BRIGHAM-YOUNG",
            "BROWN",
            "BRYANT",
            "BUCKNELL",
            "BUFFALO",
            "BUTLER",
            "CAL-POLY",
            "CAL-STATE-BAKERSFIELD",
            "CAL-STATE-FULLERTON",
            "CAL-STATE-NORTHRIDGE",
            "CALIFORNIA",
            "CALIFORNIA-BAPTIST",
            "CAMPBELL",
            "CANISIUS",
            "CENTRAL-ARKANSAS",
            "CENTRAL-CONNECTICUT-STATE",
            "CENTRAL-FLORIDA",
            "CENTRAL-MICHIGAN",
            "CHARLESTON-SOUTHERN",
            "CHARLOTTE",
            "CHATTANOOGA",
            "CHICAGO-STATE",
            "CINCINNATI",
            "CLEMSON",
            "CLEVELAND-STATE",
            "COASTAL-CAROLINA",
            "COLGATE",
            "COLLEGE-OF-CHARLESTON",
            "COLORADO",
            "COLORADO-STATE",
            "COLUMBIA",
            "CONNECTICUT",
            "COPPIN-STATE",
            "CORNELL",
            "CREIGHTON",
            "DARTMOUTH",
            "DAVIDSON",
            "DAYTON",
            "DELAWARE",
            "DELAWARE-STATE",
            "DENVER",
            "DEPAUL",
            "DETROIT-MERCY",
            "DRAKE",
            "DREXEL",
            "DUKE",
            "DUQUESNE",
            "EAST-CAROLINA",
            "EAST-TENNESSEE-STATE",
            "EASTERN-ILLINOIS",
            "EASTERN-KENTUCKY",
            "EASTERN-MICHIGAN",
            "EASTERN-WASHINGTON",
            "ELON",
            "EVANSVILLE",
            "FAIRFIELD",
            "FAIRLEIGH-DICKINSON",
            "FLORIDA",
            "FLORIDA-AM",
            "FLORIDA-ATLANTIC",
            "FLORIDA-GULF-COAST",
            "FLORIDA-INTERNATIONAL",
            "FLORIDA-STATE",
            "FORDHAM",
            "FRESNO-STATE",
            "FURMAN",
            "GARDNER-WEBB",
            "GEORGE-MASON",
            "GEORGE-WASHINGTON",
            "GEORGETOWN",
            "GEORGIA",
            "GEORGIA-SOUTHERN",
            "GEORGIA-STATE",
            "GEORGIA-TECH",
            "GONZAGA",
            "GRAMBLING",
            "GRAND-CANYON",
            "GREEN-BAY",
            "HAMPTON",
            "HARTFORD",
            "HARVARD",
            "HAWAII",
            "HIGH-POINT",
            "HOFSTRA",
            "HOLY-CROSS",
            "HOUSTON",
            "HOUSTON-BAPTIST",
            "HOWARD",
            "IDAHO",
            "IDAHO-STATE",
            "ILLINOIS",
            "ILLINOIS-STATE",
            "ILLINOIS-CHICAGO",
            "INCARNATE-WORD",
            "INDIANA",
            "INDIANA-STATE",
            "IONA",
            "IOWA",
            "IOWA-STATE",
            "IUPUI",
            "JACKSON-STATE",
            "JACKSONVILLE",
            "JACKSONVILLE-STATE",
            "JAMES-MADISON",
            "KANSAS",
            "MISSOURI-KANSAS-CITY",
            "KANSAS-STATE",
            "KENNESAW-STATE",
            "KENT-STATE",
            "KENTUCKY",
            "LA-SALLE",
            "LAFAYETTE",
            "LAMAR",
            "LEHIGH",
            "LIBERTY",
            "LIPSCOMB",
            "ARKANSAS-LITTLE-ROCK",
            "LONG-BEACH-STATE",
            "LONG-ISLAND-UNIVERSITY",
            "LONGWOOD",
            "LOUISIANA-LAFAYETTE",
            "LOUISIANA-STATE",
            "LOUISIANA-TECH",
            "LOUISIANA-MONROE",
            "LOUISVILLE",
            "LOYOLA-IL",
            "LOYOLA-MD",
            "LOYOLA-MARYMOUNT",
            "MAINE",
            "MANHATTAN",
            "MARIST",
            "MARQUETTE",
            "MARSHALL",
            "MARYLAND",
            "MARYLAND-BALTIMORE-COUNTY",
            "MARYLAND-EASTERN-SHORE",
            "MASSACHUSETTS",
            "MASSACHUSETTS-LOWELL",
            "MCNEESE-STATE",
            "MEMPHIS",
            "MERCER",
            "MERRIMACK",
            "MIAMI-FL",
            "MIAMI-OH",
            "MICHIGAN",
            "MICHIGAN-STATE",
            "MIDDLE-TENNESSEE",
            "MILWAUKEE",
            "MINNESOTA",
            "MISSISSIPPI",
            "MISSISSIPPI-STATE",
            "MISSISSIPPI-VALLEY-STATE",
            "MISSOURI",
            "MISSOURI-STATE",
            "MONMOUTH",
            "MONTANA",
            "MONTANA-STATE",
            "MOREHEAD-STATE",
            "MORGAN-STATE",
            "MOUNT-ST-MARYS",
            "MURRAY-STATE",
            "NAVY",
            "NORTH-CAROLINA-STATE",
            "NEBRASKA",
            "NEVADA",
            "NEVADA-LAS-VEGAS",
            "NEW-HAMPSHIRE",
            "NEW-MEXICO",
            "NEW-MEXICO-STATE",
            "NEW-ORLEANS",
            "NIAGARA",
            "NICHOLLS-STATE",
            "NJIT",
            "NORFOLK-STATE",
            "NORTH-ALABAMA",
            "NORTH-CAROLINA",
            "NORTH-CAROLINA-AT",
            "NORTH-CAROLINA-CENTRAL",
            "NORTH-DAKOTA",
            "NORTH-DAKOTA-STATE",
            "NORTH-FLORIDA",
            "NORTH-TEXAS",
            "NORTHEASTERN",
            "NORTHERN-ARIZONA",
            "NORTHERN-COLORADO",
            "NORTHERN-ILLINOIS",
            "NORTHERN-IOWA",
            "NORTHERN-KENTUCKY",
            "NORTHWESTERN",
            "NORTHWESTERN-STATE",
            "NOTRE-DAME",
            "OAKLAND",
            "OHIO",
            "OHIO-STATE",
            "OKLAHOMA",
            "OKLAHOMA-STATE",
            "OLD-DOMINION",
            "NEBRASKA-OMAHA",
            "ORAL-ROBERTS",
            "OREGON",
            "OREGON-STATE",
            "PACIFIC",
            "PENN-STATE",
            "PENNSYLVANIA",
            "PEPPERDINE",
            "PITTSBURGH",
            "PORTLAND",
            "PORTLAND-STATE",
            "PRAIRIE-VIEW",
            "PRESBYTERIAN",
            "PRINCETON",
            "PROVIDENCE",
            "PURDUE",
            "IPFW",
            "QUINNIPIAC",
            "RADFORD",
            "RHODE-ISLAND",
            "RICE",
            "RICHMOND",
            "RIDER",
            "ROBERT-MORRIS",
            "RUTGERS",
            "SACRAMENTO-STATE",
            "SACRED-HEART",
            "SAINT-FRANCIS-PA",
            "SAINT-JOSEPHS",
            "SAINT-LOUIS",
            "SAINT-MARYS-CA",
            "SAINT-PETERS",
            "SAM-HOUSTON-STATE",
            "SAMFORD",
            "SAN-DIEGO",
            "SAN-DIEGO-STATE",
            "SAN-FRANCISCO",
            "SAN-JOSE-STATE",
            "SANTA-CLARA",
            "SEATTLE",
            "SETON-HALL",
            "SIENA",
            "SOUTH-ALABAMA",
            "SOUTH-CAROLINA",
            "SOUTH-CAROLINA-STATE",
            "SOUTH-CAROLINA-UPSTATE",
            "SOUTH-DAKOTA",
            "SOUTH-DAKOTA-STATE",
            "SOUTH-FLORIDA",
            "SOUTHEAST-MISSOURI-STATE",
            "SOUTHEASTERN-LOUISIANA",
            "SOUTHERN",
            "SOUTHERN-CALIFORNIA",
            "SOUTHERN-ILLINOIS",
            "SOUTHERN-ILLINOIS-EDWARDSVILLE",
            "SOUTHERN-METHODIST",
            "SOUTHERN-MISSISSIPPI",
            "SOUTHERN-UTAH",
            "ST-BONAVENTURE",
            "ST-FRANCIS-NY",
            "ST-JOHNS-NY",
            "ST-THOMAS-MN",
            "STANFORD",
            "STEPHEN-F-AUSTIN",
            "STETSON",
            "STONY-BROOK",
            "SYRACUSE",
            "TARLETON-STATE",
            "TEXAS-CHRISTIAN",
            "TEMPLE",
            "TENNESSEE",
            "TENNESSEE-STATE",
            "TENNESSEE-TECH",
            "TENNESSEE-MARTIN",
            "TEXAS",
            "TEXAS-AM",
            "TEXAS-AM-CORPUS-CHRISTI",
            "TEXAS-SOUTHERN",
            "TEXAS-STATE",
            "TEXAS-TECH",
            "TEXAS-PAN-AMERICAN",
            "CITADEL",
            "TOLEDO",
            "TOWSON",
            "TROY",
            "TULANE",
            "TULSA",
            "ALABAMA-BIRMINGHAM",
            "CALIFORNIA-DAVIS",
            "CALIFORNIA-IRVINE",
            "CALIFORNIA-RIVERSIDE",
            "CALIFORNIA-SAN-DIEGO",
            "CALIFORNIA-SANTA-BARBARA",
            "UCLA",
            "NORTH-CAROLINA-ASHEVILLE",
            "NORTH-CAROLINA-GREENSBORO",
            "NORTH-CAROLINA-WILMINGTON",
            "TEXAS-ARLINGTON",
            "UTAH",
            "UTAH-STATE",
            "DIXIE-STATE",
            "UTAH-VALLEY",
            "TEXAS-EL-PASO",
            "TEXAS-SAN-ANTONIO",
            "VALPARAISO",
            "VANDERBILT",
            "VERMONT",
            "VILLANOVA",
            "VIRGINIA",
            "VIRGINIA-COMMONWEALTH",
            "VIRGINIA-MILITARY-INSTITUTE",
            "VIRGINIA-TECH",
            "WAGNER",
            "WAKE-FOREST",
            "WASHINGTON",
            "WASHINGTON-STATE",
            "WEBER-STATE",
            "WEST-VIRGINIA",
            "WESTERN-CAROLINA",
            "WESTERN-ILLINOIS",
            "WESTERN-KENTUCKY",
            "WESTERN-MICHIGAN",
            "WICHITA-STATE",
            "WILLIAM-MARY",
            "WINTHROP",
            "WISCONSIN",
            "WOFFORD",
            "WRIGHT-STATE",
            "WYOMING",
            "XAVIER",
            "YALE",
            "YOUNGSTOWN-STATE",
        ]

    def test_ncaab_integration_returns_correct_number_of_teams(self, teams):
        assert len(teams) == len(self.abbreviations)

    def test_ncaab_integration_returns_correct_attributes_for_team(self, teams):
        team = teams(TEAM)

        for attribute, value in self.results.items():
            assert getattr(team, attribute) == value

    def test_ncaab_integration_returns_correct_team_abbreviations(self, teams):
        for team in teams:
            assert team.abbreviation in self.abbreviations

    def test_ncaab_integration_dataframe_returns_dataframe(self, teams):
        df = pd.DataFrame([self.results], index=[TEAM])

        team = teams(TEAM)
        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected one above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, team.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_ncaab_integration_all_teams_dataframe_returns_dataframe(self, teams):
        result = teams.dataframes.drop_duplicates(keep=False)

        assert len(result) == len(self.abbreviations)
        assert set(result.columns.values) == set(self.results.keys())

    def test_ncaab_invalid_team_name_raises_value_error(self, teams):
        with pytest.raises(ValueError):
            teams("INVALID_NAME")

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_ncaab_empty_page_returns_no_teams(self, *args, **kwargs):
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

        assert team.__repr__() == "Purdue (PURDUE) - 2022"

    def test_teams_string_representation(self, teams):
        expected = """Abilene Christian (ABILENE-CHRISTIAN)
Air Force (AIR-FORCE)
Akron (AKRON)
Alabama (ALABAMA)
Alabama A&M (ALABAMA-AM)
Alabama State (ALABAMA-STATE)
Albany (NY) (ALBANY-NY)
Alcorn State (ALCORN-STATE)
American (AMERICAN)
Appalachian State (APPALACHIAN-STATE)
Arizona (ARIZONA)
Arizona State (ARIZONA-STATE)
Arkansas (ARKANSAS)
Arkansas State (ARKANSAS-STATE)
Arkansas-Pine Bluff (ARKANSAS-PINE-BLUFF)
Army (ARMY)
Auburn (AUBURN)
Austin Peay (AUSTIN-PEAY)
Ball State (BALL-STATE)
Baylor (BAYLOR)
Bellarmine (BELLARMINE)
Belmont (BELMONT)
Bethune-Cookman (BETHUNE-COOKMAN)
Binghamton (BINGHAMTON)
Boise State (BOISE-STATE)
Boston College (BOSTON-COLLEGE)
Boston University (BOSTON-UNIVERSITY)
Bowling Green State (BOWLING-GREEN-STATE)
Bradley (BRADLEY)
Brigham Young (BRIGHAM-YOUNG)
Brown (BROWN)
Bryant (BRYANT)
Bucknell (BUCKNELL)
Buffalo (BUFFALO)
Butler (BUTLER)
Cal Poly (CAL-POLY)
Cal State Bakersfield (CAL-STATE-BAKERSFIELD)
Cal State Fullerton (CAL-STATE-FULLERTON)
Cal State Northridge (CAL-STATE-NORTHRIDGE)
California (CALIFORNIA)
California Baptist (CALIFORNIA-BAPTIST)
Campbell (CAMPBELL)
Canisius (CANISIUS)
Central Arkansas (CENTRAL-ARKANSAS)
Central Connecticut State (CENTRAL-CONNECTICUT-STATE)
Central Florida (CENTRAL-FLORIDA)
Central Michigan (CENTRAL-MICHIGAN)
Charleston Southern (CHARLESTON-SOUTHERN)
Charlotte (CHARLOTTE)
Chattanooga (CHATTANOOGA)
Chicago State (CHICAGO-STATE)
Cincinnati (CINCINNATI)
Clemson (CLEMSON)
Cleveland State (CLEVELAND-STATE)
Coastal Carolina (COASTAL-CAROLINA)
Colgate (COLGATE)
College of Charleston (COLLEGE-OF-CHARLESTON)
Colorado (COLORADO)
Colorado State (COLORADO-STATE)
Columbia (COLUMBIA)
Connecticut (CONNECTICUT)
Coppin State (COPPIN-STATE)
Cornell (CORNELL)
Creighton (CREIGHTON)
Dartmouth (DARTMOUTH)
Davidson (DAVIDSON)
Dayton (DAYTON)
Delaware (DELAWARE)
Delaware State (DELAWARE-STATE)
Denver (DENVER)
DePaul (DEPAUL)
Detroit Mercy (DETROIT-MERCY)
Drake (DRAKE)
Drexel (DREXEL)
Duke (DUKE)
Duquesne (DUQUESNE)
East Carolina (EAST-CAROLINA)
East Tennessee State (EAST-TENNESSEE-STATE)
Eastern Illinois (EASTERN-ILLINOIS)
Eastern Kentucky (EASTERN-KENTUCKY)
Eastern Michigan (EASTERN-MICHIGAN)
Eastern Washington (EASTERN-WASHINGTON)
Elon (ELON)
Evansville (EVANSVILLE)
Fairfield (FAIRFIELD)
Fairleigh Dickinson (FAIRLEIGH-DICKINSON)
Florida (FLORIDA)
Florida A&M (FLORIDA-AM)
Florida Atlantic (FLORIDA-ATLANTIC)
Florida Gulf Coast (FLORIDA-GULF-COAST)
Florida International (FLORIDA-INTERNATIONAL)
Florida State (FLORIDA-STATE)
Fordham (FORDHAM)
Fresno State (FRESNO-STATE)
Furman (FURMAN)
Gardner-Webb (GARDNER-WEBB)
George Mason (GEORGE-MASON)
George Washington (GEORGE-WASHINGTON)
Georgetown (GEORGETOWN)
Georgia (GEORGIA)
Georgia Southern (GEORGIA-SOUTHERN)
Georgia State (GEORGIA-STATE)
Georgia Tech (GEORGIA-TECH)
Gonzaga (GONZAGA)
Grambling (GRAMBLING)
Grand Canyon (GRAND-CANYON)
Green Bay (GREEN-BAY)
Hampton (HAMPTON)
Hartford (HARTFORD)
Harvard (HARVARD)
Hawaii (HAWAII)
High Point (HIGH-POINT)
Hofstra (HOFSTRA)
Holy Cross (HOLY-CROSS)
Houston (HOUSTON)
Houston Christian (HOUSTON-BAPTIST)
Howard (HOWARD)
Idaho (IDAHO)
Idaho State (IDAHO-STATE)
Illinois (ILLINOIS)
Illinois State (ILLINOIS-STATE)
Illinois-Chicago (ILLINOIS-CHICAGO)
Incarnate Word (INCARNATE-WORD)
Indiana (INDIANA)
Indiana State (INDIANA-STATE)
Iona (IONA)
Iowa (IOWA)
Iowa State (IOWA-STATE)
IUPUI (IUPUI)
Jackson State (JACKSON-STATE)
Jacksonville (JACKSONVILLE)
Jacksonville State (JACKSONVILLE-STATE)
James Madison (JAMES-MADISON)
Kansas (KANSAS)
Kansas City (MISSOURI-KANSAS-CITY)
Kansas State (KANSAS-STATE)
Kennesaw State (KENNESAW-STATE)
Kent State (KENT-STATE)
Kentucky (KENTUCKY)
La Salle (LA-SALLE)
Lafayette (LAFAYETTE)
Lamar (LAMAR)
Lehigh (LEHIGH)
Liberty (LIBERTY)
Lipscomb (LIPSCOMB)
Little Rock (ARKANSAS-LITTLE-ROCK)
Long Beach State (LONG-BEACH-STATE)
Long Island University (LONG-ISLAND-UNIVERSITY)
Longwood (LONGWOOD)
Louisiana (LOUISIANA-LAFAYETTE)
Louisiana State (LOUISIANA-STATE)
Louisiana Tech (LOUISIANA-TECH)
Louisiana-Monroe (LOUISIANA-MONROE)
Louisville (LOUISVILLE)
Loyola (IL) (LOYOLA-IL)
Loyola (MD) (LOYOLA-MD)
Loyola Marymount (LOYOLA-MARYMOUNT)
Maine (MAINE)
Manhattan (MANHATTAN)
Marist (MARIST)
Marquette (MARQUETTE)
Marshall (MARSHALL)
Maryland (MARYLAND)
Maryland-Baltimore County (MARYLAND-BALTIMORE-COUNTY)
Maryland-Eastern Shore (MARYLAND-EASTERN-SHORE)
Massachusetts (MASSACHUSETTS)
Massachusetts-Lowell (MASSACHUSETTS-LOWELL)
McNeese State (MCNEESE-STATE)
Memphis (MEMPHIS)
Mercer (MERCER)
Merrimack (MERRIMACK)
Miami (FL) (MIAMI-FL)
Miami (OH) (MIAMI-OH)
Michigan (MICHIGAN)
Michigan State (MICHIGAN-STATE)
Middle Tennessee (MIDDLE-TENNESSEE)
Milwaukee (MILWAUKEE)
Minnesota (MINNESOTA)
Mississippi (MISSISSIPPI)
Mississippi State (MISSISSIPPI-STATE)
Mississippi Valley State (MISSISSIPPI-VALLEY-STATE)
Missouri (MISSOURI)
Missouri State (MISSOURI-STATE)
Monmouth (MONMOUTH)
Montana (MONTANA)
Montana State (MONTANA-STATE)
Morehead State (MOREHEAD-STATE)
Morgan State (MORGAN-STATE)
Mount St. Mary's (MOUNT-ST-MARYS)
Murray State (MURRAY-STATE)
Navy (NAVY)
NC State (NORTH-CAROLINA-STATE)
Nebraska (NEBRASKA)
Nevada (NEVADA)
Nevada-Las Vegas (NEVADA-LAS-VEGAS)
New Hampshire (NEW-HAMPSHIRE)
New Mexico (NEW-MEXICO)
New Mexico State (NEW-MEXICO-STATE)
New Orleans (NEW-ORLEANS)
Niagara (NIAGARA)
Nicholls State (NICHOLLS-STATE)
NJIT (NJIT)
Norfolk State (NORFOLK-STATE)
North Alabama (NORTH-ALABAMA)
North Carolina (NORTH-CAROLINA)
North Carolina A&T (NORTH-CAROLINA-AT)
North Carolina Central (NORTH-CAROLINA-CENTRAL)
North Dakota (NORTH-DAKOTA)
North Dakota State (NORTH-DAKOTA-STATE)
North Florida (NORTH-FLORIDA)
North Texas (NORTH-TEXAS)
Northeastern (NORTHEASTERN)
Northern Arizona (NORTHERN-ARIZONA)
Northern Colorado (NORTHERN-COLORADO)
Northern Illinois (NORTHERN-ILLINOIS)
Northern Iowa (NORTHERN-IOWA)
Northern Kentucky (NORTHERN-KENTUCKY)
Northwestern (NORTHWESTERN)
Northwestern State (NORTHWESTERN-STATE)
Notre Dame (NOTRE-DAME)
Oakland (OAKLAND)
Ohio (OHIO)
Ohio State (OHIO-STATE)
Oklahoma (OKLAHOMA)
Oklahoma State (OKLAHOMA-STATE)
Old Dominion (OLD-DOMINION)
Omaha (NEBRASKA-OMAHA)
Oral Roberts (ORAL-ROBERTS)
Oregon (OREGON)
Oregon State (OREGON-STATE)
Pacific (PACIFIC)
Penn State (PENN-STATE)
Pennsylvania (PENNSYLVANIA)
Pepperdine (PEPPERDINE)
Pittsburgh (PITTSBURGH)
Portland (PORTLAND)
Portland State (PORTLAND-STATE)
Prairie View (PRAIRIE-VIEW)
Presbyterian (PRESBYTERIAN)
Princeton (PRINCETON)
Providence (PROVIDENCE)
Purdue (PURDUE)
Purdue-Fort Wayne (IPFW)
Quinnipiac (QUINNIPIAC)
Radford (RADFORD)
Rhode Island (RHODE-ISLAND)
Rice (RICE)
Richmond (RICHMOND)
Rider (RIDER)
Robert Morris (ROBERT-MORRIS)
Rutgers (RUTGERS)
Sacramento State (SACRAMENTO-STATE)
Sacred Heart (SACRED-HEART)
Saint Francis (PA) (SAINT-FRANCIS-PA)
Saint Joseph's (SAINT-JOSEPHS)
Saint Louis (SAINT-LOUIS)
Saint Mary's (CA) (SAINT-MARYS-CA)
Saint Peter's (SAINT-PETERS)
Sam Houston State (SAM-HOUSTON-STATE)
Samford (SAMFORD)
San Diego (SAN-DIEGO)
San Diego State (SAN-DIEGO-STATE)
San Francisco (SAN-FRANCISCO)
San Jose State (SAN-JOSE-STATE)
Santa Clara (SANTA-CLARA)
Seattle (SEATTLE)
Seton Hall (SETON-HALL)
Siena (SIENA)
South Alabama (SOUTH-ALABAMA)
South Carolina (SOUTH-CAROLINA)
South Carolina State (SOUTH-CAROLINA-STATE)
South Carolina Upstate (SOUTH-CAROLINA-UPSTATE)
South Dakota (SOUTH-DAKOTA)
South Dakota State (SOUTH-DAKOTA-STATE)
South Florida (SOUTH-FLORIDA)
Southeast Missouri State (SOUTHEAST-MISSOURI-STATE)
Southeastern Louisiana (SOUTHEASTERN-LOUISIANA)
Southern (SOUTHERN)
Southern California (SOUTHERN-CALIFORNIA)
Southern Illinois (SOUTHERN-ILLINOIS)
SIU Edwardsville (SOUTHERN-ILLINOIS-EDWARDSVILLE)
Southern Methodist (SOUTHERN-METHODIST)
Southern Mississippi (SOUTHERN-MISSISSIPPI)
Southern Utah (SOUTHERN-UTAH)
St. Bonaventure (ST-BONAVENTURE)
St. Francis (NY) (ST-FRANCIS-NY)
St. John's (NY) (ST-JOHNS-NY)
St. Thomas (MN) (ST-THOMAS-MN)
Stanford (STANFORD)
Stephen F. Austin (STEPHEN-F-AUSTIN)
Stetson (STETSON)
Stony Brook (STONY-BROOK)
Syracuse (SYRACUSE)
Tarleton State (TARLETON-STATE)
TCU (TEXAS-CHRISTIAN)
Temple (TEMPLE)
Tennessee (TENNESSEE)
Tennessee State (TENNESSEE-STATE)
Tennessee Tech (TENNESSEE-TECH)
Tennessee-Martin (TENNESSEE-MARTIN)
Texas (TEXAS)
Texas A&M (TEXAS-AM)
Texas A&M-Corpus Christi (TEXAS-AM-CORPUS-CHRISTI)
Texas Southern (TEXAS-SOUTHERN)
Texas State (TEXAS-STATE)
Texas Tech (TEXAS-TECH)
Texas-Rio Grande Valley (TEXAS-PAN-AMERICAN)
The Citadel (CITADEL)
Toledo (TOLEDO)
Towson (TOWSON)
Troy (TROY)
Tulane (TULANE)
Tulsa (TULSA)
UAB (ALABAMA-BIRMINGHAM)
UC Davis (CALIFORNIA-DAVIS)
UC Irvine (CALIFORNIA-IRVINE)
UC Riverside (CALIFORNIA-RIVERSIDE)
UC San Diego (CALIFORNIA-SAN-DIEGO)
UC Santa Barbara (CALIFORNIA-SANTA-BARBARA)
UCLA (UCLA)
UNC Asheville (NORTH-CAROLINA-ASHEVILLE)
UNC Greensboro (NORTH-CAROLINA-GREENSBORO)
UNC Wilmington (NORTH-CAROLINA-WILMINGTON)
UT Arlington (TEXAS-ARLINGTON)
Utah (UTAH)
Utah State (UTAH-STATE)
Utah Tech (DIXIE-STATE)
Utah Valley (UTAH-VALLEY)
UTEP (TEXAS-EL-PASO)
UTSA (TEXAS-SAN-ANTONIO)
Valparaiso (VALPARAISO)
Vanderbilt (VANDERBILT)
Vermont (VERMONT)
Villanova (VILLANOVA)
Virginia (VIRGINIA)
Virginia Commonwealth (VIRGINIA-COMMONWEALTH)
VMI (VIRGINIA-MILITARY-INSTITUTE)
Virginia Tech (VIRGINIA-TECH)
Wagner (WAGNER)
Wake Forest (WAKE-FOREST)
Washington (WASHINGTON)
Washington State (WASHINGTON-STATE)
Weber State (WEBER-STATE)
West Virginia (WEST-VIRGINIA)
Western Carolina (WESTERN-CAROLINA)
Western Illinois (WESTERN-ILLINOIS)
Western Kentucky (WESTERN-KENTUCKY)
Western Michigan (WESTERN-MICHIGAN)
Wichita State (WICHITA-STATE)
William & Mary (WILLIAM-MARY)
Winthrop (WINTHROP)
Wisconsin (WISCONSIN)
Wofford (WOFFORD)
Wright State (WRIGHT-STATE)
Wyoming (WYOMING)
Xavier (XAVIER)
Yale (YALE)
Youngstown State (YOUNGSTOWN-STATE)"""

        assert teams.__repr__() == expected

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_teams_before_1993_raises_value_error(self, *args, **kwargs):
        with pytest.raises(ValueError):
            Teams("1992")

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_teams_no_opponent_data_before_2010(self, mock_pq, **kwargs):
        year = "2009"
        teams = Teams(year)
        mock_pq.assert_called_with(ADVANCED_STATS_URL % year)

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_teams_all_data_before_2010(self, mock_pq, **kwargs):
        teams = Teams(YEAR)
        mock_pq.assert_called_with(ADVANCED_OPPONENT_STATS_URL % YEAR)
