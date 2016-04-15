import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  
import re
import urllib
import urllib3
import time
import requests
import os
import os.path
import sys
import calendar
import weakref
from datetime import datetime
from PyQt4 import QtCore, QtGui,QtNetwork,QtWebKit

from PyQt4.QtNetwork import QNetworkAccessManager

class NetWorkManager(QNetworkAccessManager):
	def __init__(self):
		super(NetWorkManager, self).__init__()
   
	def createRequest(self, op, request, device = None ):
		global lst
		try:
			path = str(request.url().path())
		except UnicodeEncodeError:
			pass
		lower_case = path.lower()
		#lst = tuple(open("easylist.txt", 'r'))
		lst = ["doubleclick.net" ,"ads",'.jpg','redirector','itag=','.png','.gif','.css','google','facebook','.aspx',r"http[^'].mp4",r"http[^'].flv", r"||youtube-nocookie.com/gen_204?", r"youtube.com###watch-branded-actions", "imagemapurl","b.scorecardresearch.com","rightstuff.com","scarywater.net","popup.js","banner.htm","_tribalfusion","||n4403ad.doubleclick.net^$third-party",".googlesyndication.com","graphics.js","fonts.googleapis.com/css","s0.2mdn.net","server.cpmstar.com","||banzai/banner.$subdocument","@@||anime-source.com^$document","google","/pagead2.","frugal.gif","jriver_banner.png","show_ads.js",'##a[href^="http://billing.frugalusenet.com/"]',"http://jriver.com/video.html","||animenewsnetwork.com^*.aframe?","||contextweb.com^$third-party",".gutter",".iab",'http://www.animenewsnetwork.com/assets/[^"]*.jpg']
		block = False
		for l in lst:
			if lower_case.find(l) != -1:
				block = True
				break
		if block:
			print ("Skipping")
			print (request.url().path())
			return QNetworkAccessManager.createRequest(self, QNetworkAccessManager.GetOperation, QtNetwork.QNetworkRequest(QtCore.QUrl()))
		else:
			return QNetworkAccessManager.createRequest(self, op, request, device)

  
class BrowserPage(QWebPage):  
	def __init__(self,url):
		super(BrowserPage, self).__init__()
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
		#self.loadFinished.connect(self._loadFinished)
		self.loadProgress.connect(self._loadProgress)
		self.url = url
		
	def userAgentForUrl(self, url):
		return self.hdr
		
	def _loadFinished(self):
		
		print('Finished')
		print(self.url)
		
		
	def _loadProgress(self):
		print('Progress')
		print(self.url)
		if 'kissanime' in self.url:
			cookie_file = '/tmp/AnimeWatch/kcookie.txt'
		elif 'kisscartoon' in self.url:
			cookie_file = '/tmp/AnimeWatch/kcookieC.txt'
		elif 'kissasian' in self.url:
			cookie_file = '/tmp/AnimeWatch/kcookieD.txt'
		elif 'masterani' in self.url:
			cookie_file = '/tmp/AnimeWatch/animeSquare.txt'
		elif 'animeget' in self.url:
			cookie_file = '/tmp/AnimeWatch/animeget.txt'
		if 'moetube' in self.url:
			cookie_file = '/tmp/AnimeWatch/moetube.txt'
			frame = self.mainFrame()  
			html = frame.toHtml()
			#print(html)
			if 'var glink = ' in html:
				if os.path.exists(cookie_file):
					f = open(cookie_file,'a')
				else:
					f = open(cookie_file,'w')
				f.write(html)
				f.close()
		frame = self.mainFrame()  
		html = frame.toHtml()
		#print(html)
		listCookies = self.networkAccessManager().cookieJar().allCookies()
		n = []
		m = ''
		o = ''
		for cookie in  listCookies:
			k=cookie.toRawForm()
			#k = getContentUnicode(k)
			k = re.sub("b'","'",str(k))
			#print(k)
			j = re.findall("'[^']*",k)
			for i in j:
				i = re.sub("'",'',i)
				if 'kissanime.to' in i or 'kissasian.com' in i or 'kisscartoon.me' in i or 'masterani.me' in i or 'animeget.io' in i:
					j = re.findall('expires=[^;]*',i)
					if j:
						l = re.sub('expires=','',j[0])
						d = datetime.strptime(l,"%a, %d-%b-%Y %H:%M:%S %Z")
						t = calendar.timegm(d.timetuple())
						i = i+'; expiry='+str(int(t))
					else:
						i = i+'; expiry='+str(0)
					n.append(i)
		#print(n)
		cfc=''
		cfd =''
		asp = ''
		clr = False
		for i in n:
			if 'cf_clearance' in i:
				clr = True
				print(n)
		if clr:
			for i in n:
				if 'cf_clearance' in i:
					cfc = self.cookie_split(i)
				elif '__cfduid' in i:
					cfd = self.cookie_split(i)
				elif 'ASP.NET_SessionId' in i:
					asp = self.cookie_split(i)
		if cfc and cfd:
			print(cfc)
			print(cfd)
			print(asp)
			str1 = cfc['domain']+'	'+cfc['HttpOnly']+'	'+cfc['path']+'	'+'FALSE'+'	'+cfc['expiry']+'	'+'cf_clearance'+'	'+cfc['cf_clearance']
			str2 = cfd['domain']+'	'+cfd['HttpOnly']+'	'+cfd['path']+'	'+'FALSE'+'	'+cfd['expiry']+'	'+'__cfduid'+'	'+cfd['__cfduid']
			if asp:
				str3 = asp['domain']+'	'+'FALSE'+'	'+asp['path']+'	'+'FALSE'+'	'+asp['expiry']+'	'+'ASP.NET_SessionId'+'	'+asp['ASP.NET_SessionId']
			else:
				str3 = ''
			
			if not os.path.exists('/tmp/AnimeWatch'):
				os.makedirs('/tmp/AnimeWatch')
			f = open(cookie_file,'w')
			if str3:
				f.write(str2+'\n'+str1+'\n'+str3)
			else:
				f.write(str2+'\n'+str1)
			f.close()
	
		

	def cookie_split(self,i):
		m = []
		j = i.split(';')
		for k in j:
			if '=' in k:
				l = k.split('=')
				l[0] = re.sub(' ','',l[0])
				t = (l[0],l[1])
			else:
				k = re.sub(' ','',k)
				t = (k,'TRUE')
			m.append(t)
		d = dict(m)
		#print(d)
		return(d)
		
