# -*- coding: utf-8 -*-

import  os

import bs.model as model

from flask import Flask, render_template, request

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

@app.route('/episodes/<id_serie>/<season_num>')
def episodes(id_serie, season_num):
    serie = model.Session.query(model.Serie).get(id_serie)
    seasons = filter(lambda item: item.num == season_num, serie.seasons)
    assert(len(seasons) == 1)
    return render_template('episodes.html', serie=serie, season=seasons[0])
    
@app.route('/episode/<id_serie>/<episode_num>')
def episode(id_serie, episode_num):
	episode = model.Session.query( model.Episode ).filter_by(num=episode_num).join( model.Season ).filter_by(id_serie=id_serie).one()
	return render_template('episode.html', episode=episode)

@app.route('/ajax/<action>')
def ajax(action):
    if action == 'setEnabled':
        kind = request.args.get('kind', None)
        if kind is not None and kind in ['serie', 'season', 'episode']:
            kid = request.args.get('id', None)
            value = request.args.get('value', None)
            
            if kid is None or value is None:
                raise Exception('Please provide id/value pair')
            
            if value not in ['on', 'off']:
                raise Exception('Value can only be on/off')
            
            models = {
                'serie': model.Serie,
                'episode': model.Episode,
                'season': model.Season
            }
            model.Session.query( models[kind] ).get(kid).enabled = (value == 'on')
            model.Session.flush
            
            return 'ok'
            
    	raise Exception('Provide a valid kind')
    raise Exception('Unknown action')

@app.route('/downloads')
def downloads():
	episodes = model.Session.query( model.Episode ).filter_by(path=None).all()
	raise Exception(episodes)
	return render_template('downloads.html')

@app.route('/renames')
def renames():
	return render_template('renames.html')
