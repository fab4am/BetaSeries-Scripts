
from urllib import urlencode
from urllib2 import urlopen
import simplejson
import os

class BetaSeriesException(Exception):
    pass

class DBBetaSeriesException(Exception):
    pass
class VariableBetaSeriesException(Exception):
    pass
class UserBetaSeriesException(Exception):
    pass
class APIBetaSeriesException(Exception):
    pass

class API(object):
    
    def __init__(self, apikey, url='http://api.betaseries.com/', format='json'):
        self.apikey = apikey
        self.url = url
        self.format = format
        self.auth = False
    
    def __getContent(self, url):
        print "Fetching : %s" % url
        ret = None
        if self.format == 'json':
            ret = simplejson.loads(urlopen(url).read())
        
        if ret is None:
            raise BetaSeriesException('No results found !')
        
        if int(ret['root']['code']) == 0:
            error = ret['root']['errors']['error']
            msg = 'Code %s, Message %s' % (error['code'], error['content'])
            exc = [BetaSeriesException(msg), APIBetaSeriesException(msg), UserBetaSeriesException(msg), VariableBetaSeriesException(msg), DBBetaSeriesException(msg)]
            raise exc[int(str(error['code'])[0])]
        
        return ret['root']
    
    def __getUrl(self, action, params = None):
        if params is None:
            params = {}
        
        params['key'] = self.apikey
        
        url = os.path.join(self.url, action)
        url = "%s.%s" % (url, self.format)
        if params is not None:
            url = "%s?%s" % (url, urlencode(params))
        return url
    
    def resultsToArray(self, results, key):
        #print results
        if key[-1] != 's':
            return results[key]
            
        ret = []
        for k in range(len(results[key].keys())):
            k = unicode(k)
            ret.append(results[key][k])
        return ret
    
    def __call(self, action, params, key):
        return self.resultsToArray(self.__getContent(self.__getUrl(action, params)), key)
        
    def status(self):
        return self.__getContent(self.__getUrl('status'))
        
    def search(self, text):
        return self.__call('shows/search', {'title': text}, 'shows')
        
    def showDetails(self, show_id):
        return self.__call('shows/display/%s' % show_id, {}, 'show')
        
    def episodeDetails(self, show_id, season = None, episode = None):
        params = {}
        if season is not None:
            params['season'] = int(season)
            if episode is not None:
                params['episode'] = int(episode)
                
        return self.__call('shows/episodes/%s' % show_id, params, 'seasons')
        
    def planningMember(self, member = None, unseen=False):
        if member is None and not self.auth:
            raise BetaSeriesException('Provide either member or credentials')
        
        planning = {}
        if member is not None:
            params = {}
            if unseen:
                params['view'] = 'unseen'
            planning = self.__getContent(self.__getUrl('planning/member/%s' % member, params))['planning']
        else:
            planning = self.__getContent(self.__getUrl('planning/member'))['planning']
        
        return planning
    
if __name__ == '__main__':
    api = API('c4fa190ce08c')
    planning = api.planningMember('PiTiLeZarD', unseen=True)

    retplanning = []
    for key in range(len(planning.keys())):
        key = unicode(key)
        retplanning.append("%s %s %s" % (planning[key]['show'], planning[key]['number'], planning[key]['title']))
    
    print retplanning