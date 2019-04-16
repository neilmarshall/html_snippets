import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_SCHEME') + \
            os.path.abspath(os.environ.get('SQLALCHEMY_DATABASE_RELATIVE_PATH'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
