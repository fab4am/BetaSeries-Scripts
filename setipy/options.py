# -*- coding: utf-8 -*-

options = {
    'basepath': '/Volumes/Drobo/Movies/Series/',
    'dburi': 'sqlite:///setipy.db',
    'dbverbose': False,
    'episodesRegexps': [r'[sS][0-9]+[eE]([0-9]+)', r'[0-9]+[xX]([0-9]+)'],
    'betaseries.apikey': 'c4fa190ce08c'
}

def getOption(key):
    """ One day in database and such """
    if key not in options:
        return None
    return options[key]
