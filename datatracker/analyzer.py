from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
from types import SimpleNamespace
import requests, json

bp = Blueprint('analyzer', __name__)


@bp.route('/test')
def test():
    return "All good!"

@bp.route('/analyzer', methods=['GET', 'POST'])
def index():

    response = requests.get("https://api.dccresource.com/api/games/5faac562db090e1a5c2dea16")
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))

    if request.method == 'POST':
        response = requests.get("https://api.dccresource.com/api/games/")
        games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))

        user_input = request.form['gametitlesearch']
        foundgame = []
        for game in games:
            if user_input in game.name:
                foundgame.append(game)

    return render_template('analyzer/index.html', foundgame=foundgame)
    #games = API call

# @bp.route('/analyzer')
# def index():
#     message = "This text is coming from the 'analyzer.py' module, not the html file!"
#     phrase = "Python is cool!"
#     return render_template('analyzer/index.html', message=message, word=phrase)


@bp.route('/postform', methods=('GET', 'POST'))
def other_example():
    if request.method == 'POST':
        page_title = request.form['title']
        error = None

        if not page_title:
            error = 'You must enter a title'

        if error is not None:
            flash(error)
        elif request.form['title'] == "go home":
            return redirect(url_for('analyzer.index'))
        else:
            return render_template('analyzer/postform.html', page_title=page_title)

    else:
        return render_template('analyzer/postform.html', page_title="PostForm from Module Function")

