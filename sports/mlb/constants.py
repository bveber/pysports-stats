PARSING_SCHEME = {
    "name": "a",
    "league": 'td[data-stat="lg_ID"]:first',
    "games": 'td[data-stat="G"]:first',
    "wins": 'td[data-stat="W"]:first',
    "losses": 'td[data-stat="L"]:first',
    "win_percentage": 'td[data-stat="win_loss_perc"]:first',
    "streak": 'td[data-stat="winning_streak"]:first',
    "runs": 'td[data-stat="R"]:first',
    "runs_against": 'td[data-stat="RA"]:first',
    "run_difference": 'td[data-stat="run_diff"]:first',
    "strength_of_schedule": 'td[data-stat="strength_of_schedule"]:first',
    "simple_rating_system": 'td[data-stat="simple_rating_system"]:first',
    "pythagorean_win_loss": 'td[data-stat="record_pythag"]:first',
    "luck": 'td[data-stat="luck_pythag"]:first',
    "interleague_record": 'td[data-stat="record_interleague"]:first',
    "home_record": 'td[data-stat="record_home"]:first',
    "away_record": 'td[data-stat="record_road"]:first',
    "extra_inning_record": 'td[data-stat="record_xinn"]:first',
    "single_run_record": 'td[data-stat="record_one_run"]:first',
    "record_vs_right_handed_pitchers": 'td[data-stat="record_vs_rhp"]:first',
    "record_vs_left_handed_pitchers": 'td[data-stat="record_vs_lhp"]:first',
    "record_vs_teams_over_500": 'td[data-stat="record_vs_over_500"]:first',
    "record_vs_teams_under_500": 'td[data-stat="record_vs_under_500"]:first',
    "last_ten_games_record": 'td[data-stat="record_last_10"]:first',
    "last_twenty_games_record": 'td[data-stat="record_last_20"]:first',
    "last_thirty_games_record": 'td[data-stat="record_last_30"]:first',
    "number_players_used": 'td[data-stat="batters_used"]:first',
    "average_batter_age": 'td[data-stat="age_bat"]:first',
    "plate_appearances": 'td[data-stat="PA"]:first',
    "at_bats": 'td[data-stat="AB"]:first',
    "total_runs": 'td[data-stat="R"]:first',
    "hits": 'td[data-stat="H"]:first',
    "doubles": 'td[data-stat="2B"]:first',
    "triples": 'td[data-stat="3B"]:first',
    "home_runs": 'td[data-stat="HR"]:first',
    "runs_batted_in": 'td[data-stat="RBI"]:first',
    "stolen_bases": 'td[data-stat="SB"]:first',
    "times_caught_stealing": 'td[data-stat="CS"]:first',
    "bases_on_balls": 'td[data-stat="BB"]:first',
    "times_struck_out": 'td[data-stat="SO"]:first',
    "batting_average": 'td[data-stat="batting_avg"]:first',
    "on_base_percentage": 'td[data-stat="onbase_perc"]:first',
    "slugging_percentage": 'td[data-stat="slugging_perc"]:first',
    "on_base_plus_slugging_percentage": 'td[data-stat="onbase_plus_slugging"]:first',
    "on_base_plus_slugging_percentage_plus": 'td[data-stat="onbase_plus_slugging_plus"]:first',
    "total_bases": 'td[data-stat="TB"]:first',
    "grounded_into_double_plays": 'td[data-stat="GIDP"]:first',
    "times_hit_by_pitch": 'td[data-stat="HBP"]:first',
    "sacrifice_hits": 'td[data-stat="SH"]:first',
    "sacrifice_flies": 'td[data-stat="SF"]:first',
    "intentional_bases_on_balls": 'td[data-stat="IBB"]:first',
    "runners_left_on_base": 'td[data-stat="LOB"]:first',
    "number_of_pitchers": 'td[data-stat="pitchers_used"]:first',
    "average_pitcher_age": 'td[data-stat="age_pitch"]:first',
    "runs_allowed_per_game": 'td[data-stat="runs_allowed_per_game"]:first',
    "earned_runs_against": 'td[data-stat="earned_run_avg"]:first',
    "games_finished": 'td[data-stat="GF"]:first',
    "complete_games": 'td[data-stat="CG"]:first',
    "shutouts": 'td[data-stat="SHO_team"]:first',
    "complete_game_shutouts": 'td[data-stat="SHO_cg"]:first',
    "saves": 'td[data-stat="SV"]:first',
    "innings_pitched": 'td[data-stat="IP"]:first',
    "hits_allowed": 'td[data-stat="H"]:first',
    "home_runs_against": 'td[data-stat="HR"]:first',
    "bases_on_walks_given": 'td[data-stat="BB"]:first',
    "strikeouts": 'td[data-stat="SO"]:first',
    "hit_pitcher": 'td[data-stat="HBP"]:first',
    "balks": 'td[data-stat="BK"]:first',
    "wild_pitches": 'td[data-stat="WP"]:first',
    "batters_faced": 'td[data-stat="batters_faced"]:first',
    "earned_runs_against_plus": 'td[data-stat="earned_run_avg_plus"]:first',
    "fielding_independent_pitching": 'td[data-stat="fip"]:first',
    "whip": 'td[data-stat="whip"]:first',
    "hits_per_nine_innings": 'td[data-stat="hits_per_nine"]:first',
    "home_runs_per_nine_innings": 'td[data-stat="home_runs_per_nine"]:first',
    "bases_on_walks_given_per_nine_innings": 'td[data-stat="bases_on_balls_per_nine"]:first',
    "strikeouts_per_nine_innings": 'td[data-stat="strikeouts_per_nine"]:first',
    "strikeouts_per_base_on_balls": 'td[data-stat="strikeouts_per_base_on_balls"]:first',
    "opposing_runners_left_on_base": 'td[data-stat="LOB"]:first',
}

