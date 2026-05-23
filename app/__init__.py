from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# charger le ficher .env
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
  app = Flask(__name__)
  

  # Configurations depuis le .env
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  # Initialisation des outils

  db.init_app(app)
  login_manager.init_app(app)
  migrate.init_app(app, db)


  login_manager.login_view = 'auth.login'


  # Enregistrement des Blueprints (directions)
  from app.auth.routes import auth_bp
  from app.main.routes import main_bp
  from app.api.routes import api_bp

  app.register_blueprint(auth_bp, url_prefixe='/auth')
  app.register_blueprint(main_bp)
  app.register_blueprint(api_bp, url_prefixe='/api')

  return app



