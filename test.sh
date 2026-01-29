#!/bin/bash
ITER_DEPTH=6 poetry run pytest src/gomoku/core/tests/minimax_test.py::TestMinimax::test_get_next_move_should_attack_case2_with_iter_depth_6
ITER_DEPTH=4 poetry run coverage run --branch -m pytest
poetry run coverage report -m