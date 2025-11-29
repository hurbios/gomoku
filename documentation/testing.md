# Testing

## Coverage
Unit testing up to date coverage can be seen here: [![codecov](https://codecov.io/github/hurbios/gomoku/graph/badge.svg?token=TGI5QXQLXL)](https://codecov.io/github/hurbios/gomoku)

The coverage when writing this document is:
```
Name                             Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------------
src/gomoku/core/config.py            3      0      0      0   100%
src/gomoku/core/directions.py        1      0      0      0   100%
src/gomoku/core/game_board.py      173     10     86      4    93%   24, 28, 32, 37-39, 45-47, 109->100, 142
src/gomoku/core/minimax.py         103      0     40      0   100%
src/gomoku/core/player_rows.py     139      0     56      1    99%   98->101
----------------------------------------------------------------------------
TOTAL                              419     10    182      5    97%
```


# Tested portions
- The tested portions are mostly currently game board logic and move "goodness" evaluation testing with unit tests.
- Testing for minimax algorithm is still mostly missing because the algorithm is still under development.
    - Testing this has been mostly empirical with game UI. 
    - This can later be improved to work by inputting values one by one of a game play so that the game can be replayed in different game types.
    - Should test that the AI can win in situations that should be "easily" winnable with couple of moves and doesn't lose in couple of moves in situations that should be "easily" defendable. Cases TBD later.




