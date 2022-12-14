PARSING_SCHEME = {
    "name": "a",
    "games_played": 'td[data-stat="g"]:first',
    "wins": 'td[data-stat="wins"]:first',
    "losses": 'td[data-stat="losses"]:first',
    "win_percentage": 'td[data-stat="win_loss_pct"]:first',
    "simple_rating_system": 'td[data-stat="srs"]:first',
    "strength_of_schedule": 'td[data-stat="sos"]:first',
    "conference_wins": 'td[data-stat="wins_conf"]:first',
    "conference_losses": 'td[data-stat="losses_conf"]:first',
    "home_wins": 'td[data-stat="wins_home"]:first',
    "home_losses": 'td[data-stat="losses_home"]:first',
    "away_wins": 'td[data-stat="wins_visitor"]:first',
    "away_losses": 'td[data-stat="losses_visitor"]:first',
    "points": 'td[data-stat="pts"]:first',
    "opp_points": 'td[data-stat="opp_pts"]:first',
    "minutes_played": 'td[data-stat="mp"]:first',
    "field_goals": 'td[data-stat="fg"]:first',
    "field_goal_attempts": 'td[data-stat="fga"]:first',
    "field_goal_percentage": 'td[data-stat="fg_pct"]:first',
    "three_point_field_goals": 'td[data-stat="fg3"]:first',
    "three_point_field_goal_attempts": 'td[data-stat="fg3a"]:first',
    "three_point_field_goal_percentage": 'td[data-stat="fg3_pct"]:first',
    "two_point_field_goals": 'td[data-stat="fg2"]:first',
    "two_point_field_goal_attempts": 'td[data-stat="fg2a"]:first',
    "two_point_field_goal_percentage": 'td[data-stat="fg2_pct"]:first',
    "free_throws": 'td[data-stat="ft"]:first',
    "free_throw_attempts": 'td[data-stat="fta"]:first',
    "free_throw_percentage": 'td[data-stat="ft_pct"]:first',
    "offensive_rebounds": 'td[data-stat="orb"]:first',
    "defensive_rebounds": 'td[data-stat="drb"]:first',
    "total_rebounds": 'td[data-stat="trb"]:first',
    "assists": 'td[data-stat="ast"]:first',
    "steals": 'td[data-stat="stl"]:first',
    "blocks": 'td[data-stat="blk"]:first',
    "turnovers": 'td[data-stat="tov"]:first',
    "personal_fouls": 'td[data-stat="pf"]:first',
    "points": 'td[data-stat="pts"]:first',
    "opp_minutes_played": 'td[data-stat="opp_mp"]:first',
    "opp_field_goals": 'td[data-stat="opp_fg"]:first',
    "opp_field_goal_attempts": 'td[data-stat="opp_fga"]:first',
    "opp_field_goal_percentage": 'td[data-stat="opp_fg_pct"]:first',
    "opp_three_point_field_goals": 'td[data-stat="opp_fg3"]:first',
    "opp_three_point_field_goal_attempts": 'td[data-stat="opp_fg3a"]:first',
    "opp_three_point_field_goal_percentage": 'td[data-stat="opp_fg3_pct"]:first',
    "opp_two_point_field_goals": 'td[data-stat="opp_fg2"]:first',
    "opp_two_point_field_goal_attempts": 'td[data-stat="opp_fg2a"]:first',
    "opp_two_point_field_goal_percentage": 'td[data-stat="opp_fg2_pct"]:first',
    "opp_free_throws": 'td[data-stat="opp_ft"]:first',
    "opp_free_throw_attempts": 'td[data-stat="opp_fta"]:first',
    "opp_free_throw_percentage": 'td[data-stat="opp_ft_pct"]:first',
    "opp_offensive_rebounds": 'td[data-stat="opp_orb"]:first',
    "opp_defensive_rebounds": 'td[data-stat="opp_drb"]:first',
    "opp_total_rebounds": 'td[data-stat="opp_trb"]:first',
    "opp_assists": 'td[data-stat="opp_ast"]:first',
    "opp_steals": 'td[data-stat="opp_stl"]:first',
    "opp_blocks": 'td[data-stat="opp_blk"]:first',
    "opp_turnovers": 'td[data-stat="opp_tov"]:first',
    "opp_personal_fouls": 'td[data-stat="opp_pf"]:first',
    "opp_points": 'td[data-stat="opp_pts"]:first',
    "pace": 'td[data-stat="pace"]:first',
    "offensive_rating": 'td[data-stat="off_rtg"]:first',
    "free_throw_attempt_rate": 'td[data-stat="fta_per_fga_pct"]:first',
    "three_point_attempt_rate": 'td[data-stat="fg3a_per_fga_pct"]:first',
    "true_shooting_percentage": 'td[data-stat="ts_pct"]:first',
    "total_rebound_percentage": 'td[data-stat="trb_pct"]:first',
    "assist_percentage": 'td[data-stat="ast_pct"]:first',
    "steal_percentage": 'td[data-stat="stl_pct"]:first',
    "block_percentage": 'td[data-stat="blk_pct"]:first',
    "effective_field_goal_percentage": 'td[data-stat="efg_pct"]:first',
    "turnover_percentage": 'td[data-stat="tov_pct"]:first',
    "offensive_rebound_percentage": 'td[data-stat="orb_pct"]:first',
    "free_throws_per_field_goal_attempt": 'td[data-stat="ft_rate"]:first',
    "opp_offensive_rating": 'td[data-stat="def_rtg"]:first',
    "opp_free_throw_attempt_rate": 'td[data-stat="opp_fta_per_fga_pct"]:first',
    "opp_three_point_attempt_rate": 'td[data-stat="opp_fg3a_per_fga_pct"]:first',
    "opp_true_shooting_percentage": 'td[data-stat="opp_ts_pct"]:first',
    "opp_total_rebound_percentage": 'td[data-stat="opp_trb_pct"]:first',
    "opp_assist_percentage": 'td[data-stat="opp_ast_pct"]:first',
    "opp_steal_percentage": 'td[data-stat="opp_stl_pct"]:first',
    "opp_block_percentage": 'td[data-stat="opp_blk_pct"]:first',
    "opp_effective_field_goal_percentage": 'td[data-stat="opp_efg_pct"]:first',
    "opp_turnover_percentage": 'td[data-stat="opp_tov_pct"]:first',
    "opp_offensive_rebound_percentage": 'td[data-stat="opp_orb_pct"]:first',
    "opp_free_throws_per_field_goal_attempt": 'td[data-stat="opp_ft_rate"]:first',
}

