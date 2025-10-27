import pygame

####################
####  UI SETUP  ####
####################

# These values can be changed
PLAYER1_COLOR = (255, 255, 255)                 # Color of the player1 pieces (r,g,b)
PLAYER2_COLOR = (0, 0, 0)                       # Color of the player2 pieces
BACKGROUND_COLOR = (168, 127, 127)              # Color of the background
GRID_COLOR = (64, 64, 64)                       # Color of the grid
GRID_SIZE = 2                                   # Weight of the lines in px
BLOCK_SIZE = 40                                 # Height and width of the block (including grid) in px
BLOCKS_IN_SIDE = 20                             # Amount of blocks per side so the game area is: BLOCKS_IN_SIDE x BLOCKS_IN_SIDE

# These values are derived from above values
BLOCK_OFFSET = BLOCK_SIZE // 2                  # Offset for center of the block
PIECE_SIZE = BLOCK_SIZE // 2 - GRID_SIZE * 2    # Player piece size in pixels.

AREA_WIDTH = BLOCK_SIZE*BLOCKS_IN_SIDE          # Width of the game area
AREA_HEIGHT = BLOCK_SIZE*BLOCKS_IN_SIDE         # Height of the game area



pygame.init()
naytto = pygame.display.set_mode((AREA_WIDTH, AREA_HEIGHT))

player1 = True
player1_pieces = []
player2_pieces = []


def draw_game_area():
    naytto.fill(BACKGROUND_COLOR)

    for i in range(1,BLOCKS_IN_SIDE):
        pygame.draw.line(naytto, GRID_COLOR, (i*BLOCK_SIZE, 0), (i*BLOCK_SIZE, AREA_HEIGHT), GRID_SIZE)
        pygame.draw.line(naytto, GRID_COLOR, (0, i*BLOCK_SIZE), (AREA_WIDTH, i*BLOCK_SIZE), GRID_SIZE)


def draw_player_pieces(pieces, color):
    for piece in pieces:
        pygame.draw.circle(naytto, color, (BLOCK_OFFSET + piece[0]*BLOCK_SIZE, BLOCK_OFFSET+piece[1]*BLOCK_SIZE), PIECE_SIZE)


while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_piece = (event.pos[0]//BLOCK_SIZE, event.pos[1]//BLOCK_SIZE)
            if new_piece not in player1_pieces and new_piece not in player2_pieces:
                player_pieces = player1_pieces if player1 else player2_pieces
                player_pieces.append(new_piece)
                player1 = not player1
        if event.type == pygame.QUIT:
            exit()
    
    draw_game_area()
    draw_player_pieces(player1_pieces, PLAYER1_COLOR)
    draw_player_pieces(player2_pieces, PLAYER2_COLOR)
    pygame.display.flip()
    