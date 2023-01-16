W, H = 10, 20  # Number of Tile per dimension
TILE = 45  # Dimension of Tile
GAME_RES = W * TILE, H * TILE  # Dimension of the Game-part window
RES = 900, 940
FPS = 60

S_SHAPE_TEMPLATE = [['00000', '00000', '00110', '01100', '00000'],
                    ['00000', '00100', '00110', '00010', '00000']]

Z_SHAPE_TEMPLATE = [['00000', '00000', '01100', '00110', '00000'],
                    ['00000', '00001', '00110', '00100', '00000']]

I_SHAPE_TEMPLATE = [['00000', '00000', '11110', '00000', '00000'],
                    ['00010', '00010', '00010', '00010', '00010']]

O_SHAPE_TEMPLATE = [['00000', '00000', '01100', '01100', '00000']]

J_SHAPE_TEMPLATE = [['00000', '00000', '00111', '00001', '00000'],
                    ['00000', '00100', '00100', '01100', '00000'],
                    ['00000', '00000', '10000', '11100', '00000'],
                    ['00000', '00110', '00100', '00100', '00000']]

L_SHAPE_TEMPLATE = [['00000', '00100', '11100', '00000', '00000'],
                    ['00000', '00100', '00100', '00110', '00000'],
                    ['00000', '00000', '11100', '10000', '00000'],
                    ['00000', '01100', '00100', '00100', '00000']]

T_SHAPE_TEMPLATE = [['00000', '00100', '01110', '00000', '00000'],
                    ['00000', '00100', '00110', '00100', '00000'],
                    ['00000', '00000', '01110', '00100', '00000'],
                    ['00000', '00100', '01100', '00100', '00000']]

PIECES_IA = {
    'S': S_SHAPE_TEMPLATE,
    'Z': Z_SHAPE_TEMPLATE,
    'J': J_SHAPE_TEMPLATE,
    'L': L_SHAPE_TEMPLATE,
    'I': I_SHAPE_TEMPLATE,
    'O': O_SHAPE_TEMPLATE,
    'T': T_SHAPE_TEMPLATE,
}

BLANK = '0'

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5




def add_to_board(board, piece):
    """
    # riempie nella board il tetramino nella locazione definita
    # fill in the board based on piece's location, shape, and rotation
    :param board: Matrix (lists of lists) of strings
    :param piece: Object with'shape', 'rotation', 'x', 'y', 'color' attributes
    :return: None
    """
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES_IA[piece['shape']][piece['rotation']][y][x] != BLANK and x + piece['x'] < 10 and y + piece[
                'y'] < 20:
                board[x + piece['x']][y + piece['y']] = '1'
                # DEBUGGING NOTE: SOMETIMES THIS IF STATEMENT ISN'T
                # SATISFIED, WHICH NORMALLY WOULD RAISE AN ERROR.
                # NOT SURE WHAT CAUSES THE INDICES TO BE THAT HIGH.
                # THIS IS A BAND-AID FIX


def is_complete_line(board, y):
    """
    Check if a line of blocks is compleate or not
    :param board: Matrix (lists of lists) of strings
    :param y: int value (coordinate)
    :return: bool value
    """
    for x in range(W):
        if board[x][y] == BLANK:
            return False
    return True


def remove_complete_lines(board):
    """

    """
    lines_removed = 0
    y = H - 1  # start y at the bottom of the board
    while y >= 0:
        if is_complete_line(board, y):
            # Remove the line and pull boxes down by one line.
            for pull_down_y in range(y, 0, -1):
                for x in range(W):
                    board[x][pull_down_y] = board[x][pull_down_y - 1]
            # Set very top line to blank.
            for x in range(W):
                board[x][0] = BLANK
            lines_removed += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1  # move on to check next row up
    return lines_removed, board


def is_on_board(x, y):
    """

    """
    return 0 <= x < W and y < H


def is_valid_position(board, piece, adj_x=0, adj_y=0):
    """

    """
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            is_above_board = y + piece['y'] + adj_y < 0
            if is_above_board or PIECES_IA[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not is_on_board(x + piece['x'] + adj_x, y + piece['y'] + adj_y):
                return False  # The piece is off the board
            if board[x + piece['x'] + adj_x][y + piece['y'] + adj_y] != BLANK:
                return False  # The piece collides
    return True
