import mock
import os
import pandas as pd
import pytest
from flexmock import flexmock
from sports import utils
from sports.ncaaf.roster import Player, Roster
from sports.ncaaf.teams import Team
from ..utils import read_file


YEAR = '2021'
TEAM = 'PURDUE'


def mock_pyquery(url):
    if 'BAD' in url or 'bad' in url:
        return None
    if 'aidan-oconnell' in url:
        return read_file('aidan-oconnell-1.html', 'ncaaf', 'roster')
    if 'david-bell' in url:
        return read_file('david-bell-6.html', 'ncaaf', 'roster')
    if 'jaylan-alexander' in url:
        return read_file('jaylan-alexander-1.html', 'ncaaf', 'roster')
    if 'mitchell-fineran-1' in url:
        return read_file('mitchell-fineran-1.html', 'ncaaf', 'roster')
    if '2021-roster' in url:
        return read_file('2021-roster.html', 'ncaaf', 'roster')
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


class TestNCAAFPlayer:
    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.results_career = {
            'adjusted_yards_per_attempt': 7.4,
            'assists_on_tackles': 0,
            'completed_passes': 776,
            'extra_points_attempted': None,
            'extra_points_made': 0,
            'extra_point_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': 0,
            'field_goal_percentage': None,
            'fumbles_forced': 0,
            'fumbles_recovered': 0,
            'fumbles_recovered_for_touchdown': 0.0,
            'games': None,
            'height': '6-3',
            'interceptions': 0,
            'interceptions_returned_for_touchdown': 0,
            'interceptions_thrown': 28,
            'kickoff_return_touchdowns': 0,
            'name': "Aidan O'Connell",
            'other_touchdowns': 0.0,
            'pass_attempts': 1163,
            'passes_defended': 0,
            'passing_completion': 66.7,
            'passing_touchdowns': 63,
            'passing_yards': 8563,
            'passing_yards_per_attempt': 7.4,
            'player_id': 'aidan-oconnell-1',
            'plays_from_scrimmage': 84,
            'points': 12,
            'position': 'QB',
            'punt_return_touchdowns': 0,
            'quarterback_rating': 141.6,
            'receiving_touchdowns': 0,
            'receiving_yards': 0,
            'receiving_yards_per_reception': None,
            'receptions': 0,
            'rush_attempts': 84,
            'rush_touchdowns': 2,
            'rush_yards': -232,
            'rush_yards_per_attempt': -2.8,
            'rushing_and_receiving_touchdowns': 2,
            'sacks': 0.0,
            'safeties': 0.0,
            'season': 'Career',
            'solo_tackles': 1,
            'tackles_for_loss': 0.0,
            'team_abbreviation': 'Purdue',
            'total_tackles': 1,
            'total_touchdowns': 2.0,
            'two_point_conversions': 0.0,
            'weight': 200,
            'yards_from_scrimmage': -232,
            'yards_from_scrimmage_per_play': -2.8,
            'yards_recovered_from_fumble': 0.0,
            'yards_returned_from_interceptions': 0,
            'yards_returned_per_interception': None,
            'year': ''
        }
        

        self.results_year = {
            'adjusted_yards_per_attempt': 8.6,
            'assists_on_tackles': 0,
            'completed_passes': 315,
            'extra_points_attempted': None,
            'extra_points_made': 0,
            'extra_point_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': 0,
            'field_goal_percentage': None,
            'fumbles_forced': 0,
            'fumbles_recovered': 0,
            'fumbles_recovered_for_touchdown': None,
            'games': 12.0,
            'height': '6-3',
            'interceptions': 0,
            'interceptions_returned_for_touchdown': 0,
            'interceptions_thrown': 11,
            'kickoff_return_touchdowns': 0,
            'name': "Aidan O'Connell",
            'other_touchdowns': None,
            'pass_attempts': 440,
            'passes_defended': 0,
            'passing_completion': 71.6,
            'passing_touchdowns': 28,
            'passing_yards': 3712,
            'passing_yards_per_attempt': 8.4,
            'player_id': 'aidan-oconnell-1',
            'plays_from_scrimmage': 25,
            'points': 6,
            'position': 'QB',
            'punt_return_touchdowns': 0,
            'quarterback_rating': 158.5,
            'receiving_touchdowns': 0,
            'receiving_yards': 0,
            'receiving_yards_per_reception': None,
            'receptions': 0,
            'rush_attempts': 25,
            'rush_touchdowns': 1,
            'rush_yards': -120,
            'rush_yards_per_attempt': -4.8,
            'rushing_and_receiving_touchdowns': 1,
            'sacks': 0.0,
            'safeties': None,
            'season': '2021',
            'solo_tackles': 1,
            'tackles_for_loss': 0.0,
            'team_abbreviation': 'Purdue',
            'total_tackles': 1,
            'total_touchdowns': 1.0,
            'two_point_conversions': None,
            'weight': 200,
            'yards_from_scrimmage': -120,
            'yards_from_scrimmage_per_play': -4.8,
            'yards_recovered_from_fumble': None,
            'yards_returned_from_interceptions': 0,
            'yards_returned_per_interception': None,
            'year': 'SR'
        }
        self.player = Player('aidan-oconnell-1')

    def test_ncaaf_player_returns_requested_career_stats(self):
        # Request the career stats
        player = self.player('')

        for attribute, value in self.results_career.items():
            assert getattr(player, attribute) == value

    def test_ncaaf_player_returns_requested_season_stats(self):
        # Request the 2017 stats
        player = self.player(YEAR)

        for attribute, value in self.results_year.items():
            assert getattr(player, attribute) == value

    def test_dataframe_returns_dataframe(self):
        dataframe = [
            {'adjusted_yards_per_attempt': 6.6,
            'assists_on_tackles': 0,
            'completed_passes': 103,
            'extra_points_attempted': None,
            'extra_points_made': 0,
            'extra_point_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': 0,
            'field_goal_percentage': None,
            'fumbles_forced': 0,
            'fumbles_recovered': 0,
            'fumbles_recovered_for_touchdown': None,
            'games': 6.0,
            'height': '6-3',
            'interceptions': 0,
            'interceptions_returned_for_touchdown': 0,
            'interceptions_thrown': 4,
            'kickoff_return_touchdowns': 0,
            'name': "Aidan O'Connell",
            'other_touchdowns': None,
            'pass_attempts': 164,
            'passes_defended': 0,
            'passing_completion': 62.8,
            'passing_touchdowns': 8,
            'passing_yards': 1101,
            'passing_yards_per_attempt': 6.7,
            'player_id': 'aidan-oconnell-1',
            'plays_from_scrimmage': 15,
            'points': 0,
            'position': 'QB',
            'punt_return_touchdowns': 0,
            'quarterback_rating': 130.4,
            'receiving_touchdowns': 0,
            'receiving_yards': 0,
            'receiving_yards_per_reception': None,
            'receptions': 0,
            'rush_attempts': 15,
            'rush_touchdowns': 0,
            'rush_yards': -9,
            'rush_yards_per_attempt': -0.6,
            'rushing_and_receiving_touchdowns': 0,
            'sacks': 0.0,
            'safeties': None,
            'season': '2019',
            'solo_tackles': 0,
            'tackles_for_loss': 0.0,
            'team_abbreviation': 'Purdue',
            'total_tackles': 0,
            'total_touchdowns': 0.0,
            'two_point_conversions': None,
            'weight': 200,
            'yards_from_scrimmage': -9,
            'yards_from_scrimmage_per_play': -0.6,
            'yards_recovered_from_fumble': None,
            'yards_returned_from_interceptions': 0,
            'yards_returned_per_interception': None,
            'year': 'SO'},
            {'adjusted_yards_per_attempt': 7.1,
            'assists_on_tackles': 0,
            'completed_passes': 88,
            'extra_points_attempted': None,
            'extra_points_made': 0,
            'extra_point_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': 0,
            'field_goal_percentage': None,
            'fumbles_forced': 0,
            'fumbles_recovered': 0,
            'fumbles_recovered_for_touchdown': None,
            'games': 3.0,
            'height': '6-3',
            'interceptions': 0,
            'interceptions_returned_for_touchdown': 0,
            'interceptions_thrown': 2,
            'kickoff_return_touchdowns': 0,
            'name': "Aidan O'Connell",
            'other_touchdowns': None,
            'pass_attempts': 136,
            'passes_defended': 0,
            'passing_completion': 64.7,
            'passing_touchdowns': 7,
            'passing_yards': 916,
            'passing_yards_per_attempt': 6.7,
            'player_id': 'aidan-oconnell-1',
            'plays_from_scrimmage': 12,
            'points': 0,
            'position': 'QB',
            'punt_return_touchdowns': 0,
            'quarterback_rating': 135.3,
            'receiving_touchdowns': 0,
            'receiving_yards': 0,
            'receiving_yards_per_reception': None,
            'receptions': 0,
            'rush_attempts': 12,
            'rush_touchdowns': 0,
            'rush_yards': -64,
            'rush_yards_per_attempt': -5.3,
            'rushing_and_receiving_touchdowns': 0,
            'sacks': 0.0,
            'safeties': None,
            'season': '2020',
            'solo_tackles': 0,
            'tackles_for_loss': 0.0,
            'team_abbreviation': 'Purdue',
            'total_tackles': 0,
            'total_touchdowns': None,
            'two_point_conversions': None,
            'weight': 200,
            'yards_from_scrimmage': -64,
            'yards_from_scrimmage_per_play': -5.3,
            'yards_recovered_from_fumble': None,
            'yards_returned_from_interceptions': 0,
            'yards_returned_per_interception': None,
            'year': 'JR'},
            {'adjusted_yards_per_attempt': 8.6,
            'assists_on_tackles': 0,
            'completed_passes': 315,
            'extra_points_attempted': None,
            'extra_points_made': 0,
            'extra_point_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': 0,
            'field_goal_percentage': None,
            'fumbles_forced': 0,
            'fumbles_recovered': 0,
            'fumbles_recovered_for_touchdown': None,
            'games': 12.0,
            'height': '6-3',
            'interceptions': 0,
            'interceptions_returned_for_touchdown': 0,
            'interceptions_thrown': 11,
            'kickoff_return_touchdowns': 0,
            'name': "Aidan O'Connell",
            'other_touchdowns': None,
            'pass_attempts': 440,
            'passes_defended': 0,
            'passing_completion': 71.6,
            'passing_touchdowns': 28,
            'passing_yards': 3712,
            'passing_yards_per_attempt': 8.4,
            'player_id': 'aidan-oconnell-1',
            'plays_from_scrimmage': 25,
            'points': 6,
            'position': 'QB',
            'punt_return_touchdowns': 0,
            'quarterback_rating': 158.5,
            'receiving_touchdowns': 0,
            'receiving_yards': 0,
            'receiving_yards_per_reception': None,
            'receptions': 0,
            'rush_attempts': 25,
            'rush_touchdowns': 1,
            'rush_yards': -120,
            'rush_yards_per_attempt': -4.8,
            'rushing_and_receiving_touchdowns': 1,
            'sacks': 0.0,
            'safeties': None,
            'season': '2021',
            'solo_tackles': 1,
            'tackles_for_loss': 0.0,
            'team_abbreviation': 'Purdue',
            'total_tackles': 1,
            'total_touchdowns': 1.0,
            'two_point_conversions': None,
            'weight': 200,
            'yards_from_scrimmage': -120,
            'yards_from_scrimmage_per_play': -4.8,
            'yards_recovered_from_fumble': None,
            'yards_returned_from_interceptions': 0,
            'yards_returned_per_interception': None,
            'year': 'SR'},
            {'adjusted_yards_per_attempt': 6.5,
            'assists_on_tackles': 0,
            'completed_passes': 270,
            'extra_points_attempted': None,
            'extra_points_made': 0,
            'extra_point_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': 0,
            'field_goal_percentage': None,
            'fumbles_forced': 0,
            'fumbles_recovered': 0,
            'fumbles_recovered_for_touchdown': 0.0,
            'games': 10.0,
            'height': '6-3',
            'interceptions': 0,
            'interceptions_returned_for_touchdown': 0,
            'interceptions_thrown': 11,
            'kickoff_return_touchdowns': 0,
            'name': "Aidan O'Connell",
            'other_touchdowns': 0.0,
            'pass_attempts': 423,
            'passes_defended': 0,
            'passing_completion': 63.8,
            'passing_touchdowns': 20,
            'passing_yards': 2834,
            'passing_yards_per_attempt': 6.7,
            'player_id': 'aidan-oconnell-1',
            'plays_from_scrimmage': 32,
            'points': 6,
            'position': 'QB',
            'punt_return_touchdowns': 0,
            'quarterback_rating': 130.5,
            'receiving_touchdowns': 0,
            'receiving_yards': 0,
            'receiving_yards_per_reception': None,
            'receptions': 0,
            'rush_attempts': 32,
            'rush_touchdowns': 1,
            'rush_yards': -39,
            'rush_yards_per_attempt': -1.2,
            'rushing_and_receiving_touchdowns': 1,
            'sacks': 0.0,
            'safeties': 0.0,
            'season': '2022',
            'solo_tackles': 0,
            'tackles_for_loss': 0.0,
            'team_abbreviation': 'Purdue',
            'total_tackles': 0,
            'total_touchdowns': 1.0,
            'two_point_conversions': 0.0,
            'weight': 200,
            'yards_from_scrimmage': -39,
            'yards_from_scrimmage_per_play': -1.2,
            'yards_recovered_from_fumble': 0.0,
            'yards_returned_from_interceptions': 0,
            'yards_returned_per_interception': None,
            'year': 'SR'},
            {'adjusted_yards_per_attempt': 7.4,
            'assists_on_tackles': 0,
            'completed_passes': 776,
            'extra_points_attempted': None,
            'extra_points_made': 0,
            'extra_point_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': 0,
            'field_goal_percentage': None,
            'fumbles_forced': 0,
            'fumbles_recovered': 0,
            'fumbles_recovered_for_touchdown': 0.0,
            'games': None,
            'height': '6-3',
            'interceptions': 0,
            'interceptions_returned_for_touchdown': 0,
            'interceptions_thrown': 28,
            'kickoff_return_touchdowns': 0,
            'name': "Aidan O'Connell",
            'other_touchdowns': 0.0,
            'pass_attempts': 1163,
            'passes_defended': 0,
            'passing_completion': 66.7,
            'passing_touchdowns': 63,
            'passing_yards': 8563,
            'passing_yards_per_attempt': 7.4,
            'player_id': 'aidan-oconnell-1',
            'plays_from_scrimmage': 84,
            'points': 12,
            'position': 'QB',
            'punt_return_touchdowns': 0,
            'quarterback_rating': 141.6,
            'receiving_touchdowns': 0,
            'receiving_yards': 0,
            'receiving_yards_per_reception': None,
            'receptions': 0,
            'rush_attempts': 84,
            'rush_touchdowns': 2,
            'rush_yards': -232,
            'rush_yards_per_attempt': -2.8,
            'rushing_and_receiving_touchdowns': 2,
            'sacks': 0.0,
            'safeties': 0.0,
            'season': 'Career',
            'solo_tackles': 1,
            'tackles_for_loss': 0.0,
            'team_abbreviation': 'Purdue',
            'total_tackles': 1,
            'total_touchdowns': 2.0,
            'two_point_conversions': 0.0,
            'weight': 200,
            'yards_from_scrimmage': -232,
            'yards_from_scrimmage_per_play': -2.8,
            'yards_recovered_from_fumble': 0.0,
            'yards_returned_from_interceptions': 0,
            'yards_returned_per_interception': None,
            'year': ''}
        ]
        indices = ['2019', '2020', '2021', '2022', 'Career']

        df = pd.DataFrame(dataframe, index=indices)
        player = self.player('')

        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected on above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, player.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_ncaaf_offensive_skills_skips_passing_without_errors(self, *args,
                                                          **kwargs):
        player = Player('david-bell-6')

        assert player.name == 'David Bell'
        assert player.dataframe is not None

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_ncaaf_kicker_returns_expected_kicking_stats(self, *args,
                                                         **kwargs):
        stats = {
            'extra_points_attempted': 80,
            'extra_points_made': 76,
            'extra_point_percentage': 95.0,
            'field_goals_attempted': 47,
            'field_goals_made': 36,
            'field_goal_percentage': 76.6,
        }

        player = Player('mitchell-fineran-1')

        assert player.name == 'Mitchell Fineran'
        for attribute, value in stats.items():
            assert getattr(player, attribute) == value

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_ncaaf_404_returns_none_with_no_errors(self, *args, **kwargs):
        player = Player('bad')

        assert player.name is None
        assert player.dataframe is None

    def test_ncaaf_player_string_representation(self):
        # Request the career stats
        player = self.player('')

        assert player.__repr__() == "Aidan O'Connell (aidan-oconnell-1)"