SCHEDULE_SCHEME = {
    "game": 'th[data-stat="g"]:first',
    "date": 'td[data-stat="date_game"]:first',
    "time": 'td[data-stat="time_game"]:first',
    "type": 'td[data-stat="game_type"]:first',
    "location": 'td[data-stat="game_location"]:first',
    "opponent_abbr": 'td[data-stat="opp_name"]:first',
    "opponent_name": 'td[data-stat="opp_name"]:first',
    "opponent_conference": 'td[data-stat="conf_abbr"]:first',
    "result": 'td[data-stat="game_result"]:first',
    "points_for": 'td[data-stat="pts"]:first',
    "points_against": 'td[data-stat="opp_pts"]:first',
    "overtimes": 'td[data-stat="overtimes"]:first',
    "season_wins": 'td[data-stat="wins"]:first',
    "season_losses": 'td[data-stat="losses"]:first',
    "streak": 'td[data-stat="game_streak"]:first',
    "arena": 'td[data-stat="arena"]:first',
}

BOXSCORE_SCHEME = {
    "date": 'div[class="scorebox_meta"]',
    "location": 'div[class="scorebox_meta"]',
    "away_name": 'div[class="scorebox"] div:nth-child(1) div strong a',
    "home_name": 'div[class="scorebox"] div:nth-child(2) div strong a',
    "winning_name": "",
    "winning_abbr": "",
    "losing_name": "",
    "losing_abbr": "",
    "summary": "table#line-score",
    "pace": 'td[data-stat="pace"]:first',
    "away_record": 'div#boxes div[class="table_wrapper"] h2',
    "away_minutes_played": 'tfoot td[data-stat="mp"]',
    "away_field_goals": 'tfoot td[data-stat="fg"]',
    "away_field_goal_attempts": 'tfoot td[data-stat="fga"]',
    "away_field_goal_percentage": 'tfoot td[data-stat="fg_pct"]',
    "away_two_point_field_goals": 'tfoot td[data-stat="fg2"]',
    "away_two_point_field_goal_attempts": 'tfoot td[data-stat="fg2a"]',
    "away_two_point_field_goal_percentage": 'tfoot td[data-stat="fg2_pct"]',
    "away_three_point_field_goals": 'tfoot td[data-stat="fg3"]',
    "away_three_point_field_goal_attempts": 'tfoot td[data-stat="fg3a"]',
    "away_three_point_field_goal_percentage": 'tfoot td[data-stat="fg3_pct"]',
    "away_free_throws": 'tfoot td[data-stat="ft"]',
    "away_free_throw_attempts": 'tfoot td[data-stat="fta"]',
    "away_free_throw_percentage": 'tfoot td[data-stat="ft_pct"]',
    "away_offensive_rebounds": 'tfoot td[data-stat="orb"]',
    "away_defensive_rebounds": 'tfoot td[data-stat="drb"]',
    "away_total_rebounds": 'tfoot td[data-stat="trb"]',
    "away_assists": 'tfoot td[data-stat="ast"]',
    "away_steals": 'tfoot td[data-stat="stl"]',
    "away_blocks": 'tfoot td[data-stat="blk"]',
    "away_turnovers": 'tfoot td[data-stat="tov"]',
    "away_personal_fouls": 'tfoot td[data-stat="pf"]',
    "away_points": 'tfoot td[data-stat="pts"]',
    "away_true_shooting_percentage": 'tfoot td[data-stat="ts_pct"]',
    "away_effective_field_goal_percentage": 'tfoot td[data-stat="efg_pct"]',
    "away_three_point_attempt_rate": 'tfoot td[data-stat="fg3a_per_fga_pct"]',
    "away_free_throw_attempt_rate": 'tfoot td[data-stat="fta_per_fga_pct"]',
    "away_offensive_rebound_percentage": 'tfoot td[data-stat="orb_pct"]',
    "away_defensive_rebound_percentage": 'tfoot td[data-stat="drb_pct"]',
    "away_total_rebound_percentage": 'tfoot td[data-stat="trb_pct"]',
    "away_assist_percentage": 'tfoot td[data-stat="ast_pct"]',
    "away_steal_percentage": 'tfoot td[data-stat="stl_pct"]',
    "away_block_percentage": 'tfoot td[data-stat="blk_pct"]',
    "away_turnover_percentage": 'tfoot td[data-stat="tov_pct"]',
    "away_offensive_rating": 'tfoot td[data-stat="off_rtg"]',
    "away_defensive_rating": 'tfoot td[data-stat="def_rtg"]',
    "away_ranking": 'div[class="game_summary nohover current"] tr',
    "home_record": 'div#boxes div[class="table_wrapper"] h2',
    "home_minutes_played": 'tfoot td[data-stat="mp"]',
    "home_field_goals": 'tfoot td[data-stat="fg"]',
    "home_field_goal_attempts": 'tfoot td[data-stat="fga"]',
    "home_field_goal_percentage": 'tfoot td[data-stat="fg_pct"]',
    "home_two_point_field_goals": 'tfoot td[data-stat="fg2"]',
    "home_two_point_field_goal_attempts": 'tfoot td[data-stat="fg2a"]',
    "home_two_point_field_goal_percentage": 'tfoot td[data-stat="fg2_pct"]',
    "home_three_point_field_goals": 'tfoot td[data-stat="fg3"]',
    "home_three_point_field_goal_attempts": 'tfoot td[data-stat="fg3a"]',
    "home_three_point_field_goal_percentage": 'tfoot td[data-stat="fg3_pct"]',
    "home_free_throws": 'tfoot td[data-stat="ft"]',
    "home_free_throw_attempts": 'tfoot td[data-stat="fta"]',
    "home_free_throw_percentage": 'tfoot td[data-stat="ft_pct"]',
    "home_offensive_rebounds": 'tfoot td[data-stat="orb"]',
    "home_defensive_rebounds": 'tfoot td[data-stat="drb"]',
    "home_total_rebounds": 'tfoot td[data-stat="trb"]',
    "home_assists": 'tfoot td[data-stat="ast"]',
    "home_steals": 'tfoot td[data-stat="stl"]',
    "home_blocks": 'tfoot td[data-stat="blk"]',
    "home_turnovers": 'tfoot td[data-stat="tov"]',
    "home_personal_fouls": 'tfoot td[data-stat="pf"]',
    "home_points": 'tfoot td[data-stat="pts"]',
    "home_true_shooting_percentage": 'tfoot td[data-stat="ts_pct"]',
    "home_effective_field_goal_percentage": 'tfoot td[data-stat="efg_pct"]',
    "home_three_point_attempt_rate": 'tfoot td[data-stat="fg3a_per_fga_pct"]',
    "home_free_throw_attempt_rate": 'tfoot td[data-stat="fta_per_fga_pct"]',
    "home_offensive_rebound_percentage": 'tfoot td[data-stat="orb_pct"]',
    "home_defensive_rebound_percentage": 'tfoot td[data-stat="drb_pct"]',
    "home_total_rebound_percentage": 'tfoot td[data-stat="trb_pct"]',
    "home_assist_percentage": 'tfoot td[data-stat="ast_pct"]',
    "home_steal_percentage": 'tfoot td[data-stat="stl_pct"]',
    "home_block_percentage": 'tfoot td[data-stat="blk_pct"]',
    "home_turnover_percentage": 'tfoot td[data-stat="tov_pct"]',
    "home_offensive_rating": 'tfoot td[data-stat="off_rtg"]',
    "home_defensive_rating": 'tfoot td[data-stat="def_rtg"]',
    "home_ranking": 'div[class="game_summary nohover current"] tr',
}

