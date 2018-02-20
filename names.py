#!/usr/bin/env python

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def random_name():
    name = 'Fred Frobisher'
    return render_template('name.html', name=name)