TEAM_ELEMENT = {
    "home_wins": 0,
    "home_losses": 1,
    "away_wins": 0,
    "away_losses": 1,
    "extra_inning_wins": 0,
    "extra_inning_losses": 1,
    "single_run_wins": 0,
    "single_run_losses": 1,
    "wins_vs_right_handed_pitchers": 0,
    "losses_vs_right_handed_pitchers": 1,
    "wins_vs_left_handed_pitchers": 0,
    "losses_vs_left_handed_pitchers": 1,
    "wins_vs_teams_over_500": 0,
    "losses_vs_teams_over_500": 1,
    "wins_vs_teams_under_500": 0,
    "losses_vs_teams_under_500": 1,
    "wins_last_ten_games": 0,
    "losses_last_ten_games": 1,
    "wins_last_twenty_games": 0,
    "losses_last_twenty_games": 1,
    "wins_last_thirty_games": 0,
    "losses_last_thirty_games": 1,
}

SCHEDULE_SCHEME = {
    "game": 'th[data-stat="team_game"]:first',
    "date": 'td[data-stat="date_game"]:first',
    "location": 'td[data-stat="homeORvis"]:first',
    "opponent_abbr": 'td[data-stat="opp_ID"]:first',
    "result": 'td[data-stat="win_loss_result"]:first',
    "runs_scored": 'td[data-stat="R"]:first',
    "runs_allowed": 'td[data-stat="RA"]:first',
    "innings": 'td[data-stat="extra_innings"]:first',
    "record": 'td[data-stat="win_loss_record"]:first',
    "rank": 'td[data-stat="rank"]:first',
    "games_behind": 'td[data-stat="games_back"]:first',
    "winner": 'td[data-stat="winning_pitcher"]:first',
    "loser": 'td[data-stat="losing_pitcher"]:first',
    "save": 'td[data-stat="saving_pitcher"]:first',
    "game_duration": 'td[data-stat="time_of_game"]:first',
    "day_or_night": 'td[data-stat="day_or_night"]:first',
    "attendance": 'td[data-stat="attendance"]:first',
    "streak": 'td[data-stat="win_loss_streak"]:first',
}

ELEMENT_INDEX = {
    "total_runs": 1,
    "bases_on_walks_given": 1,
    "hits_allowed": 1,
    "strikeouts": 1,
    "home_runs_against": 1,
    "opposing_runners_left_on_base": 1,
}

