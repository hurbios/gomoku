from gomoku.core.game_board import Board

PLAYER = {
    'USER': 1,
    'AI': 2
}
MAX_DEPTH = 1
MOVE_RANGE = 2

class Minimax:
    def __init__(self, board: Board):
        self.__board = board

    def minimax(self, last_move, depth, player):
        last_move_score = self.__board.evaluate_state_after_move(last_move)
        WIN_SCORES = {
            "PLAYER1": [-7, -5],
            "PLAYER2": [8, 5]
        }
        if depth <= 0 or (last_move_score in WIN_SCORES["PLAYER2"] and player == 1) or (last_move_score in WIN_SCORES["PLAYER1"] and player == 2):
            return last_move_score, [last_move]
        moves = []
        if player == 1:
            low_score = 100
            for coordinates in self.__board.get_surrounding_free_coordinates(last_move, MOVE_RANGE):
                self.__board.add_move(coordinates,1)
                move_score, moves_inner = self.minimax(coordinates, depth-1, 2)
                self.__board.remove_move(coordinates,1)
                if move_score < low_score:
                    low_score = move_score
                    moves=moves_inner
                    moves.append(coordinates)

        else:
            high_score = -100
            for coordinates in self.__board.get_surrounding_free_coordinates(last_move, MOVE_RANGE):
                self.__board.add_move(coordinates,2)
                move_score, moves_inner = self.minimax(coordinates, depth-1, 1)
                self.__board.remove_move(coordinates,2)
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
        # for coordinates in self.__board.get_surrounding_free_coordinates(last_move, MOVE_RANGE):
        for coordinates in [(2,2),(3,2),(4,2)]:
            self.__board.add_move(coordinates,2)
            print(coordinates, self.__board.get_player_move_result(coordinates,2), self.__board.evaluate_state_after_move(coordinates))
            move_score, moves_inner = self.minimax(coordinates, MAX_DEPTH - 1, 1)
            self.__board.remove_move(coordinates,2)
            # print(coordinates, move_score, high_score, "curr score = ", self.__board.evaluate_state_after_move(coordinates), "player1: ", self.__board.get_player_pieces(1), "player2",self.__board.get_player_pieces(2))
            if move_score > high_score:
                high_score = move_score
                move = coordinates
                moves=moves_inner
                moves.append(coordinates)
        print("final: ", move, move_score, moves)
        return move
