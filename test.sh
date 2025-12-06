#!/bin/bash
ITER_DEPTH=4 poetry run coverage run --branch -m pytest
poetry run coverage report -m