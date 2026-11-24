from dataclasses import dataclass
import random

@dataclass
class Grille:
    width: int
    height: int
    cells: list[list[int]]

def nouvelle_grille(w: int, h:int) -> Grille | None:  #returns Grid or None
    if w <= 0 or h <= 0: return None

    cells = [[0 for _ in range(w)] for _ in range(h)]  #creates a grid of 0s
    return Grille(width=w, height=h, cells=cells)

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