import tkinter as tk
from tkinter import messagebox
import json
from pymongo import MongoClient

class CadreSaisieActeur(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        # Widgets pour la saisie des informations de l'acteur
        self.etiquette_id_acteur = tk.Label(self, text="ID Acteur:")
        self.saisie_id_acteur = tk.Entry(self)
        self.etiquette_prenom = tk.Label(self, text="Prénom:")
        self.saisie_prenom = tk.Entry(self)
        self.etiquette_nom = tk.Label(self, text="Nom:")
        self.saisie_nom = tk.Entry(self)

        # Placement des widgets dans la grille
        self.etiquette_id_acteur.grid(row=0, column=0, padx=5, pady=5)
        self.saisie_id_acteur.grid(row=0, column=1, padx=5, pady=5)
        self.etiquette_prenom.grid(row=1, column=0, padx=5, pady=5)
        self.saisie_prenom.grid(row=1, column=1, padx=5, pady=5)
        self.etiquette_nom.grid(row=2, column=0, padx=5, pady=5)
        self.saisie_nom.grid(row=2, column=1, padx=5, pady=5)

class ApplicationPrincipale:
    def __init__(self, maitre):
        self.maitre = maitre
        self.cadres_saisie_acteur = []  # Liste pour stocker les cadres de saisie d'acteur
        self.creer_widgets()

    def creer_widgets(self):
        # Widgets pour la saisie des informations du film
        self.etiquette_nom_film = tk.Label(self.maitre, text="Nom du Film:")
        self.saisie_nom_film = tk.Entry(self.maitre)
        self.etiquette_description = tk.Label(self.maitre, text="Description du Film:")
        self.saisie_description = tk.Entry(self.maitre)
        self.etiquette_langue = tk.Label(self.maitre, text="Langue du Film:")
        self.saisie_langue = tk.Entry(self.maitre)
        self.etiquette_nb_acteurs = tk.Label(self.maitre, text="Nombre d'acteurs:")
        self.saisie_nb_acteurs = tk.Entry(self.maitre)
        self.bouton_soumettre = tk.Button(self.maitre, text="Soumettre", command=self.afficher_interface_saisie_acteur)

        # Placement des widgets dans la grille
        self.etiquette_nom_film.grid(row=0, column=0, padx=10, pady=10)
        self.saisie_nom_film.grid(row=0, column=1, padx=10, pady=10)
        self.etiquette_description.grid(row=1, column=0, padx=10, pady=10)
        self.saisie_description.grid(row=1, column=1, padx=10, pady=10)
        self.etiquette_langue.grid(row=2, column=0, padx=10, pady=10)
        self.saisie_langue.grid(row=2, column=1, padx=10, pady=10)
        self.etiquette_nb_acteurs.grid(row=3, column=0, padx=10, pady=10)
        self.saisie_nb_acteurs.grid(row=3, column=1, padx=10, pady=10)
        self.bouton_soumettre.grid(row=4, column=0, columnspan=2, pady=10)

    def afficher_interface_saisie_acteur(self):
        try:
            # Récupérer le nombre d'acteurs depuis l'entrée utilisateur
            nb_acteurs = int(self.saisie_nb_acteurs.get())

            # Créer une fenêtre de saisie pour les acteurs
            interface_saisie_acteur = tk.Toplevel(self.maitre)
            interface_saisie_acteur.title("Saisie des Acteurs")

            # Créer un dictionnaire pour stocker les données du film
            donnees_film = {
                "nom": self.saisie_nom_film.get(),
                "description": self.saisie_description.get(),
                "langue": self.saisie_langue.get(),
                "acteurs": []
            }

            # Afficher les informations du film dans la fenêtre de saisie d'acteur
            tk.Label(interface_saisie_acteur, text=f"Nom du Film: {donnees_film['nom']}").pack()
            tk.Label(interface_saisie_acteur, text=f"Description du Film: {donnees_film['description']}").pack()
            tk.Label(interface_saisie_acteur, text=f"Langue du Film: {donnees_film['langue']}").pack()

            # Réinitialiser la liste des cadres de saisie d'acteur
            self.cadres_saisie_acteur = []

            # Créer les cadres de saisie d'acteur en fonction du nombre d'acteurs
            for i in range(nb_acteurs):
                cadre_saisie_acteur = CadreSaisieActeur(interface_saisie_acteur)
                cadre_saisie_acteur.pack(pady=10)
                self.cadres_saisie_acteur.append(cadre_saisie_acteur)

            # Ajouter un bouton pour enregistrer les données
            tk.Button(interface_saisie_acteur, text="Enregistrer", command=lambda: self.recueillir_et_enregistrer_donnees(donnees_film)).pack()

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide d'acteurs.")

    def recueillir_et_enregistrer_donnees(self, donnees_film):
        # Parcourir chaque cadre de saisie d'acteur et collecter les données
        for cadre_saisie_acteur in self.cadres_saisie_acteur:
            donnees_acteur = {
                "id_acteur": cadre_saisie_acteur.saisie_id_acteur.get(),
                "prenom": cadre_saisie_acteur.saisie_prenom.get(),
                "nom": cadre_saisie_acteur.saisie_nom.get()
            }
            # Ajouter les données de l'acteur à la liste d'acteurs dans le dictionnaire du film
            donnees_film["acteurs"].append(donnees_acteur)

        # Enregistrez localement dans un fichier JSON
        nom_fichier = f"{donnees_film['nom']}_donnees.json"
        with open(nom_fichier, 'w') as fichier_json:
            json.dump(donnees_film, fichier_json, indent=2)

        # Enregistrez dans MongoDB
        client = MongoClient('localhost', 27017)  # Mettez les paramètres appropriés
        db = client['pagila']
        collection = db['film']
        collection.insert_one(donnees_film)

        # Afficher un message de succès
        messagebox.showinfo("Succès", f"Données enregistrées localement dans {nom_fichier} et dans MongoDB.")

if __name__ == "__main__":
    racine = tk.Tk()
    racine.title("Saisie de Données")

    application = ApplicationPrincipale(racine)

    racine.mainloop()
