import sys
import time
import pygame
from gomoku.core.minimax import Minimax
from gomoku.core.game_board import Board

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
# Amount of blocks per side so the game area is: BLOCKS_PER_SIDE x BLOCKS_PER_SIDE
BLOCKS_PER_SIDE = 20


# These values are derived from above values and should not be changed

BLOCK_OFFSET = BLOCK_SIZE // 2                  # Offset for center of the block
PIECE_SIZE = BLOCK_SIZE // 2 - GRID_SIZE * 2    # Player piece size in pixels.

AREA_WIDTH = BLOCK_SIZE*BLOCKS_PER_SIDE          # Width of the game area
AREA_HEIGHT = BLOCK_SIZE*BLOCKS_PER_SIDE         # Height of the game area


class BoardUI:
    def __init__(self, board:Board, minimax:Minimax):
        pygame.init()
        self.display = pygame.display.set_mode((AREA_WIDTH, AREA_HEIGHT))

        self.player = 1
        self.player1_pieces = []
        self.player2_pieces = []

        self.board = board
        self.minimax = minimax

    # Draws background and grid
    def draw_game_area(self):
        self.display.fill(BACKGROUND_COLOR)

        for i in range(1,BLOCKS_PER_SIDE):
            pygame.draw.line(
                self.display,
                GRID_COLOR,
                (i*BLOCK_SIZE, 0),
                (i*BLOCK_SIZE, AREA_HEIGHT),
                GRID_SIZE
            )
            pygame.draw.line(
                self.display,
                GRID_COLOR,
                (0, i*BLOCK_SIZE),
                (AREA_WIDTH,
                i*BLOCK_SIZE),
                GRID_SIZE
            )

    # Draws one players pieces
    def draw_player_pieces(self,pieces, color):
        for piece in pieces:
            pygame.draw.circle(
                self.display,
                color,
                (BLOCK_OFFSET + piece[0]*BLOCK_SIZE, BLOCK_OFFSET+piece[1]*BLOCK_SIZE),
                PIECE_SIZE
            )

    # Draws the game area, player pieces draws additional if some additional drawing is definer
    def draw_game(self,additional_draw=None):
        self.draw_game_area()
        if additional_draw:
            additional_draw(self)
        self.draw_player_pieces(self.board.get_player_pieces(1), PLAYER1_COLOR)
        self.draw_player_pieces(self.board.get_player_pieces(2), PLAYER2_COLOR)
        pygame.display.flip()

    # Normal game draw but add just a text about the winning player
    def draw_game_win(self):
        def draw_winning_text(self):
            font = pygame.font.SysFont("Arial", 42)
            text = font.render(f"Player{self.player} wins!", True, (255, 0, 0))
            self.display.blit(text, (100, 50))
        self.draw_game(draw_winning_text)

    def actions_after_player_move(self, can_move, wins):
        if wins:
            self.draw_game_win()
            time.sleep(2)
            self.board.reset()
        if can_move and not wins:
            self.player = 2 if self.player == 1 else 1

    # Main UI loop
    def run(self):
        prev_piece = (0,0)
        while True:
            if self.player == 2:
                time.sleep(0.5)
                new_piece = self.minimax.get_next_move(prev_piece)
                can_move, wins = self.board.add_move(new_piece, self.player) if new_piece else (None, None)
                self.actions_after_player_move(can_move, wins)
            else:
                # Check user inputs
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        new_piece = (event.pos[0]//BLOCK_SIZE, event.pos[1]//BLOCK_SIZE)
                        prev_piece = new_piece
                        can_move, wins = self.board.add_move(new_piece, self.player)
                        self.actions_after_player_move(can_move, wins)
                    if event.type == pygame.QUIT:
                        sys.exit()
            # Refresh the game UI
            self.draw_game()
