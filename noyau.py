# ============================================================
# NOYAU FONCTIONNEL - Projet : Organisation de Repas Partagé
# ============================================================
# Ce fichier contient toute la logique métier (données + calculs)
# Il ne contient AUCUN code tkinter.
# ============================================================

CATEGORIES = ["Entrees", "Plats", "Desserts", "Boissons"]

participants = []


# ------------------------------------------------------------
# Opérations CRUD
# ------------------------------------------------------------

def ajouter_participant(nom, prenom, categorie, nom_element, quantite):
    erreur = valider_saisie(nom, prenom, categorie, nom_element, quantite)
    if erreur:
        return erreur
    participants.append({
        "nom": nom.strip(),
        "prenom": prenom.strip(),
        "categorie": categorie,
        "nom_element": nom_element.strip(),
        "quantite": int(quantite)
    })
    return True


def modifier_participant(index, nom, prenom, categorie, nom_element, quantite):
    erreur = valider_saisie(nom, prenom, categorie, nom_element, quantite)
    if erreur:
        return erreur
    participants[index] = {
        "nom": nom.strip(),
        "prenom": prenom.strip(),
        "categorie": categorie,
        "nom_element": nom_element.strip(),
        "quantite": int(quantite)
    }
    return True


def supprimer_participant(index):
    if 0 <= index < len(participants):
        participants.pop(index)


def valider_saisie(nom, prenom, categorie, nom_element, quantite):
    if not nom.strip():
        return "Le champ Nom est obligatoire."
    if not prenom.strip():
        return "Le champ Prenom est obligatoire."
    if categorie not in CATEGORIES:
        return "Veuillez selectionner une categorie valide."
    if not nom_element.strip():
        return "Le champ Nom de l'element est obligatoire."
    try:
        q = int(quantite)
        if q <= 0:
            return "La quantite doit etre un entier strictement positif."
    except (ValueError, TypeError):
        return "La quantite doit etre un entier strictement positif."
    return None


# ------------------------------------------------------------
# Indicateurs
# ------------------------------------------------------------

def total_participants():
    return len(participants)


def total_elements():
    return sum(p["quantite"] for p in participants)


def calculer_indicateurs():
    """Retourne {cat: quantite_totale} pour chaque categorie."""
    ind = {cat: 0 for cat in CATEGORIES}
    for p in participants:
        if p["categorie"] in ind:
            ind[p["categorie"]] += p["quantite"]
    return ind


def max_categorie():
    """Retourne la quantite maximale parmi toutes les categories pour pouvoir effectuer la comparaison."""
    ind = calculer_indicateurs()
    valeurs = list(ind.values())
    return max(valeurs) if valeurs else 0


def etat_categorie(categorie):
    """
    Retourne "OK" si la categorie a autant d'elements que la categorie max,
    "MANQUE" sinon (ou si elle est a 0).
    Si toutes les categories sont a 0, toutes sont "MANQUE".
    """
    ind = calculer_indicateurs()
    maximum = max_categorie()
    if maximum == 0:
        return "MANQUE"
    nb = ind.get(categorie, 0)
    if nb == maximum:
        return "OK"
    return "MANQUE"


def calculer_nb_repas_possible():
    """Nombre de services possibles = min des categories (0 si une manque)."""
    ind = calculer_indicateurs()
    valeurs = list(ind.values())
    if 0 in valeurs:
        return 0
    return min(valeurs)


def verifier_repas_possible():
    return len(participants) > 0 and calculer_nb_repas_possible() >= len(participants)


def calculer_manquants():
    """Categories dont la quantite est inferieure au max (donc MANQUE)."""
    ind = calculer_indicateurs()
    maximum = max_categorie()
    if maximum == 0:
        return list(CATEGORIES)
    return [cat for cat, nb in ind.items() if nb < maximum]


def pourcentage_categorie(categorie):
    total = total_elements()
    if total == 0:
        return 0.0
    ind = calculer_indicateurs()
    return round(ind.get(categorie, 0) / total * 100, 1)


# ------------------------------------------------------------
# Tri
# ------------------------------------------------------------

def trier(colonne, ordre_croissant=True):
    reverse = not ordre_croissant
    if colonne == "quantite":
        participants.sort(key=lambda p: p["quantite"], reverse=reverse)
    else:
        participants.sort(key=lambda p: p.get(colonne, "").lower(), reverse=reverse)
