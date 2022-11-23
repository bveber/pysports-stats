import pandas as pd
import pytest
from datetime import datetime
from flexmock import flexmock
from mock import patch
from os import path
from pyquery import PyQuery as pq
from sports import utils
from sports.constants import AWAY, DRAW
from sports.fb.schedule import Schedule
from ..utils import read_file


NUM_GAMES_IN_SCHEDULE = 47


def mock_pyquery(url):
    if '361ca564' in url:
        return read_file('tottenham-hotspur-2022-2023.html', 'fb', 'schedule')
    return None


class TestFBSchedule:
    @patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.game_date = datetime(2022,8,14)
        self.results = {
            'competition': 'Premier League',
            'matchweek': 'Matchweek 2',
            'day': 'Sun',
            'date': '2022-08-14',
            'time': None,
            'datetime': self.game_date,
            'venue': 'Away',
            'result': 'Draw',
            'goals_for': 2,
            'goals_against': 2,
            'shootout_scored': None,
            'shootout_against': None,
            'opponent': 'Chelsea',
            'opponent_id': 'cff3d9bb',
            'expected_goals': 1.0,
            'expected_goals_against': 1.6,
            'attendance': 39946,
            'captain': 'Hugo Lloris',
            'captain_id': '8f62b6ee',
            'formation': '3-4-3',
            'referee': 'Anthony Taylor',
            'match_report': '01e57bf5',
            'notes': ''
        }

        self.schedule = Schedule('Tottenham Hotspur')

    def test_fb_schedule_returns_correct_number_of_games(self):
        assert len(self.schedule) == NUM_GAMES_IN_SCHEDULE

    def test_fb_schedule_returns_requested_match_from_index(self):
        match_two = self.schedule[1]

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_fb_schedule_returns_requested_match_from_date(self):
        match_two = self.schedule(self.game_date)

        for attribute, value in self.results.items():
            assert getattr(match_two, attribute) == value

    def test_no_games_for_date_raises_value_error(self):
        with pytest.raises(ValueError):
            self.schedule(datetime(2022, 7, 1))

    @patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_empty_page_return_no_games(self, *args, **kwargs):
        flexmock(utils) \
            .should_receive('_no_data_found') \
            .once()
        flexmock(utils) \
            .should_receive('_get_stats_table') \
            .and_return(None)

        schedule = Schedule('Tottenham Hotspur')

        assert len(schedule) == 0

    def test_schedule_iter_returns_correct_number_of_games(self):
        for count, _ in enumerate(self.schedule):
            pass

        assert count + 1 == NUM_GAMES_IN_SCHEDULE

    def test_fb_schedule_dataframe_returns_dataframe(self):
        df = pd.DataFrame([self.results], index=['a4ba771e'])

        match_two = self.schedule[1]
        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected on above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, match_two.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

        assert df1.empty

    def test_no_captain_returns_default(self):
        table_item = '<td data-stat="captain"><a></a></td>'

        captain = self.schedule[0]._parse_captain_id(pq(table_item))

        assert not captain

    def test_no_match_report_returns_default(self):
        table_item = '<td data-stat="match_report"><a></a></td>'

        report = self.schedule[0]._parse_match_report(pq(table_item))

        assert not report

    def test_fb_schedule_string_representation(self):
        expected = """2022-08-06 - Southampton
2022-08-14 - Chelsea
2022-08-20 - Wolves
2022-08-28 - Nott'ham Forest
2022-08-31 - West Ham
2022-09-03 - Fulham
2022-09-07 - fr Marseille
2022-09-10 - Manchester City
2022-09-13 - pt Sporting CP
2022-09-17 - Leicester City
2022-10-01 - Arsenal
2022-10-04 - de Eint Frankfurt
2022-10-08 - Brighton
2022-10-12 - de Eint Frankfurt
2022-10-15 - Everton
2022-10-19 - Manchester Utd
2022-10-23 - Newcastle Utd
2022-10-26 - pt Sporting CP
2022-10-29 - Bournemouth
2022-11-01 - fr Marseille
2022-11-06 - Liverpool
2022-11-09 - Nott'ham Forest
2022-11-12 - Leeds United
2022-12-26 - Brentford
2023-01-01 - Aston Villa
2023-01-04 - Crystal Palace
2023-01-15 - Arsenal
2023-01-23 - Fulham
2023-02-04 - Manchester City
2023-02-11 - Leicester City
2023-02-14 - it Milan
2023-02-18 - West Ham
2023-02-25 - Chelsea
2023-03-04 - Wolves
2023-03-08 - it Milan
2023-03-11 - Nott'ham Forest
2023-03-18 - Southampton
2023-04-01 - Everton
2023-04-08 - Brighton
2023-04-15 - Bournemouth
2023-04-22 - Newcastle Utd
2023-04-25 - Manchester Utd
2023-04-29 - Liverpool
2023-05-06 - Crystal Palace
2023-05-13 - Aston Villa
2023-05-20 - Brentford
2023-05-28 - Leeds United"""

        assert self.schedule.__repr__() == expected

    def test_fb_game_string_representation(self):
        game = self.schedule[0]

        assert game.__repr__() == '2022-08-06 - Southampton'
