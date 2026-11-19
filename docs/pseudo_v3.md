FUNCTION Update_grid(grid, periodic)
    DECLARE next as Grid = Create_grid(grid.width, grid.height)

    FOR i = 0 to grid.height - 1
        FOR j = 0 to grid.width - 1
            DECLARE n as INT = Count_neighbours(grid, i, j, periodic)
            next.cells[i,j] = Check_rules(grid.cells[i,j], n)
        NEXT j
    NEXT i

    RETURN next
ENDFUNCTION

FUNCTION Count_neighbours(grid, i, j, periodic)
    DECLARE total as INT = 0
    FOR di = -1 to 1
        FOR dj = -1 to 1
            IF (di = 0 AND dj = 0) THEN CONTINUE
            DECLARE vi = i + di
            DECLARE vj = j + dj
            IF periodic THEN
                vi = vi MOD grid.height
                vj = vj MOD grid.width
            ELSEIF (vi < 0 OR vi >= grid.height OR vj < 0 OR vj >= grid.width) THEN
                CONTINUE
            ENDIF
            total = total + grid.cells[vi,vj]
        NEXT dj
    NEXT di
    RETURN total
ENDFUNCTION

FUNCTION Check_rules(state, n)
    IF state = 1 THEN RETURN (n = 2 OR n = 3)
    RETURN (n = 3)
ENDFUNCTION