import time
from gomoku.core.helper import draw
from gomoku.core.game_board import Board
from gomoku.core.config import INSPECT_DEPTH, MAX_DEPTH, DEBUG

WINNING_SCORES = {
    'player1': {-8,-6},
    'player2': {8,5}
}

def get_player(is_player1:int)->int:
    return 1 if is_player1 else 2

class Minimax:
    def __init__(self, board:Board):
        self.__board = board

    def minimax(self, last_move:tuple[int,int], depth:int, is_player1:bool, inspect_moves:set):
        last_move_score = self.__board.evaluate_state_after_move(last_move)

        if depth <= 0:
            return last_move_score
            # return last_move_score, [last_move]

        if ((not is_player1 and last_move_score == WINNING_SCORES["player1"]) 
            or (is_player1 and last_move_score == WINNING_SCORES["player2"])):
            return last_move_score
        # moves = []

        low_score = 100
        high_score = -100
        for coordinates in inspect_moves:
            self.__board.add_move(coordinates, get_player(is_player1))
            new_ispect_moves = self.__board.get_surrounding_free_coordinates(last_move, INSPECT_DEPTH)
            move_score = self.minimax(coordinates, depth-1, not is_player1, inspect_moves.union(new_ispect_moves))
            # move_score, moves_inner = self.minimax(coordinates, depth-1, not is_player1, inspect_moves.union(new_ispect_moves))
            self.__board.remove_move(coordinates, get_player(is_player1))
            if is_player1:
                if move_score < low_score:
                    low_score = move_score
                    # moves=moves_inner
                    # moves.append(coordinates)
            else:
                if move_score > high_score:
                    high_score = move_score
                    # moves=moves_inner
                    # moves.append(coordinates)
        # if(move_score >= 1):
        #     print("-"*depth, move_score, player)
        return move_score
        # return move_score, moves

    def get_next_move(self, last_move:tuple[int,int]):
        moves = []
        high_score = -100
        
        # for coordinates in [(2,2),(3,2),(4,2)]:
        for coordinates in self.__board.inspect_moves:
            self.__board.add_move(coordinates, 2)
            # print(coordinates, self.__board.get_player_move_result(coordinates,2), self.__board.evaluate_state_after_move(coordinates), flush=True)
            new_ispect_moves = self.__board.get_surrounding_free_coordinates(coordinates, INSPECT_DEPTH)
            DEBUG and print(self.__board.inspect_moves, new_ispect_moves)
            # time.sleep(5)
            move_score = self.minimax(coordinates, MAX_DEPTH - 1, True, self.__board.inspect_moves.union(new_ispect_moves))
            # move_score, moves_inner = self.minimax(coordinates, MAX_DEPTH - 1, True, self.__board.inspect_moves.union(new_ispect_moves))
            DEBUG and draw(self.__board)
            self.__board.remove_move(coordinates, 2)
            # print(coordinates, move_score, high_score, "curr score = ", self.__board.evaluate_state_after_move(coordinates), "player1: ", self.__board.get_player_pieces(1), "player2",self.__board.get_player_pieces(2))
            if move_score > high_score:
                high_score = move_score
                move = coordinates
                # moves=moves_inner
            DEBUG and print("player1: ", self.__board.get_player_pieces(1), flush=True)
            DEBUG and print("player2: ", self.__board.get_player_pieces(2), flush=True)
            
        DEBUG and print("final: ", move, move_score, moves, "====================================", flush=True)
        DEBUG and print("player1: ", self.__board.get_player_pieces(1), flush=True)
        DEBUG and print("player2: ", self.__board.get_player_pieces(2), flush=True)
        return move
