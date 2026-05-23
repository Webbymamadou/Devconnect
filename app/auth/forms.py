# On importe les composants de base pour fabriquer un formulaire
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

# 1. FORMULAIRE D'INSCRIPTION (Registration)
class RegistrationForm(FlaskForm):
  username = StringField("Nom d utilisateur", validators=[
    DataRequired(message="Ce champ est obligatoire."),
    Length(min=2, max=50, message="Le pseudo doit contenir entre 2 et 50 caractères.")
  ])
  
  email = StringField("Adresse Email", validators=[
    DataRequired(message="L email est obligatoire"),
    Email(message="Veuillez saisir votre adresse email.")
  ])
  
  password = PasswordField("mot de passe", validators=[
    DataRequired(message="Le mot de passe est obligatoire."),
    Length(min=6, message="Le mot de passe doit contenir au moins 6 caracteres.")
  ])
  
  confirm_password = PasswordField("Confirmer le mot de passe", validators=[
    DataRequired(message="veuillez confirmer votre de passe."),
    EqualTo('password', message="Les mot de passe ne correspont pas.")
  ])
  
  # Bouton de validation
  submit = SubmitField("S'inscrire")
  
  # VÉRIFICATION : Empêcher d'utiliser un pseudo déjà pris en base de données
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError("Ce nom d utilisateur exist deja.")
  
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError("cette email exist deja.")

# 2. FORMULAIRE DE CONNEXION (Login)
class LoginForm(FlaskForm):
  email = StringField(message="Adresse Email", validators=[
    DataRequired(message="Le mot de passe est obligatoire.")
  ])
  
  password = PasswordField("Mot de passe", validators=[
   DataRequired("Le mot de passe est obligatoire")
  ])
  
  remember = BooleanField("Se souvenir de moi")
  # Bouton de validation
  submit = SubmitField("Se connecter")

