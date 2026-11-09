```text

TYPE Grid
    DEFINE width, height as INT
    DEFINE cells[width, height] as BOOL     //TRUE = live; cells[0,0] exists
ENDTYPE

FUNCTION Create_grid(w, h)
    IF (w < 0 OR h < 0) THEN RETURN NULL

    DEFINE new_grid as Grid
    
    new_grid.width = w
    new_grid.height = h

    DEFINE i, j as INT

    FOR i = 0 to w
        FOR j = 0 to h: new_grid.cells[i,j] = FALSE
    NEXT i

    RETURN new_grid
ENDFUNCTION

FUNCTION Update_grid(grid)
    DEFINE i, j as INT
    FOR i = 0 to grid.width
        FOR j = 0 to grid.height: grid.cells[i,j] = Check_rules(grid, i, j)
    NEXT i

    RETURN grid
ENDFUNCTION

FUNCTION Check_rules(grid, x, y)
    DEFINE n as INT = Count_neightbours(grid, x, y)
    DEFINE state as BOOL = grid.cells[x,y]

    IF state = TRUE THEN
        IF (n < 2 AND n > 3) THEN state = FALSE
    ELSE
        IF n = 3 THEN state = TRUE
    ENDIF

    RETURN state
ENDFUNCTION

FUNCTION Count_neightbours(grid, x, y)
    DECLARE n as INT = 0

    IF x = 0 THEN Check_y_left_x(grid, x, y)
    ELSEIF x > 0 AND x < grid.width THEN Check_y_mid_x(grid, x, y)
    ELSE Check_y_right_x(grid, x, y)

    RETURN n
ENDFUNCTION

PROCEDURE Check_y_left_x(grid, x, y)
    IF y = 0 THEN
        FOR i = x to x + 1
            FOR j = y to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN n+=1
            NEXT j
        NEXT i
    ELSEIF y > 0 AND y < grid.height THEN
        FOR i = x to x + 1
            FOR j = y - 1 to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN n+=1
            NEXT j
        NEXT i
    ELSE
        FOR i = x to x + 1
            FOR j = y - 1 to y
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN n+=1
            NEXT j
        NEXT i
    ENDIF
ENDPROCEDURE

PROCEDURE Check_y_mid_x(grid, x, y)
    IF y = 0 THEN
        FOR i = x - 1 to x + 1
            FOR j = y to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN n+=1
            NEXT j
        NEXT i
    ELSEIF y > 0 AND y < grid.height THEN
        FOR i = x - 1 to x + 1
            FOR j = y - 1 to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN n+=1
            NEXT j
        NEXT i
    ELSE
        FOR i = x - 1 to x + 1
            FOR j = y - 1 to y
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN n+=1
            NEXT j
        NEXT i
    ENDIF
ENDPROCEDURE

PROCEDURE Check_y_right_x(grid, x, y)
    IF y = 0 THEN
        FOR i = x - 1 to x
            FOR j = y to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN n+=1
            NEXT j
        NEXT i
    ELSEIF y > 0 AND y < grid.height THEN
        FOR i = x - 1 to x
            FOR j = y - 1 to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN n+=1
            NEXT j
        NEXT i
    ELSE
        FOR i = x - 1 to x
            FOR j = y - 1 to y
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN n+=1
            NEXT j
        NEXT i
    ENDIF
ENDPROCEDURE

FUNCTION Is_neighbour(i, j, x, y)
    IF (i = x AND j = y) THEN RETURN FALSE
    ELSE RETURN TRUE
ENDFUNCTION

```