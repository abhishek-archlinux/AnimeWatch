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
import urllib
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
from PyQt5 import QtCore,QtGui,QtNetwork,QtWebKitWidgets,QtWidgets
from PyQt5.QtWebKitWidgets import QWebPage,QWebView
from PyQt5.QtCore import (QCoreApplication, QObject, Q_CLASSINFO, pyqtSlot,pyqtSignal,
                          pyqtProperty,QUrl)
from PyQt5.QtNetwork import QNetworkAccessManager
from player_functions import ccurl


def parse_file(content,url,quality):
	txt = ''
	soup = BeautifulSoup(content,'lxml')
	if 'kissanime' in url:
		m = soup.findAll('select',{'id':'slcQualix'})
	else:
		m = soup.findAll('select',{'id':'selectQuality'})
	#print(m,'---select--quality---')
	if m:
		arr = []
		arr_lnk = []
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
				arr_lnk.append(l)
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
					if total_q >= 3:
						txt = arr_dict['720p']
					elif total_q == 2:
						txt = arr_lnk[0]
					else:
						txt = arr_dict['360p']
				elif quality == 'sd480p':
					if total_q >= 2:
						txt = arr_dict['480p']
					else:
						txt = arr_dict['360p']
				elif quality == 'best':
					txt = arr_lnk[0]
			except:
				txt = arr_dict['360p']
	return txt

class NetWorkManager(QNetworkAccessManager):
	def __init__(self):
		super(NetWorkManager, self).__init__()
   
	def createRequest(self, op, request, device = None ):
		global block_list,TMP_DIR
		try:
			urlLnk = (request.url()).toString()
			path = (request.url().toString())
		except UnicodeEncodeError:
			path = (request.url().path())
			
		lower_path = path.lower()
		#block_list = []
		block_list = ["doubleclick.net" ,"ads",'.gif','.css','facebook','.aspx', r"||youtube-nocookie.com/gen_204?", r"youtube.com###watch-branded-actions", "imagemapurl","b.scorecardresearch.com","rightstuff.com","scarywater.net","popup.js","banner.htm","_tribalfusion","||n4403ad.doubleclick.net^$third-party",".googlesyndication.com","graphics.js","fonts.googleapis.com/css","s0.2mdn.net","server.cpmstar.com","||banzai/banner.$subdocument","@@||anime-source.com^$document","/pagead2.","frugal.gif","jriver_banner.png","show_ads.js",'##a[href^="http://billing.frugalusenet.com/"]',"http://jriver.com/video.html","||animenewsnetwork.com^*.aframe?","||contextweb.com^$third-party",".gutter",".iab",'http://www.animenewsnetwork.com/assets/[^"]*.jpg','revcontent']
		block = False
		for l in block_list:
			if l in lower_path:
				block = True
				break
		if block:
			return QNetworkAccessManager.createRequest(self, QNetworkAccessManager.GetOperation, QtNetwork.QNetworkRequest(QtCore.QUrl()))
		else:
			if 'itag=' in urlLnk and 'redirector' not in urlLnk:
				print('*********')
				#f = open(os.path.join(TMP_DIR,'lnk.txt'),'w')
				#f.write(urlLnk)
				#f.close()
				return QNetworkAccessManager.createRequest(self, op, request, device)
			
			else:
				return QNetworkAccessManager.createRequest(self, op, request, device)

  
