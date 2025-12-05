from gomoku.core.directions import DIRECTIONS

class Row:
    def __init__(self, moves, board):
        self.__moves = moves
        self._direction = None
        self._ends = None
        self.__potential = 0
        self.__board = board
        self.__surrounding_spaces = set()

        if len(self.__moves) > 1:
            self._direction = self.get_direction(moves[0], moves[1])
            self.__refresh_row()

    @property
    def direction(self):
        return self._direction

    @property
    def moves(self):
        return self.__moves

    @property
    def ends(self):
        return self._ends

    @property
    def score(self):
        return self.__potential

    @property
    def surrounding_moves(self):
        return self.__surrounding_spaces

    def __len__(self):
        return len(self.__moves)

    def __str__(self):
        return str(self.__moves)

    def __refresh_row_ends(self):
        """check what are the rows opposite ends"""
        if len(self) > 1:
            self._ends = (self.__moves[0], self.__moves[len(self)-1])
        else:
            self._ends = None

    def __refresh_row_potential(self):
        """
        calculate and save the potential of this row
        This is simplified potential calculation for testing. Could improve.
        """
        free_spaces = 0
        for space in self.next_spaces():
            if not self.__board.is_outside_of_game_area(space):
                self.__surrounding_spaces.add(space)
                if self.__board.is_free_space(space):
                    free_spaces += 1
        if len(self) <= 1:
            score = min(2, free_spaces)
        else:
            score = 10**len(self) * free_spaces
            if len(self) >= 5:
                score = float('inf')
            if len(self) == 4:
                if free_spaces >= 2:
                    score = 100000000
                elif free_spaces >= 1:
                    score = 50000000
            if len(self) == 3 and free_spaces >= 2:
                score = 50000000
        self.__potential = score

    def __refresh_row(self):
        """refresh row potential and row ends"""
        if len(self.__moves) > 1:
            self.__moves.sort()
        self.__refresh_row_ends()
        if len(self) <= 1:
            self._direction = None
        self.__refresh_row_potential()

    def refresh_potential(self):
        self.__refresh_row_potential()

    def get_direction(self, move, comparison_move=None):
        """checks the direction of the move compared to provided comparison move"""
        if not comparison_move:
            comparison_move = self.moves[0]
        move_offset = (move[0] - comparison_move[0], move[1] - comparison_move[1])
        for direction, offsets in DIRECTIONS.items():
            if move_offset in (offsets['low'], offsets['high']):
                return direction
        return None

    def __get_close_moves(self, move):
        """get moves that are close to this row and what is their direction in realtion to this move"""
        close_moves = []
        for comparison_move in self.__moves:
            direction = self.get_direction(move, comparison_move)
            if direction:
                close_moves.append((comparison_move, direction))
        return close_moves

    def join_row(self, move, row_to_join):
        """
        creates new row if row is not same direction.
        Append only one in row_to_join if different direction.
        """
        self.add(move)
        if self._direction == row_to_join.direction or not row_to_join.direction:
            for m in row_to_join.moves:
                self.add(m)
        self.__refresh_row()

    def add(self, move):
        """add move to this row"""
        if move not in self.__moves:
            if len(self) <= 1 and not self._direction:
                self._direction = self.get_direction(move, self.__moves[0])
            self.__moves.append(move)
            self.__refresh_row()

    def remove(self, move):
        """remove move from this row"""
        if move not in self._ends:
            split_at = self.__moves.index(move)
            new_row = Row(self.__moves[split_at+1:], self.__board)
            self.__moves = self.__moves[:split_at]
            self.__refresh_row()
            return new_row

        self.__moves.remove(move)
        self.__refresh_row()
        return None


    def contains(self, move):
        return move in self.__moves

    def row_relation(self, move):
        """check what is the relation of the move to this row"""
        if self.contains(move):
            return 'contains'
        closest_moves = self.__get_close_moves(move)
        if len(closest_moves) == 1:
            if not self.direction or closest_moves[0][1] == self.direction:
                return 'builds'
        if len(closest_moves) >= 1:
            return 'touches'
        return None

    def get_touching_building_move(self, move, direction):
        """
        get moves that are touching and would build the row i.e. are next in same direction
        method should only be used if row_relation = touches. No verification for improved performance.
        """
        comparison_move = (move[0] + DIRECTIONS[direction]['low'][0], move[1] + DIRECTIONS[direction]['low'][1])
        if comparison_move in self.__moves:
            return comparison_move
        comparison_move = (move[0] + DIRECTIONS[direction]['high'][0], move[1] + DIRECTIONS[direction]['high'][1])
        if comparison_move in self.__moves:
            return comparison_move
        return None

    def next_spaces(self, direction=None):
        """find the moves that are next moves from this move"""
        if direction:
            comp_move = (self.moves[0],self.moves[0]) if not self._ends else self._ends
            low = (
                comp_move[0][0]+DIRECTIONS[direction]['low'][0],
                comp_move[0][1]+DIRECTIONS[direction]['low'][1]
            )
            high = (
                comp_move[1][0]+DIRECTIONS[direction]['high'][0],
                comp_move[1][1]+DIRECTIONS[direction]['high'][1]
            )
            return [low, high]
        if self._ends:
            low = (
                self._ends[0][0]+DIRECTIONS[self._direction]['low'][0],
                self._ends[0][1]+DIRECTIONS[self._direction]['low'][1]
            )
            high = (
                self._ends[1][0]+DIRECTIONS[self._direction]['high'][0],
                self._ends[1][1]+DIRECTIONS[self._direction]['high'][1]
            )
            return [low, high]

        spaces = []
        for _, offset in DIRECTIONS.items():
            spaces.append((self.moves[0][0]+offset['low'][0], self.moves[0][1]+offset['low'][1]))
            spaces.append((self.moves[0][0]+offset['high'][0], self.moves[0][1]+offset['high'][1]))
        return spaces

    def next_space_count(self, move, direction, is_out_of_game_fn):
        """check how many spaces the row has around it to build with"""
        spaces = self.next_spaces(direction=direction)
        count = 0 if is_out_of_game_fn(spaces[0]) or spaces[0] == move else 1
        count += 0 if is_out_of_game_fn(spaces[1]) or spaces[1] == move else 1
        return count
