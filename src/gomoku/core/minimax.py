from gomoku.core.game_board import Board

PLAYER = {
    'USER': 1,
    'AI': 2
}
MAX_DEPTH = 1

class Minimax:
    def __init__(self, board: Board):
        self.__board = board

    def get_direction_counts(self, starting_point, player):
        direction_counts = [
            (self.__board.get_direction_count(starting_point,player,'vertical'), 'vertical'),
            (self.__board.get_direction_count(starting_point,player,'horizontal'), 'horizontal'),
            (self.__board.get_direction_count(starting_point,player,'diagonal'), 'diagonal'),
            (self.__board.get_direction_count(starting_point,player,'inverse_diagonal'),'inverse_diagonal')
        ]
        direction_counts.sort(reverse=True)
        return direction_counts

    # TODO: temp return only direction and count, fix later
    def _get_next_move(self, last_move: tuple[int, int]):
        # player1 = self.__board.get_player_pieces(1) # User
        # player2 = self.__board.get_player_pieces(2) # AI

        # Check how many pieces user has for each direction
        directions = self.get_direction_counts(last_move, PLAYER['USER'])
        all_tuples = [self.__board.get_next_free_coordinates(last_move, PLAYER['USER'], direction[1]) for direction in directions]
        flattened = [x for tup in all_tuples for x in tup if x is not None]
        return next(iter(flattened)) if len(flattened) > 0 else None

    # def get_next_move(self, last_move: tuple[int, int]):
    #     high_score = -100
    #     move = last_move
    #     # print(self.__board.get_surrounding_free_coordinates(last_move))
    #     for coordinates in self.__board.get_surrounding_free_coordinates(last_move,6):
    #         move_score = self.__board.evaluate_move(coordinates)
    #         if move_score > high_score:
    #             high_score = move_score
    #             move = coordinates
    #     # print(move)
    #     return move
    
    # def __get_next_move(self, last_move: tuple[int, int], depth=1, isPlayer1=False):
    #     curr_move_score = self.__board.evaluate_move(last_move)
    #     if depth <= 0 or curr_move_score in [15, 10]:
    #         return last_move, curr_move_score
    #     high_score = -100
    #     low_score = 100
    #     move = last_move
    #     # print(self.__board.get_surrounding_free_coordinates(last_move))
    #     for coordinates in self.__board.get_surrounding_free_coordinates(last_move,2):
    #         self.__board.add_temp_move(coordinates, 1 if isPlayer1 else 2)
    #         _move, move_score = self.get_next_move(coordinates, depth-1, not isPlayer1)
    #         self.__board.remove_temp_move(coordinates, 1 if isPlayer1 else 2)
    #         if isPlayer1:
    #             if move_score < low_score:
    #                 low_score = move_score
    #                 move = coordinates
    #         else:
    #             # print(move_score, high_score)
    #             if move_score > high_score:
    #                 high_score = move_score
    #                 move = coordinates
    #                 if move_score in [15, 10]:
    #                     break
    #     print('-' * depth, isPlayer1, move, low_score if isPlayer1 else high_score)
    #     return move, low_score if isPlayer1 else high_score
    
    
    def get_next_move(self, last_move, depth=MAX_DEPTH, player=2):
        last_move_score = self.__board.evaluate_move(last_move)
        WIN_SCORES = {
            "PLAYER1": [-7, -5],
            "PLAYER2": [8, 5]
        }
        if depth <= 0 or (last_move_score in WIN_SCORES["PLAYER2"] and player == 1) or (last_move_score in WIN_SCORES["PLAYER1"] and player == 2):
            return last_move, last_move_score, [last_move]
        if depth < MAX_DEPTH:
            self.__board.add_temp_move(last_move, 2 if player==1 else 1)
        moves = []
        move=last_move
        if player == 1:
            low_score = 100
            for coordinates in self.__board.get_surrounding_free_coordinates(last_move, 2):
                # self.__board.add_temp_move(coordinates, 1)
                _move, move_score, moves_inner = self.get_next_move(coordinates, depth-1, 2)
                # self.__board.remove_temp_move(coordinates, 1)
                if move_score < low_score:
                    low_score = move_score
                    move = coordinates
                    moves=moves_inner
                    moves.append(coordinates)
                    # if move_score in  WIN_SCORES["PLAYER1"]:
                    #     break
        else:
            high_score = -100
            for coordinates in self.__board.get_surrounding_free_coordinates(last_move, 2):
                # self.__board.add_temp_move(coordinates, 2)
                _move, move_score, moves_inner = self.get_next_move(coordinates, depth-1, 1)
                # self.__board.remove_temp_move(coordinates, 2)
                print(coordinates, move_score, high_score, "curr score = ", self.__board.evaluate_move(coordinates), "player1: ", self.__board.get_player_pieces(1), "player2",self.__board.get_player_pieces(2))
                if move_score > high_score:
                    high_score = move_score
                    move = coordinates
                    moves=moves_inner
                    moves.append(coordinates)
                    # if move_score in  WIN_SCORES["PLAYER2"]:
                    #     break
        # if(depth >= 2):
        if(move_score >= 1):
            print("-"*depth, move, move_score, player)
        if(depth >= 3):
            print(moves)
        if depth < MAX_DEPTH:
            self.__board.remove_temp_move(last_move, 2 if player==1 else 1)
        return move, move_score, moves
