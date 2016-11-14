import sys  
#from PyQt5.QtGui import *  
#from PyQt5.QtCore import *  
#from PyQt5.QtWebEngineWidgets import *  
#from PyQt5.QtWebEngineCore import *  
import re
import urllib
import urllib3
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

def getContentUnicode(content):
		if isinstance(content,bytes):
			print("I'm byte")
			try:
				content = str((content).decode('utf-8'))
			except:
				content = str(content)
		else:
			print(type(content))
			content = str(content)
			print("I'm unicode")
		return content

def ccurl(url):
	global hdr
	hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
	print(url)
	c = pycurl.Curl()
	
	
	curl_opt = ''
	picn_op = ''
	rfr = ''
	nUrl = url
	cookie_file = ''
	if '#' in url:
		curl_opt = nUrl.split('#')[1]
		url = nUrl.split('#')[0]
		if curl_opt == '-o':
			picn_op = nUrl.split('#')[2]
		elif curl_opt == '-Ie':
			rfr = nUrl.split('#')[2]
		elif curl_opt == '-Icb' or curl_opt == '-bc' or curl_opt == '-b' or curl_opt == '-Ib':
			cookie_file = nUrl.split('#')[2]
	url = str(url)
	print(url,'----------url------')
	try:
		c.setopt(c.URL, url)
	except UnicodeEncodeError:
		c.setopt(c.URL, url.encode('utf-8'))
	storage = BytesIO()
	if curl_opt == '-o':
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.USERAGENT, hdr)
		f = open(picn_op,'wb')
		c.setopt(c.WRITEDATA, f)
		c.perform()
		c.close()
		f.close()
	else:
		if curl_opt == '-I':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.NOBODY, 1)
			c.setopt(c.HEADERFUNCTION, storage.write)
		elif curl_opt == '-Ie':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(pycurl.REFERER, rfr)
			c.setopt(c.NOBODY, 1)
			c.setopt(c.HEADERFUNCTION, storage.write)
		elif curl_opt == '-IA':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.NOBODY, 1)
			c.setopt(c.HEADERFUNCTION, storage.write)
		elif curl_opt == '-Icb':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.NOBODY, 1)
			c.setopt(c.HEADERFUNCTION, storage.write)
			if os.path.exists(cookie_file):
				os.remove(cookie_file)
			c.setopt(c.COOKIEJAR,cookie_file)
			c.setopt(c.COOKIEFILE,cookie_file)
		elif curl_opt == '-Ib':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.NOBODY, 1)
			c.setopt(c.HEADERFUNCTION, storage.write)
			c.setopt(c.COOKIEFILE,cookie_file)
		elif curl_opt == '-bc':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
			c.setopt(c.COOKIEJAR,cookie_file)
			c.setopt(c.COOKIEFILE,cookie_file)
		elif curl_opt == '-b':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
			c.setopt(c.COOKIEFILE,cookie_file)
		elif curl_opt == '-L':
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
		else:
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
		c.perform()
		c.close()
		content = storage.getvalue()
		content = getContentUnicode(content)
		return content


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
			try:
				p = subprocess.Popen(['python3','-B',enginePath,url,self.quality,self.cookie_file])
			except:
				p = subprocess.Popen(['python','-B',enginePath,url,self.quality,self.cookie_file])
			
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
			if 'kissasian' in url:
				str3 = '\nkissasian.com	FALSE	/	FALSE	0		__test'
				f = open(self.cookie_file,'a')
				f.write(str3)
				f.close()
			if ('id=' in url) and os.path.exists(self.cookie_file) and ('kisscartoon' in url or 'kissasian' in url):
				cnt = 0
				file_path = os.path.join(tmp_dir,'tmp_cookie')
				while(not os.path.exists(lnk_file) and cnt < 30):
					if os.path.exists(file_path):
						os.remove(file_path)
						try:
							p = subprocess.Popen(['python3','-B',enginePath,url,self.quality,self.cookie_file])
						except:
							p = subprocess.Popen(['python','-B',enginePath,url,self.quality,self.cookie_file])
					print(cnt)
					print('wait Clouflare ')
					time.sleep(1)
					cnt = cnt+1
					
				
			p.kill()
		else:
			f = open(self.cookie_file,'w')
			f.close()
		


