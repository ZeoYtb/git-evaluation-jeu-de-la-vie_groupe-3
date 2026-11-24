# Jeu de la vie — Groupe 3

## Sommaire

- [Présentation](#présentation)
- [Membres du groupe](#membres-du-groupe)
- [Règles du jeu](#règles-du-jeu)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [Options du programme](#options-du-programme)
  - [Exemples d'utilisation](#exemples-dutilisation)
  - [Tests](#tests)
  - [Sorties générées](#sorties-générées)
- [Vidéos du projet](#vidéos-du-projet)
- [À propos](#à-propos)
- [Liens utiles](#liens-utiles)

---

## Présentation

Ce projet consiste à réaliser une implémentation du **Jeu de la vie de Conway** en Python, dans le cadre d’une évaluation portant sur l’utilisation de Git et le travail collaboratif.
Le Jeu de la vie est un automate cellulaire imaginé par le mathématicien John Conway. Il repose sur un ensemble de cellules disposées sur une grille, qui peuvent être vivantes ou mortes. À partir d’une configuration initiale, ces cellules évoluent au fil des générations en suivant des règles précises.
Même si le jeu ne possède aucun joueur et aucune action directe, il permet d’observer des comportements et des motifs qui apparaissent, disparaissent, se déplacent ou se reproduisent au cours de la simulation.
L’objectif du projet est de développer un programme capable de créer une grille, de simuler l’évolution des cellules et de représenter les différentes générations obtenues.

## Membres du groupe

- Sania HASSANALY — 45004337
- Maya LOUAFI — 45000708
- Raphaël MONFORT — 45001607
- Danish PUTTYAH — 45003583

## Règles du jeu

Chaque cellule possède deux états :

- `0` : cellule morte
- `1` : cellule vivante

Chaque cellule possède huit voisines au maximum : les cellules situées horizontalement, verticalement et diagonalement autour d’elle.

À chaque génération, les règles suivantes sont appliquées :

- Une cellule vivante ayant moins de deux voisins vivants meurt par sous-population.
- Une cellule vivante ayant deux ou trois voisins vivants survit.
- Une cellule vivante ayant plus de trois voisins vivants meurt par surpopulation.
- Une cellule morte ayant exactement trois voisins vivants devient vivante.

L’ensemble des cellules évolue simultanément. La nouvelle génération est calculée à partir de l’état précédent de la grille, ce qui permet de respecter les règles du jeu.

## Fonctionnalités

Le programme propose plusieurs fonctionnalités permettant de personnaliser et d’observer la simulation du Jeu de la vie.

- **Génération d’une grille aléatoire :** création d’une grille carrée contenant des cellules vivantes et mortes.
- **Personnalisation de la taille :** choix du nombre de lignes et de colonnes de la grille, qui reste carrée.
- **Reproductibilité :** utilisation d’une seed permettant de retrouver la même grille initiale lors de plusieurs exécutions.
- **Simulation des générations :** choix du nombre d’itérations à effectuer afin d’observer l’évolution des cellules.
- **Affichage en mode texte :** représentation des cellules directement dans le terminal.
- **Génération d’images :** création d’images PNG représentant les différentes générations de la simulation.
- **Personnalisation du dossier de sortie :** choix du répertoire dans lequel les images générées seront enregistrées.
- **Bords périodiques :** possibilité de relier les bords de la grille afin que les cellules situées sur un bord puissent considérer celles de l’autre côté comme leurs voisines.
- **Grille fournie en entrée :** possibilité de démarrer la simulation à partir d’une configuration définie par l’utilisateur plutôt que d’une grille aléatoire.

## Prérequis

Pour utiliser le programme, les éléments suivants sont nécessaires :

- Python 3 pour exécuter le programme.
- Git pour récupérer le projet et gérer les différentes versions du code.
- Les fichiers du projet, notamment `main.py` et `lib.py`.

Pour générer les vidéos de présentation du projet, les logiciels suivants sont également nécessaires :

- **FFmpeg :** permet de créer une vidéo à partir des images générées.
- **Gource :** permet de visualiser l’historique et l’évolution du dépôt Git.

## Installation

Commencez par récupérer le dépôt GitHub :

```bash
git clone <URL_DU_DEPOT>
```

Accédez ensuite au répertoire du projet :

```bash
cd git-evaluation-jeu-de-la-vie_groupe-3
```

Le programme peut ensuite être exécuté à partir de ce répertoire.

Sur Ubuntu ou Debian, les outils nécessaires peuvent être installés avec les commandes suivantes :

```bash
sudo apt update
sudo apt install python3 git gource ffmpeg
```

## Utilisation

Le programme peut être lancé sans argument. Dans ce cas, les paramètres par défaut sont utilisés pour générer et simuler une grille.

```bash
python3 main.py
```

Il est également possible de modifier le fonctionnement de la simulation grâce aux options disponibles.

### Options du programme

| Option | Description | Valeur par défaut |
|---|---|---|
| `-n`, `--nb_cells` | Définit la taille de la grille carrée (nombre de lignes et de colonnes). | `10` |
| `-m`, `--max_iterations` | Définit le nombre de générations à simuler. | `20` |
| `-s`, `--seed` | Définit la seed du générateur aléatoire pour reproduire une même grille. | `42` |
| `-o`, `--output_directory` | Définit le répertoire dans lequel les images générées seront enregistrées. | `Outputs` |
| `-t`, `--output_type` | Choisit le format de sortie : image ou texte. | `Image` |
| `-p`, `--periodic` | Active les bords périodiques de la grille. | Désactivé |
| `-h`, `--help` | Affiche l'aide et les options disponibles. | — |

Le nombre d’itérations correspond au nombre de générations calculées après la génération initiale. Par exemple, avec `-m 20`, la simulation commence à la génération 0 et va jusqu'à la génération 20.

### Exemples d'utilisation

**Créer une grille de 10 × 10 cellules :**

```bash
python3 main.py -n 10
```

**Simuler 5 générations :**

```bash
python3 main.py -m 5
```

**Afficher la grille en mode texte :**

```bash
python3 main.py -t text
```

**Générer les images dans le dossier outputs :**

```bash
python3 main.py -t image -o outputs
```

**Utiliser une seed afin de reproduire la génération aléatoire :**

```bash
python3 main.py -s 42
```

**Activer les bords périodiques :**

```bash
python3 main.py -p
```

**Combiner plusieurs options pour personnaliser la simulation :**

```bash
python3 main.py -n 10 -m 20 -s 42 -t image -p
```

Ces options peuvent être combinées afin de choisir la taille de la grille, le nombre de générations, le mode d’affichage et les conditions de simulation.

Il est également possible de fournir une grille en entrée à l’aide de l’entrée standard. Par exemple, pour utiliser une configuration de test :

```bash
cat tests/matrix3/input.txt | python3 main.py
```

*Remarque : le nom et le chemin du fichier sont à adapter selon les fichiers réellement présents dans le dossier de tests.*

### Tests

Des scripts de vérification sont fournis avec le projet afin de contrôler le fonctionnement du programme et de vérifier que les options respectent les résultats attendus.

Le script `check_tests.sh` permet de vérifier le fonctionnement du Jeu de la vie à partir de différents tests :

```bash
sh check_tests.sh
```

Le script `check_script_options.sh` permet de vérifier la gestion des arguments et les différentes options du programme :

```bash
sh check_script_options.sh
```

Ces tests permettent de détecter d’éventuelles erreurs et de s’assurer que le programme respecte les contraintes attendues.

### Sorties générées

Lorsque le programme est exécuté en mode image, les différentes générations sont enregistrées sous forme de fichiers PNG dans le répertoire de sortie.

Le dossier utilisé peut être défini avec l’option `-o`. Si aucun répertoire n’est spécifié, les images sont enregistrées dans le dossier `outputs`.

En mode texte, les résultats sont directement affichés dans le terminal.

Les images générées sont nommées selon le format `grid_XXXX.png`, où `XXXX` représente le numéro de la génération correspondante.

Par exemple :

```text
outputs/
├── grid_0000.png
├── grid_0001.png
├── grid_0002.png
├── grid_0003.png
└── ...
```

Ces images peuvent ensuite être utilisées pour créer une vidéo présentant l’évolution de la simulation.

## Vidéos du projet

Deux vidéos sont prévues pour présenter le projet et son évolution :

- **Simulation du Jeu de la vie :** présentation visuelle de l’évolution des cellules au cours des générations.

  [Voir la vidéo de simulation](https://youtube.com/shorts/pTzeKftaQ3U?feature=share)

- **Historique Git avec Gource :** visualisation de l’évolution du dépôt et du travail effectué par les membres du groupe.

  [Voir la vidéo de l'historique Git avec Gource](https://youtu.be/sNoQFDtsh8E)

Les vidéos peuvent être générées à partir des images produites par le programme et de l’historique du dépôt Git.

**Exemple de génération des images destinées à la vidéo :**

```bash
python3 main.py -n 50 -m 2000 -s 4200 -t image
```

**Création de la vidéo à partir des images avec FFmpeg :**

```bash
ffmpeg -framerate 20 -i outputs/grid_%04d.png -c:v libx264 -pix_fmt yuv420p jeu_de_la_vie.mp4
```

**Visualisation de l’historique du dépôt avec Gource :**

```bash
gource --output-framerate 20 --seconds-per-day 0.1 --auto-skip-seconds 1 -1280x720 -o - | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -pix_fmt yuv420p -crf 18 -threads 0 -bf 0 gource.mp4
```

*Remarque : ces commandes sont à adapter si les chemins ou les noms des fichiers générés sont différents.*

Les images et les vidéos générées sont des fichiers de sortie. Elles n’ont pas besoin d’être ajoutées au dépôt Git si elles sont exclues par le fichier `.gitignore`.

## À propos

Ce projet est réalisé dans le cadre d’une évaluation universitaire autour de Git, du développement Python et du travail collaboratif.

Il permet également de mettre en pratique la gestion de versions, l’organisation du code, la collaboration entre plusieurs développeurs et le suivi de l’évolution d’un projet.

## Liens utiles

- [An Introduction to Conway's The Game of Life](https://youtu.be/ouipbDkwHWA?si=IuqA-GTtExhdbaAh) : vidéo présentant le Jeu de la vie de Conway et son fonctionnement.
- [Le Jeu de la Vie](https://youtu.be/eMn43As24Bo) : vidéo en français permettant de mieux comprendre le fonctionnement et les évolutions du Jeu de la vie.
- [Conway's Game of Life, Explained Visually](https://youtu.be/rBaK4-EoF_8?si=SQ8nhDv2lRGpByUJ) : explication visuelle des règles et du comportement des cellules au fil des générations.
- [Documentation officielle de FFmpeg](https://ffmpeg.org/documentation.html) : documentation de l'outil utilisé pour encoder et convertir les vidéos, notamment au format MP4.
- [Documentation de Gource](https://github.com/acaudwell/Gource/wiki) : documentation de l'outil permettant de visualiser graphiquement l'évolution de l'historique d'un dépôt Git et de générer une vidéo de son activité.
