import sys  
from PyQt5.QtGui import *  
from PyQt5.QtCore import *  
from PyQt5.QtWebEngineWidgets import *  
from PyQt5.QtWebEngineCore import *  
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
from io import StringIO,BytesIO
from PyQt5 import QtCore, QtGui,QtNetwork,QtWidgets,QtWebEngineWidgets,QtWebEngineCore

from PyQt5.QtNetwork import QNetworkAccessManager
from headlessBrowser import ccurl



def _get_video_val(url,c_file,q):
		
		st =''
		quality = q
		#x = ccurl(url+'#'+'-b'+'#'+c_file)
		
		cookie_file = c_file
		html = url
		
		soup = BeautifulSoup(html,'lxml')
		m = soup.findAll('select',{'id':'selectQuality'})
		if m:
			#print(m)
			arr = []
			for i in m:
				j = i.findAll('option')
				for k in j:
					l = k['value']
					#print(l)
					l1 = k.text
					l1 = re.sub(' ','',l1)
					if l1:
						l3 = (l1,l)
					else:
						l3 = ('Not Available',l)
					arr.append(l3)
			total_q = len(arr)
			try:
				arr_dict = dict(arr)
			except:
				arr_dict = []
			
			print(arr_dict)
			
			if arr_dict or arr:
				print('----------total Different Quality Video------',total_q)
				try:
					if quality == 'sd':
						txt = arr_dict['360p']
					elif quality == 'hd':
						txt = arr_dict['720p']
					elif quality == 'sd480p':
						txt = arr_dict['480p']
				except:
					txt = arr_dict['360p']
					
					
				#st = 'document.getElementById("selectQuality").value="'+txt+'"'
				#st = 'document.getElementById("selectQuality").selected="360p"'
				#st = 'document.querySelector(select[id="selectQuality"]).value="'+txt+'"'
				#st = 'document.querySelector(option[value="'+txt+'"])'
				#st= 'document.getElementsByTagName("option").value="'+txt+'"'
				st = "$('#selectQuality').val("+'"'+txt+'"'+")"
				return st

