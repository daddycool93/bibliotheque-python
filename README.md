Un petit projet Python qu'on a développé dans le cadre de notre cours de python en Msc Cyber. L'idée de base c'est simple : gérer une bibliothèque personnelle, avec des livres, des utilisateurs, et la possibilité d'emprunter ou de retourner des livres. 

le travail de : 
HOUETOHOSSOU Stephane Bignon Vincent J	stephanebignonvincentjunior.houetohossou@edu.ece.fr
TRAORÉ Ali	ali.traore@edu.ece.fr
KOUAKOU Nanan	nanan.kouakou@edu.ece.fr

## Comment lancer le projet
Pas besoin d'installer quoi que ce soit, Python suffit. Il suffit de lancer :

```bash
python bibliotheque.py
```
Et le menu s'affiche directement dans le terminal.


## Ce que le programme permet de faire

- Ajouter ou supprimer des livres
- Rechercher un livre par titre ou par auteur
- Créer des utilisateurs
- Emprunter et retourner des livres
- Voir les statistiques de la bibliothèque (livres les plus empruntés, auteurs, etc.)
- Sauvegarder automatiquement les données en JSON et en CSV

## Les fichiers du projet

| Fichier | Rôle |
|--------|------|
| `bibliotheque.py` | Le code principal |
| `livres.csv` | Données de départ pour les livres |
| `utilisateurs.csv` | Données de départ pour les utilisateurs |
| `bibliotheque_data.json` | Fichier de sauvegarde (généré automatiquement) |

## Organisation du code

On a essayé de bien structurer le projet en suivant ce qu'on a vu en cours :

- **Classe `Livre`** : représente un livre avec son titre, auteur, année, ISBN et son statut (disponible ou emprunté)
- **Classe `Utilisateur`** : représente un utilisateur avec la liste des livres qu'il a empruntés
- **Les fonctions** : gèrent toute la logique de la bibliothèque (ajout, recherche, affichage, stats...)
- **Le menu** : l'interface en ligne de commande pour naviguer entre les options

## Sauvegarde des données

À chaque fois qu'on quitte le programme, les données sont sauvegardées dans deux formats :
- un fichier **JSON** (`bibliotheque_data.json`)
- deux fichiers **CSV** (`livres.csv` et `utilisateurs.csv`)

Au prochain lancement, le programme recharge tout automatiquement.

---

## Ce qu'on a utilisé comme notions Python

- Les classes et la POO
- Les dictionnaires, listes, sets et tuples
- Les fonctions
- Les boucles et conditions
- La gestion des fichiers (JSON et CSV)
- La gestion des erreurs avec try/except

Projet réalisé dans le cadre du cours Python — TC SPRING M1 (Fr) 2025-2026

v1 :  depot initial
v2 : Mise à jour du fichier principal