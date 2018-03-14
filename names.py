#!/usr/bin/env python

from flask import Flask, flash, render_template, request
from wtforms import Form, TextField
import csv
import logging
import random
import sys

CSV_FILE = 'names.csv'
CSV_HEADERS = ('Firstname', 'Lastname', 'Firstlastfunny', 'Resolution',
    'Explanation', 'Author', 'Comment')

logging.basicConfig(level=logging.DEBUG)

class Name:

    def __init__(self, firstname, lastname, firstlastfunny):
        self.firstname = firstname
        self.lastname = lastname
        self.firstlastfunny = firstlastfunny

    def get_puzzle_name(self):
        '''
        Get the name in the form that lets you puzzle a bit what's funny about
        it. For example, "Sigrid Top" is the puzzle form of "Top, Sigrid".
        '''
        if self.firstlastfunny:
            s = self.lastname + ', ' + self.firstname
        else:
            s = self.firstname + ' ' + self.lastname
        return s

    def get_funny_name(self):
        '''
        Get the name in it's (presumably) funny form. For example, "Top, Sigrid"
        is the funny form of "Sigrid Top".
        '''
        if self.firstlastfunny:
            s = self.firstname + self.lastname
        else:
            s = self.lastname + self.firstname
        return s.capitalize()

    @staticmethod
    def from_csv(f):
        '''
        Returns a list of names, read from a CSV file.

        This reads all fields as unicode.
        '''
        dr = csv.DictReader(f, fieldnames=CSV_HEADERS, delimiter=';')
        names = []
        for row in dr:
            logging.debug('Got CSV row: %s' % row)
            name = Name(unicode(row['Firstname'], 'utf-8'),
                unicode(row['Lastname'], 'utf-8'),
                unicode(row['Firstlastfunny'], 'utf-8'))

            # The fields are not mandatory, so reading may fail gracefully with a
            # default value.
            name.resolution = unicode(row.get('Resolution'), 'utf-8')
            name.explanation = unicode(row.get('Explanation'), 'utf-8')
            name.author = unicode(row.get('Author', 'utf-8'))
            name.comment = unicode(row.get('Comment', 'utf-8'))
            logging.debug('Read name with firstname %s and lastname %s' %
                    (name.firstname, name.lastname))
            names.append(name)
        return names

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

#import pdb; pdb.set_trace()

names = Name.from_csv(open(CSV_FILE))

# Ignore the header, we are only interested in the data.
names = names[1:]

@app.route('/')
def random_name():

    # This ignores the first row, which contains the header.
    name = random.choice(names)

    return render_template('name.html', name=name)

class SearchForm(Form):
    firstname = TextField('Firstname:')
    lastname = TextField('Lastname:')

@app.route('/search', methods=['GET', 'POST'])
def search_name():
    form = SearchForm(request.form)

    print form.errors
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        name = Name.search_name(names, firstname, lastname)
        print 'Found name', name.firstname, name.lastname

        if form.validate():
            # Save the comment here.
            flash('Hello ' + firstname)
        else:
            flash('All the form fields are required. ')

    return render_template('search.html', form=form)
