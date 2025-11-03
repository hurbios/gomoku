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
        # return if already win amount
        if count >= 5:
            return 5
        # check map boundaries
        if any(iter([(self.__width <= (position[0]+direction[0])),
            ((position[0]+direction[0]) < 0),
            self.__height <= (position[1]+direction[1]),
            ((position[1]+direction[1]) < 0)])):
            return count
        # check if current position is the players piece
        if self.__moves[position[0]+direction[0]][position[1]+direction[1]] is not player:
            return count
        # recursion
        return self.__count_pieces_direction(count+1,(position[0]+direction[0], position[1]+direction[1]),player,direction)


    def get_direction_count(self, position:tuple[int, int], player:int, direction:str):
        match direction:
            case 'vertical':
                return 1 + (self.__count_pieces_direction(0,position,player,(1,0)) + self.__count_pieces_direction(0,position,player,(-1,0)))
            case 'horizontal':
                return 1 + (self.__count_pieces_direction(0,position,player,(0,1)) + self.__count_pieces_direction(0,position,player,(0,-1)))
            case 'inverse_diagonal':
                return 1 + (self.__count_pieces_direction(0,position,player,(1,-1)) + self.__count_pieces_direction(0,position,player,(-1,1)))
            case 'diagonal':
                return 1 + (self.__count_pieces_direction(0,position,player,(-1,-1)) + self.__count_pieces_direction(0,position,player,(1,1)))

    def __player_wins(self, move: tuple[int, int], player:int):
        max_in_row = max(
            self.get_direction_count(move,player,'vertical'),           # - direction
            self.get_direction_count(move,player,'horizontal'),         # | direction
            self.get_direction_count(move,player,'diagonal'),           # / direction
            self.get_direction_count(move,player,'inverse_diagonal')    # \ direction
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

    # returns 2 coordinates. Bot sides of the line if empty space exists
    def __get_next_coordinate(self, position:tuple[int, int], player:int, direction:tuple[int, int]):
        # check map boundaries
        if any(iter([(self.__width <= (position[0]+direction[0])),
            ((position[0]+direction[0]) < 0),
            self.__height <= (position[1]+direction[1]),
            ((position[1]+direction[1]) < 0)])):
            return None
        # check if current position is the players piece
        if self.__moves[position[0]+direction[0]][position[1]+direction[1]] is not player:
            # return position only if empty space
            if not self.__moves[position[0]+direction[0]][position[1]+direction[1]]:
                return (position[0]+direction[0],position[1]+direction[1])
            return None
        # recursion
        return self.__get_next_coordinate((position[0]+direction[0], position[1]+direction[1]),player,direction)

    def get_next_free_coordinates(self, position:tuple[int, int], player:int, direction:str):
        match direction:
            case 'vertical':
                return ((self.__get_next_coordinate(position,player,(1,0)), self.__get_next_coordinate(position,player,(-1,0))))
            case 'horizontal':
                return ((self.__get_next_coordinate(position,player,(0,1)), self.__get_next_coordinate(position,player,(0,-1))))
            case 'inverse_diagonal':
                return ((self.__get_next_coordinate(position,player,(1,-1)), self.__get_next_coordinate(position,player,(-1,1))))
            case 'diagonal':
                return ((self.__get_next_coordinate(position,player,(-1,-1)), self.__get_next_coordinate(position,player,(1,1))))
            case _:
                return None,None
