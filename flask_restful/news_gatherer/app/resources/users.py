from datetime import datetime, timedelta
from secrets import token_urlsafe

from werkzeug.security import check_password_hash, generate_password_hash

from app import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    token = db.Column(db.String(64))
    token_expiry = db.Column(db.DateTime)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, password_hash={self.password_hash})"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_token(self, expires_in=600):
        self.token = token_urlsafe()
        self.token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)

    requests = db.relationship('NewsRequest', lazy=True, backref='user')


class NewsSource(db.Model):

    __tablename__ = 'news_sources'

    source_id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(64), nullable=False)

    requests = db.relationship('NewsRequest', lazy=True, backref='source')


class NewsRequest(db.Model):

    __tablename__ = 'news_requests'

    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    news_source = db.Column(db.Integer, db.ForeignKey('news_sources.source_id'), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False)
