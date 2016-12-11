import sys  
import re
import urllib
import time
import os
import os.path
import sys
import calendar
import weakref
import threading
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
	
	def __init__(self,url,quality,c):
		super(BrowseUrl, self).__init__()
		#QtWidgets.__init__()
		self.url = url
		self.add_cookie = True
		self.quality = quality
		self.media_val = ''
		self.cnt = 0
		self.cookie_file = c
		self.Browse(self.url)
		
	def Browse(self,url):
		hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		html = ''
		#url = sys.argv[1]	
		home1 = os.path.expanduser("~")
		#home1 = "/usr/local/share"
		enginePath = os.path.join(home1,'.config','AnimeWatch','src','Plugins','headlessEngine.py')
		tmp_dir,new_c = os.path.split(self.cookie_file)
		
		if 'animeget' in url or 'masterani' in url or 'animeplace' in url or 'moetube' in url or 'nyaa' in url:
			content = ccurl(url)
		else:
			content = 'checking_browser'
		#web = BrowseUrl(url,quality)
		if 'checking_browser' in content:
			if os.name == 'posix':
				p = subprocess.Popen(['python3','-B',enginePath,url,self.quality,self.cookie_file])
			else:
				p = subprocess.Popen(['python','-B',enginePath,url,self.quality,self.cookie_file],shell=True)
			
			cnt = 0
			
			lnk_file = os.path.join(tmp_dir,'lnk.txt')
			if os.path.exists(lnk_file):
				os.remove(lnk_file)
			#cloud_cookie = '/tmp/AnimeWatch/cloud_cookie.txt'
			while(not os.path.exists(self.cookie_file) and cnt < 20):
				print(cnt)
				print('wait Clouflare ')
				time.sleep(1)
				cnt = cnt+1
			if 'kissasian' in url or 'kisscartoon' in url:
				if 'kissasian' in url:
					str3 = '\nkissasian.com	FALSE	/	FALSE	0		__test'
				else:
					str3 = '\nkisscartoon.me	FALSE	/	FALSE	0		__test'
				f = open(self.cookie_file,'a')
				f.write(str3)
				f.close()
			if ('id=' in url) and os.path.exists(self.cookie_file) and ('kisscartoon' in url or 'kissasian' in url):
				cnt = 0
				file_path = os.path.join(tmp_dir,'tmp_cookie')
				while(not os.path.exists(lnk_file) and cnt < 30):
					if os.path.exists(file_path):
						os.remove(file_path)
						if os.name == 'posix':
							p = subprocess.Popen(['python3','-B',enginePath,url,self.quality,self.cookie_file])
						else:
							p = subprocess.Popen(['python','-B',enginePath,url,self.quality,self.cookie_file],shell=True)
					print(cnt)
					print('wait Clouflare ')
					time.sleep(1)
					cnt = cnt+1
					
				
			p.kill()
		else:
			f = open(self.cookie_file,'w')
			f.close()
		


