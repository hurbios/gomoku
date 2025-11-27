from itertools import product
# from functools import reduce
# from typing import Generator
from gomoku.core.player_rows import Row
from gomoku.core.directions import DIRECTIONS
from gomoku.core.config import INSPECT_DEPTH, DEBUG
from gomoku.core.helper import debug_log


class Board:
    def __init__(self, width:int, height:int):
        self.__width = width
        self.__height = height
        self.__moves = [[0 for _ in range(height)] for _ in range(width)]
        self.__player1_rows = []
        self.__player2_rows = []
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
            debug_log('player1 rows')
            for row in self.__player1_rows:
                debug_log(row)
        return self.__player1_rows

    @property
    def player2_rows(self)->list[Row]:
        if DEBUG:
            debug_log('player2 rows')
            for row in self.__player2_rows:
                debug_log(row)
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
        for direction in DIRECTIONS:
            surrounding_moves_in_direction = get_surrounding_moves_of_direction(move, direction)
            players_surrounding_rows_in_direction[direction] = self.__get_rows_containing_move(surrounding_moves_in_direction[0], player)
            players_surrounding_rows_in_direction[direction] += self.__get_rows_containing_move(surrounding_moves_in_direction[1], player)

        return players_surrounding_rows_in_direction


    ## ERROR. The rows are inserted twice if touching
    def __add_building_move_to_rows(self, move:tuple[int, int], player:int):
        player_rows = self.__get_players_surrounding_rows_in_directions(move, player)
        rows_added = []
        rows_to_remove = []
        for direction in DIRECTIONS:
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
        debug_log(f"added_rows {len(added_rows[len(added_rows)-1])}")

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

    def remove_move(self, move:tuple[int, int], player:int):
        self.__moves[move[0]][move[1]] = 0
        self.__remove_move_from_rows(move, player)
        for row in self.__player1_rows:
            if move in row.surrounding_moves:
                row.refresh_potential()

        for row in self.__player2_rows:
            if move in row.surrounding_moves:
                row.refresh_potential()

    def get_player_pieces(self, player:int):
        moves = set()
        player_rows = self.__player1_rows if player == 1 else self.__player2_rows
        for row in player_rows:
            moves.update(row.moves)
        return moves

    def reset(self):
        self.__moves = [[0 for _ in range(self.__height)] for _ in range(self.__width)]
        self.__player1_rows = []
        self.__player2_rows = []
        self.__inspect_moves = set()

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
        debug_log(f"depth {depth} score after player {player} move {move}: {score}")
        return score
