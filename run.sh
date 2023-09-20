#!/bin/sh
cd `dirname $0`

# Create a virtual environment to run our code
VENV_NAME="venv"
PYTHON="$VENV_NAME/bin/python"

python3 -m venv $VENV_NAME
$PYTHON -m pip install -r requirements.txt -U # remove -U if viam-sdk should not be upgraded whenever possible


exec $PYTHON src/main.py $@
