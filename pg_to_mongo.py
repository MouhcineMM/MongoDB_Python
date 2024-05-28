import psycopg2
from psycopg2 import sql
import pandas as pd
import json
from pymongo import MongoClient


i =input("Quel pagila faut-il mettre à jour :\n")


# Informations de connexion à la base de données
db_config = {
    'host': '10.11.159.10',
    'database': '2023_Maimouni_Almodovar_pagila'+str(i),
    'user': 'admindbetu',
    'password': 'admindbetu',
    'port': '5432',  # Port par défaut pour PostgreSQL
}

# Connexion à la base de données
connection = psycopg2.connect(**db_config)
cursor = connection.cursor()

# Exécutez la requête SQL pour obtenir les résultats
cursor.execute("SELECT film_id,title,description,language_id,original_language_id FROM film;")
films_data = cursor.fetchall()

# Créez un DataFrame pandas à partir des résultats de la requête
columns = ['film_id','title','description','language_id','original_language_id']
df_film = pd.DataFrame(films_data, columns=columns)

# Affichez le DataFrame
print(df_film)

#________________________________________________________________________________________________________________

# Exécutez la requête SQL pour obtenir les résultats
cursor.execute("SELECT actor_id,film_id FROM film_actor;")
films_data = cursor.fetchall()

# Créez un DataFrame pandas à partir des résultats de la requête
columns = ['actor_id','film_id']
df_film_actor = pd.DataFrame(films_data, columns=columns)

# Affichez le DataFrame
print(df_film_actor)


#________________________________________________________________________________________________________________

# Exécutez la requête SQL pour obtenir les résultats
cursor.execute("SELECT actor_id,first_name, last_name FROM actor;")
films_data = cursor.fetchall()

# Créez un DataFrame pandas à partir des résultats de la requête
columns = ['actor_id','first_name', 'last_name']
df_actor = pd.DataFrame(films_data, columns=columns)

# Affichez le DataFrame
print(df_actor)


#________________________________________________________________________________________________________________



# Suppose you have three dataframes named df_film, df_actor, and df_film_actor

# Remplacer les valeurs NaN par des chaînes vides dans les DataFrames
df_film = df_film.fillna('')
df_actor = df_actor.fillna('')
df_film_actor = df_film_actor.fillna('')

# Create JSON for actors
json_actors = df_actor.to_json(orient='records')

# Manipulation du JSON pour correspondre au schéma spécifié
films_data = []
for film_data in pd.read_json(df_film.to_json(orient='records')).to_dict(orient='records'):
    # Get actors associated with the film
    actors_in_film = df_film_actor[df_film_actor['film_id'] == film_data['film_id']].to_dict(orient='records')
    actors_info = []
    for actor_in_film in actors_in_film:
        actor_info = df_actor[df_actor['actor_id'] == actor_in_film['actor_id']].to_dict(orient='records')[0]
        actors_info.append({
            "actor_id": actor_info["actor_id"],
            "first_name": actor_info["first_name"],
            "last_name": actor_info["last_name"]
        })

    films_data.append({
        "_id": film_data["film_id"],
        "title": film_data["title"],
        "description": film_data["description"],
        "language_id": film_data["language_id"],
        "original_language_id": film_data["original_language_id"],
        "actors": actors_info
    })

# Affichage du JSON final pour les films
#print(films_data)
json_film = films_data

# Exporter les données au format JSON dans un fichier
with open("film_data.json", 'w') as fichier_json:
    json.dump(films_data, fichier_json, indent=2)

#________________________________________________________________________________________________________________
json_actors = df_actor.to_json(orient='records')

# Manipulation du JSON pour correspondre au schéma spécifié
actors_data = []
for actor_data in pd.read_json(json_actors).to_dict(orient='records'):
    films_data = []
    for film_id in df_film_actor[df_film_actor['actor_id'] == actor_data['actor_id']]['film_id']:
        film_info = df_film[df_film['film_id'] == film_id].to_dict(orient='records')[0]
        films_data.append({
            "film_id": film_info["film_id"],
            "title": film_info["title"],
            "description": film_info["description"],
            "language_id": film_info["language_id"],
            "original_language_id": film_info["original_language_id"]
        })

    actors_data.append({
        "_id": actor_data["actor_id"],
        "first_name": actor_data["first_name"],
        "last_name": actor_data["last_name"],
        "films": films_data
    })

