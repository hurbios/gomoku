# import time
from gomoku.core.helper import draw
from gomoku.core.game_board import Board
from gomoku.core.config import INSPECT_DEPTH, MAX_DEPTH
from gomoku.core.helper import debug_log


def get_player(is_player1:int)->int:
    return 1 if is_player1 else 2

class Minimax:
    def __init__(self, board:Board):
        self.__board = board

    def minimax(self, last_move:tuple[int,int], depth:int, is_player1:bool, inspect_moves:set):
        last_move_score = self.__board.evaluate_state(get_player(not is_player1), last_move, depth)

        if depth <= 0:
            return last_move_score

        if last_move_score >= 10000 or last_move_score <= -10000:
            return last_move_score

        low_score = 1000000
        high_score = -1000000
        for coordinates in inspect_moves:
            self.__board.add_move(coordinates, get_player(is_player1))
            new_ispect_moves = self.__board.get_surrounding_free_coordinates(last_move, INSPECT_DEPTH)
            move_score = self.minimax(coordinates, depth-1, not is_player1, inspect_moves.union(new_ispect_moves))
            self.__board.remove_move(coordinates, get_player(is_player1))
            if is_player1:
                low_score = min(low_score, move_score)
            else:
                high_score = max(high_score, move_score)
        return low_score if is_player1 else high_score

    def get_next_move(self, last_move:tuple[int,int]):
        moves = []
        high_score = -1000000

        move_score = 0
        move = last_move
        for coordinates in self.__board.inspect_moves:
            self.__board.add_move(coordinates, 2)
            new_ispect_moves = self.__board.get_surrounding_free_coordinates(coordinates, INSPECT_DEPTH)
            debug_log(f"{self.__board.inspect_moves} {new_ispect_moves}")
            # time.sleep(5)
            move_score = self.minimax(coordinates, MAX_DEPTH - 1, True, self.__board.inspect_moves.union(new_ispect_moves))
            draw(self.__board)
            self.__board.remove_move(coordinates, 2)
            if move_score > high_score:
                high_score = move_score
                move = coordinates
            print(f"{coordinates} score: {move_score}")
            debug_log(f"player1: {self.__board.get_player_pieces(1)}")
            debug_log(f"player2: {self.__board.get_player_pieces(2)}")

        debug_log(f"final: {move} {move_score} {moves} ====================================")
        debug_log(f"player1: {self.__board.get_player_pieces(1)}")
        debug_log(f"player2: {self.__board.get_player_pieces(2)}")
        return move
