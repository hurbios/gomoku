# from typing import Generator
from gomoku.core.player_rows import Row
from gomoku.core.directions import DIRECTIONS


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
        return self.__player1_rows

    @property
    def player2_rows(self)->list[Row]:
        return self.__player2_rows

    @property
    def inspect_moves(self):
        return self.__inspect_moves

    def __get_player_rows_list(self, player:int)->list[Row]:
        return self.__player1_rows if player == 1 else self.__player2_rows

    def is_free_space(self, move:tuple[int, int]):
        return not self.__moves[move[0]][move[1]]

    def is_outside_of_game_area(self, move:tuple[int, int]):
        """check if the move is inside game area limits"""
        return any(iter([
                (self.__width <= move[0]),
                (move[0] < 0),
                (self.__height <= move[1]),
                (move[1] < 0),
              ]))

    def __get_rows_containing_move(self, move:tuple[int, int], player:int)->list[Row]:
        """get all the players rows that are containing the move"""
        rows_containing_move = []
        player_rows = self.__player1_rows if player == 1 else self.__player2_rows
        for row in player_rows:
            if row.contains(move):
                rows_containing_move.append(row)
        return rows_containing_move

    def __get_players_surrounding_rows_in_directions(self, move:tuple[int, int], player:int)->dict[str, Row]:
        """get players rows of each direction"""
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

    def __add_building_move_to_rows(self, move:tuple[int, int], player:int):
        """
        add move to players rows if the move is building the rows
        create a new row of 2 pieces if the move is not building but touching the row
        create a new row of 1 pieces if the move is not touching or building any of the players rows
        """
        player_rows = self.__get_players_surrounding_rows_in_directions(move, player)
        rows_added = []
        rows_to_remove = []
        for direction in DIRECTIONS:
            direction_row_added = None
            for row in player_rows[direction]:
                if row.row_relation(move) == 'builds': #TODO improve by adding direction to relation check
                    if not direction_row_added:
                        direction_row_added = row
                        row.add(move)
                        rows_added.append(row)
                    else:
                        direction_row_added.join_row(move, row) # join connected same direction rows
                        rows_to_remove.append(row)
                elif row.row_relation(move) == 'touches': # create new row for touching but not building rows
                    if not direction_row_added:
                        new_row = Row([move, row.get_touching_building_move(move, direction)], self)
                        direction_row_added = new_row
                        rows_added.append(new_row)
                        self.__get_player_rows_list(player).append(new_row)
                    else:
                        direction_row_added.add(row.get_touching_building_move(move, direction)) # join connected same direction rows
        for row in rows_to_remove:
            self.__get_player_rows_list(player).remove(row)
        if len(rows_added) <= 0:
            new_row = Row([move], self)
            self.__get_player_rows_list(player).append(new_row)
            rows_added.append(new_row)

        return rows_added

    def __recalculate_inspectable_area_after_move_addition(self, move:tuple[int,int]):
        """recalculate the new area that is inspectable after a move is added"""
        if move in self.__inspect_moves:
            self.__inspect_moves.remove(move)
        surrounding_free_moves = self.get_surrounding_free_coordinates(move)
        self.__inspect_moves.update(surrounding_free_moves[0].union(surrounding_free_moves[1]))

    def add_move(self, move:tuple[int, int], player:int, update_inspect_moves:bool = False)->tuple[bool, bool]:
        """
        Add a move to board. Refresh/add to rows. Refresh surrounding free moves.
        Returns tuple: (True if player piece was added, True if player wins)
        """
        # Check that the move is within the game area boundaries and valid player
        if self.is_outside_of_game_area(move) or player not in [1,2]:
            return False, False

        # Check that no piece exists yet in the move coordinates
        if self.__moves[move[0]][move[1]]:
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

        if update_inspect_moves:
            self.__recalculate_inspectable_area_after_move_addition(move)

        for row in added_rows:
            if len(row) >= 5:
                return True, True

        return True, False

    def __remove_move_from_rows(self, move:tuple[int, int], player:int):
        """removes move from all rows"""
        rows = self.__get_rows_containing_move(move, player)
        for row in rows:
            if len(row) <= 1:
                player_rows = self.__get_player_rows_list(player)
                player_rows.remove(row)
            else:
                new_row = row.remove(move) # will split to old and new row if move is not at the end of row
                if new_row:
                    if len(new_row) > 1 or len(self.__get_rows_containing_move(new_row.moves[0], player)) < 1:
                        self.__get_player_rows_list(player).append(new_row)
                if len(row) <= 1:
                    if len(self.__get_rows_containing_move(row.moves[0], player)) > 1:
                        player_rows = self.__get_player_rows_list(player)
                        player_rows.remove(row)

    def remove_move(self, move:tuple[int, int], player:int):
        """
        remove a move from all players rows and from board.
        refresh row all row potentials after removal that have relation to the move
        """
        self.__moves[move[0]][move[1]] = 0
        self.__remove_move_from_rows(move, player)
        for row in self.__player1_rows:
            if move in row.surrounding_moves:
                row.refresh_potential()

        for row in self.__player2_rows:
            if move in row.surrounding_moves:
                row.refresh_potential()

    def get_player_pieces(self, player:int):
        """returns all players played moves"""
        moves = set()
        player_rows = self.__player1_rows if player == 1 else self.__player2_rows
        for row in player_rows:
            moves.update(row.moves)
        return moves

    def reset(self):
        """resets the entire board to starting point"""
        self.__moves = [[0 for _ in range(self.__height)] for _ in range(self.__width)]
        self.__player1_rows = []
        self.__player2_rows = []
        self.__inspect_moves = set()

    def get_surrounding_free_coordinates(self, position:tuple[int, int]):
        """
        get all the free coordinates that are surrounding the move
        return in 2 layers, 1st layer is inner circle of moves and 2nd layer is outer cirle of moves
        """
        def surrounding_moves(offsets):
            for offset in offsets:
                yield (position[0]+offset[0], position[1]+offset[1])

        offsets = ([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)],
                    [(0, 2), (1, 2), (2, -2), (2, 0), (2, 2), (-2, -2), (-2, 0), (-2, 2), (0, -2)])
        free_coordinates_inner = set()
        free_coordinates_outer = set()
        for surrounding_move in surrounding_moves(offsets[0]):
            if not self.is_outside_of_game_area(surrounding_move):
                if self.is_free_space(surrounding_move):
                    free_coordinates_inner.add(surrounding_move)
        for surrounding_move in surrounding_moves(offsets[1]):
            if not self.is_outside_of_game_area(surrounding_move):
                if self.is_free_space(surrounding_move):
                    free_coordinates_outer.add(surrounding_move)

        return free_coordinates_inner, free_coordinates_outer

    def get_surrounding_moves_of_moves_rows(self, move:tuple[int,int], player: int)->set[tuple[int,int]]:
        """get moves that would build players rows related to the move"""
        rows = self.__get_rows_containing_move(move, player)
        moves = set()
        for row in rows:
            for m in row.surrounding_moves:
                if self.is_free_space(m):
                    moves.add(m)
        return moves
    
    def get_moves_with_high_score_rows(self):
        moves_in_order = []
        for row in self.__player2_rows:
            if row.score >= 50000000:
                for move in row.surrounding_moves:
                    if self.is_free_space(move):
                        moves_in_order.append(move)
        for row in self.__player1_rows:
            if row.score >= 50000000:
                for move in row.surrounding_moves:
                    if self.is_free_space(move):
                        moves_in_order.append(move)
        return moves_in_order

    ############################
    ### Move evaluations #######
    ############################

    def is_move_part_of_winning_row(self, move:tuple[int,int], player: int)->bool:
        """check if move is part of winning row i.e. row that has 5 in a row"""
        rows = self.__get_rows_containing_move(move, player)
        for row in rows:
            if len(row) >= 5:
                return True
        return False

    def evaluate_state(self):
        """sum up the players row potentials so that user rows reduce the score and AI rows increase the score"""
        score = 0
        for row in self.player1_rows:
            score -= row.score
        for row in self.player2_rows:
            score += row.score
        return score