BOXSCORE_ELEMENT_INDEX = {
    "date": 0,
    "location": 1,
    "away_ranking": 0,
    "home_ranking": 1,
    "home_record": 1,
    "home_minutes_played": 1,
    "home_field_goals": 1,
    "home_field_goal_attempts": 1,
    "home_field_goal_percentage": 1,
    "home_two_point_field_goals": 1,
    "home_two_point_field_goal_attempts": 1,
    "home_two_point_field_goal_percentage": 1,
    "home_three_point_field_goals": 1,
    "home_three_point_field_goal_attempts": 1,
    "home_three_point_field_goal_percentage": 1,
    "home_free_throws": 1,
    "home_free_throw_attempts": 1,
    "home_free_throw_percentage": 1,
    "home_offensive_rebounds": 1,
    "home_defensive_rebounds": 1,
    "home_total_rebounds": 1,
    "home_assists": 1,
    "home_steals": 1,
    "home_blocks": 1,
    "home_turnovers": 1,
    "home_personal_fouls": 1,
    "home_points": 1,
    "home_true_shooting_percentage": 1,
    "home_effective_field_goal_percentage": 1,
    "home_three_point_attempt_rate": 1,
    "home_free_throw_attempt_rate": 1,
    "home_offensive_rebound_percentage": 1,
    "home_defensive_rebound_percentage": 1,
    "home_total_rebound_percentage": 1,
    "home_assist_percentage": 1,
    "home_steal_percentage": 1,
    "home_block_percentage": 1,
    "home_turnover_percentage": 1,
    "home_offensive_rating": 1,
    "home_defensive_rating": 1,
}

