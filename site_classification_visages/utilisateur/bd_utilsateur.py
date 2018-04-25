from extensions import db
from site_classification_visages.models import Utilisateur


def obtenir_utilisateur_par_username(username):
    return Utilisateur.query.filter_by(username=username).first()


def ajouter_utilisateur(user, password):
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
