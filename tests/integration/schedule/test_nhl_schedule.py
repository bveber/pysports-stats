import mock
import os
import pandas as pd
import pytest
from datetime import datetime
from flexmock import flexmock
from sportsipy import utils
from sportsipy.constants import AWAY, LOSS
from sportsipy.nhl.boxscore import Boxscore
from sportsipy.nhl.constants import SCHEDULE_URL
from sportsipy.nhl.schedule import Schedule
from ..utils import read_file


MONTH = 1
YEAR = 2022
TEAM = 'MIN'

NUM_GAMES_IN_SCHEDULE = 82


def mock_pyquery(url):
    if 'MIN/2022_gamelog' in url:
        return read_file('MIN-2022_gamelog.html', 'nhl', 'schedule')
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


class TestNHLSchedule:
    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.game_datetime = datetime(2021,10,16)
        self.results = {
            'boxscore_index': '202110160LAK',
            'date': '2021-10-16',
            'datetime': self.game_datetime,
            'game': 2,
            'goals_allowed': 2,
            'goals_scored': 3,
            'location': 'Away',
            'opponent_abbr': 'LAK',
            'opponent_name': 'Los Angeles Kings',
            'overtime': 0,
            'penalties_in_minutes': 10,
            'power_play_goals': 0,
            'power_play_opportunities': 1,
            'result': 'Win',
            'short_handed_goals': 0,
            'shots_on_goal': 30,
            'opp_shots_on_goal': 31,
            'opp_penalties_in_minutes': 4,
            'opp_power_play_goals': 1,
            'opp_power_play_opportunities': 4,
            'opp_short_handed_goals': 0,
            'corsi_for': 39,
            'corsi_against': 49,
            'corsi_for_percentage': 44.3,
            'fenwick_for': 34,
            'fenwick_against': 36,
            'fenwick_for_percentage': 48.6,
            'faceoff_wins': 17,
            'faceoff_losses': 22,
            'faceoff_win_percentage': 43.6,
            'offensive_zone_start_percentage': 44.0,
            'pdo': 107.3
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

        
        self.schedule = Schedule(TEAM, year=YEAR)

    def test_nhl_schedule_returns_correct_number_of_games(self):
        assert len(self.schedule) == NUM_GAMES_IN_SCHEDULE

    def test_nhl_schedule_returns_requested_match_from_index(self):
        match_two = self.schedule[1]

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_nhl_schedule_returns_requested_match_from_date(self):
        match_two = self.schedule(self.game_datetime)

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_nhl_schedule_dataframe_returns_dataframe(self):
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

    def test_nhl_schedule_dataframe_extended_returns_dataframe(self):
        df = pd.DataFrame([{'key': 'value'}])

        result = self.schedule[1].dataframe_extended

        frames = [df, result]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_nhl_schedule_all_dataframe_returns_dataframe(self):
        result = self.schedule.dataframe.drop_duplicates(keep=False)

        assert len(result) == NUM_GAMES_IN_SCHEDULE
        assert set(result.columns.values) == set(self.results.keys())

    def test_nhl_schedule_all_dataframe_extended_returns_dataframe(self):
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

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_game_string_representation(self, *args, **kwargs):
        game = self.schedule[0]

        assert game.__repr__() == '2021-10-15 - ANA'

    def test_schedule_string_representation(self):
        expected = """2021-10-15 - ANA
2021-10-16 - LAK
2021-10-19 - WPG
2021-10-23 - ANA
2021-10-24 - NSH
2021-10-26 - VAN
2021-10-28 - SEA
2021-10-30 - COL
2021-11-02 - OTT
2021-11-06 - PIT
2021-11-07 - NYI
2021-11-10 - ARI
2021-11-11 - VEG
2021-11-13 - SEA
2021-11-16 - SJS
2021-11-18 - DAL
2021-11-20 - FLA
2021-11-21 - TBL
2021-11-24 - NJD
2021-11-26 - WPG
2021-11-28 - TBL
2021-11-30 - ARI
2021-12-02 - NJD
2021-12-04 - TOR
2021-12-07 - EDM
2021-12-09 - SJS
2021-12-11 - LAK
2021-12-12 - VEG
2021-12-16 - BUF
2021-12-20 - DAL
2022-01-01 - STL
2022-01-06 - BOS
2022-01-08 - WSH
2022-01-14 - ANA
2022-01-17 - COL
2022-01-21 - CHI
2022-01-22 - CHI
2022-01-24 - MTL
2022-01-28 - NYR
2022-01-30 - NYI
2022-02-02 - CHI
2022-02-08 - WPG
2022-02-12 - CAR
2022-02-14 - DET
2022-02-16 - WPG
2022-02-18 - FLA
2022-02-20 - EDM
2022-02-22 - OTT
2022-02-24 - TOR
2022-02-26 - CGY
2022-03-01 - CGY
2022-03-03 - PHI
2022-03-04 - BUF
2022-03-06 - DAL
2022-03-08 - NYR
2022-03-10 - DET
2022-03-11 - CBJ
2022-03-13 - NSH
2022-03-16 - BOS
2022-03-19 - CHI
2022-03-21 - VEG
2022-03-24 - VAN
2022-03-26 - CBJ
2022-03-27 - COL
2022-03-29 - PHI
2022-03-31 - PIT
2022-04-02 - CAR
2022-04-03 - WSH
2022-04-05 - NSH
2022-04-08 - STL
2022-04-10 - LAK
2022-04-12 - EDM
2022-04-14 - DAL
2022-04-16 - STL
2022-04-17 - SJS
2022-04-19 - MTL
2022-04-21 - VAN
2022-04-22 - SEA
2022-04-24 - NSH
2022-04-26 - ARI
2022-04-28 - CGY
2022-04-29 - COL"""

        assert self.schedule.__repr__() == expected