BOXSCORE_SCHEME = {
    "game_info": 'div[class="scorebox_meta"]',
    "away_name": 'div[class="linescore_wrap"] table tbody tr:first td:nth-child(2)',
    "home_name": 'div[class="linescore_wrap"] table tbody tr:last td:nth-child(2)',
    "winner": 'td[data-stat=""]',
    "summary": 'table[class="linescore nohover stats_table no_freeze"]',
    "winning_name": 'td[data-stat=""]',
    "winning_abbr": 'td[data-stat=""]',
    "losing_name": 'td[data-stat=""]',
    "losing_abbr": 'td[data-stat=""]',
    "losing_abbr": 'td[data-stat=""]',
    "away_at_bats": 'tfoot td[data-stat="AB"]',
    "away_runs": 'tfoot td[data-stat="R"]',
    "away_hits": 'tfoot td[data-stat="H"]',
    "away_rbi": 'tfoot td[data-stat="RBI"]',
    "away_earned_runs": 'tfoot td[data-stat="earned_run_avg"]',
    "away_bases_on_balls": 'tfoot td[data-stat="BB"]',
    "away_strikeouts": 'tfoot td[data-stat="SO"]',
    "away_plate_appearances": 'tfoot td[data-stat="PA"]',
    "away_batting_average": 'tfoot td[data-stat="batting_avg"]',
    "away_on_base_percentage": 'tfoot td[data-stat="onbase_perc"]',
    "away_slugging_percentage": 'tfoot td[data-stat="slugging_perc"]',
    "away_on_base_plus": 'tfoot td[data-stat="onbase_plus_slugging"]',
    "away_pitches": 'tfoot td[data-stat="pitches"]',
    "away_strikes": 'tfoot td[data-stat="strikes_total"]',
    "away_win_probability_for_offensive_player": 'tfoot td[data-stat="wpa_bat"]',
    "away_average_leverage_index": 'tfoot td[data-stat="leverage_index_avg"]',
    "away_win_probability_added": 'tfoot td[data-stat="wpa_bat_pos"]',
    "away_win_probability_subtracted": 'tfoot td[data-stat="wpa_bat_neg"]',
    "away_base_out_runs_added": 'tfoot td[data-stat="re24_bat"]',
    "away_putouts": 'tfoot td[data-stat="PO"]',
    "away_assists": 'tfoot td[data-stat="A"]',
    "away_innings_pitched": 'tfoot td[data-stat="IP"]',
    "away_home_runs": 'tfoot td[data-stat="HR"]',
    "away_strikes_by_contact": 'tfoot td[data-stat="strikes_contact"]',
    "away_strikes_swinging": 'tfoot td[data-stat="strikes_swinging"]',
    "away_strikes_looking": 'tfoot td[data-stat="strikes_looking"]',
    "away_grounded_balls": 'tfoot td[data-stat="inplay_gb_total"]',
    "away_fly_balls": 'tfoot td[data-stat="inplay_fb_total"]',
    "away_line_drives": 'tfoot td[data-stat="inplay_ld"]',
    "away_unknown_bat_type": 'tfoot td[data-stat="inplay_unk"]',
    "away_game_score": 'tfoot td[data-stat="game_score"]',
    "away_inherited_runners": 'tfoot td[data-stat="inherited_runners"]',
    "away_inherited_score": 'tfoot td[data-stat="inherited_score"]',
    "away_win_probability_by_pitcher": 'tfoot td[data-stat="wpa_def"]',
    "away_average_leverage_index": 'tfoot td[data-stat="leverage_index_avg"]',
    "away_base_out_runs_saved": 'tfoot td[data-stat="re24_def"]',
    "home_at_bats": 'tfoot td[data-stat="AB"]',
    "home_runs": 'tfoot td[data-stat="R"]',
    "home_hits": 'tfoot td[data-stat="H"]',
    "home_rbi": 'tfoot td[data-stat="RBI"]',
    "home_earned_runs": 'tfoot td[data-stat="earned_run_avg"]',
    "home_bases_on_balls": 'tfoot td[data-stat="BB"]',
    "home_strikeouts": 'tfoot td[data-stat="SO"]',
    "home_plate_appearances": 'tfoot td[data-stat="PA"]',
    "home_batting_average": 'tfoot td[data-stat="batting_avg"]',
    "home_on_base_percentage": 'tfoot td[data-stat="onbase_perc"]',
    "home_slugging_percentage": 'tfoot td[data-stat="slugging_perc"]',
    "home_on_base_plus": 'tfoot td[data-stat="onbase_plus_slugging"]',
    "home_pitches": 'tfoot td[data-stat="pitches"]',
    "home_strikes": 'tfoot td[data-stat="strikes_total"]',
    "home_win_probability_for_offensive_player": 'tfoot td[data-stat="wpa_bat"]',
    "home_average_leverage_index": 'tfoot td[data-stat="leverage_index_avg"]',
    "home_win_probability_added": 'tfoot td[data-stat="wpa_bat_pos"]',
    "home_win_probability_subtracted": 'tfoot td[data-stat="wpa_bat_neg"]',
    "home_base_out_runs_added": 'tfoot td[data-stat="re24_bat"]',
    "home_putouts": 'tfoot td[data-stat="PO"]',
    "home_assists": 'tfoot td[data-stat="A"]',
    "home_innings_pitched": 'tfoot td[data-stat="IP"]',
    "home_home_runs": 'tfoot td[data-stat="HR"]',
    "home_strikes_by_contact": 'tfoot td[data-stat="strikes_contact"]',
    "home_strikes_swinging": 'tfoot td[data-stat="strikes_swinging"]',
    "home_strikes_looking": 'tfoot td[data-stat="strikes_looking"]',
    "home_grounded_balls": 'tfoot td[data-stat="inplay_gb_total"]',
    "home_fly_balls": 'tfoot td[data-stat="inplay_fb_total"]',
    "home_line_drives": 'tfoot td[data-stat="inplay_ld"]',
    "home_unknown_bat_type": 'tfoot td[data-stat="inplay_unk"]',
    "home_game_score": 'tfoot td[data-stat="game_score"]',
    "home_inherited_runners": 'tfoot td[data-stat="inherited_runners"]',
    "home_inherited_score": 'tfoot td[data-stat="inherited_score"]',
    "home_win_probability_by_pitcher": 'tfoot td[data-stat="wpa_def"]',
    "home_average_leverage_index": 'tfoot td[data-stat="leverage_index_avg"]',
    "home_base_out_runs_saved": 'tfoot td[data-stat="re24_def"]',
}

