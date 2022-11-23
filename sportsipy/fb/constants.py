SQUAD_URL = 'https://fbref.com/en/squads/%s'

SCHEDULE_SCHEME = {
    'date': 'th[data-stat="date"]',
    'competition': 'td[data-stat="comp"]',
    'matchweek': 'td[data-stat="round"]',
    'day': 'td[data-stat="dayofweek"]',
    'time': 'td[data-stat="time"]',
    'venue': 'td[data-stat="venue"]',
    'result': 'td[data-stat="result"]',
    'goals_for': 'td[data-stat="goals_for"]',
    'goals_against': 'td[data-stat="goals_against"]',
    'opponent': 'td[data-stat="opponent"]',
    'expected_goals': 'td[data-stat="xg_for"]',
    'expected_goals_against': 'td[data-stat="xg_against"]',
    'attendance': 'td[data-stat="attendance"]',
    'captain': 'td[data-stat="captain"]',
    'formation': 'td[data-stat="formation"]',
    'referee': 'td[data-stat="referee"]',
    'match_report': 'td[data-stat="match_report"]',
    'notes': 'td[data-stat="notes"]'
}

ROSTER_SCHEME = {
    'name': 'th[data-stat="player"]',
    'nationality': 'td[data-stat="nationality"] a',
    'position': 'td[data-stat="position"]',
    'age': 'td[data-stat="age"]',
    'matches_played': 'td[data-stat="games"]',
    'starts': 'td[data-stat="games_starts"]',
    'minutes': 'td[data-stat="minutes"]',
    'goals': 'td[data-stat="goals"]',
    'assists': 'td[data-stat="assists"]',
    'penalty_kicks': 'td[data-stat="pens_made"]',
    'penalty_kick_attempts': 'td[data-stat="pens_att"]',
    'yellow_cards': 'td[data-stat="cards_yellow"]',
    'red_cards': 'td[data-stat="cards_red"]',
    'goals_per_90': 'td[data-stat="goals_per90"]',
    'assists_per_90': 'td[data-stat="assists_per90"]',
    'goals_and_assists_per_90': 'td[data-stat="goals_assists_per90"]',
    'goals_non_penalty_per_90': 'td[data-stat="goals_pens_per90"]',
    'goals_and_assists_non_penalty_per_90':
    'td[data-stat="goals_assists_pens_per90"]',
    'expected_goals': 'td[data-stat="xg"]',
    'expected_goals_non_penalty': 'td[data-stat="npxg"]',
    'expected_assists': 'td[data-stat="xg_assist"]',
    'expected_goals_per_90': 'td[data-stat="xg_per90"]',
    'expected_assists_per_90': 'td[data-stat="xg_assist_per90"]',
    'expected_goals_and_assists_per_90': 'td[data-stat="xg_xg_assist_per90"]',
    'expected_goals_non_penalty_per_90': 'td[data-stat="npxg_per90"]',
    'expected_goals_and_assists_non_penalty_per_90':
    'td[data-stat="npxg_xg_assist_per90"]',
    'own_goals': 'td[data-stat="own_goals"]',
    'goals_against': 'td[data-stat="gk_goals_against"]',
    'own_goals_against': 'td[data-stat="gk_own_goals_against"]',
    'goals_against_per_90': 'td[data-stat="gk_goals_against_per90"]',
    'shots_on_target_against': 'td[data-stat="gk_shots_on_target_against"]',
    'saves': 'td[data-stat="gk_saves"]',
    'save_percentage': 'td[data-stat="gk_save_pct"]',
    'wins': 'td[data-stat="gk_wins"]',
    'draws': 'td[data-stat="gk_ties"]',
    'losses': 'td[data-stat="gk_losses"]',
    'clean_sheets': 'td[data-stat="gk_clean_sheets"]',
    'clean_sheet_percentage': 'td[data-stat="gk_clean_sheets_pct"]',
    'penalty_kicks_attempted': 'td[data-stat="gk_pens_att"]',
    'penalty_kicks_allowed': 'td[data-stat="gk_pens_allowed"]',
    'penalty_kicks_saved': 'td[data-stat="gk_pens_saved"]',
    'penalty_kicks_missed': 'td[data-stat="gk_pens_missed"]',
    'free_kick_goals_against': 'td[data-stat="gk_free_kick_goals_against"]',
    'corner_kick_goals_against': 'td[data-stat="gk_corner_kick_goals_against"]',
    'post_shot_expected_goals': 'td[data-stat="gk_psxg"]',
    'post_shot_expected_goals_per_shot':
    'td[data-stat="gk_psnpxg_per_shot_on_target_against"]',
    'post_shot_expected_goals_minus_allowed': 'td[data-stat="gk_psxg_net"]',
    'post_shot_expected_goals_minus_allowed_per_90':
    'td[data-stat="gk_psxg_net_per90"]',
    'launches_completed': 'td[data-stat="gk_passes_completed_launched"]',
    'launches_attempted': 'td[data-stat="gk_passes_launched"]',
    'launch_completion_percentage': 'td[data-stat="gk_passes_pct_launched"]',
    'keeper_passes_attempted': 'td[data-stat="gk_passes"]',
    'throws_attempted': 'td[data-stat="gk_passes_throws"]',
    'launch_percentage': 'td[data-stat="gk_pct_passes_launched"]',
    'average_keeper_pass_length': 'td[data-stat="gk_passes_length_avg"]',
    'goal_kicks_attempted': 'td[data-stat="gk_goal_kicks"]',
    'goal_kick_launch_percentage': 'td[data-stat="gk_pct_goal_kicks_launched"]',
    'average_goal_kick_length': 'td[data-stat="gk_goal_kick_length_avg"]',
    'opponent_cross_attempts': 'td[data-stat="gk_crosses"]',
    'opponent_cross_stops': 'td[data-stat="gk_crosses_stopped"]',
    'opponent_cross_stop_percentage': 'td[data-stat="gk_crosses_stopped_pct"]',
    'keeper_actions_outside_penalty_area':
    'td[data-stat="gk_def_actions_outside_pen_area"]',
    'keeper_actions_outside_penalty_area_per_90':
    'td[data-stat="gk_def_actions_outside_pen_area_per90"]',
    'average_keeper_action_outside_penalty_distance':
    'td[data-stat="gk_avg_distance_def_actions"]',
    'shots': 'td[data-stat="shots"]',
    'shots_on_target': 'td[data-stat="shots_on_target"]',
    'free_kick_shots': 'td[data-stat="shots_free_kicks"]',
    'shots_on_target_percentage': 'td[data-stat="shots_on_target_pct"]',
    'shots_per_90': 'td[data-stat="shots_per90"]',
    'shots_on_target_per_90': 'td[data-stat="shots_on_target_per90"]',
    'goals_per_shot': 'td[data-stat="goals_per_shot"]',
    'goals_per_shot_on_target': 'td[data-stat="goals_per_shot_on_target"]',
    'expected_goals_non_penalty_per_shot': 'td[data-stat="npxg_per_shot"]',
    'goals_minus_expected': 'td[data-stat="xg_net"]',
    'non_penalty_minus_expected_non_penalty': 'td[data-stat="npxg_net"]',
    'assists_minus_expected': 'td[data-stat="xg_assist_net"]',
    'key_passes': 'td[data-stat="assisted_shots"]',
    'passes_completed': 'td[data-stat="passes_completed"]',
    'passes_attempted': 'td[data-stat="passes"]',
    'pass_completion': 'td[data-stat="passes_pct"]',
    'short_passes_completed': 'td[data-stat="passes_completed_short"]',
    'short_passes_attempted': 'td[data-stat="passes_short"]',
    'short_pass_completion': 'td[data-stat="passes_pct_short"]',
    'medium_passes_completed': 'td[data-stat="passes_completed_medium"]',
    'medium_passes_attempted': 'td[data-stat="passes_medium"]',
    'medium_pass_completion': 'td[data-stat="passes_pct_medium"]',
    'long_passes_completed': 'td[data-stat="passes_completed_long"]',
    'long_passes_attempted': 'td[data-stat="passes_long"]',
    'long_pass_completion': 'td[data-stat="passes_pct_long"]',
    'left_foot_passes': 'td[data-stat="passes_left_foot"]',
    'right_foot_passes': 'td[data-stat="passes_right_foot"]',
    'free_kick_passes': 'td[data-stat="passes_free_kicks"]',
    'through_balls': 'td[data-stat="through_balls"]',
    'corner_kicks': 'td[data-stat="corner_kicks"]',
    'throw_ins': 'td[data-stat="throw_ins"]',
    'final_third_passes': 'td[data-stat="passes_into_final_third"]',
    'penalty_area_passes': 'td[data-stat="passes_into_penalty_area"]',
    'penalty_area_crosses': 'td[data-stat="crosses_into_penalty_area"]',
    'minutes_per_match': 'td[data-stat="minutes_per_game"]',
    'minutes_played_percentage': 'td[data-stat="minutes_pct"]',
    'nineties_played': 'td[data-stat="minutes_90s"]',
    'minutes_per_start': 'td[data-stat="minutes_per_start"]',
    'subs': 'td[data-stat="games_subs"]',
    'minutes_per_sub': 'td[data-stat="minutes_per_sub"]',
    'unused_sub': 'td[data-stat="unused_subs"]',
    'points_per_match': 'td[data-stat="points_per_game"]',
    'goals_scored_on_pitch': 'td[data-stat="on_goals_for"]',
    'goals_against_on_pitch': 'td[data-stat="on_goals_against"]',
    'goal_difference_on_pitch': 'td[data-stat="plus_minus"]',
    'goal_difference_on_pitch_per_90': 'td[data-stat="plus_minus_per90"]',
    'net_difference_on_pitch_per_90': 'td[data-stat="plus_minus_wowy"]',
    'expected_goals_on_pitch': 'td[data-stat="on_xg_for"]',
    'expected_goals_against_on_pitch': 'td[data-stat="on_xg_against"]',
    'expected_goal_difference': 'td[data-stat="xg_plus_minus"]',
    'expected_goal_difference_per_90': 'td[data-stat="xg_plus_minus_per90"]',
    'net_expected_goal_difference_per_90':
    'td[data-stat="xg_plus_minus_wowy"]',
    'soft_reds': 'td[data-stat="cards_yellow_red"]',
    'fouls_committed': 'td[data-stat="fouls"]',
    'fouls_drawn': 'td[data-stat="fouled"]',
    'offsides': 'td[data-stat="offsides"]',
    'crosses': 'td[data-stat="crosses"]',
    'tackles_won': 'td[data-stat="tackles_won"]',
    'interceptions': 'td[data-stat="interceptions"]',
    'penalty_kicks_won': 'td[data-stat="pens_won"]',
    'penalty_kicks_conceded': 'td[data-stat="pens_conceded"]',
    'successful_dribbles': 'td[data-stat="dribbles_completed"]',
    'attempted_dribbles': 'td[data-stat="dribbles"]',
    'dribble_success_rate': 'td[data-stat="dribbles_completed_pct"]',
    'players_dribbled_past': 'td[data-stat="players_dribbled_past"]',
    'nutmegs': 'td[data-stat="nutmegs"]',
    'dribblers_tackled': 'td[data-stat="dribble_tackles"]',
    'dribblers_contested': 'td[data-stat="dribbles_vs"]',
    'tackle_percentage': 'td[data-stat="dribble_tackles_pct"]',
    'times_dribbled_past': 'td[data-stat="dribbled_past"]'
}
