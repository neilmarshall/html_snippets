import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class League(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __repr__(self):
        return f"League(id={self.id}, name={self.name})"

class Match(db.Model):

    league_id = db.Column(db.Integer, db.ForeignKey(League.id), primary_key=True, )
    season = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return f"Match(league_id={self.league_id}, season={self.season})"


def get_seasons_by_league(session, league):
    return [season for (season,) in session.query(Match.season).filter(League.id==Match.league_id).filter(League.name==league).all()]


class TestLeague(unittest.TestCase):

    def setUp(self):
        db.create_all()
        db.session.add_all(
            [League(id=1729, name="England Premier League"),
             League(id=4769, name="France Ligue 1"),
             League(id=10257, name="Italy Serie A")])
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
              Match(league_id=10257, season="2009/2010"),
              Match(league_id=10257, season="2010/2011"),
              Match(league_id=10257, season="2011/2012"),
              Match(league_id=10257, season="2012/2013")])
        db.session.commit()
 
    def test_get_seasons_by_league(self):
        seasons = get_seasons_by_league(db.session, "England Premier League")
        self.assertEqual(seasons, ["2008/2009", "2009/2010", "2010/2011", "2011/2012", "2012/2013", "2013/2014", "2014/2015", "2015/2016"])
        seasons = get_seasons_by_league(db.session, "France Ligue 1")
        self.assertEqual(seasons, ["2010/2011", "2011/2012", "2012/2013", "2013/2014", "2014/2015", "2015/2016"])
        seasons = get_seasons_by_league(db.session, "Italy Serie A")
        self.assertEqual(seasons, ["2008/2009", "2009/2010", "2010/2011", "2011/2012", "2012/2013"])
 
 
if __name__ == '__main__':
    unittest.main()
