import mock
import os
import pandas as pd
import pytest
from flexmock import flexmock
from sports import utils
from sports.utils import _rate_limit_pq
from sports.nfl.roster import Player, Roster
from sports.nfl.teams import Team
from ..utils import read_file
from pyquery import PyQuery as pq


YEAR = 2018


def mock_pyquery(url):
    if 'BAD' in url or 'bad' in url:
        return None
    if '404' in url:
        return 'Page Not Found (404 error)'
    if 'Davi' in url:
        return read_file('DaviDe00.html', 'nfl', 'roster')
    if 'Lewi' in url:
        return read_file('LewiTo00.html', 'nfl', 'roster')
    if 'Lutz' in url:
        return read_file('LutzWi00.html', 'nfl', 'roster')
    if 'Mors' in url:
        return read_file('MorsTh00.html', 'nfl', 'roster')
    if 'Hatf' in url:
        return read_file('HatfDo00.html', 'nfl', 'roster')
    if 'nor' in url:
        return read_file('2018_roster.htm', 'nfl', 'roster')
    if 'Bree' in url:
        return read_file('BreeDr00.html', 'nfl', 'roster')
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


class TestNFLPlayer:
    def setup_method(self):
        self.qb_results_career = {
            'adjusted_net_yards_per_attempt_index': None,
            'adjusted_net_yards_per_pass_attempt': 7.1,
            'adjusted_yards_per_attempt': 7.7,
            'adjusted_yards_per_attempt_index': None,
            'all_purpose_yards': None,
            'approximate_value': 277,
            'assists_on_tackles': None,
            'attempted_passes': 10551,
            'birth_date': '1979-01-15',
            'blocked_punts': None,
            'catch_percentage': 88.9,
            'completed_passes': 7142,
            'completion_percentage_index': None,
            'drop_percentage': None,
            'dropped_passes': None,
            'espn_qbr': None,
            'extra_point_percentage': None,
            'extra_points_attempted': None,
            'extra_points_made': None,
            'field_goal_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': None,
            'fifty_plus_yard_field_goal_attempts': None,
            'fifty_plus_yard_field_goals_made': None,
            'first_downs_receiving': None,
            'first_downs_rushing': None,
            'fourth_quarter_comebacks': 36.0,
            'fourty_to_fourty_nine_yard_field_goal_attempts': None,
            'fourty_to_fourty_nine_yard_field_goals_made': None,
            'fumbles': 111,
            'fumbles_forced': 0.0,
            'fumbles_recovered': 34.0,
            'fumbles_recovered_for_touchdown': 0.0,
            'game_winning_drives': 53.0,
            'games': 287,
            'games_started': 286,
            'height': '72',
            'interception_percentage': 2.3,
            'interception_percentage_index': None,
            'interceptions': None,
            'interceptions_returned_for_touchdown': None,
            'interceptions_thrown': 243,
            'kickoff_return_touchdown': None,
            'kickoff_return_yards': None,
            'kickoff_returns': None,
            'less_than_nineteen_yards_field_goal_attempts': None,
            'less_than_nineteen_yards_field_goals_made': None,
            'longest_field_goal_made': None,
            'longest_interception_return': None,
            'longest_kickoff_return': None,
            'longest_pass': 98,
            'longest_punt': None,
            'longest_punt_return': None,
            'longest_reception': 38.0,
            'longest_rush': 22,
            'name': 'Drew Brees',
            'net_yards_per_attempt_index': None,
            'net_yards_per_pass_attempt': 7.05,
            'passer_rating_index': None,
            'passes_defended': None,
            'passing_completion': 67.7,
            'passing_touchdown_percentage': 5.4,
            'passing_touchdowns': 571,
            'passing_yards': 80358,
            'passing_yards_per_attempt': 7.6,
            'player_id': 'BreeDr00',
            'position': 'QB',
            'punt_return_touchdown': None,
            'punt_return_yards': None,
            'punt_returns': None,
            'punts': None,
            'qb_record': '172-114-0',
            'quarterback_rating': 98.7,
            'receiving_broken_tackles': None,
            'receiving_touchdowns': 1.0,
            'receiving_yards': 74.0,
            'receiving_yards_after_catch': None,
            'receiving_yards_after_catch_per_reception': None,
            'receiving_yards_before_catch': None,
            'receiving_yards_before_catch_per_reception': None,
            'receiving_yards_per_game': 0.3,
            'receiving_yards_per_reception': 9.3,
            'receptions': 8.0,
            'receptions_per_broken_tackle': None,
            'receptions_per_game': 0.0,
            'rush_attempts': 498,
            'rush_attempts_per_broken_tackle': None,
            'rush_attempts_per_game': 1.7,
            'rush_broken_tackles': None,
            'rush_touchdowns': 25,
            'rush_yards': 752,
            'rush_yards_after_contact': None,
            'rush_yards_after_contact_per_attempt': None,
            'rush_yards_before_contact': None,
            'rush_yards_before_contact_per_attempt': None,
            'rush_yards_per_attempt': 1.5,
            'rush_yards_per_game': 2.6,
            'rushing_and_receiving_touchdowns': 26,
            'sack_percentage': None,
            'sack_percentage_index': None,
            'sacks': 0.0,
            'safeties': None,
            'season': 'Career',
            'tackles': None,
            'team_abbreviation': '',
            'thirty_to_thirty_nine_yard_field_goal_attempts': None,
            'thirty_to_thirty_nine_yard_field_goals_made': None,
            'times_pass_target': 9.0,
            'times_sacked': 420,
            'total_punt_yards': None,
            'touchdown_percentage_index': None,
            'touches': 506,
            'twenty_to_twenty_nine_yard_field_goal_attempts': None,
            'twenty_to_twenty_nine_yard_field_goals_made': None,
            'weight': 213,
            'yards_from_scrimmage': 826,
            'yards_lost_to_sacks': 2991,
            'yards_per_attempt_index': None,
            'yards_per_completed_pass': 11.3,
            'yards_per_game_played': 280.0,
            'yards_per_kickoff_return': None,
            'yards_per_punt': None,
            'yards_per_punt_return': None,
            'yards_per_touch': 1.6,
            'yards_recovered_from_fumble': -102.0,
            'yards_returned_from_interception': None
        }

        self.qb_results_2017 = {
            'adjusted_net_yards_per_attempt_index': 121.0,
            'adjusted_net_yards_per_pass_attempt': 7.71,
            'adjusted_yards_per_attempt': 8.3,
            'adjusted_yards_per_attempt_index': 117.0,
            'all_purpose_yards': None,
            'approximate_value': 17,
            'assists_on_tackles': None,
            'attempted_passes': 536,
            'birth_date': '1979-01-15',
            'blocked_punts': None,
            'catch_percentage': None,
            'completed_passes': 386,
            'completion_percentage_index': 131.0,
            'drop_percentage': None,
            'dropped_passes': None,
            'espn_qbr': 62.5,
            'extra_point_percentage': None,
            'extra_points_attempted': None,
            'extra_points_made': None,
            'field_goal_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': None,
            'fifty_plus_yard_field_goal_attempts': None,
            'fifty_plus_yard_field_goals_made': None,
            'first_downs_receiving': None,
            'first_downs_rushing': None,
            'fourth_quarter_comebacks': 2.0,
            'fourty_to_fourty_nine_yard_field_goal_attempts': None,
            'fourty_to_fourty_nine_yard_field_goals_made': None,
            'fumbles': 5,
            'fumbles_forced': 0.0,
            'fumbles_recovered': 3.0,
            'fumbles_recovered_for_touchdown': 0.0,
            'game_winning_drives': 2.0,
            'games': 16,
            'games_started': 16,
            'height': '72',
            'interception_percentage': 1.5,
            'interception_percentage_index': 114.0,
            'interceptions': None,
            'interceptions_returned_for_touchdown': None,
            'interceptions_thrown': 8,
            'kickoff_return_touchdown': None,
            'kickoff_return_yards': None,
            'kickoff_returns': None,
            'less_than_nineteen_yards_field_goal_attempts': None,
            'less_than_nineteen_yards_field_goals_made': None,
            'longest_field_goal_made': None,
            'longest_interception_return': None,
            'longest_kickoff_return': None,
            'longest_pass': 54,
            'longest_punt': None,
            'longest_punt_return': None,
            'longest_reception': None,
            'longest_rush': 7,
            'name': 'Drew Brees',
            'net_yards_per_attempt_index': 124.0,
            'net_yards_per_pass_attempt': 7.53,
            'passer_rating_index': 119.0,
            'passes_defended': None,
            'passing_completion': 72.0,
            'passing_touchdown_percentage': 4.3,
            'passing_touchdowns': 23,
            'passing_yards': 4334,
            'passing_yards_per_attempt': 8.1,
            'player_id': 'BreeDr00',
            'position': 'QB',
            'punt_return_touchdown': None,
            'punt_return_yards': None,
            'punt_returns': None,
            'punts': None,
            'qb_record': '11-5-0',
            'quarterback_rating': 103.9,
            'receiving_broken_tackles': None,
            'receiving_touchdowns': None,
            'receiving_yards': None,
            'receiving_yards_after_catch': None,
            'receiving_yards_after_catch_per_reception': None,
            'receiving_yards_before_catch': None,
            'receiving_yards_before_catch_per_reception': None,
            'receiving_yards_per_game': None,
            'receiving_yards_per_reception': None,
            'receptions': None,
            'receptions_per_broken_tackle': None,
            'receptions_per_game': None,
            'rush_attempts': 33,
            'rush_attempts_per_broken_tackle': None,
            'rush_attempts_per_game': 2.1,
            'rush_broken_tackles': None,
            'rush_touchdowns': 2,
            'rush_yards': 12,
            'rush_yards_after_contact': None,
            'rush_yards_after_contact_per_attempt': None,
            'rush_yards_before_contact': None,
            'rush_yards_before_contact_per_attempt': None,
            'rush_yards_per_attempt': 0.4,
            'rush_yards_per_game': 0.8,
            'rushing_and_receiving_touchdowns': 2,
            'sack_percentage': None,
            'sack_percentage_index': 120.0,
            'sacks': 0.0,
            'safeties': None,
            'season': '2017',
            'tackles': None,
            'team_abbreviation': 'NOR',
            'thirty_to_thirty_nine_yard_field_goal_attempts': None,
            'thirty_to_thirty_nine_yard_field_goals_made': None,
            'times_pass_target': None,
            'times_sacked': 20,
            'total_punt_yards': None,
            'touchdown_percentage_index': 99.0,
            'touches': 33,
            'twenty_to_twenty_nine_yard_field_goal_attempts': None,
            'twenty_to_twenty_nine_yard_field_goals_made': None,
            'weight': 213,
            'yards_from_scrimmage': 12,
            'yards_lost_to_sacks': 145,
            'yards_per_attempt_index': 119.0,
            'yards_per_completed_pass': 11.2,
            'yards_per_game_played': 270.9,
            'yards_per_kickoff_return': None,
            'yards_per_punt': None,
            'yards_per_punt_return': None,
            'yards_per_touch': 0.4,
            'yards_recovered_from_fumble': -12.0,
            'yards_returned_from_interception': None
        }

        self.olb_results_career = {
            'adjusted_net_yards_per_attempt_index': None,
            'adjusted_net_yards_per_pass_attempt': None,
            'adjusted_yards_per_attempt': None,
            'adjusted_yards_per_attempt_index': None,
            'all_purpose_yards': None,
            'approximate_value': 92.0,
            'assists_on_tackles': 359,
            'attempted_passes': None,
            'birth_date': '1989-01-11',
            'blocked_punts': None,
            'catch_percentage': None,
            'completed_passes': None,
            'completion_percentage_index': None,
            'drop_percentage': None,
            'dropped_passes': None,
            'espn_qbr': None,
            'extra_point_percentage': None,
            'extra_points_attempted': None,
            'extra_points_made': None,
            'field_goal_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': None,
            'fifty_plus_yard_field_goal_attempts': None,
            'fifty_plus_yard_field_goals_made': None,
            'first_downs_receiving': None,
            'first_downs_rushing': None,
            'fourth_quarter_comebacks': None,
            'fourty_to_fourty_nine_yard_field_goal_attempts': None,
            'fourty_to_fourty_nine_yard_field_goals_made': None,
            'fumbles': 0.0,
            'fumbles_forced': 3.0,
            'fumbles_recovered': 7.0,
            'fumbles_recovered_for_touchdown': 0.0,
            'game_winning_drives': None,
            'games': 170,
            'games_started': 156,
            'height': '74',
            'interception_percentage': None,
            'interception_percentage_index': None,
            'interceptions': 2.0,
            'interceptions_returned_for_touchdown': 0.0,
            'interceptions_thrown': None,
            'kickoff_return_touchdown': None,
            'kickoff_return_yards': None,
            'kickoff_returns': None,
            'less_than_nineteen_yards_field_goal_attempts': None,
            'less_than_nineteen_yards_field_goals_made': None,
            'longest_field_goal_made': None,
            'longest_interception_return': 1.0,
            'longest_kickoff_return': None,
            'longest_pass': None,
            'longest_punt': None,
            'longest_punt_return': None,
            'longest_reception': None,
            'longest_rush': None,
            'name': 'Demario Davis',
            'net_yards_per_attempt_index': None,
            'net_yards_per_pass_attempt': None,
            'passer_rating_index': None,
            'passes_defended': 43.0,
            'passing_completion': None,
            'passing_touchdown_percentage': None,
            'passing_touchdowns': None,
            'passing_yards': None,
            'passing_yards_per_attempt': None,
            'player_id': 'DaviDe00',
            'position': 'LB',
            'punt_return_touchdown': None,
            'punt_return_yards': None,
            'punt_returns': None,
            'punts': None,
            'qb_record': None,
            'quarterback_rating': None,
            'receiving_broken_tackles': None,
            'receiving_touchdowns': None,
            'receiving_yards': None,
            'receiving_yards_after_catch': None,
            'receiving_yards_after_catch_per_reception': None,
            'receiving_yards_before_catch': None,
            'receiving_yards_before_catch_per_reception': None,
            'receiving_yards_per_game': None,
            'receiving_yards_per_reception': None,
            'receptions': None,
            'receptions_per_broken_tackle': None,
            'receptions_per_game': None,
            'rush_attempts': None,
            'rush_attempts_per_broken_tackle': None,
            'rush_attempts_per_game': None,
            'rush_broken_tackles': None,
            'rush_touchdowns': None,
            'rush_yards': None,
            'rush_yards_after_contact': None,
            'rush_yards_after_contact_per_attempt': None,
            'rush_yards_before_contact': None,
            'rush_yards_before_contact_per_attempt': None,
            'rush_yards_per_attempt': None,
            'rush_yards_per_game': None,
            'rushing_and_receiving_touchdowns': None,
            'sack_percentage': None,
            'sack_percentage_index': None,
            'sacks': 35.5,
            'safeties': None,
            'season': 'Career',
            'tackles': 726,
            'team_abbreviation': '',
            'thirty_to_thirty_nine_yard_field_goal_attempts': None,
            'thirty_to_thirty_nine_yard_field_goals_made': None,
            'times_pass_target': None,
            'times_sacked': None,
            'total_punt_yards': None,
            'touchdown_percentage_index': None,
            'touches': None,
            'twenty_to_twenty_nine_yard_field_goal_attempts': None,
            'twenty_to_twenty_nine_yard_field_goals_made': None,
            'weight': 235,
            'yards_from_scrimmage': None,
            'yards_lost_to_sacks': None,
            'yards_per_attempt_index': None,
            'yards_per_completed_pass': None,
            'yards_per_game_played': None,
            'yards_per_kickoff_return': None,
            'yards_per_punt': None,
            'yards_per_punt_return': None,
            'yards_per_touch': None,
            'yards_recovered_from_fumble': 8.0,
            'yards_returned_from_interception': 1.0
        }

        self.kicker_results_career = {
            'adjusted_net_yards_per_attempt_index': None,
            'adjusted_net_yards_per_pass_attempt': None,
            'adjusted_yards_per_attempt': None,
            'adjusted_yards_per_attempt_index': None,
            'all_purpose_yards': None,
            'approximate_value': 20.0,
            'assists_on_tackles': 1.0,
            'attempted_passes': None,
            'birth_date': '1994-07-07',
            'blocked_punts': None,
            'catch_percentage': None,
            'completed_passes': None,
            'completion_percentage_index': None,
            'drop_percentage': None,
            'dropped_passes': None,
            'espn_qbr': None,
            'extra_point_percentage': 97.5,
            'extra_points_attempted': 281,
            'extra_points_made': 274,
            'field_goal_percentage': 85.3,
            'field_goals_attempted': 184,
            'field_goals_made': 157,
            'fifty_plus_yard_field_goal_attempts': 27,
            'fifty_plus_yard_field_goals_made': 16,
            'first_downs_receiving': None,
            'first_downs_rushing': None,
            'fourth_quarter_comebacks': None,
            'fourty_to_fourty_nine_yard_field_goal_attempts': 65,
            'fourty_to_fourty_nine_yard_field_goals_made': 55,
            'fumbles': 0.0,
            'fumbles_forced': None,
            'fumbles_recovered': None,
            'fumbles_recovered_for_touchdown': None,
            'game_winning_drives': None,
            'games': 90,
            'games_started': None,
            'height': None,
            'interception_percentage': None,
            'interception_percentage_index': None,
            'interceptions': None,
            'interceptions_returned_for_touchdown': None,
            'interceptions_thrown': None,
            'kickoff_return_touchdown': None,
            'kickoff_return_yards': None,
            'kickoff_returns': None,
            'less_than_nineteen_yards_field_goal_attempts': 3.0,
            'less_than_nineteen_yards_field_goals_made': 3.0,
            'longest_field_goal_made': 60,
            'longest_interception_return': None,
            'longest_kickoff_return': None,
            'longest_pass': None,
            'longest_punt': None,
            'longest_punt_return': None,
            'longest_reception': None,
            'longest_rush': 4.0,
            'name': 'Wil Lutz',
            'net_yards_per_attempt_index': None,
            'net_yards_per_pass_attempt': None,
            'passer_rating_index': None,
            'passes_defended': None,
            'passing_completion': None,
            'passing_touchdown_percentage': None,
            'passing_touchdowns': None,
            'passing_yards': None,
            'passing_yards_per_attempt': None,
            'player_id': 'LutzWi00',
            'position': '',
            'punt_return_touchdown': None,
            'punt_return_yards': None,
            'punt_returns': None,
            'punts': None,
            'qb_record': None,
            'quarterback_rating': None,
            'receiving_broken_tackles': None,
            'receiving_touchdowns': None,
            'receiving_yards': None,
            'receiving_yards_after_catch': None,
            'receiving_yards_after_catch_per_reception': None,
            'receiving_yards_before_catch': None,
            'receiving_yards_before_catch_per_reception': None,
            'receiving_yards_per_game': None,
            'receiving_yards_per_reception': None,
            'receptions': None,
            'receptions_per_broken_tackle': None,
            'receptions_per_game': None,
            'rush_attempts': 1.0,
            'rush_attempts_per_broken_tackle': None,
            'rush_attempts_per_game': 0.0,
            'rush_broken_tackles': None,
            'rush_touchdowns': 0.0,
            'rush_yards': 4.0,
            'rush_yards_after_contact': None,
            'rush_yards_after_contact_per_attempt': None,
            'rush_yards_before_contact': None,
            'rush_yards_before_contact_per_attempt': None,
            'rush_yards_per_attempt': 4.0,
            'rush_yards_per_game': 0.0,
            'rushing_and_receiving_touchdowns': 0.0,
            'sack_percentage': None,
            'sack_percentage_index': None,
            'sacks': 0.0,
            'safeties': None,
            'season': 'Career',
            'tackles': 6.0,
            'team_abbreviation': '',
            'thirty_to_thirty_nine_yard_field_goal_attempts': 51,
            'thirty_to_thirty_nine_yard_field_goals_made': 46,
            'times_pass_target': None,
            'times_sacked': None,
            'total_punt_yards': None,
            'touchdown_percentage_index': None,
            'touches': 1.0,
            'twenty_to_twenty_nine_yard_field_goal_attempts': 38,
            'twenty_to_twenty_nine_yard_field_goals_made': 37,
            'weight': None,
            'yards_from_scrimmage': 4.0,
            'yards_lost_to_sacks': None,
            'yards_per_attempt_index': None,
            'yards_per_completed_pass': None,
            'yards_per_game_played': None,
            'yards_per_kickoff_return': None,
            'yards_per_punt': None,
            'yards_per_punt_return': None,
            'yards_per_touch': 4.0,
            'yards_recovered_from_fumble': None,
            'yards_returned_from_interception': None
        }

        self.punter_results_career = {
            'adjusted_net_yards_per_attempt_index': None,
            'adjusted_net_yards_per_pass_attempt': -2.0,
            'adjusted_yards_per_attempt': None,
            'adjusted_yards_per_attempt_index': None,
            'all_purpose_yards': None,
            'approximate_value': 35.0,
            'assists_on_tackles': 0.0,
            'attempted_passes': 0.0,
            'birth_date': '1986-03-08',
            'blocked_punts': 1,
            'catch_percentage': None,
            'completed_passes': 0.0,
            'completion_percentage_index': None,
            'drop_percentage': None,
            'dropped_passes': None,
            'espn_qbr': None,
            'extra_point_percentage': None,
            'extra_points_attempted': None,
            'extra_points_made': None,
            'field_goal_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': None,
            'fifty_plus_yard_field_goal_attempts': None,
            'fifty_plus_yard_field_goals_made': None,
            'first_downs_receiving': None,
            'first_downs_rushing': None,
            'fourth_quarter_comebacks': None,
            'fourty_to_fourty_nine_yard_field_goal_attempts': None,
            'fourty_to_fourty_nine_yard_field_goals_made': None,
            'fumbles': None,
            'fumbles_forced': None,
            'fumbles_recovered': None,
            'fumbles_recovered_for_touchdown': None,
            'game_winning_drives': None,
            'games': 190,
            'games_started': 0,
            'height': '76',
            'interception_percentage': None,
            'interception_percentage_index': None,
            'interceptions': None,
            'interceptions_returned_for_touchdown': None,
            'interceptions_thrown': 0.0,
            'kickoff_return_touchdown': None,
            'kickoff_return_yards': None,
            'kickoff_returns': None,
            'less_than_nineteen_yards_field_goal_attempts': None,
            'less_than_nineteen_yards_field_goals_made': None,
            'longest_field_goal_made': None,
            'longest_interception_return': None,
            'longest_kickoff_return': None,
            'longest_pass': 0.0,
            'longest_punt': 70,
            'longest_punt_return': None,
            'longest_reception': None,
            'longest_rush': None,
            'name': 'Thomas Morstead',
            'net_yards_per_attempt_index': None,
            'net_yards_per_pass_attempt': -2.0,
            'passer_rating_index': None,
            'passes_defended': None,
            'passing_completion': None,
            'passing_touchdown_percentage': None,
            'passing_touchdowns': 0.0,
            'passing_yards': 0.0,
            'passing_yards_per_attempt': None,
            'player_id': 'MorsTh00',
            'position': '',
            'punt_return_touchdown': None,
            'punt_return_yards': None,
            'punt_returns': None,
            'punts': 768,
            'qb_record': '',
            'quarterback_rating': None,
            'receiving_broken_tackles': None,
            'receiving_touchdowns': None,
            'receiving_yards': None,
            'receiving_yards_after_catch': None,
            'receiving_yards_after_catch_per_reception': None,
            'receiving_yards_before_catch': None,
            'receiving_yards_before_catch_per_reception': None,
            'receiving_yards_per_game': None,
            'receiving_yards_per_reception': None,
            'receptions': None,
            'receptions_per_broken_tackle': None,
            'receptions_per_game': None,
            'rush_attempts': None,
            'rush_attempts_per_broken_tackle': None,
            'rush_attempts_per_game': None,
            'rush_broken_tackles': None,
            'rush_touchdowns': None,
            'rush_yards': None,
            'rush_yards_after_contact': None,
            'rush_yards_after_contact_per_attempt': None,
            'rush_yards_before_contact': None,
            'rush_yards_before_contact_per_attempt': None,
            'rush_yards_per_attempt': None,
            'rush_yards_per_game': None,
            'rushing_and_receiving_touchdowns': None,
            'sack_percentage': None,
            'sack_percentage_index': None,
            'sacks': 0.0,
            'safeties': None,
            'season': 'Career',
            'tackles': 13.0,
            'team_abbreviation': 'NOR',
            'thirty_to_thirty_nine_yard_field_goal_attempts': None,
            'thirty_to_thirty_nine_yard_field_goals_made': None,
            'times_pass_target': None,
            'times_sacked': 1.0,
            'total_punt_yards': 35729,
            'touchdown_percentage_index': None,
            'touches': None,
            'twenty_to_twenty_nine_yard_field_goal_attempts': None,
            'twenty_to_twenty_nine_yard_field_goals_made': None,
            'weight': 225,
            'yards_from_scrimmage': None,
            'yards_lost_to_sacks': 2.0,
            'yards_per_attempt_index': None,
            'yards_per_completed_pass': None,
            'yards_per_game_played': 0.0,
            'yards_per_kickoff_return': None,
            'yards_per_punt': 46.5,
            'yards_per_punt_return': None,
            'yards_per_touch': None,
            'yards_recovered_from_fumble': None,
            'yards_returned_from_interception': None
        }

        self.receiver_results_career = {
            'adjusted_net_yards_per_attempt_index': None,
            'adjusted_net_yards_per_pass_attempt': None,
            'adjusted_yards_per_attempt': None,
            'adjusted_yards_per_attempt_index': None,
            'all_purpose_yards': 1361,
            'approximate_value': 3,
            'assists_on_tackles': 0.0,
            'attempted_passes': None,
            'birth_date': '1992-10-24',
            'blocked_punts': None,
            'catch_percentage': 66.7,
            'completed_passes': None,
            'completion_percentage_index': None,
            'drop_percentage': None,
            'dropped_passes': None,
            'espn_qbr': None,
            'extra_point_percentage': None,
            'extra_points_attempted': None,
            'extra_points_made': None,
            'field_goal_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': None,
            'fifty_plus_yard_field_goal_attempts': None,
            'fifty_plus_yard_field_goals_made': None,
            'first_downs_receiving': None,
            'first_downs_rushing': None,
            'fourth_quarter_comebacks': None,
            'fourty_to_fourty_nine_yard_field_goal_attempts': None,
            'fourty_to_fourty_nine_yard_field_goals_made': None,
            'fumbles': 4,
            'fumbles_forced': 0.0,
            'fumbles_recovered': 1.0,
            'fumbles_recovered_for_touchdown': 0.0,
            'game_winning_drives': None,
            'games': 41,
            'games_started': 4,
            'height': None,
            'interception_percentage': None,
            'interception_percentage_index': None,
            'interceptions': None,
            'interceptions_returned_for_touchdown': None,
            'interceptions_thrown': None,
            'kickoff_return_touchdown': 0,
            'kickoff_return_yards': 640,
            'kickoff_returns': 28,
            'less_than_nineteen_yards_field_goal_attempts': None,
            'less_than_nineteen_yards_field_goals_made': None,
            'longest_field_goal_made': None,
            'longest_interception_return': None,
            'longest_kickoff_return': 39,
            'longest_pass': None,
            'longest_punt': None,
            'longest_punt_return': 59,
            'longest_reception': 52,
            'longest_rush': 16.0,
            'name': 'Tommylee Lewis',
            'net_yards_per_attempt_index': None,
            'net_yards_per_pass_attempt': None,
            'passer_rating_index': None,
            'passes_defended': None,
            'passing_completion': None,
            'passing_touchdown_percentage': None,
            'passing_touchdowns': None,
            'passing_yards': None,
            'passing_yards_per_attempt': None,
            'player_id': 'LewiTo00',
            'position': 'WR',
            'punt_return_touchdown': 0,
            'punt_return_yards': 408,
            'punt_returns': 48,
            'punts': None,
            'qb_record': None,
            'quarterback_rating': None,
            'receiving_broken_tackles': None,
            'receiving_touchdowns': 2,
            'receiving_yards': 264,
            'receiving_yards_after_catch': None,
            'receiving_yards_after_catch_per_reception': None,
            'receiving_yards_before_catch': None,
            'receiving_yards_before_catch_per_reception': None,
            'receiving_yards_per_game': 6.4,
            'receiving_yards_per_reception': 12.0,
            'receptions': 22,
            'receptions_per_broken_tackle': None,
            'receptions_per_game': 0.5,
            'rush_attempts': 9.0,
            'rush_attempts_per_broken_tackle': None,
            'rush_attempts_per_game': 0.2,
            'rush_broken_tackles': None,
            'rush_touchdowns': 0.0,
            'rush_yards': 49.0,
            'rush_yards_after_contact': None,
            'rush_yards_after_contact_per_attempt': None,
            'rush_yards_before_contact': None,
            'rush_yards_before_contact_per_attempt': None,
            'rush_yards_per_attempt': 5.4,
            'rush_yards_per_game': 1.2,
            'rushing_and_receiving_touchdowns': 2,
            'sack_percentage': None,
            'sack_percentage_index': None,
            'sacks': 0.0,
            'safeties': None,
            'season': 'Career',
            'tackles': 1.0,
            'team_abbreviation': '',
            'thirty_to_thirty_nine_yard_field_goal_attempts': None,
            'thirty_to_thirty_nine_yard_field_goals_made': None,
            'times_pass_target': 33,
            'times_sacked': None,
            'total_punt_yards': None,
            'touchdown_percentage_index': None,
            'touches': 31,
            'twenty_to_twenty_nine_yard_field_goal_attempts': None,
            'twenty_to_twenty_nine_yard_field_goals_made': None,
            'weight': None,
            'yards_from_scrimmage': 313,
            'yards_lost_to_sacks': None,
            'yards_per_attempt_index': None,
            'yards_per_completed_pass': None,
            'yards_per_game_played': None,
            'yards_per_kickoff_return': 22.9,
            'yards_per_punt': None,
            'yards_per_punt_return': 8.5,
            'yards_per_touch': 10.1,
            'yards_recovered_from_fumble': 0.0,
            'yards_returned_from_interception': None
        }

        self.receiver_results_2017 = {
            'adjusted_net_yards_per_attempt_index': None,
            'adjusted_net_yards_per_pass_attempt': None,
            'adjusted_yards_per_attempt': None,
            'adjusted_yards_per_attempt_index': None,
            'all_purpose_yards': 552,
            'approximate_value': 1,
            'assists_on_tackles': None,
            'attempted_passes': None,
            'birth_date': '1992-10-24',
            'blocked_punts': None,
            'catch_percentage': 71.4,
            'completed_passes': None,
            'completion_percentage_index': None,
            'drop_percentage': None,
            'dropped_passes': None,
            'espn_qbr': None,
            'extra_point_percentage': None,
            'extra_points_attempted': None,
            'extra_points_made': None,
            'field_goal_percentage': None,
            'field_goals_attempted': None,
            'field_goals_made': None,
            'fifty_plus_yard_field_goal_attempts': None,
            'fifty_plus_yard_field_goals_made': None,
            'first_downs_receiving': None,
            'first_downs_rushing': None,
            'fourth_quarter_comebacks': None,
            'fourty_to_fourty_nine_yard_field_goal_attempts': None,
            'fourty_to_fourty_nine_yard_field_goals_made': None,
            'fumbles': 1,
            'fumbles_forced': 0.0,
            'fumbles_recovered': 0.0,
            'fumbles_recovered_for_touchdown': 0.0,
            'game_winning_drives': None,
            'games': 15,
            'games_started': 0,
            'height': None,
            'interception_percentage': None,
            'interception_percentage_index': None,
            'interceptions': None,
            'interceptions_returned_for_touchdown': None,
            'interceptions_thrown': None,
            'kickoff_return_touchdown': 0,
            'kickoff_return_yards': 307,
            'kickoff_returns': 13,
            'less_than_nineteen_yards_field_goal_attempts': None,
            'less_than_nineteen_yards_field_goals_made': None,
            'longest_field_goal_made': None,
            'longest_interception_return': None,
            'longest_kickoff_return': 39,
            'longest_pass': None,
            'longest_punt': None,
            'longest_punt_return': 24,
            'longest_reception': 52,
            'longest_rush': 8.0,
            'name': 'Tommylee Lewis',
            'net_yards_per_attempt_index': None,
            'net_yards_per_pass_attempt': None,
            'passer_rating_index': None,
            'passes_defended': None,
            'passing_completion': None,
            'passing_touchdown_percentage': None,
            'passing_touchdowns': None,
            'passing_yards': None,
            'passing_yards_per_attempt': None,
            'player_id': 'LewiTo00',
            'position': 'WR',
            'punt_return_touchdown': 0,
            'punt_return_yards': 115,
            'punt_returns': 14,
            'punts': None,
            'qb_record': None,
            'quarterback_rating': None,
            'receiving_broken_tackles': None,
            'receiving_touchdowns': 1,
            'receiving_yards': 116,
            'receiving_yards_after_catch': None,
            'receiving_yards_after_catch_per_reception': None,
            'receiving_yards_before_catch': None,
            'receiving_yards_before_catch_per_reception': None,
            'receiving_yards_per_game': 7.7,
            'receiving_yards_per_reception': 11.6,
            'receptions': 10,
            'receptions_per_broken_tackle': None,
            'receptions_per_game': 0.7,
            'rush_attempts': 2.0,
            'rush_attempts_per_broken_tackle': None,
            'rush_attempts_per_game': 0.1,
            'rush_broken_tackles': None,
            'rush_touchdowns': 0.0,
            'rush_yards': 14.0,
            'rush_yards_after_contact': None,
            'rush_yards_after_contact_per_attempt': None,
            'rush_yards_before_contact': None,
            'rush_yards_before_contact_per_attempt': None,
            'rush_yards_per_attempt': 7.0,
            'rush_yards_per_game': 0.9,
            'rushing_and_receiving_touchdowns': 1,
            'sack_percentage': None,
            'sack_percentage_index': None,
            'sacks': 0.0,
            'safeties': None,
            'season': '2017',
            'tackles': None,
            'team_abbreviation': 'NOR',
            'thirty_to_thirty_nine_yard_field_goal_attempts': None,
            'thirty_to_thirty_nine_yard_field_goals_made': None,
            'times_pass_target': 14,
            'times_sacked': None,
            'total_punt_yards': None,
            'touchdown_percentage_index': None,
            'touches': 12,
            'twenty_to_twenty_nine_yard_field_goal_attempts': None,
            'twenty_to_twenty_nine_yard_field_goals_made': None,
            'weight': None,
            'yards_from_scrimmage': 130,
            'yards_lost_to_sacks': None,
            'yards_per_attempt_index': None,
            'yards_per_completed_pass': None,
            'yards_per_game_played': None,
            'yards_per_kickoff_return': 23.6,
            'yards_per_punt': None,
            'yards_per_punt_return': 8.2,
            'yards_per_touch': 10.8,
            'yards_recovered_from_fumble': 0.0,
            'yards_returned_from_interception': None
        }

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_qb_returns_requested_career_stats(self, *args, **kwargs):
        # Request the career stats
        player = Player('BreeDr00')
        player = player('')

        for attribute, value in self.qb_results_career.items():
            assert getattr(player, attribute) == value

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_qb_returns_requested_player_season_stats(self,
                                                          *args,
                                                          **kwargs):
        # Request the 2017 stats
        player = Player('BreeDr00')
        player = player('2017')

        for attribute, value in self.qb_results_2017.items():
            assert getattr(player, attribute) == value

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_olb_returns_requested_career_stats(self, *args, **kwargs):
        # Request the career stats
        player = Player('DaviDe00')
        player = player('')

        for attribute, value in self.olb_results_career.items():
            assert getattr(player, attribute) == value

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_kicker_returns_requested_career_stats(self, *args, **kwargs):
        # Request the career stats
        player = Player('LutzWi00')
        player = player('')

        for attribute, value in self.kicker_results_career.items():
            assert getattr(player, attribute) == value

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_punter_returns_requested_career_stats(self, *args, **kwargs):
        # Request the career stats
        player = Player('MorsTh00')
        player = player('')

        for attribute, value in self.punter_results_career.items():
            assert getattr(player, attribute) == value

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_receiver_requested_career_stats(self, *args, **kwargs):
        # Request the career stats
        player = Player('LewiTo00')
        player = player('')

        for attribute, value in self.receiver_results_career.items():
            assert getattr(player, attribute) == value

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_receiver_season_stats(self, *args, **kwargs):
        # Request the 2017 stats
        player = Player('LewiTo00')
        player = player('2017')

        for attribute, value in self.receiver_results_2017.items():
            assert getattr(player, attribute) == value

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_dataframe_returns_dataframe(self, *args, **kwargs):
        dataframe = [
            {'adjusted_net_yards_per_attempt_index': 116,
             'adjusted_net_yards_per_pass_attempt': 7.71,
             'adjusted_yards_per_attempt': 8.3,
             'adjusted_yards_per_attempt_index': 114,
             'all_purpose_yards': None,
             'approximate_value': 16,
             'assists_on_tackles': None,
             'attempted_passes': 536,
             'birth_date': '1979-01-15',
             'blocked_punts': None,
             'catch_percentage': None,
             'completed_passes': 386,
             'completion_percentage_index': 128,
             'espn_qbr': 64.6,
             'extra_point_percentage': None,
             'extra_points_attempted': None,
             'extra_points_made': None,
             'field_goal_percentage': None,
             'field_goals_attempted': None,
             'field_goals_made': None,
             'fifty_plus_yard_field_goal_attempts': None,
             'fifty_plus_yard_field_goals_made': None,
             'fourth_quarter_comebacks': 2,
             'fourty_to_fourty_nine_yard_field_goal_attempts': None,
             'fourty_to_fourty_nine_yard_field_goals_made': None,
             'fumbles': 5,
             'fumbles_forced': 0,
             'fumbles_recovered': 5,
             'fumbles_recovered_for_touchdown': -12,
             'game_winning_drives': 2,
             'games': 16,
             'games_started': 16,
             'height': '6-0',
             'interception_percentage': 1.5,
             'interception_percentage_index': 112,
             'interceptions': None,
             'interceptions_returned_for_touchdown': None,
             'interceptions_thrown': 8,
             'kickoff_return_touchdown': None,
             'kickoff_return_yards': None,
             'kickoff_returns': None,
             'less_than_nineteen_yards_field_goal_attempts': None,
             'less_than_nineteen_yards_field_goals_made': None,
             'longest_field_goal_made': None,
             'longest_interception_return': None,
             'longest_kickoff_return': None,
             'longest_pass': 54,
             'longest_punt': None,
             'longest_punt_return': None,
             'longest_reception': None,
             'longest_rush': 7,
             'name': 'Drew Brees',
             'net_yards_per_attempt_index': 118,
             'net_yards_per_pass_attempt': 7.53,
             'passer_rating_index': 116,
             'passes_defended': None,
             'passing_completion': 72.0,
             'passing_touchdown_percentage': 4.3,
             'passing_touchdowns': 23,
             'passing_yards': 4334,
             'passing_yards_per_attempt': 8.1,
             'player_id': 'BreeDr00',
             'position': 'QB',
             'punt_return_touchdown': None,
             'punt_return_yards': None,
             'punt_returns': None,
             'punts': None,
             'qb_record': '11-5-0',
             'quarterback_rating': 103.9,
             'receiving_touchdowns': None,
             'receiving_yards': None,
             'receiving_yards_per_game': None,
             'receiving_yards_per_reception': None,
             'receptions': None,
             'receptions_per_game': None,
             'rush_attempts': 33,
             'rush_attempts_per_game': 2.1,
             'rush_touchdowns': 2,
             'rush_yards': 12,
             'rush_yards_per_attempt': 0.4,
             'rush_yards_per_game': 0.8,
             'rushing_and_receiving_touchdowns': 2,
             'sack_percentage': None,
             'sack_percentage_index': 116,
             'sacks': None,
             'safeties': None,
             'season': '2017',
             'tackles': None,
             'team_abbreviation': 'NOR',
             'thirty_to_thirty_nine_yard_field_goal_attempts': None,
             'thirty_to_thirty_nine_yard_field_goals_made': None,
             'times_pass_target': None,
             'times_sacked': 20,
             'total_punt_yards': None,
             'touchdown_percentage_index': 100,
             'touches': 33,
             'twenty_to_twenty_nine_yard_field_goal_attempts': None,
             'twenty_to_twenty_nine_yard_field_goals_made': None,
             'weight': 209,
             'yards_from_scrimmage': 12,
             'yards_lost_to_sacks': 145,
             'yards_per_attempt_index': 115,
             'yards_per_completed_pass': 11.2,
             'yards_per_game_played': 270.9,
             'yards_per_kickoff_return': None,
             'yards_per_punt': None,
             'yards_per_punt_return': None,
             'yards_per_touch': 0.4,
             'yards_recovered_from_fumble': 3,
             'yards_returned_from_interception': None},
            {'adjusted_net_yards_per_attempt_index': 126,
             'adjusted_net_yards_per_pass_attempt': 8.93,
             'adjusted_yards_per_attempt': 9.6,
             'adjusted_yards_per_attempt_index': 125,
             'all_purpose_yards': None,
             'approximate_value': None,
             'assists_on_tackles': None,
             'attempted_passes': 129,
             'birth_date': '1979-01-15',
             'blocked_punts': None,
             'catch_percentage': None,
             'completed_passes': 104,
             'completion_percentage_index': 151,
             'espn_qbr': None,
             'extra_point_percentage': None,
             'extra_points_attempted': None,
             'extra_points_made': None,
             'field_goal_percentage': None,
             'field_goals_attempted': None,
             'field_goals_made': None,
             'fifty_plus_yard_field_goal_attempts': None,
             'fifty_plus_yard_field_goals_made': None,
             'fourth_quarter_comebacks': 2,
             'fourty_to_fourty_nine_yard_field_goal_attempts': None,
             'fourty_to_fourty_nine_yard_field_goals_made': None,
             'fumbles': 1,
             'fumbles_forced': 0,
             'fumbles_recovered': 1,
             'fumbles_recovered_for_touchdown': 0,
             'game_winning_drives': 2,
             'games': 3,
             'games_started': 3,
             'height': '6-0',
             'interception_percentage': 0.0,
             'interception_percentage_index': 131,
             'interceptions': None,
             'interceptions_returned_for_touchdown': None,
             'interceptions_thrown': 0,
             'kickoff_return_touchdown': None,
             'kickoff_return_yards': None,
             'kickoff_returns': None,
             'less_than_nineteen_yards_field_goal_attempts': None,
             'less_than_nineteen_yards_field_goals_made': None,
             'longest_field_goal_made': None,
             'longest_interception_return': None,
             'longest_kickoff_return': None,
             'longest_pass': 42,
             'longest_punt': None,
             'longest_punt_return': None,
             'longest_reception': None,
             'longest_rush': 7,
             'name': 'Drew Brees',
             'net_yards_per_attempt_index': 120,
             'net_yards_per_pass_attempt': 7.73,
             'passer_rating_index': 133,
             'passes_defended': None,
             'passing_completion': 80.6,
             'passing_touchdown_percentage': 6.2,
             'passing_touchdowns': 8,
             'passing_yards': 1078,
             'passing_yards_per_attempt': 8.4,
             'player_id': 'BreeDr00',
             'position': 'QB',
             'punt_return_touchdown': None,
             'punt_return_yards': None,
             'punt_returns': None,
             'punts': None,
             'qb_record': '2-1-0',
             'quarterback_rating': 122.2,
             'receiving_touchdowns': None,
             'receiving_yards': None,
             'receiving_yards_per_game': None,
             'receiving_yards_per_reception': None,
             'receptions': None,
             'receptions_per_game': None,
             'rush_attempts': 4,
             'rush_attempts_per_game': 1.3,
             'rush_touchdowns': 2,
             'rush_yards': 6,
             'rush_yards_per_attempt': 1.5,
             'rush_yards_per_game': 2.0,
             'rushing_and_receiving_touchdowns': 2,
             'sack_percentage': None,
             'sack_percentage_index': 116,
             'sacks': None,
             'safeties': None,
             'season': '2018',
             'tackles': None,
             'team_abbreviation': 'NOR',
             'thirty_to_thirty_nine_yard_field_goal_attempts': None,
             'thirty_to_thirty_nine_yard_field_goals_made': None,
             'times_pass_target': None,
             'times_sacked': 5,
             'total_punt_yards': None,
             'touchdown_percentage_index': 113,
             'touches': 4,
             'twenty_to_twenty_nine_yard_field_goal_attempts': None,
             'twenty_to_twenty_nine_yard_field_goals_made': None,
             'weight': 209,
             'yards_from_scrimmage': 6,
             'yards_lost_to_sacks': 42,
             'yards_per_attempt_index': 117,
             'yards_per_completed_pass': 10.4,
             'yards_per_game_played': 359.3,
             'yards_per_kickoff_return': None,
             'yards_per_punt': None,
             'yards_per_punt_return': None,
             'yards_per_touch': 1.5,
             'yards_recovered_from_fumble': 1,
             'yards_returned_from_interception': None},
            {'adjusted_net_yards_per_attempt_index': 113,
             'adjusted_net_yards_per_pass_attempt': 6.98,
             'adjusted_yards_per_attempt': 7.6,
             'adjusted_yards_per_attempt_index': 111,
             'all_purpose_yards': None,
             'approximate_value': 239,
             'assists_on_tackles': 0,
             'attempted_passes': 9423,
             'birth_date': '1979-01-15',
             'blocked_punts': None,
             'catch_percentage': None,
             'completed_passes': 6326,
             'completion_percentage_index': 119,
             'espn_qbr': None,
             'extra_point_percentage': None,
             'extra_points_attempted': None,
             'extra_points_made': None,
             'field_goal_percentage': None,
             'field_goals_attempted': None,
             'field_goals_made': None,
             'fifty_plus_yard_field_goal_attempts': None,
             'fifty_plus_yard_field_goals_made': None,
             'fourth_quarter_comebacks': 30,
             'fourty_to_fourty_nine_yard_field_goal_attempts': None,
             'fourty_to_fourty_nine_yard_field_goals_made': None,
             'fumbles': 102,
             'fumbles_forced': 0,
             'fumbles_recovered': 102,
             'fumbles_recovered_for_touchdown': 0,
             'game_winning_drives': 43,
             'games': 252,
             'games_started': 251,
             'height': '6-0',
             'interception_percentage': 2.4,
             'interception_percentage_index': 105,
             'interceptions': None,
             'interceptions_returned_for_touchdown': None,
             'interceptions_thrown': 228,
             'kickoff_return_touchdown': None,
             'kickoff_return_yards': None,
             'kickoff_returns': None,
             'less_than_nineteen_yards_field_goal_attempts': None,
             'less_than_nineteen_yards_field_goals_made': None,
             'longest_field_goal_made': None,
             'longest_interception_return': None,
             'longest_kickoff_return': None,
             'longest_pass': 98,
             'longest_punt': None,
             'longest_punt_return': None,
             'longest_reception': 38,
             'longest_rush': 22,
             'name': 'Drew Brees',
             'net_yards_per_attempt_index': 114,
             'net_yards_per_pass_attempt': 7.01,
             'passer_rating_index': 114,
             'passes_defended': None,
             'passing_completion': 67.1,
             'passing_touchdown_percentage': 5.3,
             'passing_touchdowns': 496,
             'passing_yards': 71523,
             'passing_yards_per_attempt': 7.6,
             'player_id': 'BreeDr00',
             'position': '',
             'punt_return_touchdown': None,
             'punt_return_yards': None,
             'punt_returns': None,
             'punts': None,
             'qb_record': '144-107-0',
             'quarterback_rating': 97.1,
             'receiving_touchdowns': 1,
             'receiving_yards': 73,
             'receiving_yards_per_game': 0.3,
             'receiving_yards_per_reception': 10.4,
             'receptions': 7,
             'receptions_per_game': 0.0,
             'rush_attempts': 444,
             'rush_attempts_per_game': 1.8,
             'rush_touchdowns': 20,
             'rush_yards': 742,
             'rush_yards_per_attempt': 1.7,
             'rush_yards_per_game': 2.9,
             'rushing_and_receiving_touchdowns': 21,
             'sack_percentage': None,
             'sack_percentage_index': 116,
             'sacks': None,
             'safeties': None,
             'season': 'Career',
             'tackles': 13,
             'team_abbreviation': '',
             'thirty_to_thirty_nine_yard_field_goal_attempts': None,
             'thirty_to_thirty_nine_yard_field_goals_made': None,
             'times_pass_target': 8,
             'times_sacked': 383,
             'total_punt_yards': None,
             'touchdown_percentage_index': 110,
             'touches': 451,
             'twenty_to_twenty_nine_yard_field_goal_attempts': None,
             'twenty_to_twenty_nine_yard_field_goals_made': None,
             'weight': 209,
             'yards_from_scrimmage': 815,
             'yards_lost_to_sacks': 2734,
             'yards_per_attempt_index': 110,
             'yards_per_completed_pass': 11.3,
             'yards_per_game_played': 283.8,
             'yards_per_kickoff_return': None,
             'yards_per_punt': None,
             'yards_per_punt_return': None,
             'yards_per_touch': 1.8,
             'yards_recovered_from_fumble': 29,
             'yards_returned_from_interception': None}
        ]
        indices = ['2017', '2018', 'Career']

        df = pd.DataFrame(dataframe, index=indices)
        player = Player('BreeDr00')
        player = player('')

        # Pandas doesn't natively allow comparisons of DataFrames.
        # Concatenating the two DataFrames (the one generated during the test
        # and the expected one above) and dropping duplicate rows leaves only
        # the rows that are unique between the two frames. This allows a quick
        # check of the DataFrame to see if it is empty - if so, all rows are
        # duplicates, and they are equal.
        frames = [df, player.dataframe]
        df1 = pd.concat(frames).drop_duplicates(keep=False)

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_fake_404_page_returns_none_with_no_errors(self,
                                                           *args,
                                                           **kwargs):
        player = Player('404')

        assert player.name is None
        assert player.dataframe is None

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_fake_404_page_returns_none_for_different_season(self,
                                                                 *args,
                                                                 **kwargs):
        player = Player('404')
        player = player('2017')

        assert player.name is None
        assert player.dataframe is None

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_player_with_no_career_stats_handled_properly(self,
                                                              *args,
                                                              **kwargs):
        player = Player('HatfDo00')

        assert player.name == 'Dominique Hatfield'

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_nfl_player_string_representation(self, *args, **kwargs):
        player = Player('BreeDr00')

        assert player.__repr__() == 'Drew Brees (BreeDr00)'


