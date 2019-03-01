from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class League(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    matches = relationship("Match", back_populates='leagues')

    def __repr__(self):
        return f"League(id={self.id}, name={self.name})"

class Match(db.Model):

    league_id = db.Column(db.Integer, ForeignKey(League.id), primary_key=True)
    season = db.Column(db.Text, primary_key=True)

    leagues = relationship("League", back_populates='matches')

    def __repr__(self):
        return f"Match(league_id={self.league_id}, season={self.season})"


def get_seasons_by_league(league):
    return [match.season for match in db.session.query(Match.season)
                                                .join(League)
                                                .filter(League.name==league)
                                                .order_by(Match.season)
                                                .distinct()]

def get_all_leagues():
    return [league.name for league in db.session.query(League.name).order_by(League.name).distinct()]
