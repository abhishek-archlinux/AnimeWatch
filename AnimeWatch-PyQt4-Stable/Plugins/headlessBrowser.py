import sys  
#from PyQt4.QtGui import *  
#from PyQt4.QtCore import *  
#from PyQt4.QtWebKit import *  
import re
import urllib
import urllib3
import pycurl
import time
import os
import os.path
import sys
import calendar
import weakref
from bs4 import BeautifulSoup
from datetime import datetime
from io import StringIO,BytesIO
from PyQt4 import QtCore, QtGui,QtNetwork,QtWebKit
from PyQt4.QtWebKit import QWebPage,QWebView
from PyQt4.QtCore import (QCoreApplication, QObject, Q_CLASSINFO, pyqtSlot,pyqtSignal,
                          pyqtProperty,QUrl)
from PyQt4.QtNetwork import QNetworkAccessManager


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


class NetWorkManager(QNetworkAccessManager):
	def __init__(self):
		super(NetWorkManager, self).__init__()
   
	def createRequest(self, op, request, device = None ):
		global lst,pg
		try:
			#print(str(request.url()))
			urlLnk = (request.url()).toString()
			#print(urlLnk)
			path = str(request.url().path())
		except UnicodeEncodeError:
			pass
		#print(path)
		lower_case = path.lower()
		#lst = tuple(open("easylist.txt", 'r'))
		lst = ["doubleclick.net" ,"ads",'.jpg','.png','.gif','.css','facebook','.aspx', r"||youtube-nocookie.com/gen_204?", r"youtube.com###watch-branded-actions", "imagemapurl","b.scorecardresearch.com","rightstuff.com","scarywater.net","popup.js","banner.htm","_tribalfusion","||n4403ad.doubleclick.net^$third-party",".googlesyndication.com","graphics.js","fonts.googleapis.com/css","s0.2mdn.net","server.cpmstar.com","||banzai/banner.$subdocument","@@||anime-source.com^$document","/pagead2.","frugal.gif","jriver_banner.png","show_ads.js",'##a[href^="http://billing.frugalusenet.com/"]',"http://jriver.com/video.html","||animenewsnetwork.com^*.aframe?","||contextweb.com^$third-party",".gutter",".iab",'http://www.animenewsnetwork.com/assets/[^"]*.jpg']
		block = False
		for l in lst:
			if lower_case.find(l) != -1:
				block = True
				break
		if block:
			#print ("Skipping")
			#print (request.url().path())
			
			return QNetworkAccessManager.createRequest(self, QNetworkAccessManager.GetOperation, QtNetwork.QNetworkRequest(QtCore.QUrl()))
		else:
			if 'itag=' in urlLnk and 'redirector' not in urlLnk:
				print('*********')
				#print()
				#print(path)
				#print(urlLnk)
				#pg.web.setHtml('<html>got the link</html>')
				#self.lnkUrl.emit(path)
				f = open('/tmp/AnimeWatch/lnk.txt','w')
				f.write(urlLnk)
				f.close()
				return QNetworkAccessManager.createRequest(self, op, request, device)
				#return QNetworkAccessManager.createRequest(self, op, request, device)
				#return QNetworkAccessManager.createRequest(self, QNetworkAccessManager.GetOperation, QtNetwork.QNetworkRequest(QtCore.QUrl()))
			
			else:
				return QNetworkAccessManager.createRequest(self, op, request, device)

  
class BrowserPage(QWebPage):  
	def __init__(self,url,quality):
		super(BrowserPage, self).__init__()
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		#self.loadFinished.connect(self._loadFinished)
		self.loadProgress.connect(self._loadProgress)
		self.url = url
		self.cnt = 0
		self.quality = quality
	def userAgentForUrl(self, url):
		return self.hdr
		
	def _loadFinished(self):
		
		print('Finished')
		print(self.url)
		
		
	def _loadProgress(self):
		#print('Progress')
		#print(self.url)
		
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
		elif 'animeplace' in self.url:
			cookie_file = '/tmp/AnimeWatch/animeplace.txt'
		elif 'moetube' in self.url:
			cookie_file = '/tmp/AnimeWatch/animeHQ.txt'
		if 'moetube' in self.url:
			txt_file = '/tmp/AnimeWatch/moetube.txt'
			frame = self.mainFrame()  
			html = frame.toHtml()
			#print(html)
			if 'var glink = ' in html:
				if os.path.exists(txt_file):
					f = open(txt_file,'a')
				else:
					f = open(txt_file,'w')
				f.write(html)
				f.close()
		
		if self.cnt == 0 and os.path.exists(cookie_file) and ('kisscartoon' in self.url or 'kissasian' in self.url):
			frame = self.mainFrame()
			html = frame.toHtml()
			soup = BeautifulSoup(html,'lxml')
			m = soup.findAll('select',{'id':'selectQuality'})
			if m:
				print(m)
				arr = []
				for i in m:
					j = i.findAll('option')
					for k in j:
						l = k['value']
						#print(l)
						arr.append(l)
				total_q = len(arr)
				
					
						
				if arr:
					print('----------total Different Quality Video------',total_q)
					if self.quality == 'sd':
						txt = arr[-1]
					elif self.quality == 'hd':
						if total_q == 1:
							txt = arr[-1]
						elif total_q == 2:
							txt = arr[-2]
						elif total_q == 3 or total_q == 4:
							txt = arr[-3]
							
					elif self.quality == 'sd480p':
						if total_q == 1:
							txt = arr[-1]
						elif total_q == 2 or total_q == 3 or total_q == 4:
							txt = arr[-2]
						
					doc = frame.documentElement()
					bt = doc.findFirst("select[id=selectQuality]")
					#txt = arr[-1]
					bt.evaluateJavaScript('this.value="'+txt+'"')
					self.cnt = 1
		
		
		
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
				if 'kissanime.to' in i or 'kissasian.com' in i or 'kisscartoon.me' in i or 'masterani.me' in i or 'animeget.io' in i or 'animeplace.co' in i or 'moetube.net' in i:
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
				#print(n)
		if clr:
			for i in n:
				if 'cf_clearance' in i:
					cfc = self.cookie_split(i)
				elif '__cfduid' in i:
					cfd = self.cookie_split(i)
				elif 'ASP.NET_SessionId' in i:
					asp = self.cookie_split(i)
		if cfc and cfd:
			#print(cfc)
			#print(cfd)
			#print(asp)
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
	def __init__(self,url,quality):
		super(Browser, self).__init__()
		self.setPage(BrowserPage(url,quality))
		