BOXSCORE_ELEMENT_INDEX = {
    "date": 0,
    "time": 1,
    "attendance": 2,
    "venue": 3,
    "duration": 4,
    "time_of_day": 5,
    "away_at_bats": 0,
    "away_runs": 0,
    "away_hits": 0,
    "away_rbi": 0,
    "away_earned_runs": 1,
    "away_bases_on_balls": 0,
    "away_strikeouts": 0,
    "away_plate_appearances": 0,
    "away_batting_average": 0,
    "away_on_base_percentage": 0,
    "away_slugging_percentage": 0,
    "away_on_base_plus": 0,
    "away_pitches": 1,
    "away_strikes": 0,
    "away_win_probability_for_offensive_player": 0,
    "away_average_leverage_index": 1,
    "away_win_probability_added": 0,
    "away_win_probability_subtracted": 0,
    "away_base_out_runs_added": 0,
    "away_putouts": 0,
    "away_assists": 0,
    "away_innings_pitched": 0,
    "away_home_runs": 0,
    "away_strikes_by_contact": 1,
    "away_strikes_swinging": 1,
    "away_strikes_looking": 1,
    "away_grounded_balls": 1,
    "away_fly_balls": 1,
    "away_line_drives": 1,
    "away_unknown_bat_type": 1,
    "away_game_score": 0,
    "away_inherited_runners": 0,
    "away_inherited_score": 0,
    "away_win_probability_by_pitcher": 0,
    "away_base_out_runs_saved": 0,
    "home_at_bats": 1,
    "home_runs": 1,
    "home_hits": 1,
    "home_rbi": 1,
    "home_earned_runs": 0,
    "home_bases_on_balls": 1,
    "home_strikeouts": 1,
    "home_plate_appearances": 1,
    "home_batting_average": 1,
    "home_on_base_percentage": 1,
    "home_slugging_percentage": 1,
    "home_on_base_plus": 1,
    "home_pitches": 0,
    "home_strikes": 1,
    "home_win_probability_for_offensive_player": 1,
    "home_average_leverage_index": 0,
    "home_win_probability_added": 1,
    "home_win_probability_subtracted": 1,
    "home_base_out_runs_added": 1,
    "home_putouts": 1,
    "home_assists": 1,
    "home_innings_pitched": 1,
    "home_home_runs": 1,
    "home_strikes_by_contact": 0,
    "home_strikes_swinging": 0,
    "home_strikes_looking": 0,
    "home_grounded_balls": 0,
    "home_fly_balls": 0,
    "home_line_drives": 0,
    "home_unknown_bat_type": 0,
    "home_game_score": 1,
    "home_inherited_runners": 1,
    "home_inherited_score": 1,
    "home_win_probability_by_pitcher": 1,
    "home_base_out_runs_saved": 1,
}

