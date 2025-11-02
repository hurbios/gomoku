[![Lint and test](https://github.com/hurbios/gomoku/actions/workflows/pipeline.yml/badge.svg)](https://github.com/hurbios/gomoku/actions/workflows/pipeline.yml)[![codecov](https://codecov.io/github/hurbios/gomoku/graph/badge.svg?token=TGI5QXQLXL)](https://codecov.io/github/hurbios/gomoku)
# gomoku
This is Gomuku game with AI. The used AI algorithm is minimax enhanced with alpha-beta pruning.

The used language is Python

This is a learning project with main focus on the algorithm.

## How to install
(This app requires Python 3.12 because pygame does not support newer versions.)
- Run `poetry install`

## How to run
- Poetry directly: run `poetry run python3.12 -m gomoku.main`
- Poetry shell: run `poetry shell` and inside shell `python3.12 -m gomoku.main`
- Use start script: run `sh run.sh`
    
## Run unit tests and test coverage
- Run using poetry: `poetry run pytest`
- Run test script for coverage test and report: `sh test.sh`

## Lint
- Pylint config is created with: `poetry run pylint --generate-rcfile >> .pylintrc`
- The pylint can be run with: `poetry run pylint src`
    - (This might take a few seconds to output something)
- There is a Github Actions workflow that runs the pylint (click the badge to see results)
