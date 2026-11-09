```text

TYPE Grid
    DECLARE width, height as INT
    DECLARE cells[width, height] as BOOL     //TRUE = live; cells[0,0] exists
ENDTYPE

TYPE Checklist
    DECLARE x as INT
    DECLARE y as INT
ENDTYPE

FUNCTION Create_grid(w, h)
    IF (w <= 0 OR h <= 0) THEN RETURN NULL

    DECLARE new_grid as Grid
    
    new_grid.width = w
    new_grid.height = h

    DECLARE i, j as INT

    FOR i = 0 to w
        FOR j = 0 to h: new_grid.cells[i,j] = FALSE
    NEXT i

    RETURN new_grid
ENDFUNCTION

FUNCTION Update_grid(grid)
    DECLARE i, j as INT
    FOR i = 0 to grid.width
        FOR j = 0 to grid.height: grid.cells[i,j] = Check_rules(grid, i, j)
    NEXT i

    RETURN grid
ENDFUNCTION

FUNCTION Check_rules(grid, x, y)
    DECLARE n as INT = Count_neighbours(grid, x, y)
    DECLARE state as BOOL = grid.cells[x,y]

    IF state = TRUE THEN
        IF (n < 2 OR n > 3) THEN state = FALSE
    ELSE
        IF n = 3 THEN state = TRUE
    ENDIF

    RETURN state
ENDFUNCTION

FUNCTION Count_neighbours(grid, x, y)
    DECLARE n as INT = 0
    DECLARE p as INT = 0
    DECLARE checked[grid.width * grid.height] as Checklist

    IF x = 0 THEN Check_y_left_x(grid, checked, x, y, n)
    ELSEIF x > 0 AND x < grid.width THEN Check_y_mid_x(grid, checked, x, y, n)
    ELSE Check_y_right_x(grid, checked, x, y, n)

    RETURN n
ENDFUNCTION

PROCEDURE Check_y_left_x(grid, checked, x, y, n)
    IF y = 0 THEN
        FOR i = x to x + 1
            FOR j = y to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF (x in checked[].x AND y in checked[].y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                ENDIF
            NEXT j
        NEXT i
    ELSEIF y > 0 AND y < grid.height THEN
        FOR i = x to x + 1
            FOR j = y - 1 to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF (x in checked[].x AND y in checked[].y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                ENDIF
            NEXT j
        NEXT i
    ELSE
        FOR i = x to x + 1
            FOR j = y - 1 to y
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF (x in checked[].x AND y in checked[].y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                ENDIF
            NEXT j
        NEXT i
    ENDIF
ENDPROCEDURE

PROCEDURE Check_y_mid_x(grid, checked, x, y, n)
    IF y = 0 THEN
        FOR i = x - 1 to x + 1
            FOR j = y to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF (x in checked[].x AND y in checked[].y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                ENDIF
            NEXT j
        NEXT i
    ELSEIF y > 0 AND y < grid.height THEN
        FOR i = x - 1 to x + 1
            FOR j = y - 1 to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF (x in checked[].x AND y in checked[].y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                ENDIF
            NEXT j
        NEXT i
    ELSE
        FOR i = x - 1 to x + 1
            FOR j = y - 1 to y
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF (x in checked[].x AND y in checked[].y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                ENDIF
            NEXT j
        NEXT i
    ENDIF
ENDPROCEDURE

PROCEDURE Check_y_right_x(grid, checked, x, y, n)
    IF y = 0 THEN
        FOR i = x - 1 to x
            FOR j = y to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF (x in checked[].x AND y in checked[].y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                ENDIF
            NEXT j
        NEXT i
    ELSEIF y > 0 AND y < grid.height THEN
        FOR i = x - 1 to x
            FOR j = y - 1 to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF (x in checked[].x AND y in checked[].y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                ENDIF
            NEXT j
        NEXT i
    ELSE
        FOR i = x - 1 to x
            FOR j = y - 1 to y
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF (x in checked[].x AND y in checked[].y) THEN CONTINUE
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                ENDIF
            NEXT j
        NEXT i
    ENDIF
ENDPROCEDURE

//last minute thought: does the grid wrap around itself or is it bounded??? If it's bounded i'm gonna have to rework sooooo many ifs
//currently rereading instructions: replace TRUE/FALSE with 1/0
//by default, the grid has an edge; the option -p or --periodic, i.e. the horizontal and vertical edges wrap around each other
//currently adding a checklist for counting neighbours

FUNCTION Is_neighbour(i, j, x, y)
    IF (i = x AND j = y) THEN RETURN FALSE
    ELSE RETURN TRUE
ENDFUNCTION

```