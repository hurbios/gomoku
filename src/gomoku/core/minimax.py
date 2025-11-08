from gomoku.core.game_board import Board

PLAYER = {
    'USER': 1,
    'AI': 2
}

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

    # temp return only direction and count, fix later
    def get_next_move(self, last_move: tuple[int, int]):
        # player1 = self.__board.get_player_pieces(1) # User
        # player2 = self.__board.get_player_pieces(2) # AI

        # Check how many pieces user has for each direction
        directions = self.get_direction_counts(last_move, PLAYER['USER'])
        all_tuples = [self.__board.get_next_free_coordinates(last_move, PLAYER['USER'], direction[1]) for direction in directions]
        flattened = [x for tup in all_tuples for x in tup if x is not None]
        return next(iter(flattened)) if len(flattened) > 0 else None