RANKINGS_SCHEME = {
    "name": 'td[data-stat="school_name"]',
    "week": 'th[data-stat="week_poll"]',
    "date": 'td[data-stat="date_poll"]',
    "rank": 'td[data-stat="rank"]',
    "previous": 'td[data-stat="rank_prev"]',
    "change": 'td[data-stat="rank_diff"]',
}

PLAYER_SCHEME = {
    "summary": '[data-template="Partials/Teams/Summary"]',
    "conference": 'td[data-stat="conf_abbr"]',
    "season": 'th[data-stat="season"]:first',
    "name": 'div[class="players"] span:first',
    "team_abbreviation": 'td[data-stat="school_name"]',
    "position": 'td[data-stat="pos"]',
    "height": 'div[class="players"] span:nth-child(1)',
    "weight": 'div[class="players"] span:nth-child(2)',
    "birth_date": 'td[data-stat=""]',
    "nationality": 'td[data-stat=""]',
    "age": "nobr",
    "games_played": 'td[data-stat="games"]',
    "games_started": 'td[data-stat="games_started"]',
    "minutes_played": 'td[data-stat="mp"]',
    "field_goals": 'td[data-stat="fg"]',
    "field_goal_attempts": 'td[data-stat="fga"]',
    "field_goal_percentage": 'td[data-stat="fg_pct"]',
    "three_pointers": 'td[data-stat="fg3"]',
    "three_point_attempts": 'td[data-stat="fg3a"]',
    "three_point_percentage": 'td[data-stat="fg3_pct"]',
    "two_pointers": 'td[data-stat="fg2"]',
    "two_point_attempts": 'td[data-stat="fg2a"]',
    "two_point_percentage": 'td[data-stat="fg2_pct"]',
    "effective_field_goal_percentage": 'td[data-stat="efg_pct"]',
    "free_throws": 'td[data-stat="ft"]',
    "free_throw_attempts": 'td[data-stat="fta"]',
    "free_throw_percentage": 'td[data-stat="ft_pct"]',
    "offensive_rebounds": 'td[data-stat="orb"]',
    "defensive_rebounds": 'td[data-stat="drb"]',
    "total_rebounds": 'td[data-stat="trb"]',
    "assists": 'td[data-stat="ast"]',
    "steals": 'td[data-stat="stl"]',
    "blocks": 'td[data-stat="blk"]',
    "turnovers": 'td[data-stat="tov"]',
    "personal_fouls": 'td[data-stat="pf"]',
    "points": 'td[data-stat="pts"]',
    "player_efficiency_rating": 'td[data-stat="per"]',
    "true_shooting_percentage": 'td[data-stat="ts_pct"]',
    "three_point_attempt_rate": 'td[data-stat="fg3a_per_fga_pct"]',
    "free_throw_attempt_rate": 'td[data-stat="fta_per_fga_pct"]',
    "points_produced": 'td[data-stat="pprod"]',
    "offensive_rebound_percentage": 'td[data-stat="orb_pct"]',
    "defensive_rebound_percentage": 'td[data-stat="drb_pct"]',
    "total_rebound_percentage": 'td[data-stat="trb_pct"]',
    "assist_percentage": 'td[data-stat="ast_pct"]',
    "steal_percentage": 'td[data-stat="stl_pct"]',
    "block_percentage": 'td[data-stat="blk_pct"]',
    "turnover_percentage": 'td[data-stat="tov_pct"]',
    "usage_percentage": 'td[data-stat="usg_pct"]',
    "offensive_win_shares": 'td[data-stat="ows"]',
    "defensive_win_shares": 'td[data-stat="dws"]',
    "win_shares": 'td[data-stat="ws"]',
    "win_shares_per_40_minutes": 'td[data-stat="ws_per_40"]',
    "offensive_box_plus_minus": 'td[data-stat="obpm"]',
    "defensive_box_plus_minus": 'td[data-stat="dbpm"]',
    "box_plus_minus": 'td[data-stat="bpm"]',
    "offensive_rating": 'td[data-stat="off_rtg"]',
    "defensive_rating": 'td[data-stat="def_rtg"]',
}

