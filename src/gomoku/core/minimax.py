import time
from gomoku.core.helper import draw
from gomoku.core.game_board import Board
from gomoku.core.config import CUTOFFTIME
from gomoku.core.helper import debug_log

SMALL = float('-inf')
LARGE = float('inf')

def has_time_exceeded(start_time):
    current_time = time.time()
    if CUTOFFTIME <= (current_time - start_time):
        print(CUTOFFTIME, current_time - start_time)
        return True
    return False


def get_player(is_player1:int)->int:
    return 1 if is_player1 else 2

class Minimax:
    def __init__(self, board:Board):
        self.__board = board
        self.__start_time = time.time()
        self.__current_max_depth = 1
        self.__time_exceeded = False

    def __generate_inspect_moves(self, starting_moves, inspect_moves, current_depth, surrounding_moves, row_surrounding_moves):
        """
        Generator to generate next moves to inspect
        First iterate moves that were deemed as best moves in previous iteration,
        Then iterate 2 closest building moves of rows related to the latest move,
        Then iterate moves that are surrounding the latest move first inner layer and then outer layer,
        Lastly iterate through rest of the moves to inspect
        """
        if len(starting_moves) > (self.__current_max_depth - current_depth):
            # print(current_depth, starting_moves, starting_moves[self.__current_max_depth - current_depth])
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
                if  move not in row_surrounding_moves:
                    yield move
            for move in surrounding_moves[1]:
                if  move not in row_surrounding_moves:
                    yield move
            for move in inspect_moves:
                if ((move not in surrounding_moves) and
                    (move not in row_surrounding_moves)):
                    yield move

    def minimax(self, last_move:tuple[int,int], depth:int, is_player1:bool, inspect_moves:set, last_moves, alpha, beta, starting_moves):
        next_moves = last_moves + [last_move]
        self.__time_exceeded = has_time_exceeded(self.__start_time)

        if self.__board.is_move_part_of_winning_row(last_move, get_player(not is_player1)):
            return float('-inf') if not is_player1 else float('inf'), next_moves
        
        if depth <= 0 or self.__time_exceeded:
            last_move_score = self.__board.evaluate_state(get_player(not is_player1), last_move, depth)
            return last_move_score, next_moves

        low_score = LARGE
        high_score = SMALL
        return_next_moves = []
        surrounding_moves = self.__board.get_surrounding_free_coordinates(last_move)
        row_surrounding_moves = self.__board.get_surrounding_moves_of_moves_rows(last_move, get_player(not is_player1))
        for coordinates in self.__generate_inspect_moves(starting_moves, inspect_moves, depth, surrounding_moves, row_surrounding_moves):
            # time.sleep(10)
            _, player_wins = self.__board.add_move(coordinates, get_player(is_player1))
            new_ispect_moves = inspect_moves.union(surrounding_moves[0].union(surrounding_moves[1]))
            new_ispect_moves.discard(coordinates)
            (
                move_score,
                new_moves
            ) = self.minimax(coordinates, depth-1, not is_player1, new_ispect_moves, next_moves, alpha, beta, starting_moves)
            self.__board.remove_move(coordinates, get_player(is_player1))
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

    def minimax_iterative_depth(self, starting_moves:tuple[int,int], last_move):
        move = None
        high_score = SMALL
        move_score = 0
        return_next_moves = []
        surrounding_moves = self.__board.get_surrounding_free_coordinates(last_move)
        row_surrounding_moves = self.__board.get_surrounding_moves_of_moves_rows(last_move, get_player(True))
        for coordinates in self.__generate_inspect_moves(starting_moves, self.__board.inspect_moves, self.__current_max_depth, surrounding_moves, row_surrounding_moves):
            if not move:
                move = coordinates
            _, player_wins = self.__board.add_move(coordinates, 2)
            new_ispect_moves = self.__board.inspect_moves.union(surrounding_moves[0].union(surrounding_moves[1]))
            new_ispect_moves.discard(coordinates)
            debug_log(f"{self.__board.inspect_moves} {new_ispect_moves}")
            (
                move_score,
                next_moves
            ) = self.minimax(coordinates, self.__current_max_depth - 1, True, new_ispect_moves, [], SMALL, LARGE, starting_moves)
            draw(self.__board)
            self.__board.remove_move(coordinates, 2)
            if move_score > high_score:
                high_score = move_score
                move = coordinates
                return_next_moves = next_moves
            print(f"{coordinates} score: {move_score}")
            print(next_moves)
            if self.__time_exceeded or move == float('inf'):
                break
        return move, return_next_moves, high_score

    def get_next_move(self, last_move:tuple[int,int]):
        self.__start_time = time.time()
        self.__current_max_depth = 1
        move = None
        move_before_timeout = None
        self.__time_exceeded = False
        starting_moves = []
        while not self.__time_exceeded and last_move:
            print(f"depth: {self.__current_max_depth}")
            move, starting_moves, score = self.minimax_iterative_depth(starting_moves, last_move)
            if not self.__time_exceeded:
                move_before_timeout = move
                if not move_before_timeout or score == float('inf'):
                    break
            self.__current_max_depth+=1
        return move_before_timeout or (9,9)
