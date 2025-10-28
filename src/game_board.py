class Board:
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.__moves = [[0 for _ in range(height)] for _ in range(width)]
        self.__player1_pieces = []
        self.__player2_pieces = []


    def size(self):
        return len(self.__moves), len(self.__moves[0])
    
    def count_pieces_direction(self, count:int, position:tuple[int, int], player:int, x_direction:int, y_direction:int):
        if count >= 4:
            return 4
        if self.__width < (position[0]+x_direction) < 0 or self.__height < (position[1]+y_direction) < 0:
            return count
        if self.__moves[position[0]+x_direction][position[1]+y_direction] is not player:
            return count
        return self.count_pieces_direction(count+1,(position[0]+x_direction, position[1]+y_direction),player,x_direction,y_direction)
        

    def __player_wins(self, move: tuple[int, int], player:int):
        max_in_row = max(
            self.count_pieces_direction(0,move,player,1,0) + self.count_pieces_direction(0,move,player,-1,0),   # - direction
            self.count_pieces_direction(0,move,player,0,1) + self.count_pieces_direction(0,move,player,0,-1),   # | direction
            self.count_pieces_direction(0,move,player,1,-1) + self.count_pieces_direction(0,move,player,-1,1),  # \ direction
            self.count_pieces_direction(0,move,player,-1,-1) + self.count_pieces_direction(0,move,player,1,1),  # / direction
        )
        return True if max_in_row >=4 else False

    def add_move(self, move: tuple[int, int], player:int):
        if self.__moves[move[0]][move[1]]:
            return False, False
        self.__moves[move[0]][move[1]] = player
        if player == 1:
            self.__player1_pieces.append(move)
        else:
            self.__player2_pieces.append(move)
        return True, (True if self.__player_wins(move, player) else False)
    
    def get_player_pieces(self, player):
        return self.__player1_pieces if player == 1 else self.__player2_pieces
    
    def reset(self):
        self.__moves = [[0 for _ in range(self.__height)] for _ in range(self.__width)]
        self.__player1_pieces = []
        self.__player2_pieces = []