class BrowserPage(QWebPage):  
	def __init__(self,url,quality,c,end_point=None,get_cookie=None,domain_name=None,captcha=None,get_epn=None):
		super(BrowserPage, self).__init__()
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		#self.loadFinished.connect(self._loadFinished)
		self.loadProgress.connect(self._loadProgress)
		self.url = url
		self.cnt = 0
		self.quality = quality
		self.cookie_file = c
		self.tmp_dir,self.new_c = os.path.split(self.cookie_file)
		if not end_point:
			self.end_point = 'cf_clearance'
		else:
			self.end_point = end_point
		self.domain_name = domain_name
		if self.domain_name:
			if self.domain_name.lower() == 'none':
				self.domain_name = None
		self.get_cookie = get_cookie
		self.captcha = captcha
		self.get_epn = get_epn
		
	def userAgentForUrl(self, url):
		return self.hdr
		
	def _loadFinished(self):
		
		print('Finished')
		print(self.url)
		
		
	def _loadProgress(self):
		
		if (not self.cnt and os.path.exists(self.cookie_file) and self.get_epn):
			frame = self.mainFrame()
			html = frame.toHtml()
			txt = parse_file(html,self.url,self.quality)
			print(txt)
			if txt:
				urlLnk = ''
				if 'kissanime' in self.url:
					url_val = frame.evaluateJavaScript('ovelWrap("{0}");'.format(txt))
				else:
					url_val = frame.evaluateJavaScript('$kissenc.decrypt("{0}");'.format(txt))
				print(url_val)
				
				if url_val.startswith('http'):
					y1 = re.findall("http[^']*",url_val)
					print(y1)
					for y in y1:
						content = ccurl(y+'#'+'-I')
						if "Location:" in content:
							m = re.findall('Location: [^\n]*',content)
							urlLnk = re.sub('Location: |\r','',m[-1])
						else:
							urlLnk = y
					print(urlLnk)
					f = open(os.path.join(TMP_DIR,'lnk.txt'),'w')
					f.write(urlLnk)
					f.close()
					self.cnt = 1
				"""
				doc = frame.documentElement()
				if 'kissanime' in self.url:
					bt = doc.findFirst("select[id=slcQualix]")
				else:
					bt = doc.findFirst("select[id=selectQuality]")
				#txt = arr[-1]
				bt.evaluateJavaScript('this.value="'+txt+'"')
				self.cnt = 1
				"""
		
		if self.get_cookie:
			listCookies = self.networkAccessManager().cookieJar().allCookies()
			#print(listCookies)
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
					if 'kissanime.ru' in i or 'kissasian.com' in i or 'kimcartoon.me' in i or 'masterani.me' in i or 'animeget.io' in i or 'animeplace.co' in i or 'moetube.net' in i or 'nyaa.se' in i or self.domain_name:
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
			idt = ''
			test_idt = ''
			utmc = ''
			clr = False
			reqkey = ''
			new_arr = []
			for i in n:
				if self.end_point in i:
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
					elif 'idtz' in i:
						idt = self.cookie_split(i)
					elif '__utmc' in i:
						utmc = self.cookie_split(i)
					elif self.domain_name:
						reqkey = self.cookie_split(i)
						try:
							if reqkey['domain']:
								if self.domain_name in reqkey['domain']:
									dm = True
								try:
									reqkey['expiry']
								except:
									reqkey.update({'expiry':'0'})
								try:
									reqkey['HttpOnly']
								except:
									reqkey.update({'HttpOnly':'False'})
								if reqkey:
									str3 = reqkey['domain']+'	'+'FALSE'+'	'+reqkey['path']+'	'+'FALSE'+'	'+reqkey['expiry']+'	'+reqkey['name_id']+'	'+reqkey[reqkey['name_id']]
									new_arr.append(str3)
						except Exception as e:
							print(e,'--240--')
							
			if new_arr:
				f = open(self.cookie_file,'w')
				for i in new_arr:
					f.write(i+'\n')
				f.close()
			elif (cfc and cfd):
				#print(cfc)
				#print(cfd)
				#print(asp)
				str3 = ''
				str1 = cfc['domain']+'	'+cfc['HttpOnly']+'	'+cfc['path']+'	'+'FALSE'+'	'+cfc['expiry']+'	'+'cf_clearance'+'	'+cfc['cf_clearance']
				str2 = cfd['domain']+'	'+cfd['HttpOnly']+'	'+cfd['path']+'	'+'FALSE'+'	'+cfd['expiry']+'	'+'__cfduid'+'	'+cfd['__cfduid']
				if asp:
					str3 = asp['domain']+'	'+'FALSE'+'	'+asp['path']+'	'+'FALSE'+'	'+asp['expiry']+'	'+'ASP.NET_SessionId'+'	'+asp['ASP.NET_SessionId']
					
				if idt:
					str3 = idt['domain']+'	'+'FALSE'+'	'+idt['path']+'	'+'FALSE'+'	'+idt['expiry']+'	'+'idtz'+'	'+idt['idtz']
					
				if 'kissasian' in self.url:
					str3 = 'kissasian.com	FALSE	/	FALSE	0		__test'
				
				if utmc:
					str3 = utmc['domain']+'	'+'FALSE'+'	'+utmc['path']+'	'+'FALSE'+'	'+str(0)+'	'+'__utmc'+'	'+utmc['__utmc']
				
				if reqkey:
					str3 = reqkey['domain']+'	'+'FALSE'+'	'+reqkey['path']+'	'+'FALSE'+'	'+reqkey['expiry']+'	'+reqkey['name_id']+'	'+reqkey[reqkey['name_id']]
				
				f = open(self.cookie_file,'w')
				if str3:
					f.write(str2+'\n'+str1+'\n'+str3)
				else:
					f.write(str2+'\n'+str1)
				f.close()
		
		

	def cookie_split(self,i):
		m = []
		j = i.split(';')
		index = 0
		for k in j:
			if '=' in k:
				l = k.split('=')
				l[0] = re.sub(' ','',l[0])
				t = (l[0],l[1])
			else:
				k = re.sub(' ','',k)
				t = (k,'TRUE')
			m.append(t)
			if index == 0 and '=' in k:
				m.append(('name_id',l[0]))
			index = index + 1
		d = dict(m)
		print(d)
		return(d)
		
