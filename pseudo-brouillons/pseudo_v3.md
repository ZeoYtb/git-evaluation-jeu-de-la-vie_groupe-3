```text

TYPE Grid
    DECLARE width, height as INT
    DECLARE cells[width, height] as INT     //cells[0,0] exists
ENDTYPE

FUNCTION Create_grid(w, h)
    IF (w <= 0 OR h <= 0) THEN RETURN NULL

    DECLARE new_grid as Grid
    
    new_grid.width = w - 1
    new_grid.height = h - 1

    DECLARE i, j as INT

    FOR i = 0 to w
        FOR j = 0 to h: new_grid.cells[i,j] = 0
    NEXT i

    RETURN new_grid
ENDFUNCTION

FUNCTION Update_grid(grid, periodic)
    DECLARE new_state as Grid = Create_grid(grid.width, grid.height)

    FOR INT i = 0 to grid.height - 1
        FOR INT j = 0 to grid.width - 1
            DECLARE live as INT = Count_neighbours(grid, i, j, periodic)        //no. of live neighbours
            new_state.cells[i,j] = Update_state(grid.cells[i,j], live)
        NEXT j
    NEXT i

    RETURN new_state
ENDFUNCTION

FUNCTION Count_neighbours(grid, i, j, periodic)
    DECLARE live as INT = 0     
    FOR INT di = -1 to 1
        FOR INT dj = -1 to 1
            IF (di = 0 AND dj = 0) THEN CONTINUE
            
            DECLARE vi = i + di
            DECLARE vj = j + dj
            
            IF periodic THEN            //grid wraps around
                vi = vi MOD grid.height
                vj = vj MOD grid.width
            ELSEIF (vi < 0 OR vi >= grid.height OR vj < 0 OR vj >= grid.width) THEN
                CONTINUE
            ENDIF
            
            live += grid.cells[vi,vj]
        NEXT dj
    NEXT di
    
    RETURN live

ENDFUNCTION

FUNCTION Update_state(state, live)                          //updates cell [i,j] against set rules
    IF state = 1 AND (live = 2 OR live = 3) THEN RETURN 1
    ELSEIF state = 0 AND live = 3 THEN RETURN 1
    ELSE RETURN 0
ENDFUNCTION

```