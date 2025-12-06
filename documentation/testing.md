# Testing

## Coverage
Unit testing up to date coverage can be seen here: [![codecov](https://codecov.io/github/hurbios/gomoku/graph/badge.svg?token=TGI5QXQLXL)](https://codecov.io/github/hurbios/gomoku)

The coverage when writing this document is:
```
Name                             Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------------
src/gomoku/core/config.py            2      0      0      0   100%
src/gomoku/core/directions.py        1      0      0      0   100%
src/gomoku/core/game_board.py      177      4     90      1    98%   22, 26, 30, 143
src/gomoku/core/minimax.py         125      6     68      6    92%   29-31, 45-46, 61->60, 64->63, 67->66, 112
src/gomoku/core/player_rows.py     141      0     64      0   100%
----------------------------------------------------------------------------
TOTAL                              446     10    222      7    97%
```


# Tested portions
- The tested portions are mostly currently game board logic and move "goodness" evaluation testing with unit tests.
- Testing for minimax algorithm
    - Testing this has been mostly empirical with game UI. 
    - Unit tests are covering normal situations where the algorithm should detect moves to do. Some tests require more iteration depth so those will take more time than normal CI pipeline has time. Those are then omitted from the normal tests.
    - Should test that the AI can win in situations that should be "easily" winnable with couple of moves and doesn't lose in couple of moves in situations that should be "easily" defendable. Cases TBD later.




