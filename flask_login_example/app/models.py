from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, unique=True, nullable=False)
    identity = db.Column(db.Text)
    alignment = db.Column(db.Text)
    gender = db.Column(db.Text)
    sex = db.Column(db.Text)
    eye_colour = db.Column(db.Text)
    hair_colour = db.Column(db.Text)
    is_alive = db.Column(db.Text)
    hair_colour = db.Column(db.Text)
    is_alive = db.Column(db.Boolean)
    appearances = db.Column(db.Integer)

    def __repr__(self):
        return (f"User(username={self.username}, password_hash={self.password_hash}, "
                f"identity={self.identity}, alignment={self.alignment}, gender={self.gender}, "
                f"sex={self.sex}, eye_colour={self.eye_colour}, hair_colour={self.hair_colour}, "
                f"is_alive={self.is_alive}, hair_colour={self.hair_colour}, "
                f"is_alive={self.is_alive}, appearances={self.appearances})")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
