# Testing
This application is tested with unit tests, integration tests and manual testing from UI.

The tested portions for unit tests are parts that are used in other components but not used so much in other components that mocking/stubbing would require rewriting most of the functionalities of the component. Those components that are using only 100% coverage unit tested components are tested with integration testing with 100% coverage.

Minimax is tested only with integration testing / end-to-end testing.

The tested portions are divided roughly to 2 categories:
- The tested portions are mostly currently game board logic and move "goodness" evaluation testing with automatic tests.
- Testing for minimax algorithm
    - Testing this has been mostly empirical with game UI. 
    - Unit tests are covering normal situations where the algorithm should detect moves to do. Some tests require more iteration depth so those will take more time than normal CI pipeline has time. Those tests are then omitted from the github actions workflow.
    - Automatic test are testing that the AI can win in situations that should be "easily" winnable with couple of moves and doesn't lose in couple of moves in situations that should be "easily" defendable.

Project files and rationales for test type and test exclusion for some modules:
- `gomoku.core.directions` and `gomoku.core.config` there are no tests specifically targeting these modules because they have no logic, only constants.
- `gomoku.core.helper` there are no tests specifically targeting this module because this module contains only helper functions for debugging purposes.
- `gomoku.main` there are no tests specifically targeting this module because the module is just launching the application but there is nothing specific to be tested here.
- `gomoku.ui.game_board_ui` is not tested / only manually tested as part of end-to-end testing. UI testing is out of the scope of this project.
- `gomoku.core.player_rows` is unit tested with 100% coverage. Any external component to the player_rows module is mocked.
- `gomoku.core.game_board` is integration tested. The module depends on `gomoku.core.player_rows` and `gomoku.core.directions` modules. Because the `gomoku.core.game_board` modules functions are highly depended on the functionality of the `gomoku.core.player_rows` module, and would thus need to nearly duplicate the functionality for the mock, there is no point of doing unit testing for each function. Integration test offers better reliability in this case.
- `gomoku.core.minimax` is integration tested and manually tested as part of end-to-end testing. This module is depending of `gomoku.core.game_board` heavily and thus cannot be easily unit tested. Same rationale as with above applies here as well.


## Unit tests and integration tests
Unit and integration tests are done with Python's unittest library.

Unit testing up to date coverage can be seen here: [![codecov](https://codecov.io/github/hurbios/gomoku/graph/badge.svg?token=TGI5QXQLXL)](https://codecov.io/github/hurbios/gomoku) 

However, this automatic coverage is not testing full set of test in `minimax_test.py` because some of the tests are skipped in Github Actions Workflow to keep the testing time short. So the actual coverage can be a bit higher than what is stated in the badge.

The coverage when writing this document is:
```
Name                             Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------------
src/gomoku/core/config.py            2      0      0      0   100%
src/gomoku/core/directions.py        1      0      0      0   100%
src/gomoku/core/game_board.py      189      0    108      0   100%
src/gomoku/core/minimax.py         113      4     54      2    95%   32-34, 131
src/gomoku/core/player_rows.py     142      0     64      0   100%
----------------------------------------------------------------------------
TOTAL                              447      4    226      2    99%
```
Lines 32-34, 130 in `src/gomoku/core/minimax.py` are about timeout functionality so that the AI calculation stops at predifined max calculation time instead of iteration depth. This functionality is tested manually.


### Automatic tests for the algorithm
- Test that algorithm selects a winning move from when certain win on board with `XX_XX` row
- Test that algorithm selects a blocking move from when certain lose without blocking `__OOO__` row
    - Continues to block if `O` builds row after first block so that after two moves row is `_OOOOX_` and finally becomes `XOOOOX_`
- Test that algorithm selects blocking move that maximizes blocking effect by blocking 2 crossing rows with one move
- Test that algorithm selects winning a move with 3 moves instead of blocking other players win in 4 moves if not blocked but certain win if not blocking with next move and cannot win within 3 moves
- Test that algorithm selects winning move on next move instead of blocking other players winning move in 2 moves
- Test that algorithm selects winning move in 3 and selects the winning move after other player has selected blocking move


## Manual testing
### Case 1: Block open row of 3
- block instead of attacking to make open row of 3
- block instead of blocking one side open row of 3

### Case 2: Block one side open row of 4
- block instead of attacking to make open row of 4 or one side open row of 4
- block instead of blocking rows with less pieces in row

### Case 3: Attack open row of 3
- attack to create open row of 3 if not losing in 4 moves if not blocking some other row
- attack to create open row of 3 instead of creating row of 2
- attack to create open row of 3 instead of blocking one side open row of 3

### Case 4: Attack open row of 4
- attack to create open row of 4 if not losing on next other players move if not blocking some other row
- attack to create open row of 4 instead of one side open row of 4

### Case 5: Attack one side open row of 4
- Test that AI wins when one side open row of 4 exist for example in following situations
    - other player has open or one side open row of 4


## Performance testing
- Performance testing is done with help of manual testing from UI. To achieve this, a decorator helper function is created to handle this. The function logs to a separate file time it takes for minimax to iterate to depth 4 and amount of current moves on game board.
- The times of the created file was imported to Google Sheets to calculate the average times in seconds (y-axis) when certain number of moves (x-axis) is on the board when `gomoku.core.minimax.get_next_move` method is called.

![AVERAGE of time vs. moves from 36 games](avg_time_graph.png "AVERAGE of time vs. moves from 36 games")

As it can be seen from the graph, there are couple of spikes in the average time. These are due to having one calculation that is taking longer than most. This is because alpha-beta pruning is not successful in these cases. In most cases the alpha-beta pruning with iterative deepening works sufficiently to keep the calculation time below 5 seconds. The calculation time is also dependent on the system that the calculation is run on. This graph should however reflect how well the algorithm performs on normal modern laptop.



