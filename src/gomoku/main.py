from gomoku.ui import game_board_ui
from gomoku.core import game_board

board = game_board.Board(game_board_ui.BLOCKS_IN_SIDE,game_board_ui.BLOCKS_IN_SIDE)
board_ui = game_board_ui.BoardUI(board)
board_ui.run()
