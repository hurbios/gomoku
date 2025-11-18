from gomoku.core.game_board import Board

def draw(board:Board):
    drawing = ""
    for row in range(board.height):
        rowstr = ""
        for col in range(board.width):
            rowstr += " " + str(board.moves[col][row])
        rowstr+= "\n"
        drawing+=rowstr
    print(drawing)
    