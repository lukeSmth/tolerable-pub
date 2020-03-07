import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG=True,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing other configs
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        from . import forms
        from . import input_forms
        from . import output_forms
        from . import routes
        from . import util
        from . import symbolic
        from . import simulate

    return app