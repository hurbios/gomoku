from itertools import product
from functools import reduce
# from typing import Generator
from gomoku.core.player_rows import Row
from gomoku.core.directions import DIRECTIONS
from gomoku.core.config import INSPECT_DEPTH, DEBUG


class Board:
    def __init__(self, width:int, height:int):
        self.__width = width
        self.__height = height
        self.__moves = [[0 for _ in range(height)] for _ in range(width)]
        self.__player1_rows = list()
        self.__player2_rows = list()
        self.__inspect_moves = set()

    def size(self):
        return len(self.__moves), len(self.__moves[0])
    
    @property
    def height(self):
        return self.__height
    
    @property
    def width(self):
        return self.__width
    
    @property
    def moves(self):
        return self.__moves

    @property
    def player1_rows(self)->list[Row]:
        if DEBUG:
            print('player1 rows')
            for row in self.__player1_rows:
                print(row)
        return self.__player1_rows
    
    @property
    def player2_rows(self)->list[Row]:
        if DEBUG:
            print('player2 rows')
            for row in self.__player2_rows:
                print(row)
        return self.__player2_rows
    
    @property
    def inspect_moves(self):
        return self.__inspect_moves
    
    def __get_player_rows_list(self, player:int)->list[Row]:
        return self.__player1_rows if player == 1 else self.__player2_rows

    def is_free_space(self, move:tuple[int, int]):
        return not self.__moves[move[0]][move[1]]
    
    def is_outside_of_game_area(self, move:tuple[int, int]):
        return any(iter([
                (self.__width <= move[0]),
                (move[0] < 0),
                (self.__height <= move[1]),
                (move[1] < 0),
              ]))

    def __get_rows_containing_move(self, move:tuple[int, int], player:int)->list[Row]:
        rows_containing_move = []
        player_rows = self.__player1_rows if player == 1 else self.__player2_rows
        for row in player_rows:
            if row.contains(move):
                rows_containing_move.append(row)
        return rows_containing_move

    def __get_players_surrounding_rows_in_directions(self, move:tuple[int, int], player:int)->dict[str, Row]:
        def get_surrounding_moves_of_direction(move:tuple[int,int], direction:str)->tuple[tuple[int,int],tuple[int,int]]:
            offset = DIRECTIONS[direction]
            return (
                (move[0]-offset['low'][0], move[1]-offset['low'][1]),
                (move[0]-offset['high'][0], move[1]-offset['high'][1])
            )
        
        players_surrounding_rows_in_direction = {}
        for direction in DIRECTIONS.keys():
            surrounding_moves_in_direction = get_surrounding_moves_of_direction(move, direction)
            players_surrounding_rows_in_direction[direction] = self.__get_rows_containing_move(surrounding_moves_in_direction[0], player)
            players_surrounding_rows_in_direction[direction] += self.__get_rows_containing_move(surrounding_moves_in_direction[1], player)

        return players_surrounding_rows_in_direction


    ## ERROR. The rows are inserted twice if touching 
    def __add_building_move_to_rows(self, move:tuple[int, int], player:int):
        player_rows = self.__get_players_surrounding_rows_in_directions(move, player)
        rows_added = []
        rows_to_remove = []
        for direction in DIRECTIONS.keys():
            direction_row_added = None
            for row in player_rows[direction]:
                if row.row_relation(move) == 'builds': #TODO improve by adding direction to relation check
                    # DEBUG and print('builds')
                    if not direction_row_added:
                        # DEBUG and print('no dir row')
                        direction_row_added = row
                        row.add(move)
                        rows_added.append(row)
                    else:
                        # DEBUG and print('yes dir row')
                        direction_row_added.join_row(move, row) # join connected same direction rows
                        rows_to_remove.append(row)
                elif row.row_relation(move) == 'touches': # create new row for touching but not building rows
                    # DEBUG and print('touches')
                    if not direction_row_added:
                        # DEBUG and print('no dir row')
                        new_row = Row([move, row.get_touching_building_move(move, direction)], self)
                        direction_row_added = new_row
                        rows_added.append(new_row)
                        self.__get_player_rows_list(player).append(new_row)
                    else:
                        # DEBUG and print('yes dir row')
                        direction_row_added.add(row.get_touching_building_move(move, direction)) # join connected same direction rows
        for row in rows_to_remove:
            self.__get_player_rows_list(player).remove(row)
        if len(rows_added) <= 0:
            new_row = Row([move], self)
            self.__get_player_rows_list(player).append(new_row)
            rows_added.append(new_row)

        return rows_added

    def __recalculate_inspectable_area_after_move_addition(self, move:tuple[int,int], depth:int):
        if move in self.__inspect_moves:
            self.__inspect_moves.remove(move)
        self.__inspect_moves.update(self.get_surrounding_free_coordinates(move, depth))

    # Returns tuple: (True if player piece was added, True if player wins)
    def add_move(self, move:tuple[int, int], player:int, update_inspect_moves:bool = False)->tuple[bool, bool]:
        # Check that the move is within the game area boundaries and valid player
        if self.is_outside_of_game_area(move) or player not in [1,2]:
            return False, False

        # Check that no piece exists yet in the move coordinates
        if self.__moves[move[0]][move[1]]:
            return False, False
        # Check that the player is valid
        if player not in [1,2]:
            return False, False

        # Add move to players pieces and on game board
        self.__moves[move[0]][move[1]] = player

        for row in self.__player1_rows:
            if move in row.surrounding_moves:
                row.refresh_potential()
        
        for row in self.__player2_rows:
            if move in row.surrounding_moves:
                row.refresh_potential()

        added_rows = self.__add_building_move_to_rows(move, player)
        DEBUG and print('added_rows', len(added_rows[len(added_rows)-1]), flush=True)

        if update_inspect_moves:
            self.__recalculate_inspectable_area_after_move_addition(move, INSPECT_DEPTH)

        for row in added_rows:
            if len(row) >= 5:
                return True, True

        return True, False

    def __remove_move_from_rows(self, move:tuple[int, int], player:int):
        rows = self.__get_rows_containing_move(move, player)
        for row in rows:
            if len(row) <= 1:
                player_rows = self.__get_player_rows_list(player)
                player_rows.remove(row)
            else:
                new_row = row.remove(move) # will split to old and new row if move is not at the end of row
                if new_row:
                    if len(new_row) > 1 or len(self.__get_rows_containing_move(new_row.moves[0], player)) <= 1:
                        self.__get_player_rows_list(player).append(new_row)
                if len(row) <= 1:
                    if len(self.__get_rows_containing_move(row.moves[0], player)) > 1:
                        player_rows = self.__get_player_rows_list(player)
                        player_rows.remove(row)
        return

    def remove_move(self, move:tuple[int, int], player:int):
        self.__moves[move[0]][move[1]] = 0
        self.__remove_move_from_rows(move, player)
        # self.player1_rows #TODO: remove líne
        for row in self.__player1_rows:
            if move in row.surrounding_moves:
                row.refresh_potential()
        
        for row in self.__player2_rows:
            if move in row.surrounding_moves:
                row.refresh_potential()
        return

    def get_player_pieces(self, player:int):
        moves = []
        player_rows = self.__player1_rows if player == 1 else self.__player2_rows
        for row in player_rows:
            moves += row.moves
        return moves

    def reset(self):
        self.__moves = [[0 for _ in range(self.__height)] for _ in range(self.__width)]
        self.__player1_rows = list()
        self.__player2_rows = list()
        self.__inspect_moves = set()
        return

    def get_surrounding_free_coordinates(self, position:tuple[int, int], depth:int=1):
        def surrounding_moves():
            offset_number_list = list(range(-depth, depth+1))
            move_offsets = list(product(offset_number_list, repeat=2))
            move_offsets.remove((0,0))
            for offset in move_offsets:
                yield (position[0]+offset[0], position[1]+offset[1])

        free_coordinates = set()
        for surrounding_move in surrounding_moves():
            if not self.is_outside_of_game_area(surrounding_move):
                if not self.__moves[surrounding_move[0]][surrounding_move[1]]:
                    free_coordinates.add(surrounding_move)

        return free_coordinates


    ############################
    ### Move evaluations #######
    ############################

    def evaluate_state(self, player, move, depth):
        score = 0
        for row in self.player1_rows:
            score -= row.score
        for row in self.player2_rows:
            score += row.score
        # DEBUG and print(f"score after player {player} move: {score}")
        # print(f"depth {depth} score after player {player} move {move}: {score}", flush=True)
        return score

    ### Below not currently used

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
                # print('rows[0]')
                # print(rows[0])
                count0 = len(rows[0])
                next_spaces_count_0 = sum(1 for n in rows[0].next_spaces() if not self.is_outside_of_game_area(n) and not self.__moves[n[0]][n[1]])
                if len(rows) > 1:
                    count1 = len(rows[1])
                    next_spaces_count_1 = sum(1 for n in rows[1].next_spaces() if not self.is_outside_of_game_area(n) and not self.__moves[n[0]][n[1]])
        # else:
        #     other_players_rows_in_direction = self.__get_players_surrounding_rows_in_directions(move, 2 if player == 1 else 1)
        #     dir_rows = {}
        #     for row in rows:
        #         row_direction = row.get_direction(move)
        #         if row_direction not in dir_rows:
        #             dir_rows[row_direction] = [0,0] # len, empty space
        #         dir_rows[row_direction][0] += len(row)
        #         dir_rows[row_direction][1] += row.next_space_count(move, row_direction, self.is_outside_of_game_area)
            
        #     for val in dir_rows.values():
        #         if val[0] > count0:
        #             count0 = val[0]
        #             next_spaces_count_0 = val[1]
        #         elif val[0] > count1:
        #             count1 = val[0]
        #             next_spaces_count_1 = val[1]

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

        # print("counts: ", count_usr, usr_empty_spaces)
        # print(self.__player1_rows[0].moves,self.__player1_rows[0].contains(move), self.__player1_rows[0].row_relation(move))

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
