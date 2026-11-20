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
    for di in range(-1, 2):         #offset i
        for dj in range(-1, 2):     #offset j
            if di == 0 and dj == 0: continue  #skip current cell

            vi = i + di
            vj = j + dj

            if periodic:    #grid wraps around
                vi = vi % grid.height
                vj = vj % grid.width
            else:
                if vi < 0 or vj < 0 or vi >= grid.height or vj >= grid.width:
                    continue

            live += grid.cells[vi][vj]

    return live

def MAJ_cellule(state: int, live: int):    #checks rules, updates cells
    if state == 1 and (live == 2 or live == 3): return 1
    elif state == 0 and live == 3: return 1
    else: return 0