import mock
import os
import pandas as pd
from datetime import datetime
from flexmock import flexmock
from sports import utils
from sports.constants import HOME
from sports.nfl.constants import BOXSCORE_URL, BOXSCORES_URL
from sports.nfl.boxscore import Boxscore, Boxscores
from ..utils import read_file


MONTH = 10
YEAR = 2020

BOXSCORE = "202009100kan"


def mock_pyquery(url):
    if url == BOXSCORES_URL % (YEAR, 1):
        return read_file("boxscores-1-2020.html", "nfl", "boxscore")
    if url == BOXSCORES_URL % (YEAR, 2):
        return read_file("boxscores-2-2020.html", "nfl", "boxscore")
    boxscore = read_file("%s.html" % BOXSCORE, "nfl", "boxscore")
    return boxscore


class MockDateTime:
    def __init__(self, year, month):
        self.year = year
        self.month = month


class TestNFLBoxscore:
    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            "date": "Thursday Sep 10, 2020",
            "time": "8:20pm",
            "datetime": datetime(2020, 9, 10, 20, 20),
            "stadium": "Arrowhead Stadium",
            "attendance": 15895,
            "duration": "2:53",
            "winner": HOME,
            "winning_name": "Kansas City Chiefs",
            "winning_abbr": "KAN",
            "losing_name": "Houston Texans",
            "losing_abbr": "HTX",
            "won_toss": "Chiefs (deferred)",
            "weather": "56 degrees, relative humidity 95%, wind 7 mph",
            "vegas_line": "Kansas City Chiefs -9.5",
            "surface": "Grass",
            "roof": "Outdoors",
            "over_under": "53.5 (over)",
            "away_points": 20,
            "away_first_downs": 21,
            "away_rush_attempts": 22,
            "away_rush_yards": 118,
            "away_rush_touchdowns": 2,
            "away_pass_completions": 20,
            "away_pass_attempts": 32,
            "away_pass_yards": 253,
            "away_pass_touchdowns": 1,
            "away_interceptions": 1,
            "away_times_sacked": 4,
            "away_yards_lost_from_sacks": 11,
            "away_net_pass_yards": 242,
            "away_total_yards": 360,
            "away_fumbles": 0,
            "away_fumbles_lost": 0,
            "away_turnovers": 1,
            "away_penalties": 5,
            "away_yards_from_penalties": 37,
            "away_third_down_conversions": 4,
            "away_third_down_attempts": 10,
            "away_fourth_down_conversions": 1,
            "away_fourth_down_attempts": 1,
            "away_time_of_possession": "25:13",
            "home_points": 34,
            "home_first_downs": 28,
            "home_rush_attempts": 34,
            "home_rush_yards": 166,
            "home_rush_touchdowns": 1,
            "home_pass_completions": 24,
            "home_pass_attempts": 32,
            "home_pass_yards": 211,
            "home_pass_touchdowns": 3,
            "home_interceptions": 0,
            "home_times_sacked": 1,
            "home_yards_lost_from_sacks": 8,
            "home_net_pass_yards": 203,
            "home_total_yards": 369,
            "home_fumbles": 0,
            "home_fumbles_lost": 0,
            "home_turnovers": 0,
            "home_penalties": 1,
            "home_yards_from_penalties": 5,
            "home_third_down_conversions": 7,
            "home_third_down_attempts": 13,
            "home_fourth_down_conversions": 1,
            "home_fourth_down_attempts": 1,
            "home_time_of_possession": "34:47",
        }
        flexmock(utils).should_receive("_todays_date").and_return(
            MockDateTime(YEAR, MONTH)
        )

        self.boxscore = Boxscore(BOXSCORE)

    def test_nfl_boxscore_returns_requested_boxscore(self):
        for attribute, value in self.results.items():
            assert getattr(self.boxscore, attribute) == value
        assert getattr(self.boxscore, "summary") == {
            "away": [7, 0, 0, 13],
            "home": [0, 17, 7, 10],
        }

    def test_invalid_url_yields_empty_class(self):
        flexmock(Boxscore).should_receive("_retrieve_html_page").and_return(None)

        boxscore = Boxscore(BOXSCORE)

        for key, value in boxscore.__dict__.items():
            if key == "_uri":
                continue
            assert value is None

    def test_nfl_boxscore_dataframe_returns_dataframe_of_all_values(self):
        df = pd.DataFrame([self.results], index=[BOXSCORE])

        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected one above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, self.boxscore.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_nfl_boxscore_players(self):
        boxscore = self.boxscore

        assert len(boxscore.home_players) == 33
        assert len(boxscore.away_players) == 28

        for player in boxscore.home_players:
            assert not player.dataframe.empty
        for player in boxscore.away_players:
            assert not player.dataframe.empty

    def test_nfl_boxscore_string_representation(self):
        expected = (
            "Boxscore for Houston Texans at Kansas City Chiefs "
            "(Thursday Sep 10, 2020)"
        )

        assert self.boxscore.__repr__() == expected