PLAYER_SCHEME = {
    "summary": '[data-template="Partials/Teams/Summary"]',
    "season": 'th[data-stat="year_ID"]',
    "name": 'div[class="players"] span:first',
    "team_abbreviation": 'td[data-stat="team_ID"]',
    "position": 'td[data-stat="pos"]',
    "height": 'div[class="players"] span:nth-child(1)',
    "weight": 'div[class="players"] span:nth-child(2)',
    "birth_date": "span#necro-birth",
    "nationality": 'td[data-stat=""]',
    "games": 'td[data-stat="G"]',
    "games_started": 'td[data-stat="GS"]',
    "plate_appearances": 'td[data-stat="PA"]',
    "at_bats": 'td[data-stat="AB"]',
    "runs": 'td[data-stat="R"]',
    "hits": 'td[data-stat="H"]',
    "doubles": 'td[data-stat="2B"]',
    "triples": 'td[data-stat="3B"]',
    "home_runs": 'td[data-stat="HR"]',
    "runs_batted_in": 'td[data-stat="RBI"]',
    "stolen_bases": 'td[data-stat="SB"]',
    "times_caught_stealing": 'td[data-stat="CS"]',
    "bases_on_balls": 'td[data-stat="BB"]',
    "times_struck_out": 'td[data-stat="SO"]',
    "batting_average": 'td[data-stat="batting_avg"]',
    "on_base_percentage": 'td[data-stat="onbase_perc"]',
    "slugging_percentage": 'td[data-stat="slugging_perc"]',
    "on_base_plus_slugging_percentage": 'td[data-stat="onbase_plus_slugging"]',
    "on_base_plus_slugging_percentage_plus": 'td[data-stat="onbase_plus_slugging_plus"]',
    "total_bases": 'td[data-stat="TB"]',
    "grounded_into_double_plays": 'td[data-stat="GIDP"]',
    "times_hit_by_pitch": 'td[data-stat="HBP"]',
    "sacrifice_hits": 'td[data-stat="SH"]',
    "sacrifice_flies": 'td[data-stat="SF"]',
    "intentional_bases_on_balls": 'td[data-stat="IBB"]',
    "complete_games": 'td[data-stat="CG"]',
    "innings_played": 'td[data-stat="Inn_def"]',
    "defensive_chances": 'td[data-stat="chances"]',
    "putouts": 'td[data-stat="PO"]',
    "assists": 'td[data-stat="A"]',
    "errors": 'td[data-stat="E_def"]',
    "double_plays_turned": 'td[data-stat="DP_def"]',
    "fielding_percentage": 'td[data-stat="fielding_perc"]',
    "total_fielding_runs_above_average": 'td[data-stat="tz_runs_total"]',
    "defensive_runs_saved_above_average": 'td[data-stat="bis_runs_total"]',
    "total_fielding_runs_above_average_per_innings": 'td[data-stat="tz_runs_total_per_season"]',
    "defensive_runs_saved_above_average_per_innings": 'td[data-stat="bis_runs_total_per_season"]',
    "range_factor_per_nine_innings": 'td[data-stat="range_factor_per_nine"]',
    "range_factor_per_game": 'td[data-stat="range_factor_per_game"]',
    "league_fielding_percentage": 'td[data-stat="fielding_perc_lg"]',
    "league_range_factor_per_nine_innings": 'td[data-stat="range_factor_per_nine_lg"]',
    "league_range_factor_per_game": 'td[data-stat="range_factor_per_game_lg"]',
    "games_in_batting_order": 'td[data-stat="G_batting"]',
    "games_in_defensive_lineup": 'td[data-stat="G_defense"]',
    "games_pitcher": 'td[data-stat="G_p_app"]',
    "games_catcher": 'td[data-stat="G_c"]',
    "games_first_baseman": 'td[data-stat="G_1b"]',
    "games_second_baseman": 'td[data-stat="G_2b"]',
    "games_third_baseman": 'td[data-stat="G_3b"]',
    "games_shortstop": 'td[data-stat="G_ss"]',
    "games_left_fielder": 'td[data-stat="G_lf_app"]',
    "games_center_fielder": 'td[data-stat="G_cf_app"]',
    "games_right_fielder": 'td[data-stat="G_rf_app"]',
    "games_outfielder": 'td[data-stat="G_of_app"]',
    "games_designated_hitter": 'td[data-stat="G_dh"]',
    "games_pinch_hitter": 'td[data-stat="G_ph"]',
    "games_pinch_runner": 'td[data-stat="G_pr"]',
    "wins": 'td[data-stat="W"]',
    "losses": 'td[data-stat="L"]',
    "win_percentage": 'td[data-stat="win_loss_perc"]',
    "era": 'td[data-stat="earned_run_avg"]',
    "games_finished": 'td[data-stat="GF"]',
    "shutouts": 'td[data-stat="SHO"]',
    "saves": 'td[data-stat="SV"]',
    "hits_allowed": 'td[data-stat="H"]',
    "runs_allowed": 'td[data-stat="R"]',
    "earned_runs_allowed": 'td[data-stat="ER"]',
    "home_runs_allowed": 'td[data-stat="HR"]',
    "bases_on_balls_given": 'td[data-stat="BB"]',
    "intentional_bases_on_balls_given": 'td[data-stat="IBB"]',
    "strikeouts": 'td[data-stat="SO"]',
    "times_hit_player": 'td[data-stat="HBP"]',
    "balks": 'td[data-stat="BK"]',
    "wild_pitches": 'td[data-stat="WP"]',
    "batters_faced": 'td[data-stat="batters_faced"]',
    "era_plus": 'td[data-stat="earned_run_avg_plus"]',
    "fielding_independent_pitching": 'td[data-stat="fip"]',
    "whip": 'td[data-stat="whip"]',
    "hits_against_per_nine_innings": 'td[data-stat="hits_per_nine"]',
    "home_runs_against_per_nine_innings": 'td[data-stat="home_runs_per_nine"]',
    "bases_on_balls_given_per_nine_innings": 'td[data-stat="bases_on_balls_per_nine"]',
    "batters_struckout_per_nine_innings": 'td[data-stat="strikeouts_per_nine"]',
    "strikeouts_thrown_per_walk": 'td[data-stat="strikeouts_per_base_on_balls"]',
    "win_probability_for_offensive_player": 'td[data-stat="wpa_bat"]',
    "win_probability_added": 'td[data-stat="wpa_bat_pos"]',
    "win_probability_subtracted": 'td[data-stat="wpa_bat_neg"]',
    "average_leverage_index": 'td[data-stat="leverage_index_avg"]',
    "average_leverage_index_pitcher": 'td[data-stat="leverage_index_avg"]',
    "base_out_runs_added": 'td[data-stat="re24_bat"]',
    "strikes": 'td[data-stat="strikes_total"]',
    "innings_pitched": 'td[data-stat="IP"]',
    "earned_runs_against": 'td[data-stat="earned_run_avg"]',
    "pitches_thrown": 'td[data-stat="pitches"]',
    "strikes_thrown": 'td[data-stat="strikes_total"]',
    "strikes_contact": 'td[data-stat="strikes_contact"]',
    "strikes_swinging": 'td[data-stat="strikes_swinging"]',
    "strikes_looking": 'td[data-stat="strikes_looking"]',
    "grounded_balls": 'td[data-stat="inplay_gb_total"]',
    "fly_balls": 'td[data-stat="inplay_fb_total"]',
    "line_drives": 'td[data-stat="inplay_ld"]',
    "unknown_bat_types": 'td[data-stat="inplay_unk"]',
    "game_score": 'td[data-stat="game_score"]',
    "inherited_runners": 'td[data-stat="inherited_runners"]',
    "inherited_score": 'td[data-stat="inherited_score"]',
    "win_probability_added_pitcher": 'td[data-stat="wpa_def"]',
    "base_out_runs_saved": 'td[data-stat="re24_def"]',
    "home_runs_thrown": 'td[data-stat="HR"]',
}

