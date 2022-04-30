
# Total ammount (if split, adds the columns of all parts)
NCOLS_PART = 6

NCOLS = NCOLS_PART*2
NROWS = 5


def keypos2rowcol(keypos, selected_part):
    
    row = keypos // NCOLS_PART
    col = keypos % NCOLS_PART
    
    if selected_part == 'right':
        col += NCOLS_PART
    
    return row, col
