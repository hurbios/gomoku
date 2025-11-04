import unittest
# from unittest.mock import Mock, ANY
from gomoku.core.game_board import Board
from gomoku.ui import game_board_ui


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(20,20)

    def test_board_initialization(self):
        self.assertEqual(self.board.size(), (20,20))
        self.assertEqual(self.board.get_player_pieces(1), [])
        self.assertEqual(self.board.get_player_pieces(2), [])

    def test_add_move_horizontal_win(self):
        play = [
            [0,0,1,2,0],
            [0,0,1,2,0],
            [0,0,1,2,0],
            [0,0,1,2,0],
            [0,2,1,0,0]
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                ok, has_won = self.board.add_move((x,y),col)
                if(x,y) == (2,4):
                    self.assertEqual((ok, has_won), (True,True), f"coordinates ({x},{y})")
                elif(x,y) in [(2,0),(2,1),(2,2),(2,3)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                elif(x,y) in [(3,0),(3,1),(3,2),(3,3),(1,4)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                else:
                    self.assertEqual((ok, has_won), (False,False), f"coordinates ({x},{y})")

    def test_add_move_vertical_win(self):
        play = [
            [0,2,0,2,0],
            [0,0,0,2,0],
            [1,1,1,1,1],
            [0,0,1,2,0],
            [0,2,2,0,0]
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                ok, has_won = self.board.add_move((x,y),col)
                if(x,y) == (4,2):
                    self.assertEqual((ok, has_won), (True,True), f"coordinates ({x},{y})")
                elif(x,y) in [(0,2),(1,2),(2,2),(3,2),(2,3)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                elif(x,y) in [(1,0),(3,0),(3,1),(3,3),(1,4),(2,4)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                else:
                    self.assertEqual((ok, has_won), (False,False), f"coordinates ({x},{y})")

    def test_add_move_diagonal_win(self):
        play = [
            [1,2,0,2,0],
            [0,1,0,2,0],
            [0,0,1,0,0],
            [0,0,1,1,0],
            [0,2,2,2,1]
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                ok, has_won = self.board.add_move((x,y),col)
                if(x,y) == (4,4):
                    self.assertEqual((ok, has_won), (True,True), f"coordinates ({x},{y})")
                elif(x,y) in [(0,0),(1,1),(2,2),(3,3),(2,3)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                elif(x,y) in [(1,0),(3,0),(3,1),(1,4),(2,4),(3,4)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                else:
                    self.assertEqual((ok, has_won), (False,False), f"coordinates ({x},{y})")

    def test_add_move_inverse_diagonal_win(self):
        play = [
            [0,2,2,2,1],
            [0,0,0,1,0],
            [0,0,1,0,0],
            [0,1,1,0,0],
            [1,2,2,2,0]
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                ok, has_won = self.board.add_move((x,y),col)
                if(x,y) == (0,4):
                    self.assertEqual((ok, has_won), (True,True), f"coordinates ({x},{y})")
                elif(x,y) in [(4,0),(3,1),(2,2),(1,3),(2,3)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                elif(x,y) in [(1,0),(2,0),(3,0),(1,4),(2,4),(3,4)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                else:
                    self.assertEqual((ok, has_won), (False,False), f"coordinates ({x},{y})")

    def test_add_move_horizontal_win_6_pieces(self):
        play = [
            [0,0,1,2,0,0],
            [0,0,1,2,0,0],
            [0,0,1,2,0,0],
            [0,0,1,2,0,0],
            [0,2,1,0,0,0],
            [0,2,0,0,0,0]
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                ok, has_won = self.board.add_move((x,y),col)
                if(x,y) == (2,4):
                    self.assertEqual((ok, has_won), (True,True), f"coordinates ({x},{y})")
                elif(x,y) in [(2,0),(2,1),(2,2),(2,3)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                elif(x,y) in [(3,0),(3,1),(3,2),(3,3),(1,4),(1,5)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                else:
                    self.assertEqual((ok, has_won), (False,False), f"coordinates ({x},{y})")
        ok, has_won = self.board.add_move((2,5),1)
        self.assertEqual((ok, has_won), (True,True), "coordinates (2,5)")

    def test_get_direction_count_unknown(self):
        self.assertEqual(0, self.board.get_direction_count((2,0),1,'unknown'))

    def test_add_move_existing_piece(self):
        ok, has_won = self.board.add_move((1,1),1)
        self.assertEqual((ok, has_won), (True,False))

        ok, has_won = self.board.add_move((1,1),1)
        self.assertEqual((ok, has_won), (False,False))

        ok, has_won = self.board.add_move((1,1),2)
        self.assertEqual((ok, has_won), (False,False))

    def test_add_add_piece_outside_area(self):
        ok, has_won = self.board.add_move((1,1),1)
        self.assertEqual((ok, has_won), (True,False))

        ok, has_won = self.board.add_move((-1,1),1)
        self.assertEqual((ok, has_won), (False,False))

        ok, has_won = self.board.add_move((1,-1),1)
        self.assertEqual((ok, has_won), (False,False))

        ok, has_won = self.board.add_move((1,game_board_ui.BLOCKS_PER_SIDE+1),1)
        self.assertEqual((ok, has_won), (False,False))

        ok, has_won = self.board.add_move((game_board_ui.BLOCKS_PER_SIDE+1,1),1)
        self.assertEqual((ok, has_won), (False,False))

    def test_get_player_pieces(self):
        play = [
            [0,0,1,2,0],
            [0,0,1,2,0],
            [0,0,1,2,0],
            [0,0,1,2,0],
            [0,2,1,0,0]
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                self.board.add_move((y,i),col)

        self.assertEqual(self.board.get_player_pieces(1), [(2,0),(2,1),(2,2),(2,3),(2,4)])
        self.assertEqual(self.board.get_player_pieces(2), [(3,0),(3,1),(3,2),(3,3),(1,4)])

    def test_reset(self):
        ok, has_won = self.board.add_move((1,1),1)
        self.assertEqual((ok, has_won), (True,False))

        ok, has_won = self.board.add_move((1,1),1)
        self.assertEqual((ok, has_won), (False,False))
        self.assertEqual(self.board.get_player_pieces(1), [(1,1)])

        self.board.reset()

        self.assertEqual(self.board.get_player_pieces(1), [])
        ok, has_won = self.board.add_move((1,1),1)
        self.assertEqual((ok, has_won), (True,False))

    def test_next_free_coordinates(self):
        self.board = Board(5,5)
        play = [
            [0,0,1,2,0],
            [0,0,1,2,0],
            [0,0,1,2,0],
            [0,0,1,2,0],
            [0,2,1,0,0]
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                self.board.add_move((y,i),col)

        self.assertEqual(self.board.get_next_free_coordinates((2,0),1,'vertical'), (None,(1,0)))
        self.assertEqual(self.board.get_next_free_coordinates((2,0),1,'horizontal'), (None,None))
        self.assertEqual(self.board.get_next_free_coordinates((2,0),1,'diagonal'), (None,None))
        self.assertEqual(self.board.get_next_free_coordinates((2,0),1,'inverse_diagonal'), (None,(1,1)))
        self.assertEqual(self.board.get_next_free_coordinates((2,0),1,'asdf'), (None,None))
