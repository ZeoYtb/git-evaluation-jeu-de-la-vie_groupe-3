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

FUNCTION Create_checklist(x, y)
    IF (x <= 0 OR y <= 0) THEN RETURN NULL

    DECLARE new_checklist[x*y] as Checklist

    DECLARE i as INT
    FOR i = 0 to len(new_checklist): new_checklist[i] = NULL

    RETURN new_checklist
ENDFUNCTION

FUNCTION Update_grid(grid)
    // Keep one cache for the whole pass, so later cells can reuse it.
    // Create a fresh cache for each pass.

    DECLARE checked[] as Checklist = Create_checklist(grid.width+1, grid.height+1)

    DECLARE p as INT = 0    //checked is a stack, needs a pointer
    
    DECLARE i, j as INT
    FOR i = 0 to grid.width
        FOR j = 0 to grid.height
            DECLARE new_state as BOOL = Check_rules(grid, checked, i, j, p)
            IF new_state = TRUE THEN Remove_checked(checked, i, j, p)
            grid.cells[i,j] = new_state
        NEXT j
    NEXT i

    RETURN grid
ENDFUNCTION

FUNCTION Check_rules(grid, checked, x, y, p)
    DECLARE n as INT = Count_neighbours(grid, checked, x, y, p)
    DECLARE state as BOOL = grid.cells[x,y]

    IF state = TRUE THEN
        IF (n < 2 OR n > 3) THEN state = FALSE
    ELSE
        IF n = 3 THEN state = TRUE
    ENDIF

    RETURN state
ENDFUNCTION

FUNCTION Count_neighbours(grid, checked, x, y, p)
    DECLARE n as INT = 0

    IF x = 0 THEN Check_y_left_x(grid, checked, x, y, n, p)
    ELSEIF x > 0 AND x < grid.width THEN Check_y_mid_x(grid, checked, x, y, n, p)
    ELSE Check_y_right_x(grid, checked, x, y, n, p)

    RETURN n
ENDFUNCTION

PROCEDURE Check_y_left_x(grid, checked, x, y, n, p)
    DECLARE i, j as INT

    IF y = 0 THEN
        FOR i = x to x + 1
            FOR j = y to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF Is_dead(checked, i, j, p) THEN CONTINUE
                
                //checks if we have a pair (i,j) exists in the checklist
                
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                    p+=1 
                ENDIF
            NEXT j
        NEXT i
    ELSEIF y > 0 AND y < grid.height THEN
        FOR i = x to x + 1
            FOR j = y - 1 to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF Is_dead(checked, i, j, p) THEN CONTINUE
                
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                    p+=1 
                ENDIF
            NEXT j
        NEXT i
    ELSE
        FOR i = x to x + 1
            FOR j = y - 1 to y
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF Is_dead(checked, i, j, p) THEN CONTINUE
                
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                    p+=1 
                ENDIF
            NEXT j
        NEXT i
    ENDIF
ENDPROCEDURE

PROCEDURE Check_y_mid_x(grid, checked, x, y, n, p)
    DECLARE i, j as INT

    IF y = 0 THEN
        FOR i = x - 1 to x + 1
            FOR j = y to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF Is_dead(checked, i, j, p) THEN CONTINUE
                
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                    p+=1
                ENDIF
            NEXT j
        NEXT i
    ELSEIF y > 0 AND y < grid.height THEN
        FOR i = x - 1 to x + 1
            FOR j = y - 1 to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF Is_dead(checked, i, j, p) THEN CONTINUE
                
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                    p+=1
                ENDIF
            NEXT j
        NEXT i
    ELSE
        FOR i = x - 1 to x + 1
            FOR j = y - 1 to y
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF Is_dead(checked, i, j, p) THEN CONTINUE
                
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                    p+=1
                ENDIF
            NEXT j
        NEXT i
    ENDIF
ENDPROCEDURE

PROCEDURE Check_y_right_x(grid, checked, x, y, n, p)
    DECLARE i, j as INT

    IF y = 0 THEN
        FOR i = x - 1 to x
            FOR j = y to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF Is_dead(checked, i, j, p) THEN CONTINUE
                
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                    p+=1
                ENDIF
            NEXT j
        NEXT i
    ELSEIF y > 0 AND y < grid.height THEN
        FOR i = x - 1 to x
            FOR j = y - 1 to y + 1
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF Is_dead(checked, i, j, p) THEN CONTINUE
                
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                    p+=1
                ENDIF
            NEXT j
        NEXT i
    ELSE
        FOR i = x - 1 to x
            FOR j = y - 1 to y
                IF NOT Is_neighbour(i,j,x,y) THEN CONTINUE
                IF Is_dead(checked, i, j, p) THEN CONTINUE
                
                IF grid.cells[i,j] = TRUE THEN
                    n+=1
                ELSE 
                    checked[p].x = i
                    checked[p].y = j
                    p+=1
                ENDIF
            NEXT j
        NEXT i
    ENDIF
ENDPROCEDURE

//last minute thought: does the grid wrap around itself or is it bounded??? If it's bounded i'm gonna have to rework sooooo many ifs
//currently rereading instructions: replace TRUE/FALSE with 1/0
//by default, the grid has an edge; the option -p or --periodic makes the horizontal and vertical edges wrap around each other
//currently adding a checklist for counting neighbours

FUNCTION Is_neighbour(i, j, x, y)
    IF (i = x AND j = y) THEN RETURN FALSE
    ELSE RETURN TRUE
ENDFUNCTION

FUNCTION Is_dead(checked, i, j, p)
    DECLARE k as INT
    FOR k in 0 to p-1
        IF (checked[k].x = i AND checked[k].y = j) THEN RETURN TRUE
    NEXT k
    RETURN FALSE
ENDFUNCTION

PROCEDURE Remove_checked(checked, x, y, p)
    DECLARE k as INT
    FOR k in 0 to p-1
        IF (checked[k].x = x AND checked[k].y = y) THEN
            checked[k].x = checked[p-1].x
            checked[k].y = checked[p-1].y

            checked[p-1].x = NULL
            checked[p-1].y = NULL

            p-=1
            BREAK
            //moves last element in the stack into newly freed slot and clears the top slot => first free slot is always at p
        ENDIF
    NEXT k
ENDPROCEDURE
```