import mock
import os
import pandas as pd
import pytest
from datetime import datetime
from flexmock import flexmock
from sports import utils
from sports.constants import AWAY, WIN
from sports.nba.boxscore import Boxscore
from sports.nba.constants import SCHEDULE_URL
from sports.nba.schedule import Schedule
from ..utils import read_file


MONTH = 1
YEAR = 2022

NUM_GAMES_IN_SCHEDULE = 87


def mock_pyquery(url):
    if '2022' in url:
        return read_file('%s_games.html' % YEAR, 'nba', 'schedule')
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


class TestNBASchedule:
    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            'boxscore_index': '202110220DEN',
            'date': 'Fri, Oct 22, 2021',
            'datetime': datetime(2021, 10, 22, 0, 0),
            'game': 2,
            'location': 'Home',
            'losses': 0,
            'opponent_abbr': 'SAS',
            'opponent_name': 'San Antonio Spurs',
            'playoffs': False,
            'points_allowed': 96,
            'points_scored': 102,
            'result': 'Win',
            'streak': 'W 2',
            'time': '9:00p',
            'wins': 2
        }
        flexmock(Boxscore) \
            .should_receive('_parse_game_data') \
            .and_return(None)
        flexmock(Boxscore) \
            .should_receive('dataframe') \
            .and_return(pd.DataFrame([{'key': 'value'}]))
        flexmock(utils) \
            .should_receive('_todays_date') \
            .and_return(MockDateTime(YEAR, MONTH))

        self.schedule = Schedule('DEN')

    def test_nba_schedule_returns_correct_number_of_games(self):
        assert len(self.schedule) == NUM_GAMES_IN_SCHEDULE

    def test_nba_schedule_returns_requested_match_from_index(self):
        match_two = self.schedule[1]

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_nba_schedule_returns_requested_match_from_date(self):
        match_two = self.schedule(datetime(2021, 10, 22))

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_nba_schedule_dataframe_returns_dataframe(self):
        df = pd.DataFrame([self.results], index=['PHO'])

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

    def test_nba_schedule_dataframe_extended_returns_dataframe(self):
        df = pd.DataFrame([{'key': 'value'}])

        result = self.schedule[1].dataframe_extended

        frames = [df, result]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_nba_schedule_all_dataframe_returns_dataframe(self):
        result = self.schedule.dataframe.drop_duplicates(keep=False)

        assert len(result) == NUM_GAMES_IN_SCHEDULE
        assert set(result.columns.values) == set(self.results.keys())

    def test_nba_schedule_all_dataframe_extended_returns_dataframe(self):
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

        schedule = Schedule('DEN')

        assert len(schedule) == 0

    def test_game_string_representation(self):
        game = self.schedule[0]

        assert game.__repr__() == 'Wed, Oct 20, 2021 - PHO'

    def test_schedule_string_representation(self):
        expected = """Wed, Oct 20, 2021 - PHO
Fri, Oct 22, 2021 - SAS
Mon, Oct 25, 2021 - CLE
Tue, Oct 26, 2021 - UTA
Fri, Oct 29, 2021 - DAL
Sat, Oct 30, 2021 - MIN
Mon, Nov 1, 2021 - MEM
Wed, Nov 3, 2021 - MEM
Sat, Nov 6, 2021 - HOU
Mon, Nov 8, 2021 - MIA
Wed, Nov 10, 2021 - IND
Fri, Nov 12, 2021 - ATL
Sun, Nov 14, 2021 - POR
Mon, Nov 15, 2021 - DAL
Thu, Nov 18, 2021 - PHI
Fri, Nov 19, 2021 - CHI
Sun, Nov 21, 2021 - PHO
Tue, Nov 23, 2021 - POR
Fri, Nov 26, 2021 - MIL
Mon, Nov 29, 2021 - MIA
Wed, Dec 1, 2021 - ORL
Sat, Dec 4, 2021 - NYK
Mon, Dec 6, 2021 - CHI
Wed, Dec 8, 2021 - NOP
Thu, Dec 9, 2021 - SAS
Sat, Dec 11, 2021 - SAS
Mon, Dec 13, 2021 - WAS
Wed, Dec 15, 2021 - MIN
Fri, Dec 17, 2021 - ATL
Wed, Dec 22, 2021 - OKC
Thu, Dec 23, 2021 - CHO
Sun, Dec 26, 2021 - LAC
Tue, Dec 28, 2021 - GSW
Sat, Jan 1, 2022 - HOU
Mon, Jan 3, 2022 - DAL
Wed, Jan 5, 2022 - UTA
Fri, Jan 7, 2022 - SAC
Sun, Jan 9, 2022 - OKC
Tue, Jan 11, 2022 - LAC
Thu, Jan 13, 2022 - POR
Sat, Jan 15, 2022 - LAL
Sun, Jan 16, 2022 - UTA
Wed, Jan 19, 2022 - LAC
Fri, Jan 21, 2022 - MEM
Sun, Jan 23, 2022 - DET
Tue, Jan 25, 2022 - DET
Wed, Jan 26, 2022 - BRK
Fri, Jan 28, 2022 - NOP
Sun, Jan 30, 2022 - MIL
Tue, Feb 1, 2022 - MIN
Wed, Feb 2, 2022 - UTA
Fri, Feb 4, 2022 - NOP
Sun, Feb 6, 2022 - BRK
Tue, Feb 8, 2022 - NYK
Fri, Feb 11, 2022 - BOS
Sat, Feb 12, 2022 - TOR
Mon, Feb 14, 2022 - ORL
Wed, Feb 16, 2022 - GSW
Thu, Feb 24, 2022 - SAC
Sat, Feb 26, 2022 - SAC
Sun, Feb 27, 2022 - POR
Wed, Mar 2, 2022 - OKC
Fri, Mar 4, 2022 - HOU
Sun, Mar 6, 2022 - NOP
Mon, Mar 7, 2022 - GSW
Wed, Mar 9, 2022 - SAC
Thu, Mar 10, 2022 - GSW
Sat, Mar 12, 2022 - TOR
Mon, Mar 14, 2022 - PHI
Wed, Mar 16, 2022 - WAS
Fri, Mar 18, 2022 - CLE
Sun, Mar 20, 2022 - BOS
Tue, Mar 22, 2022 - LAC
Thu, Mar 24, 2022 - PHO
Sat, Mar 26, 2022 - OKC
Mon, Mar 28, 2022 - CHO
Wed, Mar 30, 2022 - IND
Fri, Apr 1, 2022 - MIN
Sun, Apr 3, 2022 - LAL
Tue, Apr 5, 2022 - SAS
Thu, Apr 7, 2022 - MEM
Sun, Apr 10, 2022 - LAL
Sat, Apr 16, 2022 - GSW
Mon, Apr 18, 2022 - GSW
Thu, Apr 21, 2022 - GSW
Sun, Apr 24, 2022 - GSW
Wed, Apr 27, 2022 - GSW"""

        assert self.schedule.__repr__() == expected


class TestNBAScheduleInvalidError:
    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    @mock.patch('requests.head', side_effect=mock_request)
    def test_invalid_default_year_reverts_to_previous_year(self,
                                                           *args,
                                                           **kwargs):
        results = {
            'boxscore_index': '202110220DEN',
            'date': 'Fri, Oct 22, 2021',
            'datetime': datetime(2021, 10, 22, 0, 0),
            'game': 2,
            'location': 'Home',
            'losses': 0,
            'opponent_abbr': 'SAS',
            'opponent_name': 'San Antonio Spurs',
            'playoffs': False,
            'points_allowed': 96,
            'points_scored': 102,
            'result': 'Win',
            'streak': 'W 2',
            'time': '9:00p',
            'wins': 2
        }
        flexmock(Boxscore) \
            .should_receive('_parse_game_data') \
            .and_return(None)
        flexmock(Boxscore) \
            .should_receive('dataframe') \
            .and_return(pd.DataFrame([{'key': 'value'}]))
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return(YEAR)

        schedule = Schedule('DEN')

        for attribute, value in results.items():
            assert getattr(schedule[1], attribute) == value