class NetWorkManager(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
	netS = pyqtSignal(str)
	def __init__(self,parent,quality,url):
		super(NetWorkManager, self).__init__(parent)
		self.quality = quality
		self.url = url
	def interceptRequest(self,info):
		#print('hello network')
		#print(info)
		t = info.requestUrl()
		urlLnk = t.url()
		#print(m)
		block_url = ''
		if (quality == 'sd' or quality == 'sd480p') and ('kisscartoon' in self.url or 'kissasian' in self.url) and ('id=' in self.url):
			block_url = 'itag=22'
		
		lower_case = urlLnk.lower()
		lst = ["doubleclick.net" ,"ads",'.jpg','.png','.gif','.css','facebook','.aspx', r"||youtube-nocookie.com/gen_204?", r"youtube.com###watch-branded-actions", "imagemapurl","b.scorecardresearch.com","rightstuff.com","scarywater.net","popup.js","banner.htm","_tribalfusion","||n4403ad.doubleclick.net^$third-party",".googlesyndication.com","graphics.js","fonts.googleapis.com/css","s0.2mdn.net","server.cpmstar.com","||banzai/banner.$subdocument","@@||anime-source.com^$document","/pagead2.","frugal.gif","jriver_banner.png","show_ads.js",'##a[href^="http://billing.frugalusenet.com/"]',"http://jriver.com/video.html","||animenewsnetwork.com^*.aframe?","||contextweb.com^$third-party",".gutter",".iab",'http://www.animenewsnetwork.com/assets/[^"]*.jpg']
		block = False
		for l in lst:
			if lower_case.find(l) != -1:
				block = True
				#info.block(True)
				#print(m,'---blocking----')
				break
		if block:
			info.block(True)
			#print(m,'---blocking----')
			
			
		else:
			
			if 'itag=' in urlLnk and 'redirector' not in urlLnk:
				if block_url and block_url in urlLnk:
					info.block(True)
				else:
					print(urlLnk)
					self.netS.emit(urlLnk)
			
		
			





class BrowserPage(QWebEnginePage):  
	cookie_signal = pyqtSignal(str)
	media_signal = pyqtSignal(str)
	#val_signal = pyqtSignal(str)
	def __init__(self,url,quality,add_cookie,c_file,m_val):
		super(BrowserPage, self).__init__()
		print('hello')
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		x = ''
		self.m = self.profile().cookieStore()
		self.profile().setHttpUserAgent(self.hdr)
		self.loadFinished.connect(self._loadFinished)
		self.loadProgress.connect(self._loadProgress)
		self.loadStarted.connect(self._loadstart)
		p = NetWorkManager(self,quality,url)
		p.netS.connect(lambda y = x : self.urlMedia(y))
		self.profile().setRequestInterceptor(p)
		#self.profile().clearHttpCache()
		self.profile().setCachePath('/tmp/AnimeWatch')
		self.profile().setPersistentStoragePath('/tmp/AnimeWatch')
		self.url = url
		z = ''
		#self.val_signal.connect(lambda y = z : self.val_found(y))
		self.c_list = []
		#print(self.url)
		t = ''
		self.cnt = 0
		self.quality = quality
		self.val = m_val
		self.add_cookie = add_cookie
		self.cookie_file = c_file
		if not self.add_cookie:
			self.m.deleteAllCookies()
			self.set_cookie(self.cookie_file)
			
		
		self.text = ''
		
		#ag = self.page().profile().httpUserAgent()
		#print(ag)
		#self.m.loadAllCookies()
		
		#if self.add_cookie:
		if self.add_cookie:
			self.m.deleteAllCookies()
			self.m.cookieAdded.connect(lambda  x = t : self._cookie(x))
		print("end")
	@pyqtSlot(str)
	def urlMedia(self,info):
		if os.path.exists('/tmp/AnimeWatch/lnk.txt'):
			os.remove('/tmp/AnimeWatch/lnk.txt')
		print('*******')
		print(info)
		f = open('/tmp/AnimeWatch/lnk.txt','w')
		f.write(info)
		f.close()
		self.media_signal.emit(info)
		print('********')
	@pyqtSlot(str)
	def val_found(self,info):
		print(info,'*******info*********')
		#self.page().runJavaScript(info)
		self.val = info
	
	
	def set_cookie(self,cookie_file):
		cookie_arr = QtNetwork.QNetworkCookie()
		c = []
		f = open(cookie_file,'r')
		lines = f.readlines()
		f.close()
		for i in lines:
			k = re.sub('\n','',i)
			l = k.split('	')
			d = QtNetwork.QNetworkCookie()
			d.setDomain(l[0])
			print(l[0])
			if l[1]== 'TRUE':
				l1= True
			else:
				l1= False
			d.setHttpOnly(l1)
			d.setPath(l[2])
			print(l1)
			print(l[2])
			if l[3]== 'TRUE':
				l3= True
			else:
				l3= False
			d.setSecure(l3)
			print(l[3])
			l4 = int(l[4])
			print(l4)
			d.setExpirationDate(QtCore.QDateTime.fromTime_t(l4))
			l5 = bytes(l[5],'utf-8')
			d.setName((l5))
			l6 = bytes(l[6],'utf-8')
			d.setValue(l6)
			c.append(d)
			#cookie_arr.append(d)
			self.profile().cookieStore().setCookie(d)
		
		
	def _cookie(self,x):
		result = ''
		#print(x)
		#print('Cookie')
		l = str(x.toRawForm())
		l = re.sub("b'|'",'',l)
		#print(l)
		#self.c_list.append(l)
		l = self._getTime(l)
		print(l)
		
		if 'kisscartoon' in self.url or 'kissasian' in self.url:
			self._writeCookies(l)
			if 'ASP.NET_SessionId' in l:
				self.cookie_signal.emit("Cookie Found")
		else :
			#print(l)
			#if self.add_cookie:
			self._writeCookies(l)
			if 'cf_clearance' in l:
				self.cookie_signal.emit("Cookie Found")
			#f = open('/tmp/ck.txt','w')
			#f.close()
			print('------cf----------')
		
			
		#self.setHtml('<html>cookie Obtained</html>')
		#self.page().toHtml(lambda x = result: self.htm(x))
		
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
		
	def _writeCookies(self,i):
		cfc = ''
		cfd = ''
		asp = ''
		if 'cf_clearance' in i:
			cfc = self.cookie_split(i)
		elif '__cfduid' in i:
			cfd = self.cookie_split(i)
		elif 'ASP.NET_SessionId' in i:
			asp = self.cookie_split(i)
		if cfc or cfd or asp:
			str1 = ''
			#print(cfc)
			#print(cfd)
			#print(asp)
			if cfc:
				str1 = cfc['domain']+'	'+cfc['HttpOnly']+'	'+cfc['path']+'	'+'FALSE'+'	'+cfc['expiry']+'	'+'cf_clearance'+'	'+cfc['cf_clearance']
			
			if cfd:
				str1 = cfd['domain']+'	'+cfd['HttpOnly']+'	'+cfd['path']+'	'+'FALSE'+'	'+cfd['expiry']+'	'+'__cfduid'+'	'+cfd['__cfduid']
			if asp:
				str1 = asp['domain']+'	'+'FALSE'+'	'+asp['path']+'	'+'FALSE'+'	'+str(0)+'	'+'ASP.NET_SessionId'+'	'+asp['ASP.NET_SessionId']
				
			if not os.path.exists('/tmp/AnimeWatch/cloud_cookie.txt'):
				f = open('/tmp/AnimeWatch/cloud_cookie.txt','w')
				f.write(str1)
			else:
				f = open('/tmp/AnimeWatch/cloud_cookie.txt','a')
				f.write('\n'+str1)
			#print('written--cloud_cookie--------------')
			f.close()
			
			
	def _getTime(self,i):
		j = re.findall('expires=[^;]*',i)
		if j:
			l = re.sub('expires=','',j[0])
			d = datetime.strptime(l,"%a, %d-%b-%Y %H:%M:%S %Z")
			t = calendar.timegm(d.timetuple())
			k = '; expiry='+str(int(t))
		else:
			k = '; expiry='+str(0)
		i = re.sub('; expires=[^;]*',k,i)
		return i
	
	def htm(self,x):
		r = 0
		#print(x)
		if self.val and 'selectQuality' in x:
			print(self.cnt,'---quality-----cnt----')
			self.cnt = self.cnt+1
		"""
		if self.val and 'selectQuality' in x and self.cnt == 0:
			if os.path.exists('/tmp/AnimeWatch/lnk.txt'):
				os.remove('/tmp/AnimeWatch/lnk.txt')
				print('------link--------found-------media------')
			self.cnt = 1
			self.runJavaScript(self.val,self.val_scr)
			self.triggerAction(QWebEnginePage.Reload)
		"""
		#if self.cnt == 1:
			#super(BrowserPage,self).stop()
		#	self.triggerAction(QWebEnginePage.Stop)
		#	self.runJavaScript(self.val,self.val_scr)
		#	
		#	self.runJavaScript(self.val,self.val_scr)
	def _loadstart(self):
		result = ''
		#self.cnt = 0
	def htm_src(self,x):
		html = x
		if 'var glink = ' in html:
			c_f = '/tmp/AnimeWatch/cloud_cookie.txt'
			if os.path.exists(c_f):
				f = open(c_f,'a')
			else:
				f = open(c_f,'w')
				#print('file-not-present+++++++++++++++')
			f.write(html)
			f.close()
			self.cookie_signal.emit("Cookie Found")
	def val_scr(self,x):
		print('===============java----------scr')
		print(x)
		#self.runJavaScript("$('#selectQuality').change();")
		print('===============java----------scr')
	def _loadProgress(self):
		
		result =''
		#
		if ('kisscartoon' in self.url or 'kissasian' in self.url) and ('id=' in self.url):
			#x = self.toHtml(self.htm)
			if self.val:
				#QtWidgets.QApplication.processEvents()
				#st = 'document.getElementById("selectQuality").value="'+self.val+'"'
				#st = "$('#selectQuality').val("+'"'+self.val+'"'+")"
				#self.runJavaScript("$('#selectQuality').change();",self.val_scr)
				self.runJavaScript(self.val,self.val_scr)
				#QtWidgets.QApplication.processEvents()
				
				#self.runJavaScript("$('#selectQuality').change();",self.val_scr)
				#self.runJavaScript('document.location.reload(true)')
		elif 'moetube' in url:
			x = self.toHtml(self.htm_src)
			
		self.cnt = self.cnt+1
		
	def _loadFinished(self):
		result = ""
		print('Finished')
		
		#if self.cnt == 1:
		#	self.runJavaScript(self.val,self.val_scr)
		#	self.triggerAction(QWebEnginePage.Reload)
			
		#self.cnt = self.cnt+1
		#x = self.page().toHtml(lambda x = result: self.htm(x))
		


	
	


		
		
	

class BrowseUrlT(QWebEngineView):
	#cookie_s = pyqtSignal(str)
	def __init__(self,url,quality,cookie):
		super(BrowseUrlT, self).__init__()
		#QtWidgets.__init__()
		self.url = url
		self.add_cookie = True
		self.quality = quality
		self.media_val = ''
		self.cnt = 0
		self.cookie_file = cookie
		self.Browse(self.url)
		
	def Browse(self,url):
		
		
		
		
		
		if os.path.exists(self.cookie_file):
			content = ccurl(url+'#'+'-b'+'#'+self.cookie_file)
			#print(content)
			if 'checking_browser' in content:
				os.remove(self.cookie_file)
				self.add_cookie = True
			else:
				self.add_cookie = False
				if ('kisscartoon' in url or 'kissasian' in url) and self.quality and ('id=' in url):
					self.media_val = _get_video_val(content,self.cookie_file,self.quality)
		else:
			self.add_cookie = True
		
		self.tab_web = QtWidgets.QWidget()
		self.tab_web.setMaximumSize(300,50)
		self.tab_web.setWindowTitle('Wait!')
		self.horizontalLayout_5 = QtWidgets.QVBoxLayout(self.tab_web)
		self.horizontalLayout_5.addWidget(self)
		
		if self.add_cookie:
			if 'moetube' not in url:
				self.tab_web.setWindowTitle('Wait! Cloudflare')
			self.web = BrowserPage(url,self.quality,self.add_cookie,self.cookie_file,self.media_val)
			
			self.web.cookie_signal.connect(self.cookie_found)
			self.web.media_signal.connect(self.media_source_found)
			self.setPage(self.web)
			print('add_cookie')
			self.load(QUrl(url))
			print('--')
			#self.load(QUrl(url))
			self.cnt = 1
			
			
		elif ('kisscartoon' in url or 'kissasian' in url) and self.quality and ('id=' in url):
			print('+++++++++++++++++++')
			self.tab_web.setWindowTitle('Wait! Resolving Link')
			self.web = BrowserPage(url,self.quality,self.add_cookie,self.cookie_file,self.media_val)
			
			self.web.cookie_signal.connect(self.cookie_found)
			self.web.media_signal.connect(self.media_source_found)
			self.setPage(self.web)
			self.load(QUrl(url))
		QtWidgets.QApplication.processEvents()
		QtWidgets.QApplication.processEvents()
		self.tab_web.show()
		
		
		
	@pyqtSlot(str)
	def cookie_found(self):
		#global web
		print('cookie')
		self.add_cookie = False
		if ('id=' in self.url) and ('kisscartoon' in url or 'kissasian' in url):
			print('Cookie Obtained, now link finding')
			f = open('/tmp/AnimeWatch/tmp_cookie','w')
			f.write('Cookie Obtained, now link finding')
			f.close()
			
		elif 'moetube' in url:
			self.setHtml('<html>Link Resolved</html>')
		else:
			self.setHtml('<html>cookie Obtained</html>')
		c_f = '/tmp/AnimeWatch/cloud_cookie.txt'
		if os.path.exists(c_f):
			content = open(c_f).read()
			f = open(self.cookie_file,'w')
			f.write(content)
			f.close()
			os.remove(c_f)
		if ('id=' in self.url) and ('kisscartoon' in url or 'kissasian' in url):
			sys.exit(0)
	@pyqtSlot(str)
	def media_source_found(self):
		#global web
		#self.setHtml('<html>Media Source Obtained</html>')
		print('media found')
		
	
		

if __name__ == "__main__":
		
		url = sys.argv[1]	
		print(url)
		quality = sys.argv[2]
		print(quality)
		cookie = sys.argv[3]
		app = QtWidgets.QApplication(sys.argv)
		web = BrowseUrlT(url,quality,cookie)
		ret = app.exec_()
		sys.exit(ret)

