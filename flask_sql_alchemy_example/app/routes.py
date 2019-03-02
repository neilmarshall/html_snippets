import json
from flask import render_template, request
from app import app
import app.models as models

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    leagues = models.get_all_leagues()
    seasons = json.dumps({league: models.get_seasons_by_league(league) for league in leagues})
    results = None
    selected_league = None
    selected_season = None
    if request.method == 'POST':
        selected_league = request.form['leagues_selector']
        selected_season = request.form['seasons_selector']
        results = models.ResultsAggregator(models.get_matches(selected_league,
            selected_season))
    return render_template('index.html', leagues=leagues, seasons=seasons,
            results=results, selected_league=selected_league,
            selected_season=selected_season)
