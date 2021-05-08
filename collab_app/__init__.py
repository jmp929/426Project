import os
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
print(__name__)
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

    from collab_app import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import post
    app.register_blueprint(post.bp)
    app.add_url_rule('/', endpoint='index')

    return app



create_app()
app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)))