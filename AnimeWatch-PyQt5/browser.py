"""
Copyright (C) 2016 kanishka-linux kanishka.linux@gmail.com

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


from PyQt5 import QtCore, QtGui,QtNetwork,QtWidgets
import sys
import urllib
import urllib3
import pycurl
from io import StringIO,BytesIO
import re
import subprocess
import os.path
from subprocess import check_output
from bs4 import BeautifulSoup

from PyQt5 import QtWebEngineWidgets,QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
	
from PyQt5.QtNetwork import QNetworkAccessManager
from PyQt5.QtCore import QUrl

#from adb import NetWorkManager

import time
from yt import get_yt_url
from PyQt5.QtCore import (QCoreApplication, QObject, Q_CLASSINFO, pyqtSlot,pyqtSignal,
                          pyqtProperty)




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
	postfield = ''
	if '#' in url:
		curl_opt = nUrl.split('#')[1]
		url = nUrl.split('#')[0]
		if curl_opt == '-o':
			picn_op = nUrl.split('#')[2]
		elif curl_opt == '-Ie' or curl_opt == '-e':
			rfr = nUrl.split('#')[2]
		elif curl_opt == '-Icb' or curl_opt == '-bc':
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
		else:
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
		c.perform()
		c.close()
		content = storage.getvalue()
		content = getContentUnicode(content)
		return content
		

class MyPage(QtWebEngineWidgets.QWebEnginePage):
	def __init__(self):
		super(MyPage, self).__init__()
		
	def acceptNavigationRequest(self, url, nav_type,frame):
		#print(url,nav_type,'--print--nav--type--')
		if nav_type == 0:
			print('clicked')
			#self.parent.urlSignal.emit(url.url())
		return super(MyPage, self).acceptNavigationRequest(url,nav_type,frame)
		
class NetWorkManager(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
	
	def __init__(self,parent):
		super(NetWorkManager, self).__init__(parent)
		self.p = parent
	def interceptRequest(self,info):
		t = info.requestUrl()
		urlLnk = t.url()
		
		
		lower_path = urlLnk.lower()
		
		block_list = ["doubleclick.net",'adnxs','facebook','.aspx', r"||youtube-nocookie.com/gen_204?", r"youtube.com###watch-branded-actions", "imagemapurl","b.scorecardresearch.com","rightstuff.com","scarywater.net","popup.js","banner.htm","_tribalfusion","||n4403ad.doubleclick.net^$third-party",".googlesyndication.com","graphics.js","fonts.googleapis.com/css","s0.2mdn.net","server.cpmstar.com","||banzai/banner.$subdocument","@@||anime-source.com^$document","/pagead2.","frugal.gif","jriver_banner.png","show_ads.js",'##a[href^="http://billing.frugalusenet.com/"]',"http://jriver.com/video.html","||animenewsnetwork.com^*.aframe?","||contextweb.com^$third-party",".gutter",".iab",'http://www.animenewsnetwork.com/assets/[^"]*.jpg','revcontent']
		block = False
		for l in block_list:
			if l in lower_path:
				block = True
				break
		try:
			if self.p.wait_player:
				if 'itag=' in urlLnk:
					block = True
					#print(urlLnk,'--urlLnk--')
					#a = 0
		except:
			pass
		if block:
			info.block(True)
class Browser(QtWebEngineWidgets.QWebEngineView):
	urlSignal = pyqtSignal(str)
	def __init__(self,ui,home,screen_width,quality,site,epnArrList):
		super(Browser, self).__init__()
		
		self.epn_name_in_list = ''
		self.wait_player = False
		#self.action_arr = []
		#self.threadPool = []
		self.home = home
		self.ui = ui
		self.quality = quality
		self.site = site
		self.epnArrList = epnArrList
		self.pg = MyPage()
		self.setPage(self.pg)
		if self.ui.btnWebReviews.currentText() == 'Youtube':
			self.hdr = 'Mozilla/5.0 (Linux; Android 4.4.4; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'
		else:
			self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		#self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		#self.m = self.profile().cookieStore()
		#self.page().profile().QWebEngineProfile()
		#profile_ = QtWebEngineWidgets.QWebEngineProfile(self)
		#self.page().profile().NoPersistentCookies
		#self.page().profile().cookieStore().deleteAllCookies()
		self.page().profile().setHttpUserAgent(self.hdr)
		p = NetWorkManager(self)
		self.page().profile().setRequestInterceptor(p)
		#self.profile().clearHttpCache()
		cache_path = os.path.join(home,'Cache')
		print(cache_path,'--cache--path--')
		if not os.path.exists(cache_path):
			os.makedirs(cache_path)
		#self.page().profile().setCachePath('/tmp/AnimeWatch')
		#self.page().profile().setPersistentStoragePath('/tmp/AnimeWatch')
		self.page().profile().setCachePath(cache_path)
		self.page().profile().setPersistentStoragePath(cache_path)
		self.page().linkHovered.connect(self.custom_links)
		self.urlChanged.connect(self.url_changed)
		self.hoveredLink = ''
		self.media_url = ''
		#self.loadFinished.connect(self._load_finished)
		#self.loadStarted.connect(self._load_started)
		self.titleChanged.connect(self.title_changed)
		self.loadProgress.connect(self.load_progress)
		self.current_link = ''
		self.title_page = ''
		#ui.tab_2.showMaximized()
		self.ui.tab_2.setMaximumWidth(screen_width)
		self.url_arr = []
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.player_wait)
		self.timer.setSingleShot(True)
		self.urlSignal.connect(self.final_found)
	@pyqtSlot(str)
	def final_found(self,final_url):
		print(final_url,'clicked')
		if final_url:
			print(final_url,'--youtube--')
			self.ui.watchDirectly(final_url,self.epn_name_in_list,'yes')
			self.ui.tab_5.show()
			self.ui.frame1.show()
			self.ui.tab_2.setMaximumWidth(400)
	def player_wait(self):
		#global wait_player
		self.wait_player = False
		self.page().runJavaScript("location.reload();",self.var_remove)
	def get_html(self,var):
		print('--got--html--')
		if 'youtube.com' in self.url().url():
		
			
					
			soup = BeautifulSoup(var,'lxml')
			m = soup.find('div',{'id':'player'})
			
			if m:
				print('removing')
				#self.page().runJavaScript("var element = document.getElementById('player');element.parentNode.removeChild(element);",self.var_remove)
				self.page().runJavaScript("var element = document.getElementById('player');element.innerHtml='';",self.var_remove)
			title = soup.find('title')
			if title:
				if self.current_link.startswith("https://m.youtube.com/watch?v=") or self.current_link.startswith("https://www.youtube.com/watch?v="):
					self.epn_name_in_list = title.text
					self.ui.epn_name_in_list = title.text
					#self.clicked_link(self.current_link)
			print(title,self.url().url(),'--changed-title--')
		
	def var_remove(self,var):
		print(var,'--js--')
	def load_progress(self,var):
		if var == 100 and 'youtube.com' in self.url().url():
			print(self.url(),self.title(),'--load--progress--')
			self.page().toHtml(self.get_html)
	def title_changed(self,title):
		a = 0
	def url_changed(self,link):
		
		if not self.url_arr:
			self.url_arr.append(link.url())
			prev_url = ''
		else:
			prev_url = self.url_arr[-1]
			self.url_arr.append(link.url())
			
		if prev_url != link.url() and 'youtube.com' in link.url():
			self.current_link = link.url()
			m = []
			if '/watch?' in link.url():
				a = link.url().split('?')[-1]
				b = a.split('&')
				if b:
					for i in b:
						j = i.split('=')
						k = (j[0],j[1])
						m.append(k)
				else:
					j = a.split('=')
					k = (j[0],j[1])
					m.append(k)
				d = dict(m)
				print(d,'----dict--arguments---generated---')
				try:
					self.current_link = 'https://m.youtube.com/watch?v='+d['v']
				except:
					pass
			if (self.current_link.startswith("https://m.youtube.com/watch?v=") or self.current_link.startswith("https://www.youtube.com/watch?v=")) and not self.wait_player:
				self.page().runJavaScript("var element = document.getElementById('player');element.innerHtml='';",self.var_remove)
				#self.page().runJavaScript("var element = document.getElementById('player');element.parentNode.removeChild(element);",self.var_remove)
				self.wait_player = True
				self.clicked_link(self.current_link)
				#asyncio.get_event_loop().run_until_complete(self.clicked_link(self.current_link))
				self.timer.start(1000)
				
				
		#print(self.url_arr)
	
	def clicked_link(self,link):
		
		final_url = ''
		url = link
		self.epn_name_in_list = self.title_page
		print(url,'clicked_link')
		if 'youtube.com/watch?v=' in url:
			if self.ui.mpvplayer_val.pid() > 0:
				self.ui.mpvplayer_val.kill()
			final_url = get_yt_url(url,self.ui.quality_val)
			if final_url:
				print(final_url,'--youtube--')
				self.ui.watchDirectly(final_url,self.epn_name_in_list,'yes')
				self.ui.tab_5.show()
				self.ui.frame1.show()
				self.ui.tab_2.setMaximumWidth(400)
	def custom_links(self,q_url):
		url = q_url
		self.hoveredLink = url
		
	def urlHeaders(self,url):
		m =[]
		o = []
		content = ccurl(url+'#'+'-I')
		n = content.split('\n')
		#print(n)
		k = 0
		for i in n:
			i = re.sub('\r','',i)
			if i and ':' in i:
				p = i.split(': ',1)
				if p:
					t = (p[0],p[1])
				else:
					t = (i,"None")
				
				m.append(t)
				#print(m,'-----')
				k = k+1
				#print(k)
			else:
				t = (i,'')
				m.append(t)
		d = dict(m)
		print(d)
		#result = int(int(d['Content-Length'])/(1024*1024))
		return d
	
	def keyPressEvent(self, event):
		
		if event.modifiers() == QtCore.Qt.AltModifier and event.key() == QtCore.Qt.Key_Left:
			self.back()
		elif event.modifiers() == QtCore.Qt.AltModifier and event.key() == QtCore.Qt.Key_Right:
			self.forward()
		super(Browser, self).keyPressEvent(event)
		
	def triggerPlaylist(self,value,url,title):
		print ('Menu Clicked')
		print (value)
		file_path = os.path.join(self.home,'Playlists',str(value))
		if '/' in title:
			title = title.replace('/','-')
		print(title,url,file_path)
		t = title + '	'+url+'	'+'NONE'
		if os.stat(file_path).st_size == 0:
			f = open(file_path,'w')
		else:
			f = open(file_path,'a')
			t = '\n'+t
		try:
			f.write(str(t))
		except:
			f.write(t)
		f.close()
		self.ui.update_playlist(file_path)
	def contextMenuEvent(self, event):
		self.media_url = ''
		menu = self.page().createStandardContextMenu()
		try:
			data = self.page().contextMenuData()
			url = data.linkUrl().url()
			self.title_page = data.linkText()
			try:
				#self.title_page = self.title_page.strip()
				tmp = self.title_page.replace('\n','#')
				print(tmp)
				tmp = re.search('[#][^#]*',tmp)
				print(tmp)
				self.title_page = tmp.group()
				self.title_page = self.title_page.replace('#','')
			except:
				pass
			self.epn_name_in_list = self.title_page
			print(data.mediaUrl().url(),data.mediaType(),data.linkText(),data.linkUrl().url(),'--media--url--and--type--')
			if data.mediaType() == 1:
				self.media_url = data.mediaUrl().url()
				if not self.media_url.startswith('http'):
					self.media_url = ''
					print('--no--image-url--')
				print(data.mediaUrl().url(),'--media-url--image--')
			
		except:
			url = self.hoveredLink
			pass
		print(url)
		if not url.startswith('http'):
			url = self.media_url
			print(url)
			
		arr = ['Download As Fanart','Download As Cover']
		arr_extra_tvdb = ['Series Link','Season Episode Link']
		arr_last = ['Artist Link']
		action = []
		yt = False
		if url or self.media_url:
			if url:
				if 'tvdb' in url:
					arr = arr + arr_extra_tvdb
				if 'last.fm' in url:
					arr = arr + arr_last
				if 'youtube.com' in url:
					yt = True
					arr[:]=[]
					arr.append('Play with AnimeWatch')
					arr.append('Download')
					#self.page().profile().setHttpUserAgent(self.hdr1)
				
					menu.addSeparator()
					submenuR = QtWidgets.QMenu(menu)
					submenuR.setTitle("Add To Playlist")
					menu.addMenu(submenuR)
					pls = os.listdir(os.path.join(self.home,'Playlists'))
					home1 = os.path.join(self.home,'Playlists')
					pls = sorted(pls,key = lambda x:os.path.getmtime(os.path.join(home1,x)),reverse=True)
					item_m = []
					for i in pls:
						item_m.append(submenuR.addAction(i))
					
					submenuR.addSeparator()
					new_pls = submenuR.addAction("Create New Playlist")
			
			for i in range(len(arr)):
				action.append(menu.addAction(arr[i]))
				
			act = menu.exec_(event.globalPos())
			
			for i in range(len(action)):
				if act == action[i]:
					self.download(url,arr[i])
			if yt:
				for i in range(len(item_m)):
					if act == item_m[i]:
						self.triggerPlaylist(pls[i],url,self.epn_name_in_list)
				
				
				if act == new_pls:
					print ("creating")
					MainWindow = QtWidgets.QWidget()
					item, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Input Dialog', 'Enter Playlist Name')
					if ok and item:
						file_path = os.path.join(self.home,'Playlists',item)
						if not os.path.exists(file_path):
							f = open(file_path,'w')
							f.close()
			#j = j+1
		#menu.exec_(event.globalPos())
		else:
			if 'youtube.com/watch?v=' in self.url().url():
				self.title_page = self.title()
				arr = ['Play with AnimeWatch','Download']
				action = []
				menu.addSeparator()
				
				submenuR = QtWidgets.QMenu(menu)
				submenuR.setTitle("Add To Playlist")
				menu.addMenu(submenuR)
				pls = os.listdir(os.path.join(self.home,'Playlists'))
				home1 = os.path.join(self.home,'Playlists')
				pls = sorted(pls,key = lambda x:os.path.getmtime(os.path.join(home1,x)),reverse=True)
				item_m = []
				for i in pls:
					item_m.append(submenuR.addAction(i))
				
				submenuR.addSeparator()
				new_pls = submenuR.addAction("Create New Playlist")
				
				for i in range(len(arr)):
					action.append(menu.addAction(arr[i]))
					
				act = menu.exec_(event.globalPos())
				
				for i in range(len(action)):
					if act == action[i]:
						self.download(self.url().url(),arr[i])
				
				for i in range(len(item_m)):
					if act == item_m[i]:
						self.triggerPlaylist(pls[i],self.url().url(),self.title_page)
				
				
				if act == new_pls:
					print ("creating")
					MainWindow = QtWidgets.QWidget()
					item, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Input Dialog', 'Enter Playlist Name')
					if ok and item:
						file_path = os.path.join(self.home,'Playlists',item)
						if not os.path.exists(file_path):
							f = open(file_path,'w')
							f.close()
			elif 'tvdb' in self.url().url() or 'last.fm' in self.url().url():
				print(self.url().url(),'--tvdb-url--')
				if 'tvdb' in self.url().url():
					arr = arr + arr_extra_tvdb
				if 'last.fm' in self.url().url():
					arr = arr + arr_last
			
				for i in range(len(arr)):
					action.append(menu.addAction(arr[i]))
					
				act = menu.exec_(event.globalPos())
				
				for i in range(len(action)):
					if act == action[i]:
						self.download(self.url().url(),arr[i])
			else:
				super(Browser, self).contextMenuEvent(event)
	def getContentUnicode(self,content):
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
	def ccurlT(self,url,rfr):
		hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		content = ccurl(url)
		return content
	def download(self, url,option):
		
		if option.lower() == 'play with animewatch':
			final_url = ''
			self.ui.epn_name_in_list = self.title_page
			print(self.ui.epn_name_in_list)
			if self.ui.mpvplayer_val.pid() > 0:
				self.ui.mpvplayer_val.kill()
			final_url = get_yt_url(url,self.ui.quality_val)
			if final_url:
				self.ui.watchDirectly(final_url,self.ui.epn_name_in_list,'yes')
				self.ui.tab_5.show()
				self.ui.frame1.show()
				self.ui.tab_2.setMaximumWidth(400)
		elif option.lower() == 'download':
			if self.ui.quality_val == 'sd480p':
				txt = "Video can't be saved in 480p, Saving in either HD or SD"
				subprocess.Popen(['notify-send',txt])
				quality = 'hd'
			else:
				quality = self.ui.quality_val
			finalUrl = get_yt_url(url,quality)
			finalUrl = finalUrl.replace('\n','')
			title = self.title_page+'.mp4'
			title = title.replace('"','')
			title = title.replace('/','-')
			if os.path.exists(self.ui.default_download_location):
				title = os.path.join(self.ui.default_download_location,title)
			else:
				title = '/tmp/AnimeWatch/'+title
			command = "wget -c --user-agent="+'"'+self.hdr+'" '+'"'+finalUrl+'"'+" -O "+'"'+title+'"'
			print (command)		
			self.ui.infoWget(command,0)
		elif option.lower() == 'season episode link':
			
			if self.site != "Music" and self.site != "PlayLists":
				self.ui.getTvdbEpnInfo(url)
				
		elif option.lower() == 'artist link' or option.lower() == 'series link':
			self.ui.posterfound(url)
			self.ui.copyImg()
			self.ui.copySummary()
		else:
			print ("Hello")
			hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
			if url:
				url1 = str(url)
			else:
				url1 = self.media_url
			print (url1)
			url_artist = url1
			found = ""
			final_found = False
			url1Code = url1.split('/')[-1]
			#dict_tmp = self.urlHeaders(url1)
			#content_type = dict_tmp['Content-Type']
			t_content = ccurl(url1+'#'+'-I')
			if 'image/jpeg' in t_content and not 'Location:' in t_content:
				final_found = True
			elif 'image/jpeg' in t_content and 'Location:' in t_content:
				m = re.findall('Location: [^\n]*',t_content)
				found = re.sub('Location: |\r','',m[0])
				url1 = found
				final_found = True
			elif self.media_url:
				url1 = self.media_url
				final_found = True
			else:
				return 0
			print(url1,'----------image-url----------')
			if self.site == "Music":
				if (self.ui.list3.currentItem().text())=="Artist":
					name = str(self.ui.list1.currentItem().text())
				else:
					r = self.ui.list2.currentRow()
					name = self.epnArrList[r].split('	')[2]
			else:
				name = str(self.ui.list1.currentItem().text())
				
			if '/' in name:
					name = name.replace('/','-')
					
			if (url1.endswith('.jpg') or final_found) and (self.site!='Music'):
				final = url1
				if self.site == "Local":
					if name.startswith('@'):
						name1 = name.split('@')[-1]
					else:
						name1 = name
					thumb = '/tmp/AnimeWatch/'+name1+'.jpg'
				else:
					thumb = '/tmp/AnimeWatch/'+name+'.jpg'
				#subprocess.call(["curl",'-A',self.hdr,'-L',"-o",thumb,final])
				ccurl(final+'#'+'-o'+'#'+thumb)
			else:
				if self.site == "Music" and (option == "Download As Fanart" or option == "Download As Cover"):
					if 'last.fm' in url1:
						print(url1,'--artist-link---')
						#content = self.ccurl(url1,'')
						content = ccurl(url1)
						soup = BeautifulSoup(content,'lxml')
						link = soup.findAll('img')
						
						for i in link:
							if 'src' in str(i):
								j = i['src']
								k = j.split('/')[-1]
								if url1Code == k:
									found = j
									break
						print (str(found))
						u1 = found.rsplit('/',2)[0]
						u2 = found.split('/')[-1]
						final = u1 + '/770x0/'+u2
						print (final)
					elif final_found:
						final = url1
					else:
						final = ''
					if '/' in name:
						name = name.replace('/','-')
					thumb = '/tmp/AnimeWatch/'+name+'.jpg'
					try:
						if final.startswith('http'):
							ccurl(final+'#'+'-o'+'#'+thumb)
					except:
						pass
			print (option)
			if str(option) == "Download As Fanart":
				self.ui.copyFanart()
			elif str(option) == "Download As Cover":
				self.ui.copyImg()
								
	def finishedDownload(self):
		self.ui.copyImg()
