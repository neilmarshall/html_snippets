from app import create_app, db
from app.models import *

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'League': League, 'Team': Team, 'Match': Match,
            'get_all_leagues': get_all_leagues, 'get_seasons_by_league': get_seasons_by_league,
            'get_matches': get_matches, 'ResultsAggregator': ResultsAggregator}
