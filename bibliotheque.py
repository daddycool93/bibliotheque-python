# =============================================================================
# SYSTÈME DE GESTION DE BIBLIOTHÈQUE PERSONNELLE
# Projet Final Python - TC SPRING M1 (Fr) 2025-2026
# =============================================================================

import json
import os
import csv
from datetime import date


# =============================================================================
# PARTIE 1 : CLASSE LIVRE
# =============================================================================

class Livre:
    """Représente un livre dans la bibliothèque."""

    def __init__(self, titre: str, auteur: str, annee: int, isbn: str):
        """Constructeur de la classe Livre."""
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.isbn = isbn
        self.disponible = True  # True si disponible, False si emprunté
        self.nb_emprunts = 0    # compteur pour les statistiques

    def __str__(self) -> str:
        """Affiche les informations du livre."""
        statut = "✅ Disponible" if self.disponible else "❌ Emprunté"
        return (f"[ISBN: {self.isbn}] \"{self.titre}\" - {self.auteur} "
                f"({self.annee}) | {statut}")

    def emprunter(self) -> bool:
        """Marque le livre comme indisponible. Retourne True si succès."""
        if self.disponible:
            self.disponible = False
            self.nb_emprunts += 1
            return True
        return False

    def retourner(self) -> bool:
        """Marque le livre comme disponible. Retourne True si succès."""
        if not self.disponible:
            self.disponible = True
            return True
        return False

    def to_dict(self) -> dict:
        """Convertit le livre en dictionnaire pour la sauvegarde JSON."""
        return {
            "titre": self.titre,
            "auteur": self.auteur,
            "annee": self.annee,
            "isbn": self.isbn,
            "disponible": self.disponible,
            "nb_emprunts": self.nb_emprunts
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Crée un Livre à partir d'un dictionnaire (chargement JSON)."""
        livre = cls(data["titre"], data["auteur"], data["annee"], data["isbn"])
        livre.disponible = data.get("disponible", True)
        livre.nb_emprunts = data.get("nb_emprunts", 0)
        return livre


# =============================================================================
# PARTIE 2 : CLASSE UTILISATEUR
# =============================================================================

class Utilisateur:
    """Représente un utilisateur de la bibliothèque."""

    def __init__(self, nom: str, id_utilisateur: int):
        """Constructeur de la classe Utilisateur."""
        self.nom = nom
        self.id_utilisateur = id_utilisateur
        self.livres_empruntes = []  # liste des ISBN empruntés

    def __str__(self) -> str:
        """Affiche les informations de l'utilisateur."""
        nb = len(self.livres_empruntes)
        return (f"[ID: {self.id_utilisateur}] {self.nom} "
                f"| Livres empruntés : {nb}")

    def emprunter_livre(self, livre: Livre) -> bool:
        """Ajoute un livre à la liste des livres empruntés."""
        if livre.isbn not in self.livres_empruntes:
            if livre.emprunter():
                self.livres_empruntes.append(livre.isbn)
                return True
        return False

    def retourner_livre(self, livre: Livre) -> bool:
        """Retire un livre de la liste des livres empruntés."""
        if livre.isbn in self.livres_empruntes:
            if livre.retourner():
                self.livres_empruntes.remove(livre.isbn)
                return True
        return False

    def to_dict(self) -> dict:
        """Convertit l'utilisateur en dictionnaire pour la sauvegarde JSON."""
        return {
            "nom": self.nom,
            "id_utilisateur": self.id_utilisateur,
            "livres_empruntes": self.livres_empruntes
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Crée un Utilisateur à partir d'un dictionnaire (chargement JSON)."""
        u = cls(data["nom"], data["id_utilisateur"])
        u.livres_empruntes = data.get("livres_empruntes", [])
        return u


# =============================================================================
# PARTIE 3 : FONCTIONS DE GESTION DE LA BIBLIOTHÈQUE
# =============================================================================

def ajouter_livre(bibliotheque: dict, livre: Livre) -> bool:
    """Ajoute un livre à la bibliothèque (dict indexé par ISBN)."""
    if livre.isbn in bibliotheque:
        print(f"  ⚠️  Un livre avec l'ISBN '{livre.isbn}' existe déjà.")
        return False
    bibliotheque[livre.isbn] = livre
    print(f"  ✅ Livre \"{livre.titre}\" ajouté avec succès.")
    return True


def supprimer_livre(bibliotheque: dict, isbn: str) -> bool:
    """Supprime un livre par son ISBN."""
    if isbn not in bibliotheque:
        print(f"  ⚠️  Aucun livre trouvé avec l'ISBN '{isbn}'.")
        return False
    if not bibliotheque[isbn].disponible:
        print(f"  ⚠️  Ce livre est actuellement emprunté, impossible de le supprimer.")
        return False
    titre = bibliotheque[isbn].titre
    del bibliotheque[isbn]
    print(f"  ✅ Livre \"{titre}\" supprimé avec succès.")
    return True


def rechercher_par_titre(bibliotheque: dict, titre: str) -> list:
    """Retourne les livres dont le titre contient la chaîne recherchée."""
    titre_lower = titre.lower()
    resultats = [l for l in bibliotheque.values() if titre_lower in l.titre.lower()]
    return resultats


def rechercher_par_auteur(bibliotheque: dict, auteur: str) -> list:
    """Retourne les livres d'un auteur (recherche partielle)."""
    auteur_lower = auteur.lower()
    resultats = [l for l in bibliotheque.values() if auteur_lower in l.auteur.lower()]
    return resultats


def afficher_tous_les_livres(bibliotheque: dict) -> None:
    """Affiche tous les livres de la bibliothèque."""
    if not bibliotheque:
        print("  📭 La bibliothèque est vide.")
        return
    print(f"\n  📚 Total : {len(bibliotheque)} livre(s)\n")
    for livre in bibliotheque.values():
        print(f"    {livre}")


def afficher_livres_disponibles(bibliotheque: dict) -> None:
    """Affiche uniquement les livres disponibles."""
    disponibles = [l for l in bibliotheque.values() if l.disponible]
    if not disponibles:
        print("  📭 Aucun livre disponible.")
        return
    print(f"\n  ✅ Livres disponibles : {len(disponibles)}\n")
    for livre in disponibles:
        print(f"    {livre}")


def afficher_livres_empruntes(bibliotheque: dict) -> None:
    """Affiche uniquement les livres empruntés."""
    empruntes = [l for l in bibliotheque.values() if not l.disponible]
    if not empruntes:
        print("  📭 Aucun livre emprunté actuellement.")
        return
    print(f"\n  ❌ Livres empruntés : {len(empruntes)}\n")
    for livre in empruntes:
        print(f"    {livre}")


def statistiques(bibliotheque: dict, utilisateurs: dict) -> None:
    """Affiche des statistiques générales sur la bibliothèque."""
    total_livres = len(bibliotheque)
    total_utilisateurs = len(utilisateurs)
    disponibles = sum(1 for l in bibliotheque.values() if l.disponible)
    empruntes = total_livres - disponibles

    # Ensemble des auteurs uniques (utilisation d'un SET)
    auteurs = {l.auteur for l in bibliotheque.values()}

    # Années de publication (utilisation d'un TUPLE pour affichage)
    if bibliotheque:
        annees = tuple(sorted(set(l.annee for l in bibliotheque.values())))
        annee_min, annee_max = annees[0], annees[-1]
    else:
        annee_min = annee_max = "N/A"

    # Top 3 des livres les plus empruntés
    top_livres = sorted(bibliotheque.values(), key=lambda l: l.nb_emprunts, reverse=True)[:3]

    print("\n" + "=" * 50)
    print("         📊 STATISTIQUES DE LA BIBLIOTHÈQUE")
    print("=" * 50)
    print(f"  📚 Total livres         : {total_livres}")
    print(f"  ✅ Livres disponibles   : {disponibles}")
    print(f"  ❌ Livres empruntés     : {empruntes}")
    print(f"  👥 Utilisateurs inscrits : {total_utilisateurs}")
    print(f"  ✍️  Auteurs différents   : {len(auteurs)}")
    print(f"  📅 Années : de {annee_min} à {annee_max}")

    if top_livres:
        print("\n  🏆 Top livres les plus empruntés :")
        for i, livre in enumerate(top_livres, 1):
            print(f"    {i}. \"{livre.titre}\" ({livre.nb_emprunts} emprunt(s))")

    if utilisateurs:
        print("\n  👤 Utilisateurs les plus actifs :")
        top_users = sorted(utilisateurs.values(),
                           key=lambda u: len(u.livres_empruntes), reverse=True)[:3]
        for u in top_users:
            print(f"    - {u.nom} : {len(u.livres_empruntes)} livre(s) en cours")
    print("=" * 50)


# =============================================================================
# PERSISTANCE DES DONNÉES (JSON + CSV)
# =============================================================================

FICHIER_JSON             = "bibliotheque_data.json"
FICHIER_LIVRES_CSV       = "livres.csv"
FICHIER_UTILISATEURS_CSV = "utilisateurs.csv"


# ---------- JSON ----------

def sauvegarder_donnees(bibliotheque: dict, utilisateurs: dict) -> None:
    """Sauvegarde les données en JSON ET en CSV."""
    # --- JSON ---
    data = {
        "livres": [l.to_dict() for l in bibliotheque.values()],
        "utilisateurs": [u.to_dict() for u in utilisateurs.values()],
        "date_sauvegarde": str(date.today())
    }
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  💾 JSON  → '{FICHIER_JSON}'")
    # --- CSV ---
    sauvegarder_csv_livres(bibliotheque)
    sauvegarder_csv_utilisateurs(utilisateurs)


def charger_donnees() -> tuple:
    """Charge depuis JSON (prioritaire) ou depuis CSV si JSON absent."""
    if os.path.exists(FICHIER_JSON):
        return charger_depuis_json()
    elif os.path.exists(FICHIER_LIVRES_CSV):
        return charger_depuis_csv()
    return {}, {}


def charger_depuis_json() -> tuple:
    """Charge les données depuis le fichier JSON."""
    bibliotheque = {}
    utilisateurs = {}
    try:
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        for ld in data.get("livres", []):
            livre = Livre.from_dict(ld)
            bibliotheque[livre.isbn] = livre
        for ud in data.get("utilisateurs", []):
            u = Utilisateur.from_dict(ud)
            utilisateurs[u.id_utilisateur] = u
        print(f"  📂 JSON chargé ({len(bibliotheque)} livre(s), "
              f"{len(utilisateurs)} utilisateur(s)).")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"  ⚠️  Erreur JSON : {e}")
    return bibliotheque, utilisateurs


# ---------- CSV ----------

def sauvegarder_csv_livres(bibliotheque: dict) -> None:
    """Sauvegarde les livres dans livres.csv."""
    champs = ["titre", "auteur", "annee", "isbn", "disponible", "nb_emprunts"]
    with open(FICHIER_LIVRES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        for livre in bibliotheque.values():
            writer.writerow({
                "titre":       livre.titre,
                "auteur":      livre.auteur,
                "annee":       livre.annee,
                "isbn":        livre.isbn,
                "disponible":  livre.disponible,
                "nb_emprunts": livre.nb_emprunts,
            })
    print(f"  💾 CSV   → '{FICHIER_LIVRES_CSV}'")


def sauvegarder_csv_utilisateurs(utilisateurs: dict) -> None:
    """Sauvegarde les utilisateurs dans utilisateurs.csv."""
    champs = ["nom", "id_utilisateur", "livres_empruntes"]
    with open(FICHIER_UTILISATEURS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        for u in utilisateurs.values():
            # Plusieurs ISBN séparés par "|" dans la colonne
            writer.writerow({
                "nom":            u.nom,
                "id_utilisateur": u.id_utilisateur,
                "livres_empruntes": "|".join(u.livres_empruntes),
            })
    print(f"  💾 CSV   → '{FICHIER_UTILISATEURS_CSV}'")


def charger_depuis_csv() -> tuple:
    """Charge les données depuis les fichiers CSV."""
    bibliotheque = {}
    utilisateurs = {}

    # Livres
    if os.path.exists(FICHIER_LIVRES_CSV):
        try:
            with open(FICHIER_LIVRES_CSV, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    livre = Livre(
                        titre=row["titre"],
                        auteur=row["auteur"],
                        annee=int(row["annee"]),
                        isbn=row["isbn"]
                    )
                    livre.disponible  = row["disponible"].strip() == "True"
                    livre.nb_emprunts = int(row.get("nb_emprunts", 0))
                    bibliotheque[livre.isbn] = livre
            print(f"  📂 CSV livres chargé ({len(bibliotheque)} livre(s)).")
        except Exception as e:
            print(f"  ⚠️  Erreur CSV livres : {e}")

    # Utilisateurs
    if os.path.exists(FICHIER_UTILISATEURS_CSV):
        try:
            with open(FICHIER_UTILISATEURS_CSV, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    uid = int(row["id_utilisateur"])
                    u = Utilisateur(row["nom"], uid)
                    empruntes = row.get("livres_empruntes", "").strip()
                    u.livres_empruntes = empruntes.split("|") if empruntes else []
                    utilisateurs[uid] = u
            print(f"  📂 CSV utilisateurs chargé ({len(utilisateurs)} utilisateur(s)).")
        except Exception as e:
            print(f"  ⚠️  Erreur CSV utilisateurs : {e}")

    return bibliotheque, utilisateurs


# =============================================================================
# UTILITAIRES D'INTERFACE
# =============================================================================

def afficher_menu() -> None:
    """Affiche le menu principal."""
    print("\n" + "=" * 40)
    print("      === BIBLIOTHÈQUE PERSONNELLE ===")
    print("=" * 40)
    print("  1.  Ajouter un livre")
    print("  2.  Supprimer un livre")
    print("  3.  Rechercher un livre")
    print("  4.  Afficher tous les livres")
    print("  5.  Afficher les livres disponibles")
    print("  6.  Afficher les livres empruntés")
    print("  7.  Ajouter un utilisateur")
    print("  8.  Afficher tous les utilisateurs")
    print("  9.  Emprunter un livre")
    print("  10. Retourner un livre")
    print("  11. Statistiques")
    print("  12. Sauvegarder & Quitter")
    print("=" * 40)


def saisir_entier(message: str) -> int:
    """Demande un entier à l'utilisateur avec validation."""
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("  ⚠️  Veuillez entrer un nombre entier valide.")


def saisir_texte(message: str, min_len: int = 1) -> str:
    """Demande une chaîne non vide à l'utilisateur."""
    while True:
        valeur = input(message).strip()
        if len(valeur) >= min_len:
            return valeur
        print(f"  ⚠️  Ce champ ne peut pas être vide.")


def afficher_resultats(resultats: list, label: str) -> None:
    """Affiche une liste de résultats de recherche."""
    if not resultats:
        print(f"  📭 Aucun livre trouvé pour '{label}'.")
    else:
        print(f"\n  🔍 {len(resultats)} résultat(s) pour '{label}' :\n")
        for livre in resultats:
            print(f"    {livre}")


# =============================================================================
# PARTIE 4 : MENU INTERACTIF PRINCIPAL
# =============================================================================

def menu_ajouter_livre(bibliotheque: dict) -> None:
    print("\n--- Ajouter un livre ---")
    titre = saisir_texte("  Titre     : ")
    auteur = saisir_texte("  Auteur    : ")
    annee = saisir_entier("  Année     : ")
    isbn = saisir_texte("  ISBN      : ")
    livre = Livre(titre, auteur, annee, isbn)
    ajouter_livre(bibliotheque, livre)


def menu_supprimer_livre(bibliotheque: dict) -> None:
    print("\n--- Supprimer un livre ---")
    if not bibliotheque:
        print("  📭 La bibliothèque est vide.")
        return
    isbn = saisir_texte("  ISBN du livre à supprimer : ")
    supprimer_livre(bibliotheque, isbn)


def menu_rechercher_livre(bibliotheque: dict) -> None:
    print("\n--- Rechercher un livre ---")
    print("  1. Par titre")
    print("  2. Par auteur")
    choix = input("  Votre choix : ").strip()
    if choix == "1":
        titre = saisir_texte("  Titre recherché : ")
        resultats = rechercher_par_titre(bibliotheque, titre)
        afficher_resultats(resultats, titre)
    elif choix == "2":
        auteur = saisir_texte("  Auteur recherché : ")
        resultats = rechercher_par_auteur(bibliotheque, auteur)
        afficher_resultats(resultats, auteur)
    else:
        print("  ⚠️  Choix invalide.")


def menu_ajouter_utilisateur(utilisateurs: dict) -> None:
    print("\n--- Ajouter un utilisateur ---")
    nom = saisir_texte("  Nom de l'utilisateur : ")
    # Génère un ID unique automatiquement
    new_id = max(utilisateurs.keys(), default=0) + 1
    u = Utilisateur(nom, new_id)
    utilisateurs[new_id] = u
    print(f"  ✅ Utilisateur '{nom}' ajouté avec l'ID {new_id}.")


def menu_afficher_utilisateurs(utilisateurs: dict) -> None:
    print("\n--- Liste des utilisateurs ---")
    if not utilisateurs:
        print("  📭 Aucun utilisateur enregistré.")
        return
    for u in utilisateurs.values():
        print(f"    {u}")


def menu_emprunter_livre(bibliotheque: dict, utilisateurs: dict) -> None:
    print("\n--- Emprunter un livre ---")
    if not utilisateurs:
        print("  ⚠️  Aucun utilisateur enregistré. Ajoutez d'abord un utilisateur.")
        return
    id_u = saisir_entier("  ID de l'utilisateur : ")
    if id_u not in utilisateurs:
        print(f"  ⚠️  Aucun utilisateur avec l'ID {id_u}.")
        return
    isbn = saisir_texte("  ISBN du livre à emprunter : ")
    if isbn not in bibliotheque:
        print(f"  ⚠️  Livre avec l'ISBN '{isbn}' introuvable.")
        return
    utilisateur = utilisateurs[id_u]
    livre = bibliotheque[isbn]
    if not livre.disponible:
        print(f"  ⚠️  Le livre \"{livre.titre}\" est déjà emprunté.")
        return
    if utilisateur.emprunter_livre(livre):
        print(f"  ✅ {utilisateur.nom} a emprunté \"{livre.titre}\".")
    else:
        print("  ⚠️  Emprunt impossible (déjà emprunté par cet utilisateur ?).")


def menu_retourner_livre(bibliotheque: dict, utilisateurs: dict) -> None:
    print("\n--- Retourner un livre ---")
    id_u = saisir_entier("  ID de l'utilisateur : ")
    if id_u not in utilisateurs:
        print(f"  ⚠️  Aucun utilisateur avec l'ID {id_u}.")
        return
    utilisateur = utilisateurs[id_u]
    if not utilisateur.livres_empruntes:
        print(f"  ℹ️  {utilisateur.nom} n'a aucun livre emprunté.")
        return
    print(f"  Livres empruntés par {utilisateur.nom} :")
    for isbn in utilisateur.livres_empruntes:
        if isbn in bibliotheque:
            print(f"    - {bibliotheque[isbn]}")
    isbn = saisir_texte("  ISBN du livre à retourner : ")
    if isbn not in bibliotheque:
        print(f"  ⚠️  ISBN '{isbn}' introuvable.")
        return
    livre = bibliotheque[isbn]
    if utilisateur.retourner_livre(livre):
        print(f"  ✅ {utilisateur.nom} a retourné \"{livre.titre}\".")
    else:
        print("  ⚠️  Ce livre ne figure pas dans les emprunts de cet utilisateur.")


# =============================================================================
# POINT D'ENTRÉE PRINCIPAL
# =============================================================================

def main():
    print("\n🚀 Bienvenue dans le Système de Gestion de Bibliothèque Personnelle !")

    # Chargement des données existantes
    bibliotheque, utilisateurs = charger_donnees()

    # Données de démonstration si la bibliothèque est vide
    if not bibliotheque:
        print("  ℹ️  Chargement de données de démonstration...")
        livres_demo = [
            Livre("Le Petit Prince", "Antoine de Saint-Exupéry", 1943, "978-2-07-040850-4"),
            Livre("1984", "George Orwell", 1949, "978-2-07-036822-8"),
            Livre("L'Étranger", "Albert Camus", 1942, "978-2-07-036024-6"),
            Livre("Harry Potter et la Pierre Philosophale", "J.K. Rowling", 1997, "978-2-07-054090-1"),
            Livre("Dune", "Frank Herbert", 1965, "978-2-07-036369-8"),
        ]
        for l in livres_demo:
            bibliotheque[l.isbn] = l

    # Boucle principale du menu
    while True:
        afficher_menu()
        choix = input("  Entrez votre choix : ").strip()

        if choix == "1":
            menu_ajouter_livre(bibliotheque)
        elif choix == "2":
            menu_supprimer_livre(bibliotheque)
        elif choix == "3":
            menu_rechercher_livre(bibliotheque)
        elif choix == "4":
            afficher_tous_les_livres(bibliotheque)
        elif choix == "5":
            afficher_livres_disponibles(bibliotheque)
        elif choix == "6":
            afficher_livres_empruntes(bibliotheque)
        elif choix == "7":
            menu_ajouter_utilisateur(utilisateurs)
        elif choix == "8":
            menu_afficher_utilisateurs(utilisateurs)
        elif choix == "9":
            menu_emprunter_livre(bibliotheque, utilisateurs)
        elif choix == "10":
            menu_retourner_livre(bibliotheque, utilisateurs)
        elif choix == "11":
            statistiques(bibliotheque, utilisateurs)
        elif choix == "12":
            sauvegarder_donnees(bibliotheque, utilisateurs)
            print("\n👋 Au revoir !\n")
            break
        else:
            print("  ⚠️  Choix invalide. Veuillez entrer un nombre entre 1 et 12.")


if __name__ == "__main__":
    main()
