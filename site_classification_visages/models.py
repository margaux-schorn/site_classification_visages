from flask_login import UserMixin
from extensions import db, login
from werkzeug.security import generate_password_hash, check_password_hash


class Utilisateur(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    images = db.relationship('Image', backref='utilisateur', lazy='dynamic')

    def __repr__(self):
        return '<Utilisateur {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return Utilisateur.query.get(int(id))


class Image(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    user_id=db.Column(db.Integer, db.ForeignKey('utilisateur.id'))

    def __repr__(self):
        return '<Image {}>'.format(self.name)
