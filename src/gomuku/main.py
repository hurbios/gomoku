from ui.game_board_ui import BoardUI,BLOCKS_IN_SIDE
import core.game_board as game_board

board = game_board.Board(BLOCKS_IN_SIDE,BLOCKS_IN_SIDE)
board_ui = BoardUI(board)
board_ui.run()