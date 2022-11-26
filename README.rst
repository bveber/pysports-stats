sports: A free sports API written for python
###############################################
**Development Status: This project is no longer undergoing active development. Please consider
opening a pull request for any new features or bug fixes to be reviewed and
merged.**

.. image:: https://github.com/bveber/sports/workflows/sports%20push%20tests/badge.svg
    :target: https://github.com/bveber/sports/actions
.. image:: https://readthedocs.org/projects/pysports-stats/badge/?version=latest
    :target: https://pysports-stats.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/pysports-stats.svg
    :target: https://pypi.org/project/pysports-stats

.. contents::

sports is a free python API that pulls the stats from
www.sports-reference.com and allows them to be easily be used in python-based
applications, especially ones involving data analytics and machine learning.

sports exposes a plethora of sports information from major sports
leagues in North America, such as the MLB, NBA, College Football and Basketball,
NFL, and NHL. sports also now supports Professional Football (or
Soccer) for thousands of teams from leagues around the world. Every sport has
its own set of valid API queries ranging from the list of teams in a league, to
the date and time of a game, to the total number of wins a team has secured
during the season, and many, many more metrics that paint a more detailed
picture of how a team has performed during a game or throughout a season.

NOTE (2022-11-23): The source website has implemented traffic restrictions that 
will result in your IP being temporarily blacklisted if you exceed 20 requests 
per minute. Therefore all outgoing requests are now passed through a utility function
that ensures you will not surpass the rate limit threshold. This runtime slowdown
is most noticeable for sports with many teams. If you are trying to bulk gather data
you will need to schedule a long running job, and its recommended that you cache any 
historical data you intend to reuse.


Installation
============

TODO: This has not been released to Pypi yet, so standard pip install will not work.
But I'm keepin the documentation as a template for now. 

The easiest way to install `pysports-stats` is by downloading the latest
released binary from PyPI using PIP. For instructions on installing PIP, visit
`PyPA.io <https://pip.pypa.io/en/stable/installing/>`_ for detailed steps on
installing the package manager for your local environment.

Next, run::

    pip install pysports-stats

to download and install the latest official release of `pysports-stats` on
your machine. You now have the latest stable version of `pysports-stats`
installed and can begin using it following the examples below!

If the bleeding-edge version of `pysports-stats` is desired, clone this
repository using git and install all of the package requirements with PIP::

    git clone https://github.com/bveber/pysports-stats
    cd pysports-stats
    poetry install

Once complete, create a Python wheel for your default version of Python by
running the following command::

    poetry build

This will create a `.whl` file in the `dist` directory which can be installed
with the following command::

    pip install dist/*.whl

Examples
========

The following are a few examples showcasing how easy it can be to collect
an abundance of metrics and information from all of the tracked leagues. The
examples below are only a miniscule subset of the total number of statistics
that can be pulled using pysports-stats. TODO: Create documentation 

Get instances of all NHL teams for the 2018 season
--------------------------------------------------

.. code-block:: python

    from sports.nhl.teams import Teams

    teams = Teams(2018)

Print every NBA team's name and abbreviation
--------------------------------------------

.. code-block:: python

    from sports.nba.teams import Teams

    teams = Teams()
    for team in teams:
        print(team.name, team.abbreviation)

Get a specific NFL team's season information
--------------------------------------------

.. code-block:: python

    from sports.nfl.teams import Teams

    teams = Teams()
    lions = teams('DET')

Print the date of every game for a NCAA Men's Basketball team
-------------------------------------------------------------

.. code-block:: python

    from sports.ncaab.schedule import Schedule

    purdue_schedule = Schedule('purdue')
    for game in purdue_schedule:
        print(game.date)

Print the number of interceptions by the away team in a NCAA Football game
--------------------------------------------------------------------------

.. code-block:: python

    from sports.ncaaf.boxscore import Boxscore

    championship_game = Boxscore('2018-01-08-georgia')
    print(championship_game.away_interceptions)

Get a Pandas DataFrame of all stats for a MLB game
--------------------------------------------------

.. code-block:: python

    from sports.mlb.boxscore import Boxscore

    game = Boxscore('BOS201806070')
    df = game.dataframe

Find the number of goals a football team has scored
---------------------------------------------------

.. code-block:: python

    from sports.fb.team import Team

    tottenham = Team('Tottenham Hotspur')
    print(tottenham.goals_scored)

Documentation
=============

This repository is based on `sportsipy`. I am incredibly grateful for
the work done by Robert Clark in creating this code base. Some internal components
have been changed, but the basic interface remains the same.
Two blog posts detailing the creation and basic usage of `sportsipy` can
be found on The Medium at the following links:

- `Part 1: Creating a public sports API <https://medium.com/clarktech-sports/python-sports-analytics-made-simple-part-1-14569d6e9a86>`_
- `Part 2: Pull any sports metric in 10 lines of Python <https://medium.com/clarktech-sports/python-sports-analytics-made-simple-part-2-40e591a7f3db>`_

The second post in particular is a great guide for getting started with
`pysports-stats` and is highly recommended for anyone who is new to the
package. 

Testing
=======

Pysports-stats contains a testing suite which aims to test all major portions
of code for proper functionality. To run the test suite against your
environment, ensure all of the requirements are installed by running::

    pip install -r requirements.txt
    pip install coverage flexmock mock pycodestyle pytest pytest-cov pytest-xdist

Next, start the tests by running py.test while optionally including coverage
flags which identify the amount of production code covered by the testing
framework::

    py.test --cov=sports --cov-report term-missing tests/

If the tests were successful, it will return a green line will show a message at
the end of the output similar to the following::

    ======================= 751 passed, 72 warnings in 110.67 seconds =======================

If a test failed, it will show the number of failed and what went wrong within
the test output. If that's the case, ensure you have the latest version of code
and are in a supported environment. Otherwise, create an issue on GitHub to
attempt to get the issue resolved.

NOTE (2022-11-23): Due to traffic restriction on the source webpage the exhaustive
are unusable. They have been commented out for now, but should be replaced with a more 
sensible set of tests to validate connectivity.