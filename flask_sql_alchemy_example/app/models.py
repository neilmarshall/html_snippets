from app import db

class League(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __repr__(self):
        return f"League(id={self.id}, name={self.name})"

class Match(db.Model):

    league_id = db.Column(db.Integer, primary_key=True, )
    season = db.Column(db.Text, primary_key=True)

    def __repr__(self):
        return f"Match(league_id={self.league_id}, season={self.season})"


def get_seasons_by_league(league):
    return [season for (season,) in db.session.query(Match.season)
                                              .filter(League.id==Match.league_id)
                                              .filter(League.name==league)
                                              .distinct()]
