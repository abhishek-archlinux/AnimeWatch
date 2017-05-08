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
import os
path_val = sys.argv[7]
path_val_arr = path_val.split('::')
for i in path_val_arr:
	if os.path.exists(i):
		sys.path.insert(0,i)
print(sys.path,'---path---')  
import re
import urllib.parse
import time
import calendar
import weakref
from bs4 import BeautifulSoup
from datetime import datetime
import pycurl
from io import StringIO,BytesIO
from PyQt5 import QtCore, QtGui,QtNetwork,QtWidgets,QtWebEngineWidgets,QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtNetwork import QNetworkAccessManager
from PyQt5.QtCore import QUrl,pyqtSlot,pyqtSignal


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

def ccurl(url,external_cookie=None):
	hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
	if 'youtube.com' in url:
		hdr = 'Mozilla/5.0 (Linux; Android 4.4.4; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'
	print(url)
	c = pycurl.Curl()
	curl_opt = ''
	picn_op = ''
	rfr = ''
	nUrl = url
	cookie_file = ''
	postfield = ''
	if '#' in url:
		curl_opt = nUrl.split('#')[1]
		url = nUrl.split('#')[0]
		if curl_opt == '-o':
			picn_op = nUrl.split('#')[2]
		elif curl_opt == '-Ie' or curl_opt == '-e':
			rfr = nUrl.split('#')[2]
		elif curl_opt == '-Icb' or curl_opt == '-bc' or curl_opt == '-b' or curl_opt == '-Ib':
			cookie_file = nUrl.split('#')[2]
		if curl_opt == '-d':
			post = nUrl.split('#')[2]
			post = re.sub('"','',post)
			post = re.sub("'","",post)
			post1 = post.split('=')[0]
			post2 = post.split('=')[1]
			post_data = {post1:post2}
			postfield = urllib.parse.urlencode(post_data)
	url = str(url)
	#c.setopt(c.URL, url)
	try:
		c.setopt(c.URL, url)
	except UnicodeEncodeError:
		c.setopt(c.URL, url.encode('utf-8'))
	storage = BytesIO()
	if os.name == 'nt':
		ca_cert = get_ca_certificate()
		if ca_cert:
			c.setopt(c.CAINFO, ca_cert)
		else:
			c.setopt(c.SSL_VERIFYPEER,False)
	if curl_opt == '-o':
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.USERAGENT, hdr)
		try:
			f = open(picn_op,'wb')
			c.setopt(c.WRITEDATA, f)
		except:
			return 0
		
		try:
			c.perform()
			c.close()
		except:
			print('failure in obtaining image try again')
			pass
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
		elif curl_opt == '-e':
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
		elif curl_opt == '-bc':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
			c.setopt(c.COOKIEJAR,cookie_file)
			c.setopt(c.COOKIEFILE,cookie_file)
		elif curl_opt == '-L':
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
		elif curl_opt == '-d':
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
			c.setopt(c.POSTFIELDS,postfield)
		elif curl_opt == '-b':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
			c.setopt(c.COOKIEFILE,cookie_file)
		else:
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
		try:
			c.perform()
			c.close()
			content = storage.getvalue()
			content = getContentUnicode(content)
		except:
			print('curl failure try again')
			content = ''
		return content

def get_ca_certificate():
	ca_cert = ''
	if os.name == 'nt':
		try:
			import certifi
			ca_cert = certifi.where()
		except Exception as e:
			print(e)
	return ca_cert

def _get_video_val(htm,c_file,q,u):
		
		st =''
		quality = q
		#x = ccurl(url+'#'+'-b'+'#'+c_file)
		
		cookie_file = c_file
		html = htm
		url = u
		soup = BeautifulSoup(html,'lxml')
		#title_page = soup.find('title').text.strip().lower()
		if 'Are You Human' in html:
			return ('Nothing',False,True,'txt')
		server_found = True
		if 'kissanime' in url:
			server_found = False
			mir = soup.findAll('select',{'id':'selectServer'})
			for i in mir:
				j = i.findAll('option')
				for k in j:
					ltxt = k.text.lower()
					if ltxt == 'kissanime':
						server_found = True
					print(ltxt,server_found)
			if not server_found:
				html = ccurl(url+'&s=beta'+'#'+'-b'+'#'+c_file)
				soup = BeautifulSoup(html,'lxml')
			m = soup.findAll('select',{'id':'slcQualix'})
		else:
			m = soup.findAll('select',{'id':'selectQuality'})
		#print(m,'---select--quality---')
		if m:
			#print(m)
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
			
			#print(arr_dict)
			
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
					
				if 'kissanime' in url:
					st = "$('#slcQualix').val("+'"'+txt+'"'+")"
				else:
					st = "$('#selectQuality').val("+'"'+txt+'"'+")"
				return (st,server_found,False,txt)


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