# Affichage du JSON final pour les acteurs
#print(actors_data)

# Exporter les données au format JSON dans un fichier
with open("actor_data.json", 'w') as fichier_json:
    json.dump(actors_data, fichier_json)



# Fermez la connexion à la base de données
cursor.close()
connection.close()
print("Connexion à la base de données fermée.")

#________________________________________________________________________________________________________________


# Connexion à la base de données MongoDB
client = MongoClient('localhost', 27017)  # Assurez-vous de spécifier la bonne adresse et le bon port
database = client['film_actor']
collection = database['film']

# Récupérer les _id des documents dans la collection
liste_ids = collection.find({}, {"id": 1})

#Liste des _id présent dans la base mongoDB
liste_mongo_id = []
for i in liste_ids:
    liste_mongo_id.append(i["_id"])
    
    
#Création d'une liste, on stocke toutes les données qui ne sont pas dans la base mongodb
#On compare les id
#La liste créer sera utilisée pour insérer les données
id_a_inserer_film = []
 
for i in range(len(json_film)):
    if json_film[i]['_id']  not in liste_mongo_id:
        id_a_inserer_film.append(json_film[i])


#Si la liste des données à insérer est vide, on affiche un message adapté, sinon on insère les données
if len(id_a_inserer_film) != 0:
    print("Nombre éléments json film: "+str(len(json_film)))
    # Insérer les données dans la collection
    collection.insert_many(id_a_inserer_film)
else:
    print("Pas de données insérer (Les données dont déjà présentes dans la table)")



#________________________________________________________________________________________________________________




collection = database['actor']

# Récupérer les _id des documents dans la collection
liste_ids = collection.find({}, {"id": 1})

#Liste des _id présent dans la base mongoDB
liste_mongo_id = []
for i in liste_ids:
    liste_mongo_id.append(i["_id"])
    
    
#Création d'une liste, on stocke toutes les données qui ne sont pas dans la base mongodb
#On compare les id
#La liste créer sera utilisée pour insérer les données
id_a_inserer_actors = []
 
for i in range(len(actors_data)):
    if actors_data[i]['_id']  not in liste_mongo_id:
        id_a_inserer_actors.append(actors_data[i])
    else:
        #Créer une liste qui renseigne les films où l'acteur a joué qui sont stocké dans la base Mongo
        actor_id = collection.find_one({'_id': actors_data[i]['_id']})
        print(actor_id)
        nb_film = len(actor_id["films"])
        id_film_joue_mongo =  []
        for id_film in range(nb_film):   
            id_film_joue_mongo = actor_id["films"]
        
        
                
            
        #Créer la liste de ses nouveaux films
        nb_film_json = len(actors_data[i]["films"])
        id_film_joue_json =  []
        for id_film in range(nb_film_json):   
            film_joue_json = actors_data[i]["films"][id_film]
            id_film_joue_json.append(film_joue_json)
            

       
        test = []
        test = id_film_joue_json
        test.extend(id_film_joue_mongo)
        
        
        # Supprimer les doublons en utilisant un ensemble (set)
        unique_films = []
        seen_ids = set()
        
        for film in test:
            film_id = film['film_id']
            if film_id not in seen_ids:
                unique_films.append(film)
                seen_ids.add(film_id)
        
        # Maintenant, unique_films contient la liste sans doublons
        print(unique_films)





        actors_data[i]["films"] = unique_films
        
        collection.delete_one({'_id':  actors_data[i]["_id"]})
        
        id_a_inserer_actors.append(actors_data[i])
        

        

        

#Si la liste des données à insérer est vide, on affiche un message adapté, sinon on insère les données
if len(id_a_inserer_actors) != 0:
    print("Nombre éléments json actors: "+str(len(actors_data)))
    # Insérer les données dans la collection
    collection.insert_many(id_a_inserer_actors)
else:
    print("Pas de données insérer (Les données dont déjà présentes dans la table)")


# Fermer la connexion à MongoDB
client.close()


