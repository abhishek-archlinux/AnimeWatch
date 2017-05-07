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

import sys  
import re
import time
import os
import calendar
import weakref
from bs4 import BeautifulSoup
from datetime import datetime
import pycurl
import subprocess
from io import StringIO,BytesIO
from PyQt5 import QtCore, QtGui,QtNetwork,QtWidgets,QtWebEngineWidgets,QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtNetwork import QNetworkAccessManager
from player_functions import ccurl



class BrowseUrl(QWebEngineView):
	
	def __init__(self,url,quality,c,end_point=None,get_cookie=None,domain_name=None):
		super(BrowseUrl, self).__init__()
		#QtWidgets.__init__()
		self.url = url
		self.add_cookie = True
		self.quality = quality
		self.media_val = ''
		self.cnt = 0
		self.cookie_file = c
		if end_point:
			self.end_pt = end_point
		else:
			self.end_pt = 'cf_clearance'
		if get_cookie:
			self.get_cookie = 'true'
		else:
			self.get_cookie = 'false'
		if domain_name:
			self.domain_name = domain_name
		else:
			self.domain_name= 'None'
		self.path_val = ''
		j = 0
		print(sys.path)
		new_path = [i for i in sys.path]
		new_path.reverse()
		print(new_path)
		for i in new_path:
			if j == 0:
				self.path_val = i
			else:
				self.path_val = self.path_val + '::' + i
			j = j+1
		self.Browse(self.url)
		
	def Browse(self,url):
		hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		html = ''
		home1 = os.path.expanduser("~")
		
		BASEDIR,BASEFILE = os.path.split(os.path.abspath(__file__))
		
		if 'AnimeWatch' in BASEDIR:
			enginePath = os.path.join(home1,'.config','AnimeWatch','src','Plugins','headlessEngine.py')
		elif 'kawaii-player' in BASEDIR:
			enginePath = os.path.join(home1,'.config','kawaii-player','src','Plugins','headlessEngine.py')
		tmp_dir,new_c = os.path.split(self.cookie_file)
		
		content = ccurl(url+'#-b#'+self.cookie_file)
		if 'checking_browser' in content or self.get_cookie == 'true':
			if os.path.exists(self.cookie_file):
				os.remove(self.cookie_file)
			if os.name == 'posix':
				print('--checking__browser-----57--')
				print(enginePath,url,self.quality,self.cookie_file)
				p = subprocess.Popen(['python3','-B',enginePath,url,self.quality,
						self.cookie_file,self.end_pt,self.get_cookie,self.domain_name,self.path_val])
			else:
				p = subprocess.Popen(['python','-B',enginePath,url,self.quality,
						self.cookie_file,self.end_pt,self.get_cookie,self.domain_name,self.path_val],shell=True)
			
			cnt = 0
			
			lnk_file = os.path.join(tmp_dir,'lnk.txt')
			if os.path.exists(lnk_file):
				os.remove(lnk_file)
			print(lnk_file,'--lnk--file--')
			while(not os.path.exists(self.cookie_file) and cnt < 20):
				print(cnt)
				print('wait Clouflare ')
				time.sleep(1)
				cnt = cnt+1
			p.kill()
			if 'kissasian' in url or 'kimcartoon' in url:
				if 'kissasian' in url:
					str3 = '\nkissasian.com	FALSE	/	FALSE	0		__test'
				else:
					str3 = '\nkimcartoon.me	FALSE	/	FALSE	0		__test'
				f = open(self.cookie_file,'a')
				f.write(str3)
				f.close()
			if ('id=' in url) and os.path.exists(self.cookie_file) and ('kimcartoon' in url or 'kissasian' in url or 'kissanime' in url):
				if os.name == 'posix':
					p = subprocess.Popen(['python3','-B',enginePath,url,self.quality,
							self.cookie_file,self.end_pt,self.get_cookie,self.domain_name,self.path_val])
				else:
					p = subprocess.Popen(['python','-B',enginePath,url,self.quality,
							self.cookie_file,self.end_pt,self.get_cookie,self.domain_name,self.path_val],shell=True)
				cnt = 0
				while(not os.path.exists(lnk_file) and cnt < 60):
					print(cnt)
					print('wait Clouflare ')
					time.sleep(1)
					cnt = cnt+1
			p.kill()
		else:
			if ('id=' in url) and os.path.exists(self.cookie_file) and ('kimcartoon' in url or 'kissasian' in url or 'kissanime' in url):
				lnk_file = os.path.join(tmp_dir,'lnk.txt')
				if os.path.exists(lnk_file):
					os.remove(lnk_file)
				print(lnk_file,'--lnk--file--')
				if os.name == 'posix':
					p = subprocess.Popen(['python3','-B',enginePath,url,self.quality,
							self.cookie_file,self.end_pt,self.get_cookie,self.domain_name,self.path_val])
				else:
					p = subprocess.Popen(['python','-B',enginePath,url,self.quality,
							self.cookie_file,self.end_pt,self.get_cookie,self.domain_name,self.path_val],shell=True)
				cnt = 0
				file_path = os.path.join(tmp_dir,'tmp_cookie')
				while(not os.path.exists(lnk_file) and cnt < 60):
					print(cnt)
					print('wait Clouflare ')
					time.sleep(1)
					cnt = cnt+1
				p.kill()
			else:
				f = open(self.cookie_file,'w')
				f.close()
		


