from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint
from types import SimpleNamespace
import requests, json

bp = Blueprint('analyzer', __name__)

@bp.route('/test')
def test():
    return "All good!"

@bp.route('/analyzer/systems', methods=['GET', 'POST'])
def system_sales():
    response = requests.get("https://api.dccresource.com/api/games/")
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))

    platform_total_sales = {}

    #PSEUDOCODE FOR PLATFORM SALES CALCULATION
    #for each game
        #identify its platform
        #if new platform
            #add platform to dict
        #if existing platform
            #add num of global sales to dict "platform_total_sales"

    for game in games:
        platform = game.platform
        if platform not in platform_total_sales.keys():
            platform_total_sales.update({platform: game.globalSales})
        else:
            platform_total_sales.update({platform: (platform_total_sales[platform] + game.globalSales)})

    return_systems = list(platform_total_sales.keys())
    return_sales = list(platform_total_sales.values())
    return render_template('analyzer/systems.html', platforms = return_systems, sales = return_sales)


@bp.route('/analyzer', methods=['GET', 'POST'])
def index():

    response = requests.get("https://api.dccresource.com/api/games/5faac562db090e1a5c2dea16")
    games = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
    foundgame = []

    if request.method == 'POST':
        response = requests.get("https://api.dccresource.com/api/games/")
        games = json.loads(response.content, object_hook=lambda d:SimpleNamespace(**d))

        user_input = request.form['gametitlesearch']
        for game in games:
            if user_input in game.name:
                foundgame.append(game)

    return render_template('analyzer/index.html', foundgame = foundgame)
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

