# importation des outils et extensions
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash , check_password_hash


# CHARGEMENT DE L'UTILISATEUR (Pour Flask-Login)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))



# LA CLASSE USER (Table des utilisateurs)
class User(db.Model, UserMixin):
  # Définit le nom réel de la table qui sera créée dans PostgreSQL
  __tablename__ = "users"
  #on definit les colones
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True , nullable=False)
  email = db.Column(db.String(120), unique=True , nullable=False)
  password_hash = db.Column(db.String(256), nullable=False)
  is_admin = db.Column(db.Boolean, default=False, nullable=False)
  
  #les relations si le compt est supprimer tout les articles sont aussi supprimer 
  posts = db.relationship('Post', backref='author',lazy=True, cascade="all, delete-orphan")
  comments = db.relationship('Comment', backref='author',lazy=True, cascade="all, delete-orphan")
  
    # MÉTHODE POUR SÉCURISER : prend un mot de passe en clair (ex: "mon_pass") et remplit la colonne password_hash
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
    
  # MÉTHODE POUR VÉRIFIER : compare un mot de passe soumis avec le code secret stocké en base de données
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
    
# LA CLASSE POST (Table des articles du blog)
class Post(db.Model):
  __tablename__ = "posts"

  id = db.Column(db.Integer , primary_key=True)
  titre = db.Column(db.Text, nullable=False)
  content = db.Column(db.Text , nullable=True)
  date_posted = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
  #cle etrangers user qui a poster
  user_id = db.Column(db.Integer, db.ForeignKey('users.id') , nullable=False) 
  
  # RELATION VIRTUELLE : permet de faire `mon_article.comments` pour lister ses commentaires
  comments = db.relationship('Comment' , backref='post', lazy=True, cascade="all, delete-orphan")
  
  
# LA CLASSE COMMENT (Table des commentaires sous les articles)
# On crée la classe Comment pour lier les avis des utilisateurs aux articles
class Comment(db.Model):
  __tablename__ = "comments"
  
  id = db.Column(db.Integer , primary_key=True)
  content = db.Column(db.Text, nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)       # Date du commentaire générée automatiquement
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  post_id = db.Column(db.Integer , db.ForeignKey('posts.id'), nullable=False)
  
  
  

