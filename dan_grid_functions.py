from dataclasses import dataclass

@dataclass
class Grille:
    width: int
    height: int
    cells: list[list[int]]

def Nouvelle_grille(w: int, h:int) -> Grille | None:  #returns Grid or None
    if w <= 0 or h <= 0: return None

    cells = [[0 for _ in range(w)] for _ in range(h)]
    return Grille(width=w, height=h, cells=cells)

def MAJ_grille(grid: Grille, periodic: bool) -> Grille:
    new_state = Nouvelle_grille(grid.width, grid.height)

    if new_state is None: raise ValueError("Erreur dimensions : height > 0,  width > 0")
    #stops function and signals error value, i.e. dimensions < 0

    for i in range(0, grid.height):
        for j in range(0, grid.width):
            live = Compter_voisins(grid, i, j, periodic)
            new_state.cells[i][j] = MAJ_cellule(grid.cells[i][j], live)
    return new_state

def Compter_voisins(grid: Grille, i: int, j: int, periodic: bool) -> int:   #returns no. of live neighbours
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

def MAJ_cellule(state: int, live: int):    #checks rules, updates cells
    if state == 1 and (live == 2 or live == 3): return 1
    elif state == 0 and live == 3: return 1
    else: return 0