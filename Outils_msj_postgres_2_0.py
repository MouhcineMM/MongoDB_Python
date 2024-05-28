import psycopg2
from psycopg2 import sql
import pandas as pd
import time



i = input("Quel pagila voulez-vous modifier/créer ? \n")

try:
    host = "10.11.159.10"
    database = "2023_Maimouni_Almodovar_pagila" + i
    user = "admindbetu"
    password = "admindbetu"
   
    # Connexion à la base de données
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    cursor = conn.cursor()
except psycopg2.Error as e:
    print(f"Erreur lors de la connexion à la base de données : {e}")
    a = input(f"Pagila{i} n'existe pas, voulez-vous créer la base de données ? \n Répondez O / N \n")
   
    if a == "N":
        print("Annulation du programme...")
    elif a != 'N' and a != "O":
        print("Réponse non comprise \n Répondez O / N")
    else:
        # Connexion au serveur postgres
        conn = psycopg2.connect(dbname="postgres", host=host, user=user, password=password)
        conn.autocommit = True
        cursor = conn.cursor()
       
        # Remplacez "nouvelle_base_de_donnees" par le nom que vous souhaitez donner à votre base de données
        nom_nouvelle_base_de_donnees = "2023_Maimouni_Almodovar_pagila" + i
       
        # Utiliser l'objet sql.Identifier pour s'assurer que le nom de la base de données est correctement formaté
        nom_nouvelle_base_de_donnees_identifie = sql.Identifier(nom_nouvelle_base_de_donnees)
       
        # Exécuter la requête SQL CREATE DATABASE
        requete = sql.SQL("CREATE DATABASE {}").format(nom_nouvelle_base_de_donnees_identifie)
        cursor.execute(requete)
       
        # Fermer le curseur et la connexion
        cursor.close()
        conn.close()
        time.sleep(5)
        print(f"Base de données {nom_nouvelle_base_de_donnees} créée avec succès")

        # Reconnecter à la nouvelle base de données
        database = "2023_Maimouni_Almodovar_pagila" + i
        conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        cursor = conn.cursor()

        # Création des tables et insertion de données
        cursor.execute("""
            CREATE TABLE public.film (
                film_id integer NOT NULL,
                title text NOT NULL,
                description text,
                language_id integer NOT NULL,
                original_language_id integer
            );
            ALTER TABLE public.film OWNER TO postgres;
           
            CREATE TABLE public.actor (
                actor_id integer NOT NULL,
                first_name text NOT NULL,
                last_name text NOT NULL
            );
            ALTER TABLE public.actor OWNER TO postgres;
           
            CREATE TABLE public.film_actor (
                actor_id integer NOT NULL,
                film_id integer NOT NULL
            );
            ALTER TABLE public.film_actor OWNER TO postgres;
        """)

        # Valider les changements
        conn.commit()

# Supprimer les données existantes si l'utilisateur le souhaite
r = input(f"Voulez-vous écraser la base de données pagila{i} ? Répondez O / N \n")
if r == "N":
    print("Annulation du programme...")
elif r != 'N' and r != "O":
    print("Réponse non comprise \n Répondez O / N")
else:
    cursor.execute("DELETE FROM actor")
    cursor.execute("DELETE FROM film")
    cursor.execute("DELETE FROM film_actor")

    # Valider les changements
    conn.commit()

    # Chargement des données depuis les fichiers CSV
    actor = pd.read_csv('actor'+i+'.csv', sep=',')
    film_actor = pd.read_csv('film_actor'+i+'.csv', sep=',')
    film = pd.read_csv('film'+i+'.csv', sep=',')

    # Insertion des données dans les tables
    for ligne in range(0, len(actor)):
        actor_id = actor["actor_id"][ligne]
        first_name = actor["first_name"][ligne]
        last_name = actor["last_name"][ligne]
        requete = f"INSERT INTO actor VALUES ({actor_id}, '{first_name}', '{last_name}')"
        cursor.execute(requete)
        conn.commit()

    for ligne in range(0, len(film_actor)):
        actor_id = film_actor["actor_id"][ligne]
        film_id = film_actor["film_id"][ligne]
        requete = f"INSERT INTO film_actor VALUES ({actor_id}, {film_id})"
        cursor.execute(requete)
        conn.commit()

    for ligne in range(0, len(film)):
        film_id = film["film_id"][ligne]
        title = film["title"][ligne]
        description = film["description"][ligne]
        language_id = film["language_id"][ligne]
        original_language_id = film["original_language_id"][ligne]

        if pd.isna(original_language_id):
            original_language_id = 'NULL'

        requete = f"INSERT INTO film VALUES ({film_id}, '{title}', '{description}', {language_id}, {original_language_id})"
        cursor.execute(requete)
        conn.commit()

    print(f"Données insérées dans {database} avec succès.")

# Fermer la connexion à la fin du programme
conn.close()