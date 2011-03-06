# -*- coding: utf-8 -*-

import  os

import bs.model as model
import bs.downloads as downloadsTools
from bs.filesystem import FileSystemSyncer
from bs.bs_updater import BetaseriesSyncer

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('menu.html')

@app.route('/series')
def series():
    series = model.Session.query( model.Serie ).all()
    return render_template('series.html', series=series)

@app.route('/serie/<id>')
def serie(id):
    serie = model.Session.query(model.Serie).get(id)
    return render_template('serie.html', serie=serie)

@app.route('/season/<int:id_serie>/<season_num>')
def season(id_serie, season_num):
    serie = model.Session.query(model.Serie).get(id_serie)
    seasons = filter(lambda item: item.num == season_num, serie.seasons)
    assert(len(seasons) == 1)
    return render_template('season.html', serie=serie, season=seasons[0])
    
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
@app.route('/downloads/<episode_id>')
def downloads(episode_id=None):
    if episode_id:
        if episode_id == 'all':
            downloadsTools.downloadAll()
        else:
            episode = model.Session.query( model.Episode ).join(model.Download ).get( episode_id )
            downloadsTools.downloadEpisode(episode)
        model.Session.flush()
        model.Session.commit()
    
    downloading = model.Session.query( model.Download ).filter_by(finished=False).all()
    return render_template('downloads.html', downloads=downloadsTools.getPendingDownloads(), downloading=downloading)

@app.route('/renames')
def renames():
    return render_template('renames.html')

@app.route('/options', methods=['GET', 'POST'])
def options():
    if request.method == 'POST':
        for option in request.form.items():
            name, value = option
            if name.startswith('option_'):
                id_option = int(name.split('_')[1])
                model.Session.query( model.Option ).get(id_option).value = value
        
        model.Session.flush()
        model.Session.commit()
        
    options = model.Session.query( model.Option ).all()
    return render_template('options.html', options=options)

@app.route('/sync/<kind>')
@app.route('/sync/<kind>/<int:serie_id>')
@app.route('/sync/<kind>/<int:serie_id>/<int:season_id>')
@app.route('/sync/<kind>/<int:serie_id>/<int:season_id>/<int:episode_id>')
def sync(kind, serie_id=None, season_id=None, episode_id=None):
    if kind == 'disk':
        
        syncer = FileSystemSyncer()
        if episode_id is not None:
            episode = model.Session.query( model.Episode ).get(episode_id)
            syncer.syncEpisode(episode.season.serie.path, episode.season.path, episode.path)
        elif season_id is not None:
            season = model.Session.query( model.Season ).get(season_id)
            syncer.syncSeason(season.serie.path, season.path)
        elif serie_id is not None:
            serie = model.Session.query( model.Serie ).get(serie_id)
            syncer.syncSerie(serie.path)
        else:
            syncer.syncAll()
            
    if kind == 'bs':
        
        syncer = BetaseriesSyncer()
        if serie_id and season_id:
            season = model.Session.query( model.Season ).get(season_id)
            syncer.syncSeason(season.serie, season)
    
    model.Session.commit()
    return 'ok'