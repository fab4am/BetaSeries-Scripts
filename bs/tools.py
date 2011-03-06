# -*- coding: utf-8 -*-

import re, os
from options import getOption

def getSeasonNumFromFoldername(foldername):
    try:
        return 'S%s' % re.search(r'([0-9])+', foldername).group(1).zfill(2)
    except:
        return None

def getEpisodeNumFromFilename(filename):
    d = None
    for regexp in getOption('episodesRegexps').split('|||'):
        p = re.compile('.*%s.*' % regexp)
        if p.match(filename):
            d = dict(zip( ('s', 'e'), [ t.zfill(2) for t in p.search(filename).groups()] ) )
    
    if d is not None:
        return "S%(s)sE%(e)s" % d

    return None

def rename(episode):
    return "%s %s%s" % (episode.num, episode.name, os.path.splitext(episode.path)[1])