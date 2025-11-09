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
                return (1
                        + (self.__count_pieces_direction(0,position,player,(1,0))
                        + self.__count_pieces_direction(0,position,player,(-1,0))))
            case 'horizontal':
                return (1
                        + (self.__count_pieces_direction(0,position,player,(0,1))
                        + self.__count_pieces_direction(0,position,player,(0,-1))))
            case 'inverse_diagonal':
                return (1
                        + (self.__count_pieces_direction(0,position,player,(1,-1))
                        + self.__count_pieces_direction(0,position,player,(-1,1))))
            case 'diagonal':
                return (1
                        + (self.__count_pieces_direction(0,position,player,(-1,-1))
                        + self.__count_pieces_direction(0,position,player,(1,1))))
            case _:
                return 0

    # returns pair (count, direction)
    def __get_max_in_row_count(self, move: tuple[int, int], player:int):
        return sorted([
            (self.get_direction_count(move,player,'vertical'), 'vertical'),           # - direction
            (self.get_direction_count(move,player,'horizontal'), 'horizontal'),         # | direction
            (self.get_direction_count(move,player,'diagonal'), 'diagonal'),           # / direction
            (self.get_direction_count(move,player,'inverse_diagonal'), 'inverse_diagonal')   # \ direction
        ], reverse=True)

    def __player_wins(self, move: tuple[int, int], player:int):
        return self.__get_max_in_row_count(move, player)[0][0] >=5

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

    ############################
    ### Move evaluations #######
    ############################

    def __get_count_for_x_order_direction(self, move:tuple[int, int], player:int):
        # TODO: improve: if multiple same, get the one with most empty spaces
        ordered_max_counts_high_to_low = self.__get_max_in_row_count(move, player)
        count, direction = ordered_max_counts_high_to_low[0]
        next_coordinates = self.get_next_free_coordinates(move, player, direction)
        empty_spaces = 1 if next_coordinates[0] is not None else 0
        empty_spaces += 1 if next_coordinates[1] is not None else 0
        second_count, second_direction = ordered_max_counts_high_to_low[1]
        if count >= 3 and second_count >= 3:
            second_next_coordinates = self.get_next_free_coordinates(move, 1, second_direction)
            second_empty_spaces = 1 if second_next_coordinates[0] is not None else 0
            second_empty_spaces += 1 if second_next_coordinates[1] is not None else 0
        else:
            second_empty_spaces = 0
        return count, empty_spaces, second_count, second_empty_spaces

    # number - description - ((points))
    # 0.  LOST - other has 5th in row ((-8))
    # 1.  ATTACK - add 5th for the row ((8))
    # 2.  BLOCK - block 5th in a row with one sided empty space ((-7))
    # 3.  ATTACK - add 4th in a row both sides empty space ((7))
    # 3.  ATTACK - add 4th in a row (one or more empty space) ((6))
    # 4.  BLOCK - block 4th in a row with both sides empty space ((-6))
    # 5.  ATTACK - add center for dual 3rd in a row with empty spaces around (4)  ((5))
    # 6.  BLOCK - block center for dual 3rd in a row with empty spaces around (4) ((-5))
    # 7.  ATTACK - add 3rd in a row with empty spaces around ((4))
    # 8.  BLOCK - block center for dual 3rd in a row with 3 or less empty spaces around ((-4))
    # 9.  ATTACK - add 3rd in a row with one side empty space ((3))
    # 10. BLOCK - block 4th in a row with one side empty space ((-3))
    # 11. BLOCK - block 3rd in a row with empty spaces around ((-2))
    # 12. ATTACK - add 2nd in a row with empty spaces around ((2))
    # 13. BLOCK - block 3rd in a row with one side empty spaces around ((-1))
    # 14. BLOCK - block 2nd in a row with empty spaces around (4) ((0))
    # 15. ATTACK - add 1st in a row with as many empty spaces around as possible ((1))
    def evaluate_move(self, move:tuple[int, int]):
        (
            count_usr,
            usr_empty_spaces,
            second_count_usr,
            second_usr_empty_spaces
        ) = self.__get_count_for_x_order_direction(move, 1)

        (
            count_ai,
            ai_empty_spaces,
            second_count_ai,
            second_ai_empty_spaces
        ) = self.__get_count_for_x_order_direction(move, 2)

        evaluations = (
            # 0.  LOST - other has 5th in row ((-8))
            (count_usr >= 6, -8),
            # 1.  ATTACK - add 5th for the row ((8))
            (count_ai >= 5, 8),
            # 2.  BLOCK - block 5th in a row with one sided empty space ((-7))
            (count_usr >= 5, -7),
            # 3.  ATTACK - add 4th in a row (two empty space) ((7))
            (count_ai >= 4 and ai_empty_spaces >= 2, 7),
            # 3.  ATTACK - add 4th in a row (one empty space) ((6))
            (count_ai >= 4 and ai_empty_spaces >= 1, 6),
            # 4.  BLOCK - block 4th in a row with both sides empty space ((-6))
            (count_usr >= 4 and usr_empty_spaces >= 2, -6),
            # 5.  ATTACK - add center for dual 3rd in a row with empty spaces around (3)  ((5))
            (count_ai >= 3 and second_count_ai >= 3 and ai_empty_spaces + second_ai_empty_spaces >= 3, 5),
            # 6.  BLOCK - block center for dual 3rd in a row with empty spaces around (4) ((-5))
            (count_usr >= 3 and second_count_usr >= 3 and usr_empty_spaces + second_usr_empty_spaces >= 4, -5),
            # 7.  ATTACK - add 3rd in a row with empty spaces around ((4))
            (count_ai >= 3 and ai_empty_spaces >= 2, 4),
            # 8.  BLOCK - block center for dual 3rd in a row with 3 or less empty spaces around ((-4))
            (count_usr >= 3 and second_count_usr >= 3 and usr_empty_spaces + second_usr_empty_spaces >= 3, -4),
            # 9.  ATTACK - add 3rd in a row with one side empty space ((3))
            (count_ai >= 3 and ai_empty_spaces >= 1, 3),
            # 10. BLOCK - block 4th in a row with one side empty space ((-3))
            (count_usr >= 4 and usr_empty_spaces >= 1, -3),
            # 11. BLOCK - block 3rd in a row with empty spaces around ((-2))
            (count_usr >= 3 and usr_empty_spaces >= 2, -2),
            # 12. ATTACK - add 2nd in a row with empty spaces around ((2))
            (count_ai >= 2 and ai_empty_spaces >= 2, 2),
            # 13. BLOCK - block 3rd in a row with one side empty spaces around ((-1))
            (count_usr >= 3 and usr_empty_spaces >= 1, -1),
            # 14. BLOCK - block 2nd in a row with empty spaces around (4) ((0))
            (count_usr >= 2 and usr_empty_spaces >= 2, 0),
            # 15. ATTACK - add 1st in a row with as many empty spaces around as possible ((1))
            (count_usr >= 1 and usr_empty_spaces >= 2, 1)
        )

        for i,evaluation in enumerate(iter(evaluations)):
            print(i, evaluation[0], evaluation[1], count_ai, ai_empty_spaces)
            if evaluation[0]:
                return evaluation[1]

        return 0
