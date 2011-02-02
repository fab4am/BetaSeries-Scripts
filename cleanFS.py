"""
- modify the folder variable (just under this text) to point on the series folder
- choose a folder name in this folder (supposed to be a serie)
- $ python cleanFS.py 'My Serie'
- check on "No can do" and fix those names
- when your satisfied with the output : 
- $ python cleanFS.py 'My Serie' false
"""
folder = '/Volumes/Drobo/Movies/Series/'


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

data = api.search(serie)
if len(data) == 1:
    if data[0]['title'] != serie:
        cmds.append((os.path.join(folder, serie), os.path.join(folder, data[0]['title'])))
else:
    print "Not only one result found :"
    print data
    sys.exit()

serie_url = data[0]['url']
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
    
    s_name = "Season_%s" % s_num
    if s_name != season:
        cmds.append((os.path.join(folder, serie, season), os.path.join(folder, serie, s_name)))
    
    episodes = []
    for ext in ['avi', 'mkv', 'mp4', 'mpg']:
        episodes += [f[f.rfind('/') + 1:] for f in glob(os.path.join(folder, serie, season, '*.%s'%ext))]
        
    for episode in episodes:
        print "- Checking %s" % episode
        e_num = 0
        try:
            e_num = int(re.search(r'[sS][0-9]+[eE]([0-9]+)', episode).group(1))
        except:
            try:
                e_num = int(re.search(r'[0-9]+[xX]([0-9]+)', episode).group(1))
            except:
                print "/!\\ Can no do !"
                continue
        
        e_details = details[s_num - 1][e_num - 1]
        ext = episode[episode.rfind('.') + 1:]
        
        e_name = "%s - %s.%s" % (e_details['number'], e_details['title'], ext)
        if e_name != episode:
            cmds.append((os.path.join(folder, serie, season, episode), os.path.join(folder, serie, season, e_name)))
            if os.path.isfile(os.path.join(folder, serie, season, episode.replace(ext, 'srt'))):
                cmds.append((os.path.join(folder, serie, season, episode.replace(ext, 'srt')), os.path.join(folder, serie, season, e_name).replace(ext, 'srt')))
                
                
            
cmds.reverse()
for cmd in cmds:
    if simulate:
        print "mv %s %s" % (cmd[0], cmd[1])
    else:
        shutil.move(cmd[0], cmd[1])