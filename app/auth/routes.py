from flask import Blueprint
auth_bp = Blueprint('auth', __name__)

# 1. IMPORTATIONS DES OUTILS ET EXTENSIONS
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User

# 2. ROUTE D'INSCRIPTION (Register)
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  # Si l'utilisateur est déjà connecté, on le redirige directement vers l'accueil
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  
  # On instancie le formulaire d'inscription
  form = RegistrationForm()
  
  # Si le formulaire est soumis et valide (les critères WTForms sont respectés)
  if form.validate_on_submit():
    new_user = User(username=form.username.data, email=form.email.data)    # On crée un nouvel objet utilisateur avec les données du formulaire
    new_user.set_password(form.password.data)    # On utilise notre méthode de modèle pour hacher le mot de passe de manière sécurisée

    
    # On ajoute et on valide l'enregistrement dans notre base PostgreSQL
    db.session.add(new_user)
    db.session.commit()
    
    flash("votre compt a ete cree avec succes !!")
    return redirect(url_for('auth.login'))     # On le redirige vers la page de connexion
  
    # Si c'est une requête GET, on affiche simplement le template HTML de l'inscription
  return render_template('auth/register.html', title="Inscription", form=form)



# 3. ROUTE DE CONNEXION (Login)
@auth_bp.route('/login',methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  
  form = LoginForm()
  
  if form.validate_on_submit():
    # On cherche l'utilisateur dans PostgreSQL grâce à son adresse email
    user = User.query.filter_by(email=form.email.data).first()
    
    # Si l'utilisateur existe ET que le mot de passe correspond au hash stocké
    if user and user.check_password(form.password.data):
      login_user(user, remember=form.remember.data)       # Flask-Login ouvre officiellement la session
            
      # Gestion de la redirection "next" (si l'utilisateur essayait d'accéder à une page privée)
      next_page = request.args.get('next')
      flash(f"Ravi de vous revoir, {user.username} !", "success")
      return redirect(next_page) if next_page else redirect(url_for('main.index'))
    else:
      # En cas d'erreur, on affiche un message d'alerte générique (sécurité oblige)
      flash("Connexion échouée. Veuillez vérifier votre email et votre mot de passe.", "danger")
            
  return render_template('auth/login.html', title="Connexion", form=form)

# 4. ROUTE DE DÉCONNEXION (Logout)

@auth_bp.route('/logout')
@login_required  # Cette route est protégée : seul un utilisateur connecté peut se déconnecter
def logout():
  # Flask-Login détruit la session actuelle
  logout_user()
  flash("Vous etes deconnecterc!!")
  return redirect(url_for('main.index'))


@auth_bp.route('/admin/users')
@login_required   # Obligatoire d'être connecté
def admin_users():
  # Sécurité stricte : si l'utilisateur n'est pas admin, on bloque l'accès (Erreur 403)
  if not current_user.is_admin:
    abort(403)
    
  # Récupère tous les utilisateurs inscrits
  all_users = User.query.all()
  return render_template('auth/admin_users.html', title="Gestion Utilisateurs", users=all_users)

@auth_bp.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
  if not current_user.is_admin:
    abort(403)
      
  user_to_delete = User.query.get_or_404(user_id)
  
  # Empêche un admin de se supprimer lui-même par erreur
  if user_to_delete == current_user:
    flash("Vous ne pouvez pas supprimer votre propre compte admin !", "danger")
    return redirect(url_for('auth.admin_users'))
      
  db.session.delete(user_to_delete)
  db.session.commit() # Grâce au cascade="all, delete-orphan", tous ses articles et commentaires disparaissent aussi
  flash(f"L'utilisateur {user_to_delete.username} a été banni.", "success")
  return redirect(url_for('auth.admin_users'))


@auth_bp.route('/admin/user/<int:user_id>/make-admin', methods=['POST'])
@login_required
def make_admin(user_id):
  if not current_user.is_admin:
    abort(403)
      
  user = User.query.get_or_404(user_id)
  user.is_admin = True  # On passe l'utilisateur en admin directement en Python
  db.session.commit()   # SQLAlchemy enregistre tout seul dans PostgreSQL en arrière-plan
  
  flash(f"{user.username} est maintenant administrateur !", "success")
  return redirect(url_for('auth.admin_users'))


