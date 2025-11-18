import unittest
from gomoku.core.game_board import Row

class TestRow(unittest.TestCase):
    def setUp(self):
        self.row = Row([(2,0),(2,1),(2,2),(2,3)])

    def test_direction(self):
        self.assertEqual(self.row.direction, 'vertical')

    def test_size(self):
        self.assertEqual(len(self.row), 4)
    
    def test_ends(self):
        self.assertEqual(self.row.ends, ((2,0),(2,3)))
    
    def test_moves(self):
        self.assertEqual(self.row.moves, [(2,0),(2,1),(2,2),(2,3)])

    # [0,0,0,0,0],
    # [0,2,0,0,0],
    # [0,0,1,0,0],
    # [0,0,0,3,0]
    # [0,0,0,0,0],
    def test_add(self):
        row = Row([(1,1)])
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
        row = Row([(1,1)])
        self.assertEqual(row.row_relation((1,2)), 'builds')
        row.add((1,2))
        self.assertEqual(row.row_relation((2,3)), 'touches')

    def test_next_space_count(self):
        row = Row([(1,1),(1,2),(1,3)])
        self.assertEqual(row.next_space_count((1,4), 'vertical', lambda x: x[0] < 0 or x[1] < 0), 1)
        self.assertEqual(row.next_space_count((1,4), 'vertical', lambda x: x[0] < 1 or x[1] < 1), 0)