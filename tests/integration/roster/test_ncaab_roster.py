import mock
import os
import pandas as pd
import pytest
from datetime import datetime
from flexmock import flexmock
from sportsipy import utils
from sportsipy.ncaab.roster import Player, Roster
from sportsipy.ncaab.teams import Team
from ..utils import read_file


YEAR = 2022


def mock_pyquery(url):
    if 'purdue' in url:
        return read_file('2022.html', 'ncaab', 'roster')
    if 'jaden-ivey-1' in url:
        return read_file('jaden-ivey-1.html', 'ncaab', 'roster')
    if 'zach-edey-1' in url:
        return read_file('zach-edey-1.html', 'ncaab', 'roster')
    if 'bad' in url:
        return None
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


class TestNCAABPlayer:
    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results_career = {
            'assist_percentage': 18.2,
            'assists': 153,
            'block_percentage': 2.6,
            'blocks': 36,
            'box_plus_minus': 7.1,
            'conference': '',
            'defensive_box_plus_minus': 1.8,
            'defensive_rebound_percentage': 14.0,
            'defensive_rebounds': 209,
            'defensive_win_shares': 2.2,
            'effective_field_goal_percentage': 0.507,
            'field_goal_attempts': 664,
            'field_goal_percentage': 0.44,
            'field_goals': 292,
            'free_throw_attempt_rate': 0.422,
            'free_throw_attempts': 280,
            'free_throw_percentage': 0.739,
            'free_throws': 207,
            'games_played': 59,
            'games_started': 46,
            'height': 'Jaden Ivey',
            'minutes_played': 1689,
            'offensive_box_plus_minus': 5.3,
            'offensive_rebound_percentage': 3.1,
            'offensive_rebounds': 43,
            'offensive_win_shares': 4.8,
            'personal_fouls': 102,
            'player_efficiency_rating': 21.1,
            'player_id': 'jaden-ivey-1',
            'points': 880,
            'points_produced': 830,
            'position': 'Guard',
            'steal_percentage': 1.8,
            'steals': 50,
            'team_abbreviation': 'purdue',
            'three_point_attempt_rate': 0.416,
            'three_point_attempts': 276,
            'three_point_percentage': 0.322,
            'three_pointers': 89,
            'total_rebound_percentage': 8.8,
            'total_rebounds': 252,
            'true_shooting_percentage': 0.552,
            'turnover_percentage': 13.6,
            'turnovers': 125,
            'two_point_attempts': 388,
            'two_point_percentage': 0.523,
            'two_pointers': 203,
            'usage_percentage': 28.1,
            'weight': 200,
            'win_shares': 7.0,
            'win_shares_per_40_minutes': 0.166
        }

        self.results_year = {
            'assist_percentage': 19.2,
            'assists': 110,
            'block_percentage': 2.0,
            'blocks': 20,
            'box_plus_minus': 7.2,
            'conference': 'big-ten',
            'defensive_box_plus_minus': 1.6,
            'defensive_rebound_percentage': 15.0,
            'defensive_rebounds': 152,
            'defensive_win_shares': 1.4,
            'effective_field_goal_percentage': 0.533,
            'field_goal_attempts': 441,
            'field_goal_percentage': 0.46,
            'field_goals': 203,
            'free_throw_attempt_rate': 0.469,
            'free_throw_attempts': 207,
            'free_throw_percentage': 0.744,
            'free_throws': 154,
            'games_played': 36,
            'games_started': 34,
            'height': 'Jaden Ivey',
            'minutes_played': 1132,
            'offensive_box_plus_minus': 5.7,
            'offensive_rebound_percentage': 2.7,
            'offensive_rebounds': 24,
            'offensive_win_shares': 3.7,
            'personal_fouls': 63,
            'player_efficiency_rating': 22.5,
            'player_id': 'jaden-ivey-1',
            'points': 624,
            'points_produced': 586,
            'position': 'Guard',
            'steal_percentage': 1.7,
            'steals': 33,
            'team_abbreviation': 'purdue',
            'three_point_attempt_rate': 0.406,
            'three_point_attempts': 179,
            'three_point_percentage': 0.358,
            'three_pointers': 64,
            'total_rebound_percentage': 9.3,
            'total_rebounds': 176,
            'true_shooting_percentage': 0.579,
            'turnover_percentage': 14.8,
            'turnovers': 94,
            'two_point_attempts': 262,
            'two_point_percentage': 0.531,
            'two_pointers': 139,
            'usage_percentage': 28.7,
            'weight': 200,
            'win_shares': 5.1,
            'win_shares_per_40_minutes': 0.181
        }

        self.player = Player('jaden-ivey-1')

    def test_ncaab_player_returns_requested_player_career_stats(self):
        # Request the career stats
        player = self.player('')

        for attribute, value in self.results_career.items():
            assert getattr(player, attribute) == value

    def test_ncaab_player_returns_requested_player_season_stats(self):
        # Request the 2021-22 stats
        player = self.player('2021-22')

        for attribute, value in self.results_year.items():
            assert getattr(player, attribute) == value

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_correct_initial_index_found(self, *args):
        seasons = ['2020-21', '2021-22', 'Career']
        mock_season = mock.PropertyMock(return_value=seasons)
        player = Player('jaden-ivey-1')
        type(player)._season = mock_season

        result = player._find_initial_index()

        assert player._index == 2

    def test_dataframe_returns_dataframe(self):
        dataframe = [
            {'assist_percentage': 16.4,
            'assists': 43,
            'block_percentage': 3.8,
            'blocks': 16,
            'box_plus_minus': 6.7,
            'conference': 'big-ten',
            'defensive_box_plus_minus': 2.3,
            'defensive_rebound_percentage': 11.8,
            'defensive_rebounds': 57,
            'defensive_win_shares': 0.8,
            'effective_field_goal_percentage': 0.455,
            'field_goal_attempts': 223,
            'field_goal_percentage': 0.399,
            'field_goals': 89,
            'free_throw_attempt_rate': 0.327,
            'free_throw_attempts': 73,
            'free_throw_percentage': 0.726,
            'free_throws': 53,
            'games_played': 23,
            'games_started': 12,
            'height': 'Jaden Ivey',
            'minutes_played': 557,
            'offensive_box_plus_minus': 4.4,
            'offensive_rebound_percentage': 4.0,
            'offensive_rebounds': 19,
            'offensive_win_shares': 1.1,
            'personal_fouls': 39,
            'player_efficiency_rating': 18.3,
            'player_id': 'jaden-ivey-1',
            'points': 256,
            'points_produced': 243,
            'position': 'Guard',
            'steal_percentage': 1.8,
            'steals': 17,
            'team_abbreviation': 'purdue',
            'three_point_attempt_rate': 0.435,
            'three_point_attempts': 97,
            'three_point_percentage': 0.258,
            'three_pointers': 25,
            'total_rebound_percentage': 8.0,
            'total_rebounds': 76,
            'true_shooting_percentage': 0.497,
            'turnover_percentage': 10.7,
            'turnovers': 31,
            'two_point_attempts': 126,
            'two_point_percentage': 0.508,
            'two_pointers': 64,
            'usage_percentage': 26.8,
            'weight': 200,
            'win_shares': 1.9,
            'win_shares_per_40_minutes': 0.136},
            {'assist_percentage': 19.2,
            'assists': 110,
            'block_percentage': 2.0,
            'blocks': 20,
            'box_plus_minus': 7.2,
            'conference': 'big-ten',
            'defensive_box_plus_minus': 1.6,
            'defensive_rebound_percentage': 15.0,
            'defensive_rebounds': 152,
            'defensive_win_shares': 1.4,
            'effective_field_goal_percentage': 0.533,
            'field_goal_attempts': 441,
            'field_goal_percentage': 0.46,
            'field_goals': 203,
            'free_throw_attempt_rate': 0.469,
            'free_throw_attempts': 207,
            'free_throw_percentage': 0.744,
            'free_throws': 154,
            'games_played': 36,
            'games_started': 34,
            'height': 'Jaden Ivey',
            'minutes_played': 1132,
            'offensive_box_plus_minus': 5.7,
            'offensive_rebound_percentage': 2.7,
            'offensive_rebounds': 24,
            'offensive_win_shares': 3.7,
            'personal_fouls': 63,
            'player_efficiency_rating': 22.5,
            'player_id': 'jaden-ivey-1',
            'points': 624,
            'points_produced': 586,
            'position': 'Guard',
            'steal_percentage': 1.7,
            'steals': 33,
            'team_abbreviation': 'purdue',
            'three_point_attempt_rate': 0.406,
            'three_point_attempts': 179,
            'three_point_percentage': 0.358,
            'three_pointers': 64,
            'total_rebound_percentage': 9.3,
            'total_rebounds': 176,
            'true_shooting_percentage': 0.579,
            'turnover_percentage': 14.8,
            'turnovers': 94,
            'two_point_attempts': 262,
            'two_point_percentage': 0.531,
            'two_pointers': 139,
            'usage_percentage': 28.7,
            'weight': 200,
            'win_shares': 5.1,
            'win_shares_per_40_minutes': 0.181},
            {'assist_percentage': 18.2,
            'assists': 153,
            'block_percentage': 2.6,
            'blocks': 36,
            'box_plus_minus': 7.1,
            'conference': '',
            'defensive_box_plus_minus': 1.8,
            'defensive_rebound_percentage': 14.0,
            'defensive_rebounds': 209,
            'defensive_win_shares': 2.2,
            'effective_field_goal_percentage': 0.507,
            'field_goal_attempts': 664,
            'field_goal_percentage': 0.44,
            'field_goals': 292,
            'free_throw_attempt_rate': 0.422,
            'free_throw_attempts': 280,
            'free_throw_percentage': 0.739,
            'free_throws': 207,
            'games_played': 59,
            'games_started': 46,
            'height': 'Jaden Ivey',
            'minutes_played': 1689,
            'offensive_box_plus_minus': 5.3,
            'offensive_rebound_percentage': 3.1,
            'offensive_rebounds': 43,
            'offensive_win_shares': 4.8,
            'personal_fouls': 102,
            'player_efficiency_rating': 21.1,
            'player_id': 'jaden-ivey-1',
            'points': 880,
            'points_produced': 830,
            'position': 'Guard',
            'steal_percentage': 1.8,
            'steals': 50,
            'team_abbreviation': 'purdue',
            'three_point_attempt_rate': 0.416,
            'three_point_attempts': 276,
            'three_point_percentage': 0.322,
            'three_pointers': 89,
            'total_rebound_percentage': 8.8,
            'total_rebounds': 252,
            'true_shooting_percentage': 0.552,
            'turnover_percentage': 13.6,
            'turnovers': 125,
            'two_point_attempts': 388,
            'two_point_percentage': 0.523,
            'two_pointers': 203,
            'usage_percentage': 28.1,
            'weight': 200,
            'win_shares': 7.0,
            'win_shares_per_40_minutes': 0.166}
        ]
        indices = ['2020-21', '2021-22', 'Career']

        df = pd.DataFrame(dataframe, index=indices)
        player = self.player('')

        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected one above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, player.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

    def test_ncaab_player_string_representation(self):
        # Request the career stats
        player = self.player('')

        assert player.__repr__() == 'Jaden Ivey (jaden-ivey-1)'