class TestNFLBoxscores:
    def setup_method(self):
        self.expected = {
            "1-2020": [
                {
                    "away_abbr": "htx",
                    "away_name": "Houston Texans",
                    "away_score": 20,
                    "boxscore": "202009100kan",
                    "home_abbr": "kan",
                    "home_name": "Kansas City Chiefs",
                    "home_score": 34,
                    "losing_abbr": "htx",
                    "losing_name": "Houston Texans",
                    "winning_abbr": "kan",
                    "winning_name": "Kansas City Chiefs",
                },
                {
                    "away_abbr": "sea",
                    "away_name": "Seattle Seahawks",
                    "away_score": 38,
                    "boxscore": "202009130atl",
                    "home_abbr": "atl",
                    "home_name": "Atlanta Falcons",
                    "home_score": 25,
                    "losing_abbr": "atl",
                    "losing_name": "Atlanta Falcons",
                    "winning_abbr": "sea",
                    "winning_name": "Seattle Seahawks",
                },
                {
                    "away_abbr": "nyj",
                    "away_name": "New York Jets",
                    "away_score": 17,
                    "boxscore": "202009130buf",
                    "home_abbr": "buf",
                    "home_name": "Buffalo Bills",
                    "home_score": 27,
                    "losing_abbr": "nyj",
                    "losing_name": "New York Jets",
                    "winning_abbr": "buf",
                    "winning_name": "Buffalo Bills",
                },
                {
                    "away_abbr": "rai",
                    "away_name": "Las Vegas Raiders",
                    "away_score": 34,
                    "boxscore": "202009130car",
                    "home_abbr": "car",
                    "home_name": "Carolina Panthers",
                    "home_score": 30,
                    "losing_abbr": "car",
                    "losing_name": "Carolina Panthers",
                    "winning_abbr": "rai",
                    "winning_name": "Las Vegas Raiders",
                },
                {
                    "away_abbr": "chi",
                    "away_name": "Chicago Bears",
                    "away_score": 27,
                    "boxscore": "202009130det",
                    "home_abbr": "det",
                    "home_name": "Detroit Lions",
                    "home_score": 23,
                    "losing_abbr": "det",
                    "losing_name": "Detroit Lions",
                    "winning_abbr": "chi",
                    "winning_name": "Chicago Bears",
                },
                {
                    "away_abbr": "clt",
                    "away_name": "Indianapolis Colts",
                    "away_score": 20,
                    "boxscore": "202009130jax",
                    "home_abbr": "jax",
                    "home_name": "Jacksonville Jaguars",
                    "home_score": 27,
                    "losing_abbr": "clt",
                    "losing_name": "Indianapolis Colts",
                    "winning_abbr": "jax",
                    "winning_name": "Jacksonville Jaguars",
                },
                {
                    "away_abbr": "gnb",
                    "away_name": "Green Bay Packers",
                    "away_score": 43,
                    "boxscore": "202009130min",
                    "home_abbr": "min",
                    "home_name": "Minnesota Vikings",
                    "home_score": 34,
                    "losing_abbr": "min",
                    "losing_name": "Minnesota Vikings",
                    "winning_abbr": "gnb",
                    "winning_name": "Green Bay Packers",
                },
                {
                    "away_abbr": "mia",
                    "away_name": "Miami Dolphins",
                    "away_score": 11,
                    "boxscore": "202009130nwe",
                    "home_abbr": "nwe",
                    "home_name": "New England Patriots",
                    "home_score": 21,
                    "losing_abbr": "mia",
                    "losing_name": "Miami Dolphins",
                    "winning_abbr": "nwe",
                    "winning_name": "New England Patriots",
                },
                {
                    "away_abbr": "cle",
                    "away_name": "Cleveland Browns",
                    "away_score": 6,
                    "boxscore": "202009130rav",
                    "home_abbr": "rav",
                    "home_name": "Baltimore Ravens",
                    "home_score": 38,
                    "losing_abbr": "cle",
                    "losing_name": "Cleveland Browns",
                    "winning_abbr": "rav",
                    "winning_name": "Baltimore Ravens",
                },
                {
                    "away_abbr": "phi",
                    "away_name": "Philadelphia Eagles",
                    "away_score": 17,
                    "boxscore": "202009130was",
                    "home_abbr": "was",
                    "home_name": "Washington Football Team",
                    "home_score": 27,
                    "losing_abbr": "phi",
                    "losing_name": "Philadelphia Eagles",
                    "winning_abbr": "was",
                    "winning_name": "Washington Football Team",
                },
                {
                    "away_abbr": "sdg",
                    "away_name": "Los Angeles Chargers",
                    "away_score": 16,
                    "boxscore": "202009130cin",
                    "home_abbr": "cin",
                    "home_name": "Cincinnati Bengals",
                    "home_score": 13,
                    "losing_abbr": "cin",
                    "losing_name": "Cincinnati Bengals",
                    "winning_abbr": "sdg",
                    "winning_name": "Los Angeles Chargers",
                },
                {
                    "away_abbr": "tam",
                    "away_name": "Tampa Bay Buccaneers",
                    "away_score": 23,
                    "boxscore": "202009130nor",
                    "home_abbr": "nor",
                    "home_name": "New Orleans Saints",
                    "home_score": 34,
                    "losing_abbr": "tam",
                    "losing_name": "Tampa Bay Buccaneers",
                    "winning_abbr": "nor",
                    "winning_name": "New Orleans Saints",
                },
                {
                    "away_abbr": "crd",
                    "away_name": "Arizona Cardinals",
                    "away_score": 24,
                    "boxscore": "202009130sfo",
                    "home_abbr": "sfo",
                    "home_name": "San Francisco 49ers",
                    "home_score": 20,
                    "losing_abbr": "sfo",
                    "losing_name": "San Francisco 49ers",
                    "winning_abbr": "crd",
                    "winning_name": "Arizona Cardinals",
                },
                {
                    "away_abbr": "dal",
                    "away_name": "Dallas Cowboys",
                    "away_score": 17,
                    "boxscore": "202009130ram",
                    "home_abbr": "ram",
                    "home_name": "Los Angeles Rams",
                    "home_score": 20,
                    "losing_abbr": "dal",
                    "losing_name": "Dallas Cowboys",
                    "winning_abbr": "ram",
                    "winning_name": "Los Angeles Rams",
                },
                {
                    "away_abbr": "pit",
                    "away_name": "Pittsburgh Steelers",
                    "away_score": 26,
                    "boxscore": "202009140nyg",
                    "home_abbr": "nyg",
                    "home_name": "New York Giants",
                    "home_score": 16,
                    "losing_abbr": "nyg",
                    "losing_name": "New York Giants",
                    "winning_abbr": "pit",
                    "winning_name": "Pittsburgh Steelers",
                },
                {
                    "away_abbr": "oti",
                    "away_name": "Tennessee Titans",
                    "away_score": 16,
                    "boxscore": "202009140den",
                    "home_abbr": "den",
                    "home_name": "Denver Broncos",
                    "home_score": 14,
                    "losing_abbr": "den",
                    "losing_name": "Denver Broncos",
                    "winning_abbr": "oti",
                    "winning_name": "Tennessee Titans",
                },
            ]
        }

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_boxscores_search(self, *args, **kwargs):
        result = Boxscores(1, 2020).games

        assert result == self.expected

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_boxscores_search_invalid_end(self, *args, **kwargs):
        result = Boxscores(1, 2020, 0).games

        assert result == self.expected

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_boxscores_search_multiple_weeks(self, *args, **kwargs):
        expected = {
            "1-2020": [
                {
                    "away_abbr": "htx",
                    "away_name": "Houston Texans",
                    "away_score": 20,
                    "boxscore": "202009100kan",
                    "home_abbr": "kan",
                    "home_name": "Kansas City Chiefs",
                    "home_score": 34,
                    "losing_abbr": "htx",
                    "losing_name": "Houston Texans",
                    "winning_abbr": "kan",
                    "winning_name": "Kansas City Chiefs",
                },
                {
                    "away_abbr": "sea",
                    "away_name": "Seattle Seahawks",
                    "away_score": 38,
                    "boxscore": "202009130atl",
                    "home_abbr": "atl",
                    "home_name": "Atlanta Falcons",
                    "home_score": 25,
                    "losing_abbr": "atl",
                    "losing_name": "Atlanta Falcons",
                    "winning_abbr": "sea",
                    "winning_name": "Seattle Seahawks",
                },
                {
                    "away_abbr": "nyj",
                    "away_name": "New York Jets",
                    "away_score": 17,
                    "boxscore": "202009130buf",
                    "home_abbr": "buf",
                    "home_name": "Buffalo Bills",
                    "home_score": 27,
                    "losing_abbr": "nyj",
                    "losing_name": "New York Jets",
                    "winning_abbr": "buf",
                    "winning_name": "Buffalo Bills",
                },
                {
                    "away_abbr": "rai",
                    "away_name": "Las Vegas Raiders",
                    "away_score": 34,
                    "boxscore": "202009130car",
                    "home_abbr": "car",
                    "home_name": "Carolina Panthers",
                    "home_score": 30,
                    "losing_abbr": "car",
                    "losing_name": "Carolina Panthers",
                    "winning_abbr": "rai",
                    "winning_name": "Las Vegas Raiders",
                },
                {
                    "away_abbr": "chi",
                    "away_name": "Chicago Bears",
                    "away_score": 27,
                    "boxscore": "202009130det",
                    "home_abbr": "det",
                    "home_name": "Detroit Lions",
                    "home_score": 23,
                    "losing_abbr": "det",
                    "losing_name": "Detroit Lions",
                    "winning_abbr": "chi",
                    "winning_name": "Chicago Bears",
                },
                {
                    "away_abbr": "clt",
                    "away_name": "Indianapolis Colts",
                    "away_score": 20,
                    "boxscore": "202009130jax",
                    "home_abbr": "jax",
                    "home_name": "Jacksonville Jaguars",
                    "home_score": 27,
                    "losing_abbr": "clt",
                    "losing_name": "Indianapolis Colts",
                    "winning_abbr": "jax",
                    "winning_name": "Jacksonville Jaguars",
                },
                {
                    "away_abbr": "gnb",
                    "away_name": "Green Bay Packers",
                    "away_score": 43,
                    "boxscore": "202009130min",
                    "home_abbr": "min",
                    "home_name": "Minnesota Vikings",
                    "home_score": 34,
                    "losing_abbr": "min",
                    "losing_name": "Minnesota Vikings",
                    "winning_abbr": "gnb",
                    "winning_name": "Green Bay Packers",
                },
                {
                    "away_abbr": "mia",
                    "away_name": "Miami Dolphins",
                    "away_score": 11,
                    "boxscore": "202009130nwe",
                    "home_abbr": "nwe",
                    "home_name": "New England Patriots",
                    "home_score": 21,
                    "losing_abbr": "mia",
                    "losing_name": "Miami Dolphins",
                    "winning_abbr": "nwe",
                    "winning_name": "New England Patriots",
                },
                {
                    "away_abbr": "cle",
                    "away_name": "Cleveland Browns",
                    "away_score": 6,
                    "boxscore": "202009130rav",
                    "home_abbr": "rav",
                    "home_name": "Baltimore Ravens",
                    "home_score": 38,
                    "losing_abbr": "cle",
                    "losing_name": "Cleveland Browns",
                    "winning_abbr": "rav",
                    "winning_name": "Baltimore Ravens",
                },
                {
                    "away_abbr": "phi",
                    "away_name": "Philadelphia Eagles",
                    "away_score": 17,
                    "boxscore": "202009130was",
                    "home_abbr": "was",
                    "home_name": "Washington Football Team",
                    "home_score": 27,
                    "losing_abbr": "phi",
                    "losing_name": "Philadelphia Eagles",
                    "winning_abbr": "was",
                    "winning_name": "Washington Football Team",
                },
                {
                    "away_abbr": "sdg",
                    "away_name": "Los Angeles Chargers",
                    "away_score": 16,
                    "boxscore": "202009130cin",
                    "home_abbr": "cin",
                    "home_name": "Cincinnati Bengals",
                    "home_score": 13,
                    "losing_abbr": "cin",
                    "losing_name": "Cincinnati Bengals",
                    "winning_abbr": "sdg",
                    "winning_name": "Los Angeles Chargers",
                },
                {
                    "away_abbr": "tam",
                    "away_name": "Tampa Bay Buccaneers",
                    "away_score": 23,
                    "boxscore": "202009130nor",
                    "home_abbr": "nor",
                    "home_name": "New Orleans Saints",
                    "home_score": 34,
                    "losing_abbr": "tam",
                    "losing_name": "Tampa Bay Buccaneers",
                    "winning_abbr": "nor",
                    "winning_name": "New Orleans Saints",
                },
                {
                    "away_abbr": "crd",
                    "away_name": "Arizona Cardinals",
                    "away_score": 24,
                    "boxscore": "202009130sfo",
                    "home_abbr": "sfo",
                    "home_name": "San Francisco 49ers",
                    "home_score": 20,
                    "losing_abbr": "sfo",
                    "losing_name": "San Francisco 49ers",
                    "winning_abbr": "crd",
                    "winning_name": "Arizona Cardinals",
                },
                {
                    "away_abbr": "dal",
                    "away_name": "Dallas Cowboys",
                    "away_score": 17,
                    "boxscore": "202009130ram",
                    "home_abbr": "ram",
                    "home_name": "Los Angeles Rams",
                    "home_score": 20,
                    "losing_abbr": "dal",
                    "losing_name": "Dallas Cowboys",
                    "winning_abbr": "ram",
                    "winning_name": "Los Angeles Rams",
                },
                {
                    "away_abbr": "pit",
                    "away_name": "Pittsburgh Steelers",
                    "away_score": 26,
                    "boxscore": "202009140nyg",
                    "home_abbr": "nyg",
                    "home_name": "New York Giants",
                    "home_score": 16,
                    "losing_abbr": "nyg",
                    "losing_name": "New York Giants",
                    "winning_abbr": "pit",
                    "winning_name": "Pittsburgh Steelers",
                },
                {
                    "away_abbr": "oti",
                    "away_name": "Tennessee Titans",
                    "away_score": 16,
                    "boxscore": "202009140den",
                    "home_abbr": "den",
                    "home_name": "Denver Broncos",
                    "home_score": 14,
                    "losing_abbr": "den",
                    "losing_name": "Denver Broncos",
                    "winning_abbr": "oti",
                    "winning_name": "Tennessee Titans",
                },
            ],
            "2-2020": [
                {
                    "away_abbr": "cin",
                    "away_name": "Cincinnati Bengals",
                    "away_score": 30,
                    "boxscore": "202009170cle",
                    "home_abbr": "cle",
                    "home_name": "Cleveland Browns",
                    "home_score": 35,
                    "losing_abbr": "cin",
                    "losing_name": "Cincinnati Bengals",
                    "winning_abbr": "cle",
                    "winning_name": "Cleveland Browns",
                },
                {
                    "away_abbr": "nyg",
                    "away_name": "New York Giants",
                    "away_score": 13,
                    "boxscore": "202009200chi",
                    "home_abbr": "chi",
                    "home_name": "Chicago Bears",
                    "home_score": 17,
                    "losing_abbr": "nyg",
                    "losing_name": "New York Giants",
                    "winning_abbr": "chi",
                    "winning_name": "Chicago Bears",
                },
                {
                    "away_abbr": "min",
                    "away_name": "Minnesota Vikings",
                    "away_score": 11,
                    "boxscore": "202009200clt",
                    "home_abbr": "clt",
                    "home_name": "Indianapolis Colts",
                    "home_score": 28,
                    "losing_abbr": "min",
                    "losing_name": "Minnesota Vikings",
                    "winning_abbr": "clt",
                    "winning_name": "Indianapolis Colts",
                },
                {
                    "away_abbr": "atl",
                    "away_name": "Atlanta Falcons",
                    "away_score": 39,
                    "boxscore": "202009200dal",
                    "home_abbr": "dal",
                    "home_name": "Dallas Cowboys",
                    "home_score": 40,
                    "losing_abbr": "atl",
                    "losing_name": "Atlanta Falcons",
                    "winning_abbr": "dal",
                    "winning_name": "Dallas Cowboys",
                },
                {
                    "away_abbr": "det",
                    "away_name": "Detroit Lions",
                    "away_score": 21,
                    "boxscore": "202009200gnb",
                    "home_abbr": "gnb",
                    "home_name": "Green Bay Packers",
                    "home_score": 42,
                    "losing_abbr": "det",
                    "losing_name": "Detroit Lions",
                    "winning_abbr": "gnb",
                    "winning_name": "Green Bay Packers",
                },
                {
                    "away_abbr": "buf",
                    "away_name": "Buffalo Bills",
                    "away_score": 31,
                    "boxscore": "202009200mia",
                    "home_abbr": "mia",
                    "home_name": "Miami Dolphins",
                    "home_score": 28,
                    "losing_abbr": "mia",
                    "losing_name": "Miami Dolphins",
                    "winning_abbr": "buf",
                    "winning_name": "Buffalo Bills",
                },
                {
                    "away_abbr": "sfo",
                    "away_name": "San Francisco 49ers",
                    "away_score": 31,
                    "boxscore": "202009200nyj",
                    "home_abbr": "nyj",
                    "home_name": "New York Jets",
                    "home_score": 13,
                    "losing_abbr": "nyj",
                    "losing_name": "New York Jets",
                    "winning_abbr": "sfo",
                    "winning_name": "San Francisco 49ers",
                },
                {
                    "away_abbr": "jax",
                    "away_name": "Jacksonville Jaguars",
                    "away_score": 30,
                    "boxscore": "202009200oti",
                    "home_abbr": "oti",
                    "home_name": "Tennessee Titans",
                    "home_score": 33,
                    "losing_abbr": "jax",
                    "losing_name": "Jacksonville Jaguars",
                    "winning_abbr": "oti",
                    "winning_name": "Tennessee Titans",
                },
                {
                    "away_abbr": "ram",
                    "away_name": "Los Angeles Rams",
                    "away_score": 37,
                    "boxscore": "202009200phi",
                    "home_abbr": "phi",
                    "home_name": "Philadelphia Eagles",
                    "home_score": 19,
                    "losing_abbr": "phi",
                    "losing_name": "Philadelphia Eagles",
                    "winning_abbr": "ram",
                    "winning_name": "Los Angeles Rams",
                },
                {
                    "away_abbr": "den",
                    "away_name": "Denver Broncos",
                    "away_score": 21,
                    "boxscore": "202009200pit",
                    "home_abbr": "pit",
                    "home_name": "Pittsburgh Steelers",
                    "home_score": 26,
                    "losing_abbr": "den",
                    "losing_name": "Denver Broncos",
                    "winning_abbr": "pit",
                    "winning_name": "Pittsburgh Steelers",
                },
                {
                    "away_abbr": "car",
                    "away_name": "Carolina Panthers",
                    "away_score": 17,
                    "boxscore": "202009200tam",
                    "home_abbr": "tam",
                    "home_name": "Tampa Bay Buccaneers",
                    "home_score": 31,
                    "losing_abbr": "car",
                    "losing_name": "Carolina Panthers",
                    "winning_abbr": "tam",
                    "winning_name": "Tampa Bay Buccaneers",
                },
                {
                    "away_abbr": "was",
                    "away_name": "Washington Football Team",
                    "away_score": 15,
                    "boxscore": "202009200crd",
                    "home_abbr": "crd",
                    "home_name": "Arizona Cardinals",
                    "home_score": 30,
                    "losing_abbr": "was",
                    "losing_name": "Washington Football Team",
                    "winning_abbr": "crd",
                    "winning_name": "Arizona Cardinals",
                },
                {
                    "away_abbr": "rav",
                    "away_name": "Baltimore Ravens",
                    "away_score": 33,
                    "boxscore": "202009200htx",
                    "home_abbr": "htx",
                    "home_name": "Houston Texans",
                    "home_score": 16,
                    "losing_abbr": "htx",
                    "losing_name": "Houston Texans",
                    "winning_abbr": "rav",
                    "winning_name": "Baltimore Ravens",
                },
                {
                    "away_abbr": "kan",
                    "away_name": "Kansas City Chiefs",
                    "away_score": 23,
                    "boxscore": "202009200sdg",
                    "home_abbr": "sdg",
                    "home_name": "Los Angeles Chargers",
                    "home_score": 20,
                    "losing_abbr": "sdg",
                    "losing_name": "Los Angeles Chargers",
                    "winning_abbr": "kan",
                    "winning_name": "Kansas City Chiefs",
                },
                {
                    "away_abbr": "nwe",
                    "away_name": "New England Patriots",
                    "away_score": 30,
                    "boxscore": "202009200sea",
                    "home_abbr": "sea",
                    "home_name": "Seattle Seahawks",
                    "home_score": 35,
                    "losing_abbr": "nwe",
                    "losing_name": "New England Patriots",
                    "winning_abbr": "sea",
                    "winning_name": "Seattle Seahawks",
                },
                {
                    "away_abbr": "nor",
                    "away_name": "New Orleans Saints",
                    "away_score": 24,
                    "boxscore": "202009210rai",
                    "home_abbr": "rai",
                    "home_name": "Las Vegas Raiders",
                    "home_score": 34,
                    "losing_abbr": "nor",
                    "losing_name": "New Orleans Saints",
                    "winning_abbr": "rai",
                    "winning_name": "Las Vegas Raiders",
                },
            ],
        }
        result = Boxscores(1, 2020, 2).games

        assert result == expected

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_boxscores_search_string_representation(self, *args, **kwargs):
        result = Boxscores(1, 2020)

        assert result.__repr__() == "NFL games for week 1"

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_boxscores_search_string_representation_multi_week(self, *args, **kwargs):
        result = Boxscores(1, 2020, 2)

        assert result.__repr__() == "NFL games for weeks 1, 2"
