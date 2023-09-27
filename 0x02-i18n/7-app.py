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
import pytz


class Config:
    """ Flask Babel configuration class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
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
    force_locale = request.args.get('locale')
    if force_locale:
        locale = force_locale
    else:
        try:
            locale = g.user.get('locale')
        except Exception:
            locale = request.headers.get('locale')

    if locale and locale in app.config['LANGUAGES']:
        return locale
    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """
    Retrieves the timezone for a web page
    """
    tz = request.args.get('timezone').strip()
    if not tz and g.user:
        tz = g.user['timezone']
    try:
        return pytz.timezone(tz).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


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
