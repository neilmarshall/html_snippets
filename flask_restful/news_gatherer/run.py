from app import create_app, db
from app.resources.models import NewsRequest, NewsSource, User
from config import Config

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'NewsRequest': NewsRequest, 'NewsSource': NewsSource, 'User': User}
