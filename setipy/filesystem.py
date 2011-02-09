# -*- coding: utf-8 -*-
"""
The aim of this module is to feed or complete the database with the filesystem as a base
"""

from options import getOption
from model import Session, Serie, Season, Episode
from glob import glob
import os, re

def updateDB():
    basepath = getOption('basepath')

    series = glob(os.path.join( basepath, '*' ))
    series = filter(lambda serie: os.path.isdir(serie), series)
    for serie in [os.path.basename(s) for s in series]:
    
        qry = Session.query( Serie ).filter_by(path=serie)
        if qry.count() == 0:
            Session.add(Serie(path=serie))
        serie = qry.one()
    
        if serie.seasons is None:
            serie.seasons = []
    
        seasons = glob(os.path.join( basepath, serie.path, '*'))
        seasons = filter(lambda season: os.path.isdir(season), seasons)
    
        for season in [os.path.basename(s) for s in seasons]:
        
            path = season
            try:
                num = 'S%s' % re.search(r'([0-9])+', season).group(1).zfill(2)
            except:
                # unable to find a number ... it's probably another folder here
                continue
            season = filter(lambda season: season.num == num, serie.seasons)
            if len(season) == 0:
                season = Season(num=num, path=path)
                Session.add(season)
                serie.seasons.append(season)
            else:
                assert( 1 == len(season))
                season = season[0] 
        
            episodes = glob(os.path.join( basepath, serie.path, season.path, '*'))
            episodes = filter(lambda episode: os.path.isfile(episode), episodes)
            episodes = filter(lambda episode: os.path.splitext(episode)[1][1:].lower() in ['avi', 'mkv', 'mov', 'mpg'], episodes)
        
            for episode in [os.path.basename(e) for e in episodes]:
                path = episode
                num = None
                for regexp in getOption('episodesRegexps'):
                    if re.match(regexp, path):
                        num = re.search(regexp, path).group(1)
                if num is not None:
                    num = '%sE%s' % (season.num, num.zfill(2))
            
                episode = filter(lambda episode: episode.path == path, season.episodes)
                if len(episode) == 0:
                    episode = Episode(num=num, path=path)
                    Session.add(episode)
                    season.episodes.append(episode)
        
    Session.commit()

if __name__ == '__main__':
    updateDB()