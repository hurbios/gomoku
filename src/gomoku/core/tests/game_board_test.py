import unittest
from unittest.mock import Mock, MagicMock
from gomoku.core.game_board import Board
from gomoku.ui import game_board_ui


class TestGameBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(20,20)

    def test_board_initialization(self):
        self.assertEqual(self.board.size(), (20,20))
        self.assertEqual(self.board.get_player_pieces(1), set())
        self.assertEqual(self.board.get_player_pieces(2), set())
        self.assertEqual(self.board.height, 20)
        self.assertEqual(self.board.width, 20)
        self.assertEqual(self.board.moves, [[0 for _ in range(self.board.width)] for _ in range(self.board.height)])

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
            [1,1,1,1,0],
            [0,0,1,2,0],
            [0,2,2,0,0]
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                ok, has_won = self.board.add_move((x,y),col)
                if(x,y) in [(0,2),(1,2),(2,2),(3,2),(2,3)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                elif(x,y) in [(1,0),(3,0),(3,1),(3,3),(1,4),(2,4)]:
                    self.assertEqual((ok, has_won), (True,False), f"coordinates ({x},{y})")
                else:
                    self.assertEqual((ok, has_won), (False,False), f"coordinates ({x},{y})")
        self.assertEqual(self.board.add_move((4,2),1), (True,True), f"coordinates ({4},{2})")

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

    def test_add_move_incorrect_player(self):
        ok, has_won = self.board.add_move((1,1),3)
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

        self.assertEqual(self.board.get_player_pieces(1), {(2,0),(2,1),(2,2),(2,3),(2,4)})
        self.assertEqual(self.board.get_player_pieces(2), {(3,0),(3,1),(3,2),(3,3),(1,4)})

    def test_reset(self):
        ok, has_won = self.board.add_move((1,1),1)
        self.assertEqual((ok, has_won), (True,False))

        ok, has_won = self.board.add_move((1,1),1)
        self.assertEqual((ok, has_won), (False,False))
        self.assertEqual(self.board.get_player_pieces(1), {(1,1)})

        self.board.reset()

        self.assertEqual(self.board.get_player_pieces(1), set())
        ok, has_won = self.board.add_move((1,1),1)
        self.assertEqual((ok, has_won), (True,False))

    def test_add_move_row_amounts(self):
        self.board = Board(6,6)

        play = [
            [0,0,1,2,0,0],
            [0,0,1,2,0,0],
            [0,0,1,2,0,0],
            [0,0,1,2,2,2],
            [0,2,2,1,0,0],
            [0,2,0,0,0,0]
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                self.board.add_move((y,i),col)

        self.assertEqual(len(self.board.player1_rows), 2)
        self.assertEqual(len(self.board.player2_rows), 6)
    
    def test_add_building_move_to_rows_touching_case(self):
        self.board = Board(6,6)
        
        play = [
            [0,0,1,2,0,0],
            [0,0,1,2,0,0],
            [0,1,1,2,0,0],
            [0,1,0,2,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0]
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                self.board.add_move((y,i),col)
        self.board._Board__get_players_surrounding_rows_in_directions = MagicMock(return_value={
            'vertical':[self.board.player2_rows[0]],
            'horizontal':[self.board.player2_rows[0]],
            'inverse_diagonal':[],
            'diagonal':[]
            })
        self.board.add_move((5,3),2)
        self.assertEqual(len(self.board.player1_rows), 5)
        self.assertEqual(len(self.board.player2_rows), 2)

    def test_remove_move(self):
        self.board = Board(6,6)

        play = [
            [0,0,1,2,0,0],
            [0,0,1,2,0,0],
            [0,1,1,2,0,0],
            [0,0,1,2,2,2],
            [0,2,2,1,0,0],
            [0,2,0,0,0,0]
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                self.board.add_move((y,i),col)

        self.assertEqual(len(self.board.player1_rows), 4)
        self.assertEqual(len(self.board.player2_rows), 6)

        self.board.remove_move((1,2),1)
        self.assertEqual(len(self.board.player1_rows), 2)
        self.assertEqual(len(self.board.player2_rows), 6)

        self.board.remove_move((4,3),2)
        self.assertEqual(len(self.board.player1_rows), 2)
        self.assertEqual(len(self.board.player2_rows), 5)

        self.board.remove_move((5,3),2)
        self.assertEqual(len(self.board.player1_rows), 2)
        self.assertEqual(len(self.board.player2_rows), 4)

    def test_remove_move2(self):
        self.board = Board(6,6)

        play = [
            [0,0,0,0,0,0],
            [0,0,2,0,0,0],
            [0,0,2,1,0,0],
            [0,0,0,1,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0]
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                self.board.add_move((y,i),col)

        self.assertEqual(len(self.board.player1_rows), 1)
        self.assertEqual(len(self.board.player2_rows), 1)

        self.board.remove_move((2,2),2)
        self.assertEqual(len(self.board.player1_rows), 1)
        self.assertEqual(len(self.board.player2_rows), 1)
    
    def test_remove_move3(self):
        self.board = Board(6,6)

        play = [
            [0,0,0,0,0,0],
            [0,0,2,0,0,0],
            [0,0,2,1,0,0],
            [0,2,2,1,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0]
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                self.board.add_move((y,i),col)

        self.assertEqual(len(self.board.player1_rows), 1)
        self.assertEqual(len(self.board.player2_rows), 3)

        self.board.remove_move((2,2),2)
        self.assertEqual(len(self.board.player1_rows), 1)
        self.assertEqual(len(self.board.player2_rows), 2)
    
    def test_get_surrounding_moves_of_moves_rows(self):
        self.board = Board(6,6)

        play = [
            [0,0,0,0,0,0],
            [0,0,2,0,0,0],
            [0,0,2,1,0,0],
            [0,2,2,1,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0]
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                self.board.add_move((y,i),col, True)

        self.assertEqual(self.board.get_surrounding_moves_of_moves_rows((2,3),2), {(0, 3),(2, 4),(2, 0)})

    def test_add_move_real1(self):
        board = Board(7,7)

        play = [
            [0,1,0,2,0,0,0],
            [1,2,2,2,1,0,0],
            [0,2,2,2,1,0,0],
            [0,1,2,1,2,0,0],
            [0,2,1,1,0,1,0],
            [1,0,2,2,0,0,0],
            [2,0,0,1,0,0,0],
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                board.add_move((y,i),col)

        self.assertEqual(len(board.player1_rows), 9)
        self.assertEqual(len(board.player2_rows), 14)

        board.add_move((4,5),1)
        self.assertEqual(len(board.player1_rows), 9)
        self.assertEqual(len(board.player2_rows), 14)

    def test_add_move_real2(self):
        board = Board(7,7)

        play = [
            [2,0,0,0,0,0,0],
            [1,0,0,0,0,0,0],
            [2,0,0,0,0,0,0],
            [0,1,0,0,0,0,0],
            [2,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                board.add_move((y,i),col)

        self.assertEqual(board.get_player_pieces(1), {(0,1),(1,3)})
        self.assertEqual(board.get_player_pieces(2), {(0,0),(0,2),(0,4)})

        board.add_move((0,3),2)
        self.assertEqual(board.get_player_pieces(1), {(0,1),(1,3)})
        self.assertEqual(board.get_player_pieces(2), {(0,0),(0,2),(0,3),(0,4)})

        board.remove_move((0,3),2)
        self.assertEqual(board.get_player_pieces(1), {(0,1),(1,3)})
        self.assertEqual(board.get_player_pieces(2), {(0,0),(0,2),(0,4)})

    def test_row_score(self):
        board = Board(7,7)

        play = [
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,1,1,1,0,0],
            [0,0,2,0,0,0,0],
            [0,0,0,2,0,0,0],
            [0,0,0,0,0,0,0],
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                board.add_move((y,i),col)

        self.assertEqual(board.player1_rows[0].score, 50000000)
        self.assertEqual(board.player2_rows[0].score, 200)
        self.assertEqual(board.evaluate_state(), -49999800)

        board.add_move((1,3),2)

        self.assertEqual(board.player1_rows[0].score, 1000)
        self.assertEqual(board.player2_rows[0].score, 50000000)
        self.assertEqual(board.evaluate_state(), 49999000)

        board.add_move((5,3),2)

        self.assertEqual(board.player1_rows[0].score, 0)
        self.assertEqual(board.player2_rows[0].score, 50000000)
        self.assertEqual(board.evaluate_state(), 50000000)

        board.remove_move((5,3),2)
        self.assertEqual(board.player1_rows[0].score, 1000)
        self.assertEqual(board.player2_rows[0].score, 50000000)
        self.assertEqual(board.evaluate_state(), 49999000)

        board.remove_move((1,3),2)
        self.assertEqual(board.player1_rows[0].score, 50000000)
        self.assertEqual(board.player2_rows[0].score, 200)
        self.assertEqual(board.evaluate_state(), -49999800)

    def test_add_move_inspect_area_refresh(self):
        board = Board(7,7)

        play = [
            [2,0,0,0,0,0,0],
            [1,0,0,0,0,0,0],
            [2,0,0,0,0,0,0],
            [0,1,0,0,0,0,0],
            [2,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0],
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                board.add_move((y,i),col, True)

        self.assertEqual(board.get_player_pieces(1), {(0,1),(1,3)})
        self.assertEqual(board.get_player_pieces(2), {(0,0),(0,2),(0,4)})

        board.add_move((0,3),2, True)
        self.assertEqual(board.get_player_pieces(1), {(0,1),(1,3)})
        self.assertEqual(board.get_player_pieces(2), {(0,0),(0,2),(0,3),(0,4)})
        self.assertEqual(board.inspect_moves, {(1, 2),(2, 1),(1, 5),(1, 4),(2, 3),(0, 5),(2, 5),(2, 4),(3, 1),(1, 1),(2, 0),(0, 6),(3, 3),(2, 6),(2, 2),(1, 0),(1, 6),(3, 5)})

    def test_is_move_part_of_winning_row(self):
        self.board = Board(6,6)

        play = [
            [0,0,0,0,0,1],
            [0,0,2,0,0,1],
            [0,0,2,1,0,0],
            [0,2,2,1,1,1],
            [0,0,0,0,0,0],
            [0,2,0,2,0,0]
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                self.board.add_move((y,i),col, True)

        self.assertEqual(self.board.is_move_part_of_winning_row((2,4),2), False)
        self.assertEqual(self.board.is_move_part_of_winning_row((2,5),2), False)
        
        self.board.add_move((2,4),2, True)
        self.assertEqual(self.board.is_move_part_of_winning_row((2,4),2), False)
        self.assertEqual(self.board.is_move_part_of_winning_row((2,5),2), False)
        
        self.board.add_move((2,5),2, True)
        self.assertEqual(self.board.is_move_part_of_winning_row((2,4),2), True)
        self.assertEqual(self.board.is_move_part_of_winning_row((2,5),2), True)

    def test_get_moves_with_high_score_rows(self):
        self.board = Board(6,6)

        play = [
            [1,0,0,0,0,0],
            [2,0,2,1,0,1],
            [2,0,2,1,0,1],
            [2,2,2,1,0,1],
            [2,0,0,1,0,0],
            [0,0,0,2,0,0]
        ]
        for i,row in enumerate(play):
            for y,col in enumerate(row):
                self.board.add_move((y,i),col, True)

        self.assertEqual(self.board.get_moves_with_high_score_rows(), [(0, 5), (2, 4), (2, 0), (3, 0), (5, 4), (5, 0)])
