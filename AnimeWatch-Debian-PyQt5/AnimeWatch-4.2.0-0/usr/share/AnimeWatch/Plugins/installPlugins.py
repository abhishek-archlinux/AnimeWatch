import os
from os.path import expanduser
import shutil
import subprocess
home1 = expanduser("~")
#home1 = "/usr/local/share"
home = home1+"/.config/AnimeWatch"
nHome = home+'/src' 
pluginDir = nHome+'/Plugins'
if not os.path.exists(home):
	os.makedirs(home)

if not os.path.exists(nHome):
	os.makedirs(nHome)

if not os.path.exists(pluginDir):
	os.makedirs(pluginDir)


if os.path.exists(pluginDir):
	n = os.listdir(pluginDir)
	for i in n:
		k = pluginDir+'/'+i
		if os.path.isfile(k):
			os.remove(k)





cwd = os.getcwd()
m = os.listdir(cwd)

for i in m:
	k = cwd+'/'+i
	if i != "installPlugins.py" and os.path.isfile(k):
		shutil.copy(k,pluginDir)
	



print ("Plugin SuccessFully Installed in Directory "+pluginDir)
