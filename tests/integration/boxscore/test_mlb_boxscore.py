import mock
import os
import pandas as pd
from datetime import datetime
from flexmock import flexmock
from sports import utils
from sports.constants import HOME
from sports.mlb.constants import BOXSCORE_URL, BOXSCORES_URL, NIGHT
from sports.mlb.boxscore import Boxscore, Boxscores
from pyquery import PyQuery as pq
from ..utils import read_file


MONTH = 10
YEAR = 2020

BOXSCORE = 'ANA/ANA202008170'


def mock_pyquery(url):
    if url == BOXSCORES_URL % (YEAR, 8, 17):
        return read_file('boxscore-8-17-2020.html', 'mlb', 'boxscore')
    if url == BOXSCORES_URL % (YEAR, 8, 18):
        return read_file('boxscore-8-18-2020.html', 'mlb', 'boxscore')
    path = '%s.shtml' % BOXSCORE
    boxscore = read_file(path.replace('ANA/', ''), 'mlb', 'boxscore')
    return boxscore


class MockDateTime:
    def __init__(self, year, month):
        self.year = year
        self.month = month


class TestMLBBoxscore:
    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results = {
            'date': 'Monday, August 17, 2020',
            'time': '6:40 p.m. Local',
            'venue': 'Angel Stadium of Anaheim',
            'time_of_day': NIGHT,
            'duration': '3:12',
            'winner': HOME,
            'winning_name': 'Los Angeles Angels',
            'winning_abbr': 'LAA',
            'losing_name': 'San Francisco Giants',
            'losing_abbr': 'SFG',
            'away_at_bats': 35,
            'away_runs': 6,
            'away_hits': 10,
            'away_rbi': 6,
            'away_earned_runs': 6.0,
            'away_bases_on_balls': 1,
            'away_strikeouts': 5,
            'away_plate_appearances': 38,
            'away_batting_average': .286,
            'away_on_base_percentage': .316,
            'away_slugging_percentage': .457,
            'away_on_base_plus': .773,
            'away_pitches': 140,
            'away_strikes': 100,
            'away_win_probability_for_offensive_player': .291,
            'away_average_leverage_index': 1.15,
            'away_win_probability_added': .896,
            'away_win_probability_subtracted': -.605,
            'away_base_out_runs_added': 1.2,
            'away_putouts': 25,
            'away_assists': 5,
            'away_innings_pitched': 8.1,
            'away_home_runs': 2,
            'away_strikes_by_contact': 63,
            'away_strikes_swinging': 14,
            'away_strikes_looking': 23,
            'away_grounded_balls': 10,
            'away_fly_balls': 21,
            'away_line_drives': 10,
            'away_unknown_bat_type': 0,
            'away_game_score': 38,
            'away_inherited_runners': 0,
            'away_inherited_score': 0,
            'away_win_probability_by_pitcher': -.791,
            'away_average_leverage_index': 1.75,
            'away_base_out_runs_saved': -2.5,
            'home_at_bats': 35,
            'home_runs': 7,
            'home_hits': 12,
            'home_rbi': 7,
            'home_earned_runs': 7.56,
            'home_bases_on_balls': 2,
            'home_strikeouts': 10,
            'home_plate_appearances': 38,
            'home_batting_average': .343,
            'home_on_base_percentage': .368,
            'home_slugging_percentage': .600,
            'home_on_base_plus': .968,
            'home_pitches': 159,
            'home_strikes': 99,
            'home_win_probability_for_offensive_player': .791,
            'home_average_leverage_index': 1.75,
            'home_win_probability_added': 1.847,
            'home_win_probability_subtracted': -1.058,
            'home_base_out_runs_added': 2.5,
            'home_putouts': 27,
            'home_assists': 8,
            'home_innings_pitched': 9,
            'home_home_runs': 1,
            'home_strikes_by_contact': 50,
            'home_strikes_swinging': 14,
            'home_strikes_looking': 35,
            'home_grounded_balls': 7,
            'home_fly_balls': 19,
            'home_line_drives': 9,
            'home_unknown_bat_type': 0,
            'home_game_score': 42,
            'home_inherited_runners': 5,
            'home_inherited_score': 2,
            'home_win_probability_by_pitcher': -.291,
            'home_average_leverage_index': 1.15,
            'home_base_out_runs_saved': -1.2
        }
        flexmock(utils) \
            .should_receive('_todays_date') \
            .and_return(MockDateTime(YEAR, MONTH))

        self.boxscore = Boxscore(BOXSCORE)

    def test_mlb_boxscore_returns_requested_boxscore(self):
        for attribute, value in self.results.items():
            assert getattr(self.boxscore, attribute) == value
        assert getattr(self.boxscore, 'summary') == {
            'away': [2, 0, 0, 0, 1, 3, 0, 0, 0],
            'home': [0, 0, 2, 0, 3, 0, 0, 0, 2]
        }

    def test_invalid_url_yields_empty_class(self):
        flexmock(Boxscore) \
            .should_receive('_retrieve_html_page') \
            .and_return(None)

        boxscore = Boxscore(BOXSCORE)

        for key, value in boxscore.__dict__.items():
            if key == '_uri':
                continue
            assert value is None

    def test_mlb_boxscore_dataframe_returns_dataframe_of_all_values(self):
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

    def test_mlb_boxscore_player(self):
        boxscore = self.boxscore

        assert len(boxscore.home_players) == 15
        assert len(boxscore.away_players) == 15

        for player in boxscore.home_players:
            assert not player.dataframe.empty
        for player in boxscore.away_players:
            assert not player.dataframe.empty

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_mlb_boxscore_string_representation(self, *args, **kwargs):
        expected = ('Boxscore for San Francisco Giants at '
                    'Los Angeles Angels (Monday, August 17, 2020)')
        boxscore = Boxscore(BOXSCORE)
        assert boxscore.__repr__() == expected


