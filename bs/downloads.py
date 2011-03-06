# -*- coding: utf-8 -*-

import model
import urllib2, urllib
import re, os
from options import getOption
from BeautifulSoup import BeautifulSoup

def getPendingDownloads():
    qry = model.Session.query( model.Episode ).filter_by( path=None, enabled=True )
    qry = qry.join(model.Season).filter_by( enabled=True )
    qry = qry.join(model.Serie).filter_by( enabled=True ).filter( model.Serie.name != None )
    qry = qry.filter( ~ model.Episode.downloads.any() )
    return qry.all()

def downloadAll():
    for episode in getPendingDownloads():
        downloadEpisode(episode)

def downloadEpisode(episode):
    search_text = "%s %s" % (episode.season.serie.name, episode.num)
    
    url = 'http://thepiratebay.org/search/%s/0/7/0' % urllib.quote(search_text)
    search = urllib2.urlopen( url ).read()
    torrents = BeautifulSoup(search).findAll('td')
    if len(torrents) > 1:
        torrent = torrents[1]
        link = BeautifulSoup("<html><body>%s</body></html>" % torrent).findAll('a')[1]
        link = re.search('href="(.*?)"', str(link)).group(1)
        
        if link.rstrip():
            download = model.Download()
            download.torrentFile = link
            download.episode = episode
        
            model.Session.add( download )
        
            fp = open( os.path.join( getOption('download.torrent.folder'), os.path.basename(link) ) , 'w')
            fp.write( urllib2.urlopen( link ).read() )
            fp.close()

if __name__ == '__main__':
    downloadAll()