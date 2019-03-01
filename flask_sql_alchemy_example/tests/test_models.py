from collections import namedtuple
import unittest
from app import app, db
from app.models import League, Match, Team, get_all_leagues, get_matches, get_seasons_by_league

class TestGetSeasonsAndLeagues(unittest.TestCase):

    app_config = None

    def setUp(self):
        # set up in-memory database
        self.app_config = app.config['SQLALCHEMY_DATABASE_URI']
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        db.session.execute('PRAGMA foreign_keys = ON;')
        db.create_all()

        # add leagues
        db.session.add_all(
            [League(id=1729, name="England Premier League"),
             League(id=4769, name="France Ligue 1"),
             League(id=10257, name="Italy Serie A"),
             League(id=8257, name="Italy Serie A"),
             League(id=17809, name="Germany 1. Bundesliga")])

        # add matches
        db.session.add_all(
             [Match(league_id=1729, season="2008/2009"),
              Match(league_id=1729, season="2009/2010"),
              Match(league_id=1729, season="2010/2011"),
              Match(league_id=1729, season="2011/2012"),
              Match(league_id=1729, season="2012/2013"),
              Match(league_id=1729, season="2013/2014"),
              Match(league_id=1729, season="2014/2015"),
              Match(league_id=1729, season="2015/2016"),
              Match(league_id=4769, season="2010/2011"),
              Match(league_id=4769, season="2011/2012"),
              Match(league_id=4769, season="2012/2013"),
              Match(league_id=4769, season="2013/2014"),
              Match(league_id=4769, season="2014/2015"),
              Match(league_id=4769, season="2015/2016"),
              Match(league_id=10257, season="2008/2009"),
              Match(league_id=10257, season="2010/2011"),
              Match(league_id=10257, season="2009/2010"),  # note order has been deliberately switched to check function returns sorted list
              Match(league_id=10257, season="2011/2012"),
              Match(league_id=10257, season="2012/2013")])
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        app.config['SQLALCHEMY_DATABASE_URI'] = self.app_config
 
    def test_get_seasons_by_league(self):
        seasons = get_seasons_by_league("England Premier League")
        self.assertEqual(seasons, ["2008/2009", "2009/2010", "2010/2011", "2011/2012", "2012/2013", "2013/2014", "2014/2015", "2015/2016"])
        seasons = get_seasons_by_league("France Ligue 1")
        self.assertEqual(seasons, ["2010/2011", "2011/2012", "2012/2013", "2013/2014", "2014/2015", "2015/2016"])
        seasons = get_seasons_by_league("Italy Serie A")
        self.assertEqual(seasons, ["2008/2009", "2009/2010", "2010/2011", "2011/2012", "2012/2013"])

    def test_get_all_leagues(self):
        countries = get_all_leagues()
        self.assertEqual(countries, ["England Premier League", "France Ligue 1", "Germany 1. Bundesliga", "Italy Serie A"])


