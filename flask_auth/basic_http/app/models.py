from flask_login import UserMixin

from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)


@login_manager.user_loader
def load_user(user_id):
    return User(id=1)
