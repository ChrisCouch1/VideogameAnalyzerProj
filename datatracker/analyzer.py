from flask import Flask, jsonify, request, redirect, flash, render_template, url_for, Blueprint, session
from types import SimpleNamespace

import requests, json

bp = Blueprint('analyzer', __name__)

@bp.route('/test')
def test():
    return "All good!"

@bp.route('/analyzer/systems', methods=['GET', 'POST'])
def system_sales():

    with open('datatracker/data/vgdb.json') as openfile:
        games = json.loads(openfile.read(), object_hook=lambda d: SimpleNamespace(**d))

    total_sales_2013 = {}
    total_sales_2019 = {}

    #PSEUDOCODE FOR PLATFORM SALES CALCULATION
    #for each game
        #if game.year > ___
        #identify its platform
        #if new platform
            #add platform to dict
        #if existing platform
            #add num of global sales to dict "platform_total_sales"

    for game in games:
        if game.year is None:
            continue
        else:
            if game.year >= 2013:
                platform = game.platform
                if platform not in total_sales_2013.keys():
                    total_sales_2013.update({platform: game.globalSales})
                else:
                    total_sales_2013.update({platform: (total_sales_2013[platform] + game.globalSales)})
            if game.year >= 2019:
                platform = game.platform
                if platform not in total_sales_2019.keys():
                    total_sales_2019.update({platform: game.globalSales})
                else:
                    total_sales_2019.update({platform: (total_sales_2019[platform] + game.globalSales)})



    systems_2013 = list(total_sales_2013.keys())
    sales_2013 = list(total_sales_2013.values())

    systems_2019 = list(total_sales_2019.keys())
    sales_2019 = list(total_sales_2019.values())

    return render_template('analyzer/systems.html', platforms13 = systems_2013, sales13 = sales_2013, platforms19 = systems_2019, sales19 = sales_2019)


@bp.route('/analyzer', methods=['GET', 'POST'])
def index():
    foundgame = []

    if request.method == 'POST':
        gameid = request.form.get('gameid')
        if gameid is not None:
            return details(gameid)

        with open('datatracker/data/vgdb.json') as openfile:
            games = json.loads(openfile.read(), object_hook=lambda d: SimpleNamespace(**d))

        user_input = request.form['gametitlesearch']
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


@bp.route('/analyzer/gamedetails', methods=['GET', 'POST'])
def details(gameid):

    gameid = request.form.get('gameid')

    with open('datatracker/data/vgdb.json') as openfile:
        games = json.loads(openfile.read(), object_hook=lambda d: SimpleNamespace(**d))

    for game in games:
        if gameid == game._id:
            foundgame = game
            break

    return render_template('analyzer/gamedetails.html', games=foundgame)


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