class Browser(QWebView):
	def __init__(self,url,quality,c,end_point=None,get_cookie=None,domain_name=None,captcha=None,get_epn=None):
		super(Browser, self).__init__()
		self.setPage(BrowserPage(url,quality,c,end_point,get_cookie,domain_name,captcha=captcha,get_epn=get_epn))
		

class BrowseUrl(QtWidgets.QWidget):
	def __init__(self,url,quality,c,end_point=None,get_cookie=None,domain_name=None):
		super(BrowseUrl, self).__init__()
		global TMP_DIR
		self.cookie_file = c
		self.tmp_dir,self.new_c = os.path.split(self.cookie_file)
		TMP_DIR = self.tmp_dir
		if not end_point:
			self.end_point = 'cf_clearance'
		else:
			self.end_point = end_point
		if get_cookie:
			self.get_cookie = True
		else:
			self.get_cookie = False
		if domain_name:
			self.domain_name = domain_name
		else:
			self.domain_name= 'None'
		self.get_epn = False
		if ('kimcartoon' in url or 'kissasian' in url or 'kissanime' in url) and quality and ('id=' in url):
			self.get_epn = True
		self.captcha = False
		self.Browse(url,quality)
		
		
	def Browse(self,url,quality):
		content = ccurl(url+'#-b#'+self.cookie_file)
		if 'Are You Human' in content:
			self.captcha = True
		if 'checking_browser' in content:
			self.get_cookie = True
			
		if self.get_cookie or self.get_epn or self.captcha:
			if not os.path.exists(self.cookie_file):
				
				self.cookie = QtNetwork.QNetworkCookieJar()
				self.nam = NetWorkManager()
				self.nam.setCookieJar(self.cookie)
			else:
				cookie_arr = QtNetwork.QNetworkCookieJar()
				c = []
				f = open(self.cookie_file,'r')
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
					d.setName(bytes(l[5],'utf-8'))
					d.setValue(bytes(l[6],'utf-8'))
					c.append(d)
					#cookie_arr.append(d)
				cookie_arr.setAllCookies(c)
				self.nam = NetWorkManager()
				self.nam.setCookieJar(cookie_arr)
			print('---364----')
			self.web = Browser(url,quality,self.cookie_file,self.end_point,self.get_cookie,self.domain_name,self.captcha,self.get_epn)
			self.tab_2 = QtWidgets.QWidget()
			if self.captcha:
				self.tab_2.setMaximumSize(700,700)
			else:
				self.tab_2.setMaximumSize(300,50)
			self.tab_2.setWindowTitle('Wait!')
			self.horizontalLayout_5 = QtWidgets.QVBoxLayout(self.tab_2)
			print('Browse: '+url)
			
			self.horizontalLayout_5.addWidget(self.web)
			self.tab_2.show()
			#self.tab_2.hide()
			#self.web.show()
			self.web.page().setNetworkAccessManager(self.nam)
			self.web.load(QUrl(url))
			cnt = 0
			
			
			while(not os.path.exists(self.cookie_file) and cnt < 30):
				#print()
				print('wait Clouflare ')
				time.sleep(1)
				QtWidgets.QApplication.processEvents()
				cnt = cnt+1
				self.tab_2.setWindowTitle('Wait! Cloudflare '+str(cnt)+'s')
				
			if cnt >= 30 and not os.path.exists(self.cookie_file):
				f = open(self.cookie_file,'w')
				f.close()
			lnk_file = os.path.join(self.tmp_dir,'lnk.txt')
			if os.path.exists(lnk_file):
				os.remove(lnk_file)
			cnt = 0
			cnt_limit = 30
			if self.captcha:
				cnt_limit = 60
			if ('kimcartoon' in url or 'kissasian' in url or 'kissanime' in url) and quality:
				while(not os.path.exists(lnk_file) and cnt < cnt_limit):
					print('wait Finding Link ')
					time.sleep(1)
					QtWidgets.QApplication.processEvents()
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
			if self.captcha:
				self.tab_2.show()
			else:
				self.tab_2.hide()
		else:
			f = open(self.cookie_file,'w')
			f.close()



