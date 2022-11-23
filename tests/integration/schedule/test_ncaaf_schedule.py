import mock
import os
import pandas as pd
import pytest
from datetime import datetime
from flexmock import flexmock
from sports import utils
from sports.constants import HOME, REGULAR_SEASON, WIN
from sports.ncaaf.boxscore import Boxscore
from sports.ncaaf.constants import SCHEDULE_URL
from sports.ncaaf.schedule import Schedule
from ..utils import read_file


MONTH = 9
YEAR = 2021
TEAM = 'PURDUE'

NUM_GAMES_IN_SCHEDULE = 13


def mock_pyquery(url):
    if 'purdue' in url:
        return read_file('PURDUE-2021-schedule.html', 'ncaaf', 'schedule')
    else:
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


class TestNCAAFSchedule:
    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            'boxscore_index': '2021-09-11-connecticut',
            'date': 'Sep 11, 2021',
            'datetime': datetime(2021, 9, 11, 15, 0),
            'day_of_week': 'Sat',
            'game': 2,
            'location': 'Away',
            'losses': 0,
            'opponent_abbr': 'connecticut',
            'opponent_conference': 'Ind',
            'opponent_name': 'Connecticut',
            'opponent_rank': None,
            'points_against': 0,
            'points_for': 49,
            'rank': None,
            'result': 'Win',
            'streak': 'W 2',
            'time': '3:00 PM',
            'wins': 2
        }
        flexmock(utils) \
            .should_receive('_todays_date') \
            .and_return(MockDateTime(YEAR, MONTH))
        flexmock(Boxscore) \
            .should_receive('_parse_game_data') \
            .and_return(None)
        flexmock(Boxscore) \
            .should_receive('dataframe') \
            .and_return(pd.DataFrame([{'key': 'value'}]))

        self.schedule = Schedule(TEAM)

    def test_ncaaf_schedule_returns_correct_number_of_games(self):
        assert len(self.schedule) == NUM_GAMES_IN_SCHEDULE

    def test_ncaaf_schedule_returns_requested_match_from_index(self):
        match_two = self.schedule[1]

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_ncaaf_schedule_returns_requested_match_from_date(self):
        match_two = self.schedule(datetime(2021, 9, 11))

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_ncaaf_schedule_dataframe_returns_dataframe(self):
        df = pd.DataFrame([self.results], index=[TEAM])

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

    def test_ncaaf_schedule_dataframe_extended_returns_dataframe(self):
        df = pd.DataFrame([{'key': 'value'}])

        result = self.schedule[1].dataframe_extended

        frames = [df, result]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_ncaaf_schedule_all_dataframe_returns_dataframe(self):
        result = self.schedule.dataframe.drop_duplicates(keep=False)

        assert len(result) == NUM_GAMES_IN_SCHEDULE
        assert set(result.columns.values) == set(self.results.keys())

    def test_ncaaf_schedule_all_dataframe_extended_returns_dataframe(self):
        result = self.schedule.dataframe_extended

        assert len(result) == NUM_GAMES_IN_SCHEDULE

    def test_no_games_for_date_raises_value_error(self):
        with pytest.raises(ValueError):
            self.schedule(datetime.now())

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_empty_page_return_no_games(self, *args, **kwargs):
        flexmock(utils) \
            .should_receive('_no_data_found') \
            .once()
        flexmock(utils) \
            .should_receive('_get_stats_table') \
            .and_return(None)

        schedule = Schedule(TEAM)

        assert len(schedule) == 0

    def test_game_string_representation(self):
        game = self.schedule[0]

        assert game.__repr__() == 'Sep 4, 2021 - oregon-state'

    def test_schedule_string_representation(self):
        expected = """Sep 4, 2021 - oregon-state
Sep 11, 2021 - connecticut
Sep 18, 2021 - notre-dame
Sep 25, 2021 - illinois
Oct 2, 2021 - minnesota
Oct 16, 2021 - iowa
Oct 23, 2021 - wisconsin
Oct 30, 2021 - nebraska
Nov 6, 2021 - michigan-state
Nov 13, 2021 - ohio-state
Nov 20, 2021 - northwestern
Nov 27, 2021 - indiana
Dec 30, 2021 - tennessee"""

        assert self.schedule.__repr__() == expected
