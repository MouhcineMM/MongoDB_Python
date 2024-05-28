# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 21:57:37 2024

@author: eddin
"""


while True:
    reponse = input("""Que voulez-vous faire ?
                
    1 : Mettre à jour une base de données pagila dans Postgres
    2 : Mettre à jour la base de données film_actor dans MongoDB
    3 : Mettre à jour une base de données pagila dans Postgres et la base de données film_actor dans MongoDB
    4 : Insérer une donnée dans la base de données film_actor dans MongoDB
    
    Répondez avec '1', '2', '3', '4' ou '5': """)
    
    if reponse in ['1', '2', '3', '4','5']:
        break
    else:
        print("Veuillez entrer une réponse valide (1, 2, 3 ou 4 ou 5).")  
        
        
        
repertoire = input("Indiqué votre répertoire de travail:\n")
repertoire = repertoire.replace("\\", "/")

if reponse == "1":
    with open(repertoire+"/Outils_msj_postgres_2_0.py", 'r', encoding='utf-8') as file:
        # Lire le contenu du fichier
        code = file.read()
        # Exécuter le code du fichier
        exec(code)


if reponse == "2":
    with open(repertoire+"/pg_to_mongo.py", 'r', encoding='utf-8') as file:
        # Lire le contenu du fichier
        code = file.read()
        # Exécuter le code du fichier
        exec(code)


if reponse == "3":
    with open(repertoire+"/Outils_msj_postgres_2_0.py", 'r', encoding='utf-8') as file:
        # Lire le contenu du fichier
        code = file.read()
        # Exécuter le code du fichier
        exec(code)
        
    with open(repertoire+"/pg_to_mongo.py", 'r', encoding='utf-8') as file:
        # Lire le contenu du fichier
        code = file.read()
        # Exécuter le code du fichier
        exec(code)
        
if reponse == "5":
    with open(repertoire+"/Mission_5.py", 'r', encoding='utf-8') as file:
        # Lire le contenu du fichier
        code = file.read()
        # Exécuter le code du fichier
        exec(code)