class TestNCAABRoster:
    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_roster_class_pulls_all_player_stats(self, *args, **kwargs):
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return(YEAR)
        roster = Roster('PURDUE')

        assert len(roster.players) == 14

        roster_players = [player.name for player in roster.players]
        for player in ['Jaden Ivey', 'Zach Edey']:
            assert player in roster_players

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_bad_url_raises_value_error(self, *args, **kwargs):
        with pytest.raises(ValueError):
            roster = Roster('BAD')

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_roster_from_team_class(self, *args, **kwargs):
        flexmock(Team) \
            .should_receive('_parse_team_data') \
            .and_return(None)
        team = Team(None, 1, YEAR)
        mock_abbreviation = mock.PropertyMock(return_value='PURDUE')
        type(team)._abbreviation = mock_abbreviation

        assert len(team.roster.players) == 14

        roster_players = [player.name for player in team.roster.players]
        for player in ['Jaden Ivey', 'Zach Edey']:
            assert player in roster_players
        type(team)._abbreviation = None

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_roster_class_with_slim_parameter(self, *args, **kwargs):
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return(YEAR)
        roster = Roster('PURDUE', slim=True)

        assert len(roster.players) == 14
        assert roster.players == {
                'jaden-ivey-1': 'Jaden Ivey',
                'zach-edey-1': 'Zach Edey',
                'trevion-williams-1': 'Trevion Williams',
                'sasha-stefanovic-1': 'Sasha Stefanovic',
                'eric-hunterjr-1': 'Eric Hunter',
                'mason-gillis-1': 'Mason Gillis',
                'isaiah-thompson-1': 'Isaiah Thompson',
                'caleb-furst-1': 'Caleb Furst',
                'brandon-newman-2': 'Brandon Newman',
                'ethan-morton-1': 'Ethan Morton',
                'carson-barrett-1': 'Carson Barrett',
                'matt-frost-1': 'Matt Frost',
                'chase-martin-1': 'Chase Martin',
                'jared-wulbrun-1': 'Jared Wulbrun'
            }

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_roster_class_string_representation(self, *args, **kwargs):
        expected = """Jaden Ivey (jaden-ivey-1)
Zach Edey (zach-edey-1)
None (trevion-williams-1)
None (sasha-stefanovic-1)
None (eric-hunterjr-1)
None (mason-gillis-1)
None (isaiah-thompson-1)
None (caleb-furst-1)
None (brandon-newman-2)
None (ethan-morton-1)
None (carson-barrett-1)
None (matt-frost-1)
None (chase-martin-1)
None (jared-wulbrun-1)"""

        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return(YEAR)
        roster = Roster('PURDUE')

        assert roster.__repr__() == expected

    @mock.patch('sportsipy.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_coach(self, *args, **kwargs):
        assert "Matt Painter" == Roster('PURDUE', year=YEAR).coach
