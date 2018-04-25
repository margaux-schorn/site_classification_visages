from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login = LoginManager()


def create_app():
    """ Cette fonction permet de créer l'application Flask
        et d'initialiser les objets utilisés dans le reste de l'application,
        comme la BD et le LoginManager."""
    app = Flask(__name__, template_folder="site_classification_visages/templates")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Pour désactiver un Warning

    db.init_app(app)
    login.init_app(app)
    Bootstrap(app)

    return app