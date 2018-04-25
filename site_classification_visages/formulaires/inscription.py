from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from site_classification_visages.models import Utilisateur


class FormulaireInscription(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Inscription')

    def validate_username(self, username):
        user = Utilisateur.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Veuillez choisir un autre nom d\'utilisateur.')