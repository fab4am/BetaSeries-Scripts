# -*- coding: utf-8 -*-
"""
The aim of this module is to feed or complete the database with the filesystem as a base
"""

from options import getOption
from model import Session, Serie, Season, Episode
from glob import glob
import os
from tools import getSeasonNumFromFoldername, getEpisodeNumFromFilename


class FileSystemSyncer:
    
    def __init__(self):
        self.basepath = getOption('basepath')
    
    def syncAll(self):
        series = glob(os.path.join( self.basepath, '*' ))
        series = filter(lambda serie: os.path.isdir(serie), series)
        
        for serie in [os.path.basename(s) for s in series]:
            self.syncSerie(serie)
        
    def syncSerie(self, serie):
        qry = Session.query( Serie ).filter_by(path=serie)
        if qry.count() == 0:
            Session.add(Serie(path=serie))
        serie = qry.one()
    
        if serie.seasons is None:
            serie.seasons = []
    
        seasons = glob(os.path.join( self.basepath, serie.path, '*'))
        seasons = filter(lambda season: os.path.isdir(season), seasons)
    
        for season in [os.path.basename(s) for s in seasons]:
            try:
                self.syncSeason(serie.path, season)
            except:
                pass
    
    def syncSeason(self, serie, season):
        qry = Session.query( Serie ).filter_by(path=serie)
        if qry.count() == 0:
            raise Exception('No serie linked to %s/%s' % (serie, saison))
        serie = qry.one()
        
        path = season
        num = getSeasonNumFromFoldername(season)

        if num is None:
            raise Exception('This is not a season (%s)' % season)

        season = filter(lambda season: season.num == num, serie.seasons)
        if len(season) == 0:
            season = Season(num=num, path=path)
            Session.add(season)
            serie.seasons.append(season)
        else:
            assert( 1 == len(season))
            season = season[0] 
            season.num = num
            season.path = path
    
        episodes = glob(os.path.join( self.basepath, serie.path, season.path, '*'))
        episodes = filter(lambda episode: os.path.isfile(episode), episodes)

        for episode in [os.path.basename(e) for e in episodes]:
            try:
                self.syncEpisode(serie.path, season.path, episode)
            except:
                pass
    
    def syncEpisode(self, serie, season, episode):
        qry = Session.query( Season ).filter_by(path=season).join( Serie ).filter_by(path=serie)
        if qry.count() == 0:
            raise Exception('No season linked to %s/%s/%s' % (serie, saison, episode))
        season = qry.one()
        
        path = episode
        ext = os.path.splitext(episode)[1][1:].lower()
        if ext not in ['avi', 'mkv', 'mov', 'mpg']:
            raise Exception('Not supported extention %s' % ext)
        
        num = getEpisodeNumFromFilename(os.path.basename(episode))
    
        episode = filter(lambda episode: episode.num == num, season.episodes)
        if len(episode) == 0:
            episode = Episode(num=num, path=path)
            Session.add(episode)
            season.episodes.append(episode)
        else:
            assert( len(episode) == 1 )
            episode = episode[0]
            episode.num = num
            episode.path = path