BASIC_STATS_URL = "https://www.sports-reference.com/cbb/seasons/" "%s-school-stats.html"
BASIC_OPPONENT_STATS_URL = (
    "https://www.sports-reference.com/cbb/seasons/" "%s-opponent-stats.html"
)
ADVANCED_STATS_URL = (
    "https://www.sports-reference.com/cbb/seasons/" "%s-advanced-school-stats.html"
)
ADVANCED_OPPONENT_STATS_URL = (
    "https://www.sports-reference.com/cbb/seasons/" "%s-advanced-opponent-stats.html"
)

SCHEDULE_URL = "https://www.sports-reference.com/cbb/schools/%s/" "%s-schedule.html"
BOXSCORE_URL = "https://www.sports-reference.com/cbb/boxscores/%s.html"
BOXSCORES_URL = (
    "https://www.sports-reference.com/cbb/boxscores/index.cgi?"
    "month=%s&day=%s&year=%s"
)
RANKINGS_URL = "https://www.sports-reference.com/cbb/seasons/%s-polls-old.html"
CONFERENCES_URL = "https://www.sports-reference.com/cbb/seasons/%s.html"
CONFERENCE_URL = "https://www.sports-reference.com/cbb/conferences/%s/%s.html"
PLAYER_URL = "https://www.sports-reference.com/cbb/players/%s.html"
ROSTER_URL = "https://www.sports-reference.com/cbb/schools/%s/%s.html"

