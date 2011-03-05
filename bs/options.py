# -*- coding: utf-8 -*-

import model

defaults = {
    'basepath': '/tmp',
    'episodesRegexps': '[sS]([0-9]+)[eE]([0-9]+)|||([0-9]+)[xX]([0-9]+)',
    'betaseries.apikey': 'c4fa190ce08c',
    'flask.host': '127.0.0.1',
    'flask.port': 5000,
    'flask.debug': True,
    'download.torrent.folder': '/tmp',
    'download.torrent.watch': '/tmp',
}


def getOption(key):
    if model.Session.query( model.Option ).count() == 0:
        for opt in defaults:
            model.Session.add( model.Option(key=opt, value=defaults[opt]) )
        model.Session.flush()
        model.Session.commit()

    try:
        return model.Session.query( model.Option ).filter_by( key=key ).one().value
    except:
        if key in defaults:
            model.Session.add( model.Option(key=key, value=defaults[key]) )
            model.Session.flush()
            model.Session.commit()
            
            return defaults[key]
    
    return None