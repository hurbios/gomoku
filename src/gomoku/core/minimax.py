import time
import os
from gomoku.core.game_board import Board
from gomoku.core.config import CUTOFFTIME
from gomoku.core.helper import debug_log

SMALL = float('-inf')
LARGE = float('inf')
ITER_DEPTH = os.environ.get('ITER_DEPTH')

def get_player(is_player1:int)->int:
    return 1 if is_player1 else 2

class Minimax:
    def __init__(self, board:Board):
        self.__board = board
        self.__start_time = time.time()
        self.__current_max_depth = 1
        self.__time_exceeded = False
        self.starting_moves = []

    def has_time_exceeded(self):
        if self.__time_exceeded:
            return True
        current_time = time.time()
        time_spent = current_time - self.__start_time
        if ITER_DEPTH:
            if self.__current_max_depth > int(ITER_DEPTH):
                debug_log(f"Cutoff with depth {self.__current_max_depth}, time spent: {time_spent}")
                return True
        else:
            if CUTOFFTIME <= time_spent:
                debug_log(f"Cutoff time: {CUTOFFTIME}, actual time spent: {time_spent}")
                return True
        return False

    def __generate_inspect_moves(self, inspect_moves, current_depth, surrounding_moves, row_surrounding_moves):
        """
        Generator to generate next moves to inspect
        First iterate moves that were deemed as best moves in previous iteration,
        Then iterate building moves of highest potential rows,
        Then iterate moves that are surrounding the latest move first inner layer and then outer layer,
        Lastly iterate through rest of the moves to inspect
        """
        def filter_starting_moves(self, move):
            return move != self.starting_moves[self.__current_max_depth - current_depth]

        def filter_row_surrounding_moves(_, move):
            return move not in row_surrounding_moves

        def filter_surrounding_moves(_, move):
            return move not in surrounding_moves[0] and move not in surrounding_moves[1]

        conditions = []
        if len(self.starting_moves) > (self.__current_max_depth - current_depth):
            conditions.append(filter_starting_moves)
            yield self.starting_moves[self.__current_max_depth - current_depth]
        for move in row_surrounding_moves:
            if all(condition(self, move) for condition in conditions):
                yield move
        conditions.append(filter_row_surrounding_moves)
        for move in surrounding_moves[0]:
            if all(condition(self,move) for condition in conditions):
                yield move
        for move in surrounding_moves[1]:
            if all(condition(self,move) for condition in conditions):
                yield move
        conditions.append(filter_surrounding_moves)
        for move in inspect_moves:
            if all(condition(self,move) for condition in conditions):
                yield move

    def minimax(
            self,
            last_move:tuple[int,int],
            depth:int,
            is_player1:bool,
            inspect_moves:set,
            last_moves:list[tuple[int,int]],
            alpha:int|float,
            beta:int|float):

        current_last_moves = last_moves + [last_move] if depth != self.__current_max_depth else []
        self.__time_exceeded = self.has_time_exceeded()

        if self.__board.is_move_part_of_winning_row(last_move, get_player(not is_player1)):
            return float('-inf') if not is_player1 else float('inf'), current_last_moves

        if depth <= 0 or self.__time_exceeded:
            last_move_score = self.__board.evaluate_state()
            return last_move_score, current_last_moves

        low_score = LARGE
        high_score = SMALL
        return_next_moves = []
        surrounding_moves = self.__board.get_surrounding_free_coordinates(last_move)
        # row_surrounding_moves = self.__board.get_surrounding_moves_of_moves_rows(last_move, get_player(not is_player1))
        row_surrounding_moves = self.__board.get_moves_with_high_score_rows()
        new_ispect_moves = inspect_moves.union(surrounding_moves[0].union(surrounding_moves[1]))
        for coordinates in self.__generate_inspect_moves(inspect_moves, depth, surrounding_moves, row_surrounding_moves):
            self.__board.add_move(coordinates, get_player(is_player1))
            new_ispect_moves.discard(coordinates)
            (move_score,new_moves) = self.minimax(
                last_move=coordinates,
                depth=depth-1,
                is_player1=not is_player1,
                inspect_moves=new_ispect_moves,
                last_moves=current_last_moves,
                alpha=alpha,
                beta=beta,
            )
            self.__board.remove_move(coordinates, get_player(is_player1))
            new_ispect_moves.add(coordinates)
            if depth == self.__current_max_depth:
                debug_log(f"{coordinates} score: {move_score}, moves: {return_next_moves}")
            if is_player1:
                if move_score < low_score:
                    return_next_moves = new_moves
                low_score = min(low_score, move_score)
                beta = min(move_score, beta)
                if beta <= alpha:
                    break
            else:
                if move_score > high_score:
                    return_next_moves = new_moves
                high_score = max(high_score, move_score)
                alpha = max(move_score, alpha)
                if beta <= alpha:
                    break
            if self.__time_exceeded:
                break
        return low_score if is_player1 else high_score, return_next_moves

    def get_next_move(self, last_move:tuple[int,int]):
        self.__start_time = time.time()
        self.__current_max_depth = 1
        move = None
        self.__time_exceeded = False
        self.starting_moves = []
        biggest = SMALL
        new_ispect_moves = self.__board.inspect_moves
        while not self.__time_exceeded and last_move:
            debug_log(f"-------- depth: {self.__current_max_depth} --------")
            score, moves = self.minimax(
                last_move=last_move,
                depth=self.__current_max_depth,
                is_player1=False,
                inspect_moves=new_ispect_moves,
                last_moves=[],
                alpha=SMALL,
                beta=LARGE,
            )
            if not self.__time_exceeded:
                if (score > biggest) and (len(moves) > 0):
                    score = max(score, biggest)
                    move = moves[0]
                    self.starting_moves = moves
                if score == float('inf'):
                    break
            self.__current_max_depth+=1
        return move or (9,9)
