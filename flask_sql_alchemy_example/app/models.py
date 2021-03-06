from collections import namedtuple

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import aliased, relationship

db = SQLAlchemy()

# define namedtuples used
MatchResult = namedtuple('MatchResult', ['date', 'home_team', 'home_team_goals', 'away_team', 'away_team_goals'])
LeagueResult = namedtuple('LeagueResult', ['team', 'games', 'points', 'goal_difference'])


# define ORM models used
class League(db.Model):
    """ORM layer modelling the 'League' table"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __repr__(self):
        return f"League(id={self.id}, name={self.name})"


class Team(db.Model):
    """ORM layer modelling the 'Team' table"""

    team_api_id = db.Column(db.Integer, primary_key=True)
    team_long_name = db.Column(db.Text)

    def __repr__(self):
        return f"Team(team_api_id={self.team_api_id}, team_long_name={self.team_long_name})"


class Match(db.Model):
    """ORM layer modelling the 'Match' table"""

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
        return (f"Match(match_api_id={self.match_api_id}, league_id={self.league_id}, season={self.season}, date={self.date}, "
            f"home_team_api_id={self.home_team_api_id}, home_team_goal={self.home_team_goal}, "
            f"away_team_api_id={self.away_team_api_id}, away_team_goal={self.away_team_goal})")


# define functions used
def get_all_leagues():
    """Return list of all leagues for which data is held"""
    return [league.name for league in db.session.query(League.name).order_by(League.name).distinct()]


def get_seasons_by_league(league):
    """Return list of all seasons for which data is held for a specified league"""
    return [match.season for match in db.session.query(Match.season)
                                                .join(League)
                                                .filter(League.name==league)
                                                .order_by(Match.season)
                                                .distinct()]


def get_matches(league, season):
    """Return list of all matches for which data is held for a specified league and season"""
    home = aliased(Team)
    away = aliased(Team)
    return [MatchResult(*match) for match in db.session.query(Match.date, home.team_long_name, Match.home_team_goal, away.team_long_name, Match.away_team_goal)
                                              .join(League)
                                              .join(home, Match.home_team_api_id == home.team_api_id)
                                              .join(away, Match.away_team_api_id == away.team_api_id)
                                              .filter(League.name == league, Match.season == season)
                                              .order_by(Match.date, Match.match_api_id)
                                              .all()]

# define results aggregator class
class ResultsAggregator():
    """Class that aggregates match results to form a league table"""

    def __init__(self, match_results):
        self._number_of_teams = len({match.home_team for match in match_results} | {match.away_team for match in match_results})
        #import pdb; pdb.set_trace()
        self._number_of_matchdays = 2 * len(match_results) // self._number_of_teams
        self._league_results = self._process_results(match_results)

    def _process_results(self, match_results):
        # instantitate a dictionary to hold list of league results throughout the season, indexed by team
        interim_results = {}

        for match_result in match_results:

            # process results for home team
            home_team = match_result.home_team
            home_points = 3 if match_result.home_team_goals > match_result.away_team_goals else 0 if match_result.home_team_goals < match_result.away_team_goals else 1
            home_goal_difference = match_result.home_team_goals - match_result.away_team_goals
            result = self._process_team(interim_results, home_team, home_points, home_goal_difference)
            interim_results[home_team] = interim_results[home_team] + [result] if home_team in interim_results else [result]

            # process results for away team
            away_team = match_result.away_team
            away_points = {3: 0, 0: 3, 1: 1}.get(home_points)
            away_goal_difference = -home_goal_difference
            result = self._process_team(interim_results, away_team, away_points, away_goal_difference)
            interim_results[away_team] = interim_results[away_team] + [result] if away_team in interim_results else [result]

        return interim_results

    @staticmethod
    def _process_team(interim_results, team, points, goal_difference):
        if team in interim_results:
            return LeagueResult(team, 1 + interim_results[team][-1].games, points + interim_results[team][-1].points, goal_difference + interim_results[team][-1].goal_difference)
        else:
            return LeagueResult(team, 1, points, goal_difference)

    @staticmethod
    def _get_league_result_at_matchday(league_results, matchday):
        for league_result in league_results:
            if league_result.games == matchday:
                return league_result
        raise ValueError('Invalid matchday specified')

    def get_league_table_at_matchday(self, matchday):
        table = [self._get_league_result_at_matchday(league_results, matchday) for league_results in self._league_results.values()]
        return sorted(table, key=lambda result: (-result.points, -result.goal_difference, result.team.lower()))

    def get_final_league_table(self):
        return self.get_league_table_at_matchday(self._number_of_matchdays)

    @property
    def NumberOfMatchdays(self):
        return self._number_of_matchdays