PLAYER_ELEMENT_INDEX = {
    "bases_on_balls_given": 1,
    "hits_allowed": 1,
    "home_runs_allowed": 1,
    "intentional_bases_on_balls_given": 1,
    "runs_allowed": 1,
    "strikeouts": 1,
    "times_hit_player": 1,
    "average_leverage_index_pitcher": 1,
    "pitches_thrown": 1,
    "strikes_thrown": 1,
}

NATIONALITY = {
    "af": "Afghanistan",
    "as": "American Samoa",
    "aw": "Aruba",
    "au": "Australia",
    "at": "Austria",
    "bs": "Bahamas",
    "be": "Belgium",
    "bz": "Belize",
    "br": "Brazil",
    "ca": "Canada",
    "cn": "China",
    "co": "Colombia",
    "cu": "Cuba",
    "cw": "Curacao",
    "cz": "Czech Republic",
    "dk": "Denmark",
    "do": "Dominican Replubic",
    "fi": "Finland",
    "fr": "France",
    "de": "Germany",
    "gr": "Greece",
    "gu": "Guam",
    "hn": "Honduras",
    "hk": "Hong Kong",
    "id": "Indonesia",
    "ie": "Ireland",
    "it": "Italy",
    "jm": "Jamaica",
    "jp": "Japan",
    "lv": "Latvia",
    "lt": "Lithuania",
    "mx": "Mexico",
    "nl": "Netherlands",
    "ni": "Nicaragua",
    "no": "Norway",
    "pa": "Panama",
    "pe": "Peru",
    "ph": "Philippines",
    "pl": "Poland",
    "pt": "Portugal",
    "pr": "Puerto Rico",
    "ru": "Russian Federation",
    "sa": "Saudi Arabia",
    "si": "Singapore",
    "sk": "Slovakia",
    "za": "South Africa",
    "kr": "South Korea",
    "es": "Spain",
    "se": "Sweden",
    "ch": "Switzerland",
    "tw": "Taiwan",
    "us": "United States of America",
    "vi": "U.S. Virgin Islands",
    "gb": "United Kingdom",
    "ve": "Venezuela",
    "vn": "Viet Nam",
}

DOUBLE_HEADER_INDICES = {
    "time": "start time",
    "attendance": "attendance",
    "venue": "venue",
    "duration": "game duration",
}

STANDINGS_URL = "https://www.baseball-reference.com/leagues/MLB/" "%s-standings.shtml"
TEAM_STATS_URL = "https://www.baseball-reference.com/leagues/MLB/%s.shtml"

SCHEDULE_URL = "https://www.baseball-reference.com/teams/%s/" "%s-schedule-scores.shtml"

BOXSCORE_URL = "https://www.baseball-reference.com/boxes/%s.shtml"

BOXSCORES_URL = "https://www.baseball-reference.com/boxes/" "?year=%s&month=%s&day=%s"
PLAYER_URL = "https://www.baseball-reference.com/players/%s/%s.shtml"
ROSTER_URL = "https://www.baseball-reference.com/teams/%s/%s.shtml"

NIGHT = "Night"
DAY = "Day"
