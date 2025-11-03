from gomoku.core.game_board import Board

class Minimax:
    def __init__(self, board: Board):
        self.__board = board

    def get_direction_counts(self, starting_point, player):
        direction_counts = [
            (self.__board.get_vertical_count(starting_point,player), 'vertical'),
            (self.__board.get_horizontal_count(starting_point,player), 'horizontal'),
            (self.__board.get_diagonal_count(starting_point,player), 'diagonal'),
            (self.__board.get_inverse_diagonal_count(starting_point,player),'inverse_diagonal')
        ]
        direction_counts.sort(reverse=True)
        return direction_counts

    # TODO: temp return only direction and count
    def get_next_move(self, last_move: tuple[int, int]):
        # player1 = self.__board.get_player_pieces(1) # User
        # player2 = self.__board.get_player_pieces(2) # AI

        # Check how many pieces user has for each direction
        return self.get_direction_counts(last_move, 1)[0]
        

        

        
