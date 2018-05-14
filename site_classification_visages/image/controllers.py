import uuid

from flask import render_template, Blueprint, request, current_app, flash,redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from site_classification_visages.image.analyseur_image import analyser_images
from site_classification_visages.image.bd_image import add_images_to_user, load_images_for_user, delete_images_of_user

image = Blueprint('image', __name__)


@image.route('/accueil', methods=["GET", "POST"])
@login_required
def accueil():
    UPLOAD_DIR = current_app.config['UPLOAD_PHOTOS_DEST']
    types_autorises = [".jpg", ".png", ".jpeg"]

    if request.method == 'POST':
        if 'images' in request.files:
            fichiers = request.files.getlist('images')
            types_errones = []
            images_a_ajouter = []
            for f in fichiers:
                type = os.path.splitext(f.filename)[1]
                if type in types_autorises:
                    filename_unique = "{}{}".format(str(uuid.uuid4()), type)
                    f.save(os.path.join(UPLOAD_DIR, secure_filename(filename_unique)))
                    images_a_ajouter.append(filename_unique)
                else:
                    types_errones.append(type)
            if len(types_errones) > 0:
                flash('Les types \'{}\' ne sont pas acceptés'.format(types_errones), 'upload')
            else:
                add_images_to_user(images_a_ajouter, current_user.username)
            return redirect(url_for('image.accueil'))

    images = chargement_images_utilisateur(UPLOAD_DIR)

    return render_template('accueil.html', title='Accueil', images=images)


@image.route('/supprimer', methods=["POST"])
@login_required
def supprimer_images():
    UPLOAD_DIR = current_app.config['UPLOAD_PHOTOS_DEST']

    if request.method == 'POST':
        images_bd_user = load_images_for_user(current_user.username)
        fichiers = os.listdir(UPLOAD_DIR)
        for img in images_bd_user:
            if img.name in fichiers:
                os.remove(os.path.join(UPLOAD_DIR, img.name))
        delete_images_of_user(current_user.username)

    return redirect(url_for('image.accueil'))


@image.route('/prediction', methods=["POST"])
@login_required
def prediction():
    UPLOAD_DIR = current_app.config['UPLOAD_PHOTOS_DEST']
    images = chargement_images_utilisateur(UPLOAD_DIR)
    images_analysees = analyser_images(images)

    return render_template('predictions.html', title='Résultats', images=images, predictions=images_analysees)


def chargement_images_utilisateur(upload_dir):
    images_bd_user = load_images_for_user(current_user.username)
    fichiers = os.listdir(upload_dir)
    images = []
    for img in images_bd_user:
        if img.name in fichiers:
            images.append(img)
    return images
