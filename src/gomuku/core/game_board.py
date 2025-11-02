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
        if count >= 4:
            return 4
        if self.__width < (position[0]+direction[0]) < 0 or self.__height < (position[1]+direction[1]) < 0:
            return count
        if self.__moves[position[0]+direction[0]][position[1]+direction[1]] is not player:
            return count
        return self.__count_pieces_direction(count+1,(position[0]+direction[0], position[1]+direction[1]),player,direction)

    def __player_wins(self, move: tuple[int, int], player:int):
        max_in_row = max(
            self.__count_pieces_direction(0,move,player,(1,0)) + self.__count_pieces_direction(0,move,player,(-1,0)),   # - direction
            self.__count_pieces_direction(0,move,player,(0,1)) + self.__count_pieces_direction(0,move,player,(0,-1)),   # | direction
            self.__count_pieces_direction(0,move,player,(1,-1)) + self.__count_pieces_direction(0,move,player,(-1,1)),  # \ direction
            self.__count_pieces_direction(0,move,player,(-1,-1)) + self.__count_pieces_direction(0,move,player,(1,1)),  # / direction
        )
        return max_in_row >=4

    def add_move(self, move: tuple[int, int], player:int):
        if self.__moves[move[0]][move[1]]:
            return False, False
        if player not in [1,2]:
            return False, False
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