class TestGetMatches(unittest.TestCase):

    app_config = None

    def setUp(self):
        # set up in-memory database
        self.app_config = app.config['SQLALCHEMY_DATABASE_URI']
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        db.session.execute('PRAGMA foreign_keys = ON;')
        db.create_all()

        # add leagues
        db.session.add(League(id=1729, name="England Premier League"))
        db.session.add(League(id=15688, name="Poland Ekstraklasa"))
        db.session.commit()

        # add teams
        db.session.add_all(
            [Team(team_api_id=8197, team_long_name="Leicester"),
             Team(team_api_id=8472, team_long_name="Sunderland"),
             Team(team_api_id=8659, team_long_name="West Bromwich Albion"),
             Team(team_api_id=8667, team_long_name="Hull"),
             Team(team_api_id=8668, team_long_name="Everton"),
             Team(team_api_id=8678, team_long_name="Bournemouth"),
             Team(team_api_id=9825, team_long_name="Arsenal"),
             Team(team_api_id=9826, team_long_name="Crystal Palace"),
             Team(team_api_id=10003, team_long_name="Swansea"),
             Team(team_api_id=10172, team_long_name="Queens Park Rangers"),
             Team(team_api_id=10194, team_long_name="Stoke"),
             Team(team_api_id=10252, team_long_name="Aston Villa"),
             Team(team_api_id=10260, team_long_name="Manchester United"),
             Team(team_api_id=8023, team_long_name="Pogon Szczecin"),
             Team(team_api_id=8033, team_long_name="Podbeskidzie Bielsko-Biala")])
        db.session.commit()

        # add matches
        db.session.add_all(
            [Match(match_api_id=1723982, league_id=1729, season="2014/2015", date="2014-08-16 00:00:00",
                 home_team_api_id=9825, home_team_goal=2, away_team_api_id=9826, away_team_goal=1),
             Match(match_api_id=1723984, league_id=1729, season="2014/2015", date="2014-08-16 00:00:00",
                 home_team_api_id=8197, home_team_goal=2, away_team_api_id=8668, away_team_goal=2),
             Match(match_api_id=1723986, league_id=1729, season="2014/2015", date="2014-08-16 00:00:00",
                 home_team_api_id=10260, home_team_goal=1, away_team_api_id=10003, away_team_goal=2),
             Match(match_api_id=1723988, league_id=1729, season="2014/2015", date="2014-08-16 00:00:00",
                 home_team_api_id=10172, home_team_goal=0, away_team_api_id=8667, away_team_goal=1),
             Match(match_api_id=1723989, league_id=1729, season="2014/2015", date="2014-08-16 00:00:00",
                 home_team_api_id=10194, home_team_goal=0, away_team_api_id=10252, away_team_goal=1),
             Match(match_api_id=1723990, league_id=1729, season="2014/2015", date="2014-08-16 00:00:00",
                 home_team_api_id=8659, home_team_goal=2, away_team_api_id=8472, away_team_goal=2),
             Match(match_api_id=1987033, league_id=1729, season="2015/2016", date="2015-08-08 00:00:00",  # right league, wrong season should be excluded from query
                 home_team_api_id=8678, home_team_goal=0, away_team_api_id=10252, away_team_goal=1),
             Match(match_api_id=1722098, league_id=15688, season="2014/2015", date="2014-07-18 00:00:00",  # right season, wrong league - should be excluded from query
                 home_team_api_id=8033, home_team_goal=2, away_team_api_id=8023, away_team_goal=3)])
        db.session.commit()

    def tearDown(self):
        db.drop_all()
        app.config['SQLALCHEMY_DATABASE_URI'] = self.app_config
 
    def test_get_matches(self):
        MatchResult = namedtuple('MatchResult', ['date', 'home_team', 'home_team_goals', 'away_team', 'away_team_goals'])
        actual_results = get_matches("England Premier League", "2014/2015")
        expected_results = [MatchResult(date="2014-08-16 00:00:00", home_team="Arsenal", home_team_goals=2, away_team="Crystal Palace", away_team_goals=1),
                            MatchResult(date="2014-08-16 00:00:00", home_team="Leicester", home_team_goals=2, away_team="Everton", away_team_goals=2),
                            MatchResult(date="2014-08-16 00:00:00", home_team="Manchester United", home_team_goals=1, away_team="Swansea", away_team_goals=2),
                            MatchResult(date="2014-08-16 00:00:00", home_team="Queens Park Rangers", home_team_goals=0, away_team="Hull", away_team_goals=1),
                            MatchResult(date="2014-08-16 00:00:00", home_team="Stoke", home_team_goals=0, away_team="Aston Villa", away_team_goals=1),
                            MatchResult(date="2014-08-16 00:00:00", home_team="West Bromwich Albion", home_team_goals=2, away_team="Sunderland", away_team_goals=2)]
        self.assertEqual(actual_results, expected_results)
 

if __name__ == '__main__':
    unittest.main()

"""
  SELECT league_id, home.match_api_id, date, home.team_long_name, home_team_goal, away.team_long_name, away_team_goal
    FROM (SELECT match_api_id, date, team_long_name, home_team_goal, season, league_id
            FROM Match
            JOIN Team
              ON Match.home_team_api_id == Team.team_api_id) AS home
    JOIN (SELECT match_api_id, team_long_name, away_team_goal
            FROM Match
            JOIN Team
              ON Match.away_team_api_id == Team.team_api_id) AS away
      ON home.match_api_id == away.match_api_id
   WHERE season == "2014/2015" AND league_id <> 1729
ORDER BY date
   LIMIT 5;
"""