class NetWorkManager(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
	netS = pyqtSignal(str)
	def __init__(self,parent,quality,url):
		super(NetWorkManager, self).__init__(parent)
		self.quality = quality
		self.url = url
	def interceptRequest(self,info):
		t = info.requestUrl()
		urlLnk = t.url()
		block_url = ''
		
		lower_case = urlLnk.lower()
		#lst = []
		lst = ["doubleclick.net" ,"ads",'.jpg','.gif','.css','facebook','.aspx', r"||youtube-nocookie.com/gen_204?", r"youtube.com###watch-branded-actions", "imagemapurl","b.scorecardresearch.com","rightstuff.com","scarywater.net","popup.js","banner.htm","_tribalfusion","||n4403ad.doubleclick.net^$third-party",".googlesyndication.com","graphics.js","fonts.googleapis.com/css","s0.2mdn.net","server.cpmstar.com","||banzai/banner.$subdocument","@@||anime-source.com^$document","/pagead2.","frugal.gif","jriver_banner.png","show_ads.js",'##a[href^="http://billing.frugalusenet.com/"]',"http://jriver.com/video.html","||animenewsnetwork.com^*.aframe?","||contextweb.com^$third-party",".gutter",".iab",'http://www.animenewsnetwork.com/assets/[^"]*.jpg','revcontent']
		block = False
		for l in lst:
			if lower_case.find(l) != -1:
				block = True
				break
		if block:
			info.block(True)
			
			
class BrowserPage(QWebEnginePage):  
	cookie_signal = pyqtSignal(str)
	media_signal = pyqtSignal(str)
	media_received = pyqtSignal(str)
	#val_signal = pyqtSignal(str)
	def __init__(self,url,quality,add_cookie,c_file,m_val,v_e,end_pt=None,get_cookie=None,domain_name=None):
		super(BrowserPage, self).__init__()
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		self.cookie_file = c_file
		self.tmp_dir,self.new_c = os.path.split(self.cookie_file)
		x = ''
		self.m = self.profile().cookieStore()
		self.profile().setHttpUserAgent(self.hdr)
		self.loadFinished.connect(self._loadFinished)
		self.loadProgress.connect(self._loadProgress)
		self.loadStarted.connect(self._loadstart)
		p = NetWorkManager(self,quality,url)
		p.netS.connect(lambda y = x : self.urlMedia(y))
		self.media_received.connect(lambda y = x : self.urlMedia(y))
		self.profile().setRequestInterceptor(p)
		#self.profile().clearHttpCache()
		self.profile().setCachePath(self.tmp_dir)
		self.profile().setPersistentStoragePath(self.tmp_dir)
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
		self.value_encode = v_e
		if end_pt:
			self.end_point = end_pt
		else:
			self.end_point = 'cf_clearance'
		self.domain_name = domain_name
		if self.domain_name:
			if self.domain_name.lower() == 'none':
				self.domain_name = None
		self.get_cookie = get_cookie
		if not self.add_cookie:
			self.m.deleteAllCookies()
			self.set_cookie(self.cookie_file)
			
		self.got_cookie = False
		self.text = ''
		self.final_url_got = False
		if self.add_cookie:
			self.m.deleteAllCookies()
			self.m.cookieAdded.connect(lambda  x = t : self._cookie(x))
			
	@pyqtSlot(str)
	def urlMedia(self,info):
		lnk = os.path.join(self.tmp_dir,'lnk.txt')
		if os.path.exists(lnk):
			os.remove(lnk)
		print('*******')
		print(info)
		f = open(lnk,'w')
		f.write(info)
		if 'kissanime' in self.url and self.url.endswith('&s=beta'):
			f.write('\n'+self.url)
		f.close()
		self.media_signal.emit(info)
		print('********')
		
	@pyqtSlot(str)
	def val_found(self,info):
		print(info,'*******info*********')
		#self.page().runJavaScript(info)
		self.val = info
	
	def javaScriptAlert(self,url,msg):
		print(msg,'--msg--',url.url())
		
	def set_cookie(self,cookie_file):
		cookie_arr = QtNetwork.QNetworkCookie()
		c = []
		f = open(cookie_file,'r')
		lines = f.readlines()
		f.close()
		for i in lines:
			k = re.sub('\n','',i)
			if k:
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
		
		if 'kissanime' in self.url:
			self._writeCookies(l)
			if ('idtz' in l) :
				self.cookie_signal.emit("Cookie Found")
		else :
			#print(l)
			#if self.add_cookie:
			if not self.got_cookie:
				self._writeCookies(l)
			if self.end_point in l and not self.got_cookie:
				self.cookie_signal.emit("Cookie Found")
				self.got_cookie = True
			#f = open('/tmp/ck.txt','w')
			#f.close()
			print('------cf----------')
		
			
		#self.setHtml('<html>cookie Obtained</html>')
		#self.page().toHtml(lambda x = result: self.htm(x))
		
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
		#print(d)
		return(d)
		
	def _writeCookies(self,i):
		cfc = ''
		cfd = ''
		asp = ''
		idt = ''
		utmc = ''
		reqkey = ''
		dm = False
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
		if cfc or cfd or asp or idt or utmc or dm:
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
			if idt:
				str1 = idt['domain']+'	'+'FALSE'+'	'+idt['path']+'	'+'FALSE'+'	'+str(0)+'	'+'idtz'+'	'+idt['idtz']
			if utmc:
				str1 = utmc['domain']+'	'+'FALSE'+'	'+utmc['path']+'	'+'FALSE'+'	'+str(0)+'	'+'__utmc'+'	'+utmc['__utmc']
			if reqkey:
				str1 = reqkey['domain']+'	'+'FALSE'+'	'+reqkey['path']+'	'+'FALSE'+'	'+reqkey['expiry']+'	'+reqkey['name_id']+'	'+reqkey[reqkey['name_id']]
			cc = os.path.join(self.tmp_dir,'cloud_cookie.txt')
			if not os.path.exists(cc):
				f = open(cc,'w')
				f.write(str1)
			else:
				f = open(cc,'a')
				f.write('\n'+str1)
			#print('written--cloud_cookie--------------')
			print(str1,'--496--')
			f.close()
			content = open(cc).read()
			print(content,'--499--')
			
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
		
		self.js = ''
		if 'checking_browser' not in x:
			if 'slcQualix' in x or 'selectQuality' in x:
				self.value_encode = parse_file(x,self.url,self.quality)
				if self.value_encode:
					if 'slcQualix' in x:
						print(self.value_encode)
						self.runJavaScript('ovelWrap("{0}");'.format(self.value_encode),self.val_scr)
						#self.runJavaScript('window'.format(self.value_encode),self.val_scr)
					else:
						self.runJavaScript('$kissenc.decrypt("{0}");'.format(self.value_encode),self.val_scr)
						
	def _loadstart(self):
		result = ''
		#self.cnt = 0
		
	def htm_src(self,x):
		html = x
		if 'var glink = ' in html:
			c_f = os.path.join(self.tmp_dir,'cloud_cookie.txt')
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
		val = str(x)
		print(val)
		if val.startswith('http') and not self.final_url_got:
			y1 = re.findall("http[^']*",val)
			print(y1)
			for y in y1:
				content = ccurl(y+'#'+'-I')
				if "Location:" in content:
					m = re.findall('Location: [^\n]*',content)
					url = re.sub('Location: |\r','',m[-1])
				else:
					url = y
				self.media_received.emit(url)
				self.final_url_got = True
				print(url)
		print('===============java----------scr')
		
	def _loadProgress(self):
		result =''
		if (('kimcartoon' in self.url or 'kissasian' in self.url or 'kissanime' in self.url) 
				and ('id=' in self.url) and self.got_cookie):
			if self.val or 'kissanime' in self.url:
				x = self.toHtml(self.htm)
				#self.runJavaScript(self.val,self.val_scr)
			
		self.cnt = self.cnt+1
		
	def _loadFinished(self):
		result = ""
		print('Finished')
		

class BrowseUrlT(QWebEngineView):
	#cookie_s = pyqtSignal(str)
	def __init__(self,url,quality,cookie,end_point=None,get_cookie=None,domain_name=None):
		super(BrowseUrlT, self).__init__()
		#QtWidgets.__init__()
		self.url = url
		self.add_cookie = True
		self.quality = quality
		self.media_val = ''
		self.cnt = 0
		self.cookie_file = cookie
		self.value_encode = ''
		if end_point:
			self.end_pt = end_point
		else:
			self.end_pt = 'cf_clearance'
		self.domain_name = domain_name
		print(self.end_pt,get_cookie)
		self.tmp_dir,self.new_c = os.path.split(self.cookie_file)
		self.get_cookie = get_cookie
		self.Browse(self.url)
		
	def Browse(self,url):
		print('---browse---591---')
		captcha = False
		if os.path.exists(self.cookie_file) and not self.get_cookie:
			content = ccurl(url+'#'+'-b'+'#'+self.cookie_file)
			print(content)
			if 'checking_browser' in content or self.get_cookie:
				os.remove(self.cookie_file)
				self.add_cookie = True
			else:
				self.add_cookie = False
				if ('kimcartoon' in url or 'kissasian' in url or 'kissanime' in url) and self.quality and ('id=' in url):
					#print("--------------------",content)
					try:
						self.media_val,server_found,captcha,self.value_encode = _get_video_val(content,self.cookie_file,self.quality,url)
					except Exception as e:
						print(e,'--622--')
						server_found = ''
					if not server_found:
						url = url + '&s=beta'
					print(self.media_val,'--media--val--')
		else:
			self.add_cookie = True
		
		self.tab_web = QtWidgets.QWidget()
		self.tab_web.setMaximumSize(500,500)
		self.tab_web.setWindowTitle('Wait!')
		self.horizontalLayout_5 = QtWidgets.QVBoxLayout(self.tab_web)
		self.horizontalLayout_5.addWidget(self)
		
		if self.add_cookie:
			self.web = BrowserPage(url,self.quality,self.add_cookie,self.cookie_file,self.media_val,self.value_encode,end_pt=self.end_pt,get_cookie=self.get_cookie,domain_name=self.domain_name)
			
			self.web.cookie_signal.connect(self.cookie_found)
			self.web.media_signal.connect(self.media_source_found)
			self.setPage(self.web)
			print('add_cookie')
			self.load(QUrl(url))
			print('--')
			#self.load(QUrl(url))
			self.cnt = 1
		elif ('kimcartoon' in url or 'kissasian' in url or 'kissanime' in url) and self.quality and ('id=' in url):
			print('+++++++++++++++++++')
			self.tab_web.setWindowTitle('Wait! Resolving Link')
			self.web = BrowserPage(url,self.quality,self.add_cookie,self.cookie_file,self.media_val,self.value_encode,end_pt=self.end_pt,get_cookie=self.get_cookie,domain_name=self.domain_name)
			self.web.got_cookie = True
			self.web.cookie_signal.connect(self.cookie_found)
			self.web.media_signal.connect(self.media_source_found)
			self.setPage(self.web)
			self.load(QUrl(url))
		QtWidgets.QApplication.processEvents()
		QtWidgets.QApplication.processEvents()
		print(captcha,'--captcha--')
		if not captcha:
			self.tab_web.hide()
		else:
			self.tab_web.show()
		
		
	@pyqtSlot(str)
	def cookie_found(self):
		#global web
		print('cookie')
		self.add_cookie = False
		if ('id=' in self.url) and ('kimcartoon' in url or 'kissasian' in url or 'kissanime' in url):
			print('Cookie Obtained, now link finding')
			f = open(os.path.join(self.tmp_dir,'tmp_cookie'),'w')
			f.write('Cookie Obtained, now link finding')
			f.close()
			
			#elif 'moetube' in url:
			#self.setHtml('<html>Link Resolved</html>')
		else:
			self.setHtml('<html>cookie Obtained</html>')
		c_f = os.path.join(self.tmp_dir,'cloud_cookie.txt')
		if os.path.exists(c_f):
			content = open(c_f).read()
			print(content,'--676---')
			f = open(self.cookie_file,'w')
			f.write(content)
			f.close()
			os.remove(c_f)
		if ('id=' in self.url) and ('kimcartoon' in url or 'kissasian' in url or 'kissanime' in url):
			sys.exit(0)
	@pyqtSlot(str)
	def media_source_found(self):
		#global web
		#self.setHtml('<html>Media Source Obtained</html>')
		print('media found')
		
	
		

if __name__ == "__main__":
		print('---------------679--------Engine--start--')
		url = sys.argv[1]	
		print(url)
		quality = sys.argv[2]
		print(quality)
		cookie = sys.argv[3]
		end_pt = sys.argv[4]
		get_cookie = sys.argv[5]
		if get_cookie == 'true':
			get_cookie = True
		else:
			get_cookie = False
		dm = sys.argv[6]
		app = QtWidgets.QApplication(sys.argv)
		print(url,quality,cookie,'--685---',end_pt)
		web = BrowseUrlT(url,quality,cookie,end_point=end_pt,get_cookie=get_cookie,domain_name=dm)
		ret = app.exec_()
		sys.exit(ret)

