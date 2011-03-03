# -*- coding: utf-8 -*-

options = {
    'basepath': '/Volumes/Drobo/Movies/Series/',
    'dburi': 'sqlite:///bs.db',
    'dbverbose': False,
    'episodesRegexps': [r'[sS][0-9]+[eE]([0-9]+)', r'[0-9]+[xX]([0-9]+)'],
    'betaseries.apikey': 'c4fa190ce08c',
    'flask.host': '127.0.0.1',
    'flask.port': 5000,
    'flask.debug': True,
}

def getOption(key):
    """ One day in database and such """
    if key not in options:
        return None
    return options[key]
