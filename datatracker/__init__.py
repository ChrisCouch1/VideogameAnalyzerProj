import json
import os
from types import SimpleNamespace

import requests
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    response = requests.get("https://api.dccresource.com/api/games/")
    if response.status_code == 200:
        games = json.loads(response.content)
        with open('datatracker/data/vgdb.json', 'w') as openfile:
            json.dump(games, openfile)

    from . import analyzer
    app.register_blueprint(analyzer.bp)

    # app.add_url_rule('/', endpoint='index')



    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
