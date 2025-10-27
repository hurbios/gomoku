# gomoku
This is Gomuku game with AI. The used AI algorithm is minimax enhanced with alpha-beta pruning.

The used language is Python

This is a learning project with main focus on the algorithm.


## How to run
- Poetry directly: run `poetry run python3.12 src/main.py`
- Poetry shell: run `poetry shell` and inside shell `python3.12 src/index.py`
- Use start script: run `sh run.sh`
    
## Lint
- Pylint config is created with: `poetry run pylint --generate-rcfile >> .pylintrc`
- The pylint can be run with: `poetry run pylint src`
    - (This might take a few seconds to output something)
