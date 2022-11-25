import mock
import pytest
from flexmock import flexmock
from os.path import join, dirname
from sports import utils
from sports.ncaaf.conferences import Conference, Conferences
from ..utils import read_file


YEAR = 2018


def mock_pyquery(url):
    if 'BAD' in url:
        return ''
    if 'acc' in url:
        html_contents = read_file('%s-acc.html' % YEAR, 'ncaaf', 'conferences')
        return html_contents
    if 'sec' in url:
        html_contents = read_file('%s-sec.html' % YEAR, 'ncaaf', 'conferences')
        return html_contents
    html_contents = read_file('%s.html' % YEAR, 'ncaaf', 'conferences')
    return html_contents


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


class TestNCAAFConferences:
    def setup_method(self):
        team_conference = {'florida-state': 'acc',
                           'boston-college': 'acc',
                           'clemson': 'acc',
                           'north-carolina-state': 'acc',
                           'syracuse': 'acc',
                           'wake-forest': 'acc',
                           'louisville': 'acc',
                           'virginia-tech': 'acc',
                           'duke': 'acc',
                           'georgia-tech': 'acc',
                           'pittsburgh': 'acc',
                           'virginia': 'acc',
                           'miami-fl': 'acc',
                           'north-carolina': 'acc',
                           'florida': 'sec',
                           'georgia': 'sec',
                           'kentucky': 'sec',
                           'missouri': 'sec',
                           'south-carolina': 'sec',
                           'vanderbilt': 'sec',
                           'tennessee': 'sec',
                           'alabama': 'sec',
                           'arkansas': 'sec',
                           'auburn': 'sec',
                           'louisiana-state': 'sec',
                           'mississippi-state': 'sec',
                           'mississippi': 'sec',
                           'texas-am': 'sec'}
        conferences_result = {
            'acc': {
                'name': 'Atlantic Coast Conference',
                'teams': {'boston-college': 'Boston College',
                    'clemson': 'Clemson',
                    'duke': 'Duke',
                    'florida-state': 'Florida State',
                    'georgia-tech': 'Georgia Tech',
                    'louisville': 'Louisville',
                    'miami-fl': 'Miami (FL)',
                    'north-carolina': 'North Carolina',
                    'north-carolina-state': 'North Carolina State',
                    'pittsburgh': 'Pitt',
                    'syracuse': 'Syracuse',
                    'virginia': 'Virginia',
                    'virginia-tech': 'Virginia Tech',
                    'wake-forest': 'Wake Forest'}
            },
            'american': {'name': 'American Athletic Conference', 'teams': {}},
            'big-12': {'name': 'Big 12 Conference', 'teams': {}},
            'big-ten': {'name': 'Big Ten Conference', 'teams': {}},
            'cusa': {'name': 'Conference USA', 'teams': {}},
            'independent': {'name': 'Independent', 'teams': {}},
            'mac': {'name': 'Mid-American Conference', 'teams': {}},
            'mwc': {'name': 'Mountain West Conference', 'teams': {}},
            'pac-12': {'name': 'Pac-12 Conference', 'teams': {}},
            'sec': {
                'name': 'Southeastern Conference',
                'teams': {'alabama': 'Alabama',
                    'arkansas': 'Arkansas',
                    'auburn': 'Auburn',
                    'florida': 'Florida',
                    'georgia': 'Georgia',
                    'kentucky': 'Kentucky',
                    'louisiana-state': 'LSU',
                    'mississippi': 'Ole Miss',
                    'mississippi-state': 'Mississippi State',
                    'missouri': 'Missouri',
                    'south-carolina': 'South Carolina',
                    'tennessee': 'Tennessee',
                    'texas-am': 'Texas A&M',
                    'vanderbilt': 'Vanderbilt'}
            },
            'sun-belt': {'name': 'Sun Belt Conference', 'teams': {}}
        }
        self.team_conference = team_conference
        self.conferences_result = conferences_result

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_conferences_integration(self, *args, **kwargs):
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return(YEAR)

        conferences = Conferences()

        assert conferences.team_conference == self.team_conference
        assert conferences.conferences == self.conferences_result

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_conferences_integration_bad_url(self, *args, **kwargs):
        with pytest.raises(ValueError):
            conferences = Conferences('BAD')

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_conference_integration_bad_url(self, *args, **kwargs):
        with pytest.raises(ValueError):
            conference = Conference('BAD')

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_conference_with_no_names_is_empty(self, *args, **kwargs):
        flexmock(Conference) \
            .should_receive('_get_team_abbreviation') \
            .and_return('')

        conference = Conference('acc')

        assert len(conference._teams) == 0

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    @mock.patch('requests.head', side_effect=mock_request)
    def test_invalid_default_year_reverts_to_previous_year(self,
                                                           *args,
                                                           **kwargs):
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return(2019)

        conferences = Conferences()

        assert conferences.team_conference == self.team_conference
        assert conferences.conferences == self.conferences_result

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    @mock.patch('requests.head', side_effect=mock_request)
    def test_invalid_conference_year_reverts_to_previous_year(self,
                                                              *args,
                                                              **kwargs):
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return(2019)

        conference = Conference('acc')

        assert len(conference._teams) == 14

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_conference_integration_bad_url(self, *args, **kwargs):
        with pytest.raises(ValueError):
            conference = Conference('BAD')

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_conferences_string_representation(self, *args, **kwargs):
        conferences = Conferences()

        assert conferences.__repr__() == 'NCAAF Conferences'

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_conference_string_representation(self, *args, **kwargs):
        conference = Conference('acc')

        assert conference.__repr__() == 'acc - NCAAF'
