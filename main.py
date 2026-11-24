import sys

from game_functions import (
    ecrire_images,
    ecrire_texte,
    lire_arguments,
    lire_grille,
    lire_stdin_si_fournie,
    random_grille,
    simuler,
)


def main():
    args = lire_arguments()
    try:
        texte = lire_stdin_si_fournie()
        if texte is None:
            grille = random_grille(args.nb_cells, args.nb_cells, args.seed)
        else:
            grille = lire_grille(texte)

        if args.output_type == "text":
            finale = simuler(grille, args.max_iterations, args.periodic)
            ecrire_texte(finale, args.max_iterations)
        else:
            ecrire_images(grille, args.max_iterations, args.periodic,
                          args.output_directory)
    except ValueError as erreur:
        print(f"Erreur : {erreur}", file=sys.stderr)
        return 1
    except OSError as erreur:
        print(f"Erreur d'écriture : {erreur}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
