"""
HOW TO USE :
- modify the folder variable (just under this text) to point on the series folder
- choose a folder name in this folder (supposed to be a serie)
- $ python cleanFS.py 'My Serie'
- check on "No can do" and fix those names
- when your satisfied with the output : 
- $ python cleanFS.py 'My Serie' false

"""
folder = '/media/docs/Video/Series/'


import os, re, sys, shutil
from glob import glob
import betaseries



serie = None
simulate = True

args = sys.argv
if len(args) >= 1 and args[0] == __file__:
    args = args[1:]
    
if len(args) == 0:
    raise Exception("Give me more params")
    
serie = args[0]
if len(args) > 1:
    simulate = False

if not os.path.isdir(os.path.join(folder, serie)):
    raise Exception("Hmmm %s not found under %s" % (serie, folder))

api = betaseries.API('c4fa190ce08c')
print ">>> Doing %s"%serie
cmds = []
mkdir = []

data = api.search(serie)
if len(data) == 1:
    if data[0]['title'] != serie:
        cmds.append((os.path.join(folder, serie), os.path.join(folder, data[0]['title'])))
    serie_url = data[0]['url']
else:
    print "Not only one result found :"
    for result in data:
        print " - %s (type '%s' to choose)" % (result['title'], result['url'])
    sys.stdout.flush()
    serie_url = raw_input("Which one is it? ")
    data = api.showDetails(serie_url)
    if data['title'] != serie:
        cmds.append((os.path.join(folder, serie), os.path.join(folder, data['title'])))

details = []
for season_d in api.episodeDetails(serie_url):
    details.append(api.resultsToArray(season_d, 'episodes'))

for season in [f[f.rfind('/') + 1:] for f in glob(os.path.join(folder, serie, '*'))]:
    print "++ Enterring %s" % season
    s_num = 0
    try:
        s_num = int(re.search(r'([0-9])+', season).group(1))
    except:
        print "/!\\ Can no do !"
        continue
    
    s_name = "%s_S%.2d" % (serie, s_num)
    if s_name != season:
	if os.path.isdir(os.path.join(folder, serie, season)) == True:
            cmds.append((os.path.join(folder, serie, season), os.path.join(folder, serie, s_name)))
	else:
	    seriedir = os.path.join(folder, serie, s_name)
	    if seriedir not in mkdir:
    	        mkdir.append(seriedir)
            cmds.append((os.path.join(folder, serie, season), os.path.join(seriedir, season)))
	    
	    
    
    episodes = []
    for ext in ['avi', 'mkv', 'mp4', 'mpg']:
        episodes += [f[f.rfind('/') + 1:] for f in glob(os.path.join(folder, serie, season, '*.%s'%ext))]
        
    for episode in episodes:
        print "- Checking %s" % episode
        e_num = 0
        try:
            e_num = int(re.search(r'[sS][0-9]+\.?[eE]([0-9]+)', episode).group(1))
        except:
            try:
                e_num = int(re.search(r'[0-9]+[xX]([0-9]+)', episode).group(1))
            except:
		try:
 		    e_num = int(re.search(r'Episode ([0-9]+)', episode).group(1))
		except:
		    try:
 		        e_num = int(re.search(r'[0-9][0-9]([0-9][0-9])', episode).group(1))
		    except:
			try:
			    e_num = int(re.search(r'[0-9]([0-9][0-9])', episode).group(1))
			except:
    		            print "Couldn't rename or identify file %s" % episode
			    continue

	if re.search(r'VOSTFR', episode, re.I):
		vost = 'VOSTFR.'
	else:
		vost = ''
        
        e_details = details[s_num - 1][e_num - 1]
        ext = episode[episode.rfind('.') + 1:]
        
	title = e_details['title'].replace('/',' ')
        e_name = "%s.%s.%s%s.%s" % (serie, e_details['number'], vost, title, ext)
        if e_name != episode:
	    current = os.path.join(folder, serie, season, episode)
	    new = os.path.join(folder, serie, season, e_name)
	    for cmd in cmds:
		if new == cmd[1]:
		    print "2 files are going to be renamed the same way, you're about to lose one of them, aborting."
		    print " - %s " % cmd[0]
		    print " - %s " % current
		    sys.exit(1)
		else:
		    continue
            cmds.append((current, new))
            if os.path.isfile(os.path.join(folder, serie, season, episode.replace(ext, 'srt'))):
                cmds.append((os.path.join(folder, serie, season, episode.replace(ext, 'srt')), os.path.join(folder, serie, season, e_name).replace(ext, 'srt')))
                
 
               
cmds.reverse()
mkdir.reverse()
if simulate:
    for path in mkdir:
        print "mkdir %s" % path
    for cmd in cmds:
        print "mv %s %s" % (cmd[0], cmd[1])
else:
    for path in mkdir:
        os.makedirs(path)
    for cmd in cmds:
	if os.path.isfile(cmd[1]) == False :
            shutil.move(cmd[0], cmd[1])
	else:
	    print "Couldn't rename %s as planned, %s already exists" % (cmd[0], cmd[1])
