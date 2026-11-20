
def creer_grille(nb_lignes, nb_colonnes):
    grille = []

    for i in range(nb_lignes):
        ligne = []

        for j in range(nb_colonnes):
            ligne.append(0)

        grille.append(ligne)

    return grille


def afficher_voisins(grille, i, j):
    nb_lignes = len(grille)
    nb_colonnes = len(grille[0])

    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):

            if x >= 0 and x < nb_lignes:
                if y >= 0 and y < nb_colonnes:

                    if x != i or y != j:
                        print(grille[x][y])


def compter_voisins(grille, i, j):
    nb_lignes = len(grille)
    nb_colonnes = len(grille[0])

    nb_voisins = 0

    for x in range(-1, 2):
        for y in range(-1, 2):

            if x != 0 or y != 0:
                pos_x = (i + x) % nb_lignes
                pos_y = (j + y) % nb_colonnes

                nb_voisins = nb_voisins + grille[pos_x][pos_y]

    return nb_voisins


def calculer_cellule(etat_cellule, nb_voisins):

    if etat_cellule == 0 and nb_voisins == 3:
        return 1

    elif etat_cellule == 1 and 2 <= nb_voisins <= 3:
        return 1

    else:
        return 0


def generation_suivante(grille):
    nb_lignes = len(grille)
    nb_colonnes = len(grille[0])

    nouvelle_grille = creer_grille(nb_lignes, nb_colonnes)

    for i in range(nb_lignes):
        for j in range(nb_colonnes):

            etat_cellule = grille[i][j]

            nb_voisins = compter_voisins(grille, i, j)

            nouvelle_grille[i][j] = calculer_cellule(
                etat_cellule, nb_voisins
            )

    return nouvelle_grille


def initialiser_cellules(grille):
    grille[4][3] = 1
    grille[4][4] = 1
    grille[4][5] = 1

    return grille


def afficher_grille(grille):

    for i in range(len(grille)):
        for j in range(len(grille[0])):

            if grille[i][j] == 1:
                print("O", end=" ")
            else:
                print(".", end=" ")

        print()


def jeu_de_la_vie():

    nb_lignes = 10
    nb_colonnes = 10

    grille = creer_grille(nb_lignes, nb_colonnes)

    grille = initialiser_cellules(grille)

    print("Generation initiale :")
    afficher_grille(grille)

    for generation in range(1, 11):

        grille = generation_suivante(grille)

        print("Generation :", generation)

        afficher_grille(grille)



jeu_de_la_vie()   