import os
from flask import Flask
print(__name__)
app = Flask(__name__, instance_relative_config=True)

def create_app(test_config=None):
    # create and configure the app

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'collab_app.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import post
    app.register_blueprint(post.bp)
    app.add_url_rule('/', endpoint='index')

    return app



create_app()
app.run(port=4004, debug=True, host='0.0.0.0', use_reloader=False)