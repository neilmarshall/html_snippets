import json
from flask import Blueprint, render_template, request, url_for
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
    selected_matchday = None
    prev_url = None
    next_url = None
    if request.args:
        selected_league = request.args['leagues_selector']
        selected_season = request.args['seasons_selector']
        results = models.ResultsAggregator(models.get_matches(selected_league, selected_season))
        if 'selected_matchday' not in request.args:
            selected_matchday = results.NumberOfMatchdays
        else:
            selected_matchday = int(request.args['selected_matchday'])
        prev_url = url_for('homepage.index', leagues_selector=selected_league, seasons_selector=selected_season,
            selected_matchday=selected_matchday - 1) if selected_matchday > 1 else None
        next_url = url_for('homepage.index', leagues_selector=selected_league, seasons_selector=selected_season,
            selected_matchday=selected_matchday + 1) if selected_matchday < results.NumberOfMatchdays else None
    return render_template('index.html', leagues=leagues, seasons=seasons,
            selected_league=selected_league, selected_season=selected_season,
            results=results.get_league_table_at_matchday(selected_matchday) if results else None,
            prev_url=prev_url, next_url=next_url)
