class Board:
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__moves = [[0 for _ in range(height)] for _ in range(width)]
        self.__player1_pieces = []
        self.__player2_pieces = []


    def size(self):
        return len(self.__moves), len(self.__moves[0])

    def __count_pieces_direction(self, count:int, position:tuple[int, int], player:int, direction:tuple[int, int]):
        if count >= 5:
            return 5
        if any(iter([(self.__width <= (position[0]+direction[0])),
            ((position[0]+direction[0]) < 0),
            self.__height <= (position[1]+direction[1]),
            ((position[1]+direction[1]) < 0)])):
            return count
        if self.__moves[position[0]+direction[0]][position[1]+direction[1]] is not player:
            return count
        return self.__count_pieces_direction(count+1,(position[0]+direction[0], position[1]+direction[1]),player,direction)

    def get_vertical_count(self, position:tuple[int, int], player:int):
        return 1 + (self.__count_pieces_direction(0,position,player,(1,0)) + self.__count_pieces_direction(0,position,player,(-1,0)))

    def get_horizontal_count(self, position:tuple[int, int], player:int):
        return 1 + (self.__count_pieces_direction(0,position,player,(0,1)) + self.__count_pieces_direction(0,position,player,(0,-1)))

    def get_inverse_diagonal_count(self, position:tuple[int, int], player:int):
        return 1 + (self.__count_pieces_direction(0,position,player,(1,-1)) + self.__count_pieces_direction(0,position,player,(-1,1)))

    def get_diagonal_count(self, position:tuple[int, int], player:int):
        return 1 + (self.__count_pieces_direction(0,position,player,(-1,-1)) + self.__count_pieces_direction(0,position,player,(1,1)))

    def __player_wins(self, move: tuple[int, int], player:int):
        max_in_row = max(
            self.get_vertical_count(move,player),           # - direction
            self.get_horizontal_count(move,player),         # | direction
            self.get_diagonal_count(move,player),           # / direction
            self.get_inverse_diagonal_count(move,player)    # \ direction
        )
        return max_in_row >=5

    # Returns tuple: (True if player piece was added, True if player wins)
    def add_move(self, move: tuple[int, int], player:int):
        # Check that the move is within the game area boundaries
        if any(iter([
                (self.__width < move[0]),
                (move[0] < 0),
                (self.__width < move[1]),
                (move[1] < 0),
                (self.__height < move[0]),
                (move[0] < 0),
                (self.__height < move[1]),
                (move[1] < 0)
              ])):
            return False, False

        # Check that no piece exists yet in the move coordinates
        if self.__moves[move[0]][move[1]]:
            return False, False
        # Check that the player is valid
        if player not in [1,2]:
            return False, False

        # Add move to players pieces and on game board
        self.__moves[move[0]][move[1]] = player
        if player == 1:
            self.__player1_pieces.append(move)
        else:
            self.__player2_pieces.append(move)

        return True, self.__player_wins(move, player)

    def get_player_pieces(self, player):
        return self.__player1_pieces if player == 1 else self.__player2_pieces

    def reset(self):
        self.__moves = [[0 for _ in range(self.__height)] for _ in range(self.__width)]
        self.__player1_pieces = []
        self.__player2_pieces = []
