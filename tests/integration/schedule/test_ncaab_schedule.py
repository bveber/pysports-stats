import mock
import os
import pandas as pd
import pytest
from datetime import datetime
from flexmock import flexmock
from sports import utils
from sports.constants import NEUTRAL, REGULAR_SEASON, WIN
from sports.ncaab.boxscore import Boxscore
from sports.ncaab.constants import SCHEDULE_URL
from sports.ncaab.schedule import Schedule
from ..utils import read_file


MONTH = 11
YEAR = 2022

NUM_GAMES_IN_SCHEDULE = 37


def mock_pyquery(url):
    if "purdue" in url:
        return read_file("PURDUE-2022-schedule.html", "ncaab", "schedule")
    else:
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


class TestNCAABSchedule:
    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            "arena": "",
            "boxscore_index": "2021-11-12-20-purdue",
            "date": "Fri, Nov 12, 2021",
            "datetime": datetime(2021, 11, 12, 20, 30),
            "game": 2,
            "location": "Home",
            "opponent_abbr": "indiana-state",
            "opponent_conference": "MVC",
            "opponent_name": "Indiana State",
            "opponent_rank": None,
            "overtimes": 0,
            "points_against": 67,
            "points_for": 92,
            "result": "Win",
            "season_losses": 0,
            "season_wins": 2,
            "streak": "W 2",
            "time": "8:30p",
            "type": "Reg",
        }
        flexmock(utils).should_receive("_todays_date").and_return(
            MockDateTime(YEAR, MONTH)
        )
        flexmock(Boxscore).should_receive("_parse_game_data").and_return(None)
        flexmock(Boxscore).should_receive("dataframe").and_return(
            pd.DataFrame([{"key": "value"}])
        )

        self.schedule = Schedule("PURDUE")

    def test_ncaab_schedule_returns_correct_number_of_games(self):
        assert len(self.schedule) == NUM_GAMES_IN_SCHEDULE

    def test_ncaab_schedule_returns_requested_match_from_index(self):
        match_two = self.schedule[1]

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_ncaab_schedule_returns_requested_match_from_date(self):
        match_two = self.schedule(datetime(2021, 11, 12))

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_ncaab_schedule_dataframe_returns_dataframe(self):
        df = pd.DataFrame([self.results], index=["PURDUE"])

        match_two = self.schedule[1]
        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected one above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, match_two.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_ncaab_schedule_dataframe_extended_returns_dataframe(self):
        df = pd.DataFrame([{"key": "value"}])

        result = self.schedule[1].dataframe_extended

        frames = [df, result]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_ncaab_schedule_all_dataframe_returns_dataframe(self):

        result = self.schedule.dataframe.drop_duplicates(keep=False)

        assert len(result) == NUM_GAMES_IN_SCHEDULE
        assert set(result.columns.values) == set(self.results.keys())

    def test_ncaab_schedule_all_dataframe_extended_returns_dataframe(self):
        result = self.schedule.dataframe_extended

        assert len(result) == NUM_GAMES_IN_SCHEDULE

    def test_no_games_for_date_raises_value_error(self):
        with pytest.raises(ValueError):
            self.schedule(datetime.now())

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_empty_page_return_no_games(self, *args, **kwargs):
        flexmock(utils).should_receive("_no_data_found").once()
        flexmock(utils).should_receive("_get_stats_table").and_return(None)

        schedule = Schedule("PURDUE")

        assert len(schedule) == 0

    def test_game_string_representation(self):
        game = self.schedule[0]

        assert game.__repr__() == "Tue, Nov 9, 2021 - bellarmine"

    def test_schedule_string_representation(self):
        expected = """Tue, Nov 9, 2021 - bellarmine
Fri, Nov 12, 2021 - indiana-state
Tue, Nov 16, 2021 - wright-state
Sat, Nov 20, 2021 - north-carolina
Sun, Nov 21, 2021 - villanova
Fri, Nov 26, 2021 - nebraska-omaha
Tue, Nov 30, 2021 - florida-state
Fri, Dec 3, 2021 - iowa
Thu, Dec 9, 2021 - rutgers
Sun, Dec 12, 2021 - north-carolina-state
Sat, Dec 18, 2021 - butler
Mon, Dec 20, 2021 - incarnate-word
Wed, Dec 29, 2021 - nicholls-state
Mon, Jan 3, 2022 - wisconsin
Sat, Jan 8, 2022 - penn-state
Fri, Jan 14, 2022 - nebraska
Mon, Jan 17, 2022 - illinois
Thu, Jan 20, 2022 - indiana
Sun, Jan 23, 2022 - northwestern
Thu, Jan 27, 2022 - iowa
Sun, Jan 30, 2022 - ohio-state
Wed, Feb 2, 2022 - minnesota
Sat, Feb 5, 2022 - michigan
Tue, Feb 8, 2022 - illinois
Thu, Feb 10, 2022 - michigan
Sun, Feb 13, 2022 - maryland
Wed, Feb 16, 2022 - northwestern
Sun, Feb 20, 2022 - rutgers
Sat, Feb 26, 2022 - michigan-state
Tue, Mar 1, 2022 - wisconsin
Sat, Mar 5, 2022 - indiana
Fri, Mar 11, 2022 - penn-state
Sat, Mar 12, 2022 - michigan-state
Sun, Mar 13, 2022 - iowa
Fri, Mar 18, 2022 - yale
Sun, Mar 20, 2022 - texas
Fri, Mar 25, 2022 - saint-peters"""

        assert self.schedule.__repr__() == expected
