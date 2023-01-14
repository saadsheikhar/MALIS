W, H = 10, 20  # Number of Tile per dimension
TILE = 45  # Dimension of Tile
GAME_RES = W * TILE, H * TILE  # Dimension of the Game-part window
RES = 900, 940
FPS = 60

S_SHAPE_TEMPLATE = [['00000', '00000', '00110', '01100', '00000'],
                    ['00000', '00100', '00110', '00010', '00000']]

Z_SHAPE_TEMPLATE = [['00000', '00000', '01100', '00110', '00000'],
                    ['00000', '00100', '01100', '01000', '00000']]

I_SHAPE_TEMPLATE = [['00100', '00100', '00100', '00100', '00000'],
                    ['00000', '00000', '11110', '00000', '00000']]

O_SHAPE_TEMPLATE = [['00000', '00000', '01100', '01100', '00000']]

J_SHAPE_TEMPLATE = [['00000', '01000', '01110', '00000', '00000'],
                    ['00000', '00110', '00100', '00100', '00000'],
                    ['00000', '00000', '01110', '00010', '00000'],
                    ['00000', '00100', '00100', '01100', '00000']]

L_SHAPE_TEMPLATE = [['00000', '00010', '01110', '00000', '00000'],
                    ['00000', '00100', '00100', '00110', '00000'],
                    ['00000', '00000', '01110', '01000', '00000'],
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

def get_blank_board():
    """
    # create and return a new blank board data structure
    generate a blank matrix as lists of lists
    """
    board = []
    for i in range(W):
        board.append(['0'] * H)
    return board