NCAA_TOURNAMENT = "NCAA"
NIT_TOURNAMENT = "NIT"
CBI_TOURNAMENT = "CBI"
CIT_TOURNAMENT = "CIT"

CONFERENCE_DICT = {
    "alabama": "sec",
    "auburn": "sec",
    "mississippi": "sec",
    "mississippi-state": "sec",
    "missouri": "sec",
    "arkansas": "sec",
    "louisiana-state": "sec",
    "florida": "sec",
    "tennessee": "sec",
    "georgia": "sec",
    "kentucky": "sec",
    "texas-am": "sec",
    "vanderbilt": "sec",
    "south-carolina": "sec",
    "indiana": "big-ten",
    "iowa": "big-ten",
    "maryland": "big-ten",
    "purdue": "big-ten",
    "wisconsin": "big-ten",
    "michigan": "big-ten",
    "ohio-state": "big-ten",
    "penn-state": "big-ten",
    "illinois": "big-ten",
    "northwestern": "big-ten",
    "rutgers": "big-ten",
    "michigan-state": "big-ten",
    "nebraska": "big-ten",
    "minnesota": "big-ten",
    "iowa-state": "big-12",
    "kansas": "big-12",
    "kansas-state": "big-12",
    "texas": "big-12",
    "west-virginia": "big-12",
    "baylor": "big-12",
    "oklahoma": "big-12",
    "texas-christian": "big-12",
    "oklahoma-state": "big-12",
    "texas-tech": "big-12",
    "arizona": "pac-12",
    "arizona-state": "pac-12",
    "southern-california": "pac-12",
    "washington": "pac-12",
    "oregon-state": "pac-12",
    "ucla": "pac-12",
    "utah": "pac-12",
    "washington-state": "pac-12",
    "colorado": "pac-12",
    "oregon": "pac-12",
    "stanford": "pac-12",
    "california": "pac-12",
    "connecticut": "big-east",
    "st-johns-ny": "big-east",
    "creighton": "big-east",
    "seton-hall": "big-east",
    "xavier": "big-east",
    "marquette": "big-east",
    "providence": "big-east",
    "butler": "big-east",
    "depaul": "big-east",
    "georgetown": "big-east",
    "villanova": "big-east",
    "towson": "colonial",
    "college-of-charleston": "colonial",
    "hofstra": "colonial",
    "drexel": "colonial",
    "william-mary": "colonial",
    "north-carolina-wilmington": "colonial",
    "delaware": "colonial",
    "north-carolina-at": "colonial",
    "hampton": "colonial",
    "stony-brook": "colonial",
    "elon": "colonial",
    "monmouth": "colonial",
    "northeastern": "colonial",
    "middle-tennessee": "cusa",
    "rice": "cusa",
    "western-kentucky": "cusa",
    "florida-atlantic": "cusa",
    "alabama-birmingham": "cusa",
    "texas-el-paso": "cusa",
    "texas-san-antonio": "cusa",
    "charlotte": "cusa",
    "north-texas": "cusa",
    "florida-international": "cusa",
    "louisiana-tech": "cusa",
    "houston": "aac",
    "central-florida": "aac",
    "east-carolina": "aac",
    "memphis": "aac",
    "tulane": "aac",
    "wichita-state": "aac",
    "cincinnati": "aac",
    "southern-methodist": "aac",
    "tulsa": "aac",
    "temple": "aac",
    "south-florida": "aac",
    "kent-state": "mac",
    "ball-state": "mac",
    "toledo": "mac",
    "akron": "mac",
    "bowling-green-state": "mac",
    "central-michigan": "mac",
    "buffalo": "mac",
    "northern-illinois": "mac",
    "western-michigan": "mac",
    "ohio": "mac",
    "miami-oh": "mac",
    "eastern-michigan": "mac",
    "saint-marys-ca": "wcc",
    "san-francisco": "wcc",
    "san-diego": "wcc",
    "gonzaga": "wcc",
    "loyola-marymount": "wcc",
    "pepperdine": "wcc",
    "portland": "wcc",
    "santa-clara": "wcc",
    "brigham-young": "wcc",
    "pacific": "wcc",
    "north-carolina": "acc",
    "notre-dame": "acc",
    "virginia": "acc",
    "miami-fl": "acc",
    "virginia-tech": "acc",
    "wake-forest": "acc",
    "clemson": "acc",
    "duke": "acc",
    "north-carolina-state": "acc",
    "boston-college": "acc",
    "georgia-tech": "acc",
    "syracuse": "acc",
    "pittsburgh": "acc",
    "florida-state": "acc",
    "louisville": "acc",
    "high-point": "big-south",
    "north-carolina-asheville": "big-south",
    "campbell": "big-south",
    "charleston-southern": "big-south",
    "longwood": "big-south",
    "radford": "big-south",
    "winthrop": "big-south",
    "south-carolina-upstate": "big-south",
    "gardner-webb": "big-south",
    "presbyterian": "big-south",
    "drake": "mvc",
    "indiana-state": "mvc",
    "illinois-chicago": "mvc",
    "missouri-state": "mvc",
    "murray-state": "mvc",
    "southern-illinois": "mvc",
    "belmont": "mvc",
    "bradley": "mvc",
    "valparaiso": "mvc",
    "illinois-state": "mvc",
    "northern-iowa": "mvc",
    "evansville": "mvc",
    "samford": "southern",
    "western-carolina": "southern",
    "wofford": "southern",
    "furman": "southern",
    "citadel": "southern",
    "east-tennessee-state": "southern",
    "north-carolina-greensboro": "southern",
    "chattanooga": "southern",
    "mercer": "southern",
    "virginia-military-institute": "southern",
    "louisiana-lafayette": "sun-belt",
    "southern-mississippi": "sun-belt",
    "troy": "sun-belt",
    "james-madison": "sun-belt",
    "marshall": "sun-belt",
    "appalachian-state": "sun-belt",
    "georgia-state": "sun-belt",
    "arkansas-state": "sun-belt",
    "texas-state": "sun-belt",
    "coastal-carolina": "sun-belt",
    "georgia-southern": "sun-belt",
    "old-dominion": "sun-belt",
    "louisiana-monroe": "sun-belt",
    "south-alabama": "sun-belt",
    "quinnipiac": "maac",
    "iona": "maac",
    "niagara": "maac",
    "saint-peters": "maac",
    "mount-st-marys": "maac",
    "siena": "maac",
    "manhattan": "maac",
    "canisius": "maac",
    "marist": "maac",
    "rider": "maac",
    "fairfield": "maac",
    "denver": "summit",
    "st-thomas-mn": "summit",
    "north-dakota": "summit",
    "oral-roberts": "summit",
    "south-dakota": "summit",
    "south-dakota-state": "summit",
    "western-illinois": "summit",
    "missouri-kansas-city": "summit",
    "north-dakota-state": "summit",
    "nebraska-omaha": "summit",
    "wright-state": "horizon",
    "youngstown-state": "horizon",
    "ipfw": "horizon",
    "cleveland-state": "horizon",
    "detroit-mercy": "horizon",
    "robert-morris": "horizon",
    "milwaukee": "horizon",
    "oakland": "horizon",
    "northern-kentucky": "horizon",
    "iupui": "horizon",
    "green-bay": "horizon",
    "davidson": "atlantic-10",
    "duquesne": "atlantic-10",
    "fordham": "atlantic-10",
    "saint-louis": "atlantic-10",
    "massachusetts": "atlantic-10",
    "dayton": "atlantic-10",
    "george-washington": "atlantic-10",
    "st-bonaventure": "atlantic-10",
    "virginia-commonwealth": "atlantic-10",
    "richmond": "atlantic-10",
    "la-salle": "atlantic-10",
    "loyola-il": "atlantic-10",
    "saint-josephs": "atlantic-10",
    "george-mason": "atlantic-10",
    "rhode-island": "atlantic-10",
    "norfolk-state": "meac",
    "coppin-state": "meac",
    "maryland-eastern-shore": "meac",
    "north-carolina-central": "meac",
    "howard": "meac",
    "morgan-state": "meac",
    "delaware-state": "meac",
    "south-carolina-state": "meac",
    "boston-university": "patriot",
    "navy": "patriot",
    "bucknell": "patriot",
    "colgate": "patriot",
    "american": "patriot",
    "lehigh": "patriot",
    "army": "patriot",
    "loyola-md": "patriot",
    "holy-cross": "patriot",
    "lafayette": "patriot",
    "nevada-las-vegas": "mwc",
    "new-mexico": "mwc",
    "utah-state": "mwc",
    "nevada": "mwc",
    "san-jose-state": "mwc",
    "colorado-state": "mwc",
    "san-diego-state": "mwc",
    "air-force": "mwc",
    "boise-state": "mwc",
    "wyoming": "mwc",
    "fresno-state": "mwc",
    "cal-state-fullerton": "big-west",
    "california-davis": "big-west",
    "california-irvine": "big-west",
    "california-santa-barbara": "big-west",
    "hawaii": "big-west",
    "california-riverside": "big-west",
    "cal-state-bakersfield": "big-west",
    "long-beach-state": "big-west",
    "cal-poly": "big-west",
    "california-san-diego": "big-west",
    "cal-state-northridge": "big-west",
    "queens-nc": "atlantic-sun",
    "jacksonville": "atlantic-sun",
    "stetson": "atlantic-sun",
    "florida-gulf-coast": "atlantic-sun",
    "kennesaw-state": "atlantic-sun",
    "lipscomb": "atlantic-sun",
    "central-arkansas": "atlantic-sun",
    "north-alabama": "atlantic-sun",
    "eastern-kentucky": "atlantic-sun",
    "austin-peay": "atlantic-sun",
    "jacksonville-state": "atlantic-sun",
    "liberty": "atlantic-sun",
    "bellarmine": "atlantic-sun",
    "north-florida": "atlantic-sun",
    "wagner": "northeast",
    "sacred-heart": "northeast",
    "fairleigh-dickinson": "northeast",
    "st-francis-ny": "northeast",
    "saint-francis-pa": "northeast",
    "stonehill": "northeast",
    "long-island-university": "northeast",
    "merrimack": "northeast",
    "central-connecticut-state": "northeast",
    "montana-state": "big-sky",
    "sacramento-state": "big-sky",
    "montana": "big-sky",
    "portland-state": "big-sky",
    "weber-state": "big-sky",
    "northern-arizona": "big-sky",
    "eastern-washington": "big-sky",
    "idaho-state": "big-sky",
    "northern-colorado": "big-sky",
    "idaho": "big-sky",
    "hartford": "independent",
    "chicago-state": "independent",
    "prairie-view": "swac",
    "grambling": "swac",
    "alcorn-state": "swac",
    "bethune-cookman": "swac",
    "arkansas-pine-bluff": "swac",
    "southern": "swac",
    "florida-am": "swac",
    "texas-southern": "swac",
    "mississippi-valley-state": "swac",
    "alabama-am": "swac",
    "alabama-state": "swac",
    "jackson-state": "swac",
    "yale": "ivy",
    "cornell": "ivy",
    "harvard": "ivy",
    "princeton": "ivy",
    "pennsylvania": "ivy",
    "columbia": "ivy",
    "dartmouth": "ivy",
    "brown": "ivy",
    "southeast-missouri-state": "ovc",
    "southern-illinois-edwardsville": "ovc",
    "tennessee-state": "ovc",
    "morehead-state": "ovc",
    "tennessee-tech": "ovc",
    "lindenwood": "ovc",
    "tennessee-martin": "ovc",
    "southern-indiana": "ovc",
    "arkansas-little-rock": "ovc",
    "eastern-illinois": "ovc",
    "sam-houston-state": "wac",
    "seattle": "wac",
    "stephen-f-austin": "wac",
    "grand-canyon": "wac",
    "texas-pan-american": "wac",
    "california-baptist": "wac",
    "southern-utah": "wac",
    "tarleton-state": "wac",
    "new-mexico-state": "wac",
    "utah-valley": "wac",
    "texas-arlington": "wac",
    "dixie-state": "wac",
    "abilene-christian": "wac",
    "massachusetts-lowell": "america-east",
    "bryant": "america-east",
    "maine": "america-east",
    "binghamton": "america-east",
    "maryland-baltimore-county": "america-east",
    "new-hampshire": "america-east",
    "albany-ny": "america-east",
    "njit": "america-east",
    "vermont": "america-east",
    "texas-am-corpus-christi": "southland",
    "northwestern-state": "southland",
    "lamar": "southland",
    "southeastern-louisiana": "southland",
    "incarnate-word": "southland",
    "mcneese-state": "southland",
    "texas-am-commerce": "southland",
    "new-orleans": "southland",
    "nicholls-state": "southland",
    "houston-baptist": "southland",
}
