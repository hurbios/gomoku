import unittest
from gomoku.core.player_rows import Row
from gomoku.core.game_board import Board
from unittest.mock import Mock, MagicMock

class TestRow(unittest.TestCase):
    def setUp(self):
        self.board = Mock(spec=Board(5,5))
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
    def test_get_touching_building_move1(self):
        row = Row([(1,1)], self.board)
        row.add((2,2))
        row.add((3,3))

        self.assertEqual(row.get_touching_building_move((4,3), 'diagonal'), None)

    # [2,0,0,0,0],
    # [0,1,0,0,0],
    # [0,0,1,0,0],
    # [0,0,0,1,0]
    # [0,0,0,0,0],
    def test_get_touching_building_move2(self):
        row = Row([(1,1)], self.board)
        row.add((2,2))
        row.add((3,3))

        self.assertEqual(row.get_touching_building_move((0,0), 'diagonal'), (1,1))

    # [0,0,0,0,0],
    # [0,1,0,0,0],
    # [0,0,1,0,0],
    # [0,0,0,1,0]
    # [0,0,0,0,2],
    def test_get_touching_building_move3(self):
        row = Row([(1,1)], self.board)
        row.add((2,2))
        row.add((3,3))

        self.assertEqual(row.get_touching_building_move((4,4), 'diagonal'), (3,3))

    # [3,3,0,0,0],
    # [0,1,0,0,0],
    # [0,0,1,0,0],
    # [0,0,0,2,0]
    # [0,0,0,0,2],
    def test_row_split(self):
        row = Row([(1,1)], self.board)
        row.add((2,2))
        row2 = Row([(4,4)], self.board)
        row2.add((3,3))
        row.join_row((3,3),row2)
        row3 = Row([(1,0)], self.board)
        row3.add((0,0))
        row.join_row((0,0),row3)
        self.assertEqual(row.moves, [(0,0),(1,1),(2,2),(3,3),(4,4)])

        new_row = row.remove((0,0))
        self.assertEqual(row.moves, [(1,1),(2,2),(3,3),(4,4)])
        self.assertEqual(new_row, None)
        new_row = row.remove((3,3))
        self.assertEqual(row.moves, [(1,1),(2,2)])
        self.assertEqual(new_row.moves, [(4,4)])
        new_row = row.remove((2,2))
        self.assertEqual(new_row, None)
        self.assertEqual(row.moves, [(1,1)])

    # [2,0,0,0,0,0,0],
    # [0,1,0,0,0,0,0],
    # [0,0,1,0,0,0,0],
    # [0,0,0,1,0,0,0],
    # [0,0,0,0,1,0,0],
    # [0,0,0,0,0,1,0],
    # [0,0,0,0,0,0,0]
    def test_row_score(self):
        blocked_spaces = []
        board = Mock(spec=Board(7,7))
        board.is_outside_of_game_area = MagicMock(return_value=False)

        def mock_is_free_space(move):
            return False if move in blocked_spaces else True
        board.is_free_space = mock_is_free_space

        row = Row([(1,1)], board)
        blocked_spaces.append((1,1))
        row.add((2,2))
        blocked_spaces.append((2,2))
        self.assertEqual(row.score, 200)
        row.add((3,3))
        blocked_spaces.append((3,3))
        self.assertEqual(row.score, 50000000)
        row.add((4,4))
        blocked_spaces.append((4,4))
        self.assertEqual(row.score, 100000000)
        row.add((5,5))
        blocked_spaces.append((5,5))
        self.assertEqual(row.score, float('inf'))
        self.assertEqual(row.surrounding_moves, {(0,0),(6,6)})
        blocked_spaces.append((0,0))
        self.assertEqual(row.score, float('inf'))
        blocked_spaces.remove((5,5))
        row.remove((5,5))
        self.assertEqual(row.score, 50000000)
        blocked_spaces.remove((4,4))
        row.remove((4,4))
        self.assertEqual(row.score, 1000)
        blocked_spaces.remove((3,3))
        row.remove((3,3))
        self.assertEqual(row.score, 100)
        blocked_spaces.remove((2,2))
        row.remove((2,2))
        self.assertEqual(row.score, 2)
        row.add((2,2))
        blocked_spaces.append((2,2))
        self.assertEqual(row.score, 100)
        blocked_spaces.remove((0,0))
        row.refresh_potential()
        self.assertEqual(row.score, 200)



        
        