class BrowseUrl(QtGui.QWidget):

	def __init__(self,url,quality):
		super(BrowseUrl, self).__init__()
		
		self.Browse(url,quality)
	
		
	def Browse(self,url,quality):
		
		
		
		
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
		elif 'animeplace' in url:
			cookie_file = '/tmp/AnimeWatch/animeplace.txt'
		elif 'moetube' in url:
			cookie_file = '/tmp/AnimeWatch/animeHQ.txt'
			#if os.path.exists(cookie_file):
			#	os.remove(cookie_file)
		
		if 'animeget' in url or 'masterani' in url or 'animeplace' in url or 'moetube' in url:
			content = ccurl(url)
		else:
			content = 'checking_browser'
		
		if 'checking_browser' in content:
			if not os.path.exists(cookie_file):
				
				self.cookie = QtNetwork.QNetworkCookieJar()
				self.nam = NetWorkManager()
				self.nam.setCookieJar(self.cookie)
			else:
				cookie_arr = QtNetwork.QNetworkCookieJar()
				c = []
				f = open(cookie_file,'r')
				lines = f.readlines()
				f.close()
				for i in lines:
					k = re.sub('\n','',i)
					l = k.split('	')
					d = QtNetwork.QNetworkCookie()
					d.setDomain(l[0])
					if l[1]== 'TRUE':
						l1= True
					else:
						l1= False
					d.setHttpOnly(l1)
					d.setPath(l[2])
					if l[3]== 'TRUE':
						l3= True
					else:
						l3= False
					d.setSecure(l3)
					l4 = int(l[4])
					print(l4)
					d.setExpirationDate(QtCore.QDateTime.fromTime_t(l4))
					d.setName(l[5])
					d.setValue(l[6])
					c.append(d)
					#cookie_arr.append(d)
				cookie_arr.setAllCookies(c)
				self.nam = NetWorkManager()
				self.nam.setCookieJar(cookie_arr)
			
			self.web = Browser(url,quality)
			self.tab_2 = QtGui.QWidget()
			self.tab_2.setMaximumSize(300,50)
			self.tab_2.setWindowTitle('Wait!')
			self.horizontalLayout_5 = QtGui.QVBoxLayout(self.tab_2)
			print('Browse: '+url)
			
			self.horizontalLayout_5.addWidget(self.web)
			self.tab_2.show()
			#self.tab_2.hide()
			#self.web.show()
			self.web.page().setNetworkAccessManager(self.nam)
			self.web.load(QUrl(url))
			cnt = 0
			
			
			while(not os.path.exists(cookie_file) and cnt < 20):
				#print()
				print('wait Clouflare ')
				time.sleep(1)
				QtGui.QApplication.processEvents()
				cnt = cnt+1
				self.tab_2.setWindowTitle('Wait! Cloudflare '+str(cnt)+'s')
				
			if cnt >= 20 and not os.path.exists(cookie_file):
				f = open(cookie_file,'w')
				f.close()
			lnk_file = '/tmp/AnimeWatch/lnk.txt'
			if os.path.exists(lnk_file):
				os.remove(lnk_file)
			cnt = 0
			if ('kisscartoon' in url or 'kissasian' in url) and quality:
				while(not os.path.exists(lnk_file) and cnt < 20):
					print('wait Finding Link ')
					time.sleep(1)
					QtGui.QApplication.processEvents()
					cnt = cnt+1
					self.tab_2.setWindowTitle('Link Resolving '+str(cnt)+'s')
				
				if os.path.exists(lnk_file):
					self.web.setHtml('<html>Link Obtained</html>')
					link = open(lnk_file).read()
					print(link)
				else:
					self.web.setHtml('<html>No Link Found</html>')
					print('No Link Available or Clear The Cache')
			else:
				self.web.setHtml('<html>cookie Obtained</html>')
			self.tab_2.hide()
		else:
			f = open(cookie_file,'w')
			f.close()



