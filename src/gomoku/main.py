from gomoku.ui import game_board_ui
from gomoku.core import game_board
from gomoku.core.minimax import Minimax

# Create board to use in the game
board = game_board.Board(game_board_ui.BLOCKS_PER_SIDE,game_board_ui.BLOCKS_PER_SIDE)
# Init minimax
minimax = Minimax(board)
# Initialize UI
board_ui = game_board_ui.BoardUI(board, minimax)
# Run UI
board_ui.run()
