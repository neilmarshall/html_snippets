import json
from flask import Blueprint, render_template, request
import app.models as models

homepage = Blueprint('homepage', __name__)

@homepage.route('/')
@homepage.route('/index')
def index():
    leagues = models.get_all_leagues()
    seasons = json.dumps({league: models.get_seasons_by_league(league) for league in leagues})
    results = None
    selected_league = None
    selected_season = None
    if request.args:
        selected_league = request.args['leagues_selector']
        selected_season = request.args['seasons_selector']
        results = models.ResultsAggregator(models.get_matches(selected_league,
            selected_season))
    return render_template('index.html', leagues=leagues, seasons=seasons,
            results=results, selected_league=selected_league,
            selected_season=selected_season)
