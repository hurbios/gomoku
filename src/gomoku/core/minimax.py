import time
from gomoku.core.helper import draw
from gomoku.core.game_board import Board
from gomoku.core.config import INSPECT_DEPTH, MAX_DEPTH
from gomoku.core.helper import debug_log

SMALL = -10000000
LARGE = 10000000

def get_player(is_player1:int)->int:
    return 1 if is_player1 else 2

class Minimax:
    def __init__(self, board:Board):
        self.__board = board

    def minimax(self, last_move:tuple[int,int], depth:int, is_player1:bool, inspect_moves:set, last_moves, alpha, beta):
        last_move_score = self.__board.evaluate_state(get_player(not is_player1), last_move, depth)
        next_moves = last_moves + [last_move]
        if depth <= 0:
            # print('----')
            # print(inspect_moves)
            # print (next_moves, ' - ', last_move_score)
            return last_move_score, next_moves

        if last_move_score >= 10000000 or last_move_score <= -10000000:
            return last_move_score, next_moves

        low_score = LARGE
        high_score = SMALL
        ret_moves = []
        for coordinates in inspect_moves:
            self.__board.add_move(coordinates, get_player(is_player1))
            new_ispect_moves = self.__board.get_surrounding_free_coordinates(last_move, INSPECT_DEPTH)
            new_ispect_moves = new_ispect_moves.union(new_ispect_moves)
            new_ispect_moves.discard(coordinates)
            move_score, asdf_moves = self.minimax(coordinates, depth-1, not is_player1, new_ispect_moves, next_moves, alpha, beta)
            self.__board.remove_move(coordinates, get_player(is_player1))
            if is_player1:
                if move_score < low_score:
                    ret_moves = asdf_moves
                low_score = min(low_score, move_score)
                beta = min(move_score, beta)
                if beta <= alpha:
                    break
            else:
                if move_score > high_score:
                    ret_moves = asdf_moves
                high_score = max(high_score, move_score)
                alpha = max(move_score, alpha)
                if beta <= alpha:
                    break
        return low_score if is_player1 else high_score, ret_moves

    def get_next_move(self, last_move:tuple[int,int]):
        moves = []
        high_score = SMALL

        move_score = 0
        move = last_move
        for coordinates in self.__board.inspect_moves:
            self.__board.add_move(coordinates, 2)
            new_ispect_moves = self.__board.get_surrounding_free_coordinates(coordinates, INSPECT_DEPTH)
            new_ispect_moves = self.__board.inspect_moves.union(new_ispect_moves)
            new_ispect_moves.discard(coordinates)
            debug_log(f"{self.__board.inspect_moves} {new_ispect_moves}")
            move_score, next_moves = self.minimax(coordinates, MAX_DEPTH - 1, True, new_ispect_moves, [], SMALL, LARGE )
            # time.sleep(5)
            draw(self.__board)
            self.__board.remove_move(coordinates, 2)
            if move_score > high_score:
                high_score = move_score
                move = coordinates
            print(f"{coordinates} score: {move_score}")
            print(next_moves)
            debug_log(f"player1: {self.__board.get_player_pieces(1)}")
            debug_log(f"player2: {self.__board.get_player_pieces(2)}")

        debug_log(f"final: {move} {move_score} {moves} ====================================")
        debug_log(f"player1: {self.__board.get_player_pieces(1)}")
        debug_log(f"player2: {self.__board.get_player_pieces(2)}")
        return move
