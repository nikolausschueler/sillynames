#!/usr/bin/env python

from flask import Flask, render_template

app = Flask(__name__)

class Name:

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

@app.route('/')
def random_name():
    name = Name('Fred', 'Frobisher')
    return render_template('name.html', name=name)
