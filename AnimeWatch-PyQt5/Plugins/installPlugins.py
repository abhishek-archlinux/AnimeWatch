"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import shutil


def copy_files(home_dir):
	nHome = os.path.join(home_dir,'src')
	pluginDir = os.path.join(nHome,'Plugins')
	
	if not os.path.exists(home_dir):
		os.makedirs(home_dir)

	if not os.path.exists(nHome):
		os.makedirs(nHome)

	if not os.path.exists(pluginDir):
		os.makedirs(pluginDir)


	if os.path.exists(pluginDir):
		n = os.listdir(pluginDir)
		for i in n:
			k = os.path.join(pluginDir,i)
			if os.path.isfile(k):
				os.remove(k)

	cwd = os.getcwd()
	m = os.listdir(cwd)

	for i in m:
		k = os.path.join(cwd,i)
		if i.lower() != "installplugins.py" and os.path.isfile(k):
			shutil.copy(k,pluginDir)
	
	print ("Plugin SuccessFully Installed in Directory "+pluginDir)

home = os.path.expanduser("~")
a_home = os.path.join(home,".config","AnimeWatch")
k_home = os.path.join(home,".config","kawaii-player")

if os.path.exists(a_home):
	copy_files(a_home)

if os.path.exists(k_home):
	copy_files(k_home)




