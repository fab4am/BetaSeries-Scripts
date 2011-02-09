# -*- coding: utf-8 -*-

import os
from betaseries import API
from options import getOption
from model import Session, Serie, Season, Episode

api = API(getOption('betaseries.apikey'))

def updateDB():
    
    for serie in Session.query( Serie ).all():
        if serie.bs_id is None or serie.bs_id.startswith('!!'):
            results = api.search(serie.path)
            if len(results) == 1:
                serie.bs_id = results[0]['url']
                serie.name = results[0]['title']
            elif serie.bs_id is not None and serie.bs_id.startswith('!!'):
                results = filter(lambda data: data['url'] == serie.bs_id[2:], results)
                assert(1 == len(results))
                serie.bs_id = results[0]['url']
                serie.name = results[0]['title']
            elif len(results) > 1:
                serie.bs_id = '??%s' % ",".join([t['url'] for t in results])
            else:
                serie.bs_id = '??'
        
        if serie.bs_id is not None and not serie.bs_id.startswith('!!') and not serie.bs_id.startswith('??'):
            details = api.episodeDetails(serie.bs_id)
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
                
                for episode_bs in api.resultsToArray(season_bs, 'episodes'):
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
                    
    Session.commit()
    
if __name__ == '__main__':
    updateDB()
            