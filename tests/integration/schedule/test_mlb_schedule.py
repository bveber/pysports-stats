import mock
import os
import pandas as pd
import pytest
from datetime import datetime
from flexmock import flexmock
from sportsipy import utils
from sportsipy.constants import AWAY, HOME, LOSS, WIN
from sportsipy.mlb.boxscore import Boxscore
from sportsipy.mlb.constants import DAY, NIGHT, SCHEDULE_URL
from sportsipy.mlb.schedule import Schedule
from ..utils import read_file


MONTH = 4
YEAR = 2022

NUM_GAMES_IN_SCHEDULE = 162
TEAM = 'HOU'


def mock_pyquery(url):
    if 'HOU/2022' in url:
        return read_file('HOU-2022-schedule.shtml', 'mlb', 'schedule')
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


class TestMLBSchedule:
    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            'attendance': 42719,
            'boxscore_index': 'ANA/ANA202204080',
            'date': 'Friday, Apr 8',
            'datetime': datetime(2022,4,8),
            'game_number_for_day': 1,
            'day_or_night': 'Night',
            'game': 2,
            'game_duration': '3:44',
            'games_behind': -0.5,
            'innings': 9,
            'location': 'Away',
            'loser': 'Ortega',
            'opponent_abbr': 'LAA',
            'rank': 1,
            'record': '2-0',
            'result': 'Win',
            'runs_allowed': 6,
            'runs_scored': 13,
            'save': None,
            'streak': '++',
            'winner': 'Montero'
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

        self.schedule = Schedule(TEAM)

    def test_mlb_schedule_returns_correct_number_of_games(self):
        assert len(self.schedule) == NUM_GAMES_IN_SCHEDULE

    def test_mlb_schedule_returns_requested_match_from_index(self):
        match_two = self.schedule[1]

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_mlb_schedule_returns_requested_match_from_date(self):
        match_two = self.schedule(datetime(2022, 4, 8))

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_mlb_schedule_returns_second_game_in_double_header(self):
        date_of_game = datetime(2022, 7, 21)
        match_two = self.schedule(date_of_game, 2)
        results = {
            'attendance': 39342,
            'boxscore_index': 'HOU/HOU202207212',
            'date': 'Thursday, Jul 21 (2)',
            'datetime': datetime(2022,7,21),
            'game_number_for_day': 2,
            'day_or_night': 'Night',
            'game': 93,
            'game_duration': '3:11',
            'games_behind': -10.0,
            'innings': 9,
            'location': 'Home',
            'loser': 'German',
            'opponent_abbr': 'NYY',
            'rank': 1,
            'record': '61-32',
            'result': 'Win',
            'runs_allowed': 5,
            'runs_scored': 7,
            'save': 'Montero',
            'streak': '++',
            'winner': 'Garcia'
        }

        for attribute, value in results.items():
            assert getattr(match_two, attribute) == value

    def test_mlb_schedule_dataframe_returns_dataframe(self):
        df = pd.DataFrame([self.results], index=['NYY'])

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

    def test_mlb_schedule_dataframe_extended_returns_dataframe(self):
        df = pd.DataFrame([{'key': 'value'}])

        result = self.schedule[1].dataframe_extended

        frames = [df, result]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_mlb_schedule_all_dataframe_returns_dataframe(self, *args, **kwargs):
        result = self.schedule.dataframe.drop_duplicates(keep=False)

        assert len(result) == NUM_GAMES_IN_SCHEDULE
        assert set(result.columns.values) == set(self.results.keys())

    def test_mlb_schedule_all_dataframe_extended_returns_dataframe(self):
        result = self.schedule.dataframe_extended

        assert len(result) == NUM_GAMES_IN_SCHEDULE

    def test_no_games_for_date_raises_value_error(self):
        with pytest.raises(ValueError):
            self.schedule(datetime.now())

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
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

        assert game.__repr__() == 'Thursday, Apr 7 - LAA'

    def test_schedule_string_representation(self):
        expected = """Thursday, Apr 7 - LAA
Friday, Apr 8 - LAA
Saturday, Apr 9 - LAA
Sunday, Apr 10 - LAA
Tuesday, Apr 12 - ARI
Wednesday, Apr 13 - ARI
Friday, Apr 15 - SEA
Saturday, Apr 16 - SEA
Sunday, Apr 17 - SEA
Monday, Apr 18 - LAA
Tuesday, Apr 19 - LAA
Wednesday, Apr 20 - LAA
Friday, Apr 22 - TOR
Saturday, Apr 23 - TOR
Sunday, Apr 24 - TOR
Monday, Apr 25 - TEX
Tuesday, Apr 26 - TEX
Wednesday, Apr 27 - TEX
Thursday, Apr 28 - TEX
Friday, Apr 29 - TOR
Saturday, Apr 30 - TOR
Sunday, May 1 - TOR
Monday, May 2 - SEA
Tuesday, May 3 - SEA
Wednesday, May 4 - SEA
Thursday, May 5 - DET
Friday, May 6 - DET
Saturday, May 7 - DET
Sunday, May 8 - DET
Tuesday, May 10 - MIN
Wednesday, May 11 - MIN
Thursday, May 12 - MIN
Friday, May 13 - WSN
Saturday, May 14 - WSN
Sunday, May 15 - WSN
Monday, May 16 - BOS
Tuesday, May 17 - BOS
Wednesday, May 18 - BOS
Thursday, May 19 - TEX
Friday, May 20 - TEX
Saturday, May 21 - TEX
Sunday, May 22 - TEX
Monday, May 23 - CLE
Tuesday, May 24 - CLE
Wednesday, May 25 - CLE
Friday, May 27 - SEA
Saturday, May 28 - SEA
Sunday, May 29 - SEA
Monday, May 30 - OAK
Tuesday, May 31 - OAK
Wednesday, Jun 1 - OAK
Friday, Jun 3 - KCR
Saturday, Jun 4 - KCR
Sunday, Jun 5 - KCR
Monday, Jun 6 - SEA
Tuesday, Jun 7 - SEA
Wednesday, Jun 8 - SEA
Friday, Jun 10 - MIA
Saturday, Jun 11 - MIA
Sunday, Jun 12 - MIA
Monday, Jun 13 - TEX
Tuesday, Jun 14 - TEX
Wednesday, Jun 15 - TEX
Friday, Jun 17 - CHW
Saturday, Jun 18 - CHW
Sunday, Jun 19 - CHW
Tuesday, Jun 21 - NYM
Wednesday, Jun 22 - NYM
Thursday, Jun 23 - NYY
Friday, Jun 24 - NYY
Saturday, Jun 25 - NYY
Sunday, Jun 26 - NYY
Tuesday, Jun 28 - NYM
Wednesday, Jun 29 - NYM
Thursday, Jun 30 - NYY
Friday, Jul 1 - LAA
Saturday, Jul 2 - LAA
Sunday, Jul 3 - LAA
Monday, Jul 4 - KCR
Tuesday, Jul 5 - KCR
Wednesday, Jul 6 - KCR
Thursday, Jul 7 - KCR
Friday, Jul 8 - OAK
Saturday, Jul 9 - OAK
Sunday, Jul 10 - OAK
Tuesday, Jul 12 - LAA
Wednesday, Jul 13 - LAA
Thursday, Jul 14 - LAA
Friday, Jul 15 - OAK
Saturday, Jul 16 - OAK
Sunday, Jul 17 - OAK
Thursday, Jul 21 (1) - NYY
Thursday, Jul 21 (2) - NYY
Friday, Jul 22 - SEA
Saturday, Jul 23 - SEA
Sunday, Jul 24 - SEA
Monday, Jul 25 - OAK
Tuesday, Jul 26 - OAK
Wednesday, Jul 27 - OAK
Thursday, Jul 28 - SEA
Friday, Jul 29 - SEA
Saturday, Jul 30 - SEA
Sunday, Jul 31 - SEA
Monday, Aug 1 - BOS
Tuesday, Aug 2 - BOS
Wednesday, Aug 3 - BOS
Thursday, Aug 4 - CLE
Friday, Aug 5 - CLE
Saturday, Aug 6 - CLE
Sunday, Aug 7 - CLE
Tuesday, Aug 9 - TEX
Wednesday, Aug 10 - TEX
Thursday, Aug 11 - TEX
Friday, Aug 12 - OAK
Saturday, Aug 13 - OAK
Sunday, Aug 14 - OAK
Monday, Aug 15 - CHW
Tuesday, Aug 16 - CHW
Wednesday, Aug 17 - CHW
Thursday, Aug 18 - CHW
Friday, Aug 19 - ATL
Saturday, Aug 20 - ATL
Sunday, Aug 21 - ATL
Tuesday, Aug 23 - MIN
Wednesday, Aug 24 - MIN
Thursday, Aug 25 - MIN
Friday, Aug 26 - BAL
Saturday, Aug 27 - BAL
Sunday, Aug 28 - BAL
Tuesday, Aug 30 - TEX
Wednesday, Aug 31 - TEX
Friday, Sep 2 - LAA
Saturday, Sep 3 - LAA
Sunday, Sep 4 - LAA
Monday, Sep 5 - TEX
Tuesday, Sep 6 - TEX
Wednesday, Sep 7 - TEX
Friday, Sep 9 - LAA
Saturday, Sep 10 - LAA
Sunday, Sep 11 - LAA
Monday, Sep 12 - DET
Tuesday, Sep 13 - DET
Wednesday, Sep 14 - DET
Thursday, Sep 15 - OAK
Friday, Sep 16 - OAK
Saturday, Sep 17 - OAK
Sunday, Sep 18 - OAK
Monday, Sep 19 - TBR
Tuesday, Sep 20 - TBR
Wednesday, Sep 21 - TBR
Thursday, Sep 22 - BAL
Friday, Sep 23 - BAL
Saturday, Sep 24 - BAL
Sunday, Sep 25 - BAL
Tuesday, Sep 27 - ARI
Wednesday, Sep 28 - ARI
Friday, Sep 30 - TBR
Saturday, Oct 1 - TBR
Sunday, Oct 2 - TBR
Monday, Oct 3 - PHI
Tuesday, Oct 4 - PHI
Wednesday, Oct 5 - PHI"""

        assert self.schedule.__repr__() == expected
