import os
import unittest
import pytest
from gomoku.core.game_board import Board
from gomoku.core.minimax import Minimax

class TestMinimax(unittest.TestCase):
    def setUp(self):
        self.board = Board(20,20)
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

    # def test_another_thing(self):
    #     play = [
    #         [0,0,1,0,0,2,2],
    #         [0,0,1,2,0,2,2],
    #         [0,0,1,2,2,0,0],
    #         [0,0,1,2,0,1,0],
    #         [2,2,1,0,0,1,0],
    #         [0,0,0,0,1,1,1],
    #         [0,0,0,0,0,1,0]
    #     ]
    #     for y,row in enumerate(play):
    #         for x,col in enumerate(row):
    #             self.board.add_move((x,y),col)

    def test_get_next_move(self):
        play = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,2,2,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                self.board.add_move((x,y),col,update_inspect_moves=True)

        self.assertIn(self.minimax.get_next_move((3,2)), [(3,3)])
    
    def test_has_time_exceeded_exceed_time(self):
        self.minimax = Minimax(self.board)
        
        self.minimax._Minimax__time_exceeded = True
        
        self.assertEqual(self.minimax.has_time_exceeded(), True)
    
    def test_has_time_exceeded_exceed_iter_depth(self):
        self.minimax = Minimax(self.board)
        
        self.minimax._Minimax__current_max_depth = 5
        
        self.assertEqual(self.minimax.has_time_exceeded(), True)

    def test_get_next_move_should_block_case1(self):
        play = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,2,2,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                self.board.add_move((x,y),col,update_inspect_moves=True)

        ai_next_move = self.minimax.get_next_move((6,4))
        self.assertIn(ai_next_move, [(5,3),(9,7)])
        self.board.add_move(ai_next_move, 2, update_inspect_moves=True)

        player_move = (9,7) if ai_next_move == (5,3) else (5,3)
        self.board.add_move(player_move, 1, update_inspect_moves=True)

        ai_next_move =  self.minimax.get_next_move(player_move)
        self.assertEqual(ai_next_move, (4,2) if player_move == (5,3) else (10,8))
        self.board.add_move(ai_next_move, 2, update_inspect_moves=True)

    @pytest.mark.skipif(os.environ.get('ITER_DEPTH') and int(os.environ.get('ITER_DEPTH')) < 4, reason='Test requires iteration depth 4')
    def test_get_next_move_should_block_case2(self):
        play = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,2,2,2,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                self.board.add_move((x,y),col,update_inspect_moves=True)
        ai_next_move = self.minimax.get_next_move((6,4))
        self.assertEqual(ai_next_move, (8,6))
        self.board.add_move(ai_next_move, 2, update_inspect_moves=True)

    @pytest.mark.skipif(os.environ.get('ITER_DEPTH') and int(os.environ.get('ITER_DEPTH')) < 4, reason='Test requires iteration depth 4')
    def test_get_next_move_should_block_case3(self):
        play = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,2,2,2,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                self.board.add_move((x,y),col,update_inspect_moves=True)
        ai_next_move = self.minimax.get_next_move((9,7))
        self.assertEqual(ai_next_move, (10,8))
        self.board.add_move(ai_next_move, 2, update_inspect_moves=True)

    @pytest.mark.skipif(os.environ.get('ITER_DEPTH') and int(os.environ.get('ITER_DEPTH')) < 4, reason='Test requires iteration depth 4')
    def test_get_next_move_should_attack_case1_to_win(self):
        play = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                self.board.add_move((x,y),col,update_inspect_moves=True)
        ai_move = self.minimax.get_next_move((7,5))
        self.assertIn(ai_move, [(6,4),(10,4)])
        (ok,wins) = self.board.add_move(ai_move, 2, update_inspect_moves=True)
        self.assertEqual((ok,wins), (True,False))

        user_move = (10,4) if ai_move == (6,4) else (6,4)
        (ok,wins) = self.board.add_move(user_move, 1, update_inspect_moves=True)
        self.assertEqual((ok,wins), (True,False))

        ai_move = self.minimax.get_next_move(user_move)
        self.assertEqual(ai_move, (5,4) if user_move == (10,4) else (11,4))
        (ok,wins) = self.board.add_move(ai_move, 2, update_inspect_moves=True)
        self.assertEqual((ok,wins), (True,True))

    @pytest.mark.skipif(os.environ.get('ITER_DEPTH') and int(os.environ.get('ITER_DEPTH')) < 4, reason='Test requires iteration depth 4')
    def test_get_next_move_should_attack_case2(self):
        play = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,2,2,0,2,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                self.board.add_move((x,y),col,update_inspect_moves=True)
        ai_next_move = self.minimax.get_next_move((6,4))
        self.assertEqual(ai_next_move, (10,4))
        self.board.add_move(ai_next_move, 2, update_inspect_moves=True)

    @pytest.mark.skipif(os.environ.get('ITER_DEPTH') and int(os.environ.get('ITER_DEPTH')) < 4, reason='Test requires iteration depth 4')
    def test_get_next_move_should_attack_case3(self):
        play = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,2,0,2,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,2,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,1,1,1,2,0,2,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,1,2,2,2,1,2,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,1,2,1,2,0,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,2,1,1,1,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,2,1,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                self.board.add_move((x,y),col,update_inspect_moves=True)
        ai_next_move = self.minimax.get_next_move((12,6))
        self.assertEqual(ai_next_move, (10,4))
        self.board.add_move(ai_next_move, 2, update_inspect_moves=True)

    @pytest.mark.skipif(os.environ.get('ITER_DEPTH') and int(os.environ.get('ITER_DEPTH')) < 4, reason='Test requires iteration depth 4')
    def test_get_next_move_should_attack_case4(self):
        play = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,2,2,2,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,2,0,2,1,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,1,2,2,2,1,2,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        for y,row in enumerate(play):
            for x,col in enumerate(row):
                self.board.add_move((x,y),col,update_inspect_moves=True)
        ai_next_move = self.minimax.get_next_move((6,4))
        self.assertEqual(ai_next_move, (12,10))
        self.board.add_move(ai_next_move, 2, update_inspect_moves=True)
        self.board.add_move((15,7), 1, update_inspect_moves=True)
        ok, win = self.board.add_move(self.minimax.get_next_move((15,7)), 2, update_inspect_moves=True)
        self.assertEqual((ok,win), (True,True))
