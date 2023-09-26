#!/usr/bin/env python3
"""
Flask app module
"""
from flask import (
    Flask,
    render_template,
    request,
    g,
)
from flask_babel import Babel


class Config:
    """ Flask Babel configuration class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "fr"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@app.route('/')
def index():
    """ Index route
    """
    return render_template('5-index.html')


@babel.localeselector
def get_locale():
    """ Gets the locale for a web page
    """
    query_str = request.query_string.decode('utf-8').split('&')
    query_dct = dict(item.split('=') for item in query_str)
    locale = query_dct.get('locale')

    user_id = query_dct.get('login_as')
    if user_id:
        stored_user =  users.get(int(user_id))
        if stored_user:
            locale = stored_user.get('locale')

    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """ Get user from request user ID
    """
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """ Perform user login on each request
    """
    user = get_user()
    if user:
        g.user = user


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
