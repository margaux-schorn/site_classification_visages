from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from site_classification_visages.models import Utilisateur
from site_classification_visages.formulaires import FormulaireConnexion, FormulaireInscription
from site_classification_visages.utilisateur.bd_utilsateur import obtenir_utilisateur_par_username, ajouter_utilisateur

utilisateur = Blueprint('utilisateur', __name__)


@utilisateur.route('/', methods=['GET', 'POST'])
@utilisateur.route('connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('image.accueil'))

    formulaire = FormulaireConnexion()

    if formulaire.validate_on_submit():
        user = obtenir_utilisateur_par_username(formulaire.username.data)
        if user is None or not user.check_password(formulaire.password.data):
            flash('Nom d\'utilisateur ou mot de passe invalide', 'connexion')
            return redirect(url_for('utilisateur.connexion'))
        login_user(user)

        # redirection sur la page d'où venait l'utilisateur ou celle d'accueil
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('image.accueil')
        return redirect(next_page)

    return render_template('connexion.html', title='Connexion', form=formulaire)


@utilisateur.route('inscription', methods=['GET', 'POST'])  # Pas besoin d'écrire /inscription
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('image.accueil'))

    formulaire = FormulaireInscription()

    if formulaire.validate_on_submit():
        # noinspection PyArgumentList
        user = Utilisateur(username=formulaire.username.data)
        ajouter_utilisateur(user, formulaire.password.data)
        flash('Votre compte à bien été enregistré.', 'inscription')
        return redirect(url_for('utilisateur.connexion'))

    return render_template('inscription.html', title='Inscription', form=formulaire)


@utilisateur.route('deconnexion')
@login_required  # doit se trouver après la définition de la route
def deconnexion():
    logout_user()
    return redirect(url_for('utilisateur.connexion', title='Connexion'))
