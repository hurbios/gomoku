import unittest
from gomoku.core.player_rows import Row
from gomoku.core.game_board import Board

class TestRow(unittest.TestCase):
    def setUp(self):
        self.board = Board(5,5) # TODO: mock board
        self.row = Row([(2,0),(2,1),(2,2),(2,3)], self.board)

    def test_direction(self):
        self.assertEqual(self.row.direction, 'vertical')

    def test_size(self):
        self.assertEqual(len(self.row), 4)

    def test_ends(self):
        self.assertEqual(self.row.ends, ((2,0),(2,3)))

    def test_moves(self):
        self.assertEqual(self.row.moves, [(2,0),(2,1),(2,2),(2,3)])

    def test_str(self):
        self.assertEqual(str(self.row), "[(2, 0), (2, 1), (2, 2), (2, 3)]")

    # [0,0,0,0,0],
    # [0,2,0,0,0],
    # [0,0,1,0,0],
    # [0,0,0,3,0]
    # [0,0,0,0,0],
    def test_add(self):
        row = Row([(1,1)], self.board)
        self.assertEqual(row.direction, None)
        self.assertEqual(row.ends, None)
        row.add((0,0))
        self.assertEqual(row.direction, 'diagonal')
        self.assertEqual(row.ends, ((0,0),(1,1)))
        row.add((2,2))
        self.assertEqual(row.direction, 'diagonal')
        self.assertEqual(row.ends, ((0,0),(2,2)))

    # [0,0,1,0,0],
    # [0,0,1,0,0],
    # [0,t,1,0,0],
    # [0,0,1(c),0,0],
    # [n,t,b,0,0]
    def test_row_relation(self):
        self.assertEqual(self.row.row_relation((1,2)), 'touches') # t
        self.assertEqual(self.row.row_relation((1,2)), 'touches') # t
        self.assertEqual(self.row.row_relation((2,3)), 'contains') # c
        self.assertEqual(self.row.row_relation((2,4)), 'builds') # b
        self.assertEqual(self.row.row_relation((0,4)), None) # n
        row = Row([(1,1)], self.board)
        self.assertEqual(row.row_relation((1,2)), 'builds')
        row.add((1,2))
        self.assertEqual(row.row_relation((2,3)), 'touches')

    def test_next_space_count(self):
        row = Row([(1,1),(1,2),(1,3)], self.board)
        self.assertEqual(row.next_space_count((1,4), 'vertical', lambda x: x[0] < 0 or x[1] < 0), 1)
        self.assertEqual(row.next_space_count((1,4), 'vertical', lambda x: x[0] < 1 or x[1] < 1), 0)
        self.assertEqual(row.score, 50000000)


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
        self.assertEqual(board.evaluate_state(1,(0,0),0), -49999800)

        board.add_move((1,3),2)

        self.assertEqual(board.player1_rows[0].score, 1000)
        self.assertEqual(board.player2_rows[0].score, 50000000)
        self.assertEqual(board.evaluate_state(1,(0,0),0), 49999000)

        board.add_move((5,3),2)

        self.assertEqual(board.player1_rows[0].score, 0)
        self.assertEqual(board.player2_rows[0].score, 50000000)
        self.assertEqual(board.evaluate_state(1,(0,0),0), 50000000)

        board.remove_move((5,3),2)
        self.assertEqual(board.player1_rows[0].score, 1000)
        self.assertEqual(board.player2_rows[0].score, 50000000)
        self.assertEqual(board.evaluate_state(1,(0,0),0), 49999000)

        board.remove_move((1,3),2)
        self.assertEqual(board.player1_rows[0].score, 50000000)
        self.assertEqual(board.player2_rows[0].score, 200)
        self.assertEqual(board.evaluate_state(1,(0,0),0), -49999800)

    # [1,0,0,0,0],
    # [0,1,0,0,0],
    # [0,0,1,0,0],
    # [0,0,0,0,0]
    # [0,0,0,0,0],
    def test_row_direction(self):
        row = Row([(1,1)], self.board)
        row.add((0,0))
        row.add((2,2))
        self.assertEqual(row.get_direction((1,0)), 'horizontal')

    # [3,3,0,0,0],
    # [0,1,0,0,0],
    # [0,0,1,0,0],
    # [0,0,0,2,0]
    # [0,0,0,0,2],
    def test_row_join(self):
        row = Row([(1,1)], self.board)
        row.add((2,2))
        row2 = Row([(4,4)], self.board)
        row2.add((3,3))
        row.join_row((3,3),row2)
        row3 = Row([(1,0)], self.board)
        row3.add((0,0))
        row.join_row((0,0),row3)
        self.assertEqual(row.moves, [(0,0),(1,1),(2,2),(3,3),(4,4)])

    # [0,0,0,0,0],
    # [0,1,0,0,0],
    # [0,0,1,0,0],
    # [0,0,0,1,2]
    # [0,0,0,0,0],
    def test_row_join2(self):
        row = Row([(1,1)], self.board)
        row.add((2,2))
        row.add((3,3))

        self.assertEqual(row.get_touching_building_move((4,3), 'diagonal'), None)
