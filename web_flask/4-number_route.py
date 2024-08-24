#!/usr/bin/python3
""" HBNB_route"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Function that generates the main route """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def do_hbnb():
    """ Function that generates the main route """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def show_c(text) -> str:
    """ Function that show c """
    if '_' in text:
        text = text.replace('_', ' ')
    return f'C {text}'


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def show_python(text) -> str:
    """ Function that show c """
    if '_' in text:
        text = text.replace('_', ' ')
    return f'Python {text}'


@app.route('/number/<int:num>', strict_slashes=False)
def show_num(num):
    """ Function that show num """
    return (f'{num} is a number')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
