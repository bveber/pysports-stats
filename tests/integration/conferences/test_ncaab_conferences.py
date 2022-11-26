import mock
import pytest
from flexmock import flexmock
from os.path import join, dirname
from sports import utils
from sports.ncaab.conferences import Conference, Conferences
from ..utils import read_file


YEAR = 2018


def mock_pyquery(url):
    if "BAD" in url:
        return ""
    if "big-12" in url:
        html_contents = read_file("%s-big-12.html" % YEAR, "ncaab", "conferences")
        return html_contents
    if "big-east" in url:
        html_contents = read_file("%s-big-east.html" % YEAR, "ncaab", "conferences")
        return html_contents
    html_contents = read_file("%s.html" % YEAR, "ncaab", "conferences")
    return html_contents


def mock_request(url):
    class MockRequest:
        def __init__(self, html_contents, status_code=200):
            self.status_code = status_code
            self.html_contents = html_contents
            self.text = html_contents

    if str(YEAR) in url:
        return MockRequest("good")
    else:
        return MockRequest("bad", status_code=404)


class TestNCAABConferences:
    def setup_method(self):
        team_conference = {
            "baylor": "big-12",
            "butler": "big-east",
            "creighton": "big-east",
            "depaul": "big-east",
            "georgetown": "big-east",
            "iowa-state": "big-12",
            "kansas": "big-12",
            "kansas-state": "big-12",
            "marquette": "big-east",
            "oklahoma": "big-12",
            "oklahoma-state": "big-12",
            "providence": "big-east",
            "seton-hall": "big-east",
            "st-johns-ny": "big-east",
            "texas": "big-12",
            "texas-christian": "big-12",
            "texas-tech": "big-12",
            "villanova": "big-east",
            "west-virginia": "big-12",
            "xavier": "big-east",
        }
        conferences_result = {
            "aac": {"name": "American Athletic Conference", "teams": {}},
            "acc": {"name": "Atlantic Coast Conference", "teams": {}},
            "america-east": {"name": "America East Conference", "teams": {}},
            "atlantic-10": {"name": "Atlantic 10 Conference", "teams": {}},
            "atlantic-sun": {"name": "Atlantic Sun Conference", "teams": {}},
            "big-12": {
                "name": "Big 12 Conference",
                "teams": {
                    "baylor": "Baylor",
                    "iowa-state": "Iowa State",
                    "kansas": "Kansas",
                    "kansas-state": "Kansas State",
                    "oklahoma": "Oklahoma",
                    "oklahoma-state": "Oklahoma State",
                    "texas": "Texas",
                    "texas-christian": "TCU",
                    "texas-tech": "Texas Tech",
                    "west-virginia": "West Virginia",
                },
            },
            "big-east": {
                "name": "Big East Conference",
                "teams": {
                    "butler": "Butler",
                    "creighton": "Creighton",
                    "depaul": "DePaul",
                    "georgetown": "Georgetown",
                    "marquette": "Marquette",
                    "providence": "Providence",
                    "seton-hall": "Seton Hall",
                    "st-johns-ny": "St. John's (NY)",
                    "villanova": "Villanova",
                    "xavier": "Xavier",
                },
            },
            "big-sky": {"name": "Big Sky Conference", "teams": {}},
            "big-south": {"name": "Big South Conference", "teams": {}},
            "big-ten": {"name": "Big Ten Conference", "teams": {}},
            "big-west": {"name": "Big West Conference", "teams": {}},
            "colonial": {"name": "Colonial Athletic Association", "teams": {}},
            "cusa": {"name": "Conference USA", "teams": {}},
            "horizon": {"name": "Horizon League", "teams": {}},
            "ivy": {"name": "Ivy League", "teams": {}},
            "maac": {"name": "Metro Atlantic Athletic Conference", "teams": {}},
            "mac": {"name": "Mid-American Conference", "teams": {}},
            "meac": {"name": "Mid-Eastern Athletic Conference", "teams": {}},
            "mvc": {"name": "Missouri Valley Conference", "teams": {}},
            "mwc": {"name": "Mountain West Conference", "teams": {}},
            "northeast": {"name": "Northeast Conference", "teams": {}},
            "ovc": {"name": "Ohio Valley Conference", "teams": {}},
            "pac-12": {"name": "Pac-12 Conference", "teams": {}},
            "patriot": {"name": "Patriot League", "teams": {}},
            "sec": {"name": "Southeastern Conference", "teams": {}},
            "southern": {"name": "Southern Conference", "teams": {}},
            "southland": {"name": "Southland Conference", "teams": {}},
            "summit": {"name": "Summit League", "teams": {}},
            "sun-belt": {"name": "Sun Belt Conference", "teams": {}},
            "swac": {"name": "Southwest Athletic Conference", "teams": {}},
            "wac": {"name": "Western Athletic Conference", "teams": {}},
            "wcc": {"name": "West Coast Conference", "teams": {}},
        }
        self.team_conference = team_conference
        self.conferences_result = conferences_result

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_conferences_integration(self, *args, **kwargs):
        flexmock(utils).should_receive("_find_year_for_season").and_return(YEAR)

        conferences = Conferences()

        assert conferences.team_conference == self.team_conference
        assert conferences.conferences == self.conferences_result

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_conferences_integration_bad_url(self, *args, **kwargs):
        with pytest.raises(ValueError):
            conferences = Conferences("BAD")

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_conference_integration_bad_url(self, *args, **kwargs):
        with pytest.raises(ValueError):
            conference = Conference("BAD")

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_conference_with_no_names_is_empty(self, *args, **kwargs):
        flexmock(Conference).should_receive("_get_team_abbreviation").and_return("")

        conference = Conference("big-12")

        assert len(conference._teams) == 0

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    @mock.patch("requests.head", side_effect=mock_request)
    def test_invalid_default_year_reverts_to_previous_year(self, *args, **kwargs):
        flexmock(utils).should_receive("_find_year_for_season").and_return(2019)

        conferences = Conferences()

        assert conferences.team_conference == self.team_conference
        assert conferences.conferences == self.conferences_result

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    @mock.patch("requests.head", side_effect=mock_request)
    def test_invalid_conference_year_reverts_to_previous_year(self, *args, **kwargs):
        flexmock(utils).should_receive("_find_year_for_season").and_return(2019)

        conference = Conference("big-12")

        assert len(conference._teams) == 10

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_conferences_string_representation(self, *args, **kwargs):
        conferences = Conferences()

        assert conferences.__repr__() == "NCAAB Conferences"

    @mock.patch("sports.utils._rate_limit_pq", side_effect=mock_pyquery)
    def test_conference_string_representation(self, *args, **kwargs):
        conference = Conference("big-12")

        assert conference.__repr__() == "big-12 - NCAAB"
