import os
from flask import current_app
from flask_login import UserMixin
from extensions import db, login
from werkzeug.security import generate_password_hash, check_password_hash


class Utilisateur(UserMixin, db.Model):
    username = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    password = db.Column(db.String(128))
    images = db.relationship('Image', backref='utilisateur', lazy='dynamic')

    def __repr__(self):
        return '<Utilisateur {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.username


@login.user_loader
def load_user(id):
    return Utilisateur.query.get(id)


class Image(db.Model):
    name = db.Column(db.String(140), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('utilisateur.username'))

    def __repr__(self):
        return '<Image {}>'.format(self.name)

    def url(self):
        return os.path.join('upload/', self.name)
