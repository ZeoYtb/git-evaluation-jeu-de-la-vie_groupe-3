
import argparse
import random
import sys
import os

from lib import write_grid


# Création de la grille de départ
# J'ai créé cette fonction pour générer une grille carrée remplie
# aléatoirement de 0 et de 1. La graine permet de retrouver
# la même grille si on utilise la même valeur.
def create_grid(size, seed):
    generator = random.Random(seed)

    return [
        [generator.randint(0, 1) for j in range(size)]
        for i in range(size)
    ]


# Comptage des voisins
# Pour chaque cellule, je regarde les 8 cases qui l'entourent
# afin de compter combien sont vivantes.
# J'ai aussi ajouté la possibilité d'utiliser des limites périodiques :
# les bords de la grille sont alors reliés entre eux.
def count_neighbors(grid, row, column, periodic):
    size = len(grid)
    count = 0

    for i in range(-1, 2):
        for j in range(-1, 2):

            if i == 0 and j == 0:
                continue

            r = row + i
            c = column + j

            if periodic:
                count += grid[r % size][c % size]

            elif 0 <= r < size and 0 <= c < size:
                count += grid[r][c]

    return count


# Calcul de la génération suivante
# J'ai créé une nouvelle grille pour calculer les changements
# sans modifier la génération précédente.
# J'applique ici les règles du Jeu de la vie :
# une cellule vivante survit avec 2 ou 3 voisins vivants,
# une cellule morte devient vivante avec exactement 3 voisins.
def next_generation(grid, periodic):
    size = len(grid)
    new_grid = []

    for row in range(size):
        new_row = []

        for column in range(size):

            neighbors = count_neighbors(
                grid, row, column, periodic
            )

            if grid[row][column] == 1:
                if neighbors in (2, 3):
                    new_row.append(1)
                else:
                    new_row.append(0)

            else:
                if neighbors == 3:
                    new_row.append(1)
                else:
                    new_row.append(0)

        new_grid.append(new_row)

    return new_grid


# Affichage de la grille en mode texte
# Cette fonction permet d'afficher les cellules sous forme de 0 et de 1.
def print_grid(grid):
    for row in grid:
        print(" ".join(map(str, row)))


# Animation du Jeu de la vie dans Carnets
# J'ai ajouté cette fonction pour voir les générations évoluer directement
# dans le notebook. Les cellules vivantes sont noires et les cellules
# mortes blanches. La grille est actualisée à chaque génération.
def show_animation(grid, periodic, iterations):
    import matplotlib.pyplot as plt
    from IPython.display import display, clear_output

    plt.ioff()

    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor("white")

    for iteration in range(iterations + 1):

        ax.clear()
        ax.set_facecolor("white")

        ax.imshow(
            grid,
            cmap="gray_r",
            vmin=0,
            vmax=1,
            interpolation="nearest"
        )

        size = len(grid)

        ax.set_xticks(
            [x - 0.5 for x in range(size + 1)],
            minor=True
        )

        ax.set_yticks(
            [y - 0.5 for y in range(size + 1)],
            minor=True
        )

        ax.grid(
            which="minor",
            color="white",
            linewidth=0.7
        )

        ax.tick_params(
            left=False,
            bottom=False,
            labelleft=False,
            labelbottom=False
        )

        ax.set_title(
            f"GENERATION {iteration}",
            color="black",
            fontsize=14
        )

        display(fig)
        plt.pause(0.15)
        clear_output(wait=True)

        if iteration < iterations:
            grid = next_generation(grid, periodic)

    plt.close(fig)


# Vérification des paramètres
# Ces deux fonctions permettent de vérifier les valeurs saisies :
# le nombre de cellules doit être supérieur à zéro,
# tandis que le nombre de générations peut être égal à zéro.
def positive_integer(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "La valeur doit etre un entier."
        )

    if number <= 0:
        raise argparse.ArgumentTypeError(
            "La valeur doit etre strictement positive."
        )

    return number


def non_negative_integer(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "La valeur doit etre un entier."
        )

    if number < 0:
        raise argparse.ArgumentTypeError(
            "La valeur doit etre positive ou nulle."
        )

    return number


# Configuration des options du programme
# J'utilise argparse pour permettre à l'utilisateur de choisir
# la taille de la grille, le nombre de générations, la graine,
# le dossier de sortie et le type d'affichage.
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Jeu de la vie de Conway"
    )

    parser.add_argument(
        "-n", "--nb_cells",
        type=positive_integer,
        default=30,
        help="Nombre de cellules par cote"
    )

    parser.add_argument(
        "-m", "--max_iterations",
        type=non_negative_integer,
        default=200,
        help="Nombre de generations"
    )

    parser.add_argument(
        "-s", "--seed",
        type=int,
        default=42,
        help="Graine aleatoire"
    )

    parser.add_argument(
        "-o", "--output_directory",
        default="outputs",
        help="Dossier de destination des images"
    )

    parser.add_argument(
        "-t", "--output_type",
        choices=["image", "text"],
        default="image",
        help="Type de sortie"
    )

    parser.add_argument(
        "-p", "--periodic",
        action="store_true",
        help="Activer les limites periodiques"
    )

    if "ipykernel" in sys.modules:
        return parser.parse_args(args=[])

    return parser.parse_args()


# Fonction principale
# Elle rassemble les différentes étapes du programme :
# récupération des paramètres, création ou lecture de la grille,
# calcul des générations et affichage des résultats.
def main():
    arguments = parse_arguments()

    #Je génère une grille.
    # Sinon, je récupère la matrice fournie en entrée.
    if "ipykernel" in sys.modules or sys.stdin.isatty():

        grid = create_grid(
            arguments.nb_cells,
            arguments.seed
        )

    else:

        content = sys.stdin.read().splitlines()

        if not content:
            raise ValueError("La grille est vide.")

        size = int(content[0])

        if size <= 0 or len(content) != size + 1:
            raise ValueError("Matrice incorrecte.")

        grid = []

        for line in content[1:]:

            row = [int(value) for value in line.split()]

            if len(row) != size:
                raise ValueError("Matrice incorrecte.")

            if any(value not in (0, 1) for value in row):
                raise ValueError("Les cellules doivent etre 0 ou 1.")

            grid.append(row)

    # Mode texte : je calcule toutes les générations demandées
    # puis j'affiche uniquement la grille finale.
    if arguments.output_type == "text":

        for iteration in range(arguments.max_iterations):
            grid = next_generation(
                grid,
                arguments.periodic
            )

        print("iteration:", arguments.max_iterations)
        print_grid(grid)

        return

    # Mode image : j'enregistre chaque génération dans un fichier PNG.
    # Je crée d'abord le dossier de sortie s'il n'existe pas.
    os.makedirs(
        arguments.output_directory,
        exist_ok=True
    )

    current_grid = [row[:] for row in grid]

    for iteration in range(arguments.max_iterations + 1):

        filename = os.path.join(
            arguments.output_directory,
            f"grid_{iteration:04d}.png"
        )

        write_grid(current_grid, filename)

        current_grid = next_generation(
            current_grid,
            arguments.periodic
        )

    # Dans une exécution classique, j'affiche le nombre d'images créées.
    if "ipykernel" in sys.modules:

        show_animation(
            grid,
            arguments.periodic,
            arguments.max_iterations
        )

    else:

        print(
            f"Generation of {arguments.max_iterations + 1} images "
            f"in directory {arguments.output_directory}"
        )


# Lancement du programme et gestion des erreurs
if __name__ == "__main__":

    try:
        main()

    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
