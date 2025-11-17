from itertools import product
from functools import reduce
from gomoku.core.player_rows import Row
from gomoku.core.directions import DIRECTIONS


class Board:
    def __init__(self, width:int, height:int):
        self.__width = width
        self.__height = height
        self.__moves = [[0 for _ in range(height)] for _ in range(width)]
        self.__player1_rows = []
        self.__player2_rows = []

    def size(self):
        return len(self.__moves), len(self.__moves[0])
            
    def __is_outside_of_game_area(self, move:tuple[int, int]):
        return any(iter([
                (self.__width <= move[0]),
                (move[0] < 0),
                (self.__height <= move[1]),
                (move[1] < 0),
              ]))

    def __get_rows_containing_move(self, move:tuple[int, int], player:int):
        rows_containing_move = []
        player_rows = self.__player1_rows if player == 1 else self.__player2_rows
        for row in player_rows:
            if row.contains(move):
                rows_containing_move.append(row)
        return rows_containing_move

    def __get_close_rows(self, move:tuple[int, int], player:int):
        def surrounding_moves(move:tuple[int,int]):
            for offset in DIRECTIONS.values():
                yield (move[0]-offset['low'][0], move[1]-offset['low'][1])
                yield (move[0]-offset['high'][0], move[1]-offset['high'][1])
        
        player_close_rows = []
        for surrounding_move in surrounding_moves(move):
            player_close_rows += self.__get_rows_containing_move(surrounding_move, player)

        return player_close_rows

    def __add_building_move_to_rows(self, move:tuple[int, int], player:int):
        player_rows = self.__get_close_rows(move, player)
        rows_added = []

        if len(player_rows) > 0:
            for row in player_rows:
                if row.row_relation(move) == 'builds':
                    row.add(move)
                    rows_added.append(row)
        
        #TODO: create new row for touching but not building rows 

        if len(rows_added) <= 0:
            new_row = Row([move])
            if player == 1:
                self.__player1_rows.append(new_row)
            else:
                self.__player2_rows.append(new_row)
            rows_added.append(new_row)

        return rows_added

    # Returns tuple: (True if player piece was added, True if player wins)
    def add_move(self, move:tuple[int, int], player:int)->tuple[bool, bool]:
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
        
        added_rows = self.__add_building_move_to_rows(move, player)
        # print(added_rows)
        for row in added_rows:
            if len(row) >= 5:
                return True, True

        return True, False

    def __remove_move_from_rows(self, move:tuple[int, int], player:int):
        rows = self.__get_rows_containing_move(move, player)
        for row in rows:
            row.remove(move)

    def remove_move(self, move:tuple[int, int], player:int):
        self.__moves[move[0]][move[1]] = 0
        self.__remove_move_from_rows(move, player)

    def get_player_pieces(self, player:int):
        moves = []
        player_rows = self.__player1_rows if player == 1 else self.__player2_rows
        for row in player_rows:
            moves += row.moves
        return moves

    def reset(self):
        self.__moves = [[0 for _ in range(self.__height)] for _ in range(self.__width)]
        self.__player1_rows = []
        self.__player2_rows = []

    def get_surrounding_free_coordinates(self, position:tuple[int, int], depth:int=1):
        def surrounding_moves():
            offset_number_list = list(range(-depth, depth+1))
            move_offsets = list(product(offset_number_list, repeat=2))
            move_offsets.remove((0,0))
            for offset in move_offsets:
                yield (position[0]+offset[0], position[1]+offset[1])

        free_coordinates = []
        for surrounding_move in surrounding_moves():
            if not self.__is_outside_of_game_area(surrounding_move):
                if not self.__moves[surrounding_move[0]][surrounding_move[1]]:
                    free_coordinates.append(surrounding_move)

        return free_coordinates


    ############################
    ### Move evaluations #######
    ############################
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
