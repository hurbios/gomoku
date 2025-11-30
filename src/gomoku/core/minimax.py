import time
from gomoku.core.helper import draw
from gomoku.core.game_board import Board
from gomoku.core.config import INSPECT_DEPTH, CUTOFFTIME
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

    def __generate_inspect_moves(self, starting_moves, inspect_moves, current_depth, surrounding_moves):
        if len(starting_moves) > (self.__current_max_depth - current_depth):
            # print(current_depth, starting_moves, starting_moves[self.__current_max_depth - current_depth])
            yield starting_moves[self.__current_max_depth - current_depth]
            for move in surrounding_moves:
                if move is not starting_moves[self.__current_max_depth - current_depth]:
                    yield move
            for move in inspect_moves:
                if move is not starting_moves[self.__current_max_depth - current_depth] or move not in surrounding_moves:
                    yield move
        else:
            yield from surrounding_moves
            for move in inspect_moves:
                if move not in surrounding_moves:
                    yield move

    def minimax(self, last_move:tuple[int,int], depth:int, is_player1:bool, inspect_moves:set, last_moves, alpha, beta, starting_moves):
        last_move_score = self.__board.evaluate_state(get_player(not is_player1), last_move, depth)
        next_moves = last_moves + [last_move]
        time_exceeded = has_time_exceeded(self.__start_time)
        if depth <= 0 or time_exceeded:
            return last_move_score, next_moves, time_exceeded

        if last_move_score >= 100000000 or last_move_score <= -100000000:
            return last_move_score, next_moves, time_exceeded

        low_score = LARGE
        high_score = SMALL
        return_next_moves = []
        surrounding_moves = self.__board.get_surrounding_free_coordinates(last_move, INSPECT_DEPTH)
        for coordinates in self.__generate_inspect_moves(starting_moves, inspect_moves, depth, surrounding_moves):
            # time.sleep(10)
            self.__board.add_move(coordinates, get_player(is_player1))
            new_ispect_moves = inspect_moves.union(surrounding_moves)
            new_ispect_moves.discard(coordinates)
            (
                move_score,
                new_moves,
                time_exceeded
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
            if time_exceeded:
                break
        return low_score if is_player1 else high_score, return_next_moves, time_exceeded

    def minimax_iterative_depth(self, starting_moves:tuple[int,int], last_move):
        move = None
        high_score = SMALL
        time_exceeded = False
        move_score = 0
        return_next_moves = []
        surrounding_moves = self.__board.get_surrounding_free_coordinates(last_move, INSPECT_DEPTH)
        for coordinates in self.__generate_inspect_moves(starting_moves, self.__board.inspect_moves, self.__current_max_depth, surrounding_moves):
            if not move:
                move = coordinates
            self.__board.add_move(coordinates, 2)
            new_ispect_moves = self.__board.inspect_moves.union(surrounding_moves)
            new_ispect_moves.discard(coordinates)
            debug_log(f"{self.__board.inspect_moves} {new_ispect_moves}")
            (
                move_score,
                next_moves,
                time_exceeded
            ) = self.minimax(coordinates, self.__current_max_depth - 1, True, new_ispect_moves, [], SMALL, LARGE, starting_moves)
            draw(self.__board)
            self.__board.remove_move(coordinates, 2)
            if move_score > high_score:
                high_score = move_score
                move = coordinates
                return_next_moves = next_moves
            print(f"{coordinates} score: {move_score}")
            print(next_moves)
            if time_exceeded:
                break
        return move, return_next_moves, time_exceeded

    def get_next_move(self, last_move:tuple[int,int]):
        self.__start_time = time.time()
        self.__current_max_depth = 1
        move = None
        ret_move = None
        time_exceeded = False
        starting_moves = []
        while not time_exceeded and last_move:
            print(f"depth: {self.__current_max_depth}")
            move, starting_moves, time_exceeded = self.minimax_iterative_depth(starting_moves, last_move)
            if not time_exceeded:
                ret_move = move
                if not ret_move:
                    break
            self.__current_max_depth+=1
        return ret_move or (9,9)
