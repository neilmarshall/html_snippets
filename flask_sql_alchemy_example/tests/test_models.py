import unittest
from app import app, db
from app.models import League, Match, get_seasons_by_league, get_all_leagues

class TestDBFunctions(unittest.TestCase):

    app_config = None

    def setUp(self):
        self.app_config = app.config['SQLALCHEMY_DATABASE_URI']
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        db.session.execute('PRAGMA foreign_keys = ON;')
        db.create_all()
        db.session.add_all(
            [League(id=1729, name="England Premier League"),
             League(id=4769, name="France Ligue 1"),
             League(id=10257, name="Italy Serie A"),
             League(id=8257, name="Italy Serie A"),
             League(id=17809, name="Germany 1. Bundesliga")])
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
 
 
if __name__ == '__main__':
    unittest.main()
