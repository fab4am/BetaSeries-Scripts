# -*- coding: utf-8 -*-

from betaseries import API
from options import getOption
from model import Session, Serie, Season, Episode, Rename

api = API(getOption('betaseries.apikey'))

def updateDB():
    
    def updateSerie(serie, result):
        serie.bs_id = result['url']
        if serie.name != result['title']:
            try:
                Session.add(Rename(categ='serie', source=serie.name, destination=result['title']))
            except:
                pass
        
    
    for serie in Session.query( Serie ).all():
        if serie.bs_id is None or serie.bs_id.startswith('!!'):
            results = api.search(serie.name)
            if len(results) == 1:
                updateSerie(serie, results[0])
            elif serie.bs_id is not None and serie.bs_id.startswith('!!'):
                results = filter(lambda data: data['url'] == serie.bs_id[2:], results)
                assert(1 == len(results))
                updateSerie(serie, results[0])
            elif len(results) > 1:
                serie.bs_id = '??%s' % ",".join([t['url'] for t in results])
            else:
                serie.bs_id = '??'
        
        # TODO check seasons and episodes

    Session.commit()
    
if __name__ == '__main__':
    updateDB()
            