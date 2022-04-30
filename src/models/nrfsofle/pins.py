import board


def get_keyboard_pins(microcontroller_name, selected_part):
    """
    Return two lists. 
     * The first one is a list of row pin numbers
     * The second one is a list of column pin numbers
    """
    
    assert selected_part in ['left', 'right']
    
    # Dependent of the board and the microcontroller
    if microcontroller_name == 'nice_nano':
        rows = [board.P0_24, board.P1_00, board.P0_11, board.P1_04, board.P1_06]
        cols = [board.P0_02, board.P1_15, board.P1_13, board.P1_11, board.P0_10, board.P0_09]
    else:
        raise ValueError('Unsupported microcontroller for nRFsofle ({})'.format(microcontroller_name))
    
    # Mirror it for right part
    if selected_part == 'right':
        cols = cols[::-1]
    
    return rows, cols


def is_row2col(selected_part):
    return False
