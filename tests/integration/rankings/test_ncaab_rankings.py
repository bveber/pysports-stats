import mock
import pytest
from flexmock import flexmock
from os.path import join, dirname
from sports import utils
from sports.ncaab.rankings import Rankings
from ..utils import read_file
from .utils import (
    NCAAB_RESULTS_COMPLETE, 
    NCAAB_CURRENT, 
    NCAAB_CURRENT_EXTENDED
)
from urllib.error import HTTPError


YEAR = 2018


def mock_pyquery(url):
    if 'BAD' in url:
        raise HTTPError('BAD', 404, 'HTTP Error 404: Not Found', None, None)
    html_contents = read_file('%s-polls.html' % YEAR, 'ncaab', 'rankings')
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


class TestNCAABRankings:
    def setup_method(self):
        self.current_extended = NCAAB_CURRENT_EXTENDED
        self.current = NCAAB_CURRENT
        self.complete = NCAAB_RESULTS_COMPLETE

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_rankings_integration(self, *args, **kwargs):
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return(YEAR)

        rankings = Rankings()

        assert rankings.current_extended == self.current_extended
        assert rankings.current == self.current
        assert rankings.complete == self.complete

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_rankings_integration_bad_url(self, *args, **kwargs):
        with pytest.raises(ValueError):
            rankings = Rankings('BAD')

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    @mock.patch('requests.head', side_effect=mock_request)
    def test_invalid_default_year_reverts_to_previous_year(self,
                                                           *args,
                                                           **kwargs):
        flexmock(utils) \
            .should_receive('_find_year_for_season') \
            .and_return(2019)

        rankings = Rankings()

        assert rankings.current_extended == self.current_extended
        assert rankings.current == self.current
        assert rankings.complete == self.complete

    @mock.patch('sports.utils._rate_limit_pq', side_effect=mock_pyquery)
    def test_rankings_string_representation(self, *args, **kwargs):
        rankings = Rankings()

        assert rankings.__repr__() == 'NCAAB Rankings'
