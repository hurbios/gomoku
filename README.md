[![Lint and test](https://github.com/hurbios/gomoku/actions/workflows/pipeline.yml/badge.svg)](https://github.com/hurbios/gomoku/actions/workflows/pipeline.yml)[![codecov](https://codecov.io/github/hurbios/gomoku/graph/badge.svg?token=TGI5QXQLXL)](https://codecov.io/github/hurbios/gomoku)
# gomoku
This is Gomoku game with AI. The used AI algorithm is minimax enhanced with alpha-beta pruning.

The used language is Python

This is a learning project with main focus on the algorithm.

## How to install
(This app requires Poetry version >=2.0.0 and Python 3.12)
- Run `poetry install`

## How to run
Options for running:
- Poetry directly: run `poetry run python3.12 -m gomoku.main`
- Poetry shell: run `poetry shell` and inside shell `python3.12 -m gomoku.main`
- Use start script: run `sh run.sh`
    - This runs the game with env param `ITER_DEPTH=4`. This will iterate 4 moves ahead instead of variable iteration depth based on time.
- When running without `ITER_DEPTH` parameter iteration time `CUTOFFTIME` can be set in ([config.py](./src/gomoku/core/config.py)).
    
## Run unit tests and test coverage
Options for testing and coverage:
- Testing
    - Run using poetry: `poetry run pytest`
    - Poetry shell: run `poetry shell` and inside shell `pytest`
- Test coverage
    - For coverage test and report, run a script: `sh test.sh`
        - This runs tests with env param `ITER_DEPTH=4`. This will increase the test time and can take minutes.
    - There is a Github Actions workflow that runs the coverage with env param `ITER_DEPTH=3` (see the badge for coverage percentage)
- For performance testing by logging minimax times with iteration depth 4 during manual testing use `sh run_with_time_log.sh` to start the game

## Lint
- Pylint config was created with: `poetry run pylint --generate-rcfile >> .pylintrc`
- The pylint can be run with: `poetry run pylint src`
    - (This might take a few seconds to output something)
- There is a Github Actions workflow that runs the pylint (click the badge to see results)
- (for vscode pylint `"pylint.args": ["--disable=E0015"]` can be added to `Pylint: Args` setting to remove linting error for first line if pylint extension is used)

## About Python and Poetry version
- Used python version is set in Poetry to be ~3.12 because pygame does not support newer versions. Coverage would require Python 3.10+ but this app has not been tested with other than version 3.12 so limiting the version to 3.12)
- The poetry version when running this app needs to be >=2.0.0 because the project is using new pyproject.toml style. More information about the poetry project.toml style change [here](https://python-poetry.org/blog/announcing-poetry-2.0.0/#supporting-the-project-section-in-pyprojecttoml-pep-621).