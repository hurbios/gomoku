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

    def __generate_inspect_moves(self, starting_moves, inspect_moves, current_depth, surrounding_moves, row_surrounding_moves):
        """
        Generator to generate next moves to inspect
        First iterate moves that were deemed as best moves in previous iteration,
        Then iterate 2 closest building moves of rows related to the latest move,
        Then iterate moves that are surrounding the latest move first inner layer and then outer layer,
        Lastly iterate through rest of the moves to inspect
        """
        if len(starting_moves) > (self.__current_max_depth - current_depth):
            yield starting_moves[self.__current_max_depth - current_depth]
            for move in row_surrounding_moves:
                if move != row_surrounding_moves[self.__current_max_depth - current_depth]:
                    yield move
            for move in surrounding_moves[0]:
                if (move != starting_moves[self.__current_max_depth - current_depth]) and (move not in row_surrounding_moves):
                    yield move
            for move in surrounding_moves[1]:
                if (move != starting_moves[self.__current_max_depth - current_depth]) and (move not in row_surrounding_moves):
                    yield move
            for move in inspect_moves:
                if ((move != starting_moves[self.__current_max_depth - current_depth]) and
                    (move not in surrounding_moves) and
                    (move not in row_surrounding_moves)):
                    yield move
        else:
            yield from row_surrounding_moves
            for move in surrounding_moves[0]:
                if move not in row_surrounding_moves:
                    yield move
            for move in surrounding_moves[1]:
                if move not in row_surrounding_moves:
                    yield move
            for move in inspect_moves:
                if ((move not in surrounding_moves) and
                    (move not in row_surrounding_moves)):
                    yield move

    def minimax(self, last_move:tuple[int,int], depth:int, is_player1:bool, inspect_moves:set, last_moves, alpha, beta, starting_moves):
        next_moves = last_moves + [last_move] if depth != self.__current_max_depth else []
        self.__time_exceeded = self.has_time_exceeded()

        if self.__board.is_move_part_of_winning_row(last_move, get_player(not is_player1)):
            return float('-inf') if not is_player1 else float('inf'), next_moves

        if depth <= 0 or self.__time_exceeded:
            last_move_score = self.__board.evaluate_state()
            return last_move_score, next_moves

        low_score = LARGE
        high_score = SMALL
        return_next_moves = []
        surrounding_moves = self.__board.get_surrounding_free_coordinates(last_move)
        row_surrounding_moves = self.__board.get_surrounding_moves_of_moves_rows(last_move, get_player(not is_player1))
        new_ispect_moves = inspect_moves.union(surrounding_moves[0].union(surrounding_moves[1]))
        for coordinates in self.__generate_inspect_moves(starting_moves, inspect_moves, depth, surrounding_moves, row_surrounding_moves):
            self.__board.add_move(coordinates, get_player(is_player1))
            new_ispect_moves.discard(coordinates)
            (
                move_score,
                new_moves
            ) = self.minimax(coordinates, depth-1, not is_player1, new_ispect_moves, next_moves, alpha, beta, starting_moves)
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
        starting_moves = []
        biggest = SMALL
        new_ispect_moves = self.__board.inspect_moves
        while not self.__time_exceeded and last_move:
            debug_log(f"-------- depth: {self.__current_max_depth} --------")
            score, starting_moves = self.minimax(last_move, self.__current_max_depth, False, new_ispect_moves, [], SMALL, LARGE, starting_moves)
            if not self.__time_exceeded:
                if (score > biggest) and (len(starting_moves) > 0):
                    score = max(score, biggest)
                    move = starting_moves[0]
                if score == float('inf'):
                    break
            self.__current_max_depth+=1
        return move or (9,9)