class TestMLBBoxscores:
    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.expected = {
            '8-17-2020': [
                {'away_abbr': 'COL',
                'away_name': 'Colorado Rockies',
                'away_score': 1,
                'boxscore': 'HOU/HOU202008180',
                'home_abbr': 'HOU',
                'home_name': 'Houston Astros',
                'home_score': 2,
                'losing_abbr': 'COL',
                'losing_name': 'Colorado Rockies',
                'winning_abbr': 'HOU',
                'winning_name': 'Houston Astros'},
               {'away_abbr': 'SDP',
                'away_name': 'San Diego Padres',
                'away_score': 6,
                'boxscore': 'TEX/TEX202008180',
                'home_abbr': 'TEX',
                'home_name': 'Texas Rangers',
                'home_score': 4,
                'losing_abbr': 'TEX',
                'losing_name': 'Texas Rangers',
                'winning_abbr': 'SDP',
                'winning_name': 'San Diego Padres'},
               {'away_abbr': 'SFG',
                'away_name': 'San Francisco Giants',
                'away_score': 8,
                'boxscore': 'ANA/ANA202008180',
                'home_abbr': 'LAA',
                'home_name': 'Los Angeles Angels',
                'home_score': 2,
                'losing_abbr': 'LAA',
                'losing_name': 'Los Angeles Angels',
                'winning_abbr': 'SFG',
                'winning_name': 'San Francisco Giants'},
               {'away_abbr': 'OAK',
                'away_name': 'Oakland Athletics',
                'away_score': 1,
                'boxscore': 'ARI/ARI202008180',
                'home_abbr': 'ARI',
                'home_name': 'Arizona Diamondbacks',
                'home_score': 10,
                'losing_abbr': 'OAK',
                'losing_name': 'Oakland Athletics',
                'winning_abbr': 'ARI',
                'winning_name': 'Arizona Diamondbacks'},
               {'away_abbr': 'TBR',
                'away_name': 'Tampa Bay Rays',
                'away_score': 6,
                'boxscore': 'NYA/NYA202008180',
                'home_abbr': 'NYY',
                'home_name': 'New York Yankees',
                'home_score': 3,
                'losing_abbr': 'NYY',
                'losing_name': 'New York Yankees',
                'winning_abbr': 'TBR',
                'winning_name': 'Tampa Bay Rays'},
               {'away_abbr': 'CLE',
                'away_name': 'Cleveland Indians',
                'away_score': 6,
                'boxscore': 'PIT/PIT202008180',
                'home_abbr': 'PIT',
                'home_name': 'Pittsburgh Pirates',
                'home_score': 3,
                'losing_abbr': 'PIT',
                'losing_name': 'Pittsburgh Pirates',
                'winning_abbr': 'CLE',
                'winning_name': 'Cleveland Indians'},
               {'away_abbr': 'WSN',
                'away_name': 'Washington Nationals',
                'away_score': 8,
                'boxscore': 'ATL/ATL202008180',
                'home_abbr': 'ATL',
                'home_name': 'Atlanta Braves',
                'home_score': 5,
                'losing_abbr': 'ATL',
                'losing_name': 'Atlanta Braves',
                'winning_abbr': 'WSN',
                'winning_name': 'Washington Nationals'},
               {'away_abbr': 'SEA',
                'away_name': 'Seattle Mariners',
                'away_score': 1,
                'boxscore': 'LAN/LAN202008180',
                'home_abbr': 'LAD',
                'home_name': 'Los Angeles Dodgers',
                'home_score': 2,
                'losing_abbr': 'SEA',
                'losing_name': 'Seattle Mariners',
                'winning_abbr': 'LAD',
                'winning_name': 'Los Angeles Dodgers'},
               {'away_abbr': 'NYM',
                'away_name': 'New York Mets',
                'away_score': 8,
                'boxscore': 'MIA/MIA202008180',
                'home_abbr': 'MIA',
                'home_name': 'Miami Marlins',
                'home_score': 3,
                'losing_abbr': 'MIA',
                'losing_name': 'Miami Marlins',
                'winning_abbr': 'NYM',
                'winning_name': 'New York Mets'},
               {'away_abbr': 'PHI',
                'away_name': 'Philadelphia Phillies',
                'away_score': 13,
                'boxscore': 'BOS/BOS202008180',
                'home_abbr': 'BOS',
                'home_name': 'Boston Red Sox',
                'home_score': 6,
                'losing_abbr': 'BOS',
                'losing_name': 'Boston Red Sox',
                'winning_abbr': 'PHI',
                'winning_name': 'Philadelphia Phillies'},
               {'away_abbr': 'TOR',
                'away_name': 'Toronto Blue Jays',
                'away_score': 8,
                'boxscore': 'BAL/BAL202008180',
                'home_abbr': 'BAL',
                'home_name': 'Baltimore Orioles',
                'home_score': 7,
                'losing_abbr': 'BAL',
                'losing_name': 'Baltimore Orioles',
                'winning_abbr': 'TOR',
                'winning_name': 'Toronto Blue Jays'},
               {'away_abbr': 'DET',
                'away_name': 'Detroit Tigers',
                'away_score': 4,
                'boxscore': 'CHA/CHA202008180',
                'home_abbr': 'CHW',
                'home_name': 'Chicago White Sox',
                'home_score': 10,
                'losing_abbr': 'DET',
                'losing_name': 'Detroit Tigers',
                'winning_abbr': 'CHW',
                'winning_name': 'Chicago White Sox'},
               {'away_abbr': 'MIL',
                'away_name': 'Milwaukee Brewers',
                'away_score': 3,
                'boxscore': 'MIN/MIN202008180',
                'home_abbr': 'MIN',
                'home_name': 'Minnesota Twins',
                'home_score': 4,
                'losing_abbr': 'MIL',
                'losing_name': 'Milwaukee Brewers',
                'winning_abbr': 'MIN',
                'winning_name': 'Minnesota Twins'},
               {'away_abbr': 'STL',
                'away_name': 'St. Louis Cardinals',
                'away_score': 3,
                'boxscore': 'CHN/CHN202008180',
                'home_abbr': 'CHC',
                'home_name': 'Chicago Cubs',
                'home_score': 6,
                'losing_abbr': 'STL',
                'losing_name': 'St. Louis Cardinals',
                'winning_abbr': 'CHC',
                'winning_name': 'Chicago Cubs'}
            ]
        }

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_boxscores_search(self, *args, **kwargs):
        result = Boxscores(datetime(2020, 8, 17)).games

        assert result == self.expected

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_boxscores_search_invalid_end(self, *args, **kwargs):
        result = Boxscores(datetime(2020, 8, 17), datetime(2020, 8, 16)).games

        assert result == self.expected

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_boxscores_search_multiple_days(self, *args, **kwargs):
        expected = {
            '8-17-2020': [
                {'away_abbr': 'COL',
                'away_name': 'Colorado Rockies',
                'away_score': 1,
                'boxscore': 'HOU/HOU202008180',
                'home_abbr': 'HOU',
                'home_name': 'Houston Astros',
                'home_score': 2,
                'losing_abbr': 'COL',
                'losing_name': 'Colorado Rockies',
                'winning_abbr': 'HOU',
                'winning_name': 'Houston Astros'},
               {'away_abbr': 'SDP',
                'away_name': 'San Diego Padres',
                'away_score': 6,
                'boxscore': 'TEX/TEX202008180',
                'home_abbr': 'TEX',
                'home_name': 'Texas Rangers',
                'home_score': 4,
                'losing_abbr': 'TEX',
                'losing_name': 'Texas Rangers',
                'winning_abbr': 'SDP',
                'winning_name': 'San Diego Padres'},
               {'away_abbr': 'SFG',
                'away_name': 'San Francisco Giants',
                'away_score': 8,
                'boxscore': 'ANA/ANA202008180',
                'home_abbr': 'LAA',
                'home_name': 'Los Angeles Angels',
                'home_score': 2,
                'losing_abbr': 'LAA',
                'losing_name': 'Los Angeles Angels',
                'winning_abbr': 'SFG',
                'winning_name': 'San Francisco Giants'},
               {'away_abbr': 'OAK',
                'away_name': 'Oakland Athletics',
                'away_score': 1,
                'boxscore': 'ARI/ARI202008180',
                'home_abbr': 'ARI',
                'home_name': 'Arizona Diamondbacks',
                'home_score': 10,
                'losing_abbr': 'OAK',
                'losing_name': 'Oakland Athletics',
                'winning_abbr': 'ARI',
                'winning_name': 'Arizona Diamondbacks'},
               {'away_abbr': 'TBR',
                'away_name': 'Tampa Bay Rays',
                'away_score': 6,
                'boxscore': 'NYA/NYA202008180',
                'home_abbr': 'NYY',
                'home_name': 'New York Yankees',
                'home_score': 3,
                'losing_abbr': 'NYY',
                'losing_name': 'New York Yankees',
                'winning_abbr': 'TBR',
                'winning_name': 'Tampa Bay Rays'},
               {'away_abbr': 'CLE',
                'away_name': 'Cleveland Indians',
                'away_score': 6,
                'boxscore': 'PIT/PIT202008180',
                'home_abbr': 'PIT',
                'home_name': 'Pittsburgh Pirates',
                'home_score': 3,
                'losing_abbr': 'PIT',
                'losing_name': 'Pittsburgh Pirates',
                'winning_abbr': 'CLE',
                'winning_name': 'Cleveland Indians'},
               {'away_abbr': 'WSN',
                'away_name': 'Washington Nationals',
                'away_score': 8,
                'boxscore': 'ATL/ATL202008180',
                'home_abbr': 'ATL',
                'home_name': 'Atlanta Braves',
                'home_score': 5,
                'losing_abbr': 'ATL',
                'losing_name': 'Atlanta Braves',
                'winning_abbr': 'WSN',
                'winning_name': 'Washington Nationals'},
               {'away_abbr': 'SEA',
                'away_name': 'Seattle Mariners',
                'away_score': 1,
                'boxscore': 'LAN/LAN202008180',
                'home_abbr': 'LAD',
                'home_name': 'Los Angeles Dodgers',
                'home_score': 2,
                'losing_abbr': 'SEA',
                'losing_name': 'Seattle Mariners',
                'winning_abbr': 'LAD',
                'winning_name': 'Los Angeles Dodgers'},
               {'away_abbr': 'NYM',
                'away_name': 'New York Mets',
                'away_score': 8,
                'boxscore': 'MIA/MIA202008180',
                'home_abbr': 'MIA',
                'home_name': 'Miami Marlins',
                'home_score': 3,
                'losing_abbr': 'MIA',
                'losing_name': 'Miami Marlins',
                'winning_abbr': 'NYM',
                'winning_name': 'New York Mets'},
               {'away_abbr': 'PHI',
                'away_name': 'Philadelphia Phillies',
                'away_score': 13,
                'boxscore': 'BOS/BOS202008180',
                'home_abbr': 'BOS',
                'home_name': 'Boston Red Sox',
                'home_score': 6,
                'losing_abbr': 'BOS',
                'losing_name': 'Boston Red Sox',
                'winning_abbr': 'PHI',
                'winning_name': 'Philadelphia Phillies'},
               {'away_abbr': 'TOR',
                'away_name': 'Toronto Blue Jays',
                'away_score': 8,
                'boxscore': 'BAL/BAL202008180',
                'home_abbr': 'BAL',
                'home_name': 'Baltimore Orioles',
                'home_score': 7,
                'losing_abbr': 'BAL',
                'losing_name': 'Baltimore Orioles',
                'winning_abbr': 'TOR',
                'winning_name': 'Toronto Blue Jays'},
               {'away_abbr': 'DET',
                'away_name': 'Detroit Tigers',
                'away_score': 4,
                'boxscore': 'CHA/CHA202008180',
                'home_abbr': 'CHW',
                'home_name': 'Chicago White Sox',
                'home_score': 10,
                'losing_abbr': 'DET',
                'losing_name': 'Detroit Tigers',
                'winning_abbr': 'CHW',
                'winning_name': 'Chicago White Sox'},
               {'away_abbr': 'MIL',
                'away_name': 'Milwaukee Brewers',
                'away_score': 3,
                'boxscore': 'MIN/MIN202008180',
                'home_abbr': 'MIN',
                'home_name': 'Minnesota Twins',
                'home_score': 4,
                'losing_abbr': 'MIL',
                'losing_name': 'Milwaukee Brewers',
                'winning_abbr': 'MIN',
                'winning_name': 'Minnesota Twins'},
               {'away_abbr': 'STL',
                'away_name': 'St. Louis Cardinals',
                'away_score': 3,
                'boxscore': 'CHN/CHN202008180',
                'home_abbr': 'CHC',
                'home_name': 'Chicago Cubs',
                'home_score': 6,
                'losing_abbr': 'STL',
                'losing_name': 'St. Louis Cardinals',
                'winning_abbr': 'CHC',
                'winning_name': 'Chicago Cubs'}],
            '8-18-2020': [
                {'away_abbr': 'COL',
                'away_name': 'Colorado Rockies',
                'away_score': 1,
                'boxscore': 'HOU/HOU202008180',
                'home_abbr': 'HOU',
                'home_name': 'Houston Astros',
                'home_score': 2,
                'losing_abbr': 'COL',
                'losing_name': 'Colorado Rockies',
                'winning_abbr': 'HOU',
                'winning_name': 'Houston Astros'},
               {'away_abbr': 'SDP',
                'away_name': 'San Diego Padres',
                'away_score': 6,
                'boxscore': 'TEX/TEX202008180',
                'home_abbr': 'TEX',
                'home_name': 'Texas Rangers',
                'home_score': 4,
                'losing_abbr': 'TEX',
                'losing_name': 'Texas Rangers',
                'winning_abbr': 'SDP',
                'winning_name': 'San Diego Padres'},
               {'away_abbr': 'SFG',
                'away_name': 'San Francisco Giants',
                'away_score': 8,
                'boxscore': 'ANA/ANA202008180',
                'home_abbr': 'LAA',
                'home_name': 'Los Angeles Angels',
                'home_score': 2,
                'losing_abbr': 'LAA',
                'losing_name': 'Los Angeles Angels',
                'winning_abbr': 'SFG',
                'winning_name': 'San Francisco Giants'},
               {'away_abbr': 'OAK',
                'away_name': 'Oakland Athletics',
                'away_score': 1,
                'boxscore': 'ARI/ARI202008180',
                'home_abbr': 'ARI',
                'home_name': 'Arizona Diamondbacks',
                'home_score': 10,
                'losing_abbr': 'OAK',
                'losing_name': 'Oakland Athletics',
                'winning_abbr': 'ARI',
                'winning_name': 'Arizona Diamondbacks'},
               {'away_abbr': 'TBR',
                'away_name': 'Tampa Bay Rays',
                'away_score': 6,
                'boxscore': 'NYA/NYA202008180',
                'home_abbr': 'NYY',
                'home_name': 'New York Yankees',
                'home_score': 3,
                'losing_abbr': 'NYY',
                'losing_name': 'New York Yankees',
                'winning_abbr': 'TBR',
                'winning_name': 'Tampa Bay Rays'},
               {'away_abbr': 'CLE',
                'away_name': 'Cleveland Indians',
                'away_score': 6,
                'boxscore': 'PIT/PIT202008180',
                'home_abbr': 'PIT',
                'home_name': 'Pittsburgh Pirates',
                'home_score': 3,
                'losing_abbr': 'PIT',
                'losing_name': 'Pittsburgh Pirates',
                'winning_abbr': 'CLE',
                'winning_name': 'Cleveland Indians'},
               {'away_abbr': 'WSN',
                'away_name': 'Washington Nationals',
                'away_score': 8,
                'boxscore': 'ATL/ATL202008180',
                'home_abbr': 'ATL',
                'home_name': 'Atlanta Braves',
                'home_score': 5,
                'losing_abbr': 'ATL',
                'losing_name': 'Atlanta Braves',
                'winning_abbr': 'WSN',
                'winning_name': 'Washington Nationals'},
               {'away_abbr': 'SEA',
                'away_name': 'Seattle Mariners',
                'away_score': 1,
                'boxscore': 'LAN/LAN202008180',
                'home_abbr': 'LAD',
                'home_name': 'Los Angeles Dodgers',
                'home_score': 2,
                'losing_abbr': 'SEA',
                'losing_name': 'Seattle Mariners',
                'winning_abbr': 'LAD',
                'winning_name': 'Los Angeles Dodgers'},
               {'away_abbr': 'NYM',
                'away_name': 'New York Mets',
                'away_score': 8,
                'boxscore': 'MIA/MIA202008180',
                'home_abbr': 'MIA',
                'home_name': 'Miami Marlins',
                'home_score': 3,
                'losing_abbr': 'MIA',
                'losing_name': 'Miami Marlins',
                'winning_abbr': 'NYM',
                'winning_name': 'New York Mets'},
               {'away_abbr': 'PHI',
                'away_name': 'Philadelphia Phillies',
                'away_score': 13,
                'boxscore': 'BOS/BOS202008180',
                'home_abbr': 'BOS',
                'home_name': 'Boston Red Sox',
                'home_score': 6,
                'losing_abbr': 'BOS',
                'losing_name': 'Boston Red Sox',
                'winning_abbr': 'PHI',
                'winning_name': 'Philadelphia Phillies'},
               {'away_abbr': 'TOR',
                'away_name': 'Toronto Blue Jays',
                'away_score': 8,
                'boxscore': 'BAL/BAL202008180',
                'home_abbr': 'BAL',
                'home_name': 'Baltimore Orioles',
                'home_score': 7,
                'losing_abbr': 'BAL',
                'losing_name': 'Baltimore Orioles',
                'winning_abbr': 'TOR',
                'winning_name': 'Toronto Blue Jays'},
               {'away_abbr': 'DET',
                'away_name': 'Detroit Tigers',
                'away_score': 4,
                'boxscore': 'CHA/CHA202008180',
                'home_abbr': 'CHW',
                'home_name': 'Chicago White Sox',
                'home_score': 10,
                'losing_abbr': 'DET',
                'losing_name': 'Detroit Tigers',
                'winning_abbr': 'CHW',
                'winning_name': 'Chicago White Sox'},
               {'away_abbr': 'MIL',
                'away_name': 'Milwaukee Brewers',
                'away_score': 3,
                'boxscore': 'MIN/MIN202008180',
                'home_abbr': 'MIN',
                'home_name': 'Minnesota Twins',
                'home_score': 4,
                'losing_abbr': 'MIL',
                'losing_name': 'Milwaukee Brewers',
                'winning_abbr': 'MIN',
                'winning_name': 'Minnesota Twins'},
               {'away_abbr': 'STL',
                'away_name': 'St. Louis Cardinals',
                'away_score': 3,
                'boxscore': 'CHN/CHN202008180',
                'home_abbr': 'CHC',
                'home_name': 'Chicago Cubs',
                'home_score': 6,
                'losing_abbr': 'STL',
                'losing_name': 'St. Louis Cardinals',
                'winning_abbr': 'CHC',
                'winning_name': 'Chicago Cubs'}
            ]
        }
        result = Boxscores(datetime(2020, 8, 17), datetime(2020, 8, 18)).games

        assert result == expected

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_boxscores_search_string_representation(self, *args, **kwargs):
        result = Boxscores(datetime(2020, 8, 17))

        assert result.__repr__() == 'MLB games for 8-17-2020'
