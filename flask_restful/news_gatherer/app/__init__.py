from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

from app.resources.authorization import GetToken, Register
from app.resources.get_news import GetNews

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    # Enable FOREIGN KEY constraints for sqlite3
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        def _fk_pragma_on_connect(dbapi_con, con_record):
            dbapi_con.execute('pragma foreign_keys=ON')
        with app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', _fk_pragma_on_connect)
        

    migrate.init_app(app, db)

    api = Api(app)
    api.add_resource(GetNews, '/get_news')
    api.add_resource(GetToken, '/token')
    api.add_resource(Register, '/register')

    return app
