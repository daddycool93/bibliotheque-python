# 📚 Système de Gestion de Bibliothèque Personnelle

**Projet Final Python — TC SPRING M1 (Fr) 2025-2026**

---

## 📋 Description

Application en ligne de commande permettant de gérer une bibliothèque personnelle :
- Gérer une collection de livres (ajout, suppression, recherche)
- Gérer des utilisateurs
- Emprunter et retourner des livres
- Consulter des statistiques
- Sauvegarder et charger les données (JSON)

---

## 🚀 Lancement

```bash
python bibliotheque.py
```

Aucune dépendance externe requise (bibliothèques standard Python uniquement : `json`, `os`, `datetime`).

---

## 🏗️ Structure du code

| Fichier | Description |
|--------|-------------|
| `bibliotheque.py` | Code source principal (unique fichier) |
| `bibliotheque_data.json` | Fichier de sauvegarde (généré automatiquement) |
| `README.md` | Ce fichier |

---

## 🧱 Architecture

### Classes (POO)

**`Livre`**
- Attributs : `titre`, `auteur`, `annee`, `isbn`, `disponible`, `nb_emprunts`
- Méthodes : `__init__`, `__str__`, `emprunter()`, `retourner()`, `to_dict()`, `from_dict()`

**`Utilisateur`**
- Attributs : `nom`, `id_utilisateur`, `livres_empruntes` (liste d'ISBN)
- Méthodes : `__init__`, `__str__`, `emprunter_livre()`, `retourner_livre()`, `to_dict()`, `from_dict()`

### Fonctions principales

| Fonction | Description |
|---------|-------------|
| `ajouter_livre()` | Ajoute un livre (vérifie l'unicité de l'ISBN) |
| `supprimer_livre()` | Supprime un livre par ISBN (si non emprunté) |
| `rechercher_par_titre()` | Recherche partielle par titre |
| `rechercher_par_auteur()` | Recherche partielle par auteur |
| `afficher_tous_les_livres()` | Affiche tous les livres |
| `afficher_livres_disponibles()` | Filtre les livres disponibles |
| `afficher_livres_empruntes()` | Filtre les livres empruntés |
| `statistiques()` | Statistiques globales + top emprunteurs |
| `sauvegarder_donnees()` | Sauvegarde JSON |
| `charger_donnees()` | Chargement JSON |

---

## 📦 Structures de données utilisées

| Structure | Utilisation |
|-----------|-------------|
| **Dictionnaire** | `bibliotheque` (clé = ISBN), `utilisateurs` (clé = ID) |
| **Liste** | `livres_empruntes` de chaque utilisateur |
| **Set** | Calcul des auteurs uniques dans les statistiques |
| **Tuple** | Années de publication triées dans les statistiques |

---

## 🎮 Menu principal

```
=== BIBLIOTHÈQUE PERSONNELLE ===
1.  Ajouter un livre
2.  Supprimer un livre
3.  Rechercher un livre
4.  Afficher tous les livres
5.  Afficher les livres disponibles
6.  Afficher les livres empruntés
7.  Ajouter un utilisateur
8.  Afficher tous les utilisateurs
9.  Emprunter un livre
10. Retourner un livre
11. Statistiques
12. Sauvegarder & Quitter
```

---

## ✅ Gestion des erreurs

- Validation des saisies (entiers, champs vides)
- Vérification de l'unicité de l'ISBN à l'ajout
- Impossible de supprimer un livre actuellement emprunté
- Vérification de l'existence d'un utilisateur avant emprunt
- Gestion des erreurs de lecture JSON

---

## 💡 Notions Python couvertes

- Variables et types de données
- Entrées/Sorties (`input`, `print`)
- Conditions (`if/elif/else`)
- Boucles (`for`, `while`)
- Listes, dictionnaires, sets, tuples
- Fonctions avec paramètres et valeurs de retour
- Programmation Orientée Objet (classes, méthodes, `__str__`, `__init__`)
- Fichiers JSON (`json.load`, `json.dump`)
- Gestion d'exceptions (`try/except`)