class Browser(QWebView):
	def __init__(self,url):
		super(Browser, self).__init__()
		self.setPage(BrowserPage(url))
		

class BrowseUrl(QtGui.QWidget):

	def __init__(self,url):
		super(BrowseUrl, self).__init__()
		self.Browse(url)


	def Browse(self,url):
		MainWindow = QtGui.QWidget()
		progress = QtGui.QProgressDialog("Please Wait", "Cancel", 0, 100, MainWindow)
		progress.setWindowModality(QtCore.Qt.WindowModal)
		progress.setAutoReset(True)
		progress.setAutoClose(True)
		progress.setMinimum(0)
		progress.setMaximum(100)
		progress.resize(500,100)
		if 'moetube' in url:
			progress.setWindowTitle("Loading, Please Wait!")
		else:
			progress.setWindowTitle("Loading, Please Wait! (Cloudflare Protection)")
		progress.show()
		progress.setValue(0)
		
		print('Browse: '+url)
		self.web = Browser(url)
		self.cookie = QtNetwork.QNetworkCookieJar()
		
		self.nam = NetWorkManager()
		self.nam.setCookieJar(self.cookie)
		
		self.web.page().setNetworkAccessManager(self.nam)
		self.web.load(QUrl(url))
		cnt = 0
		
		if 'kissanime' in url:
			cookie_file = '/tmp/AnimeWatch/kcookie.txt'
		elif 'kisscartoon' in url:
			cookie_file = '/tmp/AnimeWatch/kcookieC.txt'
		elif 'kissasian' in url:
			cookie_file = '/tmp/AnimeWatch/kcookieD.txt'
		elif 'masterani' in url:
			cookie_file = '/tmp/AnimeWatch/animeSquare.txt'
		elif 'animeget' in url:
			cookie_file = '/tmp/AnimeWatch/animeget.txt'
		elif 'moetube' in url:
			cookie_file = '/tmp/AnimeWatch/moetube.txt'
			if os.path.exists(cookie_file):
				os.remove(cookie_file)
		while(not os.path.exists(cookie_file) and cnt < 60):
			print('wait '+str(cnt))
			time.sleep(1)
			QtGui.QApplication.processEvents()
			cnt = cnt+1
		if cnt >= 60 and not os.path.exists(cookie_file):
			f = open(cookie_file,'w')
			f.close()
		self.web.setHtml('<html>Cookie Obtained</html>')
		progress.setValue(100)
		progress.hide()


