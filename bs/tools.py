# -*- coding: utf-8 -*-

import re
from options import getOption

def getSeasonNumFromFoldername(foldername):
	try:
		return 'S%s' % re.search(r'([0-9])+', season).group(1).zfill(2)
	except:
		return None

def getEpisodeNumFromFilename(filename):
	d = None
	for regexp in getOption('episodesRegexps').split('|||'):
	    p = re.compile(regexp)
		if p.match(filename):
			d = dict(zip( ('s', 'e'), [ t.zfill(2) for t in p.search(filename).groups()] )
	
	if d is not None:
		return "S%sE%s" % d.values()

	return None


if __name__ == '__main__':
	print getEpisodeNumFromFilename('Fairly.Legal.S01E01.Pilot.HDTV.XviD-FQM.avi')