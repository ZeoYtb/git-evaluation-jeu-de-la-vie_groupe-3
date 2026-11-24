"""Jeu de la vie de Conway : simulation en ligne de commande.

Usage : python3 main.py [-n N] [-m N] [-s N] [-o DOSSIER] [-t image|text] [-p]
Une grille peut aussi être fournie sur l'entrée standard (voir lire_grille).
"""

import argparse
import os
import random
import sys

from lib import write_grid


class ErreurEntree(Exception):
    """Données invalides fournies par l'utilisateur (grille mal formée...)."""


# ---------------------------------------------------------------------------
# Lecture des arguments
# ---------------------------------------------------------------------------

def convertir_en_entier(texte):
    """Convertit un texte en entier, ou signale l'erreur à argparse."""
    try:
        return int(texte)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{texte}' n'est pas un entier")


def entier_strictement_positif(texte):
    """Type argparse pour --nb_cells : entier >= 1."""
    valeur = convertir_en_entier(texte)
    if valeur <= 0:
        raise argparse.ArgumentTypeError(
            f"doit être strictement positif (reçu : {valeur})")
    return valeur


def entier_positif_ou_nul(texte):
    """Type argparse pour --max_iterations : entier >= 0."""
    valeur = convertir_en_entier(texte)
    if valeur < 0:
        raise argparse.ArgumentTypeError(
            f"doit être positif ou nul (reçu : {valeur})")
    return valeur


def lire_arguments(argv=None):
    """Déclare et lit les options de la ligne de commande."""
    parseur = argparse.ArgumentParser(
        description="Simulation du jeu de la vie de Conway.")
    parseur.add_argument(
        "-n", "--nb_cells", type=entier_strictement_positif, default=10,
        metavar="N",
        help="nombre de cellules par côté d'une grille aléatoire (défaut : 10)")
    parseur.add_argument(
        "-m", "--max_iterations", type=entier_positif_ou_nul, default=20,
        metavar="N",
        help="numéro de la dernière itération à calculer (défaut : 20)")
    parseur.add_argument(
        "-s", "--seed", type=convertir_en_entier, default=42, metavar="N",
        help="graine du générateur aléatoire (défaut : 42)")
    parseur.add_argument(
        "-o", "--output_directory", default="outputs", metavar="DOSSIER",
        help="dossier d'écriture des images (défaut : outputs)")
    parseur.add_argument(
        "-t", "--output_type", choices=["image", "text"], default="image",
        metavar="TYPE",
        help="type de sortie : image ou text (défaut : image)")
    parseur.add_argument(
        "-p", "--periodic", action="store_true",
        help="conditions aux limites périodiques (grille en tore)")
    return parseur.parse_args(argv)


# ---------------------------------------------------------------------------
# Grille initiale
# ---------------------------------------------------------------------------

def creer_grille_aleatoire(taille, graine):
    """Grille carrée aléatoire, identique pour une même taille et une même graine."""
    generateur = random.Random(graine)
    return [[generateur.choice([0, 1]) for _ in range(taille)]
            for _ in range(taille)]


def lire_stdin_si_fournie():
    """Renvoie le texte reçu sur STDIN, ou None si aucune grille n'est fournie.

    Aucune grille n'est fournie si STDIN est le terminal, ou s'il est vide
    (zéro caractère), par exemple quand le programme est lancé par un script
    sans entrée.
    """
    if sys.stdin.isatty():
        return None
    contenu = sys.stdin.read()
    if contenu == "":
        return None
    return contenu


