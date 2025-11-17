from itertools import product
from functools import reduce
from gomoku.core.player_rows import Row

DIRECTIONS = {
    'vertical': { # -
        'high': (1,0),
        'low': (-1,0)
    },
    'horizontal': { # |
        'high': (0,1),
        'low': (0,-1),
    },
    'diagonal': { # /
        'high': (1,1),
        'low': (-1,-1)
    },
    'inverse_diagonal': { # \
        'high': (1,-1),
        'low': (-1,1),
    },
}

class Board:
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__moves = [[0 for _ in range(height)] for _ in range(width)]
        self.__player1_rows = []
        self.__player2_rows = []

    def size(self):
        return len(self.__moves), len(self.__moves[0])

    def __count_pieces_direction(self, count:int, position:tuple[int, int], player:int, direction:tuple[int, int], row_pieces: list[tuple[int,int]]):
        # return if already win amount
        if count >= 5:
            return 5, row_pieces
        # check map boundaries
        if any(iter([(self.__width <= (position[0]+direction[0])),
            ((position[0]+direction[0]) < 0),
            self.__height <= (position[1]+direction[1]),
            ((position[1]+direction[1]) < 0)])):
            return count, row_pieces
        # check if current position is the players piece
        if self.__moves[position[0]+direction[0]][position[1]+direction[1]] is not player:
            return count, row_pieces
        # recursion
        row_pieces.append((position[0]+direction[0], position[1]+direction[1]))
        return self.__count_pieces_direction(count+1, (position[0]+direction[0], position[1]+direction[1]), player, direction, row_pieces)


    def __get_direction_row(self, position:tuple[int, int], player:int, direction:str):
        row_pieces = ([],[])
        match direction:
            case 'vertical':
                return ((self.__count_pieces_direction(0,position,player,DIRECTIONS['vertical']['high'], row_pieces[0]),
                        self.__count_pieces_direction(0,position,player,DIRECTIONS['vertical']['low'], row_pieces[1])))
            case 'horizontal':
                return ((self.__count_pieces_direction(0,position,player,DIRECTIONS['horizontal']['high'], row_pieces[0]),
                        self.__count_pieces_direction(0,position,player,DIRECTIONS['horizontal']['low'], row_pieces[1])))
            case 'inverse_diagonal':
                return ((self.__count_pieces_direction(0,position,player,DIRECTIONS['inverse_diagonal']['high'], row_pieces[0]),
                        self.__count_pieces_direction(0,position,player,DIRECTIONS['inverse_diagonal']['low'], row_pieces[1])))
            case 'diagonal':
                return ((self.__count_pieces_direction(0,position,player,DIRECTIONS['diagonal']['high'], row_pieces[0]),
                        self.__count_pieces_direction(0,position,player,DIRECTIONS['diagonal']['low'], row_pieces[1])))
            case _:
                return row_pieces
            
    def get_direction_count(self, position:tuple[int, int], player:int, direction:str):
        rows_dirs = self.__get_direction_row(position, player, direction)
        if len(rows_dirs[0]) <= 0:
            return 0
        return rows_dirs[0][0]+rows_dirs[1][0] + 1

    # returns pair (count, direction)
    def __get_max_in_row_count(self, move: tuple[int, int], player:int):
        return sorted([
            (self.get_direction_count(move,player,direction),direction) for direction in DIRECTIONS.keys()
        ], reverse=True)

    def __is_outside_of_game_area(self, move: tuple[int, int]):
        return any(iter([
                (self.__width <= move[0]),
                (move[0] < 0),
                (self.__width <= move[1]),
                (move[1] < 0),
                (self.__height <= move[0]),
                (move[0] < 0),
                (self.__height <= move[1]),
                (move[1] < 0)
              ]))

    def __get_close_rows(self, move, player):
        player_close_rows = []
        player_rows = self.__player1_rows if player == 1 else self.__player2_rows
        for row in player_rows:
            row_relation = row.row_relation(move)
            if row_relation:
                player_close_rows.append((row_relation, row))
        return player_close_rows

    def __get_rows_containing_move(self, move, player):
        rows_containing_move = []
        player_rows = self.__player1_rows if player == 1 else self.__player2_rows
        for row in player_rows:
            if row.contains(move):
                rows_containing_move.append(row)
        return rows_containing_move

    def add_building_move_to_rows(self, move, player):
        player_rows = self.__get_close_rows(move, player)
        rows_added = []

        if len(player_rows) > 0:
            for row in player_rows:
                if row[0] == 'builds':
                    row[1].add(move)
                    rows_added.append(row[1])

        if len(rows_added) <= 0:
            new_row = Row([move])
            if player == 1:
                self.__player1_rows.append(new_row)
            else:
                self.__player2_rows.append(new_row)

        return rows_added

    # Returns tuple: (True if player piece was added, True if player wins)
    def add_move(self, move: tuple[int, int], player:int)->tuple[bool, bool]:
        # Check that the move is within the game area boundaries
        if self.__is_outside_of_game_area(move):
            return False, False

        # Check that no piece exists yet in the move coordinates
        if self.__moves[move[0]][move[1]]:
            return False, False
        # Check that the player is valid
        if player not in [1,2]:
            return False, False

        # Add move to players pieces and on game board
        self.__moves[move[0]][move[1]] = player

        # TODO: handle joining rows if needed
        
        added_rows = self.add_building_move_to_rows(move, player)
        # print(added_rows)
        for row in added_rows:
            if len(row) >= 5:
                return True, True

        return True, False

    def remove_move_from_row(self, move, player):
        rows = self.__get_rows_containing_move(move, player)
        for row in rows:
            row.remove(move)

    def remove_move(self, move: tuple[int, int], player:int):
        self.__moves[move[0]][move[1]] = 0
        self.remove_move_from_row(move, player)

    def get_player_pieces(self, player):
        moves = []
        player_rows = self.__player1_rows if player == 1 else self.__player2_rows
        for row in player_rows:
            moves += row.moves
        return moves

    def reset(self):
        self.__moves = [[0 for _ in range(self.__height)] for _ in range(self.__width)]
        self.__player1_rows = []
        self.__player2_rows = []

    # returns 2 coordinates. Bot sides of the line if empty space exists
    def __get_next_coordinate(self, position:tuple[int, int], player:int, direction:tuple[int, int]):
        # check map boundaries
        if any(iter([(self.__width <= (position[0]+direction[0])),
            ((position[0]+direction[0]) < 0),
            self.__height <= (position[1]+direction[1]),
            ((position[1]+direction[1]) < 0)])):
            return None
        # check if current position is the players piece
        if self.__moves[position[0]+direction[0]][position[1]+direction[1]] is not player:
            # return position only if empty space
            if not self.__moves[position[0]+direction[0]][position[1]+direction[1]]:
                return (position[0]+direction[0],position[1]+direction[1])
            return None
        # recursion
        return self.__get_next_coordinate((position[0]+direction[0], position[1]+direction[1]),player,direction)

    def get_next_free_coordinates(self, position:tuple[int, int], player:int, direction:str):
        match direction:
            case 'vertical':
                return ((self.__get_next_coordinate(position,player,(1,0)), self.__get_next_coordinate(position,player,(-1,0))))
            case 'horizontal':
                return ((self.__get_next_coordinate(position,player,(0,1)), self.__get_next_coordinate(position,player,(0,-1))))
            case 'inverse_diagonal':
                return ((self.__get_next_coordinate(position,player,(1,-1)), self.__get_next_coordinate(position,player,(-1,1))))
            case 'diagonal':
                return ((self.__get_next_coordinate(position,player,(-1,-1)), self.__get_next_coordinate(position,player,(1,1))))
            case _:
                return None,None

    def get_surrounding_free_coordinates(self, position:tuple[int, int], depth:int=1):
        offset_number_list = list(range(-depth, depth+1))
        move_offsets = list(product(offset_number_list, repeat=2))
        move_offsets.remove((0,0))
        free_coordinates = []
        for offset in move_offsets:
            new_position = (position[0]+offset[0], position[1]+offset[1])
            if not self.__is_outside_of_game_area(new_position):
                if not self.__moves[new_position[0]][new_position[1]]:
                    free_coordinates.append(new_position)
        return free_coordinates


    ############################
    ### Move evaluations #######
    ############################

    def __get_direction_counts(self, move, player):
        rows = self.__get_close_rows(move, player)
        dir_rows = {}
        dir_counts = []
        for row in rows:
            if row[0] == 'builds':
                if row[1].direction not in dir_rows:
                    dir_rows[row[1].direction] = []
                dir_rows[row[1].direction].append(row)
            if row[0] == 'touches':
                pass #TODO
        for dir in DIRECTIONS.keys():
            count = reduce(lambda x, y: len(x[1]) * len(y[1]), dir_rows[dir])
            dir_counts.append((count, dir))
        return dir_counts

    # calculate touches to actually block!! 
    def get_player_move_result(self, move, player):
        count0=0
        next_spaces_count_0=0
        count1=0
        next_spaces_count_1=0

        if self.__moves[move[0]][move[1]] == player:
            rows = self.__get_rows_containing_move(move, player)
            rows.sort(key=len,reverse=True)
            if len(rows) > 0:
                count0 = len(rows[0])
                next_spaces_count_0 = sum(1 for n in rows[0].next_spaces() if not self.__moves[n[0]][n[1]])
                if len(rows) > 1:
                    count1 = len(rows[1])
                    next_spaces_count_1 = sum(1 for n in rows[1].next_spaces() if not self.__moves[n[0]][n[1]])
        else:
            rows = self.__get_close_rows(move, 2 if player == 1 else 1)
            dir_rows = {}
            for row in rows:
                row_direction = row[1].get_direction(move)
                if row_direction not in dir_rows:
                    dir_rows[row_direction] = [0,0] # len, empty space
                dir_rows[row_direction][0] += len(row[1])
                dir_rows[row_direction][1] += row[1].next_space_count(move, row_direction, self.__is_outside_of_game_area)
            
            for val in dir_rows.values():
                if val[0] > count0:
                    count0 = val[0]
                    next_spaces_count_0 = val[1]
                elif val[0] > count1:
                    count1 = val[0]
                    next_spaces_count_1 = val[1]

        return count0, next_spaces_count_0, count1, next_spaces_count_1

    def __get_count_for_x_order_direction(self, move:tuple[int, int], player:int):
        # TODO: improve: if multiple same, get the one with most empty spaces
        ordered_max_counts_high_to_low = self.__get_max_in_row_count(move, player)
        count, direction = ordered_max_counts_high_to_low[0]
        next_coordinates = self.get_next_free_coordinates(move, player, direction)
        empty_spaces = sum(1 for n in next_coordinates if n is not None)
        second_count, second_direction = ordered_max_counts_high_to_low[1]
        if count >= 3 and second_count >= 3:
            second_next_coordinates = self.get_next_free_coordinates(move, 1, second_direction)
            second_empty_spaces = sum(1 for n in second_next_coordinates if n is not None)
        else:
            second_empty_spaces = 0
        return count, empty_spaces, second_count, second_empty_spaces

    def evaluate_move(self, move:tuple[int, int]):
        (
            count_usr,
            usr_empty_spaces,
            second_count_usr,
            second_usr_empty_spaces
        ) = self.__get_count_for_x_order_direction(move, 1)

        (
            count_ai,
            ai_empty_spaces,
            second_count_ai,
            second_ai_empty_spaces
        ) = self.__get_count_for_x_order_direction(move, 2)

        evaluations = (
            # # 0.  LOST - other has 5th in row ((-8))
            # (count_usr >= 6, 16),
            # 1.  ATTACK - add 5th for the row ((8))
            (count_ai >= 5, 15),
            # 2.  BLOCK - block 5th in a row with one sided empty space ((-7))
            (count_usr >= 5, 14),
            # 3.  ATTACK - add 4th in a row (two empty space) ((7))
            (count_ai >= 4 and ai_empty_spaces >= 2, 13),
            # 3.  ATTACK - add 4th in a row (one empty space) ((6))
            (count_ai >= 4 and ai_empty_spaces >= 1, 12),
            # 4.  BLOCK - block 4th in a row with both sides empty space ((-6))
            (count_usr >= 4 and usr_empty_spaces >= 2, 11),
            # 5.  ATTACK - add center for dual 3rd in a row with empty spaces around (3)  ((5))
            (count_ai >= 3 and second_count_ai >= 3 and ai_empty_spaces + second_ai_empty_spaces >= 3, 10),
            # 6.  BLOCK - block center for dual 3rd in a row with empty spaces around (4) ((-5))
            (count_usr >= 3 and second_count_usr >= 3 and usr_empty_spaces + second_usr_empty_spaces >= 4, 9),
            # 7.  ATTACK - add 3rd in a row with empty spaces around ((4))
            (count_ai >= 3 and ai_empty_spaces >= 2, 8),
            # 8.  BLOCK - block center for dual 3rd in a row with 3 or less empty spaces around ((-4))
            (count_usr >= 3 and second_count_usr >= 3 and usr_empty_spaces + second_usr_empty_spaces >= 3, 7),
            # 9.  ATTACK - add 3rd in a row with one side empty space ((3))
            (count_ai >= 3 and ai_empty_spaces >= 1, 6),
            # 10. BLOCK - block 4th in a row with one side empty space ((-3))
            (count_usr >= 4 and usr_empty_spaces >= 1, 5),
            # 11. BLOCK - block 3rd in a row with empty spaces around ((-2))
            (count_usr >= 3 and usr_empty_spaces >= 2, 4),
            # 12. ATTACK - add 2nd in a row with empty spaces around ((2))
            (count_ai >= 2 and ai_empty_spaces >= 2,3),
            # 13. BLOCK - block 3rd in a row with one side empty spaces around ((-1))
            (count_usr >= 3 and usr_empty_spaces >= 1, 2),
            # 14. BLOCK - block 2nd in a row with empty spaces around (4) ((0))
            (count_usr >= 2 and usr_empty_spaces >= 2, 1),
            # 15. ATTACK - add 1st in a row with as many empty spaces around as possible ((1))
            (count_usr >= 1 and usr_empty_spaces >= 2, 0)
        )

        # TODO: remove obsolete logging
        # for i,evaluation in enumerate(iter(evaluations)):
        for evaluation in iter(evaluations):
            # print(i, evaluation[0], evaluation[1], count_ai, ai_empty_spaces)
            if evaluation[0]:
                return evaluation[1]

        return 0

    def evaluate_state_after_move(self, move:tuple[int, int])->int:
        (
            count_usr,
            usr_empty_spaces,
            second_count_usr,
            second_usr_empty_spaces
        ) = self.get_player_move_result(move, 1)

        (
            count_ai,
            ai_empty_spaces,
            second_count_ai,
            second_ai_empty_spaces
        ) = self.get_player_move_result(move, 2)

        print("counts: ", count_usr, usr_empty_spaces)
        print(self.__player1_rows[0].moves,self.__player1_rows[0].contains(move), self.__player1_rows[0].row_relation(move))

        evaluations = (
            # # 0.  LOST - other has 5th in row ((-8))
            # (count_usr >= 6, -8),
            # 1.  ATTACK - add 5th for the row ((8))
            (count_ai >= 5, 8),
            # 2.  BLOCK - block 5th in a row with one sided empty space ((-7))
            (count_usr >= 5, -8),
            # 3.  ATTACK - add 4th in a row (two empty space) ((7))
            (count_ai >= 4 and ai_empty_spaces >= 2, 7),
            # 3.  ATTACK - add 4th in a row (one empty space) ((6))
            (count_ai >= 4 and ai_empty_spaces >= 1, 6),
            # 4.  BLOCK - block 4th in a row with both sides empty space ((-6))
            (count_usr >= 4 and usr_empty_spaces >= 2, -7),
            # 5.  ATTACK - add center for dual 3rd in a row with empty spaces around (3)  ((5))
            (count_ai >= 3 and second_count_ai >= 3 and ai_empty_spaces + second_ai_empty_spaces >= 3, 5),
            # 6.  BLOCK - block center for dual 3rd in a row with empty spaces around (4) ((-5))
            (count_usr >= 3 and second_count_usr >= 3 and usr_empty_spaces + second_usr_empty_spaces >= 4, -6),
            # 7.  ATTACK - add 3rd in a row with empty spaces around ((4))
            (count_ai >= 3 and ai_empty_spaces >= 2, 4),
            # 8.  BLOCK - block center for dual 3rd in a row with 3 or less empty spaces around ((-4))
            (count_usr >= 3 and second_count_usr >= 3 and usr_empty_spaces + second_usr_empty_spaces >= 3, -5),
            # 9.  ATTACK - add 3rd in a row with one side empty space ((3))
            (count_ai >= 3 and ai_empty_spaces >= 1, 3),
            # 10. BLOCK - block 4th in a row with one side empty space ((-3))
            (count_usr >= 4 and usr_empty_spaces >= 1, -4),
            # 11. BLOCK - block 3rd in a row with empty spaces around ((-2))
            (count_usr >= 3 and usr_empty_spaces >= 2, -3),
            # 12. ATTACK - add 2nd in a row with empty spaces around ((2))
            (count_ai >= 2 and ai_empty_spaces >= 2,2),
            # 13. BLOCK - block 4th in a row with one side empty spaces around ((-1))
            (count_usr >= 3 and usr_empty_spaces >= 1, -2),
            # 14. BLOCK - block 3nd in a row with empty spaces around (4) ((0))
            (count_usr >= 2 and usr_empty_spaces >= 2, -1),
            # 15. BLOCK - block 1st in a row with as many empty spaces around as possible ((1))
            (count_ai >= 1 and ai_empty_spaces >= 2, 1),
            # 15. ATTACK - add 1st in a row with as many empty spaces around as possible ((1))
            (count_usr >= 1 and usr_empty_spaces >= 2, 0)
        )

        # TODO: remove obsolete logging
        # for i,evaluation in enumerate(iter(evaluations)):
        for evaluation in iter(evaluations):
            # print(i, evaluation[0], evaluation[1], count_ai, ai_empty_spaces)
            if evaluation[0]:
                return evaluation[1]

        return 0
