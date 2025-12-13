import csv
import os
from gomoku.core.config import DEBUG

LOG_TIME = os.environ.get('LOG_TIME')

# Draws the board.

# Example:

#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 2 1 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 2 0 1 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

def draw(board, debug:bool=DEBUG):
    if debug:
        drawing = ""
        for row in range(board.height):
            rowstr = ""
            for col in range(board.width):
                rowstr += " " + str(board.moves[col][row])
            rowstr+= "\n"
            drawing+=rowstr
        print(drawing)

def debug_log(to_print:str):
    if DEBUG:
        print(to_print, flush=True)

def log_calc_time(number_of_moves_on_board, time_elapsed):
    if LOG_TIME:
        with open('./times.log', 'a', encoding='UTF-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow((number_of_moves_on_board, time_elapsed))
