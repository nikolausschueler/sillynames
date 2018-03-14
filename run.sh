#!/bin/bash

if ! which flask; then
  echo Flask is not installed, will try to install >&2
  sudo pip install flask
  sudo pip install flask-wtf
fi

export FLASK_APP=names.py
flask run
