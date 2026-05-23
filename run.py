from app import create_app, db

app = create_app()

# ✅ AJOUT : On force le chargement du fichier models pour que Flask-Migrate les voie !
from app import models

if __name__ == '__main__':
  app.run(debug=True)
  # Lancement du serveur si le fichier est exécuté directement