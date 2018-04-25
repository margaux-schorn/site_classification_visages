from flask import render_template, Blueprint, request, current_app, flash,redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

image = Blueprint('image', __name__)


@image.route('/accueil', methods=["GET", "POST"])
@login_required
def accueil():
    UPLOAD_DIR = current_app.config['UPLOAD_PHOTOS_DEST']
    types_autorises = ["jpg", "png", "jpeg"]

    # TODO Eviter qu'il y ait trop de fichiers dans le dossier d'upload

    if request.method == 'POST':
        if 'images' in request.files:
            fichiers = request.files.getlist('images')
            for f in fichiers:
                type = f.content_type
                type = type.split('/')[1]
                if type in types_autorises:
                    f.save(os.path.join(UPLOAD_DIR, secure_filename(f.filename)))
                    return redirect(url_for('image.accueil'))
                else:
                    flash('Le type \'{}\' n\'est pas accepté'.format(type), 'upload')

    fichiers = os.listdir(UPLOAD_DIR)
    images = []
    for f in fichiers:
        if not f.startswith('.'):
            images.append(os.path.join('upload/', f))

    return render_template('accueil.html', title='Accueil', images=images)