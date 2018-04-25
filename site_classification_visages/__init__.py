from flask_migrate import Migrate

from extensions import create_app, db, login
from site_classification_visages.image.controllers import image
from site_classification_visages.utilisateur.controllers import utilisateur

app = create_app()
app.config.from_object('config.Config')

# initialisation bd
migrate = Migrate(app, db)

# import des modèles pour que la bd puisse les détecter
from site_classification_visages import utilisateur, image
from site_classification_visages.models import Image, Utilisateur

# initialisation de l'extension de login
login.login_view = 'utilisateur.connexion'  # redirection si utilisateur non authentifié

# définition de chemins
app.config['UPLOAD_PHOTOS_DEST'] = 'site_classification_visages/static/upload/'
app.static_folder = 'site_classification_visages/static/'

# ajout des modules qui composent l'app
app.register_blueprint(utilisateur, url_prefix='/')
app.register_blueprint(image, url_prefix='/images')

