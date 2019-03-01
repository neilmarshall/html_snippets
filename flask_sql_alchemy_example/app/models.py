from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class League(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __repr__(self):
        return f"League(id={self.id}, name={self.name})"


class Team(db.Model):

    team_api_id = db.Column(db.Integer, primary_key=True)
    team_long_name = db.Column(db.Text)

    def __repr__(self):
        return f"Team(team_api_id={self.team_api_id}, team_long_name={self.team_long_name})"


class Match(db.Model):

    match_api_id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, ForeignKey(League.id))
    season = db.Column(db.Text)
    date = db.Column(db.Text)
    home_team_api_id = db.Column(db.Integer, ForeignKey(Team.team_api_id))
    home_team_goal = db.Column(db.Integer)
    away_team_api_id = db.Column(db.Integer, ForeignKey(Team.team_api_id))
    away_team_goal = db.Column(db.Integer)

    leagues = relationship("League", foreign_keys=[league_id])
    home_team_api_ids = relationship("Team", foreign_keys=[home_team_api_id])
    away_team_api_ids = relationship("Team", foreign_keys=[away_team_api_id])

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


def get_matches(league, season):
    return []
