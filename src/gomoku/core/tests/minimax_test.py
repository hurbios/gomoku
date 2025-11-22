import unittest
from gomoku.core.game_board import Board
from gomoku.core.minimax import Minimax
class TestMinimax(unittest.TestCase):
    def setUp(self):
        self.board = Board(7,7)
        self.minimax = Minimax(self.board)

    def test_something_in_minimax(self):
        # 7x7 board:
        # [0,0,0,0,0,0,0],
        # [0,0,0,0,0,0,0],
        # [0,0,1,0,0,0,0],
        # [0,0,0,0,0,0,0],
        # [0,0,0,0,0,0,0],
        # [0,0,0,0,0,0,0],
        # [0,0,0,0,0,0,0]
        pass

    def test_another_thing(self):
        play = [
            [0,0,1,0,0,2,2],
            [0,0,1,2,0,2,2],
            [0,0,1,2,2,0,0],
            [0,0,1,2,0,1,0],
            [2,2,1,0,0,1,0],
            [0,0,0,0,1,1,1],
            [0,0,0,0,0,1,0]
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                self.board.add_move((x,y),col)
