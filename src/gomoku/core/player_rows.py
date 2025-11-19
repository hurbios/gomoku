from gomoku.core.directions import DIRECTIONS

class Row:
    def __init__(self, moves):
        self._moves = moves #TODO: performancew improve to set
        self._direction = None
        self._ends = None

        if len(self._moves) > 1:
            self._direction = self.get_direction(moves[0], moves[1])
            self.__refresh_row()
    
    @property
    def direction(self):
        return self._direction
    
    @property
    def moves(self):
        return self._moves
    
    @property
    def ends(self):
        return self._ends

    def __len__(self):
        return len(self._moves)
    
    def __str__(self):
        return str(self._moves)
    
    def __refresh_row_ends(self):
        if len(self) > 1:
            self._ends = (self._moves[0], self._moves[len(self)-1])
        else:
            self._ends = None
        return

    def __refresh_row(self):
        if len(self._moves) > 1:
            print(self._moves, flush=True)
            self._moves.sort()
        self.__refresh_row_ends()
        if len(self) <= 1:
            self._direction = None
        return

    # checks the direction of the move compared to provided comparison move
    def get_direction(self, move, comparison_move=None):
        if not comparison_move:
            comparison_move = self.moves[0]
        move_offset = (move[0] - comparison_move[0], move[1] - comparison_move[1])
        for dir, offsets in DIRECTIONS.items():
            if offsets['high'] == move_offset or offsets['low'] == move_offset:
                return dir
        return None

    def __get_close_moves(self, move):
        close_moves = []
        for comparison_move in self._moves:
            direction = self.get_direction(move, comparison_move)
            if direction:
                close_moves.append((comparison_move, direction)) 
        return close_moves

    def join_row(self, move, row_to_join):
        #TODO: create new row if row is not same direction. Append only one in row_to_join if different direction.
        self.add(move)
        if self._direction == row_to_join.direction:
            for m in row_to_join.moves:
                self.add(m)
        self.__refresh_row()
        return

    def add(self, move):
        if move not in self._moves:
            if len(self) <= 1 and not self._direction:
                self._direction = self.get_direction(move, self._moves[0])
            self._moves.append(move)
            self.__refresh_row()
        return

    def remove(self, move):
        if move != self._ends[0] and move != self._ends[1]:
            split_at = self._moves.index(move)
            print(f"split row {self._moves} to {self._moves[split_at+1:]} and {self._moves[:split_at]}, ends: {self._ends}, move: {move}")
            new_row = Row(self._moves[split_at+1:])
            self._moves = self._moves[:split_at]
            self.__refresh_row()
            return new_row
        else:
            print(f"remove {move} from row", self._moves)
            self._moves.remove(move)
            self.__refresh_row()
            return None
        
    
    def contains(self, move):
        return move in self._moves
    
    def row_relation(self, move):
        if self.contains(move):
            return 'contains'
        closest_moves = self.__get_close_moves(move)
        if len(closest_moves) == 1:
            if not self.direction or closest_moves[0][1] == self.direction:
                return 'builds'
        if len(closest_moves) >= 1:
            return 'touches'
        return None
    
    # should use only if row_relation = touches. No verification for improved performance.
    def get_touching_building_move(self, move, direction):
        comparison_move = (move[0] + DIRECTIONS[direction]['low'][0], move[1] + DIRECTIONS[direction]['low'][1])
        if comparison_move in self._moves:
            return comparison_move
        comparison_move = (move[0] + DIRECTIONS[direction]['high'][0], move[1] + DIRECTIONS[direction]['high'][1])
        if comparison_move in self._moves:
            return comparison_move
        return None

    #TODO: simplify. No just take comparison move as input
    def next_spaces(self, direction=None):
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
            # print(self._ends, '+', DIRECTIONS[direction], "=",  (low, high))
            return [low, high]
        elif self._ends:
            low = (
                self._ends[0][0]+DIRECTIONS[self._direction]['low'][0],
                self._ends[0][1]+DIRECTIONS[self._direction]['low'][1]
            )
            high = (
                self._ends[1][0]+DIRECTIONS[self._direction]['high'][0],
                self._ends[1][1]+DIRECTIONS[self._direction]['high'][1]
            )
            return [low, high]
        else:
            spaces = []
            for _, offset in DIRECTIONS.items():
                spaces.append((self.moves[0][0]+offset['low'][0], self.moves[0][1]+offset['low'][1]))
                spaces.append((self.moves[0][0]+offset['high'][0], self.moves[0][1]+offset['high'][1]))
            return spaces

    def next_space_count(self, move, direction, is_out_of_game_fn):
        spaces = self.next_spaces(direction=direction)
        print(move, spaces, flush=True)
        count = 0 if is_out_of_game_fn(spaces[0]) or spaces[0] == move else 1
        count += 0 if is_out_of_game_fn(spaces[1]) or spaces[1] == move else 1
        return count