class TestNCAAFRoster:
    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def setup_method(self, *args, **kwargs):
        self.roster = Roster(TEAM, year=YEAR)
        self.len_roster = 116

    def test_roster_class_pulls_all_player_stats(self):
        roster = self.roster

        assert len(roster.players) == self.len_roster

        roster_players = [player.name for player in roster.players]
        for player in ["Aidan O'Connell", 'David Bell', 'Jaylan Alexander', 
                                'Mitchell Fineran']:
            assert player in roster_players

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_bad_url_raises_value_error(self, *args, **kwargs):
        with pytest.raises(ValueError):
            roster = Roster('BAD')

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_roster_from_team_class(self, *args, **kwargs):
        flexmock(Team) \
            .should_receive('_parse_team_data') \
            .and_return(None)
        team = Team(team_data=None, team_conference='big-ten', year=YEAR)
        mock_abbreviation = mock.PropertyMock(return_value=TEAM)
        type(team)._abbreviation = mock_abbreviation

        assert len(team.roster.players) == self.len_roster

        roster_players = [player.name for player in team.roster.players]
        for player in ["Aidan O'Connell", 'David Bell', 'Jaylan Alexander', 
                                'Mitchell Fineran']:
            assert player in roster_players
        type(team)._abbreviation = None

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_roster_class_with_slim_parameter(self, *args, **kwargs):
        roster = Roster(TEAM, year=YEAR, slim=True)

        assert len(roster.players) == self.len_roster

        assert roster.players == {
            'aaron-roberts-3': 'Aaron Roberts',
            'abdur-rahmaan-yaseen-1': 'Abdur-Rahmaan Yaseen',
            'aidan-oconnell-1': "Aidan O'Connell",
            'alex-maxwell-1': 'Alex Maxwell',
            'alexander-horvath-1': 'Alexander Horvath',
            'andrew-hobson-1': 'Andrew Hobson',
            'andrew-sowinski-1': 'Andrew Sowinski',
            'anthony-romphf-1': 'Anthony Romphf',
            'antonio-stevens-1': 'Antonio Stevens',
            'austin-burton-1': 'Austin Burton',
            'ben-buechel-1': 'Ben Buechel',
            'ben-freehill-1': 'Ben Freehill',
            'ben-furtney-1': 'Ben Furtney',
            'ben-kreul-1': 'Ben Kreul',
            'ben-kuhns-1': 'Ben Kuhns',
            'ben-van-noord-1': 'Ben Van Noord',
            'brandon-calloway-1': 'Brandon Calloway',
            'branson-deen-1': 'Branson Deen',
            'brendan-cropsey-1': 'Brendan Cropsey',
            'broc-thompson-1': 'Broc Thompson',
            'bryce-austin-1': 'Bryce Austin',
            'byron-hubbard-1': 'Byron Hubbard',
            'caleb-krockover-1': 'Caleb Krockover',
            'caleb-lahey-1': 'Caleb Lahey',
            'cam-allen-1': 'Cam Allen',
            'cam-craig-1': 'Cam Craig',
            'camdyn-childers-1': 'Camdyn Childers',
            'chris-jefferson-1': 'Chris Jefferson',
            'chris-van-eekeren-1': 'Chris Van Eekeren',
            'christian-gelov-1': 'Christian Gelov',
            'clyde-washington-2': 'Clyde Washington',
            'collin-sullivan-1': 'Collin Sullivan',
            'cory-trice-1': 'Cory Trice',
            'damarcus-mitchell-1': 'Damarcus Mitchell',
            'damarjhe-lewis-1': 'Damarjhe Lewis',
            'dave-monnot-iii-1': 'Dave Monnot III',
            'david-bell-6': 'David Bell',
            'dedrick-mackey-1': 'Dedrick Mackey',
            'deion-burks-1': 'Deion Burks',
            'devin-mockobee-1': 'Devin Mockobee',
            'dj-washington-1': 'D.J. Washington',
            'dontay-hunter-ii-1': 'Dontay Hunter II',
            'drew-biber-1': 'Drew Biber',
            'dylan-downing-2': 'Dylan Downing',
            'edward-dellinger-1': 'Edward Dellinger',
            'elijah-ball-2': 'Elijah Ball',
            'eric-miller-6': 'Eric Miller',
            'garrett-miller-2': 'Garrett Miller',
            'george-karlaftis-1': 'George Karlaftis',
            'greg-hudgins-iii-1': 'Greg Hudgins III',
            'greg-long-2': 'Greg Long',
            'gus-german-1': 'Gus German',
            'gus-hartwig-1': 'Gus Hartwig',
            'hayden-ellinger-1': 'Hayden Ellinger',
            'hayden-parise-1': 'Hayden Parise',
            'hunter-macdonald-1': 'Hunter MacDonald',
            'jack-albers-1': 'Jack Albers',
            'jack-ansell-1': 'Jack Ansell',
            'jack-cravaack-1': 'Jack Cravaack',
            'jack-plummer-1': 'Jack Plummer',
            'jack-sullivan-1': 'Jack Sullivan',
            'jackson-anthrop-1': 'Jackson Anthrop',
            'jacob-wahlberg-1': 'Jacob Wahlberg',
            'jaelin-alstott-vandevanter-1': 'Jaelin Alstott-VanDeVanter',
            'jahvon-grigsby-1': "Jah'von Grigsby",
            'jalen-graham-1': 'Jalen Graham',
            'jamari-brown-1': 'Jamari Brown',
            'jaquez-cross-1': "Ja'Quez Cross",
            'jared-bycznski-1': 'Jared Bycznski',
            'jaylan-alexander-1': 'Jaylan Alexander',
            'jeff-marks-1': 'Jeff Marks',
            'joseph-anderson-2': 'Joseph Anderson',
            'josh-kaltenberger-1': 'Josh Kaltenberger',
            'khali-saunders-1': 'Khali Saunders',
            'khordae-sydnor-1': 'Khordae Sydnor',
            'kieren-douglas-1': 'Kieren Douglas',
            'king-doerue-1': 'King Doerue',
            'kory-taylor-1': 'Kory Taylor',
            'kydran-jenkins-1': 'Kydran Jenkins',
            'kyle-bilodeau-1': 'Kyle Bilodeau',
            'lawrence-johnson-6': 'Lawrence Johnson',
            'mahamane-moussa-1': 'Mahamane Moussa',
            'marcellus-moore-1': 'Marcellus Moore',
            'marcus-mbow-1': 'Marcus Mbow',
            'marvin-grant-1': 'Marvin Grant',
            'mershawn-rice-1': 'Mershawn Rice',
            'michael-alaimo-1': 'Michael Alaimo',
            'milton-wright-1': 'Milton Wright',
            'mitchell-fineran-1': 'Mitchell Fineran',
            'nalin-fox-1': 'Nalin Fox',
            'nick-taylor-1': 'Nick Taylor',
            'nick-zecchino-1': 'Nick Zecchino',
            'nyles-beverly-1': 'Nyles Beverly',
            'oc-brothers-1': 'O.C. Brothers',
            'paul-piferi-1': 'Paul Piferi',
            'payne-durham-1': 'Payne Durham',
            'preston-terrell-1': 'Preston Terrell',
            'prince-boyd-jr-1': 'Prince Boyd Jr.',
            'rickey-smith-1': 'Rickey Smith',
            'robert-mcwilliams-iii-1': 'Robert McWilliams III',
            'ryan-brandt-1': 'Ryan Brandt',
            'sam-garvin-1': 'Sam Garvin',
            'sampson-james-1': 'Sampson James',
            'sanoussi-kane-1': 'Sanoussi Kane',
            'semisi-fakasiieiki-1': 'Semisi Fakasiieiki',
            'spencer-holstege-1': 'Spencer Holstege',
            'sulaiman-kpaka-1': 'Sulaiman Kpaka',
            'tj-sheffield-1': 'TJ Sheffield',
            'tristan-cox-1': 'Tristan Cox',
            'tyler-witt-1': 'Tyler Witt',
            'will-chapman-1': 'Will Chapman',
            'yanni-karlaftis-1': 'Yanni Karlaftis',
            'zac-collins-1': 'Zac Collins',
            'zac-tuinei-2': 'Zac Tuinei',
            'zach-richards-2': 'Zach Richards',
            'zane-greene-1': 'Zane Greene'
        }


    def test_roster_class_string_representation(self):
        expected = """Aidan O'Connell (aidan-oconnell-1)
None (jack-plummer-1)
None (austin-burton-1)
None (jack-albers-1)
None (michael-alaimo-1)
None (christian-gelov-1)
None (andrew-hobson-1)
None (king-doerue-1)
None (alexander-horvath-1)
None (dylan-downing-2)
None (jaquez-cross-1)
None (will-chapman-1)
None (sampson-james-1)
None (caleb-lahey-1)
None (devin-mockobee-1)
None (jackson-anthrop-1)
David Bell (david-bell-6)
None (milton-wright-1)
None (deion-burks-1)
None (marcellus-moore-1)
None (tj-sheffield-1)
None (broc-thompson-1)
None (mershawn-rice-1)
None (abdur-rahmaan-yaseen-1)
None (andrew-sowinski-1)
None (alex-maxwell-1)
None (collin-sullivan-1)
None (camdyn-childers-1)
None (hayden-parise-1)
None (kory-taylor-1)
None (preston-terrell-1)
None (ben-van-noord-1)
None (payne-durham-1)
None (garrett-miller-2)
None (paul-piferi-1)
None (kyle-bilodeau-1)
None (jack-cravaack-1)
None (drew-biber-1)
None (ben-buechel-1)
None (spencer-holstege-1)
None (cam-craig-1)
None (gus-hartwig-1)
None (eric-miller-6)
None (dj-washington-1)
None (tyler-witt-1)
None (jaelin-alstott-vandevanter-1)
None (jared-bycznski-1)
None (nalin-fox-1)
None (sam-garvin-1)
None (gus-german-1)
None (josh-kaltenberger-1)
None (ben-kuhns-1)
None (greg-long-2)
None (marcus-mbow-1)
None (dave-monnot-iii-1)
None (mahamane-moussa-1)
None (zach-richards-2)
None (aaron-roberts-3)
Mitchell Fineran (mitchell-fineran-1)
None (ben-freehill-1)
None (edward-dellinger-1)
None (caleb-krockover-1)
None (chris-van-eekeren-1)
Jaylan Alexander (jaylan-alexander-1)
None (oc-brothers-1)
None (kieren-douglas-1)
None (ben-furtney-1)
None (jalen-graham-1)
None (yanni-karlaftis-1)
None (ben-kreul-1)
None (khali-saunders-1)
None (jacob-wahlberg-1)
None (clyde-washington-2)
None (semisi-fakasiieiki-1)
None (robert-mcwilliams-iii-1)
None (zac-tuinei-2)
None (jack-ansell-1)
None (zac-collins-1)
None (brendan-cropsey-1)
None (cam-allen-1)
None (joseph-anderson-2)
None (bryce-austin-1)
None (prince-boyd-jr-1)
None (ryan-brandt-1)
None (jamari-brown-1)
None (branson-deen-1)
None (marvin-grant-1)
None (zane-greene-1)
None (chris-jefferson-1)
None (kydran-jenkins-1)
None (lawrence-johnson-6)
None (sanoussi-kane-1)
None (george-karlaftis-1)
None (damarjhe-lewis-1)
None (dedrick-mackey-1)
None (jeff-marks-1)
None (damarcus-mitchell-1)
None (jack-sullivan-1)
None (cory-trice-1)
None (elijah-ball-2)
None (nyles-beverly-1)
None (brandon-calloway-1)
None (tristan-cox-1)
None (hayden-ellinger-1)
None (jahvon-grigsby-1)
None (byron-hubbard-1)
None (greg-hudgins-iii-1)
None (dontay-hunter-ii-1)
None (sulaiman-kpaka-1)
None (hunter-macdonald-1)
None (anthony-romphf-1)
None (rickey-smith-1)
None (antonio-stevens-1)
None (khordae-sydnor-1)
None (nick-taylor-1)
None (nick-zecchino-1)"""

        roster = self.roster
        assert roster.__repr__() == expected

    def test_coach(self):
        roster = self.roster
        assert "Jeff Brohm" == self.roster.coach
