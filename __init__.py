import os
import flask

def create_app(test_config=None):
    # make a new flask app with config and database files existing
    # outside the source directory.
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'lucid.sqlite'),
    )

    # read config parameters from config.py
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # make a folder for instance-related files if necessary.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, world!'


    # register database functionality
    from . import db
    db.init_app(app)

    # register all blueprints
    from . import index
    app.register_blueprint(index.bp)
    
    
    return app
