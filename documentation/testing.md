# Testing

## Coverage
Unit testing up to date coverage can be seen here: [![codecov](https://codecov.io/github/hurbios/gomoku/graph/badge.svg?token=TGI5QXQLXL)](https://codecov.io/github/hurbios/gomoku)

The coverage when writing this document is:
```
Name                                       Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------------------------
src/gomoku/core/game_board.py                114     19     52      1    82%   100-104, 107-111, 152-162, 256
src/gomoku/core/minimax.py                    49     33     20      0    23%   74-119
src/gomoku/core/tests/game_board_test.py     134      0     66      0   100%
src/gomoku/core/tests/minimax_test.py         20      0      4      0   100%
--------------------------------------------------------------------------------------
TOTAL                                        317     52    142      1    82%
```


# Tested portions
- The tested portions are mostly currently game board logic and move "goodness" evaluation testing with unit tests.
- Testing for minimax algorithm is still missing because the algorithm is still under development.
    - Testing this has been mostly empirical with game UI. 
    - This can later be improved to work by inputting values one by one of a game play so that the game can be replayed in different game types.
    - Should test that the AI can win in situations that should be "easily" winnable with couple of moves and doesn't lose in couple of moves in situations that should be "easily" defendable. Cases TBD later.




