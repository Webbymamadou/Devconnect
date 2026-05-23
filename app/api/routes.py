from flask import Blueprint
api_bp = Blueprint('api', __name__)

from flask import jsonify, abort
from app.models import Post

@api_bp.route('/posts,', methods=['GET'])
def get_posts():
  # On récupère tous les articles en base de données
  posts = Post.query.order_by(Post.data_posted.desc()).all()
  
# 2. ROUTE : Récupérer tous les articles au format JSON
  # On convertit notre liste d'objets Python en une liste de dictionnaires
  output = []
  for post in posts:
    post_data = {
      'id':post.id,
      'title': post.title,
      'content':post.content,
      'date_posted':post.date_posted,
      'author': post.author.username,
      'comments_count': len(post.comments),
    }
    output.append(post_data)
  
  # On utilise jsonify() pour transformer le dictionnaire Python en vrai JSON lisible par le web
  return jsonify({'posts':output})


# 3. ROUTE : Récupérer un seul article précis par son ID
@api_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
  # On récupère l'article ou on renvoie une erreur 404
  post = Post.query.get_or_404(post_id)
  
  # On récupère l'article ou on renvoie une erreur 404
  comments_list = []
  for comment in post.comments:
    comments_list.append({
      'id': comment.id,
      'content': comment.content,
      'author': comment.author.username,
      'date_posted': comment.date_posted.isoformat()
    })
    
  # Structure finale de la réponse JSON pour un article unique
  return jsonify({
      'id': post.id,
      'title': post.title,
      'content': post.content,
      'date_posted': post.date_posted.isoformat(),
      'author': post.author.username,
      'comments': comments_list
  })