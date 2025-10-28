import sys
import pygame
import time
import game_board

####################
####  UI SETUP  ####
####################
# These values can be changed

# Color of the player pieces (r,g,b)
PLAYER1_COLOR = (0, 0, 0)
PLAYER2_COLOR = (255, 255, 255)
# Color of the game area (r,g,b)
BACKGROUND_COLOR = (168, 127, 127)
GRID_COLOR = (64, 64, 64)
# Weight of the lines in px
GRID_SIZE = 2
# Height and width of the block (including grid) in px
BLOCK_SIZE = 40
# Amount of blocks per side so the game area is: BLOCKS_IN_SIDE x BLOCKS_IN_SIDE
BLOCKS_IN_SIDE = 20


# These values are derived from above values and should not be changed

BLOCK_OFFSET = BLOCK_SIZE // 2                  # Offset for center of the block
PIECE_SIZE = BLOCK_SIZE // 2 - GRID_SIZE * 2    # Player piece size in pixels.

AREA_WIDTH = BLOCK_SIZE*BLOCKS_IN_SIDE          # Width of the game area
AREA_HEIGHT = BLOCK_SIZE*BLOCKS_IN_SIDE         # Height of the game area


########################
####  Main Program  ####
########################

# Init pygame

pygame.init()
display = pygame.display.set_mode((AREA_WIDTH, AREA_HEIGHT))

player = 1
player1_pieces = []
player2_pieces = []

board = game_board.Board(BLOCKS_IN_SIDE,BLOCKS_IN_SIDE)


# Pygame helper functions

def draw_game_area():
    display.fill(BACKGROUND_COLOR)

    for i in range(1,BLOCKS_IN_SIDE):
        pygame.draw.line(
            display,
            GRID_COLOR,
            (i*BLOCK_SIZE, 0),
            (i*BLOCK_SIZE, AREA_HEIGHT),
            GRID_SIZE
        )
        pygame.draw.line(
            display,
            GRID_COLOR,
            (0, i*BLOCK_SIZE),
            (AREA_WIDTH,
             i*BLOCK_SIZE),
             GRID_SIZE
        )

def draw_player_pieces(pieces, color):
    for piece in pieces:
        pygame.draw.circle(
            display,
            color,
            (BLOCK_OFFSET + piece[0]*BLOCK_SIZE, BLOCK_OFFSET+piece[1]*BLOCK_SIZE),
            PIECE_SIZE
        )

def draw_game_win(player):
    draw_game_area()
    font = pygame.font.SysFont("Arial", 42)
    text = font.render(f"Player{player} wins!", True, (255, 0, 0))
    display.blit(text, (100, 50))
    draw_player_pieces(board.get_player_pieces(1), PLAYER1_COLOR)
    draw_player_pieces(board.get_player_pieces(2), PLAYER2_COLOR)
    pygame.display.flip()

def draw_game():
    draw_game_area()
    draw_player_pieces(board.get_player_pieces(1), PLAYER1_COLOR)
    draw_player_pieces(board.get_player_pieces(2), PLAYER2_COLOR)
    pygame.display.flip()

# Main UI loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_piece = (event.pos[0]//BLOCK_SIZE, event.pos[1]//BLOCK_SIZE)
            can_move, wins = board.add_move(new_piece, player)
            if wins:
                draw_game_win(player)
                time.sleep(5)
                board.reset()
            if can_move:
                player = 2 if player == 1 else 1
        if event.type == pygame.QUIT:
            sys.exit()
    draw_game()
