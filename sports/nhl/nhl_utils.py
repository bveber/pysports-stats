from pyquery import PyQuery as pq
from sports import utils
from .constants import SEASON_PAGE_URL, PARSING_SCHEME


def _add_stats_data(teams_list, team_data_dict):
    """
    Add a team's stats row to a dictionary.

    Pass table contents and a stats dictionary of all teams to accumulate all
    stats for each team in a single variable.

    Parameters
    ----------
    teams_list : generator
        A generator of all row items in a given table.
    team_data_dict : {str: {'data': str, 'rank': int}} dictionary
        A dictionary where every key is the team's abbreviation and every value
        is another dictionary with a 'data' key which contains the string
        version of the row data for the matched team, and a 'rank' key which is
        the rank of the team.

    Returns
    -------
    dictionary
        An updated version of the team_data_dict with the passed table row
        information included.
    """
    # Teams are listed in terms of rank with the first team being #1
    rank = 1
    for team_data in teams_list:
        abbr = utils._parse_field(PARSING_SCHEME, team_data, "abbreviation")
        try:
            team_data_dict[abbr]["data"] += team_data
        except KeyError:
            team_data_dict[abbr] = {"data": team_data, "rank": rank}
        rank += 1
    return team_data_dict


def _retrieve_all_teams(year, season_page=None):
    """
    Find and create Team instances for all teams in the given season.

    For a given season, parses the specified NHL stats table and finds all
    requested stats. Each team then has a Team instance created which includes
    all requested stats and a few identifiers, such as the team's name and
    abbreviation. All of the individual Team instances are added to a list.

    Note that this method is called directly once Teams is invoked and does not
    need to be called manually.

    Parameters
    ----------
    year : string
        The requested year to pull stats from.
    teams_file : string (optional)
        Link with filename to the local season page.

    Returns
    -------
    tuple
        Returns a ``tuple`` in the format of (teams_list, year) where the
        teams_list is the PyQuery data for every team in the given season, and
        the year is the request year for the season.
    """
    team_data_dict = {}

    if not year:
        year = utils._find_year_for_season("nhl")
        # If stats for the requested season do not exist yet (as is the case
        # right before a new season begins), attempt to pull the previous
        # year's stats. If it exists, use the previous year instead.
        if not utils._url_exists(SEASON_PAGE_URL % year) and utils._url_exists(
            SEASON_PAGE_URL % str(int(year) - 1)
        ):
            year = str(int(year) - 1)
    doc = utils._pull_page(SEASON_PAGE_URL % year, season_page)
    stats = utils._get_stats_table(doc, "div#all_stats")
    advanced_stats = utils._get_stats_table(doc, "div#all_stats_adv")
    if not stats and not advanced_stats:
        utils._no_data_found()
        return None, None
    for stats_list in [stats, advanced_stats]:
        team_data_dict = _add_stats_data(stats_list, team_data_dict)
    return team_data_dict, year
