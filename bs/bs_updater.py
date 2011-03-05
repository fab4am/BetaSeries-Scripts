# -*- coding: utf-8 -*-

import os
from betaseries import API
from options import getOption
from model import Session, Serie, Season, Episode


class BetaseriesSyncer:
    
    def __init__(self):
        self.api = API(getOption('betaseries.apikey'))
        self.details = None
    
    def _setDetails(self, serie):
        if self.details:
            return
            
        if serie.bs_id is None or serie.bs_id.startswith('!!'):
            results = self.api.search(serie.path)
            if len(results) > 1:
                if serie.bs_id is not None:
                    results = filter(lambda data: data['url'] == serie.bs_id[2:], results)
                    assert(1 == len(results))
                    serie.bs_id = results[0]['url']
                    serie.name = results[0]['title']
                else:
                    serie.bs_id = '??%s' % ",".join([t['url'] for t in results])
            elif len(results) == 1:
                serie.bs_id = results[0]['url']
                serie.name = results[0]['title']
            else:
                serie.bs_id = '??'
                
        if serie.bs_id is None or serie.bs_id.startswith('??'):
            raise Exception("Can't establish a link between DB and BetaSeries")

        self.details = self.api.episodeDetails(serie.bs_id)
        

    def syncAll(self):
        for serie in Session.query( Serie ).all():
            self.syncSerie(serie)

    def syncSerie(self, serie):
        self._setDetails(serie)
        
        for season_bs in details:
            season_num = 'S%s' % str(season_bs['number']).zfill(2)
            
            season = filter(lambda season: season.num == season_num, serie.seasons)
            if len(season) == 0:
                season = Season(num=season_num)
                Session.add(season)
                serie.seasons.append(season)
            else:
                assert(len(season) == 1)
                season = season[0]
            
            self.syncSeason(serie, season)
            
            
    def syncSeason(self, serie, season):
        self._setDetails(serie)

        details = self.details
        season_bs = filter(lambda s: int(s['number']) == int(season.num[1:]), self.details)
        assert(len(season_bs) == 1)
        season_bs = season_bs[0]
        
        for episode_bs in self.api.resultsToArray(season_bs, 'episodes'):
            episode_num = episode_bs['number']
            
            episode = filter(lambda episode: episode.num == episode_num, season.episodes)
            if len(episode) == 0:
                episode = Episode(num=episode_num)
                Session.add(episode)
                season.episodes.append(episode)
            else:
                assert(len(episode) == 1)
                episode = episode[0]
                
            episode.name = name=episode_bs['title']
            

    def syncEpisode(self, serie, season, episode):
        raise Exception('Not implemented')

