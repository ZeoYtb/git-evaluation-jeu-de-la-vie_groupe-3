from dataclasses import dataclass
import random
import argparse
import sys

@dataclass
class Grille:
    width: int
    height: int
    cells: list[list[int]]

def nouvelle_grille(w: int, h:int) -> Grille | None:  #returns Grid or None
    if w <= 0 or h <= 0: return None

    cells = [[0 for _ in range(w)] for _ in range(h)]  #creates a grid of 0s
    return Grille(width=w, height=h, cells=cells)

def convertir_en_entier(texte):
    try:
        return int(texte)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{texte}' n'est pas un entier")


def entier_strictement_positif(texte):
    valeur = convertir_en_entier(texte)
    if valeur <= 0:
        raise argparse.ArgumentTypeError(
            f"doit être strictement positif (reçu : {valeur})")
    return valeur


def entier_positif_ou_nul(texte):
    valeur = convertir_en_entier(texte)
    if valeur < 0:
        raise argparse.ArgumentTypeError(
            f"doit être positif ou nul (reçu : {valeur})")
    return valeur


def lire_arguments():
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
    return parseur.parse_args()

def lire_stdin_si_fournie():
    if sys.stdin.isatty():
        return None
    contenu = sys.stdin.read()
    if contenu == "":
        return None
    return contenu


def lire_grille(texte):
    lignes = texte.splitlines()
    while lignes and lignes[-1].strip() == "":
        lignes.pop()
    if not lignes:
        raise ValueError("la grille fournie est vide")

    try:
        taille = int(lignes[0].strip())
    except ValueError:
        raise ValueError(
            "la première ligne doit contenir la taille de la grille (un entier)")
    if taille <= 0:
        raise ValueError(f"la taille doit être strictement positive (reçu : {taille})")

    lignes_grille = lignes[1:]
    if len(lignes_grille) != taille:
        raise ValueError(
            f"{taille} lignes attendues après la taille, {len(lignes_grille)} reçues")

    cells = []
    for numero, ligne in enumerate(lignes_grille, start=2):
        valeurs = ligne.split()
        if len(valeurs) != taille:
            raise ValueError(
                f"ligne {numero} : {taille} cellules attendues, {len(valeurs)} reçues")
        for valeur in valeurs:
            if valeur not in ("0", "1"):
                raise ValueError(
                    f"ligne {numero} : cellule invalide '{valeur}' (0 ou 1 attendu)")
        cells.append([int(valeur) for valeur in valeurs])
    return Grille(width=taille, height=taille, cells=cells)


def random_grille(w: int, h:int, seed:int) -> Grille | None:  #returns Grid or None
    if w <= 0 or h <= 0: return None

    generator = random.Random(seed)

    cells = [[generator.randint(0,1) for _ in range(w)] for _ in range(h)]  #creates a random grid of 0s and 1s
    return Grille(width=w, height=h, cells=cells)

def next_gen(grid: Grille, periodic: bool) -> Grille:   #returns new grid
    new_state = nouvelle_grille(grid.width, grid.height)

    if new_state is None: raise ValueError("Erreur dimensions : height > 0,  width > 0")
    #stops function and signals error value, i.e. dimensions < 0

    for i in range(0, grid.height):
        for j in range(0, grid.width):
            live = compter_voisins(grid, i, j, periodic)
            new_state.cells[i][j] = maj_cellule(grid.cells[i][j], live)
    return new_state

def compter_voisins(grid: Grille, i: int, j: int, periodic: bool) -> int:   #returns no. of live neighbours
    live: int = 0
    for offset_h in range(-1, 2):
        for offset_w in range(-1, 2):
            if offset_h == 0 and offset_w == 0: continue  #skip current cell

            voisin_h = i + offset_h
            voisin_w = j + offset_w

            if periodic:    #grid wraps around
                voisin_h %= grid.height   #voisin_h = voisin_h % grid.height
                voisin_w %= grid.width
            else:
                if voisin_h < 0 or voisin_w < 0 or voisin_h >= grid.height or voisin_w >= grid.width:
                    continue

            live += grid.cells[voisin_h][voisin_w]

    return live

def maj_cellule(state: int, live: int):    #checks rules, updates cells
    if state == 1 and live in (2, 3): return 1
    elif state == 0 and live == 3: return 1
    else: return 0

