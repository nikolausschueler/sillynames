#!/usr/bin/env python3

from flask import Flask, flash, render_template, redirect, request, url_for
from wtforms import Form, TextField, validators
import csv
import logging
import random
import sys

CSV_FILE = 'names.csv'
CSV_HEADERS = (
    'Firstname',
    'Lastname',
    'Firstlastfunny',
    'Resolution',
    'Explanation',
    'Author',
    'Comment')

ERROR_NO_NAME_FOUND = 'Kein Name gefunden'
ERROR_EMPTY_SEARCH = \
        'Ich brauch mindestens einen Vor- oder Nachnamen'

logging.basicConfig(level=logging.WARN)


class Name:

    def __init__(self, firstname, lastname, firstlastfunny):
        self.firstname = firstname
        self.lastname = lastname
        self.firstlastfunny = firstlastfunny

    def get_puzzle_name(self):
        """
        Get the name in the form that lets you puzzle a bit what's funny about
        it. For example, "Sigrid Top" is the puzzle form of "Top, Sigrid".
        """
        if self.firstlastfunny:
            s = self.lastname + ', ' + self.firstname
        else:
            s = self.firstname + ' ' + self.lastname
        return s

    def get_funny_name(self):
        """
        Get the name in it's (presumably) funny form. For example,
        "Top, Sigrid" is the funny form of "Sigrid Top".
        """
        if self.firstlastfunny:
            s = self.firstname + self.lastname
        else:
            s = self.lastname + self.firstname
        return s.capitalize()

    @staticmethod
    def from_csv(f):
        """
        Returns a list of names, read from a CSV file.
        """
        dr = csv.DictReader(f, fieldnames=CSV_HEADERS, delimiter=';')
        names = []
        for row in dr:
            logging.debug('Got CSV row: %s' % row)
            name = Name(
                    row['Firstname'],
                    row['Lastname'],
                    row['Firstlastfunny'])

            # The fields are not mandatory, so reading may fail gracefully
            # with a default value.
            name.resolution = row.get('Resolution')
            name.explanation = row.get('Explanation')
            name.author = row.get('Author')
            name.comment = row.get('Comment')
            logging.debug(
                    'Read name with firstname %s and lastname %s' %
                    (name.firstname, name.lastname))
            names.append(name)
        return names

    @staticmethod
    def names_from_csv(f):
        names = Name.from_csv(f)

        # Ignore the header, we are only interested in the data.
        return names[1:]

    @staticmethod
    def search_name(names, firstname, lastname):
        for name in names:
            if ((firstname and firstname in name.firstname) or
               (lastname and lastname in name.lastname)):
                return name
        return None

#
# Initialization.
#
app = Flask(__name__)
app.config['SECRET_KEY'] = 'totally secret key'

with open(CSV_FILE, encoding='utf-8') as csv_file:
     names = Name.names_from_csv(csv_file)


@app.route('/name')
def name():
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    name = Name.search_name(names, firstname, lastname)
    return render_template('name.html', name=name)


@app.route('/')
def random_name():
    name = random.choice(names)
    return render_template('name.html', name=name)


class SearchForm(Form):
    firstname = TextField('Firstname:', validators=[validators.Optional()])
    lastname = TextField('Lastname:', validators=[validators.Optional()])
    error = ''

    def validate(self):
        if not super(SearchForm, self).validate():
            return False
        if not self.firstname.data and not self.lastname.data:
            msg = ERROR_EMPTY_SEARCH
            self.error = msg
            return False
        return True


@app.route('/search', methods=['GET', 'POST'])
def search_name():
    form = SearchForm(request.form)

    print(form.errors)
    if request.method == 'POST':

        if form.validate():
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            name = Name.search_name(names, firstname, lastname)
            if not name:
                flash(ERROR_NO_NAME_FOUND)
                return redirect(url_for('search_name'))
            else:
                return render_template('name.html', name=name)
        else:
            flash(form.error)
            return redirect(url_for('search_name'))

    return render_template('search.html', form=form)


@app.route('/all')
def all_names():
    return render_template('names.html', names=names)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