def lire_grille(texte):
    """Transforme le texte reçu sur STDIN en liste de listes de 0 et de 1.

    Format : première ligne = taille N, puis N lignes de N valeurs 0/1
    séparées par des espaces.
    """
    lignes = texte.splitlines()
    while lignes and lignes[-1].strip() == "":
        lignes.pop()                      # ignore les lignes vides finales
    if not lignes:
        raise ErreurEntree("la grille fournie est vide")

    try:
        taille = int(lignes[0].strip())
    except ValueError:
        raise ErreurEntree(
            "la première ligne doit contenir la taille de la grille (un entier)")
    if taille <= 0:
        raise ErreurEntree(f"la taille doit être strictement positive (reçu : {taille})")

    lignes_grille = lignes[1:]
    if len(lignes_grille) != taille:
        raise ErreurEntree(
            f"{taille} lignes attendues après la taille, {len(lignes_grille)} reçues")

    grille = []
    for numero, ligne in enumerate(lignes_grille, start=2):
        cellules = ligne.split()
        if len(cellules) != taille:
            raise ErreurEntree(
                f"ligne {numero} : {taille} cellules attendues, {len(cellules)} reçues")
        for cellule in cellules:
            if cellule not in ("0", "1"):
                raise ErreurEntree(
                    f"ligne {numero} : cellule invalide '{cellule}' (0 ou 1 attendu)")
        grille.append([int(cellule) for cellule in cellules])
    return grille


# ---------------------------------------------------------------------------
# Calcul d'une génération
# ---------------------------------------------------------------------------

def compter_voisines(grille, i, j, periodique):
    """Nombre de voisines vivantes de la case (ligne i, colonne j)."""
    taille = len(grille)
    total = 0
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue                  # la case elle-même n'est pas sa voisine
            vi = i + di
            vj = j + dj
            if periodique:
                vi %= taille              # le bord opposé prend le relais
                vj %= taille
            elif vi < 0 or vi >= taille or vj < 0 or vj >= taille:
                continue                  # hors grille = cellule morte
            total += grille[vi][vj]
    return total


def appliquer_regles(etat, voisines):
    """Nouvel état (0 ou 1) d'une cellule selon les règles de Conway."""
    if etat == 1:
        return 1 if voisines in (2, 3) else 0
    return 1 if voisines == 3 else 0


def generation_suivante(grille, periodique):
    """Calcule la génération suivante, sans modifier la grille reçue."""
    taille = len(grille)
    nouvelle = [[0] * taille for _ in range(taille)]
    for i in range(taille):
        for j in range(taille):
            voisines = compter_voisines(grille, i, j, periodique)
            nouvelle[i][j] = appliquer_regles(grille[i][j], voisines)
    return nouvelle


def simuler(grille, iterations, periodique):
    """Renvoie la grille obtenue après le nombre d'itérations demandé."""
    for _ in range(iterations):
        grille = generation_suivante(grille, periodique)
    return grille


# ---------------------------------------------------------------------------
# Sorties
# ---------------------------------------------------------------------------

def formater_grille(grille):
    """Texte de la grille : une ligne par ligne, cellules séparées par un espace."""
    return "\n".join(" ".join(str(cellule) for cellule in ligne)
                     for ligne in grille)


def ecrire_texte(grille, iteration):
    """Sortie texte sur STDOUT : 'iteration: N' puis la grille, rien d'autre."""
    print(f"iteration: {iteration}")
    print(formater_grille(grille))


def ecrire_images(grille, iterations, periodique, dossier):
    """Écrit une image par génération, de 0 à `iterations` incluse."""
    os.makedirs(dossier, exist_ok=True)
    for numero in range(iterations + 1):
        nom_fichier = os.path.join(dossier, f"grid_{numero:04d}.png")
        write_grid(matrix=grille, filename=nom_fichier)
        if numero < iterations:
            grille = generation_suivante(grille, periodique)
    print(f"Generation of {iterations + 1} images in directory {dossier}")


# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------

def main():
    args = lire_arguments()
    try:
        texte = lire_stdin_si_fournie()
        if texte is None:
            grille = creer_grille_aleatoire(args.nb_cells, args.seed)
        else:
            grille = lire_grille(texte)

        if args.output_type == "text":
            finale = simuler(grille, args.max_iterations, args.periodic)
            ecrire_texte(finale, args.max_iterations)
        else:
            ecrire_images(grille, args.max_iterations, args.periodic,
                          args.output_directory)
    except ErreurEntree as erreur:
        print(f"Erreur : {erreur}", file=sys.stderr)
        return 1
    except OSError as erreur:
        print(f"Erreur d'écriture : {erreur}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())