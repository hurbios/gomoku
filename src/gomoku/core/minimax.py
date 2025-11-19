import time
from gomoku.core.helper import draw
from gomoku.core.game_board import Board

MAX_DEPTH = 1
MOVE_RANGE = 1

def get_player(is_player1:int)->int:
    return 1 if is_player1 else 2

class Minimax:
    def __init__(self, board: Board):
        self.__board = board

    def minimax(self, last_move, depth, is_player1):
        last_move_score = self.__board.evaluate_state_after_move(last_move)

        if depth <= 0:
            return last_move_score, [last_move]
        moves = []

        low_score = 100
        high_score = -100
        for coordinates in self.__board.get_surrounding_free_coordinates(last_move, MOVE_RANGE):
            self.__board.add_move(coordinates, get_player(is_player1))
            move_score, moves_inner = self.minimax(coordinates, depth-1, not is_player1)
            self.__board.remove_move(coordinates, get_player(is_player1))
            if is_player1:
                if move_score < low_score:
                    low_score = move_score
                    moves=moves_inner
                    moves.append(coordinates)
            else:
                if move_score > high_score:
                    high_score = move_score
                    moves=moves_inner
                    moves.append(coordinates)
        # if(move_score >= 1):
        #     print("-"*depth, move_score, player)
        return move_score, moves

    def get_next_move(self, last_move):
        moves = []
        high_score = -100
        # for coordinates in [(2,2),(3,2),(4,2)]:
        for coordinates in self.__board.get_surrounding_free_coordinates(last_move, MOVE_RANGE):
            self.__board.add_move(coordinates,2)
            # print(coordinates, self.__board.get_player_move_result(coordinates,2), self.__board.evaluate_state_after_move(coordinates), flush=True)
            move_score, moves_inner = self.minimax(coordinates, MAX_DEPTH - 1, 1)
            draw(self.__board)
            self.__board.remove_move(coordinates,2)
            # print(coordinates, move_score, high_score, "curr score = ", self.__board.evaluate_state_after_move(coordinates), "player1: ", self.__board.get_player_pieces(1), "player2",self.__board.get_player_pieces(2))
            if move_score > high_score:
                high_score = move_score
                move = coordinates
                moves=moves_inner
            print("player1: ", self.__board.get_player_pieces(1), flush=True)
            print("player2: ", self.__board.get_player_pieces(2), flush=True)
            
        print("final: ", move, move_score, moves, "====================================", flush=True)
        print("player1: ", self.__board.get_player_pieces(1), flush=True)
        print("player2: ", self.__board.get_player_pieces(2), flush=True)
        return move
