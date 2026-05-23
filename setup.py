import os
structure = {
  "app": [
    "__init__.py",
    "models.py",
  ],
  "app/auth": [
    "__init__.py",
    "routes.py",
    "forms.py"
  ],
  "app/main": [
    "__init__.py",
    "routes.py"
  ],
  "app/api": [
    "__init__.py",
    "routes.py"
  ],
  "app/templates": [
    "base.html",
  ],
}

file_racine = [
  ".env",
  ".gitignore",
  "run.py",
  "requirements.txt"
]


def generateur_projet():
  #creation des dossiers et fichiers interne
  for folder , files in structure.items():
    os.makedirs(folder, exist_ok=True)
    print(f"Dossier cree: {folder}")
    
  
    #creation des fichiers
    for file in files:
      file_path = os.path.join(folder, file)
      with open(file_path, "w" , encoding="utf-8") as f : 
        pass
      print(f"fichier cree : {file_path}")
      
      
      
  #creation des fichier a la racine
  for file in file_racine:
    with open(file , "w" , encoding="utf-8") as f:
      pass
    print(f"fichier racine cree: {file}")
  

if __name__== "__main__":
  generateur_projet()     