# -*- coding: utf-8 -*-

import  os

import setipy.model as model

from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('menu.html')

@app.route('/series')
def series():
    series = model.Session.query(model.Serie).all()
    return render_template('series.html', series=series)

@app.route('/serie/<id>')
def serie(id):
    serie = model.Session.query(model.Serie).get(id)
    return render_template('serie.html', serie=serie)

@app.route('/episodes/<serie_id>/<season_num>')
def episodes(serie_id, season_num):
    serie = model.Session.query(model.Serie).get(serie_id)
    seasons = filter(lambda item: item.num == season_num, serie.seasons)
    assert(len(seasons) == 1)
    return render_template('episodes.html', serie=serie, season=seasons[0])

@app.route('/downloads')
def downloads():
	episodes = model.Session.query( model.Episode ).filter_by(path=None).all()
	raise Exception(episodes)
	return render_template('downloads.html')

@app.route('/renames')
def renames():
	return render_template('renames.html')
