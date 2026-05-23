from flask import Blueprint
main_bp = Blueprint('main', __name__)

# 1. IMPORTATIONS DES OUTILS ET MODÈLES
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Post, Comment

# 2. PAGE D'ACCUEIL : Liste de tous les articles
@main_bp.route('/')
@main_bp.route('/home')
def index():
    # Récupère tous les articles du plus récent au plus ancien (.desc())
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('main/index.html', posts=posts)


# 3. CRÉATION D'UN ARTICLE (Protégé par connexion)
@main_bp.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
  if request.method == 'POST':
    title = request.form.get('title')
    content = request.form.get('content')
    
    # Validation rapide des champs du formulaire natif
    if not title or not content:
        flash("Veuillez remplir tous les champs.", "danger")
        return render_template('main/create_post.html', title="Nouvel Article")
        
    # Création de l'article lié à l'utilisateur actuellement connecté (current_user)
    post = Post(title=title, content=content, author=current_user)
    db.session.add(post)
    db.session.commit()
    
    flash("Votre article a été publié avec succès !", "success")
    return redirect(url_for('main.index'))
        
  return render_template('main/create_post.html', title="Nouvel Article")


# 4. LECTURE D'UN ARTICLE ET AJOUT DE COMMENTAIRE
@main_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    # Récupère l'article par son ID, ou renvoie une erreur 404 si introuvable
    post = Post.query.get_or_404(post_id)
    
    # Si un utilisateur connecté soumet un commentaire
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("Vous devez être connecté pour laisser un commentaire.", "danger")
            return redirect(url_for('auth.login'))
            
        comment_content = request.form.get('content')
        if comment_content:
            # Création du commentaire relié à l'article et à l'utilisateur
            comment = Comment(content=comment_content, author=current_user, post=post)
            db.session.add(comment)
            db.session.commit()
            flash("Votre commentaire a été ajouté !", "success")
            return redirect(url_for('main.post_detail', post_id=post.id))
            
    return render_template('main/post_detail.html', title=post.title, post=post)


# 5. SUPPRESSION D'UN ARTICLE (Seul l'auteur peut le faire)
@main_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Sécurité : Si l'utilisateur connecté n'est pas l'auteur de l'article, on bloque (Code 403)
    if post.author != current_user:
        abort(403)
        
    db.session.delete(post)
    db.session.commit()
    flash("L'article a été supprimé.", "success")
    return redirect(url_for('main.index'))


# NOUVEAU : Redirection magique de /admin vers /auth/admin/users
@main_bp.route('/admin')
def shortcut_admin():
    return redirect(url_for('auth.admin_users'))