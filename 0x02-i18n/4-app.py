#!/usr/bin/env python3
"""
Flask app module
"""
from flask import (
    Flask,
    render_template,
    request,
)
from flask_babel import Babel


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


@app.route('/')
def index():
    """ Index route
    """
    return render_template('3-index.html')


@babel.localeselector
def get_locale():
    """ Gets the locale for a web page
    """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