class TestNFLRoster:
    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_roster_class_pulls_all_player_stats(self, *args, **kwargs):
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return('2018')
        roster = Roster('NOR')

        assert len(roster.players) == 64

        roster_players = [player.name for player in roster.players]
        for player in ['Drew Brees', 'Demario Davis',
                                   'Tommylee Lewis', 'Wil Lutz',
                                   'Thomas Morstead']:
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
        team = Team(team_data=None, rank=1, year='2018')
        mock_abbreviation = mock.PropertyMock(return_value='NOR')
        type(team)._abbreviation = mock_abbreviation

        assert len(team.roster.players) == 64

        roster_players = [player.name for player in team.roster.players]
        for player in ['Drew Brees', 'Demario Davis',
                                   'Tommylee Lewis', 'Wil Lutz',
                                   'Thomas Morstead']:
            assert player in roster_players
        type(team)._abbreviation = None

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_roster_class_with_slim_parameter(self, *args, **kwargs):
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return('2018')
        roster = Roster('NOR', slim=True)
        assert len(roster.players) == 64
        for player in ['Drew Brees', 'Demario Davis',
                                   'Tommylee Lewis', 'Wil Lutz',
                                   'Thomas Morstead']:
            assert player in [v for k, v in roster.players.items()]

    @mock.patch('requests.head', side_effect=mock_request)
    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_invalid_default_year_reverts_to_previous_year(self,
                                                           *args,
                                                           **kwargs):
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return(2019)

        roster = Roster('NOR')

        assert len(roster.players) == 64
        roster_players = [player.name for player in roster.players]
        for player in ['Drew Brees', 'Demario Davis',
                                   'Tommylee Lewis', 'Wil Lutz',
                                   'Thomas Morstead']:
            assert player in roster_players

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_roster_class_string_representation(self, *args, **kwargs):
        expected = """None (AnzaAl00)
None (ApplEl00)
None (ArmsTe00)
None (ArnoDa00)
None (BanjCh00)
None (BellVo00)
None (BiegVi00)
Drew Brees (BreeDr00)
None (BridTe00)
None (BromJa00)
None (BushJe20)
None (CarrAu00)
None (ClapWi00)
None (ColeKu99)
None (CrawKe02)
None (DaveMa00)
Demario Davis (DaviDe00)
Demario Davis (DaviTy01)
None (GillMi00)
None (GinnTe00)
None (GrayJ.00)
None (HardJu01)
None (HendTr00)
None (HillJo02)
None (HillTa00)
None (IngrMa01)
None (JordCa00)
None (KamaAl00)
None (KirkKe00)
None (KleiAJ00)
None (LattMa01)
None (LeRiJo00)
Tommylee Lewis (LewiTo00)
None (LineZa01)
None (LoewMi00)
None (LucaCo01)
Wil Lutz (LutzWi00)
None (MaulAr00)
None (MereCa00)
Thomas Morstead (MorsTh00)
None (NewtDe00)
None (OkafAl00)
None (OlaxMi00)
None (OnyeDa00)
None (PeatAn00)
None (RamcRy00)
None (RankSh00)
None (RobeCr00)
None (RobiJo01)
None (RobiPa99)
None (SmitTr03)
None (StalTa00)
None (TateBr00)
None (TeoxMa00)
None (ThomMi05)
None (TomxCa00)
None (UngeMa20)
None (WarfLa00)
None (WashDw00)
None (WatsBe00)
None (WillJo07)
None (WillMa06)
None (WillP.00)
None (WoodZa00)"""

        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return('2018')
        roster = Roster('NOR')
        assert roster.__repr__() == expected

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_coach(self, *args, **kwargs):
        assert "Sean Payton" == Roster('NOR', year=YEAR).coach
