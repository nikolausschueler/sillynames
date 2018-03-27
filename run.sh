#!/bin/bash

if ! which flask; then
  echo Flask is not installed, bailing out. >&2
fi

export FLASK_APP=names.py
flask run
