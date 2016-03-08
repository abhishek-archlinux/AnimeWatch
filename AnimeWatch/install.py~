"""
This file is part of AnimeWatch.

AnimeWatch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

AnimeWatch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with AnimeWatch.  If not, see <http://www.gnu.org/licenses/>.



"""

import os
from os.path import expanduser
import shutil
import subprocess
import platform
import sys
home1 = expanduser("~")
home = home1+"/.config/AnimeWatch"
nHome = home+'/src' 
pluginDir = nHome+'/Plugins'
if not os.path.exists(home):
	os.makedirs(home)

if not os.path.exists(nHome):
	os.makedirs(nHome)

if not os.path.exists(pluginDir):
	os.makedirs(pluginDir)


if os.path.exists(nHome):
	n = os.listdir(nHome)
	for i in n:
		k = nHome+'/'+i
		if os.path.isfile(k):
			os.remove(k)





cwd = os.getcwd()
m = os.listdir(cwd)
for i in m:
	k = cwd+'/'+i
	if os.path.isfile(k) and i != "install.py":
		shutil.copy(k,nHome)
	elif os.path.isdir(k) and i == "Plugins":
		p_dir_list = os.listdir(k)
		for j in p_dir_list:
			q = k+'/'+j
			if os.path.isfile(q) and j != "installPlugins.py":
				shutil.copy(q,pluginDir)

f = open('AnimeWatch.desktop','r')
lines = f.readlines()
f.close()
os_name = platform.platform()

os_name = os_name.lower()
print(os_name)
if 'arch' in os_name:
	lines[5]="Exec=python "+nHome+'/animeWatch.py '+'%u'+'\n'
else:
	lines[5]="Exec=python3 "+nHome+'/animeWatch.py '+'%u'+'\n'
f = open(home+'/AnimeWatch.desktop','w')
for i in lines:
	f.write(i)
f.close()

picn = home+'/default.jpg'
if not os.path.exists(picn):
	shutil.copy('default.jpg',home+'/default.jpg')
	
dest_file = '/usr/share/applications/AnimeWatch.desktop'
print("Please Give Permission to copy AnimeWatch.desktop file to /usr/share/applications/"+'\n')
print("If you don't want to give permission then press 'ctrl+c' to cancel and manually copy '"+home+ "/AnimeWatch.desktop' to the directory '/usr/share/applications/'"+' For creating Application Launcher in The Menu'+'\n' )
subprocess.call(['sudo','cp',home+'/AnimeWatch.desktop',dest_file])
print ("Installed Successfully!")
