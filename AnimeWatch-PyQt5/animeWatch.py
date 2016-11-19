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
import os
import sys

BASEDIR,BASEFILE = os.path.split(os.path.abspath(__file__))

print(BASEDIR,BASEFILE,os.getcwd())

sys.path.append(BASEDIR)

from PyQt5 import QtCore, QtGui,QtNetwork,QtWidgets

import urllib
import urllib3
import pycurl
from io import StringIO,BytesIO
import re
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup

try:
	from PyQt5 import QtWebEngineWidgets,QtWebEngineCore
	from PyQt5.QtWebEngineWidgets import QWebEngineView
	from adb import NetWorkManager
	from browser import Browser
	QT_WEB_ENGINE = True
except:
	from PyQt5 import QtWebKitWidgets
	from PyQt5.QtWebKitWidgets import QWebView
	from adb_webkit import NetWorkManager
	from browser_webkit import Browser
	QT_WEB_ENGINE = False
	


from PyQt5.QtCore import QUrl
import imp
import shutil
from tempfile import mkstemp,mkdtemp
from player_functions import write_files,ccurl,send_notification,wget_string,open_files,get_config_options,get_tmp_dir

TMPDIR = get_tmp_dir()

if TMPDIR and not os.path.exists(TMPDIR):
	try:
		os.makedirs(TMPDIR)
	except OSError as e:
		print(e)
		TMPDIR = mkdtemp(suffix=None,prefix='AnimeWatch_')
	
OSNAME=os.name

print(TMPDIR,OSNAME)

from shutil import move
from os import remove, close
import time
from PIL import Image 
import PIL
import random
from os.path import expanduser
import textwrap
from functools import partial
import weakref
import datetime
import socket
#import fcntl
import struct
from PyQt5.QtWidgets import QInputDialog
import sqlite3
try:
	import taglib
except:
	pass
from musicArtist import musicArtist
from yt import get_yt_url


from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn,TCPServer

from PyQt5 import QtDBus
from PyQt5.QtCore import (QCoreApplication, QObject, Q_CLASSINFO, pyqtSlot,pyqtSignal,
                          pyqtProperty)
from PyQt5.QtDBus import QDBusConnection, QDBusAbstractAdaptor
try:
	import dbus
	import dbus.service
	import dbus.mainloop.pyqt5
	from mpris_dbus import MprisServer
except:
	from mpris_nodbus import MprisServer


try:
	import libtorrent as lt
	from stream import ThreadServer,TorrentThread,get_torrent_info,set_torrent_info,get_torrent_info_magnet
except:
	notify_txt = 'python3 bindings for libtorrent are broken\nTorrent Streaming feature will be disabled'
	send_notification(notify_txt)
	


"""
def replace_line(file_path, pattern, subst):
	#Create temp file
	fh, abs_path = mkstemp()
	with open(abs_path,'w') as new_file:
		with open(file_path) as old_file:
			for line in old_file:
				new_file.write(line.replace(pattern, subst))
	close(fh)
	#Remove original file
	remove(file_path)
	#Move new file
	move(abs_path, file_path)
"""

		

def get_lan_ip():
	a = subprocess.check_output(['ip','addr','show'])
	b = str(a,'utf-8')
	print(b)
	c = re.findall('inet [^ ]*',b)
	final = ''
	for i in c:
		if '127.0.0.1' not in i:
			final = i.replace('inet ','')
			final = re.sub('/[^"]*','',final)
	print(c)
	print(final)
	return final

def change_config_file(ip,port):
	config_file = os.path.join(os.path.expanduser('~'),'.config','AnimeWatch','other_options.txt')
	new_ip = 'LOCAL_STREAM_IP='+ip+':'+str(port)
	content = open(config_file,'r').read()
	content = re.sub('LOCAL_STREAM_IP=[^\n]*',new_ip,content)
	f = open(config_file,'w')
	f.write(content)
	f.close()

def set_mainwindow_palette(fanart):
	if os.path.isfile(fanart):
		palette	= QtGui.QPalette()
		palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap(fanart)))
		MainWindow.setPalette(palette)


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		global current_playing_file_path,path_final_Url
		print(self.path)
		path = self.path.replace('/','')
		if path.lower() == 'play' or not path:
			
			self.row = ui.list2.currentRow()
			if self.row < 0:
				self.row = 0
			if ui.btn1.currentText().lower() == 'youtube':
				nm = path_final_Url
				if not nm:
					return 0
			else:
				nm = ui.epn_return(self.row)
			if nm.startswith('http'):
				self.send_response(303)
				self.send_header('Location',nm)
				self.end_headers()
			else:
				#ui.list2.setCurrentRow(self.row)
				self.send_response(200)
				self.send_header('Content-type','video/mp4')
				self.end_headers()
				#nm = current_playing_file_path
				nm = nm.replace('"','')
				#nm = nm.replace("'",'')
				f = open(nm,'rb')
				content = f.read()
				self.wfile.write(content)
				#time.sleep(1)
				f.close()
			
		elif path.lower() == 'next':
			self.row = ui.list2.currentRow()+1
			if self.row < 0 or self.row > ui.list2.count()-1:
				self.row = 0
			if ui.btn1.currentText().lower() == 'youtube':
				nm = path_final_Url
				if not nm:
					return 0
			else:
				nm = ui.epn_return(self.row)
			ui.list2.setCurrentRow(self.row)
			if nm.startswith('http'):
				self.send_response(303)
				self.send_header('Location',nm)
				self.end_headers()
			else:
				self.send_response(200)
				self.send_header('Content-type','video/mp4')
				self.end_headers()
				#nm = current_playing_file_path
				nm = nm.replace('"','')
				#nm = nm.replace("'",'')
				f = open(nm,'rb')
				content = f.read()
				self.wfile.write(content)
				#time.sleep(1)
				f.close()
		elif path.lower() == 'prev':
			self.row = ui.list2.currentRow()-1
			if self.row < 0:
				self.row = 0
			if ui.btn1.currentText().lower() == 'youtube':
				nm = path_final_Url
				if not nm:
					return 0
			else:
				nm = ui.epn_return(self.row)
			ui.list2.setCurrentRow(self.row)
			if nm.startswith('http'):
				self.send_response(303)
				self.send_header('Location',nm)
				self.end_headers()
			else:
				self.send_response(200)
				self.send_header('Content-type','video/mp4')
				self.end_headers()
				#nm = current_playing_file_path
				nm = nm.replace('"','')
				#nm = nm.replace("'",'')
				f = open(nm,'rb')
				content = f.read()
				self.wfile.write(content)
				#time.sleep(1)
				f.close()
		else:
			nm = 'index.html'
			self.send_header('Content-type','text/html')
		
		
		return 0

class ThreadedHTTPServerLocal(ThreadingMixIn, HTTPServer):
	pass

class MyTCPServer(TCPServer):
	def server_bind(self):
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(self.server_address)
				
class ThreadServerLocal(QtCore.QThread):
	
	def __init__(self,ip,port):
		
		QtCore.QThread.__init__(self)
		self.ip = ip
		self.port = int(port)
	def __del__(self):
		self.wait()                        
	
	def run(self):
		global httpd
		print('starting server...')
		try:
			server_address = (self.ip,self.port)
			#httpd = ThreadedHTTPServerLocal(server_address, HTTPServer_RequestHandler)
			httpd = MyTCPServer(server_address, HTTPServer_RequestHandler)
		except OSError as e:
			e_str = str(e)
			print(e_str)
			if 'errno 99' in e_str.lower():
				txt = 'Your local IP changed..or port is blocked.\n..Trying to find new IP'
				#subprocess.Popen(['notify-send',txt])
				send_notification(txt)
				self.ip = get_lan_ip()
				txt = 'Your New Address is '+self.ip+':'+str(self.port) + '\n Please restart the player'
				#subprocess.Popen(['notify-send',txt])
				send_notification(txt)
				change_config_file(self.ip,self.port)
				server_address = (self.ip,self.port)
				httpd = MyTCPServer(server_address, HTTPServer_RequestHandler)
				#httpd = ThreadedHTTPServerLocal(server_address, HTTPServer_RequestHandler)
			else:
				pass
		print('running server...at..'+self.ip+':'+str(self.port))
		#httpd.allow_reuse_address = True
		httpd.serve_forever()
		print('quitting http server')


class ThreadingExample(QtCore.QThread):
    
	def __init__(self,name):
		QtCore.QThread.__init__(self)
	
		self.name1 = name
		self.interval = 1

	def __del__(self):
		self.wait()                        
	def ccurlT(self,url,rfr):
		hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		content = ccurl(url)
		return content
	def run(self):
		name = self.name1
		name2 = name.replace(' ','+')
		if name2 != 'NONE':
			url = "http://www.last.fm/search?q="+name2
			print (url)
			
			
			print (url)
			wiki = ""
			#content = self.ccurl(url,'')
			content = ccurl(url)
			#print (content)
			soup = BeautifulSoup(content,'lxml')

			link = soup.findAll('div',{'class':'row clearfix'})
			#print link
			#print (link)
			name3 = ""
			for i in link:
				j = i.findAll('a')
				#print (j)
				for k in j:
					try:
						url = k['href']
						print (url)
						#name3 = k.text
						break
					except:
						pass
			print (url)
			
			print (url)
			if url.startswith('http'):
				url = url
			else:
				url = "http://www.last.fm" + url
			
			print (url)
			img_url = url+'/+images'
			wiki_url = url + '/+wiki'
			print (wiki_url)
			#content = self.ccurl(wiki_url,'')
			content = ccurl(wiki_url)
			soup = BeautifulSoup(content,'lxml')
			link = soup.find('div',{'class':'wiki-content'})
			#print (link)

			if link:
				
				wiki = link.text
				#print wiki

			#content = self.ccurl(img_url,'')
			content = ccurl(img_url)
			soup = BeautifulSoup(content,'lxml')
			link = soup.findAll('ul',{'class':'image-list'})
			img = []
			for i in link:
				j = i.findAll('img')
				for k in j:
					l = k['src']
					u1 = l.rsplit('/',2)[0]
					u2 = l.split('/')[-1]
					u = u1 + '/770x0/'+u2
					img.append(u)
			img = list(set(img))
			#print img
			print (len(img))
			#img.append(wiki)
			#return img
			tmp_bio = os.path.join(TMPDIR,name+'-bio.txt')
			#f = open(tmp_bio,'w')
			#f.write(str(wiki))
			#f.close()
			write_files(tmp_bio,wiki,line_by_line=False)
			thumb = os.path.join(TMPDIR,name+'.jpg')
			if img:
				url = img[0]
				try:
					#subprocess.call(["curl","-o",thumb,url])
					ccurl(url+'#'+'-o'+'#'+thumb)
				except:
					#subprocess.call(["curl",'--data-urlencode',"-o",thumb,url])
					pass
			tmp_n = os.path.join(TMPDIR,name+'.txt')
			#f = open(tmp_n,'w')
			#for i in img:
			#	f.write(str(i)+'\n')
			#f.close()
			write_files(tmp_n,img,line_by_line=True)
		#self.terminate()



class downloadThread(QtCore.QThread):
    
	def __init__(self,url):
		QtCore.QThread.__init__(self)
	
		self.url = url
		self.interval = 1

	def __del__(self):
		self.wait()                        
	
	def run(self):
		ccurl(self.url)
		
class updateListThread(QtCore.QThread):
	update_list2_signal = pyqtSignal(str,int)
	def __init__(self,e):
		QtCore.QThread.__init__(self)
		self.e = e
		self.update_list2_signal.connect(update_list2_global)
	def __del__(self):
		self.wait()                        
	
	def run(self):
		k = 0
		for i in self.e:
			self.update_list2_signal.emit(i,k)
			k = k+1
		
@pyqtSlot(str,int)
def update_list2_global(i,k):
	
	try:
		icon_name = ui.get_thumbnail_image_path(k,i)
	except:
		icon_name = ''
	if os.path.exists(icon_name):
		ui.list2.item(k).setIcon(QtGui.QIcon(icon_name))
		
class ThreadingThumbnail(QtCore.QThread):
    
	def __init__(self,path,picn,inter):
		QtCore.QThread.__init__(self)
	
		self.path = path
		self.picn = picn
		self.inter = inter
		self.interval = 1

	def __del__(self):
		self.wait()                        
	
	def run(self):
		print(self.path)
		if not os.path.exists(self.picn) and self.path:
			#try:
			if self.path.startswith('http') and (self.path.endswith('.jpg') or self.path.endswith('.png')):
				ccurl(self.path+'#'+'-o'+'#'+self.picn)
			else:
				#subprocess.call(["ffmpegthumbnailer","-i",self.path,"-o",self.picn,"-t",str(self.inter),'-q','10','-s','350'])
				ui.generate_thumbnail_method(self.picn,self.inter,self.path)
			
			#except:
			#	pass

class MainWindowWidget(QtWidgets.QWidget):
	def __init__(self):
		super(MainWindowWidget,self).__init__()
		
		
		
	def mouseMoveEvent(self,event):
		global site,MainWindow,ui
		pos = event.pos()
		px = pos.x()
		#print(pos)
		#print(pos)
		x = MainWindow.width()
		dock_w = ui.dockWidget_3.width()
		#print(px,'--',MainWindow.width())
		if ui.orientation_dock == 'right':
			if px <= x and px >= x-6:
				ui.dockWidget_3.show()
				ui.btn1.setFocus()
				#if pos.x() >= 0 and pos.x()<=10:
				#ui.dockWidget_3.show()
				#ui.btn1.setFocus()
				#elif pos.x() > 200 and ui.auto_hide_dock:
			elif px <= x-dock_w and ui.auto_hide_dock:
				ui.dockWidget_3.hide()
				if not ui.list1.isHidden():
					ui.list1.setFocus()
				elif not ui.list2.isHidden():
					ui.list2.setFocus()
		else:
			if px >= 0 and px <= 10:
				ui.dockWidget_3.show()
				ui.btn1.setFocus()
			elif px >= dock_w and ui.auto_hide_dock:
				ui.dockWidget_3.hide()
				if not ui.list1.isHidden():
					ui.list1.setFocus()
				elif not ui.list2.isHidden():
					ui.list2.setFocus()
		if MainWindow.isFullScreen() and not ui.tab_5.isHidden():
			ht = self.height()
			#print "height="+str(ht)
			#print "y="+str(pos.y())
			if pos.y() <= ht and pos.y()> ht - 5 and ui.frame1.isHidden():
				#ui.gridLayout.setSpacing(0)
				ui.frame1.show()
				#if Player == "mplayer":
				ui.frame1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			elif pos.y() <= ht-32 and not ui.frame1.isHidden():
				ui.frame1.hide()
				#ui.gridLayout.setSpacing(0)
		
		

	
def naturallysorted(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

class MyEventFilter(QtCore.QObject):
	def eventFilter(self, receiver, event):
		if(event.type() == QtCore.QEvent.MouseMove):
			#MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
				pos = event.pos()
				#print "x="+str(pos.x())
				#print pos.y()
				#widget = MainWindow.childAt(event.pos())
				#if widget:
				#	print widget.objectName()
				#print str(widget.objectName())
				if pos.x() == 0:
					ui.dockWidget_3.show()
				elif pos.x() > 300:
					ui.dockWidget_3.hide()
					ui.list1.setFocus()
				return True
		else:
		#Call Base Class Method to Continue Normal Event Processing
			return super(MyEventFilter,self).eventFilter(receiver, event)



class ScaledLabel(QtWidgets.QLabel):
	def __init__(self, *args, **kwargs):
		QtWidgets.QLabel.__init__(self)
		self._pixmap = QtGui.QPixmap(self.pixmap())

	def resizeEvent(self, event):
		self.setPixmap(self._pixmap.scaled(
		self.width(), self.height(),
		QtCore.Qt.KeepAspectRatio))


class labelDock(QtWidgets.QLabel):
	def __init__(self, *args, **kwargs):
		QtWidgets.QLabel.__init__(self)
	def mouseMoveEvent(self,event):
		print (event.pos())

class ExtendedQLabel(QtWidgets.QLabel):

	def __init(self, parent):
		QLabel.__init__(self, parent)
		#QLabel.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
		#self.destroyed.connect(onDestroyed)
		#def onDestroyed():
		#print "Hello"
	def mouseReleaseEvent(self, ev):
		#def mouseDoubleClickEvent(self,ev):
		global name,tmp_name,opt,list1_items,curR
		#self.emit(QtCore.SIGNAL('clicked()'))
		#sending_button = self.sender()
		t=str(self.objectName())
		t = re.sub('label_','',t)
		num = int(t)
		ui.label_search.clear()
		#name = tmp_name[num]
		try:
			name = str(ui.list1.item(num).text())
		except:
			name = str(list1_items[num])
			for i in range(ui.list1.count()):
				if name == str(ui.list1.item(i).text()):
					num = i
					break
		print (name)
		#ui.tabWidget1.setCurrentIndex(0)
		j = 0
		
		ui.list1.setCurrentRow(num)
		ui.labelFrame2.setText(ui.list1.currentItem().text())
		ui.btn10.clear()
		ui.btn10.addItem(_fromUtf8(""))
		ui.btn10.setItemText(0, _translate("MainWindow",name, None))
		ui.listfound()
		ui.list2.setCurrentRow(0)
		curR = 0
		items = []
		j=1
		if not ui.lock_process:
			ui.gridLayout.addWidget(ui.tab_6,0,1,1,1)
			ui.thumbnailHide('ExtendedQLabel')
			ui.IconViewEpn()
			if not ui.scrollArea1.isHidden():
				ui.scrollArea1.setFocus()
		
	def contextMenuEvent(self, event):
		global name,tmp_name,opt,list1_items,curR,nxtImg_cnt
		
		t=str(self.objectName())
		t = re.sub('label_','',t)
		num = int(t)
		try:
			name = tmp_name[num]
		except:
			name = tmp_name[num%len(tmp_name)]
		print (name)
		menu = QtWidgets.QMenu(self)
		#review = menu.addAction("Review")
		rmPoster = menu.addAction("Remove Poster")
		adPoster = menu.addAction("Find Image")
		rset = menu.addAction("Reset Counter")
		adImage = menu.addAction("Replace Image")
		action = menu.exec_(self.mapToGlobal(event.pos()))
		if action == rmPoster:
			t=str(self.objectName())
			#t = re.sub('label_','',t)
			#num = int(t)
			#name = tmp_name[num]
			#print name
			p1 = "ui."+t+".clear()"
			exec (p1)
			
			#elif action == review:
	
			#ui.btn10.setItemText(0, _translate("MainWindow",name, None))
			#ui.btn10.setItemText(0, _translate("MainWindow",name, None))
			#ui.btn2.setCurrentIndex(1)
			#ui.reviews()
		elif action == adPoster:
			if site == "SubbedAnime" and base_url == 15:
				nam = re.sub('[0-9]*','',name)
			else:
				nam = name
			url = "https://www.google.co.in/search?q="+nam+"anime&tbm=isch"
			print (url)
			content = ccurl(url)
			n = re.findall('imgurl=[^"]*.jpg',content)
			src= re.sub('imgurl=','',n[nxtImg_cnt])
			#return ccurl(src)
			#picn = "/tmp/AnimeWatch/"+name+".jpg"
			picn = os.path.join(TMPDIR,name+'.jpg')
			if os.path.isfile(picn):
				os.remove(picn)
			subprocess.call(["curl","-A",hdr,'--max-filesize',"-L","-o",picn,src])
			t=str(self.objectName())
			img = QtGui.QPixmap(picn, "1")
			q1="ui."+t+".setPixmap(img)"
			t=str(self.objectName())
			exec (q1)
			nxtImg_cnt = nxtImg_cnt+1
		elif action == rset:
			nxtImg_cnt = 0
		elif action == adImage:
			ui.copyImg()
	
	


class ExtendedQLabelEpn(QtWidgets.QLabel):

	def __init(self, parent):
		#QLabel.__init__(self, parent)
		super(ExtendedQLabelEpn, self).__init__(parent)
		
	
	def seek_mplayer(self):
		global Player,total_seek
		if Player == "mplayer":
				t = bytes('\n'+"seek " + str(total_seek)+'\n','utf-8')
				mpvplayer.write(t)
				total_seek = 0
	def osd_hide(self):
		global mpvplayer
		mpvplayer.write(b'\n osd 0 \n')
	def arrow_hide(self):
		global Player
		if Player == "mplayer" or Player == "mpv":
			self.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
		
		print ("arrow hide")
	def frameShowHide(self):
		global fullscr
		if MainWindow.isFullScreen():
			if ui.frame1.isHidden():
				ui.gridLayout.setSpacing(0)
				ui.frame1.show()
				ui.frame_timer.start(2000)
			else:
				ui.frame_timer.stop()
				ui.frame_timer.start(2000)


	def keyPressEvent(self, event):
		global mpvplayer,Player,wget,cycle_pause,cache_empty,buffering_mplayer,total_till,curR,cur_label_num,iconv_r_indicator,total_seek
		global fullscr,idwMain,idw,quitReally,new_epn,toggleCache,quitReally,pause_indicator,iconv_r,tab_6_size_indicator
		if mpvplayer:
			if mpvplayer.processId() > 0:
					#self.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
					if tab_6_size_indicator:
						tab_6_size_indicator.pop()
					tab_6_size_indicator.append(ui.tab_6.width())
					if event.key() == QtCore.Qt.Key_Equal:
						"""
						i = 0
						if total_till > 0:
							while(i<total_till):
								t = "ui.label_"+str(i)+".deleteLater()"
		
								exec t
		
								i = i+1
						"""
						#total_till = 0
						#browse_cnt = 0
						
						if iconv_r > 1:
							iconv_r = iconv_r-1
							if iconv_r_indicator:
								iconv_r_indicator.pop()
				
							iconv_r_indicator.append(iconv_r)
						if not ui.scrollArea.isHidden():
							ui.next_page('not_deleted')
							#ui.thumbnail_label_update()
						elif not ui.scrollArea1.isHidden():
							#ui.thumbnailEpn()
							ui.thumbnail_label_update()
						if iconv_r > 1:
							w = float((ui.tab_6.width()-60)/iconv_r)
							h = float((9*w)/16)
							width=str(int(w))
							height=str(int(h))
							ui.scrollArea1.verticalScrollBar().setValue((((curR+1)/iconv_r)-1)*h+((curR+1)/iconv_r)*10)
					elif event.key() == QtCore.Qt.Key_Minus:
						"""
						i = 0
						if total_till > 0:
							while(i<total_till):
								t = "ui.label_"+str(i)+".deleteLater()"
		
								exec t
		
								i = i+1
						"""
						#total_till = 0
						#browse_cnt = 0
						
						iconv_r = iconv_r+1
						if iconv_r_indicator:
							iconv_r_indicator.pop()
						iconv_r_indicator.append(iconv_r)
						if not ui.scrollArea.isHidden():
							ui.next_page('not_deleted')
							#ui.thumbnail_label_update()
						elif not ui.scrollArea1.isHidden():
							#ui.thumbnailEpn()
							ui.thumbnail_label_update()
						if iconv_r > 1:
							w = float((ui.tab_6.width()-60)/iconv_r)
							h = float((9*w)/16)
							width=str(int(w))
							height=str(int(h))
							ui.scrollArea1.verticalScrollBar().setValue((((curR+1)/iconv_r)-1)*h+((curR+1)/iconv_r)*10)
					elif event.key() == QtCore.Qt.Key_Right:
		
						if Player == "mplayer":
								if site == "Local" or site == "None" or site == "PlayLists":
									mpvplayer.write(b'\n seek +10 \n')
								else:
									total_seek = total_seek + 10
									r = "Seeking "+str(total_seek)+'s'
									ui.progressEpn.setFormat(r)
									if self.seek_timer.isActive():
										self.seek_timer.stop()
									self.seek_timer.start(500)
						else:
							mpvplayer.write(b'\n seek +10 relative+exact \n')
			
						self.frameShowHide()
			
		
					elif event.key() == QtCore.Qt.Key_1:
						mpvplayer.write(b'\n add chapter -1 \n')
					elif event.key() == QtCore.Qt.Key_2:
						mpvplayer.write(b'\n add chapter 1 \n')
					elif event.key() == QtCore.Qt.Key_3:
						mpvplayer.write(b'\n cycle ass-style-override \n')
					elif event.modifiers() == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_V:
						mpvplayer.write(b'\n cycle ass-vsfilter-aspect-compat \n')
					elif event.key() == QtCore.Qt.Key_Left:
						if Player == "mplayer":
								if site == "Local" or site == "None" or site == "PlayLists":
									mpvplayer.write(b'\n seek -10 \n')
								else:
									total_seek = total_seek - 10
									r = "Seeking "+str(total_seek)+'s'
									ui.progressEpn.setFormat(r)
									#mpvplayer.write('\n'+'seek +10'+'\n')
									if self.seek_timer.isActive():
										self.seek_timer.stop()
									self.seek_timer.start(500)
									#mpvplayer.write('\n'+'seek -10'+'\n')
						else:
							mpvplayer.write(b'\n osd-msg-bar seek -10 \n')
						self.frameShowHide()
						#mpvplayer.write('\n'+'show_progress'+'\n')
					elif event.key() == QtCore.Qt.Key_0:
						if Player == "mplayer":
								mpvplayer.write(b'\n seek +90 \n')
						else:
								mpvplayer.write(b'\n osd-msg-bar seek +90 \n')
						#mpvplayer.write('\n'+'show_progress'+'\n')
		
					elif event.key() == QtCore.Qt.Key_9:
						if Player == "mplayer":
								mpvplayer.write(b'\n seek -5 \n')
						else:
								mpvplayer.write(b'\n osd-msg-bar seek -5 \n')
						#mpvplayer.write('\n'+'show_progress'+'\n')
		
					elif event.key() == QtCore.Qt.Key_A:
						mpvplayer.write(b'\n cycle_values video-aspect "16:9" "4:3" "2.35:1" "-1" \n')
					elif event.key() == QtCore.Qt.Key_N:
						mpvplayer.write(b'\n playlist_next \n')
					elif event.key() == QtCore.Qt.Key_L:
						ui.tab_5.setFocus()
			
					elif event.key() == QtCore.Qt.Key_End:
						if Player == "mplayer":
							mpvplayer.write(b'\n seek 99 1 \n')
						else:
							mpvplayer.write(b'\n osd-msg-bar seek 100 absolute-percent \n')
		
					elif event.key() == QtCore.Qt.Key_P:
						#ui.tab_5.setFocus()
						if ui.frame1.isHidden():
							ui.gridLayout.setSpacing(0)
							ui.frame1.show()
						else:
							ui.gridLayout.setSpacing(10)
							ui.frame1.hide()
						
			
					elif event.key() == QtCore.Qt.Key_Space:
			
						buffering_mplayer = "no"
			
						if ui.frame_timer.isActive:
							ui.frame_timer.stop()
						if ui.mplayer_timer.isActive():
							ui.mplayer_timer.stop()
						if Player == "mplayer":
							if MainWindow.isFullScreen():
								ui.frame1.hide()
							mpvplayer.write(b'\n pausing_toggle osd_show_progression \n')
				
				
						else:
							if not pause_indicator:
								mpvplayer.write(b'\n set pause yes \n')
								if MainWindow.isFullScreen():
									ui.frame1.show()
									ui.gridLayout.setSpacing(0)
								pause_indicator.append("Pause")
							else:
								mpvplayer.write(b'\n set pause no \n')
								if MainWindow.isFullScreen():
									ui.gridLayout.setSpacing(0)
									ui.frame1.hide()
								pause_indicator.pop()
							#mpvplayer.write('\n'+'print-text "Pause-Status:${pause}"'+'\n')
				
					elif event.key() == QtCore.Qt.Key_Up:
						if Player == "mplayer":
							if site == "Local" or site == "None" or site == "PlayLists":
								mpvplayer.write(b'\n seek +60 \n')
							else:
								total_seek = total_seek + 60
								r = "Seeking "+str(total_seek)+'s'
								ui.progressEpn.setFormat(r)
								#mpvplayer.write('\n'+'seek +10'+'\n')
								if self.seek_timer.isActive():
									self.seek_timer.stop()
								self.seek_timer.start(500)
								#mpvplayer.write('\n'+'seek +60'+'\n')
						else:
							mpvplayer.write(b'\n osd-msg-bar seek +60 \n')
			
						self.frameShowHide()
					elif event.key() == QtCore.Qt.Key_Down:
						if Player == "mplayer":
							if site == "Local" or site == "None" or site == "PlayLists": 
								mpvplayer.write(b'\n seek -60 \n')
							else:
								total_seek = total_seek - 60
								r = "Seeking "+str(total_seek)+'s'
								ui.progressEpn.setFormat(r)
								#mpvplayer.write('\n'+'seek +10'+'\n')
								if self.seek_timer.isActive():
									self.seek_timer.stop()
								self.seek_timer.start(500)
								#mpvplayer.write('\n'+'seek -60'+'\n')
						else:
							mpvplayer.write(b'\n osd-msg-bar seek -60 \n')
			
						self.frameShowHide()
					elif event.key() == QtCore.Qt.Key_PageUp:
						if Player == "mplayer":
							if site == "Local" or site == "None" or site == "PlayLists":
								mpvplayer.write(b'\n seek +300 \n')
							else:
								total_seek = total_seek + 300
								r = "Seeking "+str(total_seek)+'s'
								ui.progressEpn.setFormat(r)
								#mpvplayer.write('\n'+'seek +10'+'\n')
								if self.seek_timer.isActive():
									self.seek_timer.stop()
								self.seek_timer.start(500)
								#mpvplayer.write('\n'+'seek +300'+'\n')
						else:
							mpvplayer.write(b'\n osd-msg-bar seek +300 \n')
			
						self.frameShowHide()
					elif event.key() == QtCore.Qt.Key_PageDown:
						if Player == "mplayer":
							if site == "Local" or site == "None" or site == "PlayLists":
								mpvplayer.write(b'\n seek -300 \n')
							else:
								total_seek = total_seek - 300
								r = "Seeking "+str(total_seek)+'s'
								ui.progressEpn.setFormat(r)
								#mpvplayer.write('\n'+'seek +10'+'\n')
								if self.seek_timer.isActive():
									self.seek_timer.stop()
								self.seek_timer.start(500)
								#mpvplayer.write('\n'+'seek -300'+'\n')
						else:
							mpvplayer.write(b'\n osd-msg-bar seek -300 \n')
			
						self.frameShowHide()
					elif event.key() == QtCore.Qt.Key_O:
						mpvplayer.write(b'\n osd \n')
					elif event.key() == QtCore.Qt.Key_M:
						#print (new_epn)
			
						if Player == "mplayer":
							mpvplayer.write(b'\n osd_show_property_text ${filename} \n')
						else:
							mpvplayer.write(b'\n show-text "${filename}" \n')
					elif event.key() == QtCore.Qt.Key_I:
						mpvplayer.write(b'\n show_text ${file-size} \n')
					elif event.key() == QtCore.Qt.Key_E:
						if Player == "mplayer":
							w=self.width()
							w = w + (0.05*w)
							h = self.height()
							h = h + (0.05*h)
							self.setMaximumSize(w,h)
							self.setMinimumSize(w,h)
						else:
							mpvplayer.write(b'\n add video-zoom +0.01 \n')
					elif event.key() == QtCore.Qt.Key_W:
						if Player == "mplayer":
							#mpvplayer.write('\n'+'panscan -0.05'+'\n')
							w=self.width()
							w = w - (0.05*w)
							h = self.height()
							h = h - (0.05*h)
							self.setMaximumSize(w,h)
							self.setMinimumSize(w,h)
						else:
							mpvplayer.write(b'\n add video-zoom -0.01 \n')
					elif event.key() == QtCore.Qt.Key_R:
						if Player == "mplayer":
							mpvplayer.write(b'\n sub_pos -1 \n')
						else:
							mpvplayer.write(b'\n add sub-pos -1 \n')
					elif event.key() == QtCore.Qt.Key_T:
						if Player == "mplayer":
							mpvplayer.write(b'\n sub_pos +1 \n')
						else:
							mpvplayer.write(b'\n add sub-pos +1 \n')
					elif event.key() == QtCore.Qt.Key_J:
						if Player == "mplayer":
							if not self.mplayer_OsdTimer.isActive():
								mpvplayer.write(b'\n osd 1 \n')
							else:
								self.mplayer_OsdTimer.stop()
							mpvplayer.write(b'\n sub_select \n')
							self.mplayer_OsdTimer.start(5000)
						else:
							mpvplayer.write(b'\n cycle sub \n')
					elif event.key() == QtCore.Qt.Key_K:
						if Player == "mplayer":
							if not self.mplayer_OsdTimer.isActive():
								mpvplayer.write(b'\n osd 1 \n')
							else:
								self.mplayer_OsdTimer.stop()
				
							mpvplayer.write(b'\n switch_audio \n')
							self.mplayer_OsdTimer.start(5000)
						else:
							mpvplayer.write(b'\n cycle audio \n')
					
					elif event.key() == QtCore.Qt.Key_Period:
						ui.mpvNextEpnList()
					elif event.key() == QtCore.Qt.Key_Comma:
						#if Player != "mplayer":
						ui.mpvPrevEpnList()
				
					
					
					elif event.key() == QtCore.Qt.Key_Q:
						#self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
						if iconv_r_indicator:
							iconv_r = iconv_r_indicator[0]
						quitReally = "yes"
						mpvplayer.write(b'\n quit \n')
						if '	' in epnArrList[cur_label_num]:
							nameEpn = (str(epnArrList[cur_label_num])).split('	')[0]
					
						else:
							#nameEpn = (str(epnArrList[cur_label_num])).split('/')[-1]
							nameEpn = os.path.basename(epnArrList[cur_label_num])
						length_1 = ui.list2.count()
						q3="ui.label_epn_"+str(length_1+cur_label_num)+".setText(nameEpn)"
						exec (q3)
						
						if MainWindow.isFullScreen():
							ui.gridLayout.setSpacing(10)
							#ui.gridLayout.setContentsMargins(10,10,10,10)
							ui.superGridLayout.setContentsMargins(10,10,10,10)
							if wget:
								if wget.processId() > 0:
									ui.goto_epn.hide()
									ui.progress.show()
				
							ui.frame2.show()
							MainWindow.showNormal()
							MainWindow.showMaximized()
							i = 0
							while(i<total_till):
								if i!=cur_label_num:
									p1="ui.label_epn_"+str(i)+".show()"
									exec (p1)
								else:
									w = float((ui.tab_6.width()-60)/iconv_r)
									h = float((9*w)/16)
									width=str(int(w))
									height=str(int(h))
									p2="ui.label_epn_"+str(i)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
									p3="ui.label_epn_"+str(i)+".setMinimumSize(QtCore.QSize("+width+","+height+"))"
									exec (p2)
									exec (p3)
								
								i = i+1
						
						else:
							
							ui.thumbnail_label_update()
						QtWidgets.QApplication.processEvents()
						QtWidgets.QApplication.processEvents()
						#if fullscr == 1:
						p1="ui.label_epn_"+str(cur_label_num)+".y()"
						yy=eval(p1)
						ui.scrollArea1.verticalScrollBar().setValue(yy)
						#ui.scrollArea1.verticalScrollBar().setValue(((curR+1)/iconv_r)*h+((curR+1)/iconv_r)*10)
					elif event.key() == QtCore.Qt.Key_F:
						if iconv_r_indicator:
							iconv_r = iconv_r_indicator[0]
						
						fullscr = 1 - fullscr
						if not MainWindow.isFullScreen():
							#ui.gridLayout.setSpacing(0)
							ui.label.hide()
							ui.text.hide()
							ui.frame1.hide()
							#ui.tab_6.hide()
							ui.goto_epn.hide()
							ui.btn10.hide()
							#ui.btn20.hide()
							ui.frame2.hide()
							if wget:
								if wget.processId() > 0:
									ui.progress.hide()
							ui.list2.hide()
							ui.list6.hide()
							ui.list1.hide()
							ui.frame.hide()
							#ui.text.hide()
							#ui.label.hide()
							#ui.tab_5.setParent(None)
							ui.gridLayout.setContentsMargins(0,0,0,0)
							ui.superGridLayout.setContentsMargins(0,0,0,0)
							ui.gridLayout1.setContentsMargins(0,0,0,0)
							ui.gridLayout2.setContentsMargins(0,0,0,0)
							ui.horizontalLayout10.setContentsMargins(0,0,0,0)
							ui.horizontalLayout10.setSpacing(0)
							ui.gridLayout.setSpacing(0)
							ui.gridLayout1.setSpacing(0)
							ui.gridLayout2.setSpacing(0)
							
							ui.tab_6.show()
							ui.tab_6.setFocus()
							p1="ui.label_epn_"+str(cur_label_num)+".setFocus()"
							exec (p1)
							#ui.tab_5.showFullScreen()
							#ui.gridLayout.showFullScreen()
				
							MainWindow.showFullScreen()
							i = 0
							while(i<total_till_epn):
								if i!=cur_label_num:
									p1="ui.label_epn_"+str(i)+".hide()"
									exec (p1)
								else:
									w = float(MainWindow.width())
									h = float((9*w)/16)
									width=str(int(w))
									height=str(int(h))
									p2="ui.label_epn_"+str(i)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
									p3="ui.label_epn_"+str(i)+".setMinimumSize(QtCore.QSize("+width+","+height+"))"
									exec (p2)
									exec (p3)
									
								i = i+1
							#QtGui.QApplication.processEvents()
						else:
				
							ui.gridLayout.setSpacing(10)
							#ui.gridLayout.setContentsMargins(10,10,10,10)
							ui.superGridLayout.setContentsMargins(10,10,10,10)
							ui.gridLayout1.setSpacing(10)
							ui.gridLayout1.setContentsMargins(10,10,10,10)
							ui.gridLayout2.setSpacing(10)
							ui.gridLayout2.setContentsMargins(10,10,10,10)
							ui.horizontalLayout10.setContentsMargins(10,10,10,10)
							ui.horizontalLayout10.setSpacing(10)
							if wget:
								if wget.processId() > 0:
									ui.goto_epn.hide()
									ui.progress.show()
					
							#ui.btn20.show()
							ui.frame2.show()
							MainWindow.showNormal()
							MainWindow.showMaximized()
							i = 0
							while(i<total_till_epn):
								if i!=cur_label_num:
									p1="ui.label_epn_"+str(i)+".show()"
									exec (p1)
								
								else:
									w = float((ui.tab_6.width()-60)/iconv_r)
									h = float((9*w)/16)
									width=str(int(w))
									height=str(int(h))
									p2="ui.label_epn_"+str(i)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
									p3="ui.label_epn_"+str(i)+".setMinimumSize(QtCore.QSize("+width+","+height+"))"
									exec (p2)
									exec (p3)
									
								i = i+1
							#QtGui.QApplication.processEvents()
							ui.thumbnail_label_update()
							QtWidgets.QApplication.processEvents()
							QtWidgets.QApplication.processEvents()
							p1="ui.label_epn_"+str(cur_label_num)+".y()"
							yy=eval(p1)
							ui.scrollArea1.verticalScrollBar().setValue(yy)
		super(ExtendedQLabelEpn, self).keyPressEvent(event)				
						
						
						
						
						
						
	def mouseMoveEvent(self,event):
		self.setFocus()
		pos = event.pos()
		#print pos.y()
		
		if Player == "mplayer" or Player=="mpv":
			if self.arrow_timer.isActive():
				self.arrow_timer.stop()
			self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			self.arrow_timer.start(2000)
	
	
		if MainWindow.isFullScreen():
			ht = self.height()
			#print "height="+str(ht)
			#print "y="+str(pos.y())
			if pos.y() <= ht and pos.y()> ht - 5 and ui.frame1.isHidden():
				ui.gridLayout.setSpacing(0)
				ui.frame1.show()
				#if Player == "mplayer":
				ui.frame1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			elif pos.y() <= ht-32 and not ui.frame1.isHidden() :
				ui.frame1.hide()
				ui.gridLayout.setSpacing(10)
	def mouseReleaseEvent(self, ev):
		#def mouseDoubleClickEvent(self,ev):
		global epnArrList,new_epn,Player,idw,mpvplayer,quitReally,curR,interval,iconv_r,total_till,browse_cnt,site,epn_name_in_list,memory_num_arr,thumbnail_indicator,mpvplayer,iconv_r_indicator,tab_6_size_indicator,tab_6_player,site,finalUrlFound,artist_name_mplayer,server,quality
	
		
		
		if ev.button() == QtCore.Qt.LeftButton:
			ui.label_search.clear()
			tab_6_player = "False"
			if tab_6_size_indicator:
				tab_6_size_indicator.pop()
			if ui.tab_6.width()>500:
				tab_6_size_indicator.append(ui.tab_6.width())
			ui.gridLayout.setSpacing(0)
			
			#if mpvplayer:
			#		if mpvplayer.processId() > 0:
			#			mpvplayer.write(b'\n quit \n')
			#			mpvplayer.kill()
			if site == "Local" or site == "PlayLists" or site == "Music" or site == "Video" or site == "None":
				
				#self.emit(QtCore.SIGNAL('clicked()'))
				quitReally = "no"
				
				#sending_button = self.sender()
				t=str(self.objectName())
				t = re.sub('label_epn_','',t)
				num = int(t)
				curR = num
				
				ui.gridLayout.addWidget(ui.tab_6, 0, 2, 1, 1)
				#ui.gridLayout.addWidget(ui.frame1, 1, 0, 1, 1)
				#ui.tab_5.setMinimumSize(500,400)
				#ui.gridLayout.addWidget(ui.tab_6, 0, 1, 1, 1)
				if '	' in epnArrList[num]:
					new_epn = (epnArrList[num]).split('	')[0]
					
					finalUrl = '"'+((epnArrList[num]).split('	')[1])+'"'
				else:
					#new_epn = (epnArrList[num]).split('/')[-1]
					new_epn = os.path.basename(epnArrList[num])
					finalUrl = '"'+epnArrList[num]+'"'
				ui.epn_name_in_list = new_epn
				
				if num < ui.list2.count():
					ui.list2.setCurrentRow(num)
					#p1 = "mn = ui.label_"+str(num)+".winId()"
					#exec p1
					#idw = str(mn)
					idw = str(int(ui.tab_5.winId()))
					ui.gridLayout.addWidget(ui.tab_5, 0, 1, 1, 1)
					##ui.gridLayout.addWidget(ui.frame1, 1, 1, 1, 1)
					#ui.horizontalLayout10.addWidget(ui.tab_5)
					#if ui.tab_5.isHidden() or ui.tab_5.width==0:
					ui.tab_5.show()
					ui.tab_5.setFocus()
					ui.frame1.show()
					i = 0
					
					##total_till = 0
					#iconv_r_indicator.append(iconv_r)
					iconv_r = 1
					#browse_cnt = 0
					ui.thumbnail_label_update_epn()
					QtWidgets.QApplication.processEvents()
					p1 = "ui.label_epn_"+str(num)+".y()"
					
					ht = eval(p1)
					print(ht,'--ht--',ui.scrollArea1.height())
					ui.scrollArea1.verticalScrollBar().setValue(ht)
					#if ui.tab_6.width() != 400:
					#ui.tab_6.setMaximumWidth(400)
					
					
						
					finalUrl = finalUrl.replace('#','')
					try:
						finalUrl = str(finalUrl)
					except:
						finalUrl = finalUrl
					finalUrl = finalUrl.replace('"','')
					if ui.if_file_path_exists_then_play(curR,ui.list2,True):
						print('---line 1868---')
					else:
						if 'youtube.com' in finalUrl:
							ui.external_url = True
							finalUrl = get_yt_url(finalUrl,quality).strip()
							if '#' in finalUrl:
								audio_url = finalUrl.split('#')[0]
								video_url = finalUrl.split('#')[1]
								if Player == 'mpv':
									finalUrl = "--audio-file="+audio_url+' '+video_url
								elif Player == 'mplayer':
									finalUrl = '-audiofile '+audio_url+' '+video_url
						ui.play_file_now(finalUrl)
					
					if site == "Music":
						print (finalUrl)
						try:
							artist_name_mplayer = epnArrList[num].split('	')[2]
							if artist_name_mplayer == "None":
								artist_name_mplayer = ""
						except:
							artist_name_mplayer = ""
						ui.updateMusicCount('count',finalUrl)
					
					elif site == "Video":
						ui.updateVideoCount('mark',finalUrl)
					
			else:
		
					
					#self.emit(QtCore.SIGNAL('clicked()'))
					quitReally = "no"
					
					#sending_button = self.sender()
					t=str(self.objectName())
					t = re.sub('label_epn_','',t)
					num = int(t)
					curR = num
					
					#ui.gridLayout.addWidget(ui.frame1, 1, 0, 1, 1)
					#ui.tab_5.setMinimumSize(500,400)
					#ui.gridLayout.addWidget(ui.tab_6, 0, 1, 1, 1)
					if '	' in epnArrList[num]:
						new_epn = (epnArrList[num]).split('	')[0]
					else:
						#if '/' in epnArrList[num] and finalUrlFound == True:
						#	new_epn = (epnArrList[num]).split('/')[-1]
						#else:
						new_epn = os.path.basename(epnArrList[num])
					ui.epn_name_in_list = new_epn
					ui.list2.setCurrentRow(num)
					
					ui.epnfound()
					if num < ui.list2.count():
						ui.gridLayout.addWidget(ui.tab_5, 0, 1, 1, 1)
						##ui.gridLayout.addWidget(ui.frame1, 1, 1, 1, 1)
						ui.gridLayout.addWidget(ui.tab_6, 0, 2, 1, 1)
						#ui.horizontalLayout10.addWidget(ui.tab_5)
					
						#if ui.tab_5.isHidden() or ui.tab_5.width()==0:
						print (ui.tab_5.width())
						ui.tab_5.show()
						ui.tab_5.setFocus()
						ui.frame1.show()
						i = 0
						thumbnail_indicator[:]=[]
						
						#total_till = 0
						#iconv_r_indicator.append(iconv_r)
						iconv_r = 1
						#browse_cnt = 0
						
						#ui.tab_6.setMaximumSize(400,1000)
						#ui.thumbnail_label_update()
						#p1 = "ui.label_"+str(num)+".y()"
						#exec (p1)
						#ht = eval(p1)
						#ui.scrollArea1.verticalScrollBar().setValue(ht)
						ui.thumbnail_label_update_epn()
						QtWidgets.QApplication.processEvents()
						p1 = "ui.label_epn_"+str(num)+".y()"
						
						ht = eval(p1)
						print(ht,'--ht--',ui.scrollArea1.height())
						ui.scrollArea1.verticalScrollBar().setValue(ht)
						#ui.scrollArea1.verticalScrollBar().setValue((num+1)*200+(num+1)*10)
						
			ui.mark_History()				
			title_num = num + ui.list2.count()
			if ui.epn_name_in_list.startswith(ui.check_symbol):
				newTitle = ui.epn_name_in_list
			else:
				newTitle = ui.check_symbol+ui.epn_name_in_list	
			sumry = "<html><h1>"+ui.epn_name_in_list+"</h1></html>"
			q3="txt = ui.label_epn_"+str(title_num)+".text()"
			exec (q3)
			q4="ui.label_epn_"+str(title_num)+".setToolTip((sumry))"			
			exec (q4)
			q3="ui.label_epn_"+str(title_num)+".setText((newTitle))"
			exec (q3)
			p8="ui.label_epn_"+str(title_num)+".home(True)"
			exec (p8)
			p8="ui.label_epn_"+str(title_num)+".deselect()"
			exec (p8)
			t= ui.epn_name_in_list[:20]
			ui.labelFrame2.setText(t)
			
			QtWidgets.QApplication.processEvents()
			
			if site == "Music":
				self.setFocus()
				r = ui.list2.currentRow()
				ui.musicBackground(r,'Search')
				
			try:
				server._emitMeta("Play",site,epnArrList)
			except:
				pass
			
	def triggerPlaylist(self,val):
		global epn,epn_name_in_list,path_final_Url,home,site,pre_opt,base_url,embed,name,epnArrList,opt,curR,refererNeeded
		print ('Menu Clicked')
		print (val.text())
		value = str(val.text())
		#print value
		#print value.data().toPyObject()
		t=str(self.objectName())
		t = re.sub('label_epn_','',t)
		num = int(t)
		curR = num
		ui.list2.setCurrentRow(curR)
		
		file_path = os.path.join(home,'Playlists',str(value))
		
		if site == "Music" or site == "Video" or site == "Local" or site == "None" or site == "PlayLists":
			#print epnArrList
			if os.path.exists(file_path):
				i = ui.list2.currentRow()
				#f = open(file_path,'a')
				
				sumr=epnArrList[i].split('	')[0]
				
				try:
					rfr_url=epnArrList[i].split('	')[2]
				except:
					rfr_url = "NONE"
				
				sumry = epnArrList[i].split('	')[1]
				sumry = sumry.replace('"','')
				if not sumry.startswith('http'):
					sumry = '"'+sumry+'"'
				t = sumr+'	'+sumry+'	'+rfr_url
				
				write_files(file_path,t,line_by_line=True)
		else:
			ui.epnfound_return()
			t = ''
			sumr=ui.epn_name_in_list
			if os.path.exists(file_path):
				#f = open(file_path,'a')
				
				if type(path_final_Url) is list:
					if refererNeeded == True:
						rfr_url = path_final_Url[1]
						sumry = path_final_Url[0]
						#f.write(sumr+'	'+sumry+'	'+rfr_url+'\n')
						t = sumr+'	'+sumry+'	'+rfr_url
					else:
						rfr_url = "NONE"
						j = 1
						t = ''
						for i in path_final_Url:
							p = "-Part-"+str(j)
							sumry = i
							#f.write(sumr+p+'	'+sumry+'	'+rfr_url+'\n')
							if j == 1:
								t = sumr+p+'	'+sumry+'	'+rfr_url
							else:
								t = t + '\n' + sumr+p+'	'+sumry+'	'+rfr_url
							j = j+1
				else:
					rfr_url = "NONE"
					
					sumry = path_final_Url
					#f.write(sumr+'	'+sumry+'	'+rfr_url+'\n')
					t = sumr+'	'+sumry+'	'+rfr_url
				
				write_files(file_path,t,line_by_line=True)
				
	def contextMenuEvent(self, event):
		global epnArrList,new_epn,Player,idw,mpvplayer,quitReally,curR,interval,quitReally,mpvplayer,Local,path_final_Url,memory_num_arr,epn_name_in_list,total_seek,cur_label_num,tab_6_player,icon_size_arr,iconv_r,iconv_r_indicator,home,siteName,finalUrlFound,refererNeeded
		total_seek = 0
		t=str(self.objectName())
		t = re.sub('label_epn_','',t)
		num = int(t)
		
		menu = QtWidgets.QMenu(self)
		
		
		submenuR = QtWidgets.QMenu(menu)
		submenuR.setTitle("Add To Playlist")
		
		menu.addMenu(submenuR)
		queue_item = menu.addAction("Queue Item")
		watch = menu.addAction("Watch in Thumbnail")
		watch1 = menu.addAction("Watch in List Form")
		thumb = menu.addAction("Show other Thumbnails")
		stop = menu.addAction("Stop Watching in Thumbnail")
		removeThumb = menu.addAction("Remove Thumbnail")
		list_mode = menu.addAction("Go To List Mode")
		
		group = QtWidgets.QActionGroup(submenuR)
		pls = os.listdir(os.path.join(home,'Playlists'))
		for i in pls:
			item = submenuR.addAction(i)
			item.setData(i)
			item.setActionGroup(group)
			#action.setCheckable(True)
			
		group.triggered.connect(self.triggerPlaylist)
		submenuR.addSeparator()
		
		new_pls = submenuR.addAction("Create New Playlist")
		
		action = menu.exec_(self.mapToGlobal(event.pos()))
		self.setFocus()
		if action == queue_item:
			if site == "Music" or site == "Video" or site == "Local" or site == "PlayLists" or site == "None":
				file_path = os.path.join(home,'Playlists','Queue')
				if not os.path.exists(file_path):
					f = open(file_path,'w')
					f.close()
					
				if not ui.queue_url_list:
					ui.list6.clear()
				#r = ui.list2.currentRow()
				r = num
				item = ui.list2.item(r)
				if item:
					ui.queue_url_list.append(epnArrList[r])
					ui.list6.addItem(epnArrList[r].split('	')[0])
					print (ui.queue_url_list)
					
					write_files(file_path,epnArrList[r],line_by_line=True)
		elif action == watch:
				if mpvplayer:
					if mpvplayer.processId()>0:
						mpvplayer.kill()
						ui.tab_5.hide()
						ui.tab_6.setMaximumSize(10000,10000)
				tab_6_player = "True"
				self.arrow_timer = QtCore.QTimer()
				self.arrow_timer.timeout.connect(self.arrow_hide)
				self.arrow_timer.setSingleShot(True)
	
				self.mplayer_OsdTimer = QtCore.QTimer()
				self.mplayer_OsdTimer.timeout.connect(self.osd_hide)
				self.mplayer_OsdTimer.setSingleShot(True)
	
				self.seek_timer = QtCore.QTimer()
				self.seek_timer.timeout.connect(self.seek_mplayer)
				self.seek_timer.setSingleShot(True)
				
				curR = num
				cur_label_num = num
				self.setFocus()
				ui.gridLayout2.setAlignment(QtCore.Qt.AlignCenter)
				
				#if icon_size_arr:
				#	w = float(1.5*int(icon_size_arr[0]))
				#	h = float(1.5*int(icon_size_arr[1]))
				#else:
				w = float(800)
				h = float((9*w)/16)
				width=str(int(w))
				height=str(int(h))
				
				
				p2="ui.label_epn_"+str(cur_label_num)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
				p3="ui.label_epn_"+str(cur_label_num)+".setMinimumSize(QtCore.QSize("+width+","+height+"))"
				exec (p2)
				exec (p3)
				QtWidgets.QApplication.processEvents()
				QtWidgets.QApplication.processEvents()
				p2="ui.label_epn_"+str(cur_label_num)+".y()"
				p3="ui.label_epn_"+str(cur_label_num)+".x()"
				yy= eval(p2)
				xy= eval(p3)
				p2="ui.label_epn_"+str(cur_label_num)+".width()"
				p3="ui.label_epn_"+str(cur_label_num)+".height()"
				wdt=eval(p2)
				hgt=eval(p3)
				
				
							
				ui.scrollArea1.horizontalScrollBar().setValue(xy-10)
				ui.scrollArea1.verticalScrollBar().setValue(yy-10)
				
				quitReally = "no"
				ui.list2.setCurrentRow(num)
				p4="ui.label_epn_"+str(num)+".setMouseTracking(True)"
				exec (p4)
				#ui.gridLayout.addWidget(ui.tab_5, 0, 0, 1, 1)
				ui.gridLayout.addWidget(ui.tab_6, 0, 1, 1, 1)
				#ui.gridLayout2.addWidget(ui.frame1,int(num/iconv_r),num%iconv_r, 1, 1)
				#num1 = num + ui.list2.count()
				#ui.horizontalLayout10.insertWidget(1,ui.frame1,0)
				#ui.tab_5.setMinimumSize(600,500)
				#ui.gridLayout.addWidget(ui.tab_6, 0, 1, 1, 1)
				#new_epn = (str(epnArrList[num])).split('/')[-1]
				#new_epn = (str(epnArrList[num])).split('/')[-1]
				if '	' in epnArrList[num]:
					finalUrl = '"'+(epnArrList[num]).split('	')[1]+'"'
					new_epn = (epnArrList[num]).split('	')[0]
					ui.epn_name_in_list = new_epn
				else:
					finalUrl = '"'+epnArrList[num]+'"'
					#ui.epn_name_in_list = new_epn
					new_epn = os.path.basename(epnArrList[num])
					ui.epn_name_in_list = new_epn
				if site != "Local" and site!="PlayLists" and site!="Music" and site!="Video":
					ui.epnfound_return()
					if type(path_final_Url) is not list:
						finalUrl = path_final_Url
					else:
						rfr_url = path_final_Url[1]
						rfr = "--referrer="+rfr_url
						finalUrl = path_final_Url[0]
				finalUrl = finalUrl.replace('#','')
				if site == "PlayLists":
					finalUrl = finalUrl.replace('""','"')
				print (finalUrl)
				if 'youtube.com' in finalUrl:
					ui.external_url = True
					finalUrl = finalUrl.replace('"','')
					finalUrl = get_yt_url(finalUrl,quality).strip()
					if '#' in finalUrl:
						audio_url = finalUrl.split('#')[0]
						video_url = finalUrl.split('#')[1]
						if Player == 'mpv':
							finalUrl = "--audio-file="+audio_url+' '+video_url
						elif Player == 'mplayer':
							finalUrl = '-audiofile '+audio_url+' '+video_url
				if num < ui.list2.count():
					ui.list2.setCurrentRow(num)
					p1 = "ui.label_epn_"+str(num)+".winId()"
					mn=int(eval(p1))
					idw = str(mn)
					#ui.tab_5.setFocus()
					ui.frame1.show()
					finalUrl = str(finalUrl)
					if Player == "mplayer":
						if site == "Local" or site == "Music" or site == "PlayLists" or site == "Video":
							command = "mplayer -identify -nocache -idle -msglevel all=4:statusline=5:global=6 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
						else:
							command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
						print (command)
						ui.infoPlay(command)
					elif Player == "mpv":
						if site == "Local" or site == "Music" or site == "PlayLists" or site == "Video":
							
							command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+finalUrl
				
						else:
							command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+finalUrl
						print (command)
						ui.infoPlay(command)	
				print ("horiz="+str(ui.scrollArea1.horizontalScrollBar().maximum()))
				#ui.scrollArea1.horizontalScrollBar().setValue((((curR+1)%iconv_r)-1)*w1)
				#ui.scrollArea1.verticalScrollBar().setValue((((curR+1)/iconv_r))*h1)
				ui.labelFrame2.setText(ui.epn_name_in_list)
		elif action == watch1:
			#if site=="Local":
				if mpvplayer:
					if mpvplayer.processId()>0:
						mpvplayer.kill()
						ui.tab_5.hide()
						ui.tab_6.setMaximumSize(10000,10000)
				iconv_r = 1
				ui.tab_6.setMaximumSize(400,1000)
				ui.thumbnail_label_update()
				#QtGui.QApplication.processEvents()
				#ui.tab_6.setMaximumSize(10000,10000)
				
				tab_6_player = "True"
				self.arrow_timer = QtCore.QTimer()
				self.arrow_timer.timeout.connect(self.arrow_hide)
				self.arrow_timer.setSingleShot(True)
	
				self.mplayer_OsdTimer = QtCore.QTimer()
				self.mplayer_OsdTimer.timeout.connect(self.osd_hide)
				self.mplayer_OsdTimer.setSingleShot(True)
	
				self.seek_timer = QtCore.QTimer()
				self.seek_timer.timeout.connect(self.seek_mplayer)
				self.seek_timer.setSingleShot(True)
				
				curR = num
				cur_label_num = num
				self.setFocus()
				ui.gridLayout2.setAlignment(QtCore.Qt.AlignCenter)
				
				#if icon_size_arr:
				#	w = float(1.5*int(icon_size_arr[0]))
				#	h = float(1.5*int(icon_size_arr[1]))
				#else:
				w = float(800)
				h = float((9*w)/16)
				width=str(int(w))
				height=str(int(h))
				
				
				p2="ui.label_epn_"+str(cur_label_num)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
				p3="ui.label_epn_"+str(cur_label_num)+".setMinimumSize(QtCore.QSize("+width+","+height+"))"
				exec (p2)
				exec (p3)
				QtWidgets.QApplication.processEvents()
				QtWidgets.QApplication.processEvents()
				p2="ui.label_epn_"+str(cur_label_num)+".y()"
				p3="ui.label_epn_"+str(cur_label_num)+".x()"
				yy=eval(p2)
				xy=eval(p3)
				p2="ui.label_epn_"+str(cur_label_num)+".width()"
				p3="ui.label_epn_"+str(cur_label_num)+".height()"
				wdt=eval(p2)
				hgt=eval(p3)
				
				
							
				ui.scrollArea1.horizontalScrollBar().setValue(xy-10)
				ui.scrollArea1.verticalScrollBar().setValue(yy-10)
				
				quitReally = "no"
				ui.list2.setCurrentRow(num)
				p4="ui.label_epn_"+str(num)+".setMouseTracking(True)"
				exec (p4)
				#ui.gridLayout.addWidget(ui.tab_5, 0, 0, 1, 1)
				ui.gridLayout.addWidget(ui.tab_6, 0, 1, 1, 1)
				#ui.gridLayout2.addWidget(ui.frame1,int(num/iconv_r),num%iconv_r, 1, 1)
				#num1 = num + ui.list2.count()
				#ui.horizontalLayout10.insertWidget(1,ui.frame1,0)
				#ui.tab_5.setMinimumSize(600,500)
				#ui.gridLayout.addWidget(ui.tab_6, 0, 1, 1, 1)
				#new_epn = (str(epnArrList[num])).split('/')[-1]
				if '	' in epnArrList[num]:
					finalUrl = '"'+(epnArrList[num]).split('	')[1]+'"'
					new_epn = (epnArrList[num]).split('	')[0]
					ui.epn_name_in_list = new_epn
				else:
					finalUrl = '"'+epnArrList[num]+'"'
					#ui.epn_name_in_list = new_epn
					new_epn = os.path.basename(epnArrList[num])
					ui.epn_name_in_list = new_epn
				if site != "Local" and site != "PlayLists":
					ui.epnfound_return()
					if type(path_final_Url) is not list:
						finalUrl = path_final_Url
					else:
						rfr_url = path_final_Url[1]
						rfr = "--referrer="+rfr_url
						finalUrl = path_final_Url[0]
				finalUrl = finalUrl.replace('#','')
				if site == "PlayLists":
					finalUrl = finalUrl.replace('""','"')
				if 'youtube.com' in finalUrl:
					ui.external_url = True
					finalUrl = finalUrl.replace('"','')
					finalUrl = get_yt_url(finalUrl,quality).strip()
					if '#' in finalUrl:
						audio_url = finalUrl.split('#')[0]
						video_url = finalUrl.split('#')[1]
						if Player == 'mpv':
							finalUrl = "--audio-file="+audio_url+' '+video_url
						elif Player == 'mplayer':
							finalUrl = '-audiofile '+audio_url+' '+video_url
				if num < ui.list2.count():
					ui.list2.setCurrentRow(num)
					p1 = "ui.label_epn_"+str(num)+".winId()"
					mn=int(eval(p1))
					idw = str(mn)
					#ui.tab_5.setFocus()
					ui.frame1.show()
					finalUrl = str(finalUrl)
					if Player == "mplayer":
						if site == "Local" or site == "Music" or site == "PlayLists" or site == "Video":
							command = "mplayer -identify -nocache -idle -msglevel all=4:statusline=5:global=6 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
						else:
							command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
						print (command)
						ui.infoPlay(command)
					elif Player == "mpv":
						if site == "Local" or site == "Music" or site == "PlayLists" or site == "Video":
							
							command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+finalUrl
				
						else:	
							command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+finalUrl
						print (command)
						ui.infoPlay(command)	
				print ("horiz="+str(ui.scrollArea1.horizontalScrollBar().maximum()))
				#ui.scrollArea1.horizontalScrollBar().setValue((((curR+1)%iconv_r)-1)*w1)
				#ui.scrollArea1.verticalScrollBar().setValue((((curR+1)/iconv_r))*h1)
				ui.labelFrame2.setText(ui.epn_name_in_list)
		elif action == stop:
			quitReally = "yes"
			if mpvplayer:
				if mpvplayer.processId() > 0:
					mpvplayer.write(b'\n quit \n')
		elif action == new_pls:
			print ("creating")
			item, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Input Dialog', 'Enter Playlist Name')
			if ok and item:
				file_path = os.path.join(home,'Playlists',item)
				if not os.path.exists(file_path):
					f = open(file_path,'w')
					f.close()
		elif action == list_mode:
			ui.thumbnailHide('none')
		elif action == removeThumb:
			nm = (ui.list1.currentItem().text())
			if site != "Local" and finalUrlFound == False:
				if '	' in epnArrList[num]:
					a = epnArrList[num].split('	')[0]
					a = a.replace('#','')
					if a.startswith(ui.check_symbol):
						a = a[1:]
					picn = os.path.join(home,'thumbnails',nm,a+'.jpg')
				else:
					a = (str(epnArrList[num])).replace('#','')
					if a.startswith(ui.check_symbol):
						a = a[1:]
					picn = os.path.join(home,'thumbnails',nm,name+'-'+a+'.jpg')
				if os.path.exists(picn):
					os.remove(picn)
					
					q1="ui.label_epn_"+str(num)+".clear()"
					exec (q1)
				if os.path.exists(picn):
					small_nm_1,new_title = os.path.split(picn)
					small_nm_2 = '128px.'+new_title
					#small_nm_2 = '128px.'+picn.rsplit('/',1)[-1]
					new_small_thumb = os.path.join(small_nm_1,small_nm_2)
					
					print(new_small_thumb)
					if os.path.exists(new_small_thumb):
						os.remove(new_small_thumb)
			elif site =="Local" or finalUrlFound == True or site=="PlayLists":
				if '	' in epnArrList[num]:
					a = (epnArrList[num]).split('	')[0]
				else:
					#a = (epnArrList[num]).split('/')[-1]
					a = os.path.basename(epnArrList[num])
				a1 = (str(a)).replace('#','')
				if a1.startswith(ui.check_symbol):
					a1 = a1[1:]
				picn = os.path.join(home,'thumbnails',nm,a1+'.jpg')
				if os.path.exists(picn):
					os.remove(picn)
					q1="ui.label_epn_"+str(num)+".clear()"
					exec (q1)
			interval = 0
		elif action == thumb:
			if site == "Local" or finalUrlFound == True or site=="None" or site =="PlayLists" or site == "Video" or site == "Music":
				ui.list2.setCurrentRow(num)
				if memory_num_arr:
					t_num = memory_num_arr.pop()
				else:
					t_num = -1
				
				if t_num != num:
					if site != "PlayLists":
						ui.epnfound_return()
					interval = 10
				memory_num_arr.append(num)
			
				if '	' in epnArrList[num]:
					a = (epnArrList[num]).split('	')[0]
					path = (epnArrList[num]).split('	')[1]
				else:	
					#a = (epnArrList[num]).split('/')[-1]
					a = os.path.basename(epnArrList[num])
					path = (epnArrList[num])
				path = path.replace('#','')
				if site == "PlayLists":
					path = path.replace('"','')
				print (path)
				a1 = a
				a1 = a1.replace('#','')
				if a1.startswith(ui.check_symbol):
					a1 = a1[1:]
				picnD = os.path.join(home,'thumbnails',name)
				if not os.path.exists(picnD):
					os.makedirs(picnD)
				picn = os.path.join(picnD,a1+'.jpg')
				#print picn
				#picn = '/tmp/AnimeWatch/'+a1+'.jpg'
				interval = (interval + 10)
				inter = str(interval)+'s'
				path = str(path)
				path = path.replace('"','')
				#path = '"'+path+'"'
				if finalUrlFound == True and refererNeeded == True:
					rfr_url = path_final_Url[1]
					rfr = "--referrer="+rfr_url
					path = path.replace('"','')
					path = '"'+path+'"'
					subprocess.call(["mpv",rfr,"--ytdl=no","--quiet","--no-audio","--vo=image:outdir="+TMPDIR,"--start="+str(interval)+"%","--frames=1",path])
					tpm_img = os.path.join(TMPDIR,'00000001.jpg')
					if os.path.exists(tmp_img):
						shutil.copy(tmp_img,picn)
						os.remove(tmp_img)
				elif site == "PlayLists":
					rfr_url = str((epnArrList[num]).split('	')[2])
					rfr_url1 = rfr_url.replace('"','')
					rfr_url1 = rfr_url1.replace("'",'')
					print (rfr_url1)
					playlist_dir = os.path.join(home,'thumbnails','PlayLists')
					if not os.path.exists(playlist_dir):
						os.makedirs(playlist_dir)
					if ui.list1.currentItem():
						pl_n = ui.list1.currentItem().text()
						playlist_name = os.path.join(playlist_dir,pl_n)
						if not os.path.exists(playlist_name):
							os.makedirs(playlist_name)
						picnD = os.path.join(playlist_name,a1)
						try:
							picn = picnD+'.jpg'
						except:
							picn = str(picnD)+'.jpg'
					if rfr_url1.lower().startswith('http'):
						path = path.replace('"','')
						path = '"'+path+'"'
						rfr = "--referrer="+rfr_url
						print (rfr)
						subprocess.call(["mpv",rfr,"--ytdl=no","--quiet","--no-audio","--vo=image:outdir="+TMPDIR,"--start="+str(interval)+"%","--frames=1",path])
						#if os.path.exists('/tmp/AnimeWatch/00000001.jpg'):
						#	shutil.copy('/tmp/AnimeWatch/00000001.jpg',picn)
						#	os.remove('/tmp/AnimeWatch/00000001.jpg')
						tpm_img = os.path.join(TMPDIR,'00000001.jpg')
						if os.path.exists(tmp_img):
							shutil.copy(tmp_img,picn)
							os.remove(tmp_img)
					else:
						path1 = path.replace('"','')
						if path1.startswith('http'):
							subprocess.call(["mpv","--ytdl=yes","--quiet","--no-audio","--vo=image:outdir="+TMPDIR,"--start="+str(interval)+"%","--frames=1",path])
							#if os.path.exists('/tmp/AnimeWatch/00000001.jpg'):
							#	shutil.copy('/tmp/AnimeWatch/00000001.jpg',picn)
							#	os.remove('/tmp/AnimeWatch/00000001.jpg')
							tpm_img = os.path.join(TMPDIR,'00000001.jpg')
							if os.path.exists(tmp_img):
								shutil.copy(tmp_img,picn)
								os.remove(tmp_img)
						else:
							#subprocess.call(["ffmpegthumbnailer","-i",path,"-o",picn,"-t",str(inter),'-q','10','-s','350'])
							ui.generate_thumbnail_method(picn,inter,path)
						
				else:
					print (path +'************')
					if ui.list1.currentItem():
						name_t = ui.list1.currentItem().text()
					else:
						name_t = ''
					if ui.list3.currentItem() and site == 'Music':
						if ui.list3.currentItem().text() == 'Playlist':
							picnD = os.path.join(home,'thumbnails','PlayLists',name_t)
						else:
							picnD = os.path.join(home,'thumbnails',site,name_t)
					else:
						picnD = os.path.join(home,'thumbnails',site,name_t)
					#print(picnD,'=picnD')
					if not os.path.exists(picnD):
						os.makedirs(picnD)
					picn = os.path.join(picnD,a1)+'.jpg'
					#subprocess.call(["ffmpegthumbnailer","-i",path,"-o",picn,"-t",str(inter),'-q','10','-s','350'])
					ui.generate_thumbnail_method(picn,inter,path)
				
				
				
				img = QtGui.QPixmap(picn, "1")			
				q1="ui.label_epn_"+str(num)+".setPixmap(img)"
				exec (q1)
				if interval == 100:
					interval = 10
			else:
					print ("num="+str(num))
					ui.list2.setCurrentRow(num)
					if memory_num_arr:
						t_num = memory_num_arr.pop()
					else:
						t_num = -1
				
					if t_num != num:
						ui.epnfound_return()
						interval = 10
					memory_num_arr.append(num)
					if '	' in epnArrList[num]:
						a = (((epnArrList[num])).split('	')[0])
					else:			
						a = ((epnArrList[num]))
					a = a.replace('#','')
					if a.startswith(ui.check_symbol):
						a = a[1:]
					#picn = home+'/thumbnails/'+name+'/'+a+'.jpg'
					
					picnD = os.path.join(home,'thumbnails',name)
					if not os.path.exists(picnD):
						os.makedirs(picnD)
					picn = os.path.join(picnD,a+'.jpg')
					
					interval = (interval + 10)
					inter = str(interval)+'s'
					path_final_Url = str(path_final_Url)
					path_final_Url = path_final_Url.replace('"','')
					if path_final_Url.startswith('/'):
						path_final_Url = '"'+path_final_Url+'"'
						
					subprocess.call(["mpv","--no-sub","--ytdl=no","--quiet","--no-audio","--vo=image:outdir="+TMPDIR,"--start="+str(interval)+"%","--frames=1",path_final_Url])
					#if os.path.exists('/tmp/AnimeWatch/00000001.jpg'):
					#	shutil.copy('/tmp/AnimeWatch/00000001.jpg',picn)
					#	os.remove('/tmp/AnimeWatch/00000001.jpg')
					tpm_img = os.path.join(TMPDIR,'00000001.jpg')
					if os.path.exists(tmp_img):
						shutil.copy(tmp_img,picn)
						os.remove(tmp_img)
					img = QtGui.QPixmap(picn, "1")			
					q1="ui.label_epn_"+str(num)+".setPixmap(img)"
					exec (q1)
					if interval == 100:
						interval = 10
			if os.path.exists(picn):
				small_nm_1,new_title = os.path.split(picn)
				small_nm_2 = '128px.'+new_title
				new_small_thumb = os.path.join(small_nm_1,small_nm_2)
				print(new_small_thumb)
				if os.path.exists(new_small_thumb):
					os.remove(new_small_thumb)


class MySlider(QtWidgets.QSlider):
	def __init__(self, parent):
		super(MySlider, self).__init__(parent)
		self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
	def mouseMoveEvent(self, event): 
		#print "hello"
		#print event.pos()
		global Player
		
		t = self.minimum() + ((self.maximum()-self.minimum()) * event.x()) / self.width()
		if Player == "mplayer":
			l=str((datetime.timedelta(milliseconds=t)))
		elif Player == "mpv":
			l=str((datetime.timedelta(seconds=t)))
		else:
			l = str(0)
		if '.' in l:
			l = l.split('.')[0]
		self.setToolTip(l)
		#ui.tab_5.show()
		#ui.tab_5.setFocus()
	def mousePressEvent(self, event):
		global mpvplayer,Player,current_playing_file_path
		old_val = self.value()
		self.setValue(self.minimum() + ((self.maximum()-self.minimum()) * event.x()) / self.width())
		event.accept()
		new_val = self.value()
		
		if mpvplayer:
			
			if mpvplayer.processId() > 0:
				if Player== "mpv":
					var = bytes('\n'+"seek "+str(new_val)+" absolute"+'\n','utf-8')
					mpvplayer.write(var)
				elif Player =="mplayer":
					#t = t/1000
					#t = int(t)
					seek_val = int((new_val-old_val)/1000)
					#var = bytes('\n'+"seek "+str(t)+" 2"+'\n','utf-8')
					var = bytes('\n'+"seek "+str(seek_val)+'\n','utf-8')
					mpvplayer.write(var)
		

	
	
		
		


class List1(QtWidgets.QListWidget):
	def __init__(self, parent):
		super(List1, self).__init__(parent)
		self.setDefaultDropAction(QtCore.Qt.MoveAction)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

	#def mouseMoveEvent(self,event):
		#ui.dockWidget_3.hide()
		#if ui.page_number.hasFocus():
			#self.setFocus()
	def mouseMoveEvent(self, event): 
		global ui
		if ui.auto_hide_dock and not ui.dockWidget_3.isHidden():
			ui.dockWidget_3.hide()
		self.setFocus()
	def dropEvent(self, event):
		if event.source() == self and (event.dropAction() == QtCore.Qt.MoveAction or self.dragDropMode() == QtWidgets.QAbstractItemView.InternalMove):
			global posterManually,site,home,pre_opt,opt,base_url,bookmark,name,embed,status,siteName,original_path_name
			i = self.currentItem()
			item = i.text()
			itemR = self.currentRow()
			print ("Mouse Release")
			print (item)
			p = self.itemAt(event.pos())
			m = p.text()
			n = self.row(p)
			print (n)
			print (itemR)
			if itemR != n:
				self.takeItem(itemR)
				del i
				self.insertItem(n,item)
			
				if bookmark == "True" or opt == "History":
					file_path = ""
					if bookmark == "True":
						if os.path.exists(os.path.join(home,'Bookmark',status+'.txt')):
							file_path = os.path.join(home,'Bookmark',status+'.txt')
							#f = open(file_path,'r')
							#l = f.readlines()
							#f.close()
							l = open_files(file_path,True)
							lines = []
							for i in l:
								i = re.sub('\n','',i)
								lines.append(i)
								
							if n > itemR:
								t = lines[itemR]
								i = itemR
								while(i < n):
									lines[i] = lines[i+1]
									i = i+1
								lines[n] = t
							else:
								i = itemR
								t = lines[itemR]
								while(i > n):
									lines[i] = lines[i-1]
									i = i -1
								lines[n]=t
							j = 0
							length = len(lines)
							"""
							f = open(file_path,'w')
							for i in lines:
								if j == length - 1:
									f.write(i)
								else:
									f.write(i+'\n')
								j = j+1
							f.close()
							"""
							write_files(file_path,lines,line_by_line=True)
							self.clear()
							for i in lines:
								j = i.split(':')
								self.addItem(j[-1])
							self.setCurrentRow(n)
					else:
						if site == "SubbedAnime" or site == "DubbedAnime":
							if os.path.exists(os.path.join(home,'History',site,siteName,'history.txt')):
								file_path = os.path.join(home,'History',site,siteName,'history.txt')
							
						else:
							if os.path.exists(os.path.join(home,'History',site,'history.txt')):
								file_path = os.path.join(home,'History',site,'history.txt')
						"""
						f = open(file_path,'w')
						i = 0
						length = self.count()
						while(i < length):
							j = self.item(i).text()
							if i == length - 1:
								f.write(j)
							else:
								f.write(j+'\n')
							i = i+1
						f.close()
						"""
						write_files(file_path,original_path_name,line_by_line=True)
						self.setCurrentRow(n)
		
		else:
		
			QListWidget.dropEvent(event)


	def hello(self):
		print ("world")
	def keyPressEvent(self, event):
		global posterManually,site,home,pre_opt,opt,base_url,bookmark,name,embed,status,siteName,finalUrlFound,refererNeeded,nameListArr,original_path_name,curR,original_path_name,show_hide_titlelist,show_hide_playlist
		if event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Right:
			ui.posterfound("")
		elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_C:
			ui.copyFanart()
		elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_C:
			ui.copyFanart()
		elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Delete:
			row = self.currentRow()
			file_path = ""
			if site == "SubbedAnime" or site == "DubbedAnime":
				if os.path.exists(os.path.join(home,'History',site,siteName,'history.txt')):
					file_path = os.path.join(home,'History',site,siteName,'history.txt')
				
			else:
				if os.path.exists(os.path.join(home,'History',site,'history.txt')):
					file_path = os.path.join(home,'History',site,'history.txt')
			
			if os.path.exists(file_path):
				row = self.currentRow()
				item = self.item(row)
				if item:
					
					self.takeItem(row)
					
					del item
					del original_path_name[row]
					length = self.count()-1
					"""
					f = open(file_path,'w')
					for i in range(self.count()):
						fname = original_path_name[i]
						if i == length:
							f.write(str(fname))
						else:
							f.write(str(fname)+'\n')
					f.close()
					"""
					write_files(file_path,original_path_name,line_by_line=True)
			
		elif event.modifiers() == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_C:
			ui.copySummary()
		elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_B:
			if bookmark == "False":
				if opt != "History":
					ui.listfound()
				tmp = site+':'+"History"+':'+siteName+':'+str(base_url)+':'+str(embed)+':'+name+':'+finalUrlFound+':'+refererNeeded
				file_path = os.path.join(home,'Bookmark','bookmark.txt')
				"""
				if not os.path.exists(file_path) or (os.stat(file_path).st_size == 0):
					
					f = open(file_path,'w')
					f.write(tmp)
					f.close()
				else:
					f = open(file_path,'a')
					f.write('\n'+tmp)
					f.close()
				"""
				write_files(file_path,tmp,line_by_line=True)
				note = name + " is Bookmarked"
				#subprocess.Popen(['notify-send',note])
				send_notification(note)
		
		elif event.key() == QtCore.Qt.Key_PageUp:
			if bookmark == "True":
				file_path = os.path.join(home,'Bookmark',status+'.txt')
				if os.path.exists(file_path):
					#f = open(file_path,'r')
					#lins = f.readlines()
					#f.close()
					lins = open_files(file_path,True)
					lines = []
					for i in lins:
						i = re.sub('\n','',i)
						lines.append(i)
					
					r = self.currentRow()
					length = self.count()
					if r == 0:
						p = length - 1
					else:
						p = r - 1
					if length > 1:
						t = lines[r]
						lines[r] = lines[p]
						lines[p] = t
						"""
						f = open(file_path,'w')
						k = 1
						while(k < length):
							lines[k] = '\n'+lines[k]
							k = k+1
						for i in lines:
							f.write(i)
						f.close()
						"""
						write_files(file_path,lines,line_by_line=True)
						self.clear()
						original_path_name[:] = []
						for i in lines:
							i = i.strip()
							j = i.split(':')
							if j[5].startswith('@'):
								self.addItem(j[5].split('@')[-1])
							elif '	' in j[5]:
								k = j[5].split('	')[0]
								self.addItem(k)	
							else:
								self.addItem(j[5])
							original_path_name.append(j[5])
							
						self.setCurrentRow(p)
			elif opt == "History" and site!= "Music":
				if site == "SubbedAnime" or site == "DubbedAnime":
					if os.path.exists(os.path.join(home,'History',site,siteName,'history.txt')):
						file_path = os.path.join(home,'History',site,siteName,'history.txt')
			
				else:
					if os.path.exists(os.path.join(home,'History',site,'history.txt')):
						file_path = os.path.join(home,'History',site,'history.txt')
				row = self.currentRow()
				if row == 0:
					prev_row = self.count()-1
				else:
					prev_row = row - 1
					
				original_path_name[row],original_path_name[prev_row] = original_path_name[prev_row],original_path_name[row]
				"""
				if os.path.exists(file_path):
					f = open(file_path,'w')
					j = 0
					for i in original_path_name:
						i = i.strip()
						if j == 0:
							f.write(i)
						else:
							f.write('\n'+i)
						j = j+1
				"""
				if os.path.exists(file_path):
					write_files(file_path,original_path_name,line_by_line=True)
				self.clear()
				for i in original_path_name:
					if '	' in i:
						i = i.split('	')[0]
					self.addItem(i)
				self.setCurrentRow(prev_row)
				"""
				epn = str(self.currentItem().text())
				row = self.currentRow()
				if row == 0:
					prev_r = self.count()-1
				else:
					prev_r = self.currentRow() - 1
				self.setCurrentRow(prev_r)
				epn_prev = str(self.currentItem().text())
				if row==0:
					f = open(file_path,'r')
					lines = f.readlines()
					f.close()
					lines[0]=epn_prev+'\n'
					lines[prev_r]=epn
					f = open(file_path,'w')
					for i in lines:
						f.write(i)
					f.close()
				else:
					nepn = epn_prev +'\n'
					#print nepn
					replc = epn +'\n#'
					#print replc
					replace_line(file_path,nepn,replc)
					nepn = '#'+epn
					#print nepn
					replc = epn_prev
					replace_line(file_path,nepn,replc)
				self.clear()
				f = open(file_path, 'r')
				lines = f.readlines()
				last_line = str(lines[-1])
				first_line = str(lines[0])
				print (last_line)
				print (first_line)
				f.close()
				for i in lines:
					i = re.sub("\n","",i)
					self.addItem(i)
				self.setCurrentRow(prev_r)
				"""
		elif event.key() == QtCore.Qt.Key_PageDown:
			if bookmark == "True":
				file_path = os.path.join(home,'Bookmark',status+'.txt')
				if os.path.exists(file_path):
					#f = open(file_path,'r')
					#lins = f.readlines()
					#f.close()
					lins = open_files(file_path,True)
					lines = []
					for i in lins:
						i = re.sub('\n','',i)
						lines.append(i)
					
					r = self.currentRow()
					length = self.count()
					if r == length -1:
						p = 0
					else:
						p = r + 1
					if length > 1:
						t = lines[r]
						lines[r] = lines[p]
						lines[p] = t
						"""
						f = open(file_path,'w')
						k = 1
						while(k < length):
							lines[k] = '\n'+lines[k]
							k = k+1
						for i in lines:
							f.write(i)
						f.close()
						"""
						write_files(file_path,lines,line_by_line=True)
						self.clear()
						original_path_name[:] = []
						for i in lines:
							i = re.sub('\n','',i)
							j = i.split(':')
							if j[5].startswith('@'):
								self.addItem(j[5].split('@')[-1])
							elif '	' in j[5]:
								k = j[5].split('	')[0]
								self.addItem(k)
							else:
								self.addItem(j[5])
							original_path_name.append(j[5])
						self.setCurrentRow(p)
			elif opt =="History" and site!= "Music":
				if site == "SubbedAnime" or site == "DubbedAnime":
					if os.path.exists(os.path.join(home,'History',site,siteName,'history.txt')):
						file_path = os.path.join(home,'History',site,siteName,'history.txt')
			
				else:
					if os.path.exists(os.path.join(home,'History',site,'history.txt')):
						file_path = os.path.join(home,'History',site,'history.txt')
				row = self.currentRow()
				if row == (self.count() - 1):
					next_row = 0
				else:
					next_row = row+1
					
				original_path_name[row],original_path_name[next_row] = original_path_name[next_row],original_path_name[row]
				"""
				if os.path.exists(file_path):
					f = open(file_path,'w')
					j = 0
					for i in original_path_name:
						i = i.strip()
						if j == 0:
							f.write(i)
						else:
							f.write('\n'+i)
						j = j+1
				"""
				if os.path.exists(file_path):
					write_files(file_path,original_path_name,line_by_line=True)
				self.clear()
				for i in original_path_name:
					if '	' in i:
						i = i.split('	')[0]
					self.addItem(i)
				self.setCurrentRow(next_row)
				"""
				epn = str(self.currentItem().text())
				row = self.currentRow()
				if row == self.count() - 1:
					next_r = 0
				else:
					next_r = self.currentRow() + 1
				self.setCurrentRow(next_r)
				epn_next = str(self.currentItem().text())
				if row == self.count() - 1:
					f = open(file_path,'r')
					lines = f.readlines()
					f.close()
					lines[next_r]=epn+'\n'
					lines[self.count()-1]=epn_next
					f = open(file_path,'w')
					for i in lines:
						f.write(i)
					f.close()
				else:
					nepn = epn +'\n'
					#print nepn
					replc = epn_next +'\n#'
					#print replc
					replace_line(file_path,nepn,replc)
					nepn = '#'+epn_next
					#print nepn
					replc = epn
					replace_line(file_path,nepn,replc)
				self.clear()
				f = open(file_path, 'r')
				lines = f.readlines()
				last_line = str(lines[-1])
				first_line = str(lines[0])
				print (last_line)
				print (first_line)
				f.close()
				for i in lines:
					i = re.sub("\n","",i)
					self.addItem(i)
				self.setCurrentRow(next_r)
				"""
		elif event.key() == QtCore.Qt.Key_Delete:
			r = self.currentRow()
			item = self.item(r)
			if item:
				if site == "PlayLists":
					index = self.currentRow()
					item_r  = self.item(index)
					if item_r:
						item = str(self.currentItem().text())
						if item != "Default":
							file_pls = os.path.join(home,'Playlists',item)
							if os.path.exists(file_pls):
								os.remove(file_pls)
							self.takeItem(index)
							del item_r
							ui.list2.clear()
				elif site == "Video" and bookmark == "False":
					video_db = os.path.join(home,'VideoDB','Video.db')
					conn = sqlite3.connect(video_db)
					cur = conn.cursor()
					
					txt = original_path_name[r].split('	')[1]
					cur.execute('Delete FROM Video Where Directory="'+txt+'"')
					print ('Deleting Directory From Database : '+txt)
					del original_path_name[r]
					conn.commit()
					conn.close()
					self.takeItem(r)
					del item
					
				elif site == "Music":
					list3n = (ui.list3.currentItem().text())
					if list3n == "Fav-Artist" or list3n == "Fav-Album" or list3n=="Fav-Directory":
						conn = sqlite3.connect(os.path.join(home,'Music','Music.db'))
						cur = conn.cursor()
						qVal = str(self.currentItem().text())
						print (qVal,'--qval')
						tmp = str(ui.list3.currentItem().text())
						if tmp == "Fav-Artist":
							qr = 'Update Music Set Favourite="no" Where Artist=?'
							cur.execute(qr,(qVal,))
						elif tmp == "Fav-Album":
							qr = 'Update Music Set Favourite="no" Where Album=?'
							cur.execute(qr,(qVal,))
						elif tmp == "Fav-Directory":
							qr = 'Update Music Set Favourite="no" Where Directory=?'
							cur.execute(qr,(qVal,))
						print ("Number of rows updated: %d" % cur.rowcount)
						
						conn.commit()
						conn.close()
						ui.options_clicked()
						self.setCurrentRow(r)
				elif site == 'None':
					print("Nothing to delete")
				else:
					ui.deleteHistory()
			
		elif event.key() == QtCore.Qt.Key_H:
			ui.setPreOpt()
		
		elif event.key() == QtCore.Qt.Key_D:
			ui.deleteArtwork()
		elif event.key() == QtCore.Qt.Key_M:
			#poster = "/tmp/AnimeWatch/" + name + "-poster.txt"
			#fanart ="/tmp/AnimeWatch/" + name + "-fanart.txt"
			poster = os.path.join(TMPDIR,name+"-poster.txt")
			fanart = os.path.join(TMPDIR,name+"-fanart.txt")
			if os.path.isfile(poster):
				os.remove(poster)
			if os.path.isfile(fanart):
				os.remove(fanart)
			posterManually = 1
			ui.posterfound("")
		elif event.key() == QtCore.Qt.Key_I:
			ui.showImage()
		elif event.key() == QtCore.Qt.Key_R:
			#if opt != "History":
			ui.shuffleList()
		elif event.key() == QtCore.Qt.Key_T:
			#if opt != "History":
			ui.sortList()
		elif event.key() == QtCore.Qt.Key_Y:
			#if opt != "History":
			ui.getList()
		elif event.key() == QtCore.Qt.Key_C:
			ui.copyImg()
			#MainWindow.showFullScreen()
			#ui.centralwidget.showFullScreen()
			#ui.tabWidget1.showFullScreen()
		
		elif event.key() == QtCore.Qt.Key_Return:
			ui.list1_double_clicked()
			"""
			ui.listfound()
			if site == "Music" and not ui.list2.isHidden():
				ui.list2.setFocus()
				ui.list2.setCurrentRow(0)
				curR = 0
				ui.epnfound()
				self.show()
				ui.frame.show()
				
				self.setFocus()
			else:
				if ui.list2.isHidden():
					ui.list1.hide()
					ui.frame.hide()
					ui.list2.show()
					ui.goto_epn.show()
					ui.list2.setFocus()
					show_hide_titlelist = 0
					show_hide_playlist = 1
			ui.update_list2()
			"""
		elif event.key() == QtCore.Qt.Key_Right:
			#ui.list_highlight()
			ui.list2.setFocus()
		elif event.key() == QtCore.Qt.Key_Left:
			ui.btn1.setFocus()
			ui.dockWidget_3.show()
			#ui.label.setMinimumSize(350,400)
		elif event.key() == QtCore.Qt.Key_Period:
			if site == "Music":
				ui.mpvNextEpnList()
			else:
				ui.nextp(ui.list3.currentRow())
		elif event.key() == QtCore.Qt.Key_Comma:
			if site == "Music":
				ui.mpvPrevEpnList()
			else:
				ui.backp(ui.list3.currentRow())
		elif event.key() == QtCore.Qt.Key_Down:
			nextr = self.currentRow() + 1
			if nextr == self.count():
				self.setCurrentRow(0)
			else:
				self.setCurrentRow(nextr)
		elif event.key() == QtCore.Qt.Key_Up:
			prev_r = self.currentRow() - 1
			if self.currentRow() == 0:
				self.setCurrentRow(self.count()-1)
			else:
				self.setCurrentRow(prev_r)
		
		#super(List1, self).keyPressEvent(event)
	def addBookmarkList(self):
		global name,tmp_name,opt,list1_items,curR,nxtImg_cnt,home,site,pre_opt,base_url,bookmark,status,siteName,finalUrlFound,refererNeeded
		if bookmark == "False":
				if opt != "History":
					ui.listfound()
				if site == "Music" or site == "Video":
					if ui.list3.currentItem():
						music_opt = str(ui.list3.currentItem().text())
						tmp = site+':'+(music_opt)+':'+siteName+':'+str(base_url)+':'+str(embed)+':'+name+':'+str(finalUrlFound)+':'+str(refererNeeded)
					else:
						return 0
				else:
					tmp = site+':'+"History"+':'+siteName+':'+str(base_url)+':'+str(embed)+':'+name+':'+str(finalUrlFound)+':'+str(refererNeeded)
				file_path = os.path.join(home,'Bookmark','bookmark.txt')
				write_files(file_path,tmp,line_by_line=True)
				
				"""
				if os.path.exists(file_path):
					f = open(file_path,'r')
					lines = f.readlines()
					f.close()
					lines.append(tmp)
					
					f = open(file_path,'w')
					for i in lines:
						i = i.replace('\n','')
						if i:
							f.write(i+'\n')
					f.close()
					
				elif not os.path.exists(file_path) or (os.stat(file_path).st_size == 0):
					
					f = open(file_path,'w')
					f.write(tmp)
					f.close()
					
				"""
				note = name + " is Bookmarked"
				#subprocess.Popen(['notify-send',note])
				
	def triggerBookmark(self,val):
		global name,tmp_name,opt,list1_items,curR,nxtImg_cnt,home,site,pre_opt,base_url,bookmark,status,siteName,finalUrlFound,refererNeeded,video_local_stream
		
		if bookmark == "False":
			self.addBookmarkList()
		if site == "Music" or site == "Video":
			if ui.list3.currentItem():
				music_opt = str(ui.list3.currentItem().text())
				tmp = site+':'+(music_opt)+':'+siteName+':'+str(base_url)+':'+str(embed)+':'+name+':'+str(finalUrlFound)+':'+str(refererNeeded)+':'+str(video_local_stream)
			else:
				return 0
			
		else:
			if ui.list1.currentItem():
				tmp = site+':'+"History"+':'+siteName+':'+str(base_url)+':'+str(embed)+':'+name+':'+str(finalUrlFound)+':'+str(refererNeeded)+':'+str(video_local_stream)
			else:
				return 0
		file_path = os.path.join(home,'Bookmark',val+'.txt')
		"""
		if os.path.exists(file_path):
			f = open(file_path,'r')
			lines = f.readlines()
			f.close()
			lines.append(tmp)
			f = open(file_path,'w')
			for i in lines:
				i = i.replace('\n','')
				if i:
					f.write(i+'\n')
			f.close()
		elif not os.path.exists(file_path) or (os.stat(file_path).st_size == 0):
			
			f = open(file_path,'w')
			f.write(tmp)
			f.close()
		"""
		write_files(file_path,tmp,line_by_line=True)
		note = name + " is Added to "+val+" Category"
		#subprocess.Popen(['notify-send',note])
		send_notification(note)
		
	def triggerPlaylist(self,value):
		global epn,epn_name_in_list,path_final_Url,home,site,pre_opt,base_url,embed,name,epnArrList,opt,finalUrlFound,refererNeeded
		print ('Menu Clicked')
		print (value)
		#ui.epnfound_return()
		file_path = os.path.join(home,'Playlists',str(value))
		#print epnArrList
		for i in range(len(epnArrList)):
			
			
			if os.path.exists(file_path):
				#f = open(file_path,'a')
				
				sumr=str(epnArrList[i].split('	')[0])
				
				try:
					rfr_url=str(epnArrList[i].split('	')[2])
				except:
					rfr_url = "NONE"
				
				sumry = str(epnArrList[i].split('	')[1])
				sumry = sumry.replace('"','')
				sumry = '"'+sumry+'"'
				t = sumr+'	'+sumry+'	'+rfr_url
				"""
				if os.stat(file_path).st_size == 0:
					f = open(file_path,'w')
				else:
					f = open(file_path,'a')
					t = '\n'+t
				try:
					f.write(str(t))
				except:
					f.write(t.encode('utf-8'))
				#f.write(sumr+'	'+sumry+'	'+rfr_url+'\n')
				f.close()
				"""
				write_files(file_path,t,line_by_line=True)
				
	def contextMenuEvent(self, event):
			global name,tmp_name,opt,list1_items,curR,nxtImg_cnt,home,site,pre_opt,base_url,bookmark,status,posterManually,siteName,finalUrlFound,refererNeeded,original_path_name,video_local_stream
			if self.currentItem():
				name = str(ui.list1.currentItem().text())
			else:
				name = ''
			#print name
			if site == "Music":
				menu = QtWidgets.QMenu(self)
				#review = menu.addAction("Review")
				submenuR = QtWidgets.QMenu(menu)
				submenuR.setTitle("Add To PlayList")
				menu.addMenu(submenuR)
				fav = menu.addAction("Add To Favourite")
				r = ui.list3.currentRow()
				itm = ui.list3.item(r)
				if itm:
					music_opt = str(itm.text())
				else:
					music_opt = ""
				pls = os.listdir(os.path.join(home,'Playlists'))
				item_m = []
				for i in pls:
					i = i.replace('.txt','')
					item_m.append(submenuR.addAction(i))
					#receiver = lambda taskType=i: self.triggerPlaylist(taskType)
					#item.triggered.connect(receiver)
				submenuR.addSeparator()
				new_pls = submenuR.addAction("Create New Playlist")
				profile = menu.addAction("Find Last.fm Profile(manually)")
				default = menu.addAction("Set Default Background")
				delPosters = menu.addAction("Delete Poster")
				delFanart = menu.addAction("Delete Fanart")
				delThumb = menu.addAction("Delete Playlist Thumbnails")
				delInfo = menu.addAction("Delete Info")
				go_to = menu.addAction("Go To Last.fm")
				thumbnail = menu.addAction("Show Thumbnail View")
				cache = menu.addAction("Clear Cache")
				action = menu.exec_(self.mapToGlobal(event.pos()))
				
				for i in range(len(item_m)):
					if action == item_m[i]:
						self.triggerPlaylist(pls[i].replace('.txt',''))
				
				if action == fav:
					r = self.currentRow()
					item = self.item(r)
					if item and music_opt!="Playlist" and music_opt!= "Fav-Artist" and music_opt!= "Fav-Album" and music_opt!= "Fav-Directory":
						txt = str(item.text())
						ui.updateMusicCount('fav',txt)
					else:
						print ("Not Permitted")
				elif action == cache:
						m = os.listdir(TMPDIR)
						for i in m:
							if '.txt' in i or '.jpg' in i:
								t = os.path.join(TMPDIR,i)
								os.remove(t)
				elif action == new_pls:
					print ("creating")
					item, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Input Dialog', 'Enter Playlist Name')
					if ok and item:
						file_path = os.path.join(home,'Playlists',item)
						if not os.path.exists(file_path):
							f = open(file_path,'w')
							f.close()
				elif action == profile:
					if '/' in name:
						nam = name.replace('/','-')
					else:
						nam = name
					#ui.reviewsMusic("Last.Fm")
					ui.reviewsWeb(srch_txt=nam,review_site='last.fm',action='search_by_name')
				elif action == thumbnail:
					if site == "Local" or bookmark == "True" or opt == "History" or site == "Video" or site == "Music":
						if ui.list3.currentItem():
							if (ui.list3.currentItem().text())=="Artist":
								ui.scrollArea.setFocus()
								ui.lock_process = True
								ui.IconView()
								ui.lock_process = False
				elif action == delInfo or action == delPosters or action == default or action == delThumb or action == delFanart:
					if (ui.list3.currentItem()):
						if str(ui.list3.currentItem().text()) == "Artist":
							if '/' in name:
								nam = name.replace('/','-')
							else:
								nam = name
							 	
						else:
								try:
									r = ui.list2.currentRow()
								
									nam = epnArrList[r].split('	')[2]
								except:
									nam = ""
									
								if '/' in nam:
									nam = nam.replace('/','-')
								else:
									nam = nam
						
						if nam:
							picn = os.path.join(home,'Music','Artist',nam,'poster.jpg')
							fanart = os.path.join(home,'Music','Artist',nam,'fanart.jpg')
							default_wall = os.path.join(home,'default.jpg')
							sumr = os.path.join(home,'Music','Artist',nam,'bio.txt')
							dir_n = os.path.join(home,'Music','Artist',nam)
							if os.path.exists(dir_n):
								if action == delInfo:
									m=os.listdir(dir_n)
									for i in m:
										if i.endswith('.txt'):
											f = open(os.path.join(dir_n,'bio.txt'),'w')
											f.write('No Information Available')
											f.close()
									m = os.listdir(TMPDIR)
									for i in m:
										if i.endswith('.jpg') or i.endswith('.txt'):
											t = os.path.join(TMPDIR,i)
											os.remove(t)
								elif action == delPosters:
									m=os.listdir(dir_n)
									for i in m:
										if i.endswith('.jpg'):
											os.remove(os.path.join(dir_n,i))
									m = os.listdir(TMPDIR)
									for i in m:
										if i.endswith('.jpg') or i.endswith('.txt'):
											t = os.path.join(TMPDIR,i)
											os.remove(t) 
								elif action == delThumb:
									m=os.listdir(dir_n)
									for i in m:
										print(i)
										if i.startswith('256px') or i.startswith('128px'):
											os.remove(os.path.join(dir_n,i))
									m = os.listdir(TMPDIR)
									for i in m:
										if i.startswith('256x') or i.startswith('128x'):
											t = os.path.join(TMPDIR,i)
											os.remove(t) 
								elif action == delFanart:
									m=os.listdir(dir_n)
									for i in m:
										if i.startswith('fanart'):
											os.remove(os.path.join(dir_n,i))
									m = os.listdir(TMPDIR)
									for i in m:
										if i.startswith('fanart'):
											t = os.path.join(TMPDIR,i)
											os.remove(t)
								elif action == default:
									shutil.copy(default_wall,picn)
									shutil.copy(default_wall,fanart)
									ui.videoImage(picn,os.path.join(home,'Music','Artist',nam,'thumbnail.jpg'),fanart,'')
				elif action == go_to:
					if '/' in name:
						nam = name.replace('/','-')
					else:
						nam = name
					#ui.reviewsMusic("Last.Fm")
					ui.reviewsWeb(srch_txt=nam,review_site='last.fm',action='search_by_name')
			else:
				menu = QtWidgets.QMenu(self)
				#review = menu.addAction("Review")
				submenuR = QtWidgets.QMenu(menu)
				submenuR.setTitle("Find Information")
				menu.addMenu(submenuR)
				submenu = QtWidgets.QMenu(menu)
				submenu.setTitle("Bookmark Options")
				menu.addMenu(submenu)
				#if bookmark == "True":
				submenu_arr_dict = {'mal':'MyAnimeList','ap':'Anime-Planet','ans':'Anime-Source','tvdb':'TVDB','ann':'ANN','anidb':'AniDB','g':'Google','yt':'Youtube','ddg':'DuckDuckGo','last.fm':'last.fm','zerochan':'Zerochan'}
				reviews = []
				for i in submenu_arr_dict:
					reviews.append(submenuR.addAction(submenu_arr_dict[i]))
				
				addBookmark = submenu.addAction("Add Bookmark")
				
				bookmark_array = ['bookmark']
				pls = os.listdir(os.path.join(home,'Bookmark'))
				item_m = []
				for i in pls:
					i = i.replace('.txt','')
					if i not in bookmark_array:
						item_m.append(submenu.addAction(i))
					
				submenu.addSeparator()
				new_pls = submenu.addAction("Create New Bookmark Category")
				
				sideBar = menu.addAction("Show Side Bar")
				thumbnail = menu.addAction("Show Thumbnail View")
				history = menu.addAction("History")
				#rmPoster = menu.addAction("Remove Poster")
				tvdb	= menu.addAction("Find Image(TVDB)")
				tvdbM	= menu.addAction("Find Image(TVDB Manually)")
				
				cache = menu.addAction("Clear Cache")
				del_history = menu.addAction("Delete (Only For History)")
				action = menu.exec_(self.mapToGlobal(event.pos()))
				
				for i in range(len(item_m)):
					if action == item_m[i]:
						item_name = item_m[i].text()
						self.triggerBookmark(item_name)
				for i in range(len(reviews)):
					if action == reviews[i]:
						ui.reviewsWeb(srch_txt=name,review_site=list(submenu_arr_dict.keys())[list(submenu_arr_dict.values()).index(reviews[i].text())],action='context_menu')
						
				if action == new_pls:
					print ("creating new bookmark category")
					item, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Input Dialog', 'Enter Playlist Name')
					if ok and item:
						file_path = os.path.join(home,'Bookmark',item+'.txt')
						if not os.path.exists(file_path):
							f = open(file_path,'w')
							f.close()
				elif action == sideBar:
					if ui.dockWidget_3.isHidden():
						ui.dockWidget_3.show()
						ui.btn1.setFocus()
					else:
						ui.dockWidget_3.hide()
						ui.list1.setFocus()
				elif action == del_history:
					ui.deleteHistory()
					
				elif action == addBookmark:
					self.addBookmarkList()
					
				elif action == thumbnail:
					if (site == "Local" or site == 'PlayLists') or bookmark == "True" or opt == "History" or site == "Video":
						ui.scrollArea.setFocus()
						ui.lock_process = True
						ui.IconView()
						ui.lock_process = False
				elif action == cache:
						m = os.listdir(TMPDIR)
						for i in m:
							if '.txt' in i or '.jpg' in i:
								t = os.path.join(TMPDIR,i)
								os.remove(t)
				elif action == tvdb:
					if self.currentItem():
						ui.posterfound("")
						r = self.currentRow()
						ui.copyImg()
						ui.copySummary()
						#ui.copyFanart()
				elif action == history:
					ui.setPreOpt()
				elif action == tvdbM:
					ui.reviewsWeb(srch_txt=name,review_site='tvdb',action='context_menu')
class List2(QtWidgets.QListWidget):
	def __init__(self, parent):
		super(List2, self).__init__(parent)
		self.setDefaultDropAction(QtCore.Qt.MoveAction)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
		self.downloadWget = []
		self.downloadWget_cnt = 0
		#self.setViewMode(QtWidgets.QListWidget.IconMode)
		#self.setIconSize(QtCore.QSize(200,200))
		#self.setResizeMode(QtWidgets.QListWidget.Adjust)
	#def mouseMoveEvent(self,event):
	#ui.dockWidget_3.hide()
	#if not self.hasFocus():
	#	self.setFocus()
	def mouseMoveEvent(self, event): 
		global ui
		if ui.auto_hide_dock and not ui.dockWidget_3.isHidden():
			ui.dockWidget_3.hide()
		self.setFocus()
		
	def dropEvent(self, event):
		if event.source() == self and (event.dropAction() == QtCore.Qt.MoveAction or self.dragDropMode() == QtWidgets.QAbstractItemView.InternalMove):
			global posterManually,site,home,pre_opt,opt,base_url,bookmark,name,embed,status,name,epnArrList,siteName
			i = self.currentItem()
			item = i.text()
			itemR = self.currentRow()
			print ("Mouse Release")
			print (item)
			p = self.itemAt(event.pos())
			m = p.text()
			n = self.row(p)
			print (n)
			print (itemR)
			if itemR != n:
				self.takeItem(itemR)
				del i
				self.insertItem(n,item)
			
				if opt == "History" or site == "PlayLists":
							file_path = ""
				
							if site == "SubbedAnime" or site == "DubbedAnime":
								if os.path.exists(os.path.join(home,'History',site,siteName,name,'Ep.txt')):
									file_path = os.path.join(home,'History',site,siteName,name,'Ep.txt')
								
							elif site == "PlayLists":
								pls = ui.list1.currentItem().text()
								file_path = os.path.join(home,'Playlists',pls)
							else:
								if os.path.exists(os.path.join(home,'History',site,name,'Ep.txt')):
									file_path = os.path.join(home,'History',site,name,'Ep.txt')
				
							if os.path.exists(file_path):
								#f = open(file_path,'r')
								#l = f.readlines()
								#f.close()
								l = open_files(file_path,True)
								lines = []
								for i in l:
									i = i.replace('\n','')
									lines.append(i)
									
								if n > itemR:
									t = lines[itemR]
									i = itemR
									while(i < n):
										lines[i] = lines[i+1]
										i = i+1
									lines[n] = t
								else:
									i = itemR
									t = lines[itemR]
									while(i > n):
										lines[i] = lines[i-1]
										i = i -1
									lines[n]=t
								j = 0
								length = len(lines)
								epnArrList[:]=[]
								#f = open(file_path,'w')
								for i in lines:
									epnArrList.append(i)
									#if j == length - 1:
									#	f.write(i)
									#else:
									#	f.write(i+'\n')
									j = j+1
								#f.close()
								write_files(file_path,lines,line_by_line=True)
								self.clear()
								if site != "PlayLists":
									ui.update_list2()
								else:
									for i in lines:
										self.addItem(i)
								self.setCurrentRow(n)
		
		else:
			QListWidget.dropEvent(event)
	def init_offline_mode(self):
		global site,wget,downloadVideo
		print(self.currentRow(),'--init--offline--')
		if site.lower() != "Local" and site.lower() != 'video' and site.lower() != 'music':
			if wget.processId() == 0:
				downloadVideo = 1
				r = self.currentRow()
				item = self.item(r)
				if item:
					ui.start_offline_mode(r)
			else:
				if not ui.queue_url_list:
					ui.list6.clear()
				r = self.currentRow()
				item = self.item(r)
				if item:
					ui.queue_url_list.append(r)
					txt = epnArrList[r].split('	')[0].replace('_',' ')
					if txt.startswith('#'):
						txt = txt.replace('#','',1)
					ui.list6.addItem(txt)
	def keyPressEvent(self, event):
		global wget,queueNo,mpvAlive,mpv,downloadVideo,quality,mirrorNo,startPlayer,getSize,finalUrl,site,hdr,rfr_url,curR,base_url,new_epn,epnArrList,show_hide_playlist,show_hide_titlelist
		global site,opt,pre_opt,name,siteName,Player,total_till,video_local_stream
		if event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Left:
			ui.tab_5.setFocus()
		elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Up:
			self.setCurrentRow(0)
		elif event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Down:
			self.setCurrentRow(self.count()-1)
		elif event.key() == QtCore.Qt.Key_Return:
			curR = self.currentRow()
			queueNo = queueNo + 1
			mpvAlive = 0
			ui.epnfound()
		
		elif event.key() == QtCore.Qt.Key_Backspace:
			if ui.list1.isHidden() and ui.list1.count() > 0:
				ui.list2.hide()
				ui.goto_epn.hide()
				ui.list1.show()
				#ui.frame.show()
				ui.list1.setFocus()
				show_hide_playlist = 0
				show_hide_titlelist = 1
		elif event.key() == QtCore.Qt.Key_Down:
			nextr = self.currentRow() + 1
			if nextr == self.count():
				#self.setCurrentRow(0)
				self.setCurrentRow(self.count()-1)
			else:
				self.setCurrentRow(nextr)
		elif event.key() == QtCore.Qt.Key_Up:
			prev_r = self.currentRow() - 1
			if self.currentRow() == 0:
				#self.setCurrentRow(self.count()-1)
				self.setCurrentRow(0)
			else:
				self.setCurrentRow(prev_r)
		elif event.key() == QtCore.Qt.Key_W:
			ui.watchToggle()
		elif event.key() == QtCore.Qt.Key_Q:
			if site == "Music" or site == "Video" or site == "Local" or site == "PlayLists" or site == "None":
				file_path = os.path.join(home,'Playlists','Queue')
				if not os.path.exists(file_path):
					f = open(file_path,'w')
					f.close()
					
				if not ui.queue_url_list:
					ui.list6.clear()
				r = self.currentRow()
				item = self.item(r)
				if item:
					ui.queue_url_list.append(epnArrList[r])
					ui.list6.addItem(epnArrList[r].split('	')[0])
					print (ui.queue_url_list)
					"""
					if os.stat(file_path).st_size == 0:
						f = open(file_path,'w')
						f.write(epnArrList[r])
					else:
						f = open(file_path,'a')
						f.write('\n'+epnArrList[r])
					f.close()
					"""
					write_files(file_path,epnArrList[r],line_by_line=True)
			elif video_local_stream:
				#if not ui.local_file_index:
				#	ui.list6.clear()
				#ui.local_file_index.append(self.currentRow())
				if ui.list6.count() >0:
					txt = ui.list6.item(0).text()
					if txt.startswith('Queue Empty:'):
						ui.list6.clear()
				if self.currentItem():
					ui.list6.addItem(self.currentItem().text()+':'+str(self.currentRow()))
			else:
				if not ui.queue_url_list:
					ui.list6.clear()
				r = self.currentRow()
				item = self.item(r)
				if item:
					ui.queue_url_list.append(r)
					ui.list6.addItem(epnArrList[r].split('	')[0])
				#ui.local_file_index.append(ui.list6.count())
		elif event.key() == QtCore.Qt.Key_Delete:
			if site == 'None':
				print("Nothing To Delete")
			elif site == "Video":
				r = self.currentRow()
				item = self.item(r)
				if item:
					if bookmark == "False":
						video_db = os.path.join(home,'VideoDB','Video.db')
						conn = sqlite3.connect(video_db)
						cur = conn.cursor()
						txt = epnArrList[r].split('	')[1]
						cur.execute('Delete FROM Video Where Path="'+txt+'"')
						print ('Deleting Directory From Database : '+txt)
						del epnArrList[r]
						conn.commit()
						conn.close()
						self.takeItem(r)
						del item
			elif site != "PlayLists" and site != "Video" and site != "Music" and opt == "History":
					row = self.currentRow()
					file_path = ""
					if site == "SubbedAnime" or site == "DubbedAnime":
						if os.path.exists(os.path.join(home,'History',site,siteName,name,'Ep.txt')):
							file_path = os.path.join(home,'History',site,siteName,name,'Ep.txt')
						
					else:
						if os.path.exists(os.path.join(home,'History',site,name,'Ep.txt')):
							file_path = os.path.join(home,'History',site,name,'Ep.txt')
					if file_path:
						ui.replace_lineByIndex(file_path,'','',row)
						ui.update_list2()
					else:
						pass
			elif site == "PlayLists" or (site == "Music" and ui.list3.currentItem()):
				go_next = True
				if site == 'Music' and ui.list3.currentItem():
					if ui.list3.currentItem().text()=="Playlist":
						go_next = True
					else:
						go_next = False
				if go_next:
					pls = ''
					if site == "Music":
						r = ui.list1.currentRow()
						if ui.list1.item(r):
							pls = str(ui.list1.item(r).text())
					else:
						if ui.list1.currentItem():
							pls = ui.list1.currentItem().text()
					if pls:
						file_path = os.path.join(home,'Playlists',pls)
						row = self.currentRow()
						item = self.item(row)
						#epnArrList[:]=[]
						if item and os.path.exists(file_path):
							
							self.takeItem(row)
							
							del item
							del epnArrList[row]
							"""
							f = open(file_path,'w')
							j = 0
							for i in range(self.count()):
								fname = epnArrList[i]
								if j == 0:
									f.write(fname)
								else:
									f.write('\n'+fname)
								j = j+1
							f.close()
							"""
							write_files(file_path,epnArrList,line_by_line=True)
		#elif event.key() == QtCore.Qt.Key_Q: 
		#	startPlayer = "No"
		#	ui.epnfound()
			
			
		elif event.key() == QtCore.Qt.Key_PageUp:
			row = self.currentRow()
			nRow = self.currentRow()-1
			if site == 'Music':
				if ui.list3.currentItem():
					if ui.list3.currentItem().text() == 'Playlist':
						opt = 'History'
						#print('playlist-update',ui.list3.currentItem().text())
			print(opt,row,site)
			
			if (opt == "History" or site =="PlayLists") and row > 0 and site!="Video":
				
				file_path = ""
				if site == "SubbedAnime" or site == "DubbedAnime":
					if os.path.exists(os.path.join(home,'History',site,siteName,name,'Ep.txt')):
						file_path = os.path.join(home,'History',site,siteName,name,'Ep.txt')
				elif site == "PlayLists" or site=="Music":
						pls = ''
						if site == "PlayLists":
							if ui.list1.currentItem():
								pls = ui.list1.currentItem().text()
						else:
							if ui.list1.currentItem():
								pls = ui.list1.currentItem().text()
						if pls:
							file_path = os.path.join(home,'Playlists',pls)
				else:
					if os.path.exists(os.path.join(home,'History',site,name,'Ep.txt')):
						file_path = os.path.join(home,'History',site,name,'Ep.txt')
				#ui.replace_lineByIndex(file_path,'','',row)
				if os.path.exists(file_path):
					#f = open(file_path,'r')
					#lines = f.readlines()
					#f.close()
					lines = open_files(file_path,True)
					length = len(lines)
					if row == length - 1:
						t = lines[row].replace('\n','')+'\n'
						lines[row]=lines[nRow].replace('\n','')
						lines[nRow]=t
					else:
						t = lines[row]
						lines[row]=lines[nRow]
						lines[nRow]=t
					epnArrList[:]=[]
					#f = open(file_path,'w')
					for i in lines:
						#f.write(i)
						j = i.strip()
						epnArrList.append(j)
					#f.close()
					write_files(file_path,lines,line_by_line=True)
					ui.update_list2()
					self.setCurrentRow(nRow)
					
					#if site != "PlayLists":
					#	ui.update_list2()
					#else:
					#	self.clear()
					#	for i in lines:
					#		i = i.replace('\n','')
					#		if i:
					#			if '	' in i:
					#				i = i.split('	')[0]
					#			self.addItem(i)
					#	self.setCurrentRow(nRow)
			elif site=="Video":
				r = self.currentRow()
				item = self.item(r)
				if item:
					if bookmark == "False":
						video_db = os.path.join(home,'VideoDB','Video.db')
						conn = sqlite3.connect(video_db)
						cur = conn.cursor()
						txt = epnArrList[r].split('	')[1]
						cur.execute('Select EPN FROM Video Where Path="'+txt+'"')
						rows = cur.fetchall()
						num1 = int(rows[0][0])
						print (num1,'--num1')
						if r >0:
							txt1 = epnArrList[r-1].split('	')[1]
							epnArrList[r],epnArrList[r-1]=epnArrList[r-1],epnArrList[r]
						else:
							txt1 = epnArrList[-1].split('	')[1]
							epnArrList[r],epnArrList[-1]=epnArrList[-1],epnArrList[r]
						cur.execute('Select EPN FROM Video Where Path="'+txt1+'"')
						rows = cur.fetchall()
						num2 = int(rows[0][0])
						print (num2,'---num2')
						qr = 'Update Video Set EPN=? Where Path=?'
						cur.execute(qr,(num2,txt))
						qr = 'Update Video Set EPN=? Where Path=?'
						cur.execute(qr,(num1,txt1))
						
						conn.commit()
						conn.close()
						self.takeItem(r)
						del item
						if r>0:
							self.insertItem(r-1,epnArrList[r-1].split('	')[0])
							row_n = r-1
						else:
							
							self.insertItem(len(epnArrList)-1,epnArrList[-1].split('	')[0])
							row_n = len(epnArrList)-1
						self.setCurrentRow(row_n)
						
		elif event.key() == QtCore.Qt.Key_PageDown:
			row = self.currentRow()
			nRow = self.currentRow()+1
			if site == 'Music':
				if ui.list3.currentItem():
					if ui.list3.currentItem().text() == 'Playlist':
						opt = 'History'
						#print('playlist-update',ui.list3.currentItem().text())
			print(opt,row,site)
			if (opt == "History" or site == "PlayLists") and row < self.count()-1 and site!="Video":
				
				file_path = ""
				if site == "SubbedAnime" or site == "DubbedAnime":
					if os.path.exists(os.path.join(home,'History',site,siteName,name,'Ep.txt')):
						file_path = os.path.join(home,'History',site,siteName,name,'Ep.txt')
				elif site == "PlayLists" or site == "Music":
						if site == "PlayLists":
							pls = ui.list1.currentItem().text()
						else:
							pls = ui.list1.currentItem().text()
						file_path = os.path.join(home,'Playlists',pls)
				else:
					if os.path.exists(os.path.join(home,'History',site,name,'Ep.txt')):
						file_path = os.path.join(home,'History',site,name,'Ep.txt')
				#ui.replace_lineByIndex(file_path,'','',row)
				if os.path.exists(file_path):
					#f = open(file_path,'r')
					#lines = f.readlines()
					#f.close()
					lines = open_files(file_path,True)
					length = len(lines)
					if nRow == length - 1:
						t = lines[row].replace('\n','')
						lines[row]=lines[nRow].replace('\n','')+'\n'
						lines[nRow]=t
					else:
						t = lines[row]
						lines[row]=lines[nRow]
						lines[nRow]=t
					epnArrList[:]=[]
					#f = open(file_path,'w')
					for i in lines:
						#f.write(i)
						j = i.strip()
						epnArrList.append(j)
					#f.close()
					write_files(file_path,lines,line_by_line=True)
					ui.update_list2()
					self.setCurrentRow(nRow)
					#ui.update_list2()
					#if site != "PlayLists":
					#	ui.update_list2()
					#else:
					#	self.clear()
					#	for i in lines:
					#		i = i.replace('\n','')
					#		if i:
					#			if '	' in i:
					#				i = i.split('	')[0]
					#			self.addItem(i)
					#	self.setCurrentRow(nRow)
			elif site=="Video":
				r = self.currentRow()
				item = self.item(r)
				if item:
					if bookmark == "False":
						video_db = os.path.join(home,'VideoDB','Video.db')
						conn = sqlite3.connect(video_db)
						cur = conn.cursor()
						txt = epnArrList[r].split('	')[1]
						cur.execute('Select EPN FROM Video Where Path="'+txt+'"')
						rows = cur.fetchall()
						num1 = int(rows[0][0])
						print (num1,'--num1')
						print (self.count()-1,'--cnt-1')
						if r < len(epnArrList) - 1:
							txt1 = epnArrList[r+1].split('	')[1]
							epnArrList[r],epnArrList[r+1]=epnArrList[r+1],epnArrList[r]
						else:
							txt1 = epnArrList[0].split('	')[1]
							epnArrList[r],epnArrList[0]=epnArrList[0],epnArrList[r]
						cur.execute('Select EPN FROM Video Where Path="'+txt1+'"')
						rows = cur.fetchall()
						num2 = int(rows[0][0])
						print (num2,'---num2')
						qr = 'Update Video Set EPN=? Where Path=?'
						cur.execute(qr,(num2,txt))
						qr = 'Update Video Set EPN=? Where Path=?'
						cur.execute(qr,(num1,txt1))
						
						conn.commit()
						conn.close()
						self.takeItem(r)
						del item
						if r< len(epnArrList) - 1:
							print ('--here--')
							self.insertItem(r+1,epnArrList[r+1].split('	')[0])
							row_n = r+1
						else:
							
							self.insertItem(0,epnArrList[0].split('	')[0])
							row_n = 0
						self.setCurrentRow(row_n)
	
		elif event.key() == QtCore.Qt.Key_Left:
			if ui.float_window.isHidden():
				if ui.list1.isHidden():
					ui.list1.show()
					#ui.frame.show()
				ui.list1.setFocus()
			else:
				prev_r = self.currentRow() - 1
				if self.currentRow() == 0:
					self.setCurrentRow(0)
				else:
					self.setCurrentRow(prev_r)
			
		elif event.key() == QtCore.Qt.Key_Right:
			if ui.float_window.isHidden():
				curR = self.currentRow()
				queueNo = queueNo + 1
				mpvAlive = 0
				ui.epnfound()
				if ui.list1.isHidden():
					ui.list1.show()
					if not ui.goto_epn.isHidden():
						ui.frame.show()
				self.setFocus()
			else:
				nextr = self.currentRow() + 1
				if nextr == self.count():
					self.setCurrentRow(self.count()-1)
				else:
					self.setCurrentRow(nextr)
		elif event.key() == QtCore.Qt.Key_O:
			self.init_offline_mode()
		elif event.key() == QtCore.Qt.Key_2: 
			mirrorNo = 2
			msg = "Mirror No. 2 Selected"
			#subprocess.Popen(["notify-send",msg]) 
			send_notification(msg)
		elif event.key() == QtCore.Qt.Key_4: 
			mirrorNo = 4
			msg = "Mirror No. 4 Selected"
			#subprocess.Popen(["notify-send",msg])
			send_notification(msg)
		elif event.key() == QtCore.Qt.Key_5: 
			mirrorNo = 5
			msg = "Mirror No. 5 Selected"
			#subprocess.Popen(["notify-send",msg])
			send_notification(msg)
		elif event.key() == QtCore.Qt.Key_3: 
			mirrorNo = 3
			msg = "Mirror No. 3 Selected"
			#subprocess.Popen(["notify-send",msg]) 
			send_notification(msg)
		elif event.key() == QtCore.Qt.Key_1: 
			mirrorNo = 1
			msg = "Mirror No. 1 Selected"
			#subprocess.Popen(["notify-send",msg]) 
			send_notification(msg)
		elif event.key() == QtCore.Qt.Key_6: 
			mirrorNo = 6
			msg = "Mirror No. 6 Selected"
			#subprocess.Popen(["notify-send",msg]) 
			send_notification(msg)
		elif event.key() == QtCore.Qt.Key_7: 
			mirrorNo = 7
			msg = "Mirror No. 7 Selected"
			#subprocess.Popen(["notify-send",msg]) 
			send_notification(msg)
		elif event.key() == QtCore.Qt.Key_8: 
			mirrorNo = 8
			msg = "Mirror No. 8 Selected"
			#subprocess.Popen(["notify-send",msg]) 
			send_notification(msg)
		elif event.key() == QtCore.Qt.Key_9: 
			mirrorNo = 9
			msg = "Mirror No. 9 Selected"
			#subprocess.Popen(["notify-send",msg]) 
			send_notification(msg)
		elif event.key() == QtCore.Qt.Key_H: 
			quality = "hd"
			msg = "Video Quality Set to 720P HD"
			subprocess.Popen(["notify-send",msg])
		elif event.key() == QtCore.Qt.Key_B: 
			quality = "sd480p"
			msg = "Video Quality Set to 480P SD"
			#subprocess.Popen(["notify-send",msg])
			send_notification(msg)
		elif event.key() == QtCore.Qt.Key_S:
			msg = "Video Quality Set to SD"
			#subprocess.Popen(["notify-send",msg]) 
			send_notification(msg)
			quality = "sd"
		elif event.key() == QtCore.Qt.Key_F:
			#mpvplayer.write('\n'+'add sub-pos +1'+'\n')
		
			#fullscr = 1 - fullscr
			if not MainWindow.isFullScreen():
				ui.gridLayout.setSpacing(0)
				ui.superGridLayout.setSpacing(0)
				ui.gridLayout.setContentsMargins(0,0,0,0)
				ui.superGridLayout.setContentsMargins(0,0,0,0)
				#ui.frame1.setMaximumHeight(20)
				ui.text.hide()
				ui.label.hide()
				#if site != "Music":
				ui.frame1.hide()
				ui.tab_6.hide()
				ui.goto_epn.hide()
				ui.btn20.hide()
				if wget:
					if wget.processId() > 0:
						ui.progress.hide()
				ui.list2.hide()
				ui.list6.hide()
				ui.list1.hide()
				ui.frame.hide()
				#ui.text.hide()
				#ui.label.hide()
				#ui.tab_5.setParent(None)
				
				#ui.tab_5.showMaximized()
				ui.tab_5.show()
				ui.tab_5.setFocus()
				#ui.tab_5.showFullScreen()
				
				#ui.gridLayout.showFullScreen()
				if (Player == "mplayer" or Player=="mpv"):
					MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
				MainWindow.showFullScreen()
				
			else:
				
				ui.gridLayout.setSpacing(10)
				ui.superGridLayout.setSpacing(10)
				#ui.gridLayout.setContentsMargins(10,10,10,10)
				ui.superGridLayout.setContentsMargins(10,10,10,10)
				ui.list2.show()
				#ui.goto_epn.show()
				ui.btn20.show()
				#if Player == "mpv":
				if wget:
					if wget.processId() > 0:
						ui.goto_epn.hide()
						ui.progress.show()
					
				ui.frame1.show()
				if Player == "mplayer" or Player=="mpv":
					MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
				MainWindow.showNormal()
				MainWindow.showMaximized()
				if total_till != 0:
					ui.tab_6.show()
					ui.list2.hide()
					ui.goto_epn.hide()
				#ui.tab_5.showNormal()
	
	def find_info(self,var):
			global wget,queueNo,mpvAlive,mpv,downloadVideo,quality,mirrorNo,startPlayer,getSize,finalUrl,site,hdr,rfr_url,curR,base_url,new_epn,site,siteName,finalUrlFound
			global quitReally,epnArrList,name,hdr,opt,pre_opt,home
			nam = re.sub('Dub|Sub|subbed|dubbed','',name)
			nam = re.sub('-|_|[ ]','+',nam)
			nam1 = nam
			print (nam)
			index = ""
			if not self.downloadWget:
				self.downloadWget[:] = []
				self.downloadWget_cnt = 0
			else:
				running = False
				len_down = len(self.downloadWget)
				for i in range(len_down):
					if self.downloadWget[i].isRunning():
						running = True
						break
				if not running:
					self.downloadWget[:] = []
					self.downloadWget_cnt = 0
				else:
					print('--Thread Already Running--')
					return 0
			#if option != "FindAll":
			if var == 1 or var == 3:
				scode = subprocess.check_output(["zenity","--entry","--text","Enter Anime Name Manually"])
				nam = re.sub("\n","",scode)
				nam = re.sub("[ ]","+",nam)
				nam1 = nam
				
				if "g:" in nam:
						arr = nam.split(':')
						if len(arr)==2:
							index=""
							na=arr[1]
						else:
							index=arr[1]
							na=arr[2]
						link = "https://www.google.co.in/search?q="+na+"+site:thetvdb.com"
						print (link)
				elif ':' in nam:
					index = nam.split(':')[0]
					nam = nam.split(':')[1]
					
			if 'g:' not in nam1:
				link = "http://thetvdb.com/index.php?seriesname="+nam+"&fieldlocation=1&language=7&genre=Animation&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch"
				print (link)
				content = ccurl(link)
				m = re.findall('/index.php[^"]tab=[^"]*',content)
				if not m:
					link = "http://thetvdb.com/index.php?seriesname="+nam+"&fieldlocation=2&language=7&genre=Animation&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch"
					content = ccurl(link)
					m = re.findall('/index.php[^"]tab=[^"]*',content)
					if not m:
						link = "http://thetvdb.com/?string="+nam+"&searchseriesid=&tab=listseries&function=Search"
						content = ccurl(link)
						m = re.findall('/[^"]tab=series[^"]*lid=7',content)
			else:
				content = ccurl(link)
				m = re.findall('http://thetvdb.com/[^"]tab=series[^"]*',content)
				print (m)
				if m:
					m[0] = m[0].replace('http://thetvdb.com','')
			if m:
				n = re.sub('amp;','',m[0])
				elist = re.sub('tab=series','tab=seasonall',n)
				url ="http://thetvdb.com" + n
				elist_url = "http://thetvdb.com" + elist
				content = ccurl(elist_url)
				soup = BeautifulSoup(content,'lxml')
				link = soup.find('div',{'class':'section'})
				link1 = link.findAll('a')
				link2 = link.findAll('img')
				imgArr_length = len(link2)
				if link2:
					img_exists = "True"
				else:
					img_exists = "False"
				length = len(link1)
				k = 0
				ep_txt = os.path.join(TMPDIR,name+'-Ep.txt')
				f =open(ep_txt,'w')
				file_start = "False"
				while k < length:
					#print link1[k].text+"	"+link1[k+1].text+"	"+(link1[k])['href']
					t = (link1[k])['href']
					m = re.findall('seriesid=[^&]*',t)
					s_id = re.sub('seriesid=','',m[0])
					m = re.findall('&id=[^&]*',t)
					img_id = re.sub('&id=','',m[0])
					img_url = "http://thetvdb.com" + "/banners/episodes/"+s_id+"/"+img_id+".jpg"
					r1 = str((link1[k].text).replace(' ',''))
					#print r1
					r2 = str((link1[k+1].text).replace(' ','-'))
					
					#if r1 in '[1-9]x[1-9][^"]*':
					#print r1
					if not index:
						n = re.findall('[1-9]x[1-9][0-9]*',r1)
					else:
						if index == "special":
							n = re.findall('Special[^"]*',r1)
						else:
							n = re.findall(index+'x[1-9][0-9]*',r1)
					if n:
						r=(str(r1)+"-"+str(r2)+"	"+img_url)
						print (r)
						if k == 0 or file_start == "False":
							f.write(str(r))
							file_start = "True"
						else:
							f.write('\n'+str(r))
					k = k + 2
				f.close()
				ep_txt = os.path.join(TMPDIR,name+'-Ep.txt')
				f = open(ep_txt,'r')
				lines = f.readlines()
				f.close()
				thumbArr = []
				nameArr= []
				nameArr[:]=[]
				for i in lines:
					j = i.split('	')
					thumbArr.append(j[-1])
					if '/' in j[0]:
						j[0] = j[0].replace('/','-')
					nameArr.append(j[0])
				
				file_path = ""
				if opt == "History":
					if site == "SubbedAnime" or site == "DubbedAnime":
						if os.path.exists(os.path.join(home,'History',site,siteName,name,'Ep.txt')):
							file_path = os.path.join(home,'History',site,siteName,name,'Ep.txt')
						
					else:
						if os.path.exists(os.path.join(home,'History',site,name,'Ep.txt')):
							file_path = os.path.join(home,'History',site,name,'Ep.txt')
					if not index:	
						f = open(file_path,'r')
						lines = f.readlines()
						f.close()
						linesEp = []
						linesEp[:]=[]
						for i in lines:
							i = i.replace('\n','')
							if '	' in i:
								j = i.split('	')[1]
								if '#' in i:
									i = '#'+j
								else:
									i = j
							linesEp.append(i)
						f = open(file_path,'w')
						j = 0
						length = len(linesEp)
						print (linesEp)
						print (nameArr)
						epnArrList[:]=[]
						while j < length:
							if j < len(nameArr):
								k = nameArr[j]+'	'+linesEp[j]
							else:
								k = linesEp[j]
							if '#' in k:
								k = k.replace('#','')
								k = "#"+k
							epnArrList.append(k)
							if j == 0:
								f.write(k)
							else:
								f.write('\n'+k)
							j = j+1
						f.close()
					else:
						f = open(file_path,'r')
						lines = f.readlines()
						f.close()
						linesEp = []
						linesEp[:]=[]
						row = ui.list2.currentRow()
						
						r = 0
						for i in lines:
							i = i.replace('\n','')
							if r >= row:
								
								if '	' in i:
									j = i.split('	')[1]
									if '#' in i:
										i = '#'+j
									else:
										i = j
							linesEp.append(i)
							r = r+1
							
						f = open(file_path,'w')
						
						length = len(linesEp)
						print (linesEp)
						print (nameArr)
						r = 0
						j = 0
						epnArrList[:]=[]
						while r < length:
							k = linesEp[r]
							if (r >= row) and (r < (row+len(nameArr))):
								if j < len(nameArr):
									k = nameArr[j]+'	'+linesEp[r]
								else:
									k = linesEp[j]
								j = j+1
							if '#' in k:
								k = k.replace('#','')
								k = "#"+k
							epnArrList.append(k)
							if r == 0:
								f.write(k)
							else:
								f.write('\n'+k)
							
							r = r+1
						f.close()	
					
				if var !=2 and var !=3:
					if not index:
						r = 0
						img_l = imgArr_length
					else:
						r = ui.list2.currentRow()
						img_l = r + len(thumbArr)
					j = 0
					for i in thumbArr:
						if (site != "Local" and site != "Video" and site != "PlayLists" and img_exists == "True" and r < img_l and r < len(epnArrList)):
							if finalUrlFound == True:
								if '	' in epnArrList[r]:
									newEpn = epnArrList[r].split('	')[0]
								else:
									#newEpn = (epnArrList[r]).split('/')[-1]
									newEpn = os.path.basename(epnArrList[r])
							else:
								if '	' in epnArrList[r]:
									newEpn = epnArrList[r].split('	')[0]
								else:
									newEpn = name+'-'+(epnArrList[r])
							newEpn = str(newEpn)
							newEpn = newEpn.replace('#','')
							if newEpn.startswith(ui.check_symbol):
								newEpn = newEpn[1:]
							dest = os.path.join(home,'thumbnails',name,newEpn+'.jpg')
							img_url= i.replace('\n','')
							#command = "wget --user-agent="+'"'+hdr+'" '+'"'+img_url+'"'+" -O "+dest
							#ua = "--user-agent="+'"'+hdr+'"'
							#subprocess.Popen(["wget",ua,img_url,"-O",dest])
							self.downloadWget.append(downloadThread(img_url+'#'+'-o'+'#'+dest))
							self.downloadWget[len(self.downloadWget)-1].finished.connect(self.download_thread_finished)
						r = r+1
				ui.update_list2()
				
			if self.downloadWget:
				length = len(self.downloadWget)
				for i in range(5):
					if i < length:
						#self.infoWget(self.downloadWget[i],i)
						self.downloadWget[i].start()
	def download_thread_finished(self):
		print ("Process Ended")
		self.downloadWget_cnt = self.downloadWget_cnt+1
		if self.downloadWget_cnt == 5:
			self.downloadWget = self.downloadWget[5:]
			length = len(self.downloadWget)
			self.downloadWget_cnt = 0
			for i in range(5):
				if i < length:
					self.downloadWget[i].start()
					
	def triggerPlaylist(self,value):
		global epn,epn_name_in_list,path_final_Url,home,site,pre_opt,base_url,embed,name,epnArrList,opt,finalUrlFound,refererNeeded
		print ('Menu Clicked')
		print (value)
		file_path = os.path.join(home,'Playlists',str(value))
		print(file_path)
		if site == "Music" or site == "Video" or site == "Local" or site == "None" or site == 'PlayLists':
			#print (epnArrList)
			if os.path.exists(file_path):
				i = self.currentRow()
				#f = open(file_path,'a')
				
				sumr=epnArrList[i].split('	')[0]
				
				try:
					rfr_url=epnArrList[i].split('	')[2]
				except:
					rfr_url = "NONE"
				
				sumry = epnArrList[i].split('	')[1]
				sumry = sumry.replace('"','')
				sumry = '"'+sumry+'"'
				t = sumr+'	'+sumry+'	'+rfr_url
				"""
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
				"""
				write_files(file_path,t,line_by_line=True)
		else:
			finalUrl = ui.epn_return(self.currentRow())
			t = ''
			#sumr=str(ui.epn_name_in_list)
			sumr = self.item(self.currentRow()).text().replace('#','')
			sumr = sumr.replace(ui.check_symbol,'')
			if os.path.exists(file_path):
				#f = open(file_path,'a')
				if type(finalUrl) is list:
					if finalUrlFound == True and refererNeeded == True:
						rfr_url = finalUrl[1]
						sumry = str(finalUrl[0])
						#sumry = sumry.replace('"','')
						#f.write(sumr+'	'+sumry+'	'+rfr_url+'\n')
						t = sumr+'	'+sumry+'	'+rfr_url
					else:
						rfr_url = "NONE"
						j = 1
						t = ''
						for i in path_final_Url:
							p = "-Part-"+str(j)
							sumry = str(i)
							#f.write(sumr+p+'	'+sumry+'	'+rfr_url+'\n')
							if j == 1:
								t = sumr+p+'	'+sumry+'	'+rfr_url
							else:
								t = t + '\n' + sumr+p+'	'+sumry+'	'+rfr_url
							j = j+1
				else:
					rfr_url = "NONE"
					
					sumry = str(finalUrl)
					#sumry = sumry.replace('"','')
					#f.write(sumr+'	'+sumry+'	'+rfr_url+'\n')
					t = sumr+'	'+sumry+'	'+rfr_url
				"""
				if os.stat(file_path).st_size == 0:
					f = open(file_path,'w')
				else:
					f = open(file_path,'a')
					t = '\n'+t
				try:
					f.write(str(t))
				except:
					f.write(t.encode('utf-8'))
				f.close()
				"""
				write_files(file_path,t,line_by_line=True)
		
		
	def fix_order(self):
		global epnArrList,opt,site,home
		row = self.currentRow()
		item = self.item(row)
		if item:
			#print(epnArrList)
			if site == "Video":
				if bookmark == "False":
					video_db = os.path.join(home,'VideoDB','Video.db')
					conn = sqlite3.connect(video_db)
					cur = conn.cursor()
					
					for num in range(len(epnArrList)):
						txt = epnArrList[num].split('	')[1]
						qr = 'Update Video Set EPN=? Where Path=?'
						cur.execute(qr,(num,txt))
					
					conn.commit()
					conn.close()
			elif site == "Music" and ui.list3.currentItem():
					go_next = True
					if ui.list3.currentItem().text() == "Playlist":
						go_next = True
					else:
						go_next = False
					if go_next:
						pls = ''
						file_path = ''
						if ui.list1.currentItem():
							pls = ui.list1.currentItem().text()
						if pls:
							file_path = os.path.join(home,'Playlists',pls)
						if os.path.exists(file_path):
							"""
							#abs_path='/tmp/AnimeWatch/tmp.txt'
							abs_path = os.path.join(TMPDIR,'tmp.txt')
							print(file_path,'--file-path--')
							writing_failed = False
							if os.path.exists(file_path):
								f = open(abs_path,'w')
								for i in range(len(epnArrList)):
									j = epnArrList[i].replace('\n','')
									if i == len(epnArrList)-1:
										j = j
									else:
										j = (j+'\n')
									print (j,'---order---')
									f.write(j)
									
									
								f.close()
								if not writing_failed:
									move(abs_path, file_path)
							"""
							write_files(file_path,epnArrList,line_by_line=True)
			elif (opt == "History" or site =="PlayLists") and row > 0 and site!="Video":
					file_path = ""
					
					if site == "PlayLists":
							if ui.list1.currentItem():
								pls = ui.list1.currentItem().text()
								file_path = os.path.join(home,'Playlists',pls)
					elif site == "Local":
						if os.path.exists(os.path.join(home,'History',site,name,'Ep.txt')):
							file_path = os.path.join(home,'History',site,name,'Ep.txt')
					#ui.replace_lineByIndex(file_path,'','',row)
					if os.path.exists(file_path):
						#abs_path='/tmp/AnimeWatch/tmp.txt'
						abs_path = os.path.join(TMPDIR,'tmp.txt')
						print(file_path,'--file-path--')
						writing_failed = False
						if os.path.exists(file_path):
							"""
							f = open(abs_path,'w')
							for i in range(len(epnArrList)):
								j = epnArrList[i].replace('\n','')
								if i == len(epnArrList)-1:
									j = j
								else:
									j = (j+'\n')
								print (j,'---order---')
								f.write(j)
								
								
							f.close()
							if not writing_failed:
								move(abs_path, file_path)
							"""
							write_files(file_path,epnArrList,line_by_line=True)
			
						
	def contextMenuEvent(self, event):
		global wget,queueNo,mpvAlive,mpv,downloadVideo,quality,mirrorNo,startPlayer,getSize,finalUrl,site,hdr,rfr_url,curR,base_url,new_epn,site,home,opt,finalUrlFound,epnArrList
		global quitReally,epnArrList,name,hdr,ui
		#print name
		if site == "Music":
			menu = QtWidgets.QMenu(self)
			submenuR = QtWidgets.QMenu(menu)
			submenuR.setTitle("Add To Playlist")
			menu.addMenu(submenuR)
			
			view_menu = QtWidgets.QMenu(menu)
			view_menu.setTitle("View Mode")
			menu.addMenu(view_menu)
			
			view_list = view_menu.addAction("List Mode (Default)")
			view_list_thumbnail = view_menu.addAction("List With Thumbnail")
			thumb = view_menu.addAction("Thumbnail Mode")
			#thumb = menu.addAction("Show Thumbnails")
			go_to = menu.addAction("Go To Last.fm")
			fix_ord = menu.addAction("Lock Order (Playlist Only)")
			pls = os.listdir(os.path.join(home,'Playlists'))
			home_n = os.path.join(home,'Playlists')
			pls = sorted(pls,key = lambda x:os.path.getmtime(os.path.join(home_n,x)),reverse=True)
			j = 0
			item_m = []
			for i in pls:
				item_m.append(submenuR.addAction(i))
			
			submenuR.addSeparator()
			new_pls = submenuR.addAction("Create New Playlist")
			default = menu.addAction("Set Default Background")
			delPosters = menu.addAction("Delete Poster")
			delInfo = menu.addAction("Delete Info")
			action = menu.exec_(self.mapToGlobal(event.pos()))
			for i in range(len(item_m)):
				if action == item_m[i]:
					self.triggerPlaylist(pls[i])
			if action == new_pls:
				print ("creating")
				item, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Input Dialog', 'Enter Playlist Name')
				if ok and item:
					file_path = os.path.join(home,'Playlists',item)
					if not os.path.exists(file_path):
						f = open(file_path,'w')
						f.close()
			elif action == view_list:
				ui.list2.setStyleSheet("""QListWidget{font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;}
				QListWidget:item {height: 30px;}
				QListWidget:item:selected:active {background:rgba(0,0,0,20%);color: violet;}
				QListWidget:item:selected:inactive {border:rgba(0,0,0,30%);}
				QMenu{font: bold 12px;color:black;background-image:url('1.png');}""")
				ui.list_with_thumbnail = False
				ui.update_list2()
			elif action == view_list_thumbnail:
				ui.list2.setStyleSheet("""QListWidget{font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;}
				QListWidget:item {height: 64px;}
				QListWidget:item:selected:active {background:rgba(0,0,0,20%);color: violet;}
				QListWidget:item:selected:inactive {border:rgba(0,0,0,30%);}
				QMenu{font: bold 12px;color:black;background-image:url('1.png');}""")
				ui.list_with_thumbnail = True
				ui.update_list2()
			elif action == thumb:
				ui.IconViewEpn()
				ui.scrollArea1.setFocus()
			
			elif action == go_to:
					if ui.list3.currentItem():
						nam1 = ''
						if str(ui.list3.currentItem().text())=="Artist":
							nam1 = str(ui.list1.currentItem().text())
						else:
							r = self.currentRow()
							try:
								nam1 = epnArrList[r].split('	')[2]
							except:
								nam1 = ''
						print (nam1)
						ui.reviewsWeb(srch_txt=nam1,review_site='last.fm',action='search_by_name')
			elif action == fix_ord:
				self.fix_order()
			elif action == delInfo or action == delPosters or action == default:
					if (ui.list3.currentItem()):
						if str(ui.list3.currentItem().text()) == "Artist":
							if '/' in name:
								nam = name.replace('/','-')
							else:
								nam = name
							 	
						else:
								try:
									r = ui.list2.currentRow()
								
									nam = epnArrList[r].split('	')[2]
								except:
									nam = ""
									
								if '/' in nam:
									nam = nam.replace('/','-')
								else:
									nam = nam
						
						if nam:
							picn = os.path.join(home,'Music','Artist',nam,'poster.jpg')
							fanart = os.path.join(home,'Music','Artist',nam,'fanart.jpg')
							default_wall = os.path.join(home,'default.jpg')
							sumr = os.path.join(home,'Music','Artist',nam,'bio.txt')
							dir_n = os.path.join(home,'Music','Artist',nam)
							if os.path.exists(dir_n):
								if action == delInfo:
									m=os.listdir(dir_n)
									for i in m:
										if i.endswith('.txt'):
											f = open(os.path.join(dir_n,'bio.txt'),'w')
											f.write('No Information Available')
											f.close()
									m = os.listdir(TMPDIR)
									for i in m:
										if i.endswith('.jpg') or i.endswith('.txt'):
											t = os.path.join(TMPDIR,i)
											os.remove(t)
								elif action == delPosters:
									m=os.listdir(dir_n)
									for i in m:
										if i.endswith('.jpg'):
											os.remove(os.path.join(dir_n,i))
									m = os.listdir(TMPDIR)
									for i in m:
										if i.endswith('.jpg') or i.endswith('.txt'):
											os.remove(os.path.join(TMPDIR,i)) 
								elif action == default:
									shutil.copy(default_wall,picn)
									shutil.copy(default_wall,fanart)
									ui.videoImage(picn,os.path.join(home,'Music','Artist',nam,'thumbnail.jpg'),fanart,'')
		else:
			menu = QtWidgets.QMenu(self)
			submenuR = QtWidgets.QMenu(menu)
			submenuR.setTitle("Add To Playlist")
			menu.addMenu(submenuR)
			
			view_menu = QtWidgets.QMenu(menu)
			view_menu.setTitle("View Mode")
			menu.addMenu(view_menu)
			
			view_list = view_menu.addAction("List Mode (Default)")
			view_list_thumbnail = view_menu.addAction("List With Thumbnail")
			thumb = view_menu.addAction("Thumbnail Mode")
			
			pls = os.listdir(os.path.join(home,'Playlists'))
			home_n = os.path.join(home,'Playlists')
			pls = sorted(pls,key = lambda x:os.path.getmtime(os.path.join(home_n,x)),reverse=True)
			item_m = []
			for i in pls:
				item_m.append(submenuR.addAction(i))
				
				
			submenuR.addSeparator()
			new_pls = submenuR.addAction("Create New Playlist")
			r = self.currentRow()
			
			
			#thumb = menu.addAction("Show Thumbnails")
			goto_web_mode = False
			offline_mode = False
			if epnArrList and self.currentItem():
				epn_arr = epnArrList[r].split('	')
				if len(epn_arr) > 2:
					url_web = epnArrList[r].split('	')[1]
				else:
					url_web = 'none'
			else:
				url_web = 'none'
				
			if 'youtube.com' in url_web:
				goto_web = menu.addAction('Open in Youtube Browser')
				goto_web_mode = True
			
			if site.lower() != 'video' and site.lower() != 'music' and site.lower() != 'local':
				if ui.btn1.currentText().lower() =='addons' or url_web.startswith('http') or url_web.startswith('"http'):
					start_offline = menu.addAction('Start In Offline Mode')
					offline_mode = True
					
			fix_ord = menu.addAction("Lock Order")
			
			submenu = QtWidgets.QMenu(menu)
			
			eplist = menu.addAction("Get Episode Thumbnails(TVDB)")
			eplistM = menu.addAction("Go To TVDB")
			#epl = menu.addAction("Get Episode Info(TVDB)")
			#epl_m = menu.addAction("Get Episode Info Manually(TVDB)")
			#default_name = menu.addAction("Default Name")
			editN = menu.addAction("Edit Name")
			remove = menu.addAction("Remove Thumbnails")
			
			
			action = menu.exec_(self.mapToGlobal(event.pos()))
			
			if self.currentItem():
				for i in range(len(item_m)):
					if action == item_m[i]:
						self.triggerPlaylist(pls[i])
			
			if offline_mode:
				if action == start_offline:
					self.init_offline_mode()
			if goto_web_mode:
				if action == goto_web:
					ui.goto_web_directly(url_web)
					#txt = action.text()
					#if txt.lower() == 'open in youtube browser':
					
			
			if action == new_pls:
				print ("creating")
				item, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Input Dialog', 'Enter Playlist Name')
				if ok and item:
					file_path = home+'/Playlists/'+item
					if not os.path.exists(file_path):
						f = open(file_path,'w')
						f.close()
			elif action == view_list:
				ui.list2.setStyleSheet("""QListWidget{font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;}
				QListWidget:item {height: 30px;}
				QListWidget:item:selected:active {background:rgba(0,0,0,20%);color: violet;}
				QListWidget:item:selected:inactive {border:rgba(0,0,0,30%);}
				QMenu{font: bold 12px;color:black;background-image:url('1.png');}""")
				ui.list_with_thumbnail = False
				ui.update_list2()
			elif action == view_list_thumbnail:
				ui.list2.setStyleSheet("""QListWidget{font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;}
				QListWidget:item {height: 112px;}
				QListWidget:item:selected:active {background:rgba(0,0,0,20%);color: violet;}
				QListWidget:item:selected:inactive {border:rgba(0,0,0,30%);}
				QMenu{font: bold 12px;color:black;background-image:url('1.png');}""")
				ui.list_with_thumbnail = True
				ui.update_list2()
			elif action == remove:
				r = 0
				for i in epnArrList:
					if '	' in i:
						newEpn = (epnArrList[r]).split('	')[0]
						
					else:
						newEpn = name+'-'+(epnArrList[r])
					newEpn = newEpn.replace('#','')
					if newEpn.startswith(ui.check_symbol):
						newEpn = newEpn[1:]
					if ui.list1.currentItem():
						nm = (ui.list1.currentItem().text())
						dest = os.path.join(home,"thumbnails",nm,newEpn+'.jpg')
						dest = ui.get_thumbnail_image_path(r,newEpn)
						#print(dest)
						if os.path.exists(dest):
							#print('removing')
							os.remove(dest)
							small_nm_1,new_title = os.path.split(dest)
							small_nm_2 = '128px.'+new_title
							new_small_thumb = os.path.join(small_nm_1,small_nm_2)
							print(new_small_thumb)
							if os.path.exists(new_small_thumb):
								os.remove(new_small_thumb)
					r = r+1
			elif action == editN and not ui.list1.isHidden():
				row = self.currentRow()
				default_text = epnArrList[row].split('	')[0]
				item, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Input Dialog', 'Enter Episode Name Manually',QtWidgets.QLineEdit.Normal,default_text)
				if ok and item:
					
					nm = item
					row = self.currentRow()
					t = epnArrList[row]
					print(nm,row,t)
					if '	' in t and '	' not in nm and site!= "Video" and site!="None" and site!= 'PlayLists':
						r = t.split('	')[1]
						epnArrList[row]=nm + '	'+r
						ui.mark_History()
					elif site == 'PlayLists':
						tmp = epnArrList[row]
						tmp = re.sub('[^	]*',nm,tmp,1)
						epnArrList[row] = tmp
						if ui.list1.currentItem():
							pls_n = os.path.join(home,'Playlists',ui.list1.currentItem().text())
							ui.update_playlist_original(pls_n)
							self.setCurrentRow(row)
			
			elif action == eplistM:
				if ui.list1.currentItem():
					name1 = (ui.list1.currentItem().text())
					#ui.reviewsMusic("TVDB:"+name1)
					ui.reviewsWeb(srch_txt=name1,review_site='tvdb',action='search_by_name')
			elif action == eplist:
				if self.currentItem():
					self.find_info(0)
			elif action == thumb:
				if self.currentItem():
					ui.IconViewEpn()
					ui.scrollArea1.setFocus()
			elif action == fix_ord:
				if self.currentItem():
					self.fix_order()
			
			
			#super(List2, self).keyPressEvent(event)

class List3(QtWidgets.QListWidget):
	def __init__(self, parent):
		super(List3, self).__init__(parent)

	def keyPressEvent(self, event):
		global category,home,site,bookmark
		if event.key() == QtCore.Qt.Key_O:
			ui.setPreOpt()
		elif event.key() == QtCore.Qt.Key_Down:
			nextr = self.currentRow() + 1
			if nextr == self.count():
				self.setCurrentRow(0)
				#ui.btnOpt.setCurrentIndex(1)
			else:
				self.setCurrentRow(nextr)
				#ui.btnOpt.setCurrentIndex(nextr+1)
		elif event.key() == QtCore.Qt.Key_Up:
			prev_r = self.currentRow() - 1
			if self.currentRow() == 0:
				self.setCurrentRow(self.count()-1)
				#ui.btnOpt.setCurrentIndex(self.count())
			else:
				self.setCurrentRow(prev_r)
				#ui.btnOpt.setCurrentIndex(prev_r+1)
		#elif event.key() == QtCore.Qt.Key_L:
		#ui.setPreOptList()
		elif event.key() == QtCore.Qt.Key_Right:
			if not ui.list1.isHidden():
				ui.list1.setFocus()
			elif not ui.scrollArea.isHidden():
				ui.scrollArea.setFocus()
			elif not ui.scrollArea1.isHidden():
				ui.scrollArea1.setFocus()
			
			ui.dockWidget_3.hide()
			#ui.label.setMinimumSize(350,400)
		elif event.key() == QtCore.Qt.Key_Return:
			ui.options('clicked')
		elif event.key() == QtCore.Qt.Key_Left:
			ui.btn1.setFocus()
		elif event.key() == QtCore.Qt.Key_H:
			ui.setPreOpt()
		elif event.key() == QtCore.Qt.Key_Delete:
			if site == "PlayLists":
				index = self.currentRow()
				item_r  = self.item(index)
				if item_r:
					item = str(self.currentItem().text())
					if item != "Default":
						file_pls = os.path.join(home,'Playlists',item)
						if os.path.exists(file_pls):
							os.remove(file_pls)
						self.takeItem(index)
						del item_r
						ui.list2.clear()
			if bookmark == "True":
				index = self.currentRow()
				item_r  = self.item(index)
				if item_r:
					item = str(self.currentItem().text())
					bookmark_array = ['All','Watching','Completed','Incomplete','Later','Interesting','Music-Videos']
					if item not in bookmark_array:
						file_pls = os.path.join(home,'Bookmark',item+'.txt')
						if os.path.exists(file_pls):
							os.remove(file_pls)
						self.takeItem(index)
						del item_r
						ui.list1.clear()
						ui.list2.clear()
						
	def contextMenuEvent(self, event):
		global name,tmp_name,opt,list1_items,curR,nxtImg_cnt,home,site,pre_opt,base_url,category
		
		#print name
		menu = QtWidgets.QMenu(self)
		
		history = menu.addAction("History")
		anime = menu.addAction("Animes")
		movie = menu.addAction("Movies")
		action = menu.exec_(self.mapToGlobal(event.pos()))
		if action == history:
			ui.setPreOpt()
		elif action == anime:
			category = "Animes"
		elif action == movie:
			category = "Movies"
		#super(List2, self).keyPressEvent(event)
		
class List4(QtWidgets.QListWidget):
	def __init__(self, parent):
		super(List4, self).__init__(parent)

	def keyPressEvent(self, event):
		global category,home,site,bookmark
		
		if event.key() == QtCore.Qt.Key_Down:
			nextr = self.currentRow() + 1
			if nextr == self.count():
				#self.setCurrentRow(0)
				ui.go_page.setFocus()
				#ui.btnOpt.setCurrentIndex(1)
			else:
				self.setCurrentRow(nextr)
				#ui.btnOpt.setCurrentIndex(nextr+1)
		elif event.key() == QtCore.Qt.Key_Up:
			prev_r = self.currentRow() - 1
			if self.currentRow() == 0:
				#self.setCurrentRow(self.count()-1)
				ui.go_page.setFocus()
				#ui.btnOpt.setCurrentIndex(self.count())
			else:
				self.setCurrentRow(prev_r)
				#ui.btnOpt.setCurrentIndex(prev_r+1)
		
		elif event.key() == QtCore.Qt.Key_Return:
			ui.search_list4_options()
		#elif event.key() == QtCore.Qt.Key_Left:
		#	ui.btn1.setFocus()
			
	def contextMenuEvent(self, event):
		global name,tmp_name,opt,list1_items,curR,nxtImg_cnt,home,site,pre_opt,base_url,category
		
		#print name
		menu = QtWidgets.QMenu(self)
		
		hd = menu.addAction("Hide Search Table")
		sideBar = menu.addAction("Show Sidebar")
		history = menu.addAction("Show History")
		action = menu.exec_(self.mapToGlobal(event.pos()))
		if action == hd:
			self.hide()
		elif action == sideBar:
			if ui.dockWidget_3.isHidden():
				ui.dockWidget_3.show()
				ui.btn1.setFocus()
			else:
				ui.dockWidget_3.hide()
				ui.list1.setFocus()
		elif action == history:
			ui.setPreOpt()
			
class List5(QtWidgets.QListWidget):
	def __init__(self, parent):
		super(List5, self).__init__(parent)

	def keyPressEvent(self, event):
		global category,home,site,bookmark,epnArrList
		
		if event.key() == QtCore.Qt.Key_Down:
			nextr = self.currentRow() + 1
			if nextr == self.count():
				#self.setCurrentRow(0)
				ui.goto_epn_filter_txt.setFocus()
				#ui.btnOpt.setCurrentIndex(1)
			else:
				self.setCurrentRow(nextr)
				#ui.epn_highlight()
				#ui.btnOpt.setCurrentIndex(nextr+1)
		elif event.key() == QtCore.Qt.Key_Up:
			prev_r = self.currentRow() - 1
			if self.currentRow() == 0:
				#self.setCurrentRow(self.count()-1)
				ui.goto_epn_filter_txt.setFocus()
				#ui.btnOpt.setCurrentIndex(self.count())
			else:
				self.setCurrentRow(prev_r)
				#ui.btnOpt.setCurrentIndex(prev_r+1)
				#ui.epn_highlight()
		elif event.key() == QtCore.Qt.Key_Return:
			ui.search_list5_options()
		elif event.key() == QtCore.Qt.Key_Q:
			if site == "Music" or site == "Video" or site == "Local" or site == "PlayLists" or site == "None":
				file_path = os.path.join(home,'Playlists','Queue')
				if not os.path.exists(file_path):
					f = open(file_path,'w')
					f.close()
					
				if not ui.queue_url_list:
					ui.list6.clear()
				
				
				indx = self.currentRow()
				item = self.item(indx)
				if item:
					tmp = str(self.currentItem().text())
					tmp1 = tmp.split(':')[0]
					r = int(tmp1)
					ui.queue_url_list.append(epnArrList[r])
					ui.list6.addItem(epnArrList[r].split('	')[0])
					print (ui.queue_url_list)
					"""
					if os.stat(file_path).st_size == 0:
						f = open(file_path,'w')
						f.write(epnArrList[r])
					else:
						f = open(file_path,'a')
						f.write('\n'+epnArrList[r])
					f.close()
					"""
					write_files(file_path,epnArrList[r],line_by_line=True)
		#elif event.key() == QtCore.Qt.Key_Left:
		#	ui.btn1.setFocus()
			
class List6(QtWidgets.QListWidget):
	def __init__(self, parent):
		super(List6, self).__init__(parent)

	def keyPressEvent(self, event):
		global category,home,site,bookmark,video_local_stream
		
		if event.key() == QtCore.Qt.Key_Down:
			nextr = self.currentRow() + 1
			if nextr == self.count():
				self.setCurrentRow(0)
			else:
				self.setCurrentRow(nextr)
		elif event.key() == QtCore.Qt.Key_Up:
			prev_r = self.currentRow() - 1
			if self.currentRow() == 0:
				self.setCurrentRow(self.count()-1)
			else:
				self.setCurrentRow(prev_r)
		elif event.key() == QtCore.Qt.Key_PageUp:
			r = self.currentRow()
			if r > 0:
				r1 = r - 1
				ui.queue_url_list[r],ui.queue_url_list[r1] = ui.queue_url_list[r1],ui.queue_url_list[r]
				item = self.item(r)
				txt = item.text()
				self.takeItem(r)
				del item
				self.insertItem(r1,txt)
				self.setCurrentRow(r1)
		elif event.key() == QtCore.Qt.Key_PageDown:
			r = self.currentRow()
			if r < self.count()-1 and r >=0:
				r1 = r + 1
				ui.queue_url_list[r],ui.queue_url_list[r1] = ui.queue_url_list[r1],ui.queue_url_list[r]
				item = self.item(r)
				txt = item.text()
				self.takeItem(r)
				del item
				self.insertItem(r1,txt)
				self.setCurrentRow(r1)
		elif event.key() == QtCore.Qt.Key_Return:
			r = self.currentRow()
			if self.item(r):
				ui.queueList_return_pressed(r)
		elif event.key() == QtCore.Qt.Key_Delete:
			r = self.currentRow()
			if self.item(r):
				item = self.item(r)
				self.takeItem(r)
				del item
				if not video_local_stream:
					del ui.queue_url_list[r]
class QLineCustom(QtWidgets.QLineEdit):
	def __init__(self, parent):
		super(QLineCustom, self).__init__(parent)

	def keyPressEvent(self, event):
		print ("down")
		global category,home,site,bookmark
		
		if (event.key() == QtCore.Qt.Key_Down):
			print ("Down")
			ui.list4.show()
			ui.list4.setFocus()
			self.show()
		elif event.key() == QtCore.Qt.Key_Up:
			ui.list4.show()
			ui.list4.setFocus()
			self.show()
			
		super(QLineCustom, self).keyPressEvent(event)
		
		
			
class QLineCustomEpn(QtWidgets.QLineEdit):
	def __init__(self, parent):
		super(QLineCustomEpn, self).__init__(parent)

	def keyPressEvent(self, event):
		print ("down")
		global category,home,site,bookmark
		
		if (event.type()==QtCore.QEvent.KeyPress) and (event.key() == QtCore.Qt.Key_Down):
			print ("Down")
			ui.list5.setFocus()
		elif event.key() == QtCore.Qt.Key_Up:
			ui.list5.setFocus()
		super(QLineCustomEpn, self).keyPressEvent(event)

class QProgressBarCustom(QtWidgets.QProgressBar):
	def __init__(self, parent,gui):
		super(QProgressBarCustom, self).__init__(parent)
		self.gui = gui
	def mouseReleaseEvent(self, ev):
		global video_local_stream
		if ev.button() == QtCore.Qt.LeftButton:
			print('progressbar clicked')
			if video_local_stream:
				print('hello')
				if self.gui.torrent_frame.isHidden():
					self.gui.torrent_frame.show()
					self.gui.label_torrent_stop.setToolTip('Stop Torrent')
					self.gui.label_down_speed.show()
					self.gui.label_up_speed.show()
					if self.gui.torrent_download_limit == 0:
						down_rate = '\u221E' + ' K'
					else:
						down_rate = str(int(self.gui.torrent_download_limit/1024))+'K'
					if self.gui.torrent_upload_limit == 0:
						up_rate = '\u221E' + ' K'
					else:
						up_rate = str(int(self.gui.torrent_upload_limit/1024))+'K'
					down = '\u2193 RATE: ' +down_rate
					up = '\u2191 RATE:' +up_rate
					self.gui.label_down_speed.setPlaceholderText(down)
					self.gui.label_up_speed.setPlaceholderText(up)
				else:
					self.gui.torrent_frame.hide()
			else:
				if self.gui.torrent_frame.isHidden():
					self.gui.torrent_frame.show()
					self.gui.label_down_speed.hide()
					self.gui.label_up_speed.hide()
					self.gui.label_torrent_stop.setToolTip('Stop Current Download')
				else:
					self.gui.torrent_frame.hide()
					
class QtGuiQWidgetScroll(QtWidgets.QScrollArea):
	def __init__(self, parent):
		super(QtGuiQWidgetScroll, self).__init__(parent)
		#global y_c
		#y_c = 0
	def sizeAdjust(self,nextR,direction):
		global icon_size_arr,iconv_r,site
		ui.list1.setCurrentRow(nextR)
		p1 = "ui.label_"+str(nextR)+".y()"
		try:
			yy=eval(p1)
			
			p1 = "ui.label_"+str(nextR)+".x()"
			xy=eval(p1)
			p1 = "ui.label_"+str(nextR)+".setFocus()"
			exec (p1)
		except:
			return 0
		if icon_size_arr:
			hi = icon_size_arr[1]
			wi = icon_size_arr[0]
			if direction == "down":		
				prevR = nextR - iconv_r
			elif direction == "up":
				prevR = nextR + iconv_r
			elif direction == "forward":
				prevR = nextR - 1
			elif direction == "backward":
				prevR = nextR + 1
			if prevR >= 0 and prevR < ui.list1.count():
				
					
				p1 = "ui.label_"+str(prevR)+".setMinimumSize("+wi+","+hi+")"
				exec (p1)
				p1 = "ui.label_"+str(prevR)+".setMaximumSize("+wi+","+hi+")"
				exec (p1)
				
				#p1 = "hgt=ui.label_"+str(prevR)+".height()"
				#exec p1
				ht1 = (0.6*int(hi))
				wd1 = (0.6*int(wi))
				ht = str(ht1)
				wd = str(wd1)
			elif prevR < 0:
				p1 = "ui.label_"+str(nextR)+".width()"
				wd1=eval(p1)
				p1 = "ui.label_"+str(nextR)+".height()"
				ht1=eval(p1)
				ht = str(0.6*ht1)
				wd = str(0.6*wd1)
				print ("ht="+wd)
				print ("wd="+wd)
			
		else:
			hi = icon_size_arr[1]
			wi = icon_size_arr[0]
			p1 = "ui.label_"+str(nextR)+".width()"
			wd1=eval(p1)
			p1 = "ui.label_"+str(nextR)+".height()"
			ht1=eval(p1)
			
			ht = str(0.6*ht1)
			wd = str(0.6*wd1)
			print ("ht="+wd)
			print ("wd="+wd)
			
		
		
		
		
		ui.scrollArea.verticalScrollBar().setValue(yy-ht1)
		
		ui.scrollArea.horizontalScrollBar().setValue(xy-wd1)
		
		p1 = "ui.label_"+str(nextR)+".setMinimumSize("+wd+","+ht+")"
		exec (p1)
		p1 = "ui.label_"+str(nextR)+".setMaximumSize("+wd+","+ht+")"
		exec (p1)
		
		ui.labelFrame2.setText(ui.list1.currentItem().text())
		
		
	def keyPressEvent(self, event):
		global iconv_r,iconv_r_indicator,total_till,browse_cnt
		
		if event.key() == QtCore.Qt.Key_Equal:
			
			#total_till = 0
			#browse_cnt = 0
			if iconv_r > 1:
				iconv_r = iconv_r-1
				if iconv_r_indicator:
					iconv_r_indicator.pop()
					
				iconv_r_indicator.append(iconv_r)
			if not ui.scrollArea.isHidden():
				ui.next_page('not_deleted')
				#ui.thumbnail_label_update()
			elif not ui.scrollArea1.isHidden():
				#ui.thumbnailEpn()
				ui.thumbnail_label_update()
			if iconv_r > 1:
				w = float((ui.tab_6.width()-60)/iconv_r)
				h = float((9*w)/16)
				width=str(int(w))
				height=str(int(h))
				ui.scrollArea1.verticalScrollBar().setValue((((curR+1)/iconv_r)-1)*h+((curR+1)/iconv_r)*10)
		elif event.key() == QtCore.Qt.Key_Minus:
			
			#total_till = 0
			#browse_cnt = 0
			iconv_r = iconv_r+1
			if iconv_r_indicator:
				iconv_r_indicator.pop()
			iconv_r_indicator.append(iconv_r)
			if not ui.scrollArea.isHidden():
				ui.next_page('not_deleted')
				#ui.thumbnail_label_update()
			elif not ui.scrollArea1.isHidden():
				#ui.thumbnailEpn()
				ui.thumbnail_label_update()
			if iconv_r > 1:
				w = float((ui.tab_6.width()-60)/iconv_r)
				h = float((9*w)/16)
				width=str(int(w))
				height=str(int(h))
				ui.scrollArea1.verticalScrollBar().setValue((((curR+1)/iconv_r)-1)*h+((curR+1)/iconv_r)*10)
		
		elif event.key() == QtCore.Qt.Key_Left:
			
				nextR = ui.list1.currentRow()-1
				if nextR >=0:
					self.sizeAdjust(nextR,"backward")
				else:
					ui.btn1.setFocus()
					ui.dockWidget_3.show()
			
			
			
		elif event.key() == QtCore.Qt.Key_Down:

				
				
				nextR = ui.list1.currentRow()
				if nextR < 0:
					self.sizeAdjust(0,"down")
				else:
					nextR = ui.list1.currentRow()+iconv_r
					if nextR < ui.list1.count():
						self.sizeAdjust(nextR,"down")
					else:
						self.sizeAdjust(nextR-iconv_r,"down")
				
		elif event.key() == QtCore.Qt.Key_Up:
				nextR = ui.list1.currentRow()
				if nextR < 0:
					self.sizeAdjust(0,"up")
				else:
					nextR = ui.list1.currentRow()-iconv_r
					if nextR >= 0:
						self.sizeAdjust(nextR,"up")
					else:
						self.sizeAdjust(nextR+iconv_r,"up")
		
			
			
			
			
		elif event.key() == QtCore.Qt.Key_Right:
			nextR = ui.list1.currentRow()
			if nextR < 0:
				self.sizeAdjust(0,"forward")
			else:
				nextR = ui.list1.currentRow()+1
				if nextR < ui.list1.count():
					self.sizeAdjust(nextR,"forward")
				else:
					self.sizeAdjust(nextR-1,"forward")
			
		elif event.key() == QtCore.Qt.Key_Return:
			
			ui.listfound()
			ui.thumbnailHide('ExtendedQLabel')
			#ui.list2.show()
			ui.IconViewEpn()
			ui.scrollArea1.show()
			ui.scrollArea1.setFocus()
		#super(ExtendedQLabel, self).keyPressEvent(event)
		#super(QtGuiQWidgetScroll, self).keyPressEvent(event)
		
class QtGuiQWidgetScroll1(QtWidgets.QScrollArea):
	def __init__(self, parent):
		super(QtGuiQWidgetScroll1, self).__init__(parent)
	def sizeAdjust(self,nextR,direction):
		global icon_size_arr,iconv_r
		ui.list2.setCurrentRow(nextR)
		try:
			p1 = "ui.label_epn_"+str(nextR)+".y()"
			yy=eval(p1)
			
			p1 = "ui.label_epn_"+str(nextR)+".x()"
			xy=eval(p1)
			p1 = "ui.label_epn_"+str(nextR)+".setFocus()"
			exec (p1)
		except:
			return 0
		if ui.list2.count() > 1:
			if icon_size_arr:
				hi = icon_size_arr[1]
				wi = icon_size_arr[0]
				if direction == "down":		
					prevR = nextR - iconv_r
				elif direction == "up":
					prevR = nextR + iconv_r
				elif direction == "forward":
					prevR = nextR - 1
				elif direction == "backward":
					prevR = nextR + 1
				if prevR >= 0 and prevR < ui.list2.count():
					
						
					p1 = "ui.label_epn_"+str(prevR)+".setMinimumSize("+wi+","+hi+")"
					exec (p1)
					p1 = "ui.label_epn_"+str(prevR)+".setMaximumSize("+wi+","+hi+")"
					exec (p1)
					ht1 = (0.6*int(hi))
					wd1 = (0.6*int(wi))
					ht = str(ht1)
					wd = str(wd1)
				elif prevR < 0:
					p1 = "ui.label_epn_"+str(nextR)+".width()"
					wd1=eval(p1)
					p1 = "ui.label_epn_"+str(nextR)+".height()"
					ht1=eval(p1)
					ht = str(0.6*ht1)
					wd = str(0.6*wd1)
					print ("ht="+wd)
					print ("wd="+wd)
			else:
				p1 = "ui.label_epn_"+str(nextR)+".width()"
				wd1=eval(p1)
				p1 = "ui.label_epn_"+str(nextR)+".height()"
				ht1=eval(p1)
				ht = str(0.6*ht1)
				wd = str(0.6*wd1)
			
			ui.scrollArea1.verticalScrollBar().setValue(yy-ht1)
			ui.scrollArea1.horizontalScrollBar().setValue(xy-wd1)
			p1 = "ui.label_epn_"+str(nextR)+".setMinimumSize("+wd+","+ht+")"
			exec (p1)
			p1 = "ui.label_epn_"+str(nextR)+".setMaximumSize("+wd+","+ht+")"
			exec (p1)
			if site != "PlayLists":
				ui.labelFrame2.setText(ui.list2.currentItem().text())
			else:
				ui.labelFrame2.setText((ui.list2.currentItem().text()).split('	')[0])
			#p1 = "ui.label_"+str(nextR)+".setAlignment(QtCore.Qt.AlignCenter)"
			#exec p1
			#print "xy="+str(xy)
			#print "yy="+str(yy)
			ui.label.hide()
			ui.text.hide()
			#ui.label.setMaximumSize(300,250)
			#ui.text.setMaximumSize(300,10000)
			#if yy+ht1 > ui.tab_6.height():
		
	def keyPressEvent(self, event):
		global epnArrList,new_epn,Player,idw,mpvplayer,quitReally,curR,interval,iconv_r,total_till,browse_cnt,site,epn_name_in_list,memory_num_arr,thumbnail_indicator,mpvplayer,iconv_r_indicator,tab_6_size_indicator,tab_6_player,finalUrlFound,quality
		if not mpvplayer:
			mpvRunning = "False"
		if  mpvplayer:
			if mpvplayer.processId() > 0:
				mpvRunning = "True"
				#if event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Right:
				#	super(QtGuiQWidgetScroll1, self).keyPressEvent(event)
			else:
				mpvRunning = "False"
		if event.key() == QtCore.Qt.Key_Equal:
			
			#total_till = 0
			#browse_cnt = 0
			if iconv_r > 1:
				iconv_r = iconv_r-1
				if iconv_r_indicator:
					iconv_r_indicator.pop()
					
				iconv_r_indicator.append(iconv_r)
			if not ui.scrollArea.isHidden():
				ui.next_page('not_deleted')
				#ui.thumbnail_label_update()
			elif not ui.scrollArea1.isHidden():
				#ui.thumbnailEpn()
				ui.thumbnail_label_update()
			if iconv_r > 1:
				w = float((ui.tab_6.width()-60)/iconv_r)
				h = float((9*w)/16)
				width=str(int(w))
				height=str(int(h))
				ui.scrollArea1.verticalScrollBar().setValue((((curR+1)/iconv_r)-1)*h+((curR+1)/iconv_r)*10)
		elif event.key() == QtCore.Qt.Key_Minus:
			
			#total_till = 0
			#browse_cnt = 0
			iconv_r = iconv_r+1
			if iconv_r_indicator:
				iconv_r_indicator.pop()
			iconv_r_indicator.append(iconv_r)
			if not ui.scrollArea.isHidden():
				ui.next_page('not_deleted')
				#ui.thumbnail_label_update()
			elif not ui.scrollArea1.isHidden():
				#ui.thumbnailEpn()
				ui.thumbnail_label_update()
			if iconv_r > 1:
				w = float((ui.tab_6.width()-60)/iconv_r)
				h = float((9*w)/16)
				width=str(int(w))
				height=str(int(h))
				ui.scrollArea1.verticalScrollBar().setValue((((curR+1)/iconv_r)-1)*h+((curR+1)/iconv_r)*10)
		if mpvRunning == "False":
			if event.key() == QtCore.Qt.Key_Right:
				nextR = ui.list2.currentRow()
				if nextR < 0:
					self.sizeAdjust(0,"forward")
				else:
					nextR = ui.list2.currentRow()+1
					if nextR < ui.list2.count():
						self.sizeAdjust(nextR,"forward")
					else:
						self.sizeAdjust(nextR-1,"forward")
			elif event.key() == QtCore.Qt.Key_Left:
				
					nextR = ui.list2.currentRow()-1
					if nextR >=0:
						self.sizeAdjust(nextR,"backward")
					else:
						ui.btn1.setFocus()
						ui.dockWidget_3.show()
				
				
				
			elif event.key() == QtCore.Qt.Key_Down:

				
				
				nextR = ui.list2.currentRow()
				if nextR < 0:
					self.sizeAdjust(0,"down")
				else:
					nextR = ui.list2.currentRow()+iconv_r
					if nextR < ui.list2.count():
						self.sizeAdjust(nextR,"down")
					else:
						self.sizeAdjust(nextR-iconv_r,"down")
				
			elif event.key() == QtCore.Qt.Key_Up:
				nextR = ui.list2.currentRow()
				if nextR < 0:
					self.sizeAdjust(0,"up")
				else:
					nextR = ui.list2.currentRow()-iconv_r
					if nextR >= 0:
						self.sizeAdjust(nextR,"up")
					else:
						self.sizeAdjust(nextR+iconv_r,"up")
			elif event.key() == QtCore.Qt.Key_Backspace:
				if ui.list1.currentItem():
					ui.labelFrame2.setText(ui.list1.currentItem().text())
					ui.prev_thumbnails()
					ui.scrollArea.setFocus()
			elif event.key() == QtCore.Qt.Key_Return:
				ui.text.hide()
				ui.label.hide()
				tab_6_player = "False"
				if tab_6_size_indicator:
					tab_6_size_indicator.pop()
				if ui.tab_6.width()>500:
					tab_6_size_indicator.append(ui.tab_6.width())
				ui.gridLayout.setSpacing(0)
				if mpvplayer:
					if mpvplayer.processId() > 0:
						mpvplayer.write(b'\n quit \n')
						mpvplayer.kill()
				if site == "Local" or site == "Video" or site == "Music" or site == "PlayLists" or site=='None':
					
					
					quitReally = "no"
					
							#return 0
					#sending_button = self.sender()
					
					num = ui.list2.currentRow()
					curR = num
					
					ui.gridLayout.addWidget(ui.tab_6, 0, 1, 1, 1)
					
					if '	' in epnArrList[num]:
						new_epn = (epnArrList[num]).split('	')[0]
						
						finalUrl = '"'+((epnArrList[num]).split('	')[1])+'"'
					else:
						#new_epn = (epnArrList[num]).split('/')[-1]
						new_epn = os.path.basename(epnArrList[num])
						finalUrl = '"'+epnArrList[num]+'"'
					ui.epn_name_in_list = new_epn
					if num < ui.list2.count():
						ui.list2.setCurrentRow(num)
						
						idw = str(int(ui.tab_5.winId()))
						ui.gridLayout.addWidget(ui.tab_5, 0, 1, 1, 1)
						##ui.gridLayout.addWidget(ui.frame1, 1, 1, 1, 1)
						#ui.horizontalLayout10.addWidget(ui.tab_5)
						if ui.tab_5.isHidden() or ui.tab_5.width==0:
							ui.tab_5.show()
							ui.tab_5.setFocus()
							ui.frame1.show()
							thumbnail_indicator[:]=[]
							iconv_r = 1
							
							#ui.tab_6.setMaximumWidth(400)
							ui.thumbnail_label_update_epn()
							QtWidgets.QApplication.processEvents()
							p1 = "ui.label_epn_"+str(num)+".y()"
							
							ht = eval(p1)
							print(ht,'--ht--',ui.scrollArea1.height(),iconv_r,'--iconv_r--')
							ui.scrollArea1.verticalScrollBar().setValue(ht)
							
							ui.scrollArea1.verticalScrollBar().setValue(ht)
							
						finalUrl = finalUrl.replace('#','')
						finalUrl = str(finalUrl)
						finalUrl = finalUrl.replace('"','')
						if not finalUrl.startswith('http'):
							finalUrl = '"'+finalUrl+'"'
						if 'youtube.com' in finalUrl:
							finalUrl = finalUrl.replace('"','')
							ui.external_url = True
							finalUrl = get_yt_url(finalUrl,quality).strip()
							if '#' in finalUrl:
								audio_url = finalUrl.split('#')[0]
								video_url = finalUrl.split('#')[1]
								if Player == 'mpv':
									finalUrl = "--audio-file="+audio_url+' '+video_url
								elif Player == 'mplayer':
									finalUrl = '-audiofile '+audio_url+' '+video_url
						
						if Player == "mplayer":
							command = "mplayer -identify -nocache -idle -msglevel all=4:statusline=5:global=6 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
							print (command)
							ui.infoPlay(command)
						elif Player == "mpv":			
							command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+finalUrl
							ui.infoPlay(command)
						
				else:
			
						
						
						quitReally = "no"
						if mpvplayer:
							if mpvplayer.processId() > 0:
								mpvplayer.write(b'\n quit \n')
								mpvplayer.kill()
						num = ui.list2.currentRow()
						curR = num
						
						
						if '	' in epnArrList[num]:
							new_epn = (str(epnArrList[num])).split('	')[0]
						else:
							#if '/' in epnArrList[num] and finalUrlFound == True:
							#	new_epn = (str(epnArrList[num])).split('/')[-1]
							#else:
							#	new_epn = str(epnArrList[num])
							new_epn = os.path.basename(epnArrList[num])
						ui.epn_name_in_list = new_epn
						ui.list2.setCurrentRow(num)
						
						ui.epnfound()
						if num < ui.list2.count():
							ui.gridLayout.addWidget(ui.tab_5, 0, 1, 1, 1)
							##ui.gridLayout.addWidget(ui.frame1, 1, 1, 1, 1)
							ui.gridLayout.addWidget(ui.tab_6, 0, 1, 1, 1)
						
							#if ui.tab_5.isHidden() or ui.tab_5.width()==0:
							print (ui.tab_5.width())
							ui.tab_5.show()
							ui.tab_5.setFocus()
							ui.frame1.show()
							thumbnail_indicator[:]=[]
							iconv_r = 1
							ui.thumbnail_label_update_epn()
							QtWidgets.QApplication.processEvents()
							p1 = "ui.label_epn_"+str(num)+".y()"
							ht = eval(p1)
							print(ht,'--ht--',ui.scrollArea1.height())
							ui.scrollArea1.verticalScrollBar().setValue(ht)
							
							
				ui.mark_History()				
				title_num = num + ui.list2.count()
				if ui.epn_name_in_list.startswith(ui.check_symbol):
					newTitle = ui.epn_name_in_list
				else:
					newTitle = ui.check_symbol+ui.epn_name_in_list	
				sumry = "<html><h1>"+ui.epn_name_in_list+"</h1></html>"
				q4="ui.label_epn_"+str(title_num)+".setToolTip((sumry))"			
				exec (q4)
				q3="ui.label_epn_"+str(title_num)+".setText((newTitle))"
				exec (q3)
				p8="ui.label_epn_"+str(title_num)+".home(True)"
				exec (p8)
				p8="ui.label_epn_"+str(title_num)+".deselect()"
				exec (p8)
				QtWidgets.QApplication.processEvents()		
			super(QtGuiQWidgetScroll1, self).keyPressEvent(event)

class Btn1(QtWidgets.QComboBox):
	def __init__(self, parent):
		super(Btn1, self).__init__(parent)
		#self.setEditable(True)
		#self.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
	def keyPressEvent(self, event):
		global iconv_r
		if event.key() == QtCore.Qt.Key_Right:
			if not ui.list1.isHidden():
				ui.list1.setFocus()
			elif not ui.scrollArea.isHidden():
				ui.scrollArea.setFocus()
			elif not ui.scrollArea1.isHidden():
				ui.scrollArea1.setFocus()
			#ui.dockWidget_3.hide()
			#ui.label.setMinimumSize(700,500)
			#ui.label.setMaximumSize(300,350)
		elif event.key() == QtCore.Qt.Key_Left:
			if self.currentText() == 'Addons':
				ui.btnAddon.setFocus()
			else:
				ui.list3.setFocus()
			
		
		super(Btn1, self).keyPressEvent(event)
		

class tab6(QtWidgets.QWidget):
	def __init__(self, parent):
		super(tab6, self).__init__(parent)
	def resizeEvent(self,event):
		global tab_6_size_indicator,total_till,browse_cnt,thumbnail_indicator,mpvplayer,tab_6_player
		#print self.x()
		#print self.y()
		#print self.geometry()	
		
		if ui.tab_6.width() > 500 and tab_6_player == "False" and iconv_r != 1 and not ui.lock_process:
				#browse_cnt = 0
				if tab_6_size_indicator:
					tab_6_size_indicator.pop()
				tab_6_size_indicator.append(ui.tab_6.width())
				if not ui.scrollArea.isHidden():
						print('--------resizing----')
						ui.next_page('not_deleted')
						QtWidgets.QApplication.processEvents()
				elif not ui.scrollArea1.isHidden():
						ui.thumbnail_label_update()
		
	def keyPressEvent(self, event):
		global mpvplayer,Player,wget,cycle_pause,cache_empty,buffering_mplayer,curR,pause_indicator,thumbnail_indicator,iconv_r_indicator,cur_label_num
		global fullscr,idwMain,idw,quitReally,new_epn,toggleCache,total_seek,site,iconv_r,browse_cnt,total_till,browse_cnt,tab_6_size_indicator
		
		if tab_6_size_indicator:
			tab_6_size_indicator.pop()
		tab_6_size_indicator.append(ui.tab_6.width())
		"""
		if event.key() == QtCore.Qt.Key_Equal:
			
			total_till = 0
			browse_cnt = 0
			if iconv_r > 1:
				iconv_r = iconv_r-1
				if iconv_r_indicator:
					iconv_r_indicator.pop()
					
				iconv_r_indicator.append(iconv_r)
			if not ui.scrollArea.isHidden():
				ui.next_page()
				#ui.thumbnail_label_update()
			elif not ui.scrollArea1.isHidden():
				#ui.thumbnailEpn()
				ui.thumbnail_label_update()
			if iconv_r > 1:
				w = float((ui.tab_6.width()-60)/iconv_r)
				h = float((9*w)/16)
				width=str(int(w))
				height=str(int(h))
				ui.scrollArea1.verticalScrollBar().setValue((((curR+1)/iconv_r)-1)*h+((curR+1)/iconv_r)*10)
		elif event.key() == QtCore.Qt.Key_Minus:
			
			total_till = 0
			browse_cnt = 0
			iconv_r = iconv_r+1
			if iconv_r_indicator:
				iconv_r_indicator.pop()
			iconv_r_indicator.append(iconv_r)
			if not ui.scrollArea.isHidden():
				ui.next_page()
				#ui.thumbnail_label_update()
			elif not ui.scrollArea1.isHidden():
				#ui.thumbnailEpn()
				ui.thumbnail_label_update()
			if iconv_r > 1:
				w = float((ui.tab_6.width()-60)/iconv_r)
				h = float((9*w)/16)
				width=str(int(w))
				height=str(int(h))
				ui.scrollArea1.verticalScrollBar().setValue((((curR+1)/iconv_r)-1)*h+((curR+1)/iconv_r)*10)
		"""
		if event.key() == QtCore.Qt.Key_F:
			#mpvplayer.write('\n'+'add sub-pos +1'+'\n')
			if tab_6_size_indicator:
				tab_6_size_indicator.pop()
			if self.width() > 500:
				tab_6_size_indicator.append(self.width())
			fullscr = 1 - fullscr
			if not MainWindow.isFullScreen():
				#ui.gridLayout.setSpacing(0)
				ui.text.hide()
				ui.label.hide()
				ui.frame1.hide()
				#ui.tab_6.hide()
				ui.goto_epn.hide()
				ui.btn10.hide()
				#ui.btn20.hide()
				#ui.frame2.hide()
				if wget:
					if wget.processId() > 0:
						ui.progress.hide()
				ui.list2.hide()
				ui.list6.hide()
				ui.list1.hide()
				ui.frame.hide()
				#ui.text.hide()
				#ui.label.hide()
				#ui.tab_5.setParent(None)
				ui.gridLayout.setContentsMargins(0,0,0,0)
				ui.gridLayout.setSpacing(0)
				ui.superGridLayout.setContentsMargins(0,0,0,0)
				ui.gridLayout1.setContentsMargins(0,0,0,0)
				ui.gridLayout1.setSpacing(10)
				
				ui.gridLayout2.setContentsMargins(0,0,0,0)
				ui.gridLayout2.setSpacing(10)
				
				ui.horizontalLayout10.setContentsMargins(0,0,0,0)
				ui.horizontalLayout10.setSpacing(0)
				
				
				
				ui.tab_6.show()
				ui.tab_6.setFocus()
				#ui.tab_5.showFullScreen()
				#ui.gridLayout.showFullScreen()
				
				MainWindow.showFullScreen()
				
			else:
				
				ui.gridLayout.setSpacing(10)
				#ui.gridLayout.setContentsMargins(10,10,10,10)
				ui.superGridLayout.setContentsMargins(10,10,10,10)
				ui.gridLayout1.setSpacing(10)
				ui.gridLayout1.setContentsMargins(10,10,10,10)
				
				ui.gridLayout2.setSpacing(10)
				ui.gridLayout2.setContentsMargins(10,10,10,10)
				
				ui.horizontalLayout10.setContentsMargins(10,10,10,10)
				ui.horizontalLayout10.setSpacing(10)
				if wget:
					if wget.processId() > 0:
						ui.goto_epn.hide()
						ui.progress.show()
					
				#ui.btn20.show()
				#ui.frame2.show()
				MainWindow.showNormal()
				MainWindow.showMaximized()
				

		
class tab5(QtWidgets.QWidget):
	def __init__(self, parent):
		global cycle_pause,total_seek
		super(tab5, self).__init__(parent)
		cycle_pause = 0
		total_seek = 0
		self.arrow_timer = QtCore.QTimer()
		self.arrow_timer.timeout.connect(self.arrow_hide)
		self.arrow_timer.setSingleShot(True)
	
		self.mplayer_OsdTimer = QtCore.QTimer()
		self.mplayer_OsdTimer.timeout.connect(self.osd_hide)
		self.mplayer_OsdTimer.setSingleShot(True)
	
		self.seek_timer = QtCore.QTimer()
		self.seek_timer.timeout.connect(self.seek_mplayer)
		self.seek_timer.setSingleShot(True)
	
		self.float_timer = QtCore.QTimer()
		self.float_timer.timeout.connect(self.float_activity)
		self.float_timer.setSingleShot(True)
		
	def seek_mplayer(self):
		global Player,total_seek
		if Player == "mplayer":
				t = bytes('\n'+"seek " + str(total_seek)+'\n','utf-8')
				mpvplayer.write(t)
				total_seek = 0
	def osd_hide(self):
		global mpvplayer
		mpvplayer.write(b'\n osd 0 \n')
	def arrow_hide(self):
		global Player
		if Player == "mplayer" or Player == "mpv":
			self.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
		
		print ("arrow hide")
	def frameShowHide(self):
		global fullscr
		if MainWindow.isFullScreen():
			if ui.frame1.isHidden():
				ui.gridLayout.setSpacing(0)
				ui.frame1.show()
				ui.frame_timer.start(2000)
			else:
				ui.frame_timer.stop()
				ui.frame_timer.start(2000)
	"""
	def anim(self):

		self.animation = QtCore.QPropertyAnimation(MainWindow, "geometry")
		self.animation.setDuration(1000)
		self.animation.setStartValue(QtCore.QSize(0,0))
		w = MainWindow.width()
		h = MainWindow.height()
		self.animation.setEndValue(QtCore.QSize(w,h))
		self.animation.start()
	"""
	def float_activity(self):
		global new_tray_widget
		if not new_tray_widget.isHidden() and new_tray_widget.remove_toolbar:
			new_tray_widget.hide()
			print('--float--activity--')
	def mouseMoveEvent(self,event):
		global Player,fullscr,pause_indicator,site,new_tray_widget,ui
		self.setFocus()
		pos = event.pos()
		#print pos.y()
		if ui.auto_hide_dock and not ui.dockWidget_3.isHidden():
			ui.dockWidget_3.hide()
		if not ui.float_window.isHidden() and new_tray_widget.remove_toolbar:
			if not self.float_timer.isActive():
				wid_height = int(ui.float_window.height()/3)
				new_tray_widget.setMaximumHeight(wid_height)
				new_tray_widget.show()
				print('--float--timer--')
				self.float_timer.start(5000)
			else:
				#print('--stopping--float--timer--and--starting--again--')
				self.float_timer.stop()
				self.float_timer.start(5000)
		if (Player == "mplayer" or Player=="mpv"):
			if self.arrow_timer.isActive():
				self.arrow_timer.stop()
			self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			self.arrow_timer.start(2000)
	
		
		if MainWindow.isFullScreen():
			ht = self.height()
			#print "height="+str(ht)
			#print "y="+str(pos.y())
			if pos.y() <= ht and pos.y()> ht - 5 and ui.frame1.isHidden():
				ui.gridLayout.setSpacing(0)
				ui.frame1.show()
				#if Player == "mplayer":
				ui.frame1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			elif pos.y() <= ht-32 and not ui.frame1.isHidden():
				if site!="Music":
					ui.frame1.hide()
				
				ui.gridLayout.setSpacing(10)
				
	def ccurlHead(self,url):
		global rfr_url
		print ("------------ccurlHead------------")
		hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		"""
		if rfr_url:
			content = subprocess.check_output(['curl','-g','-I','-A',hdr,'-e',rfr_url,url])
		else:
			content = subprocess.check_output(['curl','-I','-A',hdr,url])
		if isinstance(content,str) :
			print("I'm unicode")
			content = content
		elif isinstance(content,bytes):
			print("I'm byte")
			content = (bytes(content).decode('utf-8'))
		"""
		if rfr_url:
			content = ccurl(url+'#'+'-Ie'+'#'+rfr_url)
		else:
			content = ccurl(url+'#'+'-I')
		return content
	def urlResolveSize(self,url):
		m =[]
		o = []
		content = self.ccurlHead(url)
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
		result = int(int(d['Content-Length'])/(1024*1024))
		return result
	def set_slider_val(self,val):
		t = ui.slider.value()
		t = t+val
		ui.slider.setValue(t)
	def keyPressEvent(self, event):
		global mpvplayer,Player,wget,cycle_pause,cache_empty,buffering_mplayer,curR,pause_indicator,thumbnail_indicator,iconv_r_indicator
		global fullscr,idwMain,idw,quitReally,new_epn,toggleCache,total_seek,site,iconv_r,browse_cnt,total_till,browse_cnt,sub_id,audio_id,rfr_url,show_hide_cover,show_hide_playlist,show_hide_titlelist,video_local_stream
		if event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Right:
			ui.list2.setFocus()
		elif event.key() == QtCore.Qt.Key_Right:
		
			if Player == "mplayer":
					self.set_slider_val(10)
					if site == "Local" or site == "None" or site == "PlayLists" or site == "Music" or site == "Video":
						mpvplayer.write(b'\n seek +10 \n')
					else:
						total_seek = total_seek + 10
						r = "Seeking "+str(total_seek)+'s'
						ui.progressEpn.setFormat(r)
						if self.seek_timer.isActive():
							self.seek_timer.stop()
						self.seek_timer.start(500)
			else:
				mpvplayer.write(b'\n seek +10 relative+exact \n')
			
			self.frameShowHide()
			
		
		elif event.key() == QtCore.Qt.Key_1:
			mpvplayer.write(b'\n add chapter -1 \n')
		elif event.key() == QtCore.Qt.Key_2:
			mpvplayer.write(b'\n add chapter 1 \n')
		elif event.key() == QtCore.Qt.Key_3:
			mpvplayer.write(b'\n cycle ass-style-override \n')
		elif event.modifiers() == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_V:
			mpvplayer.write(b'\n cycle ass-vsfilter-aspect-compat \n')
		elif event.key() == QtCore.Qt.Key_Left:
			if Player == "mplayer":
					self.set_slider_val(-10)
					if site == "Local" or site == "None" or site == "PlayLists" or site == "Music" or site == "Video":
						mpvplayer.write(b'\n seek -10 \n')
					else:
						total_seek = total_seek - 10
						r = "Seeking "+str(total_seek)+'s'
						ui.progressEpn.setFormat(r)
						#mpvplayer.write('\n'+'seek +10'+'\n')
						if self.seek_timer.isActive():
							self.seek_timer.stop()
						self.seek_timer.start(500)
						#mpvplayer.write('\n'+'seek -10'+'\n')
			else:
				mpvplayer.write(b'\n osd-msg-bar seek -10 \n')
			self.frameShowHide()
			#mpvplayer.write('\n'+'show_progress'+'\n')
		elif event.key() == QtCore.Qt.Key_0:
			if Player == "mplayer":
					self.set_slider_val(90)
					mpvplayer.write(b'\n seek +90 \n')
			else:
					mpvplayer.write(b'\n osd-msg-bar seek +90 \n')
			#mpvplayer.write('\n'+'show_progress'+'\n')
		
		elif event.key() == QtCore.Qt.Key_9:
			if Player == "mplayer":
					self.set_slider_val(-5)
					mpvplayer.write(b'\n seek -5 \n')
			else:
					mpvplayer.write(b'\n osd-msg-bar seek -5 \n')
			#mpvplayer.write('\n'+'show_progress'+'\n')
		
		elif event.key() == QtCore.Qt.Key_A:
			mpvplayer.write(b'\n cycle_values video-aspect "16:9" "4:3" "2.35:1" "-1" \n')
		elif event.key() == QtCore.Qt.Key_N:
			mpvplayer.write(b'\n playlist_next \n')
		elif event.key() == QtCore.Qt.Key_L:
			ui.tab_5.setFocus()
			
		elif event.key() == QtCore.Qt.Key_End:
			if Player == "mplayer":
				mpvplayer.write(b'\n seek 99 1 \n')
			else:
				mpvplayer.write(b'\n osd-msg-bar seek 100 absolute-percent \n')
		
		elif event.key() == QtCore.Qt.Key_P:
			#ui.tab_5.setFocus()
			if ui.frame1.isHidden():
				ui.gridLayout.setSpacing(0)
				ui.frame1.show()
			else:
				ui.gridLayout.setSpacing(10)
				ui.frame1.hide()
			#if Player == "mplayer":
			#	mpvplayer.write('\n'+'pausing osd_show_progression'+'\n')
			#else:
			#	mpvplayer.write('\n'+'show_text "${osd-sym-cc} ${time-pos} / ${time-remaining} (${percent-pos}%) (Cache : ${demuxer-cache-duration}s) (Buffer : ${cache-buffering-state}%)" 3000'+'\n')
				#toggleCache = 1 - toggleCache
				#if toggleCache == 1:
				#	mpvplayer.write('\n'+'keydown p'+'\n')
				
				#else:
				#	mpvplayer.write('\n'+'keyup p'+'\n')
			
		elif event.key() == QtCore.Qt.Key_Space:
			#cycle_pause = 1 - cycle_pause
			
			txt = ui.player_play_pause.text()
			if txt == ui.player_buttons['play']:
				ui.player_play_pause.setText(ui.player_buttons['pause'])
			elif txt == ui.player_buttons['pause']:
				ui.player_play_pause.setText(ui.player_buttons['play'])
				
			buffering_mplayer = "no"
			
			if ui.frame_timer.isActive:
				ui.frame_timer.stop()
			if ui.mplayer_timer.isActive():
				ui.mplayer_timer.stop()
			if Player == "mplayer":
				if MainWindow.isFullScreen():
					ui.frame1.hide()
				mpvplayer.write(b'\n pausing_toggle osd_show_progression \n')
				
				
			else:
				if not pause_indicator:
					mpvplayer.write(b'\n set pause yes \n')
					if MainWindow.isFullScreen():
						ui.gridLayout.setSpacing(0)
						ui.frame1.show()
						#QtGui.QApplication.processEvents()
					pause_indicator.append("Pause")
					#ui.gridLayout.setContentsMargins(0,0,0,0)
					#ui.superGridLayout.setContentsMargins(0,0,0,0)
					
				else:
					mpvplayer.write(b'\n set pause no \n')
					if MainWindow.isFullScreen():
						#ui.gridLayout.setSpacing(10)
						ui.frame1.hide()
					pause_indicator.pop()
					
					#ui.gridLayout.setSpacing(0)
					#ui.gridLayout.setContentsMargins(10,10,10,10)
					#ui.superGridLayout.setContentsMargins(10,10,10,10)
				#mpvplayer.write('\n'+'print-text "Pause-Status:${pause}"'+'\n')
			
				
		elif event.key() == QtCore.Qt.Key_Up:
			if Player == "mplayer":
				self.set_slider_val(60)
				if site == "Local" or site == "None" or site == "PlayLists" or site == "Music" or site == "Video":
					mpvplayer.write(b'\n seek +60 \n')
				else:
					total_seek = total_seek + 60
					r = "Seeking "+str(total_seek)+'s'
					ui.progressEpn.setFormat(r)
					#mpvplayer.write('\n'+'seek +10'+'\n')
					if self.seek_timer.isActive():
						self.seek_timer.stop()
					self.seek_timer.start(500)
					#mpvplayer.write('\n'+'seek +60'+'\n')
			else:
				mpvplayer.write(b'\n osd-msg-bar seek +60 \n')
			
			self.frameShowHide()
		elif event.key() == QtCore.Qt.Key_Down:
			if Player == "mplayer":
				self.set_slider_val(-60)
				if site == "Local" or site == "None" or site == "PlayLists" or site == "Music" or site == "Video": 
					mpvplayer.write(b'\n seek -60 \n')
				else:
					total_seek = total_seek - 60
					r = "Seeking "+str(total_seek)+'s'
					ui.progressEpn.setFormat(r)
					#mpvplayer.write('\n'+'seek +10'+'\n')
					if self.seek_timer.isActive():
						self.seek_timer.stop()
					self.seek_timer.start(500)
					#mpvplayer.write('\n'+'seek -60'+'\n')
			else:
				mpvplayer.write(b'\n osd-msg-bar seek -60 \n')
			
			self.frameShowHide()
		elif event.key() == QtCore.Qt.Key_PageUp:
			if Player == "mplayer":
				self.set_slider_val(300)
				if site == "Local" or site == "None" or site == "PlayLists" or site == "Music" or site == "Video":
					mpvplayer.write(b'\n seek +300 \n')
				else:
					total_seek = total_seek + 300
					r = "Seeking "+str(total_seek)+'s'
					ui.progressEpn.setFormat(r)
					#mpvplayer.write('\n'+'seek +10'+'\n')
					if self.seek_timer.isActive():
						self.seek_timer.stop()
					self.seek_timer.start(500)
					#mpvplayer.write('\n'+'seek +300'+'\n')
			else:
				mpvplayer.write(b'\n osd-msg-bar seek +300 \n')
			
			self.frameShowHide()
		elif event.key() == QtCore.Qt.Key_PageDown:
			if Player == "mplayer":
				self.set_slider_val(-300)
				if site == "Local" or site == "None" or site == "PlayLists" or site == "Music" or site == "Video":
					mpvplayer.write(b'\n seek -300 \n')
				else:
					total_seek = total_seek - 300
					r = "Seeking "+str(total_seek)+'s'
					ui.progressEpn.setFormat(r)
					#mpvplayer.write('\n'+'seek +10'+'\n')
					if self.seek_timer.isActive():
						self.seek_timer.stop()
					self.seek_timer.start(500)
					#mpvplayer.write('\n'+'seek -300'+'\n')
			else:
				mpvplayer.write(b'\n osd-msg-bar seek -300 \n')
			
			self.frameShowHide()
		elif event.key() == QtCore.Qt.Key_O:
			mpvplayer.write(b'\n osd \n')
		elif event.key() == QtCore.Qt.Key_M:
			#print (new_epn)
			
			if Player == "mplayer":
				mpvplayer.write(b'\n osd_show_property_text ${filename} \n')
			else:
				mpvplayer.write(b'\n show-text "${filename}" \n')
		elif event.key() == QtCore.Qt.Key_I:
			if Player == "mpv":
				mpvplayer.write(b'\n show_text ${file-size} \n')
			else:
				print (ui.final_playing_url)
				print (rfr_url)
				if ui.total_file_size:
					sz = str(ui.total_file_size)+' MB'
				else:
					if ui.final_playing_url.startswith('http') and ui.final_playing_url.endswith('.mkv'):
						ui.total_file_size = self.urlResolveSize(ui.final_playing_url)
						sz = str(ui.total_file_size)+' MB'
					else:
						ui.total_file_size = 0
						sz = str(0)
				t = bytes('\n'+'osd_show_text '+'"'+sz+'"'+' 4000'+'\n','utf-8')
				print (t)
				mpvplayer.write(t)
				#mpvplayer.write('\n'+'osd_show_text '+(sz)+' 4000'+'\n')
		elif event.key() == QtCore.Qt.Key_E:
			if Player == "mplayer" and MainWindow.isFullScreen():
				w=self.width()
				w = w + (0.05*w)
				h = self.height()
				h = h + (0.05*h)
				self.setMaximumSize(w,h)
			else:
				mpvplayer.write(b'\n add video-zoom +0.01 \n')
		elif event.key() == QtCore.Qt.Key_W:
			if Player == "mplayer" and MainWindow.isFullScreen():
				#mpvplayer.write('\n'+'panscan -0.05'+'\n')
				w=self.width()
				w = w - (0.05*w)
				h = self.height()
				h = h - (0.05*h)
				self.setMaximumSize(w,h)
			else:
				mpvplayer.write(b'\n add video-zoom -0.01 \n')
		elif event.key() == QtCore.Qt.Key_R:
			if Player == "mplayer":
				mpvplayer.write(b'\n sub_pos -1 \n')
			else:
				mpvplayer.write(b'\n add sub-pos -1 \n')
		elif event.key() == QtCore.Qt.Key_T:
			if Player == "mplayer":
				mpvplayer.write(b'\n sub_pos +1 \n')
			else:
				mpvplayer.write(b'\n add sub-pos +1 \n')
		elif event.modifiers() == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_J:
			ui.load_external_sub()
		elif event.key() == QtCore.Qt.Key_J:
			if Player == "mplayer":
				if not self.mplayer_OsdTimer.isActive():
					mpvplayer.write(b'\n osd 1 \n')
				else:
					self.mplayer_OsdTimer.stop()
				
				mpvplayer.write(b'\n sub_select \n')
				mpvplayer.write(b'\n get_property sub \n')
				self.mplayer_OsdTimer.start(5000)
			else:
				mpvplayer.write(b'\n cycle sub \n')
				mpvplayer.write(b'\n print-text "SUB_ID=${sid}" \n')
				mpvplayer.write(b'\n show-text "${sid}" \n')
		elif event.key() == QtCore.Qt.Key_K:
			if Player == "mplayer":
				if not self.mplayer_OsdTimer.isActive():
					mpvplayer.write(b'\n osd 1 \n')
				else:
					self.mplayer_OsdTimer.stop()

				mpvplayer.write(b'\n switch_audio \n')
				mpvplayer.write(b'\n get_property switch_audio \n')
				self.mplayer_OsdTimer.start(5000)
			else:
				mpvplayer.write(b'\n cycle audio \n')
				mpvplayer.write(b'\n print-text "Audio_ID=${aid}" \n')
				mpvplayer.write(b'\n show-text "${aid}" \n')
		elif event.key() == QtCore.Qt.Key_F:
			#mpvplayer.write('\n'+'add sub-pos +1'+'\n')
		
			#fullscr = 1 - fullscr
			if not MainWindow.isHidden():
				if not MainWindow.isFullScreen():
					ui.gridLayout.setSpacing(0)
					ui.superGridLayout.setSpacing(0)
					ui.gridLayout.setContentsMargins(0,0,0,0)
					ui.superGridLayout.setContentsMargins(0,0,0,0)
					#ui.frame1.setMaximumHeight(20)
					#ui.gridLayout.addWidget(ui.frame1, 1, 1, 1, 1)
					#ui.superGridLayout.addWidget(ui.tab_5, 0, 0, 1, 1)
					#ui.superGridLayout.addWidget(ui.frame1, 0, 1, 1, 1)
					ui.text.hide()
					ui.label.hide()
					#if site != "Music":
					ui.frame1.hide()
					ui.tab_6.hide()
					ui.goto_epn.hide()
					ui.btn20.hide()
					if wget.processId() > 0 or video_local_stream:
						ui.progress.hide()
						if not ui.torrent_frame.isHidden():
							ui.torrent_frame.hide()
						
					ui.list2.hide()
					ui.list6.hide()
					ui.list1.hide()
					ui.frame.hide()
					ui.dockWidget_3.hide()
					#ui.text.hide()
					#ui.label.hide()
					#ui.tab_5.setParent(None)
					
					#ui.tab_5.showMaximized()
					self.show()
					self.setFocus()
					#ui.tab_5.showFullScreen()
					if not ui.tab_2.isHidden():
						ui.tab_2.hide()
					#ui.gridLayout.showFullScreen()
					if (Player == "mplayer" or Player=="mpv"):
						MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
					#ui.superGridLayout.insertWidget()
					MainWindow.showFullScreen()
					#self.showFullScreen()
				else:
					
					ui.gridLayout.setSpacing(10)
					ui.superGridLayout.setSpacing(10)
					#ui.gridLayout.setContentsMargins(10,10,10,10)
					ui.superGridLayout.setContentsMargins(10,10,10,10)
					ui.list2.show()
					#ui.goto_epn.show()
					ui.btn20.show()
					if wget.processId() > 0 or video_local_stream:
						ui.progress.show()
						
					ui.frame1.show()
					if Player == "mplayer" or Player=="mpv":
						MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
					MainWindow.showNormal()
					MainWindow.showMaximized()
					if total_till != 0:
						ui.tab_6.show()
						ui.list2.hide()
						ui.goto_epn.hide()
					if ui.btn1.currentText().lower() == 'youtube':
						ui.list2.hide()
						ui.goto_epn.hide()
						ui.tab_2.show()
					#ui.tab_5.showNormal()
					#self.showNormal()
			else:
				if not ui.float_window.isHidden():
					if not ui.float_window.isFullScreen():
						ui.float_window.showFullScreen()
					else:
						ui.float_window.showNormal()
		elif event.key() == QtCore.Qt.Key_Period:
			ui.mpvNextEpnList()
		elif event.key() == QtCore.Qt.Key_Comma:
			#if Player != "mplayer":
			ui.mpvPrevEpnList()
		if event.key() == QtCore.Qt.Key_Q:
			
			quitReally = "yes"
			mpvplayer.write(b'\n quit \n')
			ui.player_play_pause.setText(ui.player_buttons['play'])
			if video_local_stream:
				tmp_pl = os.path.join(TMPDIR,'player_stop.txt')
				f = open(tmp_pl,'w')
				f.close()
			if ui.tab_6.isHidden():
				ui.tab_5.showNormal()
				ui.tab_5.hide()
				if show_hide_titlelist == 1:
					ui.list1.show()
					#ui.frame.show()
				if show_hide_cover == 1:
					ui.label.show()
					ui.text.show()
				if show_hide_titlelist == 1:
					ui.list2.show()
					#ui.goto_epn.show()
				
				ui.list2.setFocus()
			else:
				ui.gridLayout.addWidget(ui.tab_6, 0, 1, 1, 1)
				#ui.tab_5.setMinimumSize(0,0)
				ui.gridLayout.setSpacing(10)
				#ui.frame1.hide()
				ui.tab_5.hide()
				i = 0
				thumbnail_indicator[:]=[]
				if iconv_r_indicator:
					iconv_r = iconv_r_indicator[0]
				else:
					iconv_r = 4
				#ui.thumbnailEpn()
				
				#ui.thumbnail_label_update()
				#QtGui.QApplication.processEvents()
				#ui.frame2.show()
				num = ui.list2.currentRow()
				ui.thumbnail_label_update_epn()
				#ui.thumbnail_label_update()
				QtWidgets.QApplication.processEvents()
				ui.frame2.show()
				p1 = "ui.label_epn_"+str(num)+".y()"
				
				ht = eval(p1)
				print(ht,'--ht--',ui.scrollArea1.height())
				ui.scrollArea1.verticalScrollBar().setValue(ht)
				
				
			if wget:
				if wget.processId() > 0:
					#ui.goto_epn.hide()
					ui.progress.show()
		
			if MainWindow.isFullScreen():
				self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
				MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
				#if MainWindow.isFullScreen():
				ui.frame1.show()
				MainWindow.showNormal()
				MainWindow.showMaximized()
				MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
				ui.gridLayout.setSpacing(10)
				ui.superGridLayout.setSpacing(10)
				ui.superGridLayout.setContentsMargins(10,10,10,10)
			#ui.list2.setFocus()
			if not ui.tab_2.isHidden():
				ui.list2.hide()
				ui.goto_epn.hide()
				ui.list1.hide()
				ui.frame.hide()
			
		#super(List2, self).keyPressEvent(event)
	


class QDockNew(QtWidgets.QDockWidget):
	def __init__(self, parent):
		global cycle_pause,total_seek
		super(QDockNew, self).__init__(parent)
	def mouseReleaseEvent(self, ev):
		if ev.button() == QtCore.Qt.LeftButton:
			self.hide()
			ui.list4.hide()
	
def findimg(img):
	if img:
		#jpgn = img[0].split("/")[-1]
		jpgn = os.path.basename(img[0])
		print ("Pic Name=" + jpgn)
		#picn = "/tmp/AnimeWatch/" + jpgn
		picn = os.path.join(TMPDIR,jpgn)
		print (picn)
		if not os.path.isfile(picn):
			subprocess.Popen(["wget",img[0],"-O",picn])
	return picn
	


try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtWidgets.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		global BASEDIR,screen_width
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		#MainWindow.resize(875, 600)
		
		icon_path = os.path.join(BASEDIR,'tray.png')
		if not os.path.exists(icon_path):
			icon_path = '/usr/share/AnimeWatch/tray.png'
		if os.path.exists(icon_path):
			icon = QtGui.QIcon(icon_path)
		else:
			icon = QtGui.QIcon("")
		MainWindow.setWindowIcon(icon)
		self.superTab = QtWidgets.QWidget(MainWindow)
		self.superTab.setObjectName(_fromUtf8("superTab"))
		self.superGridLayout = QtWidgets.QGridLayout(MainWindow)
		self.superGridLayout.setObjectName(_fromUtf8("superGridLayout"))
		self.gridLayout = QtWidgets.QGridLayout(self.superTab)
		#self.gridLayout.setMouseTracking(True)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		self.superTab.setMouseTracking(True)
		self.superGridLayout.addWidget(self.superTab,0,1,1,1)
		self.superGridLayout.setContentsMargins(5,5,5,5)
		self.superGridLayout.setSpacing(0)
		self.gridLayout.setSpacing(5)
		self.gridLayout.setContentsMargins(5,5,5,5)
		
		#self.gridLayout.setColumnStretch(0,1)
		#self.gridLayout.setColumnStretch(2,1)
		#self.gridLayout.setColumnStretch(3,2)
		
		#self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab)
		#self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		#Causes No FullScreen#
		#self.gridLayout.setAlignment(QtCore.Qt.AlignBottom)
		
		self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
		self.gridLayout.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)
		
		self.VerticalLayoutLabel = QtWidgets.QHBoxLayout()
		self.VerticalLayoutLabel.setObjectName(_fromUtf8("VerticalLayoutLabel"))
		self.gridLayout.addLayout(self.VerticalLayoutLabel, 0, 1, 1, 1)
		#self.VerticalLayoutLabel.setContentsMargins(0,0,0,0)
		#self.VerticalLayoutLabel.setSpacing(5)
		#self.VerticalLayoutLabel.setAlignment(QtCore.Qt.AlignTop)
		
		self.verticalLayout_40 = QtWidgets.QVBoxLayout()
		self.verticalLayout_40.setObjectName(_fromUtf8("verticalLayout_40"))
		self.gridLayout.addLayout(self.verticalLayout_40, 0, 2, 1, 1)
		
		self.verticalLayout_50 = QtWidgets.QVBoxLayout()
		self.verticalLayout_50.setObjectName(_fromUtf8("verticalLayout_50"))
		self.gridLayout.addLayout(self.verticalLayout_50, 0, 3, 1, 1)
		
		#self.tabWidget = QtGui.QTabWidget(self.tab)
		#self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		#self.tab_3 = QtGui.QWidget()
		#self.tab_3.setObjectName(_fromUtf8("tab_3"))
		#self.horizontalLayout_4 = QtGui.QHBoxLayout(self.tab_3)
		#self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
		###########################
		self.label = QtWidgets.QLabel(MainWindow)
		#self.label.setSizePolicy(sizePolicy)
		
		#self.label.setMinimumSize(QtCore.QSize(300, 250))
		self.label.setText(_fromUtf8(""))
		self.label.setScaledContents(True)
		self.label.setObjectName(_fromUtf8("label"))
		self.text = QtWidgets.QTextBrowser(MainWindow)
		self.text.setObjectName(_fromUtf8("text"))
		#self.text.setMaximumSize(QtCore.QSize(450, 250))
		#self.text.setMinimumSize(QtCore.QSize(450, 250))
		
		self.text.lineWrapMode()
		#self.VerticalLayoutLabel.setStretch(2,1)
		self.VerticalLayoutLabel.insertWidget(0,self.label,0)
		self.VerticalLayoutLabel.insertWidget(1,self.text,0)
		#self.VerticalLayoutLabel.setStretch(1,2)
		self.VerticalLayoutLabel.addStretch(1)
		#self.text.hide()
		self.label.setAlignment(QtCore.Qt.AlignTop)
		self.text.setAlignment(QtCore.Qt.AlignBottom)
		self.VerticalLayoutLabel.setAlignment(QtCore.Qt.AlignBottom)
		self.VerticalLayoutLabel.setSpacing(5)
		self.VerticalLayoutLabel.setContentsMargins(0,0,0,0)
		#self.text.hide()
		#self.opacity = QtGui.QGraphicsOpacityEffect()
		#self.opacity.setOpacity(0.9)
		#self.label.setGraphicsEffect(self.opacity)
		
		#self.text.setAlignment(QtCore.Qt.AlignCenter)
		#self.text.show()
		#self.text.setMaximumSize(QtCore.QSize(800,400))
		#self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
		#self.tab_4 = QtGui.QWidget()
		#self.tab_4.setObjectName(_fromUtf8("tab_4"))
		#self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
		#self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
		#self.list1 = QtGui.QListWidget(self.tab)
		######################################
		self.list1 = List1(MainWindow)
		
	
		#self.list1.setStyleSheet(_fromUtf8("background-color: rgba(255, 170, 127, 50);"))
		self.list1.setObjectName(_fromUtf8("list1"))
		#self.list1.setMaximumSize(QtCore.QSize(400, 16777215))
		self.list1.setMouseTracking(True)
		#self.list1.setMinimumSize(QtCore.QSize(450, 16777215))
		self.verticalLayout_40.insertWidget(0,self.list1,0)
		
		#self.label11 = QtGui.QLabel(self.tab)
		#self.label11.setObjectName(_fromUtf8("label11"))
		#self.verticalLayout_40.insertWidget(1,self.label11,0)
		#self.label11.setText("Hello")
		
		
		
		self.btnEpnList = QtWidgets.QComboBox(MainWindow)
		self.btnEpnList.setObjectName(_fromUtf8("btnEpnList"))
		self.verticalLayout_40.addWidget(self.btnEpnList)
		self.btnEpnList.hide()
		#self.btnEpnList.setMaximumSize(QtCore.QSize(350, 16777215))
		###################################
		#self.list2 = QtGui.QListWidget(self.tab)
		self.list2 = List2(MainWindow)
		self.list2.setObjectName(_fromUtf8("list2"))
		#self.list2.setMaximumSize(QtCore.QSize(400,16777215))
		self.list2.setMouseTracking(True)
		
		
		#self.list2.setMinimumSize(QtCore.QSize(450, 16777215))
		#self.list1.setMaximumHeight(100)
		#self.list2.setMaximumHeight(100)
		#self.text.setMaximumWidth(400)
		self.verticalLayout_40.setAlignment(QtCore.Qt.AlignBottom)
		
		
		#self.verticalLayout_50.insertWidget(0,self.list1,0)
		self.verticalLayout_50.insertWidget(0,self.list2,0)
		#self.verticalLayout_50.insertWidget(2,self.text,0)
		#self.verticalLayout_50.insertWidget(3,self.label,0)
		self.verticalLayout_50.setAlignment(QtCore.Qt.AlignBottom)
		
		self.list4 = List4(MainWindow)
		self.list4.setObjectName(_fromUtf8("list4"))
		#self.list4.setMaximumSize(QtCore.QSize(400,16777215))
		self.list4.setMouseTracking(True)
		
		self.list4.hide()
		
		self.list5 = List5(MainWindow)
		self.list5.setObjectName(_fromUtf8("list5"))
		#self.list4.setMaximumSize(QtCore.QSize(400,16777215))
		self.list5.setMouseTracking(True)
		self.verticalLayout_50.insertWidget(1,self.list5,0)
		self.list5.hide()
		
		self.list6 = List6(MainWindow)
		self.list6.setObjectName(_fromUtf8("list6"))
		#self.list4.setMaximumSize(QtCore.QSize(400,16777215))
		self.list6.setMouseTracking(True)
		self.verticalLayout_50.insertWidget(2,self.list6,0)
		self.list6.hide()
		self.list6.addItem("Queue Empty:\nSelect Item and Press 'Q' to EnQueue it.\nIf Queue List is Empty then Items Will be\nPlayed Sequentially as per Playlist.\n(Queue Feature Works Only With\n Local/Offline Content)\n\nSelect Item and Press 'W' to toggle \nwatch/unwatch status\n")
		#self.gridLayout.addWidget(self.list2, 0, 2, 1, 1)
		self.frame = QtWidgets.QFrame(MainWindow)
		#self.frame.setMinimumSize(QtCore.QSize(500, 22))
		self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame.setObjectName(_fromUtf8("frame"))
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		
		self.backward = QtWidgets.QPushButton(self.frame)
		self.backward.setObjectName(_fromUtf8("backward"))
		self.horizontalLayout_3.addWidget(self.backward)
		
		self.hide_btn_list1 = QtWidgets.QPushButton(self.frame)
		self.hide_btn_list1.setObjectName(_fromUtf8("hide_btn_list1"))
		
		self.hide_btn_list1.setMinimumHeight(30)
		self.hide_btn_list1_menu = QtWidgets.QMenu()
		self.hide_btn_menu_option = ['Sort','Shuffle']
		self.action_player_menu2 =[]
		for i in self.hide_btn_menu_option:
			self.action_player_menu2.append(self.hide_btn_list1_menu.addAction(i, lambda x=i:self.playerPlaylist1(x)))
		self.hide_btn_list1.setMenu(self.hide_btn_list1_menu)
		self.hide_btn_list1.setCheckable(True)
		self.hide_btn_list1.setText('Order')
		self.filter_btn = QtWidgets.QPushButton(self.frame)
		self.filter_btn.setObjectName(_fromUtf8("filter_btn"))
		
		self.filter_btn.setMinimumHeight(30)
		self.filter_btn.hide()
		#self.go_page = QtGui.QLineEdit(self.frame)
		
		self.page_number = QtWidgets.QLineEdit(self.frame)
		self.page_number.setObjectName(_fromUtf8("page_number"))
		
		self.page_number.setMaximumWidth(48)
		self.page_number.setMinimumHeight(30)
		
		self.go_page = QLineCustom(self.frame)
		self.go_page.setObjectName(_fromUtf8("go_page"))
		self.go_page.setMinimumHeight(30)
		self.go_page.setPlaceholderText('Filter')
		#self.go_page.hide()
	
		
		
		self.forward = QtWidgets.QPushButton(self.frame)
		self.forward.setObjectName(_fromUtf8("forward"))
		self.horizontalLayout_3.addWidget(self.forward)
		self.forward.hide()
		self.backward.hide()
		
		self.horizontalLayout_3.insertWidget(2,self.page_number,0)
		self.horizontalLayout_3.insertWidget(3,self.go_page,0)
		self.horizontalLayout_3.insertWidget(4,self.filter_btn,0)
		self.horizontalLayout_3.insertWidget(5,self.hide_btn_list1,0)
		
		
		
		#self.gridLayout.addWidget(self.frame, 1, 1, 1, 1)
		#self.goto_epn = QtGui.QLineEdit(MainWindow)
		#self.goto_epn = QLineCustom(MainWindow)
		
		self.goto_epn = QtWidgets.QFrame(MainWindow)
		self.goto_epn.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.goto_epn.setFrameShadow(QtWidgets.QFrame.Raised)
		self.goto_epn.setObjectName(_fromUtf8("goto_epn"))
		self.horizontalLayout_goto_epn = QtWidgets.QHBoxLayout(self.goto_epn)
		self.horizontalLayout_goto_epn.setObjectName(_fromUtf8("horizontalLayout_goto_epn"))
		self.horizontalLayout_goto_epn.setContentsMargins(0,0,0,0)
		self.horizontalLayout_goto_epn.setSpacing(5)
		#self.gridLayout.addWidget(self.goto_epn, 1, 2, 1, 1)
		self.horizontalLayout_3.setContentsMargins(0,0,0,0)
		self.horizontalLayout_3.setSpacing(5)
		
		self.goto_epn.hide()
		self.frame.hide()
		
		#self.progress = QtWidgets.QProgressBar(MainWindow)
		self.progress = QProgressBarCustom(MainWindow,self)
		self.progress.setObjectName(_fromUtf8("progress"))
		#self.gridLayout.addWidget(self.progress, 1, 3, 1, 1)
		self.verticalLayout_50.insertWidget(3,self.progress,0)
		self.progress.setMinimum(0)
		self.progress.setMaximum(100)
		self.progress.setMaximumSize(QtCore.QSize(300,16777215))
		self.progress.setTextVisible(True)
		self.progress.hide()
		self.progress.setToolTip("Click for more options")
		self.player_buttons = {'play':'\u25B8','pause':'\u2225','stop':'\u25FE','prev':'\u2190','next':'\u2192','lock':'\u21BA','unlock':'\u21C4','quit':'\u2127','attach':'\u2022','left':'\u21A2','right':'\u21A3'}
		self.check_symbol = '\u2714'
		self.torrent_frame = QtWidgets.QFrame(MainWindow)
		self.torrent_frame.setMaximumSize(QtCore.QSize(300,16777215))
		self.torrent_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.torrent_frame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.torrent_frame.setObjectName(_fromUtf8("torrent_frame"))
		self.verticalLayout_50.insertWidget(4,self.torrent_frame,0)
		self.horizontalLayout_torrent_frame = QtWidgets.QHBoxLayout(self.torrent_frame)
		self.horizontalLayout_torrent_frame.setContentsMargins(0,2,0,2)
		self.horizontalLayout_torrent_frame.setSpacing(2)
		self.horizontalLayout_torrent_frame.setObjectName(_fromUtf8("horizontalLayout_torrent_frame"))
		self.torrent_frame.hide()
		
		self.label_torrent_stop = QtWidgets.QPushButton(self.torrent_frame)
		self.label_torrent_stop.setObjectName(_fromUtf8("label_torrent_stop"))
		self.label_torrent_stop.setText(self.player_buttons['stop'])
		self.label_torrent_stop.setMinimumWidth(24)
		self.horizontalLayout_torrent_frame.insertWidget(0,self.label_torrent_stop,0)
		#self.label_torrent_stop.setToolTip("Stop Torrent")
		
		self.label_down_speed = QtWidgets.QLineEdit(self.torrent_frame)
		self.label_down_speed.setObjectName(_fromUtf8("label_down_speed"))
		self.label_down_speed.setToolTip("Set Download Speed Limit For Current Session in KB\nEnter Only Integer Values")
		self.horizontalLayout_torrent_frame.insertWidget(1,self.label_down_speed,0)
		#self.label_down_speed.setMaximumWidth(100)
		self.label_up_speed = QtWidgets.QLineEdit(self.torrent_frame)
		self.label_up_speed.setObjectName(_fromUtf8("label_up_speed"))
		self.label_up_speed.setToolTip("Set Upload Speed Limit in KB for Current Session\nEnter Only Integer Values")
		self.horizontalLayout_torrent_frame.insertWidget(2,self.label_up_speed,0)
		
		
		
		#self.label_up_speed.setMaximumWidth(100)
		
		
		
		
		self.frame1 = QtWidgets.QFrame(MainWindow)
		self.frame1.setMaximumSize(QtCore.QSize(10000, 32))
		self.frame1.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.frame1.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame1.setObjectName(_fromUtf8("frame1"))
		self.horizontalLayout_31 = QtWidgets.QVBoxLayout(self.frame1)
		self.horizontalLayout_31.setContentsMargins(0,0,0,0)
		self.horizontalLayout_31.setSpacing(0)
		self.horizontalLayout_31.setObjectName(_fromUtf8("horizontalLayout_31"))
		#self.gridLayout.addWidget(self.frame1, 1, 0, 1, 1)
		
		self.frame2 = QtWidgets.QFrame(MainWindow)
		self.frame2.setMaximumSize(QtCore.QSize(10000, 32))
		self.frame2.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.frame2.setFrameShadow(QtWidgets.QFrame.Raised)
		self.frame2.setObjectName(_fromUtf8("frame2"))
		self.horizontalLayout_101= QtWidgets.QHBoxLayout(self.frame2)
		self.horizontalLayout_101.setContentsMargins(0,0,0,0)
		self.horizontalLayout_101.setSpacing(10)
		self.horizontalLayout_101.setObjectName(_fromUtf8("horizontalLayout_101"))
		#self.gridLayout.addWidget(self.frame1, 1, 0, 1, 1)
	
		
		self.progressEpn = QtWidgets.QProgressBar(self.frame1)
		self.progressEpn.setObjectName(_fromUtf8("progressEpn"))
		#self.gridLayout.addWidget(self.progressEpn, 1, 0, 1, 1)
		self.progressEpn.setMinimum(0)
		self.progressEpn.setMaximum(100)
		self.progressEpn.setMaximumSize(QtCore.QSize(10000,32))
		self.progressEpn.setTextVisible(True)
		
		self.slider = MySlider(self.frame1)
		self.slider.setObjectName(_fromUtf8("slider"))
		self.slider.setOrientation(QtCore.Qt.Horizontal)
		
		self.slider.setRange(0,100)
		self.slider.setMouseTracking(True)
		
		width_allowed = int((screen_width)/4.5)
		print(width_allowed,'--width--allowed--')
		self.list1.setMaximumWidth(width_allowed)
		self.list2.setMaximumWidth(width_allowed)
		self.list2.setIconSize(QtCore.QSize(128,128))
		self.frame.setMaximumWidth(width_allowed)
		self.list4.setMaximumWidth(width_allowed)
		self.list5.setMaximumWidth(width_allowed)
		self.list6.setMaximumWidth(width_allowed)
		self.goto_epn.setMaximumWidth(width_allowed)
		self.text.setMaximumWidth(screen_width-2*width_allowed-280)
		self.text.setMaximumHeight(250)
		self.label.setMaximumSize(QtCore.QSize(280, 250))
		self.label.setMinimumSize(QtCore.QSize(280, 250))
		
		self.list1.setWordWrap(True)
		self.list1.setTextElideMode(QtCore.Qt.ElideRight)
		self.list2.setWordWrap(True)
		self.list2.setTextElideMode(QtCore.Qt.ElideRight)
		self.list4.setWordWrap(True)
		self.list4.setTextElideMode(QtCore.Qt.ElideRight)
		self.list5.setWordWrap(True)
		self.list5.setTextElideMode(QtCore.Qt.ElideRight)
		self.list6.setWordWrap(True)
		self.list6.setTextElideMode(QtCore.Qt.ElideRight)
		#self.gridLayout.setAlignment(QtCore.Qt.AlignLeft)#Can cause video disappear in fullscreen mode
		#self.superGridLayout.setAlignment(QtCore.Qt.AlignRight)Can cause video disappear in fullscreen mode
		#self.verticalLayout_40.insertWidget(1,self.frame,0)
		
		self.player_opt = QtWidgets.QFrame(self.frame1)
		self.player_opt.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.player_opt.setFrameShadow(QtWidgets.QFrame.Raised)
		self.player_opt.setObjectName(_fromUtf8("player_opt"))
		self.horizontalLayout_player_opt = QtWidgets.QHBoxLayout(self.player_opt)
		self.horizontalLayout_player_opt.setObjectName(_fromUtf8("horizontalLayout_player_opt"))
		self.horizontalLayout_player_opt.setContentsMargins(0,2,0,2)
		self.horizontalLayout_player_opt.setSpacing(2)
		self.horizontalLayout_31.insertWidget(0,self.player_opt,0)
		self.horizontalLayout_31.insertWidget(1,self.progressEpn,0)
		self.horizontalLayout_31.insertWidget(2,self.slider,0)
		
		self.player_opt_toolbar= QtWidgets.QPushButton(self.player_opt)
		self.player_opt_toolbar.setObjectName(_fromUtf8("player_opt_toolbar"))
		self.horizontalLayout_player_opt.insertWidget(0,self.player_opt_toolbar,0)
		self.player_opt_toolbar.setText("Options")
		
		self.sd_hd = QtWidgets.QPushButton(self.player_opt)
		self.sd_hd.setObjectName(_fromUtf8("sd_hd"))
		self.horizontalLayout_player_opt.insertWidget(1,self.sd_hd,0)
		self.sd_hd.setText("SD")
		
		self.audio_track = QtWidgets.QPushButton(self.player_opt)
		self.audio_track.setObjectName(_fromUtf8("audio_track"))
		self.horizontalLayout_player_opt.insertWidget(2,self.audio_track,0)
		self.audio_track.setText("A/V")
		
		self.subtitle_track = QtWidgets.QPushButton(self.player_opt)
		self.subtitle_track.setObjectName(_fromUtf8("subtitle_track"))
		self.horizontalLayout_player_opt.insertWidget(3,self.subtitle_track,0)
		self.subtitle_track.setText("SUB")
		
		self.player_loop_file = QtWidgets.QPushButton(self.player_opt)
		self.player_loop_file.setObjectName(_fromUtf8("player_loop_file"))
		self.horizontalLayout_player_opt.insertWidget(4,self.player_loop_file,0)
		self.player_loop_file.setText(self.player_buttons['unlock'])
		#self.player_loop_file.hide()
		
		self.player_stop = QtWidgets.QPushButton(self.player_opt)
		self.player_stop.setObjectName(_fromUtf8("player_stop"))
		self.horizontalLayout_player_opt.insertWidget(5,self.player_stop,0)
		self.player_stop.setText(self.player_buttons['stop'])
		
		self.player_play_pause = QtWidgets.QPushButton(self.player_opt)
		self.player_play_pause.setObjectName(_fromUtf8("player_play_pause"))
		self.horizontalLayout_player_opt.insertWidget(6,self.player_play_pause,0)
		self.player_play_pause.setText(self.player_buttons['play'])
		
		self.player_prev = QtWidgets.QPushButton(self.player_opt)
		self.player_prev.setObjectName(_fromUtf8("player_prev"))
		self.horizontalLayout_player_opt.insertWidget(7,self.player_prev,0)
		self.player_prev.setText(self.player_buttons['prev'])
		
		self.player_next = QtWidgets.QPushButton(self.player_opt)
		self.player_next.setObjectName(_fromUtf8("player_next"))
		self.horizontalLayout_player_opt.insertWidget(8,self.player_next,0)
		self.player_next.setText(self.player_buttons['next'])
		
		
		self.player_showhide_title_list = QtWidgets.QPushButton(self.player_opt)
		self.player_showhide_title_list.setObjectName(_fromUtf8("player_showhide_title_list"))
		self.horizontalLayout_player_opt.insertWidget(9,self.player_showhide_title_list,0)
		self.player_showhide_title_list.setText('T')
		self.player_showhide_title_list.clicked.connect(lambda x=0:self.playerPlaylist("Show/Hide Title List"))
		self.player_showhide_title_list.setToolTip('Show/Hide Title List')
		
		self.player_showhide_playlist = QtWidgets.QPushButton(self.player_opt)
		self.player_showhide_playlist.setObjectName(_fromUtf8("player_showhide_playlist"))
		self.horizontalLayout_player_opt.insertWidget(10,self.player_showhide_playlist,0)
		#self.player_showhide_playlist.setText('\u2118')
		self.player_showhide_playlist.setText('PL')
		self.player_showhide_playlist.clicked.connect(lambda x=0:self.playerPlaylist("Show/Hide Playlist"))
		self.player_showhide_playlist.setToolTip('Show/Hide Playlist')
		
		self.player_filter = QtWidgets.QPushButton(self.player_opt)
		self.player_filter.setObjectName(_fromUtf8("player_filter"))
		self.horizontalLayout_player_opt.insertWidget(11,self.player_filter,0)
		self.player_filter.setText('Y')
		self.player_filter.setToolTip('Show/Hide Filter and other options')
		self.player_filter.clicked.connect(self.show_hide_filter_toolbar)
		
		self.player_playlist = QtWidgets.QPushButton(self.player_opt)
		self.player_playlist.setObjectName(_fromUtf8("player_playlist"))
		self.horizontalLayout_player_opt.insertWidget(12,self.player_playlist,0)
		self.player_playlist.setText("More")
		self.player_menu = QtWidgets.QMenu()
		self.player_menu_option = ['Show/Hide Video','Show/Hide Cover And Summary','Show/Hide Title List','Show/Hide Playlist','Lock Playlist','Lock File','Shuffle','Stop After Current File','Continue(default Mode)','Start Media Server','Set As Default Background','Show/Hide Web Browser']
		self.action_player_menu =[]
		for i in self.player_menu_option:
			self.action_player_menu.append(self.player_menu.addAction(i, lambda x=i:self.playerPlaylist(x)))
			
		#self.player_menu.addAction('This is Action 2', self.playerPlaylist)
		#menu.addAction('This is Action 2', self.Action2)
		self.player_playlist.setMenu(self.player_menu)
		self.player_playlist.setCheckable(True)
		
		
		self.queue_manage = QtWidgets.QPushButton(self.goto_epn)
		self.queue_manage.setObjectName(_fromUtf8("queue_manage"))
		self.horizontalLayout_goto_epn.insertWidget(0,self.queue_manage,0)
		self.queue_manage.setText("Q")
		self.queue_manage.setMinimumWidth(30)
		
		self.mirror_change = QtWidgets.QPushButton(self.goto_epn)
		self.mirror_change.setObjectName(_fromUtf8("mirror_change"))
		self.horizontalLayout_goto_epn.insertWidget(1,self.mirror_change,0)
		self.mirror_change.setText("Mirror")
		self.mirror_change.hide()
		
		self.goto_epn_filter = QtWidgets.QPushButton(self.goto_epn)
		self.goto_epn_filter.setObjectName(_fromUtf8("Filter Button"))
		self.horizontalLayout_goto_epn.insertWidget(2,self.goto_epn_filter,0)
		self.goto_epn_filter.setText("Filter")
		self.goto_epn_filter.hide()
		
		self.goto_epn_filter_txt = QLineCustomEpn(self.goto_epn)
		self.goto_epn_filter_txt.setObjectName(_fromUtf8("Filter Text"))
		self.horizontalLayout_goto_epn.insertWidget(3,self.goto_epn_filter_txt,0)
		self.goto_epn_filter_txt.setPlaceholderText("Filter")
		#self.goto_epn_filter_txt.hide()
		
		self.player_playlist1 = QtWidgets.QPushButton(self.goto_epn)
		self.player_playlist1.setObjectName(_fromUtf8("player_playlist1"))
		self.horizontalLayout_goto_epn.insertWidget(4,self.player_playlist1,0)
		self.player_playlist1.setText("Order")
		self.player_menu1 = QtWidgets.QMenu()
		self.player_menu_option1 = ['Order by Name(Ascending)','Order by Name(Descending)','Order by Date(Ascending)','Order by Date(Descending)']
		self.action_player_menu1 =[]
		for i in self.player_menu_option1:
			self.action_player_menu1.append(self.player_menu1.addAction(i, lambda x=i:self.playerPlaylist(x)))
			
		#self.player_menu.addAction('This is Action 2', self.playerPlaylist)
		#menu.addAction('This is Action 2', self.Action2)
		self.player_playlist1.setMenu(self.player_menu1)
		self.player_playlist1.setCheckable(True)
		
		self.frame1.setMinimumHeight(60)
		self.frame.setMinimumHeight(30)
		self.goto_epn.setMinimumHeight(30)
		self.frame1.setMaximumHeight(60)
		self.frame.setMaximumHeight(30)
		self.goto_epn.setMaximumHeight(30)
		
		self.mirror_change.setMaximumHeight(30)
		self.player_playlist1.setMaximumHeight(30)
		self.backward.setMaximumHeight(30)
		self.forward.setMaximumHeight(30)
		self.goto_epn_filter.setMaximumHeight(30)
		self.goto_epn_filter_txt.setMaximumHeight(30)
		self.queue_manage.setMaximumWidth(30)
		self.queue_manage.setMaximumHeight(30)
		
		#self.frame.setMaximumWidth(300)
		#self.tabWidget1.addTab(self.tab_2, _fromUtf8(""))
		self.tab_5 = tab5(MainWindow)
		#self.tab_5 = tab5(None)
		self.tab_5.setObjectName(_fromUtf8("tab_5"))
		#self.tabWidget1.addTab(self.tab_5, _fromUtf8(""))
		self.gridLayout.addWidget(self.tab_5,0,1,1,1)
		self.tab_5.setMouseTracking(True)
		#self.tab_5.setMaximumSize(100000,100000)
		#self.VerticalLayoutLabel.insertWidget(1,self.tab_5,0)
		self.tab_5.hide()
		#self.tab_5.setMinimumSize(100,100)
		#self.tab_6 = QtGui.QWidget(MainWindow)
		self.tab_6 = tab6(MainWindow)
		self.tab_6.setMouseTracking(True)
		#self.tab_6 = QtGui.QWidget()
		#self.gridLayout.addWidget(self.tab_6)
		#ui.gridLayout.addWidget(ui.tab_6, 0, 4, 1, 1)
		self.tab_6.setObjectName(_fromUtf8("tab_6"))
		#self.tabWidget1.addTab(self.tab_6, _fromUtf8(""))
		self.tab_6.hide()
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName(_fromUtf8("tab_2"))
		self.gridLayout.addWidget(self.tab_2,0,2,1,1)
		#self.superGridLayout.addWidget(self.tab_2,2,1,1,1)
		self.gridLayout.addWidget(self.tab_6,0,1,1,1)
		self.tab_2.hide()
		#self.tab_2.setMinimumSize(900,400)
		#MainWindow.setCentralWidget(self.centralwidget)
		
		#MainWindow.setMenuBar(self.menubar)
		#self.statusbar = QtGui.QStatusBar(MainWindow)
		#self.statusbar.setObjectName(_fromUtf8("statusbar"))
		#MainWindow.setStatusBar(self.statusbar)
		#self.dockWidget_3 = QtGui.QDockWidget(MainWindow)
		#self.dockWidget_3 = QtGui.QDockWidget(MainWindow)
		#self.dockWidget_3 = QDockNew(MainWindow)
		#self.dockWidget_3.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
		self.dockWidget_3 = QtWidgets.QFrame(MainWindow)
		self.dock_vert = QtWidgets.QVBoxLayout(self.dockWidget_3)
		self.dock_vert.setContentsMargins(0,0,0,0)
		self.dockWidget_3.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.dockWidget_3.setFrameShadow(QtWidgets.QFrame.Raised)
		
		self.dockWidget_3.setMouseTracking(True)
		self.dockWidget_3.setObjectName(_fromUtf8("dockWidget_3"))
		self.dockWidget_3.setMaximumWidth(200)
		#self.dockWidget_3.setMaximumHeight(500)
		
		#self.gridLayout.addLayout(self.VerticalLayoutLabel, 0, 0, 1, 1)
		
		#self.dockWidget_3.setMaximumSize(QtCore.QSize(150, 1000))
		self.dockWidgetContents_3 = QtWidgets.QWidget()
		self.dockWidgetContents_3.setObjectName(_fromUtf8("dockWidgetContents_3"))
		self.dock_vert.insertWidget(0,self.dockWidgetContents_3,0)
		#self.gridLayout.addWidget(self.dockWidget_3, 0, 0, 1, 1)
		#self.gridLayout.addWidget(self.dockWidget_3, 0,0 , 1, 1)
		#self.superGridLayout.addWidget(self.dockWidget_3,0,0,1,1)
		
		self.VerticalLayoutLabel_Dock3 = QtWidgets.QVBoxLayout(self.dockWidgetContents_3)
		self.VerticalLayoutLabel_Dock3.setObjectName(_fromUtf8("VerticalLayoutLabel_Dock3"))
		
		self.list3 = List3(self.dockWidgetContents_3)
		self.list3.setGeometry(QtCore.QRect(20, 100, 130, 201))
		self.list3.setObjectName(_fromUtf8("list3"))
		self.line = QtWidgets.QLineEdit(self.dockWidgetContents_3)
		self.line.setGeometry(QtCore.QRect(20, 20, 130, 26))
		#self.line.setGeometry(QtCore.QRect(20, 55, 130, 31))
		self.line.setObjectName(_fromUtf8("line"))
		#self.line.hide()
		self.line.setReadOnly(True)
		self.btn1 = Btn1(self.dockWidgetContents_3)
		#self.btn1.setGeometry(QtCore.QRect(20, 55, 130, 31))
		#self.btn1.setGeometry(QtCore.QRect(20, 20, 130, 26))
		self.btn1.setObjectName(_fromUtf8("btn1"))
		
		self.btnAddon = Btn1(self.dockWidgetContents_3)
		self.btnAddon.setObjectName(_fromUtf8("btnAddon"))
		self.btnAddon.hide()
		#self.btn1.setEditable(True)
		#self.btn1.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
		
		#self.dockWidget_3.setWidget(self.dockWidgetContents_3)
		#MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_3)
		self.dockWidget_4 = QtWidgets.QDockWidget(MainWindow)
		##self.dockWidget_4.setMinimumSize(QtCore.QSize(92, 159))
		self.dockWidget_4.setMaximumSize(QtCore.QSize(52000,200))
		self.dockWidget_4.setObjectName(_fromUtf8("dockWidget_4"))
		
		self.dockWidgetContents_4 = QtWidgets.QWidget()
		self.dockWidgetContents_4.setObjectName(_fromUtf8("dockWidgetContents_4"))
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.dockWidgetContents_4)
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		#self.text = QtGui.QTextBrowser(self.dockWidgetContents_4)
		#self.text.setObjectName(_fromUtf8("text"))
		#self.horizontalLayout.addWidget(self.text)
		self.dockWidget_4.setWidget(self.dockWidgetContents_4)
		
		###################  Browser Layout  ##############################
		self.horizontalLayout_5 = QtWidgets.QVBoxLayout(self.tab_2)
		#MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_4)
		
		self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
		self.dialog = QtWidgets.QDialog()
		#self.web = QWebView(self.tab_2)
		self.web = ''
		#self.web = Browser()
		#self.web.setObjectName(_fromUtf8("web"))
		#self.horizontalLayout_5.addWidget(self.web)
		##self.gridLayout.addWidget(self.tab_2,2,1,1,1)
		#self.web.hide()
		self.horizLayout_web = QtWidgets.QHBoxLayout()
		self.horizLayout_web.setObjectName(_fromUtf8("horizLayout_web"))
		self.horizontalLayout_5.addLayout(self.horizLayout_web)
		
		self.btnWebHide = QtWidgets.QPushButton(self.tab_2)
		self.btnWebHide.setObjectName(_fromUtf8("btnWebHide"))
		self.btnWebHide.setMaximumSize(200,50)
		self.horizLayout_web.insertWidget(0,self.btnWebHide,0)
		
		self.btnWebClose = QtWidgets.QPushButton(self.tab_2)
		self.btnWebClose.setObjectName(_fromUtf8("btnWebClose"))
		self.btnWebClose.setMaximumSize(200,50)
		self.horizLayout_web.insertWidget(1,self.btnWebClose,0)
		
		self.btnWebReviews = QtWidgets.QComboBox(self.tab_2)
		self.btnWebReviews.setObjectName(_fromUtf8("btnWebReviews"))
		self.horizLayout_web.insertWidget(2,self.btnWebReviews,0)
		self.btnWebReviews.setMaximumSize(200,50)
		
		self.btnGoWeb = QtWidgets.QPushButton(self.tab_2)
		self.btnGoWeb.setObjectName(_fromUtf8("btnGoWeb"))
		self.horizLayout_web.insertWidget(3,self.btnGoWeb,0)
		self.btnGoWeb.setMaximumSize(200,50)
		self.btnGoWeb.setText("Go")
		self.btnGoWeb.clicked.connect(lambda x=0: self.reviewsWeb(action='btn_pushed'))
		
		self.btnWebReviews_search = QtWidgets.QLineEdit(self.tab_2)
		self.btnWebReviews_search.setObjectName(_fromUtf8("btnWebReviews_search"))
		self.horizLayout_web.insertWidget(4,self.btnWebReviews_search,0)
		self.btnWebReviews_search.setMaximumSize(200,50)
		self.btnWebReviews_search.setPlaceholderText('Search Web')
		self.btnWebReviews_search.returnPressed.connect(lambda x=0:self.reviewsWeb(action='return_pressed'))
		
		
		
		##################
		
		
		self.btn2 = QtWidgets.QComboBox(self.dockWidgetContents_3)
		#self.btn2.setGeometry(QtCore.QRect(20, 315, 91, 31))
		self.btn2.setObjectName(_fromUtf8("btn2"))
		self.btn3 = QtWidgets.QPushButton(self.dockWidgetContents_3)
		#self.btn3.setGeometry(QtCore.QRect(120, 315, 31, 31))
		#self.btn3.setGeometry(QtCore.QRect(20, 315, 130, 31))
		self.btn3.setObjectName(_fromUtf8("btn3"))
		#self.btn9 = QtGui.QPushButton(self.dockWidgetContents_3)
		#self.btn9.setGeometry(QtCore.QRect(30, 410, 92, 31))
		#self.btn9.setObjectName(_fromUtf8("btn9"))
		self.btn3.setMinimumHeight(30)
		
		
		
		#self.chk = QtGui.QComboBox(self.dockWidgetContents_3)
		#self.chk.setGeometry(QtCore.QRect(40, 120, 91, 21))
		#self.chk.setObjectName(_fromUtf8("chk"))
		
		
		self.horizontalLayout10 = QtWidgets.QVBoxLayout(self.tab_6)
		self.horizontalLayout10.setObjectName(_fromUtf8("horizontalLayout"))
		#self.scrollArea = QtGui.QScrollArea(self.tab_6)
		self.scrollArea = QtGuiQWidgetScroll(self.tab_6)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
		self.scrollAreaWidgetContents = QtWidgets.QWidget()
		#self.scrollAreaWidgetContents = QtGuiQWidgetScroll()
		#self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 699, 469))
		self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
		self.gridLayout1 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
		self.gridLayout1.setObjectName(_fromUtf8("gridLayout1"))
		#self.gridLayout1.setAlignment(QtCore.Qt.AlignCenter)
		#self.horizontalLayout100 = QtGui.QHBoxLayout(self.tab_6)
		#self.horizontalLayout100.setObjectName(_fromUtf8("horizontalLayout"))
		#self.scrollArea1 = QtGui.QScrollArea(self.tab_6)
		self.scrollArea1 = QtGuiQWidgetScroll1(self.tab_6)
		self.scrollArea1.setWidgetResizable(True)
		
		self.scrollArea1.setObjectName(_fromUtf8("scrollArea1"))
		#self.scrollArea1.setMouseTracking(True)
		#self.scrollArea1.setFrameShape(QtGui.QFrame.NoFrame)
		
		self.scrollAreaWidgetContents1 = QtWidgets.QWidget()
		#self.scrollAreaWidgetContents1 = QWidgetResize(self.scrollArea1)
		#self.scrollAreaWidgetContents1.setGeometry(QtCore.QRect(0, 0, 699, 469))
		self.scrollAreaWidgetContents1.setObjectName(_fromUtf8("scrollAreaWidgetContents1"))
		self.gridLayout2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents1)
		self.gridLayout2.setObjectName(_fromUtf8("gridLayout2"))
		self.gridLayout2.setSpacing(0)
		#self.gridLayout2.setContentsMargins(0,0,0,0)
		#self.horizontalLayout10.setContentsMargins(0,0,0,0)
		#self.horizontalLayout10.setSpacing(0)
		
		self.btn10 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.btn10.setObjectName(_fromUtf8("btn10"))
		self.btn10.hide()
		self.gridLayout1.addWidget(self.btn10, 0, 0, 1, 1)
		#self.gridLayout1.setAlignment(QtCore.Qt.AlignCenter)
		
		#######################################################
		self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_20.setObjectName(_fromUtf8("horizontalLayout_20"))
		self.gridLayout1.addLayout(self.horizontalLayout_20, 0, 1, 1, 1)
		self.gridLayout1.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignCenter)
		self.gridLayout2.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignCenter)
		self.gridLayout2.setSpacing(5)
		
		
		
		self.btn30 = Btn1(self.scrollAreaWidgetContents)
		self.btn30.setObjectName(_fromUtf8("btn30"))
		self.horizontalLayout_20.insertWidget(0,self.btn30,0)
		self.comboBox20 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox20.setObjectName(_fromUtf8("comboBox20"))
		self.horizontalLayout_20.insertWidget(1,self.comboBox20, 0)
		
		self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_30.setObjectName(_fromUtf8("horizontalLayout_30"))
		self.gridLayout1.addLayout(self.horizontalLayout_30, 0, 2, 1, 1)
		
		self.comboBox30 = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
		self.comboBox30.setObjectName(_fromUtf8("comboBox30"))
		self.horizontalLayout_30.insertWidget(0,self.comboBox30, 0)
		
		self.btn20 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
		self.btn20.setObjectName(_fromUtf8("btn20"))
		#self.horizontalLayout_30.insertWidget(1,self.btn20, 0)
		
		self.labelFrame2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
		self.labelFrame2.setObjectName(_fromUtf8("labelFrame2"))
		self.labelFrame2.setScaledContents(True)
		self.labelFrame2.setAlignment(QtCore.Qt.AlignCenter)
		
		self.label_search = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
		self.label_search.setObjectName(_fromUtf8("label_search"))
		self.label_search.setMaximumWidth(100)
		
		self.btn201 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
		self.btn201.setObjectName(_fromUtf8("btn201"))
		#self.horizontalLayout_30.insertWidget(1,self.btn201, 0)
		self.float_window = QtWidgets.QLabel()
		self.float_window_layout = QtWidgets.QVBoxLayout(self.float_window)
		self.float_window.setMinimumSize(250,200)
		self.float_window.hide()
		self.float_window_dim = [20,40,250,200]
		self.float_window.setScaledContents(True)
		self.float_window.setObjectName(_fromUtf8("float_window"))
		try:
			self.float_window.setWindowIcon(icon)
		except:
			pass
		#self.float_window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
		self.float_window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
		self.float_window_layout.setContentsMargins(0,0,0,0)
		self.float_window_layout.setSpacing(0)
		
		self.horizontalLayout10.insertWidget(2,self.frame2, 0)
		self.horizontalLayout_101.insertWidget(0,self.btn20, 0)
		self.horizontalLayout_101.insertWidget(1,self.labelFrame2,0)
		self.horizontalLayout_101.insertWidget(2,self.btn201, 0)
		self.horizontalLayout_101.insertWidget(3,self.label_search, 0)
		
		####################################################
		#self.btn20.hide()
		self.comboBox20.hide()
		self.comboBox30.hide()
		self.btn30.hide()
		#self.btn10.setMaximumWidth(350)
		#self.btn20.setMaximumWidth(100)
		#self.comboBox20.setMaximumWidth(100)
		self.btn10.setMaximumSize(QtCore.QSize(350, 16777215))
		#self.btn20.setMaximumSize(QtCore.QSize(100, 16777215))
		self.comboBox20.setMaximumSize(QtCore.QSize(100, 16777215))
		
		
		self.chk = QtWidgets.QComboBox(self.dockWidget_3) 
		self.chk.setObjectName(_fromUtf8("chk"))
		#self.chk.setMaximumSize(QtCore.QSize(200, 16777215))
		#self.horizontalLayout_7.addWidget(self.chk)
		#self.chk.setGeometry(QtCore.QRect(20, 380, 91, 31))
		#self.chk.setGeometry(QtCore.QRect(20, 380, 130, 31))
		self.comboView = QtWidgets.QComboBox(self.dockWidget_3) 
		self.comboView.setObjectName(_fromUtf8("comboView"))
		self.comboView.hide()
		#self.comboView.setGeometry(QtCore.QRect(20, 420, 130, 31))
		
		#self.btn9 = QtGui.QPushButton(self.dockWidget_3)
		#self.btn9.setObjectName(_fromUtf8("btn9"))
		#self.btn9.setMaximumSize(QtCore.QSize(200, 16777215))
		#self.horizontalLayout_7.addWidget(self.btn9)
		#self.btn9.setGeometry(QtCore.QRect(120, 380, 31, 31))
		#############################################
		self.btnOpt = QtWidgets.QComboBox(MainWindow)
		self.btnOpt.setObjectName(_fromUtf8("btnOpt"))
		self.horizontalLayout_7.addWidget(self.btnOpt)
		self.btnOpt.hide()
		self.go_opt = QtWidgets.QPushButton(MainWindow)
		self.go_opt.setObjectName(_fromUtf8("go_opt"))
		self.horizontalLayout_7.addWidget(self.go_opt)
		self.go_opt.hide()
		#self.btn9.hide()
		#self.btn9.setMaximumSize(QtCore.QSize(200, 16777215))
		#####################################################
		self.close_frame = QtWidgets.QFrame(MainWindow)
		self.close_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.close_frame.setFrameShadow(QtWidgets.QFrame.Raised)
		self.horiz_close_frame = QtWidgets.QHBoxLayout(self.close_frame)
		self.horiz_close_frame.setSpacing(0)
		self.horiz_close_frame.setContentsMargins(0,0,0,0)
		self.scrollArea.setWidget(self.scrollAreaWidgetContents)
		self.horizontalLayout10.addWidget(self.scrollArea)
		self.scrollArea1.setWidget(self.scrollAreaWidgetContents1)
		self.horizontalLayout10.addWidget(self.scrollArea1)
		self.btn4 = QtWidgets.QPushButton(self.dockWidgetContents_3)
		self.btn4.setObjectName(_fromUtf8("btn4"))
		self.btn4.setMinimumHeight(30)
		self.btn4.setText('--')
		self.btn4.setToolTip('Auto-Hide On/Off')
		self.btn4.clicked.connect(self.close_frame_btn)
		self.auto_hide_dock = True
		
		self.btn_orient = QtWidgets.QPushButton(self.dockWidgetContents_3)
		self.btn_orient.setObjectName(_fromUtf8("btn_orient"))
		self.btn_orient.setMinimumHeight(30)
		self.btn_orient.setText(self.player_buttons['right'])
		self.btn_orient.setToolTip('Move Dock to Right')
		self.btn_orient.clicked.connect(self.orient_dock)
		self.orientation_dock = 'left'
		
		self.btn_quit = QtWidgets.QPushButton(self.dockWidgetContents_3)
		self.btn_quit.setObjectName(_fromUtf8("btn_quit"))
		self.btn_quit.setMinimumHeight(30)
		self.btn_quit.setText(self.player_buttons['quit'])
		self.btn_quit.setToolTip('Quit')
		self.btn_quit.clicked.connect(QtWidgets.qApp.quit)
		#self.close_frame.setMaximumHeight(30)
		
		
		self.horiz_close_frame.insertWidget(0,self.btn_quit,0)
		self.horiz_close_frame.insertWidget(1,self.btn_orient,0)
		self.horiz_close_frame.insertWidget(2,self.btn4,0)
		
		
		
		self.btnHistory = QtWidgets.QPushButton(self.dockWidgetContents_3)
		self.btnHistory.setObjectName(_fromUtf8("btnHistory"))
		self.btnHistory.hide()
		
		self.VerticalLayoutLabel_Dock3.insertWidget(0,self.line,0)
		self.VerticalLayoutLabel_Dock3.insertWidget(1,self.btn1,0)
		self.VerticalLayoutLabel_Dock3.insertWidget(2,self.btnAddon,0)
		self.VerticalLayoutLabel_Dock3.insertWidget(3,self.list3,0)
		self.VerticalLayoutLabel_Dock3.insertWidget(4,self.btnHistory,0)
		self.VerticalLayoutLabel_Dock3.insertWidget(5,self.btn3,0)
		self.VerticalLayoutLabel_Dock3.insertWidget(6,self.chk,0)
		self.VerticalLayoutLabel_Dock3.insertWidget(7,self.comboView,0)
		self.VerticalLayoutLabel_Dock3.insertWidget(8,self.close_frame,0)
		
		self.btn3.setMinimumHeight(30)
		self.line.setMinimumHeight(30)
		self.btn1.setMinimumHeight(30)
		self.chk.setMinimumHeight(30)
		self.comboView.setMinimumHeight(30)
		self.btnHistory.setMinimumHeight(30)
		
		
		#gridLayout content: self.frame1,self.frame,self.goto_epn
		#superGridLayout content : self.superTab,self.dockWidget_3
		 
		
		self.superGridLayout.addWidget(self.frame1, 1, 1, 1, 1)
		#self.superGridLayout.addWidget(self.tab_5, 0, 0, 1, 1)
		#self.gridLayout.addWidget(self.frame1, 1,1 , 1, 1)
		
		self.verticalLayout_50.insertWidget(0,self.list2,0)
		self.verticalLayout_50.insertWidget(1,self.list6,0)
		self.verticalLayout_50.insertWidget(2,self.list5,0)
		self.verticalLayout_50.insertWidget(3,self.goto_epn,0)
		
		
		self.verticalLayout_40.insertWidget(0,self.list1,0)
		self.verticalLayout_40.insertWidget(1,self.list4,0)
		self.verticalLayout_40.insertWidget(2,self.frame,0)
		self.verticalLayout_40.setSpacing(5)
		self.verticalLayout_50.setSpacing(5)
		
		#self.gridLayout.addWidget(self.frame1, 1, 1, 1, 1)
		#self.gridLayout.addWidget(self.frame, 1, 2, 1, 1)
		#self.gridLayout.addWidget(self.goto_epn, 1, 3, 1, 1)

		self.frame_timer = QtCore.QTimer()
		self.frame_timer.timeout.connect(self.frame_options)
		self.frame_timer.setSingleShot(True)
	
		self.mplayer_timer = QtCore.QTimer()
		self.mplayer_timer.timeout.connect(self.mplayer_unpause)
		self.mplayer_timer.setSingleShot(True)
		#self.frame_timer.start(5000)
		self.version_number = (3,0,0,42)
		self.threadPool = []
		self.threadPoolthumb = []
		self.thumbnail_cnt = 0
		self.player_setLoop_var = 0
		self.playerPlaylist_setLoop_var = 0
		self.thread_server = QtCore.QThread()
		self.do_get_thread = QtCore.QThread()
		self.stream_session = ''
		self.start_streaming = False
		self.local_http_server = QtCore.QThread()
		self.local_ip = ''
		self.local_port = ''
		self.local_ip_stream = ''
		self.local_port_stream = ''
		self.search_term = ''
		self.mpv_cnt = 0
		self.local_file_index = []
		self.quality_val = 'sd'
		self.current_background = os.path.join(home,'default.jpg')
		self.default_background = os.path.join(home,'default.jpg')
		self.yt_sub_folder = os.path.join(home,'External-Subtitle')
		self.torrent_type = 'file'
		self.torrent_handle = ''
		self.list_with_thumbnail = False
		self.mpvplayer_val = QtCore.QProcess()
		self.torrent_upload_limit = 0
		self.torrent_download_limit = 0
		self.torrent_download_folder = TMPDIR
		self.default_download_location = TMPDIR
		self.tmp_download_folder = TMPDIR
		self.epn_name_in_list = ''
		self.external_url = False
		self.subtitle_new_added = False
		self.window_frame = 'true'
		self.float_window_open = False
		self.music_mode_dim = [20,40,900,350]
		self.music_mode_dim_show = False
		self.site_var = ''
		self.record_history = False
		self.depth_list = 0
		self.display_list = False
		self.tmp_web_srch = ''
		self.update_proc = QtCore.QProcess()
		self.btn30.addItem(_fromUtf8(""))
		self.btn30.addItem(_fromUtf8(""))
		self.btn30.addItem(_fromUtf8(""))
		self.btn30.addItem(_fromUtf8(""))
		self.btn30.addItem(_fromUtf8(""))
		self.btn30.addItem(_fromUtf8(""))
		self.btn30.addItem(_fromUtf8(""))
		self.btn30.addItem(_fromUtf8(""))
		self.btn2.addItem(_fromUtf8(""))
		self.btn2.addItem(_fromUtf8(""))
		self.btn2.addItem(_fromUtf8(""))
		self.btn2.addItem(_fromUtf8(""))
		self.btn2.addItem(_fromUtf8(""))
		self.btn2.addItem(_fromUtf8(""))
		self.btn2.addItem(_fromUtf8(""))
		self.btn2.addItem(_fromUtf8(""))
		self.btn2.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.btnWebReviews.addItem(_fromUtf8(""))
		self.chk.addItem(_fromUtf8(""))
		self.chk.addItem(_fromUtf8(""))
		self.chk.addItem(_fromUtf8(""))
		self.chk.addItem(_fromUtf8(""))
		self.chk.addItem(_fromUtf8(""))
		#self.chk.addItem(_fromUtf8(""))
		#self.chk.addItem(_fromUtf8(""))
		self.comboBox20.addItem(_fromUtf8(""))
		self.comboBox20.addItem(_fromUtf8(""))
		self.comboBox20.addItem(_fromUtf8(""))
		self.comboBox20.addItem(_fromUtf8(""))
		self.comboBox20.addItem(_fromUtf8(""))
		self.comboView.addItem(_fromUtf8(""))
		self.comboView.addItem(_fromUtf8(""))
		self.comboView.addItem(_fromUtf8(""))
		QtWidgets.QShortcut(QtGui.QKeySequence("Shift+F"), MainWindow, self.fullscreenToggle)
		QtWidgets.QShortcut(QtGui.QKeySequence("Shift+L"), MainWindow, self.setPlayerFocus)
		QtWidgets.QShortcut(QtGui.QKeySequence("Shift+G"), MainWindow, self.dockShowHide)
		#QtGui.QShortcut(QtGui.QKeySequence("Y"), MainWindow, self.textShowHide)
		#QtGui.QShortcut(QtGui.QKeySequence("U"), MainWindow, self.epnShowHide)
		#QtGui.QShortcut(QtGui.QKeySequence("Q"), MainWindow, self.mpvQuit)
		
		
		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+F"), MainWindow, self.searchAnime)
		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Z"), MainWindow, self.IconView)
		QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+X"), MainWindow, self.showHideBrowser)
		QtWidgets.QShortcut(QtGui.QKeySequence("ESC"), MainWindow, self.HideEveryThing)
		#QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Enter), self.list2, self.epnfound)
		#return1 = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self.list1)
		#return2 = QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self.list2)
		#QtGui.QShortcut(QtGui.QKeySequence("Ctrl+F"), self.fullscreenToggle)
		
		self.list1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.list1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.list2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.list2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.list3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.list3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.list4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.list4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.list5.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.list5.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.list6.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.list6.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scrollArea1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scrollArea1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.retranslateUi(MainWindow)
		
		#QtCore.QObject.connect(self.player_opt_toolbar, QtCore.SIGNAL(_fromUtf8("clicked()")),self.player_opt_toolbar_dock)
		self.player_opt_toolbar.clicked.connect(self.player_opt_toolbar_dock)
		#QtCore.QObject.connect(self.sd_hd, QtCore.SIGNAL(_fromUtf8("clicked()")),self.selectQuality)
		self.sd_hd.clicked.connect(self.selectQuality)
		#QtCore.QObject.connect(self.goto_epn_filter, QtCore.SIGNAL(_fromUtf8("clicked()")),self.goto_epn_filter_on)
		self.goto_epn_filter.clicked.connect(self.goto_epn_filter_on)
		#QtCore.QObject.connect(self.queue_manage, QtCore.SIGNAL(_fromUtf8("clicked()")),self.queue_manage_list)
		self.queue_manage.clicked.connect(self.queue_manage_list)
		#QtCore.QObject.connect(self.audio_track, QtCore.SIGNAL(_fromUtf8("clicked()")),self.toggleAudio)
		self.audio_track.clicked.connect(self.toggleAudio)
		#QtCore.QObject.connect(self.subtitle_track, QtCore.SIGNAL(_fromUtf8("clicked()")),self.toggleSubtitle)
		self.subtitle_track.clicked.connect(self.toggleSubtitle)
		#QtCore.QObject.connect(self.player_stop, QtCore.SIGNAL(_fromUtf8("clicked()")),self.playerStop)
		self.player_stop.clicked.connect(self.playerStop)
		#QtCore.QObject.connect(self.player_prev, QtCore.SIGNAL(_fromUtf8("clicked()")),self.mpvPrevEpnList)
		self.player_prev.clicked.connect(self.mpvPrevEpnList)
		self.player_play_pause.clicked.connect(self.playerPlayPause)
		self.player_loop_file.clicked.connect(lambda x=0: self.playerLoopFile(self.player_loop_file))
		#QtCore.QObject.connect(self.player_next, QtCore.SIGNAL(_fromUtf8("clicked()")),self.mpvNextEpnList)
		self.player_next.clicked.connect(self.mpvNextEpnList)
		#QtCore.QObject.connect(self.mirror_change, QtCore.SIGNAL(_fromUtf8("clicked()")),self.mirrorChange)
		self.mirror_change.clicked.connect(self.mirrorChange)
		#QtCore.QObject.connect(self.btn20, QtCore.SIGNAL(_fromUtf8("clicked()")),lambda r=0:self.thumbnailHide('clicked'))
		self.btn20.clicked.connect(lambda r = 0: self.thumbnailHide('clicked'))
		#QtCore.QObject.connect(self.btn201, QtCore.SIGNAL(_fromUtf8("clicked()")), self.prev_thumbnails)
		self.btn201.clicked.connect(self.prev_thumbnails)
		#QtCore.QObject.connect(self.btnWebClose, QtCore.SIGNAL(_fromUtf8("clicked()")), self.webHide)
		self.btnWebClose.clicked.connect(self.webClose)
		self.btnWebHide.clicked.connect(self.webHide)
		#self.btnPls.clicked.connect(self.togglePlaylist)
		#QtCore.QObject.connect(self.go_opt, QtCore.SIGNAL(_fromUtf8("clicked()")), self.go_opt_options)
		self.go_opt.clicked.connect(self.go_opt_options)
		#QtCore.QObject.connect(self.btn10, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.browse_epn)
		self.btn10.currentIndexChanged['int'].connect(self.browse_epn)
		#QtCore.QObject.connect(self.line, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.searchNew)
		self.line.returnPressed.connect(self.searchNew)
		self.label_down_speed.returnPressed.connect(self.set_new_download_speed)
		self.label_up_speed.returnPressed.connect(self.set_new_upload_speed)
		self.label_torrent_stop.clicked.connect(self.stop_torrent)
		#QtCore.QObject.connect(self.page_number, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.gotopage)
		self.page_number.returnPressed.connect(self.gotopage)
		#QtCore.QObject.connect(self.btn1, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.ka)
		self.btn1.currentIndexChanged['int'].connect(self.ka)
		self.btnAddon.currentIndexChanged['int'].connect(self.ka2)
		#QtCore.QObject.connect(self.btn30, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.ka1)
		self.btn30.currentIndexChanged['int'].connect(self.ka1)
		#QtCore.QObject.connect(self.comboBox20, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.browserView_view)
		self.comboBox20.currentIndexChanged['int'].connect(self.browserView_view)
		#QtCore.QObject.connect(self.comboView, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.viewPreference)
		self.comboView.currentIndexChanged['int'].connect(self.viewPreference)
		#QtCore.QObject.connect(self.btn2, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.reviews)
		#self.btn2.currentIndexChanged['int'].connect(self.reviews)
		#QtCore.QObject.connect(self.btnWebReviews, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.reviewsWeb)
		self.btnWebReviews.currentIndexChanged['int'].connect(lambda x: self.reviewsWeb(action='index_changed'))
		#QtCore.QObject.connect(self.list1, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.listfound)
		self.list1.itemDoubleClicked['QListWidgetItem*'].connect(self.list1_double_clicked)
		#QtCore.QObject.connect(self.list1, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.history_highlight)
		self.list1.currentRowChanged['int'].connect(self.history_highlight)
		#QtCore.QObject.connect(self.list3, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.options_clicked)
		self.list3.currentRowChanged['int'].connect(self.options_clicked)
		#QtCore.QObject.connect(self.list4, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.search_highlight)
		self.list4.currentRowChanged['int'].connect(self.search_highlight)
		#QtCore.QObject.connect(self.list2, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), self.epnClicked)
		self.list2.itemDoubleClicked['QListWidgetItem*'].connect(self.epnClicked)
		#QtCore.QObject.connect(self.list2, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.epn_highlight)
		self.list2.currentRowChanged['int'].connect(self.epn_highlight)
		#QtCore.QObject.connect(self.list3, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), lambda var="clicked": self.options("clicked"))
		self.list3.itemDoubleClicked['QListWidgetItem*'].connect(lambda var = 'clicked':self.options('clicked'))
		#QtCore.QObject.connect(self.forward, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda r= "": self.nextp('next'))
		self.forward.clicked.connect(lambda r= "": self.nextp('next'))
		#QtCore.QObject.connect(self.backward, QtCore.SIGNAL(_fromUtf8("clicked()")),lambda r= "": self.backp('back'))
		self.backward.clicked.connect(lambda r= "": self.backp('back'))
		#QtCore.QObject.connect(self.filter_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.filter_btn_options)
		self.filter_btn.clicked.connect(self.filter_btn_options)
		#QtCore.QObject.connect(self.hide_btn_list1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.hide_btn_list1_pressed)
		self.hide_btn_list1.clicked.connect(self.hide_btn_list1_pressed)
		#QtCore.QObject.connect(self.go_page, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.filter_list)
		self.go_page.textChanged['QString'].connect(self.filter_list)
		#QtCore.QObject.connect(self.label_search, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.filter_label_list)
		self.label_search.textChanged['QString'].connect(self.filter_label_list)
		#QtCore.QObject.connect(self.goto_epn_filter_txt, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.filter_epn_list_txt)
		self.goto_epn_filter_txt.textChanged['QString'].connect(self.filter_epn_list_txt)
		#QtCore.QObject.connect(self.goto_epn, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.directepn)
		#self.goto_epn.returnPressed.connect(self.directepn)
		#QtCore.QObject.connect(self.btn3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addToLibrary)
		self.btn3.clicked.connect(self.addToLibrary)
		#QtCore.QObject.connect(self.btnHistory, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setPreOpt)
		self.btnHistory.clicked.connect(self.setPreOpt)
		#QtCore.QObject.connect(self.btn4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.dockWidget_3.hide)
		#self.btn4.clicked.connect(self.dockWidget_3.hide)
		#QtCore.QObject.connect(self.chk, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.preview)
		self.chk.currentIndexChanged['int'].connect(self.preview)
		
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		#self.frame.hide()
		#self.goto_epn.hide()
		self.btn2.hide()
		#self.btn9.hide()
		self.line.setPlaceholderText("Search")
		self.label_search.setPlaceholderText("Filter")
		#self.goto_epn.setPlaceholderText("Search")
		self.go_page.setPlaceholderText("Filter")
		#self.gridLayout.addLayout(self.VerticalLayoutLabel,1, 1, 1, 1)
		#self.gridLayout.addWidget(self.frame1, 1, 1, 1, 1)
		
	def retranslateUi(self, MainWindow):
		#MainWindow.setWindowTitle(_translate("MainWindow", "Anime Watch", None))
		#self.float_window.setWindowTitle(_translate("MainWindow", "Anime Watch", None))
		MainWindow.setWindowTitle("AnimeWatch")
		self.float_window.setWindowTitle("AnimeWatch")
		self.line.setToolTip(_translate("MainWindow", "<html><head/><body><p>Enter Search Keyword</p></body></html>", None))
		
		self.backward.setText(_translate("MainWindow", "Previous", None))
		self.filter_btn.setText(_translate("MainWindow", "Filter", None))
		#self.hide_btn_list1.setText(_translate("MainWindow", "Hide", None))
		#self.btn9.setText(_translate("MainWindow", "GO", None))
		#self.btn4.setText(_translate("MainWindow", "Hide", None))
		self.btnHistory.setText(_translate("MainWindow", "History", None))
		self.go_opt.setText(_translate("MainWindow", "Go", None))
		self.go_page.setToolTip(_translate("MainWindow", "<html><head/><body><p>Filter or Search</p></body></html>", None))
		self.forward.setText(_translate("MainWindow", "Next", None))
		self.page_number.setToolTip(_translate("MainWindow", "<html><head/><body><p align=\"center\">Enter Page Number</p></body></html>", None))
		#self.goto_epn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Enter Episode Name</p></body></html>", None))
		
		self.btn30.setItemText(0, _translate("MainWindow", "Select", None))
		self.btn30.setItemText(1, _translate("MainWindow", "Animejoy", None))
		self.btn30.setItemText(2, _translate("MainWindow", "Animebam", None))
		self.btn30.setItemText(3, _translate("MainWindow", "AnimePlace", None))
		self.btn30.setItemText(4, _translate("MainWindow", "SubbedAnime", None))
		self.btn30.setItemText(5, _translate("MainWindow", "DubbedAnime", None))
		self.btn30.setItemText(6, _translate("MainWindow", "AnimeHi10", None))
		self.btn30.setItemText(7, _translate("MainWindow", "KissAnime", None))
		self.btn3.setText(_translate("MainWindow", "Library", None))
		self.btnWebClose.setText(_translate("MainWindow", "Close", None))
		self.btnWebHide.setText(_translate("MainWindow", "Hide", None))
		self.btn2.setItemText(0, _translate("MainWindow", "Reviews", None))
		self.btn2.setItemText(1, _translate("MainWindow", "MyAnimeList", None))
		self.btn2.setItemText(2, _translate("MainWindow", "Anime-Planet", None))
		self.btn2.setItemText(3, _translate("MainWindow", "Anime-Source", None))
		self.btn2.setItemText(4, _translate("MainWindow", "TVDB", None))
		self.btn2.setItemText(5, _translate("MainWindow", "ANN", None))
		self.btn2.setItemText(6, _translate("MainWindow", "AniDB", None))
		self.btn2.setItemText(7, _translate("MainWindow", "Google", None))
		self.btn2.setItemText(8, _translate("MainWindow", "Youtube", None))
		self.btnWebReviews.setItemText(0, _translate("MainWindow", "Reviews", None))
		self.btnWebReviews.setItemText(1, _translate("MainWindow", "MyAnimeList", None))
		self.btnWebReviews.setItemText(2, _translate("MainWindow", "Anime-Planet", None))
		self.btnWebReviews.setItemText(3, _translate("MainWindow", "Anime-Source", None))
		self.btnWebReviews.setItemText(4, _translate("MainWindow", "TVDB", None))
		self.btnWebReviews.setItemText(5, _translate("MainWindow", "ANN", None))
		self.btnWebReviews.setItemText(6, _translate("MainWindow", "AniDB", None))
		self.btnWebReviews.setItemText(7, _translate("MainWindow", "Google", None))
		self.btnWebReviews.setItemText(8, _translate("MainWindow", "Youtube", None))
		self.btnWebReviews.setItemText(9, _translate("MainWindow", "DuckDuckGo", None))
		self.btnWebReviews.setItemText(10, _translate("MainWindow", "Zerochan", None))
		self.btnWebReviews.setItemText(11, _translate("MainWindow", "last.fm", None))
		self.chk.setItemText(0, _translate("MainWindow", "mpv", None))
		#self.chk.setItemText(1, _translate("MainWindow", "Default", None))
		self.chk.setItemText(1, _translate("MainWindow", "mplayer", None))
		self.chk.setItemText(2, _translate("MainWindow", "vlc", None))
		self.chk.setItemText(3, _translate("MainWindow", "kodi", None))
		self.chk.setItemText(4, _translate("MainWindow", "smplayer", None))
		#self.chk.setItemText(6, _translate("MainWindow", "bomi", None))
		self.comboBox20.setItemText(0, _translate("MainWindow", "Options", None))
		self.comboBox20.setItemText(1, _translate("MainWindow", "Clear", None))
		self.comboBox20.setItemText(2, _translate("MainWindow", "MostPopular", None))
		self.comboBox20.setItemText(3, _translate("MainWindow", "Random", None))
		self.comboBox20.setItemText(4, _translate("MainWindow", "History", None))
		self.comboView.setItemText(0, _translate("MainWindow", "View Mode", None))
		self.comboView.setItemText(1, _translate("MainWindow", "List", None))
		self.comboView.setItemText(2, _translate("MainWindow", "Thumbnail", None))
		#self.btn1.setItemText(1, _translate("MainWindow", "KissAnime", None))
		#self.btn2.setText(_translate("MainWindow", "Reviews", None))
		
		#self.label_9.setText(_translate("MainWindow", "", None))
		#self.label_3.setText(_translate("MainWindow", "", None))
		#self.label_2.setText(_translate("MainWindow", "", None))
		#self.label_0.setText(_translate("MainWindow", "", None))
		#self.label_7.setText(_translate("MainWindow", "", None))
		self.btn20.setText(_translate("MainWindow", "Close", None))
		self.btn201.setText(_translate("MainWindow", "Prev", None))
		#self.label_1.setText(_translate("MainWindow", "", None))
		#self.label_5.setText(_translate("MainWindow", "", None))
		#self.label_6.setText(_translate("MainWindow", "", None))
		#self.label_10.setText(_translate("MainWindow", "", None))
		#self.btn10.setText(_translate("MainWindow", "Episodes", None))
		#self.label_11.setText(_translate("MainWindow", "", None))
		#self.label_4.setText(_translate("MainWindow", "", None))
		#self.label_8.setText(_translate("MainWindow", "", None))
		#self.chk.setText(_translate("MainWindow", "MPV", None))
		
		#self.LibraryDialog.setWindowTitle(_translate("Dialog", "Library Setting", None))
		#self.AddLibraryFolder.setText(_translate("Dialog", "ADD", None))
		#self.RemoveLibraryFolder.setText(_translate("Dialog", "Remove", None))
		#self.LibraryClose.setText(_translate("Dialog", "Close", None))
		
		self.thumb_timer = QtCore.QTimer()
		self.mplayer_OsdTimer = QtCore.QTimer()
		self.mplayer_OsdTimer.timeout.connect(self.osd_hide)
		self.mplayer_OsdTimer.setSingleShot(True)
		
		self.mplayer_SubTimer = QtCore.QTimer()
		self.mplayer_SubTimer.timeout.connect(self.subMplayer)
		self.mplayer_SubTimer.setSingleShot(True)
		
		self.external_SubTimer = QtCore.QTimer()
		self.external_SubTimer.timeout.connect(self.load_external_sub)
		self.external_SubTimer.setSingleShot(True)
		
		self.total_file_size = 0
		self.id_audio_bitrate = 0
		self.id_video_bitrate = 0
		self.final_playing_url = ""
		self.queue_url_list = []
		self.downloadWget = []
		self.downloadWget_cnt = 0
		self.lock_process = False
		#self.trigger_play = QtCore.QObject.connect(self.line, QtCore.SIGNAL(("update(QString)")), self.player_started_playing)
		self.mpv_thumbnail_lock = False
		
	def show_hide_filter_toolbar(self):
		if self.list1.isHidden() and self.list2.isHidden():
			pass
		elif not self.list1.isHidden() and self.list2.isHidden():
			if self.frame.isHidden():
				self.frame.show()
			elif not self.frame.isHidden():
				self.frame.hide()
		elif self.list1.isHidden() and not self.list2.isHidden():
			if self.goto_epn.isHidden():
				self.goto_epn.show()
			elif not self.goto_epn.isHidden():
				self.goto_epn.hide()
		elif not self.list1.isHidden() and not self.list2.isHidden():
			if self.frame.isHidden() and not self.goto_epn.isHidden():
				self.goto_epn.hide()
			elif not self.frame.isHidden() and self.goto_epn.isHidden():
				self.frame.hide()
			elif not self.frame.isHidden() and not self.goto_epn.isHidden():
				self.frame.hide()
				self.goto_epn.hide()
			elif self.frame.isHidden() and self.goto_epn.isHidden():
				self.frame.show()
				self.goto_epn.show()
				
		
	def orient_dock(self,initial_start=None):
		if initial_start:
			txt = initial_start
			if txt == 'left':
				self.btn_orient.setText(self.player_buttons['right'])
				self.btn_orient.setToolTip('Orient Dock to Right')
				self.orientation_dock = 'left'
				self.superGridLayout.addWidget(self.dockWidget_3,0,1,1,1)
			else:
				self.btn_orient.setText(self.player_buttons['left'])
				self.btn_orient.setToolTip('Orient Dock to Left')
				self.orientation_dock = 'right'
				self.superGridLayout.addWidget(self.dockWidget_3,0,5,1,1)
				#self.gridLayout.addWidget(self.dockWidget_3,0,3,1,1)
		else:
			txt = self.btn_orient.text()
			if txt == self.player_buttons['right']:
				self.btn_orient.setText(self.player_buttons['left'])
				self.btn_orient.setToolTip('Orient Dock to Left')
				self.orientation_dock = 'right'
				self.superGridLayout.addWidget(self.dockWidget_3,0,5,1,1)
				#self.gridLayout.addWidget(self.dockWidget_3,0,3,1,1)
			else:
				self.player_buttons['left']
				self.btn_orient.setText(self.player_buttons['right'])
				self.btn_orient.setToolTip('Orient Dock to Right')
				self.orientation_dock = 'left'
				self.superGridLayout.addWidget(self.dockWidget_3,0,1,1,1)
			
	def close_frame_btn(self):
		txt = self.btn4.text()
		if txt == '--':
			self.btn4.setText('+')
			#self.btn4.setToolTip('Auto Hide Off')
			self.auto_hide_dock = False
		else:
			self.btn4.setText('--')
			#self.btn4.setToolTip('Auto Hide On')
			self.auto_hide_dock = True
			self.dockWidget_3.hide()
	def generate_thumbnail_method(self,picn,interval,path):
		global Player
		path = path.replace('"','')
		inter = str(interval)
		
		new_tmp = '"'+TMPDIR+'"'
		if not self.mpv_thumbnail_lock:
			if OSNAME == 'posix':
				subprocess.call(["ffmpegthumbnailer","-i",path,"-o",picn,"-t",str(inter),'-q','10','-s','350'])
			else:
				if inter.endswith('s'):
					inter = inter[:-1]
				#self.progressEpn.setFormat('Generating Thumbnail Wait..')
				self.mpv_thumbnail_lock = True
				if 'youtube.com' in path:
					subprocess.call(["mpv","--no-sub","--ytdl=yes","--quiet","--no-audio","--vo-image:outdir="+new_tmp,"--start="+str(inter)+"%","--frames=1",path],shell=True)
				else:
					if Player == 'mpv':
						subprocess.call(["mpv","--no-sub","--ytdl=no","--quiet","--no-audio","--vo=image:outdir="+new_tmp,"--start="+str(inter)+"%","--frames=1",path],shell=True)
					elif Player == 'mplayer':
						subprocess.call(["mplayer","-nosub","-nolirc","-nosound",'-vo',"jpeg:quality=100:outdir="+new_tmp,"-ss",str(inter),"-endpos","1","-frames","1","-vf","scale=320:180",path],shell=True)
					
				picn_path = os.path.join(TMPDIR,'00000001.jpg')
				if os.path.exists(picn_path):
					shutil.copy(picn_path,picn)
					os.remove(picn_path)
				self.mpv_thumbnail_lock = False
			#self.progressEpn.setFormat('Thumbnail Generated..')
	
	def create_new_image_pixel(self,art_url,pixel):
		#art_url_name = str(pixel)+'px.'+art_url.split('/')[-1]
		art_url_name = str(pixel)+'px.'+os.path.basename(art_url)
		#thumbnail = '/tmp/AnimeWatch/'+art_url_name+''
		#path_thumb = art_url.rsplit('/',1)[0]
		path_thumb,new_title = os.path.split(art_url)
		abs_path_thumb = os.path.join(path_thumb,art_url_name)
		try:
			if not os.path.exists(abs_path_thumb) and os.path.exists(art_url):
				basewidth = pixel
				img = Image.open(str(art_url))
				wpercent = (basewidth / float(img.size[0]))
				hsize = int((float(img.size[1]) * float(wpercent)))
				img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
				img.save(str(abs_path_thumb))
			elif not os.path.exists(art_url):
				#art_url_name = str(pixel)+'px.'+self.default_background.split('/')[-1]
				art_url_name = str(pixel)+'px.'+os.path.basename(self.default_background)
				#path_thumb = self.default_background.rsplit('/',1)[0]
				path_thumb,new_title = os.path.split(self.default_background)
				abs_path_thumb = os.path.join(path_thumb,art_url_name)

				if not os.path.exists(abs_path_thumb) and os.path.exists(self.default_background):
					basewidth = pixel
					img = Image.open(str(self.default_background))
					wpercent = (basewidth / float(img.size[0]))
					hsize = int((float(img.size[1]) * float(wpercent)))
					img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
					img.save(str(abs_path_thumb))
		except:
			#art_url_name = str(pixel)+'px.'+self.default_background.split('/')[-1]
			art_url_name = str(pixel)+'px.'+os.path.basename(self.default_background)
			#path_thumb = self.default_background.rsplit('/',1)[0]
			path_thumb,new_title = os.path.split(self.default_background)
			abs_path_thumb = os.path.join(path_thumb,art_url_name)
			if not os.path.exists(abs_path_thumb) and os.path.exists(self.default_background):
				basewidth = pixel
				img = Image.open(str(self.default_background))
				wpercent = (basewidth / float(img.size[0]))
				hsize = int((float(img.size[1]) * float(wpercent)))
				img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
				img.save(str(abs_path_thumb))
			
		return abs_path_thumb
	def list1_double_clicked(self):
		global show_hide_titlelist,show_hide_playlist,curR
		self.listfound()
		if site == "Music" and not ui.list2.isHidden():
			self.list2.setFocus()
			self.list2.setCurrentRow(0)
			curR = 0
			#self.epnfound()
			self.list1.show()
			#self.frame.show()
			
			self.list1.setFocus()
		else:
			if ui.list2.isHidden():
				self.list1.hide()
				self.frame.hide()
				self.list2.show()
				#self.goto_epn.show()
				self.list2.setFocus()
				show_hide_titlelist = 0
				show_hide_playlist = 1
		self.update_list2()
	def hide_torrent_info(self):
		self.torrent_frame.hide()
		self.progress.hide()
	def stop_torrent(self):
		global video_local_stream,wget
		if video_local_stream:
			if self.do_get_thread.isRunning():
				print('----------stream-----pausing-----')
				t_list = self.stream_session.get_torrents()
				for i in t_list:
					print(i.name(),'--removing--')
					self.stream_session.remove_torrent(i)
				self.stream_session.pause()
			elif self.stream_session:
				if not self.stream_session.is_paused():
					self.stream_session.pause()
			txt = 'Torrent Stopped'
			#subprocess.Popen(['notify-send',txt])
			send_notification(txt)
			self.torrent_frame.hide()
		else:
			if wget.processId() > 0:
				wget.kill()
			txt = 'Stopping download'
			#subprocess.Popen(['notify-send',txt])
			send_notification(txt)
			self.torrent_frame.hide()
	def set_new_download_speed(self):
		txt = self.label_down_speed.text()
		try:
			self.torrent_download_limit = int(txt) * 1024
		except:
			txt_notify = 'Please enter valid speed in KB'
			#subprocess.Popen(['notify-send',txt_notify])
			send_notification(txt_notify)
		self.label_down_speed.clear()
		self.torrent_handle.set_download_limit(self.torrent_download_limit)
		print(type(self.torrent_handle))
		down = '\u2193 SET TO: ' +str(int(self.torrent_download_limit/1024))+'K'
		self.label_down_speed.setPlaceholderText(down)
	def set_new_upload_speed(self):
		txt = self.label_up_speed.text()
		try:
			self.torrent_upload_limit = int(txt) * 1024
		except:
			txt_notify = 'Please enter valid speed in KB'
			#subprocess.Popen(['notify-send',txt_notify])
			send_notification(txt_notify)
		self.label_up_speed.clear()
		self.torrent_handle.set_upload_limit(self.torrent_upload_limit)
		print(type(self.torrent_handle))
		up = '\u2191 SET TO: ' +str(int(self.torrent_upload_limit/1024))+'K'
		self.label_up_speed.setPlaceholderText(up)
		
	def quitApp(self):
		app.quit()
	def queueList_return_pressed(self,r):
		t = self.queue_url_list[r]
		del self.queue_url_list[r]
		
		item = self.list6.item(r)
		i = item.text()
		self.list6.takeItem(r)
		del item
		self.list6.insertItem(0,i)
		self.queue_url_list.insert(0,t)
		self.getQueueInList()
	def queue_manage_list(self):
		if self.list6.isHidden():
			self.list6.show()
			self.list6.setFocus()
		else:
			self.list6.hide()
			
	def goto_epn_filter_on(self):
		if self.goto_epn_filter_txt.isHidden():
			self.goto_epn_filter_txt.show()
			self.goto_epn_filter_txt.setFocus()
		else:
			self.goto_epn_filter_txt.clear()
			#self.goto_epn_filter_txt.hide()
	def player_started_playing(self):
		global player_start_now
		player_start_now = 1
		print ("started")
	def player_opt_toolbar_dock(self):
		if self.dockWidget_3.isHidden():
			self.dockWidget_3.show()
		else:
			self.dockWidget_3.hide()
	def hide_btn_list1_pressed(self):
		if self.list1.isHidden():
			self.list1.show()
			self.hide_btn_list1.setText("Hide")
		else:
			self.list1.hide()
			self.hide_btn_list1.setText("Show")
	def subMplayer(self):
		global audio_id,sub_id,Player
		if Player == 'mplayer':
			t = bytes('\n'+"switch_audio "+str(audio_id)+'\n','utf-8')
			mpvplayer.write(t)
			#self.subtitle_track.setText(t2)
			t1 = bytes('\n'+"sub_select "+str(sub_id)+'\n','utf-8')
			mpvplayer.write(t1)
	def osd_hide(self):
		global mpvplayer
		mpvplayer.write(b'\n osd 0 \n')
	def mirrorChange(self):
		global mirrorNo
		txt = str(self.mirror_change.text())
		if txt == "Mirror":
			mirrorNo = 1
			self.mirror_change.setText("1")
		else:
			mirrorNo = int(txt)
			mirrorNo = mirrorNo + 1
			if mirrorNo == 10:
				self.mirror_change.setText("Mirror")
				mirrorNo = 1
			else:
				self.mirror_change.setText(str(mirrorNo))
		
	def toggleAudio(self):
			global Player,mpvplayer,audio_id
			if mpvplayer:
				if mpvplayer.processId() > 0:
					if Player == "mplayer":
						if not self.mplayer_OsdTimer.isActive():
							mpvplayer.write(b'\n osd 1 \n')
						else:
							self.mplayer_OsdTimer.stop()
						
						mpvplayer.write(b'\n switch_audio \n')
						mpvplayer.write(b'\n get_property switch_audio \n')
						self.mplayer_OsdTimer.start(5000)
					else:
						mpvplayer.write(b'\n cycle audio \n')
						mpvplayer.write(b'\n print-text "Audio_ID=${aid}" \n')
						mpvplayer.write(b'\n show-text "${aid}" \n')
			self.audio_track.setText("A:"+str(audio_id))
			
	def load_external_sub(self):
		global Player,mpvplayer,sub_id
		external_sub = False
		sub_arr = []
		#m = os.listdir(self.yt_sub_folder)
		#print(m)
		new_name = self.epn_name_in_list.replace('/','-')
		ext_arr = ['mkv','mp4','avi','flv']
		if new_name.startswith('.'):
			new_name = new_name[1:]
			new_name = new_name.strip()
		if '.' in new_name:
			ext = new_name.rsplit('.',1)[1]
			ext_n = ext.strip()
			if ext_n in ext_arr:
				new_name = new_name.rsplit('.',1)[0]
		new_name_original = new_name
		if new_name.endswith('YouTube'):
			new_name = ''.join(new_name.rsplit('YouTube',1))
			new_name = new_name.strip()
			if new_name.endswith('-'):
				new_name = new_name[:-1]
				new_name = new_name.strip()
		lang_ext = ['.en','.es','.jp','.fr']
		sub_ext = ['.vtt','.srt','.ass']
		for i in lang_ext:
			for j in sub_ext:
				k1 = new_name_original+i+j
				k2 = new_name+i+j
				sub_name_1 = os.path.join(self.yt_sub_folder,k1)
				sub_name_2 = os.path.join(self.yt_sub_folder,k2)
				#print(sub_name)
				if os.path.exists(sub_name_1):
					sub_arr.append(sub_name_1)
					external_sub = True
					print(sub_name_1)
				if os.path.exists(sub_name_2):
					sub_arr.append(sub_name_2)
					external_sub = True
					print(sub_name_2)
		print(new_name,'--new--name--')
		if mpvplayer.processId() > 0 and sub_arr:
			sub_arr.reverse()
			for title_sub in sub_arr:
				if Player == "mplayer":
					if os.path.exists(title_sub):
						txt = '\nsub_load '+'"'+title_sub+'"\n'
						txt_b = bytes(txt,'utf-8')
						print(txt_b,txt)
						mpvplayer.write(txt_b)
				else:
					if os.path.exists(title_sub):
						txt = '\nsub_add '+'"'+title_sub+'" select\n'
						txt_b = bytes(txt,'utf-8')
						print(txt_b,txt)
						mpvplayer.write(txt_b)
						
				
	def toggleSubtitle(self):
			global Player,mpvplayer,sub_id
			if mpvplayer:
				if mpvplayer.processId() > 0:
					if Player == "mplayer":
						if not self.mplayer_OsdTimer.isActive():
							mpvplayer.write(b'\n osd 1 \n')
						else:
							self.mplayer_OsdTimer.stop()
						
						mpvplayer.write(b'\n sub_select \n')
						mpvplayer.write(b'\n get_property sub \n')
						self.mplayer_OsdTimer.start(5000)
					else:
						mpvplayer.write(b'\n cycle sub \n')
						mpvplayer.write(b'\n print-text "SUB_ID=${sid}" \n')
						mpvplayer.write(b'\n show-text "${sid}" \n')
			self.subtitle_track.setText('Sub:'+str(sub_id))
			
	def playerStop(self):
			global quitReally,mpvplayer,thumbnail_indicator,total_till,browse_cnt,iconv_r_indicator,iconv_r,curR,wget,Player,show_hide_cover,show_hide_playlist,show_hide_titlelist,video_local_stream
			if mpvplayer:
				
				if mpvplayer.processId() > 0:
					quitReally = "yes"
					mpvplayer.write(b'\n quit \n')
					self.player_play_pause.setText(self.player_buttons['play'])
					if ui.tab_6.isHidden():
						ui.tab_5.showNormal()
						ui.tab_5.hide()
						
						if show_hide_titlelist == 1:
							ui.list1.show()
							#ui.frame.show()
						if show_hide_cover == 1:
							ui.label.show()
							ui.text.show()
						if show_hide_titlelist == 1:
							ui.list2.show()
							#ui.goto_epn.show()
						
						ui.list2.setFocus()
					else:
						#ui.tab_5.setMinimumSize(0,0)
						ui.gridLayout.addWidget(ui.tab_6, 0, 1, 1, 1)
						ui.gridLayout.setSpacing(10)
						
						#ui.frame1.hide()
						ui.tab_5.hide()
						i = 0
						thumbnail_indicator[:]=[]
						
						if iconv_r_indicator:
							iconv_r = iconv_r_indicator[0]
						else:
							iconv_r = 4
						#ui.thumbnailEpn()
						ui.thumbnail_label_update()
						ui.frame2.show()
						print ("width="+str(ui.tab_6.width()))
						#ui.tab_6.setMaximumSize(10000,10000)
						w = float((ui.tab_6.width()-60)/iconv_r)
						h = float((9*w)/16)
						width=str(int(w))
						height=str(int(h))
						ui.scrollArea1.verticalScrollBar().setValue(((curR+1)/iconv_r)*h+((curR+1)/iconv_r)*10)
						print ("hello tab_6")
					if wget:
						if wget.processId() > 0:
							ui.goto_epn.hide()
							ui.progress.show()
					if MainWindow.isFullScreen():
						MainWindow.showNormal()
						MainWindow.showMaximized()
						MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
						self.gridLayout.setSpacing(10)
						self.superGridLayout.setSpacing(10)
						self.superGridLayout.setContentsMargins(10,10,10,10)
	def shufflePlaylist(self):
		global epnArrList,site
		if site == "Local" or site =="Video" or site == "Music" or site == "PlayLists" or epnArrList:
			
			t = epnArrList[0]
			if '	' in t:
				print ("++++++++++++++++")
				m = random.sample(epnArrList,len(epnArrList))
				epnArrList[:]=[]
				epnArrList=m
				self.list2.clear()
				"""
				for i in epnArrList:
					i = i.replace('\n','')
					if '	' in i:
						i = i.split('	')[0]
						if i.startswith('#'):
							i = i.replace('#',ui.check_symbol,1)
							self.list2.item(i).setFont(QtGui.QFont('SansSerif', 10,italic=True))
						else:
							self.list2.addItem((i))	
				"""
				self.update_list2()
			
	def playerPlaylist1(self,val):
		if val == "Shuffle":
			self.shuffleList()
		else:
			self.sortList()
			
	def playerLoopFile(self,loop_widget):
		global Player,quitReally,tray,new_tray_widget
		txt = loop_widget.text()
		#txt = self.player_loop_file.text()
		if txt == self.player_buttons['unlock']:
			self.player_setLoop_var = 1
			self.player_loop_file.setText(self.player_buttons['lock'])
			new_tray_widget.lock.setText(self.player_buttons['lock'])
			quitReally = 'no'
			#if Player == "mpv":
			#	mpvplayer.write(b'\n set loop inf \n')
			
		else:
			self.player_setLoop_var = 0
			self.player_loop_file.setText(self.player_buttons['unlock'])
			new_tray_widget.lock.setText(self.player_buttons['unlock'])
			#quitReally = 'yes'
			#if Player == "mpv":
			#	mpvplayer.write(b'\n set loop 1 \n')
			
	def playerPlayPause(self):
		global mpvplayer,curR
		txt = self.player_play_pause.text() 
		if txt == self.player_buttons['play']:
			if mpvplayer.processId() > 0:
				if Player == "mpv":
					mpvplayer.write(b'\n set pause no \n')
				else:
					mpvplayer.write(b'\n pausing_toggle osd_show_progression \n')
				self.player_play_pause.setText(self.player_buttons['pause'])
			else:
				
				if self.list2.currentItem():
					curR = self.list2.currentRow()
					self.epnfound()
		elif txt == self.player_buttons['pause']:
			if mpvplayer.processId() > 0:
				if Player == "mpv":
					mpvplayer.write(b'\n set pause yes \n')
				else:
					mpvplayer.write(b'\n pausing_toggle osd_show_progression \n')
				self.player_play_pause.setText(self.player_buttons['play'])
			else:
				
				if self.list2.currentItem():
					curR = self.list2.currentRow()
					self.epnfound()
		
					
	def playerPlaylist(self,val):
		global quitReally,playlist_show,mpvplayer,epnArrList,site,show_hide_cover,show_hide_playlist,show_hide_titlelist,show_hide_player,Player,httpd
		self.player_menu_option = ['Show/Hide Video','Show/Hide Cover And Summary','Show/Hide Title List','Show/Hide Playlist','Lock Playlist','Lock File','Shuffle','Stop After Current File','Continue(default Mode)','Start Media Server','Set As Default Background','Show/Hide Web Browser']
		#txt = str(self.player_playlist.text())
		#playlist_show = 1-playlist_show
		#self.action[]
		
		print(val)
		if val == "Show/Hide Cover And Summary":
			v = str(self.action_player_menu[1].text())
			if self.text.isHidden() and self.label.isHidden():
				self.text.show()
				self.label.show()
				show_hide_cover = 1
				self.tab_5.hide()
				show_hide_player = 0
			elif self.text.isHidden() and not self.label.isHidden():
				self.text.show()
				self.label.show()
				show_hide_cover = 1
				self.tab_5.hide()
				show_hide_player = 0
			elif not self.text.isHidden() and self.label.isHidden():
				self.text.show()
				self.label.show()
				show_hide_cover = 1
				self.tab_5.hide()
				show_hide_player = 0
			else:
				self.text.hide()
				self.label.hide()
				show_hide_cover = 0
				self.tab_5.show()
				show_hide_player = 1
		
		elif val == "Show/Hide Playlist":
			v = str(self.action_player_menu[3].text())
			if self.tab_6.isHidden():
				if not self.list2.isHidden():
					self.list2.hide()
					self.goto_epn.hide()
					show_hide_playlist = 0
				else:
					self.list2.show()
					#self.goto_epn.show()
					show_hide_playlist = 1
					if MainWindow.isFullScreen():
						MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			else:
				self.tab_6.hide()
		elif val == "Show/Hide Title List":
			v = str(self.action_player_menu[2].text())
			if not self.list1.isHidden():
				self.list1.hide()
				self.frame.hide()
				show_hide_titlelist = 0
			else:
				self.list1.show()
				#self.frame.show()
				show_hide_titlelist = 1
				if MainWindow.isFullScreen():
					MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
		elif val == "Lock File":
			v = str(self.action_player_menu[5].text())
			if v == "Lock File":
				self.player_setLoop_var = 1
				self.action_player_menu[5].setText("UnLock File")
				self.player_loop_file.setText("unLock")
				
			elif v == "UnLock File":
					self.player_setLoop_var = 0
					self.action_player_menu[5].setText("Lock File")
					self.player_loop_file.setText("Lock")
					
		elif val == "Lock Playlist":
			v = str(self.action_player_menu[4].text())
			if v == "Lock Playlist":
				self.playerPlaylist_setLoop_var = 1
				self.action_player_menu[4].setText("UnLock Playlist")
			elif v == "UnLock Playlist":
					self.playerPlaylist_setLoop_var = 0
					self.action_player_menu[4].setText("Lock Playlist")
		
		elif val == "Stop After Current File":
			quitReally = "yes"
			#self.player_setLoop_var = 0
		elif val == "Continue(default Mode)":
			quitReally = "no"
		elif val == "Shuffle":
			epnArrList = random.sample(epnArrList,len(epnArrList))
			self.update_list2()
		elif val == "Show/Hide Video":
			if self.tab_5.isHidden():
				self.tab_5.show()
				show_hide_player = 1
				if not self.label.isHidden():
					self.label.hide()
					self.text.hide()
					show_hide_cover = 0
			else:
				self.tab_5.hide()
				show_hide_player = 0
		elif val =="Start Media Server":
			v= str(self.action_player_menu[9].text())
			if v == 'Start Media Server':
				self.start_streaming = True
				self.action_player_menu[9].setText("Stop Media Server")
				if not self.local_http_server.isRunning():
					if not self.local_ip_stream:
						self.local_ip_stream = '127.0.0.1'
						self.local_port_stream = 9001
					self.local_http_server = ThreadServerLocal(self.local_ip_stream,self.local_port_stream)
					self.local_http_server.start()
					msg = 'Media Server Started at \n http://'+self.local_ip_stream+':'+str(self.local_port_stream)
					#subprocess.Popen(["notify-send",msg])
					send_notification(msg)
			elif v == 'Stop Media Server':
				self.start_streaming = False
				self.action_player_menu[9].setText("Start Media Server")
				if self.local_http_server.isRunning():
					httpd.shutdown()
					self.local_http_server.quit()
					msg = 'Stopping Media Server\n http://'+self.local_ip_stream+':'+str(self.local_port_stream)
					#subprocess.Popen(["notify-send",msg])
					send_notification(msg)
		elif val == "Set As Default Background":
			if os.path.exists(self.current_background) and self.current_background != self.default_background:
					shutil.copy(self.current_background,self.default_background)
		elif val == "Show/Hide Web Browser":
			if self.tab_2.isHidden():
				if mpvplayer.processId() > 0:
					self.tab_2.show()
				else:
					self.showHideBrowser()
			else:
				self.tab_2.hide()
		elif site == "Music" or site == "Local" or site == "Video" or site == "PlayLists":
			if val == "Order by Name(Descending)":
				try:
					epnArrList = sorted(epnArrList,key = lambda x : str(x).split('	')[0],reverse=True)
				except:
					epnArrList = sorted(epnArrList,key = lambda x : x.split('	')[0],reverse=True)
				self.update_list2()
			elif val == "Order by Name(Ascending)":
				try:
					epnArrList = sorted(epnArrList,key = lambda x : str(x).split('	')[0])
				except:
					epnArrList = sorted(epnArrList,key = lambda x : x.split('	')[0])
				self.update_list2()
			elif val == "Order by Date(Descending)":
				try:
					epnArrList = sorted(epnArrList,key = lambda x : os.path.getmtime((str(x).split('	')[1]).replace('"','')),reverse=True)
				except:
					epnArrList = sorted(epnArrList,key = lambda x : os.path.getmtime((x.split('	')[1]).replace('"','')),reverse=True)
				self.update_list2()
			elif val == "Order by Date(Ascending)":
				try:
					epnArrList = sorted(epnArrList,key = lambda x : os.path.getmtime((str(x).split('	')[1]).replace('"','')))
				except:
					epnArrList = sorted(epnArrList,key = lambda x : os.path.getmtime((x.split('	')[1]).replace('"','')))
				self.update_list2()
		
	def selectQuality(self):
		global quality
		txt = str(self.sd_hd.text())
		if txt == "SD":
			quality = "sd480p"
			self.sd_hd.setText("480")
		elif txt == "480":
			quality = "hd"
			self.sd_hd.setText("HD")
		elif txt == "HD":
			quality = "sd"
			self.sd_hd.setText("SD")
		self.quality_val = quality
	def filter_btn_options(self):
		if not self.frame.isHidden() and self.tab_6.isHidden():
			if self.go_page.isHidden():
				self.go_page.show()
				self.go_page.setFocus()
				self.list4.show()
				self.go_page.clear()
			else:
				#self.go_page.hide()
				self.list4.hide()
				self.list1.setFocus()
		elif not self.tab_6.isHidden():
			self.label_search.setFocus()
	def addToLibrary(self):
		global home
		#self.LibraryDialog.show()
		self.LibraryDialog = QtWidgets.QDialog()
		self.LibraryDialog.setObjectName(_fromUtf8("Dialog"))
		self.LibraryDialog.resize(582, 254)
		self.listLibrary = QtWidgets.QListWidget(self.LibraryDialog)
		self.listLibrary.setGeometry(QtCore.QRect(20, 20, 341, 192))
		self.listLibrary.setObjectName(_fromUtf8("listLibrary"))
		self.AddLibraryFolder = QtWidgets.QPushButton(self.LibraryDialog)
		self.AddLibraryFolder.setGeometry(QtCore.QRect(420, 50, 94, 27))
		self.AddLibraryFolder.setObjectName(_fromUtf8("AddLibraryFolder"))
		self.RemoveLibraryFolder = QtWidgets.QPushButton(self.LibraryDialog)
		self.RemoveLibraryFolder.setGeometry(QtCore.QRect(420, 90, 94, 27))
		self.RemoveLibraryFolder.setObjectName(_fromUtf8("RemoveLibraryFolder"))
		self.LibraryClose = QtWidgets.QPushButton(self.LibraryDialog)
		self.LibraryClose.setGeometry(QtCore.QRect(420, 130, 94, 27))
		self.LibraryClose.setObjectName(_fromUtf8("LibraryClose"))
		self.LibraryDialog.setWindowTitle(_translate("Dialog", "Library Setting", None))
		self.AddLibraryFolder.setText(_translate("Dialog", "ADD", None))
		self.RemoveLibraryFolder.setText(_translate("Dialog", "Remove", None))
		self.LibraryClose.setText(_translate("Dialog", "Close", None))
		self.LibraryDialog.show()
		file_name = os.path.join(home,'local.txt')
		if os.path.exists(file_name):
			#f = open(file_name,'r')
			#lines = f.readlines()
			#f.close()
			lines = open_files(file_name,True)
			self.listLibrary.clear()
			for i in lines:
				i = i.replace('\n','')
				#print i
				self.listLibrary.addItem(i)
		#QtCore.QObject.connect(self.AddLibraryFolder, QtCore.SIGNAL(_fromUtf8("clicked()")), self.addFolderLibrary)
		self.AddLibraryFolder.clicked.connect(self.addFolderLibrary)
		#QtCore.QObject.connect(self.RemoveLibraryFolder, QtCore.SIGNAL(_fromUtf8("clicked()")), self.removeFolderLibrary)
		self.RemoveLibraryFolder.clicked.connect(self.removeFolderLibrary)
		#QtCore.QObject.connect(self.LibraryClose, QtCore.SIGNAL(_fromUtf8("clicked()")), self.LibraryDialog.close)
		self.LibraryClose.clicked.connect(self.LibraryDialog.close)
		
		
		self.LibraryClose.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
		self.RemoveLibraryFolder.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
		self.AddLibraryFolder.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
		self.listLibrary.setStyleSheet("""QListWidget{
		font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;
		}
	
	
		QListWidget:item:selected:active {
		background:rgba(0,0,0,20%);
		color: violet;
		}
		QListWidget:item:selected:inactive {
		border:rgba(0,0,0,30%);
		}
		QMenu{
			font: bold 12px;color:black;background-image:url('1.png');
		}
		""")
		
		picn = home+'/default.jpg'
		palette	= QtGui.QPalette()
		palette.setBrush(QtGui.QPalette.Background,QtGui.QBrush(QtGui.QPixmap(picn)))
		
		self.LibraryDialog.setPalette(palette)
	def options_clicked(self):
		global site,bookmark,siteName,opt,genre_num
		#genre_num = 0
		r = self.list3.currentRow()
		item = self.list3.item(r)
		if item and not self.lock_process:
			if not self.tab_6.isHidden():
				if site == "SubbedAnime" or site == "DubbedAnime":
					siteName = str(self.list3.currentItem().text())
					opt = "History"
					self.options('history') 
				elif site == "PlayLists" or bookmark == "True" or site == "Local" or site =="Music":
					
					self.options('local')
			else:
				if site == "PlayLists" or bookmark == "True" or site == "Local" or site =="Music":
					
					self.options('local') 
				elif site == "SubbedAnime" or site == "DubbedAnime":
					siteName = str(self.list3.currentItem().text())
					opt = "notHistory"
	def addFolderLibrary(self):
		global home,lastDir
		print ("add")
		fname = QtWidgets.QFileDialog.getExistingDirectory(self.LibraryDialog,'open folder',lastDir)
		lastDir = fname
		print (lastDir)
		print (fname)
		if not fname:
			pass
		else:
			self.listLibrary.addItem(fname)
			file_name = os.path.join(home,'local.txt')
			#if not os.path.exists(file_name):
			"""
			f = open(file_name,'w')
			
			for i in range(self.listLibrary.count()):
				fname = str(self.listLibrary.item(i).text())
				f.write(fname+'\n')
			f.close()
			"""
			write_files(file_name,fname,line_by_line=True)
		#self.listLibrary.setFocus()
	def removeFolderLibrary(self):
		print ("remove")
		index = self.listLibrary.currentRow()
		item  = self.listLibrary.item(index)
		if item:
			file_name = os.path.join(home,'local.txt')
			#f = open(file_name,'r')
			#lines = f.readlines()
			#f.close()
			lines = open_files(file_name,True)
			print (self.listLibrary.item(index).text())
			self.listLibrary.takeItem(index)
			del item
			del lines[index]
			"""
			f = open(file_name,'w')
			for i in range(self.listLibrary.count()):
				fname = str(self.listLibrary.item(i).text())
				f.write(fname+'\n')
			f.close()
			"""
			write_files(file_name,lines,line_by_line=True)
	def adjustVideoScreen(self,value):
		global mpvplayer,cur_label_num,fullscr
		if mpvplayer:
			if mpvplayer.processId()>0 and fullscr != 1: 
				w = float(800)
				h = float((9*w)/16)
				
				p2="ui.label_"+str(cur_label_num)+".x()"
				p3="ui.label_"+str(cur_label_num)+".y()"
				posx=eval(p2)
				posy=eval(p3)
				print ("vertical="+str(ui.scrollArea1.verticalScrollBar().maximum()))
				ui.scrollArea1.verticalScrollBar().setValue(posy+h)
				ui.scrollArea1.horizontalScrollBar().setValue(posx+w)
				print ("horiz="+str(ui.scrollArea1.horizontalScrollBar().maximum()))
		
	def viewPreference(self):
		global viewMode
		viewMode = str(self.comboView.currentText())
		
	def prev_thumbnails(self):
			global thumbnail_indicator,total_till,browse_cnt,tmp_name,label_arr,total_till_epn,iconv_r,mpvplayer,iconv_r_indicator
			self.scrollArea1.hide()
			self.scrollArea.show()
			i = 0
			try:
				self.labelFrame2.setText(ui.list1.currentItem().text())
			except AttributeError as attr_err:
				print(attr_err)
				return 0
			if thumbnail_indicator:
				print ("prev_thumb")
				print (thumbnail_indicator)
				thumbnail_indicator.pop()
				print (thumbnail_indicator)
				while(i<total_till_epn):
					t = "self.label_epn_"+str(i)+".deleteLater()"
					exec (t)
					i = i+1
				total_till_epn=0
			"""	
			label_arr[:]=[]
			browse_cnt=0
			tmp_name[:]=[]
			self.next_page('deleted')
			row = self.list1.currentRow()
			p1 = "ui.label_"+str(row)+".y()"
			yy=eval(p1)
			self.scrollArea.verticalScrollBar().setValue(yy)
			#self.browserView()
			"""
			print(total_till,2*self.list1.count()-1,'--prev-thumbnail--')
			if mpvplayer.processId() > 0:
				print(mpvplayer.processId(),'--prev-thumb--')
				iconv_r = 1
				self.next_page('not_deleted')
				QtWidgets.QApplication.processEvents()
				row = self.list1.currentRow()
				p1 = "ui.label_"+str(row)+".y()"
				yy=eval(p1)
				self.scrollArea.verticalScrollBar().setValue(yy)
				#self.scrollArea1.hide()
				#self.scrollArea.show()
			
			elif total_till > 0 and total_till == 2*self.list1.count():
				
				
				row = self.list1.currentRow()
				p1 = "ui.label_"+str(row)+".y()"
				yy=eval(p1)
				self.scrollArea.verticalScrollBar().setValue(yy)
				self.scrollArea1.hide()
				self.scrollArea.show()
			else:
				self.next_page('deleted')
				row = self.list1.currentRow()
				p1 = "ui.label_"+str(row)+".y()"
				yy=eval(p1)
				self.scrollArea.verticalScrollBar().setValue(yy)
				self.scrollArea1.hide()
				self.scrollArea.show()
	def mouseMoveEvent(self,event):
		print ("hello how r u" )
	def mplayer_unpause(self):
		global mpvplayer,fullscr,Player,buffering_mplayer,mpv_indicator
		buffering_mplayer = "no"
		if Player == "mplayer":
			mpvplayer.write(b'\n pause \n')
		else:
			mpvplayer.write(b'\n cycle pause \n')
			mpv_indicator.pop()
		print ("UnPausing")
		if MainWindow.isFullScreen():
			if not self.frame_timer.isActive():
				self.frame1.hide()
	def frame_options(self):
		global mpvplayer,Player,wget
		global fullscr,idwMain,idw,quitReally,new_epn,toggleCache
		print ("Frame Hiding" )
		if MainWindow.isFullScreen():
			ui.frame1.hide()
			ui.gridLayout.setSpacing(10)
	def webStyle(self,web):
		web.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
		web.setStyleSheet("""
		QMenu{
			font: bold 12px;color:black;background-image:url('1.png');
		}
		""")
	def buttonStyle(self,widget=None):
		global home,BASEDIR
		png_home = os.path.join(BASEDIR,'1.png')
		if not widget:
			ui.dockWidget_3.setStyleSheet("font:bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
					
					
			ui.tab_6.setStyleSheet("font:bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);")
			ui.tab_2.setStyleSheet("font:bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);")
			ui.tab_5.setStyleSheet("font:bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);")
			#ui.btn9.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
			ui.btnWebClose.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
			ui.btnWebHide.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
			ui.btn20.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
			ui.btn201.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
			ui.btnOpt.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
			ui.go_opt.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
			#ui.list1.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);")
			#ui.list2.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%)")
			#ui.list3.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%)")
			ui.text.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%)")
			ui.goto_epn.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,25%);border:rgba(0,0,0,30%);border-radius:3px;")
			ui.line.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;")
			ui.frame.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,25%);border:rgba(0,0,0,30%);border-radius:3px;")
			ui.frame1.setStyleSheet("font: bold 11px;color:white;background:rgba(0,0,0,60%);border:rgba(0,0,0,30%);border-radius:3px;")
			ui.torrent_frame.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);")
			ui.float_window.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);")
			#ui.progress.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);")
			ui.player_opt.setStyleSheet("font:bold 11px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;height:20px")
			
			
			ui.btn1.setStyleSheet("""QComboBox {
			min-height:30px;
			max-height:63px;
			border-radius: 3px;
			font-size:10px;
			padding: 1px 1px 1px 1px;
			font:bold 10px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			selection-color:yellow;
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:black;
			
			
			}

			QComboBox::focus {
			
			color:yellow;
			
			
			}


			QComboBox::down-arrow {
			
			width: 2px;
			height: 2px;
			}""")
		
			ui.btnAddon.setStyleSheet("""QComboBox {
			min-height:20px;
			max-height:63px;
			border-radius: 3px;
			font-size:10px;
			padding: 1px 1px 1px 1px;
			font:bold 10px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			selection-color:yellow;
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:black;
			
			
			}

			
			QComboBox::focus {
			
			color:yellow;
			
			
			}
			QComboBox::down-arrow {
			
			width: 2px;
			height: 2px;
			}""")
			
			
			ui.comboView.setStyleSheet("""QComboBox {
			min-height:20px;
			max-height:63px;
			border-radius: 3px;
			padding: 1px 1px 1px 1px;
			font:bold 12px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:black;
			
			
			}

			QComboBox::down-arrow {
			
			width: 2px;
			height: 2px;
			}""")

			ui.slider.setStyleSheet("""QSlider:groove:horizontal {
		
			height: 8px;
			border:rgba(0,0,0,30%);
			background:rgba(0,0,0,30%);
			margin: 2px 0;
			}

			QSlider:handle:horizontal {
			background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
			border: 1px solid #5c5c5c;
			
			width: 2px;
			margin: -2px 0; 
			border-radius: 3px;
			}

			QToolTip {
			font : Bold 10px;
			color: white;
			background:rgba(157,131,131,80%)
			}
				""")

			ui.list1.setStyleSheet("""QListWidget{
			font: Bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius:3px;
			}
			
			QListWidget:item {
			height: 30px;
			
			}
		
			QListWidget:item:selected:active {
			background:rgba(0,0,0,20%);
			color: yellow;
			
			}
			QListWidget:item:selected:inactive {
			border:rgba(0,0,0,30%);
			}
			
			
			QMenu{
				font: bold 12px;color:black;background-image:url('1.png');
			}
			
			
		
			""")
			
			ui.list4.setStyleSheet("""QListWidget{
			font: Bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;
			}
		
		
			QListWidget:item:selected:active {
			background:rgba(0,0,0,20%);
			color: yellow;
			
			}
			QListWidget:item:selected:inactive {
			border:rgba(0,0,0,30%);
			}
			
			
			QMenu{
				font: bold 12px;color:black;background-image:url('1.png');
			}
			
		
		
			""")
			
			ui.list5.setStyleSheet("""QListWidget{
			font: Bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;
			}
		
		
			QListWidget:item:selected:active {
			background:rgba(0,0,0,20%);
			color: yellow;
			
			}
			QListWidget:item:selected:inactive {
			border:rgba(0,0,0,30%);
			}
			
			
			QMenu{
				font: bold 12px;color:black;background-image:url('1.png');
			}
			
		
		
			""")
			
			ui.list6.setStyleSheet("""QListWidget{
			font: Bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;
			}
		
		
			QListWidget:item:selected:active {
			background:rgba(0,0,0,20%);
			color: yellow;
			
			}
			QListWidget:item:selected:inactive {
			border:rgba(0,0,0,30%);
			}
			
			
			QMenu{
				font: bold 12px;color:black;background-image:url('1.png');
			}
			
		
		
			""")
			
			
			ui.scrollArea.setStyleSheet("""QListWidget{
			font: Bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;
			}
		
		
			QListWidget:item:selected:active {
			background:rgba(0,0,0,20%);
			color: yellow;
			
			}
			QListWidget:item:selected:inactive {
			border:rgba(0,0,0,30%);
			}
			
			
			QMenu{
				font: bold 12px;color:black;background-image:url('1.png');
			}
			
		
		
			""")
			
			ui.scrollArea1.setStyleSheet("""QListWidget{
			font: Bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;
			}
		
		
			QListWidget:item:selected:active {
			background:rgba(0,0,0,20%);
			color: yellow;
			
			}
			QListWidget:item:selected:inactive {
			border:rgba(0,0,0,30%);
			}
			
			
			QMenu{
				font: bold 12px;color:black;background-image:url('1.png');
			}
			
		
		
			""")
			
			if self.list_with_thumbnail:
				ui.list2.setStyleSheet("""QListWidget{font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius:3px;}
				QListWidget:item {height: 112px;}
				QListWidget:item:selected:active {background:rgba(0,0,0,20%);color: violet;}
				QListWidget:item:selected:inactive {border:rgba(0,0,0,30%);}
				QMenu{font: bold 12px;color:black;background-image:url('1.png');}""")
			else:
				ui.list2.setStyleSheet("""QListWidget{font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius:3px;}
				QListWidget:item {height: 30px;}
				QListWidget:item:selected:active {background:rgba(0,0,0,20%);color: violet;}
				QListWidget:item:selected:inactive {border:rgba(0,0,0,30%);}
				QMenu{font: bold 12px;color:black;background-image:url('1.png');}""")
			
			ui.list3.setStyleSheet("""QListWidget{
			font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;
			}
			
			QListWidget:item {
			height: 20px;
			
			}
		
			QListWidget:item:selected:active {
			background:rgba(0,0,0,20%);
			color: violet;
			}
			QListWidget:item:selected:inactive {
			border:rgba(0,0,0,30%);
			}
			QMenu{
				font: bold 12px;color:black;background-image:url('1.png');
			}
			""")
			
			ui.progress.setStyleSheet("""QProgressBar{
			font: bold 12px;
			color:white;
			background:rgba(0,0,0,30%);
			border:rgba(0,0,0,1%) ;
			border-radius: 1px;
			text-align: center;}
			
			QProgressBar:chunk {
			background-color: rgba(255,255,255,30%);
			width: 10px;
			margin: 0.5px;
			}}""")
			
			ui.progressEpn.setStyleSheet("""QProgressBar{
			font: bold 12px;
			color:white;
			background:rgba(0,0,0,30%);
			border:rgba(0,0,0,1%) ;
			border-radius: 1px;
			text-align: center;
			}
			
			QProgressBar:chunk {
			background-color: rgba(255,255,255,30%);
			width: 10px;
			margin: 0.5px;
			}}""")

			ui.btnWebReviews.setStyleSheet("""QComboBox {
			min-height:0px;
			max-height:50px;
			border-radius: 3px;
			font-size:10px;
			padding: 1px 1px 1px 1px;
			font:bold 10px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:white;
			
			
			}

			QComboBox::down-arrow {
			
			width: 2px;
			height: 2px;
			}""")
		
			ui.btn30.setStyleSheet("""QComboBox {
			min-height:20px;
			max-height:63px;
			
			font-size:10px;
			padding: 1px 1px 1px 1px;
			font:bold 10px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:black;
			
			}

			QComboBox::down-arrow {
			
			width: 2px;
			height: 2px;
			}""")

			ui.btn2.setStyleSheet("""QComboBox {
			min-height:20px;
			max-height:63px;
			
			font-size:10px;
			padding: 1px 1px 1px 1px;
			font:bold 10px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:black;
			
			}

			QComboBox::down-arrow {
			
			width: 2px;
			height: 2px;
			}""")

			ui.btn3.setStyleSheet("""QComboBox {
			min-height:20px;
			max-height:63px;
			border-radius: 3px;
			font-size:10px;
			padding: 1px 1px 1px 1px;
			font:bold 10px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:black;
			
			}

			QComboBox::down-arrow {
			
			width: 2px;
			height: 2px;
			}""")
			
			ui.btn10.setStyleSheet("""QComboBox {
			min-height:20px;
			max-height:63px;
			border-radius: 3px;
			font-size:10px;
			padding: 1px 1px 1px 1px;
			font:bold 10px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:black;
			
			}

			QComboBox::down-arrow {
			
			width: 2px;
			height: 2px;
			}""") 
			
			ui.chk.setStyleSheet("""QComboBox {
			min-height:20px;
			max-height:63px;
			
			font-size:9px;
			padding: 1px 1px 1px 1px;
			font:bold 12px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:black;
			
			}

			QComboBox::down-arrow {
			width: 2px;
			height: 2px;
			}""") 

			ui.comboBox20.setStyleSheet("""QComboBox {
			min-height:20px;
			max-height:63px;
			border-radius: 3px;
			font-size:10px;
			padding: 1px 1px 1px 1px;
			font:bold 10px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:black;
			
			}

			QComboBox::down-arrow {
			
			width: 2px;
			height: 2px;
			}""")

			ui.comboBox30.setStyleSheet("""QComboBox {
			min-height:20px;
			max-height:63px;
			border-radius: 3px;
			font-size:10px;
			padding: 1px 1px 1px 1px;
			font:bold 10px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:black;
			
			}

			QComboBox::down-arrow {
			
			width: 2px;
			height: 2px;
			}""")

			ui.btnOpt.setStyleSheet("""QComboBox {
			min-height:20px;
			max-height:63px;
			border-radius: 3px;
			font-size:10px;
			padding: 1px 1px 1px 1px;
			font:bold 10px;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);
			}
			QComboBox::drop-down {
			width: 47px;
			border: 0px;
			color:black;
			
			}

			QComboBox::down-arrow {
			
			width: 2px;
			height: 2px;
			}""")
			
			ui.label_torrent_stop.setStyleSheet("""
			QToolTip {
			font : Bold 10px;
			color: white;
			background:rgba(157,131,131,80%)
			}
				""")
			
			ui.label_down_speed.setStyleSheet("""
			QToolTip {
			font : Bold 10px;
			color: white;
			background:rgba(157,131,131,80%)
			}
				""")
			
			ui.label_up_speed.setStyleSheet("""
			QToolTip {
			font : Bold 10px;
			color: white;
			background:rgba(157,131,131,80%)
			}""")
		else:
			if widget == ui.list2:
				if self.list_with_thumbnail:
					ui.list2.setStyleSheet("""QListWidget{font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius:3px;}
					QListWidget:item {height: 112px;}
					QListWidget:item:selected:active {background:rgba(0,0,0,20%);color: violet;}
					QListWidget:item:selected:inactive {border:rgba(0,0,0,30%);}
					QMenu{font: bold 12px;color:black;background-image:url('1.png');}""")
				else:
					ui.list2.setStyleSheet("""QListWidget{font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius:3px;}
					QListWidget:item {height: 30px;}
					QListWidget:item:selected:active {background:rgba(0,0,0,20%);color: violet;}
					QListWidget:item:selected:inactive {border:rgba(0,0,0,30%);}
					QMenu{font: bold 12px;color:black;background-image:url('1.png');}""")
		

	def setPlayerFocus(self):
		global player_focus
		player_focus = 1 - player_focus
		if player_focus == 1:
			self.tab_5.show()
			#self.frame1.show()
			self.tab_5.setFocus()
			self.list1.hide()
			self.label.hide()
			self.text.hide()
			self.frame.hide()
			if not self.tab_6.isHidden():
				self.list2.hide()
				self.goto_epn.hide()
		else:
			self.tab_5.hide()
			#self.frame1.hide()
			self.list1.show()
			self.list2.show()
			self.text.show()
			self.label.show()
			#self.frame.show()
			#self.goto_epn.show()
			self.list1.setFocus()
	def PlayEpn(self):
		
		global name,epn,direct_epn_browser,opt,browse_cnt,curR
		
		val = self.btnEpnList.currentIndex()
		print ("val="+str(val))
		if val > 0:
			epn = str(self.btnEpnList.currentText())
			print (epn)
			direct_epn_browser=1
			val = val-1
			curR = val
			self.list2.setCurrentRow(val)
			self.epnfound()
	def go_opt_options_btn20(self):
	
		global site,home,opt,browse_cnt
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,label_arr
		j=0
		opt = str(self.comboBox30.currentText())
		print (opt)
		
		for index in range(self.list3.count()):
			k=str(self.list3.item(index).text())
			if k == opt:
				self.list3.setCurrentRow(j)
				print (k)
				print (self.list3.currentItem().text())
				break
			j = j+1
		self.options('Nill')
	
	
		pict_arr[:]=[]
		name_arr[:]=[]
		summary_arr[:]=[]
		#total_till=0
	
		i = 0
		while(i<total_till):
			t = "self.label_"+str(i)+".close()"
			exec (t)
			print (str(i)+" cleared")
			i = i+1
	
		total_till=0	
		label_arr[:]=[]
		browse_cnt=0
		if opt == "History":
			self.setPreOpt()
			self.next_page('deleted')
		elif opt == "Random":
			self.shuffleList()
			self.next_page('deleted')
		else:
			self.next_page('deleted')
	
	def go_opt_options(self):
		global site,opt
		j=0
		opt = str(self.btnOpt.currentText())
		for index in range(self.list3.count()):
			k=str(self.list3.item(index).text())
			if k == opt:
				self.list3.setCurrentRow(j)
				break
			j = j+1
		self.options('Nill')
	
	def load_more(self,value):
		global browse_cnt,opt,labelGeometry
		#val1 = 256*((browse_cnt/3))+1
		val1 = labelGeometry
		#if value > val1 and browse_cnt > 0 and value < self.scrollArea.verticalScrollBar().maximum() and opt!= "History":
		#if value == self.scrollArea.verticalScrollBar().maximum():
		#	self.next_page('load_more')
	def browse_epn(self):
		global name,epn,direct_epn_browser,opt,browse_cnt,curR
		if opt=="History":
			self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().minimum())
			#print self.scrollArea.verticalScrollBar().maximum()
		else:
			val=self.scrollArea.verticalScrollBar().minimum()
			"""
			val1 = 256
			val2= (browse_cnt/3)-1
			val = val1*val2
			"""
			self.scrollArea.verticalScrollBar().setValue(val)
			
		
		val = self.btn10.currentIndex()
		print ("val="+str(val))
		if val > 0:
			epn = str(self.btn10.currentText())
			print (epn)
			direct_epn_browser=1
			val = val-1
			curR = val
			self.list2.setCurrentRow(val)
			self.epnfound()
			self.tab_6.hide()
			
	def browserView_view(self):
		global site,home,opt,browse_cnt
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,label_arr,list1_items
		pict_arr[:]=[]
		name_arr[:]=[]
		summary_arr[:]=[]
		#total_till=0
		
		if site == "SubbedAnime" or site == "DubbedAnime":
			j=0
			t = str(self.comboBox30.currentText())
			for index in range(self.list3.count()):
				k=str(self.list3.item(index).text())
				if k == t:
					self.list3.setCurrentRow(j)
					break
				j = j+1
		opt1 = ""
		opt1 = str(self.comboBox20.currentText())
		print (total_till)
		i = 0
		while(i<total_till):
			t = "self.label_"+str(i)+".close()"
			exec (t)
			#print str(i)+" cleared"
			i = i+1
	
		total_till=0	
		label_arr[:]=[]
		browse_cnt=0
		tmp_name[:]=[]
		#list1_items[:]=[]
	
		if opt1 == "History":
			#opt = "History"
			self.setPreOpt()
			self.next_page('deleted')
		elif opt1 == "Random" or opt1 == "List":
			#self.shuffleList()
			#opt = "Random"
			self.next_page('deleted')
			
		#self.comboBox20.setCurrentIndex(0)	
	def browserView(self):
		global site,home,opt,browse_cnt
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,label_arr,list1_items,thumbnail_indicator
		pict_arr[:]=[]
		name_arr[:]=[]
		summary_arr[:]=[]
		#total_till=0
		self.scrollArea1.hide()
		self.scrollArea.show()
		#self.horizontalLayout10.insertWidget(1,self.btn20, 0)
		if site == "SubbedAnime" or site == "DubbedAnime":
			j=0
			t = str(self.comboBox30.currentText())
			for index in range(self.list3.count()):
				k=str(self.list3.item(index).text())
				if k == t:
					self.list3.setCurrentRow(j)
					break
				j = j+1
		opt1 = ""
		opt1 = str(self.comboBox20.currentText())
		print (total_till)
		i = 0
		thumbnail_indicator[:]=[]
		while(i<total_till):
			t = "self.label_"+str(i)+".deleteLater()"
			#t1 = "self.label_"+str(i)+".setParent(None)"
			#t2 = "self.label_"+str(i)+".deleteLater()"
			#t1 = "self.label_"+str(i)+".destroy()"
			exec (t)
			#exec t1
			#exec t2
			#exec t1
			#print str(i)+" cleared"
			i = i+1
	
		total_till=0	
		label_arr[:]=[]
		browse_cnt=0
		tmp_name[:]=[]
		#list1_items[:]=[]
	
		if opt == "History":
			#opt = "History"
			self.setPreOpt()
			self.next_page()
		else:
			#self.shuffleList()
			#opt = "Random"
			self.next_page()
			
		#self.comboBox20.setCurrentIndex(0)	
	def display_image(self,br_cnt,br_cnt_opt):
		global site,name,base_url,name1,embed,opt,pre_opt,mirrorNo,list1_items,list2_items,quality,row_history,home,epn,iconv_r,tab_6_size_indicator,labelGeometry,original_path_name,video_local_stream
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,label_arr,hist_arr,bookmark,status,thumbnail_indicator,icon_size_arr,siteName,category,finalUrlFound,refererNeeded,epnArrList
		browse_cnt = br_cnt
		#if br_cnt_opt == 'image':
		name=tmp_name[browse_cnt]
		length = len(tmp_name)
		m =[]
		if bookmark == "True" and os.path.exists(os.path.join(home,'Bookmark',status+'.txt')):
				#tmp = site+':'+opt+':'+pre_opt+':'+base_url+':'+str(embed)+':'+name
				file_name = os.path.join(home,'Bookmark',status+'.txt')
				#f = open(os.path.join(home,'Bookmark',status+'.txt'),'r')
				#line_a = f.readlines()
				#f.close()
				line_a = open_files(file_name,True)
				#r = self.list1.currentRow()
				
				
				tmp = line_a[browse_cnt]
				tmp = re.sub('\n','',tmp)
				tmp1 = tmp.split(':')
				site = tmp1[0]
				if site == "Music" or site == "Video":
					opt = "Not Defined"
					if site == "Music":
						music_opt = tmp1[1]
					else:
						video_opt = tmp1[1]
				else:
					opt = tmp1[1]
				pre_opt = tmp1[2]
				siteName = tmp1[2]
				base_url = int(tmp1[3])
				embed = int(tmp1[4])
				name = tmp1[5]
				
					
				#tmp_name.append(name)
				#original_path_name.append(name)
				
				print (name)
				if len(tmp1) > 6:
					if tmp1[6] == "True":
						finalUrlFound = True
					else:
						finalUrlFound = False
					if tmp1[7] == "True":
						refererNeeded = True
					else:
						refererNeeded = False
					if len(tmp1) >= 9:
						if tmp1[8] == "True":
							video_local_stream = True
						else:
							video_local_stream = False
					print (finalUrlFound)
					print (refererNeeded)
					print (video_local_stream)
				else:
					refererNeeded = False
					finalUrlFound = False
					video_local_stream = False
				print (site + ":"+opt)
		
		label_arr.append(name)
		label_arr.append(name)
		
		
		if (site == "Local") and opt !="History":
				m = []
				
				name=original_path_name[browse_cnt]
				#name = name.split('/')[-1]
				#path = home+'/Local/'+name
				#print path
				if os.path.exists(os.path.join(home,'Local',name)):
					if os.path.exists(os.path.join(home,'Local',name,'Ep.txt')):
						#f = open(os.path.join(home,'Local',name,'Ep.txt'),'r')
						#lines = f.readlines()
						#f.close()
						lines = open_files(os.path.join(home,'Local',name,'Ep.txt'),True)
						for i in lines:
							#j = re.sub('\n','',i)
							#k = j .split('/')[-1]
							j = i.strip()
							k = os.path.basename(j)
							m.append(k)
					picn = os.path.join(home,'Local',name,'poster.jpg')
					 
					m.append(picn)
					if os.path.exists(os.path.join(home,'Local',name,'summary.txt')):
						#g = open(os.path.join(home,'Local',name,'summary.txt'), 'r')
						#summary = g.read()
						summary = open_files(os.path.join(home,'Local',name,'summary.txt'),False)
						m.append(summary)
						#g.close()
					else:
						m.append("Summary Not Available")
					#print m
		elif site == "Video":
			
					picn = os.path.join(home,'Local',name,'poster.jpg')
					 
					m.append(picn)
					if os.path.exists(os.path.join(home,'Local',name,'summary.txt')):
						#g = open(os.path.join(home,'Local',name,'summary.txt'), 'r')
						#summary = g.read()
						summary = open_files(os.path.join(home,'Local',name,'summary.txt'),False)
						m.append(summary)
						#g.close()
					else:
						m.append("Summary Not Available")
					#print (m)
		elif site == "Music":
					#if str(self.list3.currentItem().text()) != "Artist":
					#	name = epnArrList[browse_cnt].split('	')[2]
						
					picn = os.path.join(home,'Music','Artist',name,'thumbnail.jpg')
					m.append(picn)
					if os.path.exists(os.path.join(home,'Music','Artist',name,'bio.txt')):
						#g = open(os.path.join(home,'Music','Artist',name,'bio.txt'), 'r')
						#try:
						#	summary = str(g.read())
						#except:
						#	summary = (g.read())
						summary = open_files(os.path.join(home,'Music','Artist',name,'bio.txt'),False)
						m.append(summary)
						#g.close()
					else:
						m.append("Summary Not Available")
					#print (m)
		elif opt == "History":
			
			if site == "SubbedAnime" or site == "DubbedAnime":
				dir_name =os.path.join(home,'History',site,siteName,name)	
				#print dir_name	
			elif site == "Local":
				if bookmark == "False":
					
					name = original_path_name[browse_cnt]
				dir_name =os.path.join(home,'History',site,name)
				
			else:
				dir_name =os.path.join(home,'History',site,name)
				#print dir_name
		
			if os.path.exists(dir_name):
					print (dir_name)
					picn = os.path.join(home,'History',site,name,'poster.jpg')
					thumbnail = os.path.join(home,'History',site,name,'thumbnail.jpg')
					picn = thumbnail
					#if os.path.exists(picn):
					#print picn
					m.append(os.path.join(dir_name,'poster.jpg'))
					# else:
					#	m.append('No.jpg')
					
					try:	
						#if os.path.exists(dir_name+'/summary.txt'):
						#g = open(os.path.join(dir_name,'summary.txt'), 'r')
						#summary = g.read()
						summary = open_files(os.path.join(dir_name,'summary.txt'),False)
						m.append(summary)
						#g.close()
						#else:
						#	m.append("Not Available")
					except:
						m.append("Not Available")
				
			else:
				m.append('No.jpg')
				m.append('Not Available')
			
		try:
			summary = m.pop()
		except:
			summary = "Not Available"
		try:
			picn = m.pop()
		except:
			picn = "No.jpg"
		#pict_arr.append(picn)
		#name_arr.append(name)
		#summary_arr.append(summary)
		if br_cnt_opt == "image":
			if picn != "No.jpg" and os.path.exists(picn):
				#print picn
				img = QtGui.QPixmap(picn, "1")
				q1="self.label_"+str(browse_cnt)+".setPixmap(img)"
				exec (q1)
		
			if site == "Local":
				name1 = name.split('@')[-1]
			else:
				name1 = name
			q3="self.label_"+str(length+browse_cnt)+".setText((name1))"
			exec (q3)
			try:
				sumry = "<html><h1>"+name1+"</h1><head/><body><p>"+summary+"</p>"+"</body></html>"
			except:
				sumry = "<html><h1>"+str(name1)+"</h1><head/><body><p>"+str(summary)+"</p>"+"</body></html>"
			q4="self.label_"+str(length+browse_cnt)+".setToolTip((sumry))"			
			exec (q4)
			p8="self.label_"+str(length+browse_cnt)+".home(True)"
			exec (p8)
			p8="self.label_"+str(length+browse_cnt)+".deselect()"
			exec (p8)
			total_till = total_till+2
			if total_till%(2*iconv_r) == 0:
				QtWidgets.QApplication.processEvents()
		
	def next_page(self,value_str):
			global site,name,base_url,name1,embed,opt,pre_opt,mirrorNo,list1_items,list2_items,quality,row_history,home,epn,iconv_r,tab_6_size_indicator,labelGeometry,original_path_name,total_till
			global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,label_arr,hist_arr,bookmark,status,thumbnail_indicator,icon_size_arr,siteName,category,finalUrlFound,refererNeeded,epnArrList
			
			self.lock_process = True
			#thumbnail_indicator.append("Thumbnail View")
			m=[]
			
			if value_str == "deleted":
				for i in range(total_till):
					t = "self.label_"+str(i)+".clear()"
					exec (t)
					t = "self.label_"+str(i)+".deleteLater()"
					exec (t)
				total_till = 0
		
			if total_till==0 or value_str=="not_deleted":
				
				
				tmp_name[:] = []
				
				for i in range(self.list1.count()):
						txt = str(self.list1.item(i).text())
						tmp_name.append(txt)
					#print tmp_name
				length = len(tmp_name)
				print (tmp_name)
			else:
				#if opt != "History" and opt!= "List" and opt!="Random":
				#	length = 6
					
				if site == "Local" or site == "None" or site == "PlayLists" or site=="Video" or site=="Music" or opt == "History":
					length = self.list1.count()
				
			#self.label_0.clear()
			#self.label_1.clear()
			#self.label_2.clear()
			#self.label_3.clear()
			#self.label_4.clear()
			#self.label_5.clear()
			if iconv_r == 1 and not self.tab_5.isHidden():
				self.tab_6.setMaximumSize(300,10000)
			else:
				self.tab_6.setMaximumSize(10000,10000)
			print ("width="+str(self.tab_6.width()))
			if iconv_r > 1:
				w = float((self.tab_6.width()-60)/iconv_r)
				h = float((9*w)/16)
				if self.tab_5.isHidden() and mpvplayer:
					if mpvplayer.processId() > 0:
						if tab_6_size_indicator:
							l= (tab_6_size_indicator[0]-60)/iconv_r
						else:
							l = self.tab_6.width()-60
						w = float(l)
						h = float((9*w)/16)
			elif iconv_r == 1:
				#w = float(self.tab_6.width()-60)
				w = float(self.tab_6.width()-60)
				h = float((9*w)/16)
			width = str(int(w))
			height = str(int(h))
			if icon_size_arr:
				icon_size_arr[:]=[]
			icon_size_arr.append(width)
			icon_size_arr.append(height)
			#print (len(label_arr))
			print (length)
			print (browse_cnt)
			
		
			if total_till==0 or value_str=="not_deleted":
				i = 0
				j = iconv_r+1
				k = 0
				if opt != "History":
					if site == "Local" or site == "Video" or site == "Music" or site=='PlayLists':
						length = len(tmp_name)
					else:
						length = 100
				if iconv_r == 1:
					j1 = 3
				else:
					j1 = 2*iconv_r
				if total_till == 0:
					value_str = "deleted"
				while(i<length):
					#if not thumbnail_indicator:
					print(value_str,'--value--str--')
					if value_str == "deleted":
						p1="self.label_"+str(i)+" = ExtendedQLabel(self.scrollAreaWidgetContents)"
						p7 = "l_"+str(i)+" = weakref.ref(self.label_"+str(i)+")"
						exec (p1)
						exec (p7)
					#p2="self.label_"+str(i)+".setMaximumSize(QtCore.QSize(300,200))"
					#p3="self.label_"+str(i)+".setMinimumSize(QtCore.QSize(350,250))"
					p2="self.label_"+str(i)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
					p3="self.label_"+str(i)+".setMinimumSize(QtCore.QSize("+width+","+height+"))"
					p4="self.label_"+str(i)+".setScaledContents(True)"
					p5="self.label_"+str(i)+".setObjectName(_fromUtf8("+'"'+"label_"+str(i)+'"'+"))"
					p6="self.gridLayout1.addWidget(self.label_"+str(i)+","+str(j)+","+str(k)+", 1, 1,QtCore.Qt.AlignCenter)"
					
					exec (p2)
					exec (p3)
					exec (p4)
					exec (p5)
					exec (p6)
					
					if value_str == "deleted":
						#p1="self.label_"+str(i)+" = ExtendedQLabel(self.scrollAreaWidgetContents)"
						p1="self.label_"+str(length+i)+" = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)"
						p7 = "l_"+str(length+i)+" = weakref.ref(self.label_"+str(length+i)+")"
						exec (p1)
						exec (p7)
						print ("creating")
					#p2="self.label_"+str(i)+".setMaximumSize(QtCore.QSize(300,200))"
					#p2="self.label_"+str(i)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
					p2="self.label_"+str(length+i)+".setMinimumWidth("+width+")"
					#p3="self.label_"+str(i)+".setMinimumSize(QtCore.QSize(350,250))"
					#p4="self.label_"+str(i)+".setScaledContents(True)"
					p5="self.label_"+str(length+i)+".setObjectName(_fromUtf8("+'"'+"label_"+str(length+i)+'"'+"))"
					p6="self.gridLayout1.addWidget(self.label_"+str(length+i)+","+str(j1)+","+str(k)+", 1, 1,QtCore.Qt.AlignCenter)"
					p8="self.label_"+str(length+i)+".setAlignment(QtCore.Qt.AlignCenter)"
					exec (p2)
					#exec p3
					#exec p4
					exec (p5)
					exec (p6)
					exec (p8)
					
					
					
					
					
					if value_str == "deleted":
						self.display_image(i,"image")
						
					i=i+1
					k = k+1
					
					if k == iconv_r:
						j = j + 2*iconv_r
						j1 = j1+2*iconv_r
						k = 0
			QtWidgets.QApplication.processEvents()
			self.lock_process = False
			#print tmp_name
			
	def thumbnail_label_update(self):
			global epnArrList,total_till,browse_cnt,home,iconv_r,site,thumbnail_indicator,mpvplayer,tab_6_size_indicator,icon_size_arr,finalUrlFound,total_till_epn
			m=[]
			self.scrollArea.hide()
			self.scrollArea1.show()
			#self.horizontalLayout10.insertWidget(2,self.btn20, 0)
			#self.gridLayout2.setSpacing(0)
			#print hist_arr
			if iconv_r == 1 and not self.tab_5.isHidden():
				self.tab_6.setMaximumSize(300,10000)
			else:
				self.tab_6.setMaximumSize(10000,10000)
			print ("width="+str(self.tab_6.width()))
			
			if iconv_r > 1:
				w = float((self.tab_6.width()-60)/iconv_r)
				h = float((9*w)/16)
				if self.tab_5.isHidden() and mpvplayer:
					if mpvplayer.processId() > 0:
						if tab_6_size_indicator:
							l= (tab_6_size_indicator[0]-60)/iconv_r
						else:
							l = self.tab_6.width()-60
						w = float(l)
						h = float((9*w)/16)
			elif iconv_r == 1:
				w = float(self.tab_6.width()-60)
				#w = float(self.tab_6.width())
				h = float((9*w)/16)
			width = str(int(w))
			height = str(int(h))
			print ("self.width="+width)
			print ("self.height="+height)
			if icon_size_arr:
				icon_size_arr[:]=[]
			icon_size_arr.append(width)
			icon_size_arr.append(height)
			if not thumbnail_indicator:
				thumbnail_indicator.append("Thumbnail View")
			length = self.list2.count()
		
			if total_till_epn > 0:
				i = 0
				#j = 5
				j = iconv_r+1
				k = 0
			
				while(i<length):
					
					p2="self.label_epn_"+str(i)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
					p3="self.label_epn_"+str(i)+".setMinimumSize(QtCore.QSize("+width+","+height+"))"
					#p3="self.label_"+str(i)+".setMouseTracking(True)"
					p4="self.label_epn_"+str(i)+".setScaledContents(True)"
					p5="self.label_epn_"+str(i)+".setObjectName(_fromUtf8("+'"'+"label_epn_"+str(i)+'"'+"))"
					p6="self.gridLayout2.addWidget(self.label_epn_"+str(i)+","+str(j)+","+str(k)+", 1, 1,QtCore.Qt.AlignCenter)"
					
					exec (p2)
					exec (p3)
					exec (p4)
					exec (p5)
					exec (p6)
					i=i+1
					k = k+1
					#if k == 4:
					if k == iconv_r:
						#j = j+8
						j = j + 2*iconv_r
						k = 0
			
			
				length1 = 2*length
				i = length
				#j = 8
				if iconv_r == 1:
					j = 3
				else:
					j = 2*iconv_r
				k = 0
			
			
			
				while(i<length1):
					
					#p2="self.label_"+str(i)+".setMaximumSize(QtCore.QSize(300,200))"
					#p2="self.label_"+str(i)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
					p2="self.label_epn_"+str(i)+".setMinimumWidth("+width+")"
					#p3="self.label_"+str(i)+".setMaximumSize(QtCore.QSize(300,200))"
					#p3="self.label_"+str(i)+".setMinimumSize(QtCore.QSize(350,250))"
					#p4="self.label_"+str(i)+".setScaledContents(True)"
					p5="self.label_epn_"+str(i)+".setObjectName(_fromUtf8("+'"'+"label_epn_"+str(i)+'"'+"))"
					p6="self.gridLayout2.addWidget(self.label_epn_"+str(i)+","+str(j)+","+str(k)+", 1, 1,QtCore.Qt.AlignCenter)"
					
					exec (p2)
					#exec p3
					#exec p4
					exec (p5)
					exec (p6)
					
					i=i+1
					k = k+1
					#if k == 4:
					if k == iconv_r:
						#j = j+8
						j = j+2*iconv_r
						k = 0
				total_till_epn = length1
			
				
		
			print (browse_cnt)
			print (length)
			#print tmp_name
			
	def thumbnail_label_update_epn(self):
			global epnArrList,total_till,browse_cnt,home,iconv_r,site,thumbnail_indicator,mpvplayer,tab_6_size_indicator,icon_size_arr,finalUrlFound,total_till_epn
			m=[]
			self.scrollArea.hide()
			self.scrollArea1.show()
			#self.horizontalLayout10.insertWidget(2,self.btn20, 0)
			#self.gridLayout2.setSpacing(0)
			#print hist_arr
			if iconv_r == 1 and not self.tab_5.isHidden():
				self.tab_6.setMaximumSize(300,10000)
			else:
				self.tab_6.setMaximumSize(10000,10000)
			print ("width="+str(self.tab_6.width()))
			
			if iconv_r > 1:
				w = float((self.tab_6.width()-60)/iconv_r)
				h = float((9*w)/16)
				if self.tab_5.isHidden() and mpvplayer:
					if mpvplayer.processId() > 0:
						if tab_6_size_indicator:
							l= (tab_6_size_indicator[0]-60)/iconv_r
						else:
							l = self.tab_6.width()-60
						w = float(l)
						h = float((9*w)/16)
			elif iconv_r == 1:
				w = float(self.tab_6.width()-60)
				#w = float(self.tab_6.width())
				h = float((9*w)/16)
			width = str(int(w))
			height = str(int(h))
			print ("self.width="+width)
			print ("self.height="+height)
			if icon_size_arr:
				icon_size_arr[:]=[]
			icon_size_arr.append(width)
			icon_size_arr.append(height)
			if not thumbnail_indicator:
				thumbnail_indicator.append("Thumbnail View")
			length = self.list2.count()
		
			if total_till_epn > 0:
				i = 0
				#j = 5
				j = iconv_r+1
				k = 0
			
				while(i<length):
					
					p2="self.label_epn_"+str(i)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
					p3="self.label_epn_"+str(i)+".setMinimumSize(QtCore.QSize("+width+","+height+"))"
					#p3="self.label_"+str(i)+".setMouseTracking(True)"
					p4="self.label_epn_"+str(i)+".setScaledContents(True)"
					p5="self.label_epn_"+str(i)+".setObjectName(_fromUtf8("+'"'+"label_epn_"+str(i)+'"'+"))"
					p6="self.gridLayout2.addWidget(self.label_epn_"+str(i)+","+str(j)+","+str(k)+", 1, 1,QtCore.Qt.AlignCenter)"
					
					exec (p2)
					exec (p3)
					exec (p4)
					exec (p5)
					exec (p6)
					i=i+1
					k = k+1
					#if k == 4:
					
					if k == iconv_r:
						#j = j+8
						j = j + 2*iconv_r
						k = 0
			
			
				length1 = 2*length
				i = length
				#j = 8
				if iconv_r == 1:
					j = 3
				else:
					j = 2*iconv_r
				k = 0
			
			
				#QtWidgets.QApplication.processEvents()
				while(i<length1):
					
					#p2="self.label_"+str(i)+".setMaximumSize(QtCore.QSize(300,200))"
					#p2="self.label_"+str(i)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
					p2="self.label_epn_"+str(i)+".setMinimumWidth("+width+")"
					#p3="self.label_"+str(i)+".setMaximumSize(QtCore.QSize(300,200))"
					#p3="self.label_"+str(i)+".setMinimumSize(QtCore.QSize(350,250))"
					#p4="self.label_"+str(i)+".setScaledContents(True)"
					p5="self.label_epn_"+str(i)+".setObjectName(_fromUtf8("+'"'+"label_epn_"+str(i)+'"'+"))"
					p6="self.gridLayout2.addWidget(self.label_epn_"+str(i)+","+str(j)+","+str(k)+", 1, 1,QtCore.Qt.AlignCenter)"
					
					exec (p2)
					#exec p3
					#exec p4
					exec (p5)
					exec (p6)
					
					i=i+1
					k = k+1
					#if k == 4:
					
					if k == iconv_r:
						#j = j+8
						j = j+2*iconv_r
						k = 0
				total_till_epn = length1
				#QtWidgets.QApplication.processEvents()
				
		
			
	def get_thumbnail_image_path(self,row_cnt,row_string):
		global site,epnArrList,home,name
		picn = ''
		title = row_string.strip()
		path = ''
		if site == "Local" or site=="None" or site == "Music" or site == "Video":
			if '	' in title:
				nameEpn = title.split('	')[0]
				
				path = title.split('	')[1]
			else:
				#nameEpn = title.split('/')[-1]
				nameEpn = os.path.basename(title)
				path = title
			#picn = home+'/thumbnails/'+nameEpn+'.jpg'
			if self.list1.currentItem():
				name_t = self.list1.currentItem().text()
			else:
				name_t = ''
			if self.list3.currentItem():
				if self.list3.currentItem().text() == 'Playlist':
					picnD = os.path.join(home,'thumbnails','PlayLists',name_t)
				else:
					picnD = os.path.join(home,'thumbnails',site,name_t)
			else:
				picnD = os.path.join(home,'thumbnails',site,name_t)
			#print(picnD,'=picnD')
			if not os.path.exists(picnD):
				try:
					os.makedirs(picnD)
				except Exception as e:
					print(e)
					return os.path.join(home,'default.jpg')
			picn = os.path.join(picnD,nameEpn)+'.jpg'
			picn = picn.replace('#','')
			if picn.startswith(self.check_symbol):
				picn = picn[1:]
			path = path.replace('"','')
			
			if site == "Music":
				if os.path.exists(picn):
					if os.stat(picn).st_size == 0:
						art_n =title.split('	')[2]
						pic = os.path.join(home,'Music','Artist',art_n,'poster.jpg')
						if os.path.exists(pic):
							picn = pic
						
		elif site == "PlayLists":
			item = self.list2.item(row_cnt)
			if item:
				
				
				nameEpn = title.split('	')[0]
				nameEpn = str(nameEpn)
				try:
					path = title.split('	')[1]
				except:
					return ''
				#picn = home+'/thumbnails/'+nameEpn+'.jpg'
				playlist_dir = os.path.join(home,'thumbnails','PlayLists')
				if not os.path.exists(playlist_dir):
					try:
						os.makedirs(playlist_dir)
					except Exception as e:
						print(e)
						return os.path.join(home,'default.jpg')
				pl_n = self.list1.currentItem().text()
				playlist_name = os.path.join(playlist_dir,pl_n)
				if not os.path.exists(playlist_name):
					os.makedirs(playlist_name)
				#picnD = home+'/thumbnails/'+name
				picnD = os.path.join(playlist_name,nameEpn)
				#if not os.path.exists(picnD):
				#	os.makedirs(picnD)
				#picn = picnD+'/'+nameEpn+'.jpg'
				picn = picnD+'.jpg'
				picn = picn.replace('#','')
				if picn.startswith(self.check_symbol):
					picn = picn[1:]
				path = path.replace('"','')
				
		else:
			if finalUrlFound == True:
				if '	' in title:
					nameEpn = title.split('	')[0]
				
				else:
					#nameEpn = title.split('/')[-1]
					nameEpn = os.path.basename(title)
				#nameEpn = nameEpn
			else:
				if '	' in title:
					nameEpn = title.split('	')[0]
				
				else:
					#nameEpn = name+'-'+(epnArrList[browse_cnt]).decode('utf8')
					nameEpn = title
				#nameEpn = nameEpn
			#picn = home+'/thumbnails/'+nameEpn+'.jpg'
			picnD = os.path.join(home,'thumbnails',name)
			if not os.path.exists(picnD):
				try:
					os.makedirs(picnD)
				except Exception as e:
					print(e)
					return os.path.join(home,'default.jpg')
			picn = os.path.join(picnD,nameEpn+'.jpg')
			#if not os.path.exists()
			picn = picn.replace('#','')
			if picn.startswith(self.check_symbol):
				picn = picn[1:]
		#if not picn:
		#	picn = os.path.join(home,'default.jpg')
		inter = "10s"
		if (picn and not os.path.exists(picn) and 'http' not in path) or (picn and not os.path.exists(picn) and 'http' in path and 'youtube.com' in path ):
			path = path.replace('"','')
			if 'http' in path and 'youtube.com' in path and '/watch?' in path:
				path = self.create_img_url(path)
			self.threadPoolthumb.append(ThreadingThumbnail(path,picn,inter))
			self.threadPoolthumb[len(self.threadPoolthumb)-1].finished.connect(self.thumbnail_generated)
			length = len(self.threadPoolthumb)
			if length == 1:
				if not self.threadPoolthumb[0].isRunning():
					self.threadPoolthumb[0].start()
		return picn
		
	def thumbnailEpn(self):
		
			global epnArrList,total_till,browse_cnt,home,iconv_r,site,thumbnail_indicator,mpvplayer,tab_6_size_indicator,icon_size_arr,finalUrlFound,home,total_till_epn
			m=[]
			self.scrollArea.hide()
			self.scrollArea1.show()
			#self.horizontalLayout10.insertWidget(2,self.btn20, 0)
			#self.gridLayout2.setSpacing(0)
			#print hist_arr
			if iconv_r == 1 and not self.tab_5.isHidden():
				self.tab_6.setMaximumSize(300,10000)
			else:
				self.tab_6.setMaximumSize(10000,10000)
			print ("width="+str(self.tab_6.width()))
			if iconv_r > 1:
				w = float((self.tab_6.width()-60)/iconv_r)
				h = float((9*w)/16)
				if self.tab_5.isHidden() and mpvplayer:
					if mpvplayer.processId() > 0:
						if tab_6_size_indicator:
							l= (tab_6_size_indicator[0]-60)/iconv_r
						else:
							l = self.tab_6.width()-60
						w = float(l)
						h = float((9*w)/16)
			elif iconv_r == 1:
				w = float(self.tab_6.width()-60)
				#w = float(self.tab_6.width())
				h = float((9*w)/16)
			width = str(int(w))
			height = str(int(h))
			if icon_size_arr:
				icon_size_arr[:]=[]
			icon_size_arr.append(width)
			icon_size_arr.append(height)
			print ("self.width="+width)
			print ("self.height="+height)
			if not thumbnail_indicator:
				thumbnail_indicator.append("Thumbnail View")
			length = self.list2.count()
		
			if total_till_epn==0:
				i = 0
				#j = 5
				j = iconv_r+1
				k = 0
			
				while(i<length):
					p1="self.label_epn_"+str(i)+" = ExtendedQLabelEpn(self.scrollAreaWidgetContents1)"
					p7 = "l_"+str(i)+" = weakref.ref(self.label_epn_"+str(i)+")"
					#p2="self.label_"+str(i)+".setMaximumSize(QtCore.QSize(300,200))"
					#p3="self.label_"+str(i)+".setMinimumSize(QtCore.QSize(300,200))"
					p2="self.label_epn_"+str(i)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
					p3="self.label_epn_"+str(i)+".setMinimumSize(QtCore.QSize("+width+","+height+"))"
					#p3="self.label_"+str(i)+".setMouseTracking(True)"
					p4="self.label_epn_"+str(i)+".setScaledContents(True)"
					p5="self.label_epn_"+str(i)+".setObjectName(_fromUtf8("+'"'+"label_epn_"+str(i)+'"'+"))"
					p6="self.gridLayout2.addWidget(self.label_epn_"+str(i)+","+str(j)+","+str(k)+", 1, 1,QtCore.Qt.AlignCenter)"
					exec (p1)
					exec (p7)
					exec (p2)
					exec (p3)
					exec (p4)
					exec (p5)
					exec (p6)
					i=i+1
					k = k+1
					#if k == 4:
					if k == iconv_r:
						#j = j+8
						j = j + 2*iconv_r
						k = 0
			
			
				length1 = 2*length
				i = length
				#j = 8
				if iconv_r == 1:
					j = 3
				else:
					j = 2*iconv_r
				k = 0
			
			
			
				while(i<length1):
					#p1="self.label_"+str(i)+" = ExtendedQLabelEpn(self.scrollAreaWidgetContents1)"
					p1="self.label_epn_"+str(i)+" = QtWidgets.QLineEdit(self.scrollAreaWidgetContents1)"
					p7 = "l_"+str(i)+" = weakref.ref(self.label_epn_"+str(i)+")"
					#p2="self.label_"+str(i)+".setMaximumSize(QtCore.QSize(300,200))"
					#p2="self.label_"+str(i)+".setMaximumSize(QtCore.QSize("+width+","+height+"))"
					p2="self.label_epn_"+str(i)+".setMinimumWidth("+width+")"
					#p3="self.label_"+str(i)+".setMaximumSize(QtCore.QSize(300,200))"
					#p3="self.label_"+str(i)+".setMinimumSize(QtCore.QSize(350,250))"
					#p4="self.label_"+str(i)+".setScaledContents(True)"
					p5="self.label_epn_"+str(i)+".setObjectName(_fromUtf8("+'"'+"label_epn_"+str(i)+'"'+"))"
					p6="self.gridLayout2.addWidget(self.label_epn_"+str(i)+","+str(j)+","+str(k)+", 1, 1,QtCore.Qt.AlignCenter)"
					p8="self.label_epn_"+str(i)+".setAlignment(QtCore.Qt.AlignCenter)"
					
					exec (p1)
					exec (p7)
					exec (p2)
					#exec p3
					#exec p4
					exec (p5)
					exec (p6)
					exec (p8)
					i=i+1
					k = k+1
					#if k == 4:
					if k == iconv_r:
						#j = j+8
						j = j+2*iconv_r
						k = 0
				total_till_epn = length1
			
				
		
			print ("browse-cnt="+str(browse_cnt))
			print ("length="+str(length))
			#print tmp_name
			while(browse_cnt<length and browse_cnt < len(epnArrList)):
					if site == "Local" or site=="None" or site == "Music" or site == "Video":
						if '	' in epnArrList[browse_cnt]:
							nameEpn = (epnArrList[browse_cnt]).split('	')[0]
							
							path = ((epnArrList[browse_cnt]).split('	')[1])
						else:
							#nameEpn = (epnArrList[browse_cnt]).split('/')[-1]
							nameEpn = os.path.basename(epnArrList[browse_cnt])
							#nameEpn = nameEpn
							path = (epnArrList[browse_cnt])
						#picn = home+'/thumbnails/'+nameEpn+'.jpg'
						if self.list1.currentItem():
							name_t = self.list1.currentItem().text()
						else:
							name_t = ''
						if self.list3.currentItem():
							if self.list3.currentItem().text() == 'Playlist':
								picnD = os.path.join(home,'thumbnails','PlayLists',name_t)
							else:
								picnD = os.path.join(home,'thumbnails',site,name_t)
						else:
							picnD = os.path.join(home,'thumbnails',site,name_t)
						#print(picnD,'=picnD')
						if not os.path.exists(picnD):
							os.makedirs(picnD)
						picn = os.path.join(picnD,nameEpn)+'.jpg'
						picn = picn.replace('#','')
						if picn.startswith(self.check_symbol):
							picn = picn[1:]
						path = path.replace('"','')
						if not os.path.exists(picn) and not path.startswith('http'):
							#subprocess.call(["ffmpegthumbnailer","-i",path,"-o",picn,"-t","10",'-q','10','-s','350'])
							self.generate_thumbnail_method(picn,10,path)
						elif not os.path.exists(picn) and path.startswith('http') and 'youtube.com' in path:
								if '/watch?' in path:
									a = path.split('?')[-1]
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
								try:
									img_url="https://i.ytimg.com/vi/"+d['v']+"/hqdefault.jpg"
									ccurl(img_url+'#'+'-o'+'#'+picn)
								except:
									pass
						if site == "Music":
							if os.path.exists(picn):
								if os.stat(picn).st_size == 0:
									art_n =(epnArrList[browse_cnt]).split('	')[2]
									pic = os.path.join(home,'Music','Artist',art_n,'poster.jpg')
									if os.path.exists(pic):
										picn = pic
									
					elif site == "PlayLists":
						item = self.list2.item(browse_cnt)
						if item:
							
							
							nameEpn = (epnArrList[browse_cnt]).split('	')[0]
							nameEpn = str(nameEpn)
							path = ((epnArrList[browse_cnt]).split('	')[1])
							
							#picn = home+'/thumbnails/'+nameEpn+'.jpg'
							playlist_dir = os.path.join(home,'thumbnails','PlayLists')
							if not os.path.exists(playlist_dir):
								os.makedirs(playlist_dir)
							pl_n = self.list1.currentItem().text()
							playlist_name = os.path.join(playlist_dir,pl_n)
							if not os.path.exists(playlist_name):
								os.makedirs(playlist_name)
							#picnD = home+'/thumbnails/'+name
							picnD = os.path.join(playlist_name,nameEpn)
							#if not os.path.exists(picnD):
							#	os.makedirs(picnD)
							#picn = picnD+'/'+nameEpn+'.jpg'
							picn = picnD+'.jpg'
							picn = picn.replace('#','')
							if picn.startswith(self.check_symbol):
								picn = picn[1:]
							path1 = path.replace('"','')
							if not os.path.exists(picn) and not path1.startswith('http'):
								#subprocess.call(["ffmpegthumbnailer","-i",path1,"-o",picn,"-t","10",'-q','10','-s','350'])
								self.generate_thumbnail_method(picn,10,path1)
							elif not os.path.exists(picn) and path1.startswith('http') and 'youtube.com' in path1:
								if '/watch?' in path1:
									a = path1.split('?')[-1]
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
								try:
									img_url="https://i.ytimg.com/vi/"+d['v']+"/hqdefault.jpg"
									ccurl(img_url+'#'+'-o'+'#'+picn)
								except:
									pass
								
					else:
						if finalUrlFound == True:
							if '	' in epnArrList[browse_cnt]:
								nameEpn = (epnArrList[browse_cnt]).split('	')[0]
							
							else:
								#nameEpn = (epnArrList[browse_cnt]).split('/')[-1]
								nameEpn = os.path.basename(epnArrList[browse_cnt])
							nameEpn = nameEpn
						else:
							if '	' in epnArrList[browse_cnt]:
								nameEpn = (epnArrList[browse_cnt]).split('	')[0]
							
							else:
								#nameEpn = name+'-'+(epnArrList[browse_cnt]).decode('utf8')
								nameEpn = (epnArrList[browse_cnt])
							nameEpn = nameEpn
						#picn = home+'/thumbnails/'+nameEpn+'.jpg'
						picnD = os.path.join(home,'thumbnails',name)
						if not os.path.exists(picnD):
							os.makedirs(picnD)
						picn = picnD+'/'+nameEpn+'.jpg'
						#if not os.path.exists()
						picn = picn.replace('#','')
						if picn.startswith(self.check_symbol):
							picn = picn[1:]
						print ()
						#print picn
				
						
					if nameEpn.startswith('#'):
						nameEpn = nameEpn.replace('#',self.check_symbol,1)
					if os.path.exists(picn):
						img = QtGui.QPixmap(picn, "1")
						q1="self.label_epn_"+str(browse_cnt)+".setPixmap(img)"
						exec (q1)
						#t = length
					sumry = "<html><h1>"+nameEpn+"</h1></html>"
					q4="self.label_epn_"+str(length+browse_cnt)+".setToolTip((sumry))"			
					exec (q4)
				
				
					q3="self.label_epn_"+str(length+browse_cnt)+".setText((nameEpn))"
					exec (q3)
					p8="self.label_epn_"+str(length+browse_cnt)+".home(True)"
					exec (p8)
					p8="self.label_epn_"+str(length+browse_cnt)+".deselect()"
					exec (p8)
					QtWidgets.QApplication.processEvents()
					
					
					browse_cnt = browse_cnt+1
				

	def searchAnime(self):
		global fullscrT,idwMain,idw
		
		self.filter_btn_options()
		
	def setCategoryMovie(self):
		global category,site
		category = "Movies" 
	def setCategoryAnime(self):
		global category,site
		category = "Animes" 
	def epnClicked(self):
		global queueNo,mpvAlive,curR
		curR = self.list2.currentRow()
		queueNo = queueNo + 1
		mpvAlive = 0
		self.epnfound()
	
	def mpvNextEpnList(self):
		global mpvplayer,epn,curR,Player,epnArrList,site,current_playing_file_path
		
		if mpvplayer.processId() > 0:
			print ("-----------inside-------")
			if curR == self.list2.count() - 1:
				curR = 0
				if (site == "Music" and not self.playerPlaylist_setLoop_var) or (self.list2.count()==1):
					r1 = self.list1.currentRow()
					it1 = self.list1.item(r1)
					if it1:
						if r1 < self.list1.count():
							r2 = r1+1
						else:
							r2 = 0
						self.list1.setCurrentRow(r2)
						self.listfound()
			else:
				curR = curR + 1

			self.list2.setCurrentRow(curR)
			if site != "PlayLists" and not self.queue_url_list:
				try:
					if '	' in epnArrList[curR]:
						epn = epnArrList[curR].split('	')[1]
					else:
						epn = self.list2.currentItem().text()
					epn = epn.replace('#','')
					if epn.startswith(self.check_symbol):
						epn = epn[1:]
				except:
					pass
			
			if site == "Local" or site == "Music" or site == "Video" or site == "None" or site == "PlayLists":
				if (current_playing_file_path.startswith('http') or current_playing_file_path.startswith('"http')):
					mpvplayer.kill()
					if Player == 'mplayer':
						if mpvplayer.processId() > 0:
							try:
								subprocess.Popen(['killall','mplayer'])
							except:
								pass
					del mpvplayer
					mpvplayer = QtCore.QProcess()
					
				if len(self.queue_url_list)>0:
					self.getQueueInList()
				else:
					self.localGetInList()
			else:
				if Player == "mpv":
					mpvplayer.kill()
					del mpvplayer
					mpvplayer = QtCore.QProcess()
					self.getNextInList()
				else:
					print(mpvplayer.state())
					mpvplayer.kill()
					if mpvplayer.processId() > 0:
						try:
							subprocess.call(['killall','mplayer'])
						except:
							pass
					del mpvplayer
					mpvplayer = QtCore.QProcess()
					print (mpvplayer.processId(),'--mpvnext---')
					
					self.getNextInList()
	
	def mpvPrevEpnList(self):
		#global mpvplayer,epn,curR
		global mpvplayer,epn,curR,Player,epnArrList,site,current_playing_file_path
		
		if mpvplayer.processId() > 0:
			print ("inside")
			
			if curR == 0:
				curR = self.list2.count() - 1
				if (site == "Music" and not self.playerPlaylist_setLoop_var) or (self.list2.count() == 1):
					r1 = self.list1.currentRow()
					it1 = self.list1.item(r1)
					if it1:
						if r1 > 0:
							r2 = r1-1
						else:
							r2 = self.list2.count()-1
						self.list1.setCurrentRow(r2)
						self.listfound()
						curR = self.list2.count() - 1
			else:
				curR = curR - 1
			self.list2.setCurrentRow(curR)
			if site != "PlayLists" and not self.queue_url_list:
				try:
					if '	' in epnArrList[curR]:
						epn = epnArrList[curR].split('	')[1]
					else:
						epn = self.list2.currentItem().text()
					epn = epn.replace('#','')
					if epn.startswith(self.check_symbol):
						epn = epn[1:]
				except:
					pass
			if site == "Local" or site == "Music" or site == "Video" or site == "None" or site == "PlayLists":
				if (current_playing_file_path.startswith('http') or current_playing_file_path.startswith('"http')):
					mpvplayer.kill()
					if Player == 'mplayer':
						if mpvplayer.processId() > 0:
							try:
								subprocess.Popen(['killall','mplayer'])
							except:
								pass
					del mpvplayer
					mpvplayer = QtCore.QProcess()
					
				if len(self.queue_url_list)>0:
					pass
				else:
					self.localGetInList()
			else:
				if Player == "mpv":
					mpvplayer.kill()
					del mpvplayer
					mpvplayer = QtCore.QProcess()
					self.getNextInList()
				else:
					print(mpvplayer.state())
					mpvplayer.kill()
					if mpvplayer.processId() > 0:
						try:
							subprocess.Popen(['killall','mplayer'])
						except:
							pass
					del mpvplayer
					mpvplayer = QtCore.QProcess()
					print (mpvplayer.processId(),'--mpvnext---')
					
					self.getNextInList()
			
	
	
	def HideEveryThing(self):
		global fullscrT,idwMain,idw,view_layout
		fullscrT = 1 - fullscrT
		#if not self.dockWidget_4.isFloating():
		#		self.dockWidget_4.setFloating(True)
		
		
		
		if fullscrT == 1:
			
			self.tab_2.hide()
			self.tab_6.hide()
			self.list1.hide()
			self.list2.hide()
			self.tab_5.hide()
			self.label.hide()
			self.text.hide()
			self.frame.hide()
			self.dockWidget_3.hide()
			self.tab_6.hide()
			self.tab_2.hide()
			self.goto_epn.hide()
			self.list1.setFocus()
			self.frame1.hide()
		else:
			
			self.list1.show()
			self.list2.show()
			self.label.show()
			self.text.show()
			self.frame.show()
			self.dockWidget_3.show()
			self.goto_epn.show()
			self.list1.setFocus()
			self.frame1.show()
		
	def thumbnailHide(self,context):
		global view_layout,total_till,mpvplayer,browse_cnt,iconv_r,memory_num_arr,thumbnail_indicator,iconv_r_indicator,total_till_epn
		thumbnail_indicator[:]=[]
		memory_num_arr[:]=[]
		i = 0
		if context == "ExtendedQLabel":
			pass
		else:
			if total_till > 0:
				while(i<total_till):
					t = "self.label_"+str(i)+".deleteLater()"
					exec (t)
					i = i+1
			if total_till_epn > 0:
				for i in range(total_till_epn):
					t = "self.label_epn_"+str(i)+".deleteLater()"
					exec (t)
			total_till = 0
			total_till_epn = 0
		if iconv_r_indicator:
			iconv_r = iconv_r_indicator[0]
		else:
			iconv_r = 4
		self.tab_6.setMaximumSize(10000,10000)
		browse_cnt = 0
		self.tab_6.hide()
		#self.tab_6.close()
		self.list1.show()
		self.list2.show()
		self.label.show()
		#self.frame.show()
		self.frame1.show()
		self.text.show()
		#self.goto_epn.show()
		view_layout = "List"
		if mpvplayer:
			if mpvplayer.processId() > 0:
				self.text.hide()
				self.label.hide()
				self.list1.hide()
				self.frame.hide()
				self.tab_5.show()
	def webClose(self):
		global view_layout
		#homeN = home+'/src/default.html'
		#self.web.load(QUrl(homeN))
		#self.gridLayout.addWidget(self.goto_epn, 1, 3, 1, 1)
		self.tmp_web_srch = ''
		try:
			self.web.close()
			self.web.deleteLater()
		except:
			self.web = ''
		self.web = ''
		self.tab_2.hide()
		#self.web.clear()
		#self.web.close()
		
		self.list1.show()
		self.list2.show()
		self.label.show()
		self.text.show()
		#self.frame.show()
		self.frame1.show()
		#self.goto_epn.show()
	def webHide(self):
		global mpvplayer
		if mpvplayer.processId() > 0:
			self.tab_2.hide()
		else:
			self.showHideBrowser()
		
	def togglePlaylist(self):
		if self.list2.isHidden():
			self.list2.show()
			#self.goto_epn.show()
		else:
			self.list2.hide()
			self.goto_epn.hide()
	def dockShowHide(self):
		global fullscr
		if self.dockWidget_3.isHidden():
			self.dockWidget_3.show()
			self.btn1.setFocus()
		else:
			self.dockWidget_3.hide()
			if fullscr == 1:
				self.tab_5.setFocus()
			else:
				self.list1.setFocus()
		
			
	def showHideBrowser(self):
		global fullscrT,idwMain,idw,view_layout
		
		
		if self.tab_2.isHidden():
			self.HideEveryThing()
			self.tab_2.show()
			self.frame1.show()
		else:
			self.tab_6.hide()
			self.tab_2.hide()
			self.list1.show()
			self.list2.show()
			self.label.show()
			self.text.show()
			#self.frame.show()
			self.frame1.show()
			#self.goto_epn.show()
		
		
	def IconView(self):
		global fullscrT,idwMain,idw,total_till,label_arr,browse_cnt,tmp_name,view_layout,thumbnail_indicator,total_till_epn
		#fullscrT = 1 - fullscrT
		#if not self.dockWidget_4.isFloating():
		#		self.dockWidget_4.setFloating(True)
		#total_till=0	
		
		
		thumbnail_indicator[:]=[]
		#fullscrT = 1 - fullscrT
		self.scrollArea1.hide()
		self.scrollArea.show()
		label_arr[:]=[]
		browse_cnt=0
		tmp_name[:]=[]
		num = self.list2.currentRow()
		i = 0
		if total_till > 0:
			while(i<total_till):
				t = "self.label_"+str(i)+".deleteLater()"
		
				exec (t)
		
				i = i+1
		#else:
			total_till = 0
		
		if total_till_epn > 0:
			while(i<total_till_epn):
				t = "self.label_epn_"+str(i)+".deleteLater()"
		
				exec (t)
		
				i = i+1
		#else:
			total_till_epn = 0
		if self.tab_6.isHidden():
			
			self.list1.hide()
			self.list2.hide()
			self.tab_5.hide()
			self.label.hide()
			self.text.hide()
			self.frame.hide()
			self.frame1.hide()
			self.goto_epn.hide()
			self.dockWidget_3.hide()
			
			self.tab_6.show()
			#self.browserView()
			
			self.next_page('deleted')
			
			self.tab_2.hide()
			
			#view_layout = "Thumbnail"
		else:
			self.tab_6.hide()
			self.list1.show()
			self.list2.show()
			self.label.show()
			self.list1.setFocus()
			self.text.show()
			#self.frame.show()
			self.frame1.show()
			#self.goto_epn.show()
			#view_layout = "List"
			
	def IconViewEpn(self):
		global fullscrT,idwMain,idw,total_till,label_arr,browse_cnt,tmp_name,view_layout,mpvplayer,iconv_r,curR,viewMode,thumbnail_indicator,site,total_till_epn
		thumbnail_indicator[:]=[]
		#fullscrT = 1 - fullscrT
		self.scrollArea.hide()
		label_arr[:]=[]
		#browse_cnt=0
		tmp_name[:]=[]
		num = self.list2.currentRow()
		i = 0
		
		if self.tab_6.isHidden() or (viewMode == "Thumbnail" and site == "PlayLists"):
			
			self.list1.hide()
			self.list2.hide()
			self.tab_5.hide()
			self.label.hide()
			self.text.hide()
			self.frame.hide()
			#self.frame1.hide()
			self.goto_epn.hide()
			self.dockWidget_3.hide()
			if mpvplayer.processId()>0:
				self.tab_5.show()
				self.frame1.show()
				iconv_r = 1
				self.gridLayout.addWidget(self.tab_6,0,2,1,1)	
			else:	
				self.gridLayout.addWidget(self.tab_6,0,1,1,1)		
			self.tab_6.show()
			self.thumbnailEpn()
			self.tab_2.hide()
			if mpvplayer:
				if mpvplayer.processId()>0:
					self.scrollArea1.verticalScrollBar().setValue((curR+1)*200+(curR+1)*10)
				else:
					self.scrollArea1.verticalScrollBar().setValue(((num+1)/4)*200+((num+1)/4)*10)
			else:
				self.scrollArea1.verticalScrollBar().setValue(((num+1)/4)*200+((num+1)/4)*10)
		else:
			self.tab_6.hide()
			self.list1.show()
			self.list2.show()
			self.label.show()
			self.list1.setFocus()
			self.text.show()
			#self.frame.show()
			self.frame1.show()
			#self.goto_epn.show()
				
	def textShowHide(self):
		global fullscrT,idwMain,idw
		#fullscrT = 1 - fullscrT
		#if not self.dockWidget_4.isFloating():
		#		self.dockWidget_4.setFloating(True)
		
		
		
		if fullscrT == 1:
			self.text.show()
		else:
			self.text.hide()
	def epnShowHide(self):
		global fullscrT,idwMain,idw,name,curR
		#fullscrT = 1 - fullscrT
		#if not self.dockWidget_4.isFloating():
		#		self.dockWidget_4.setFloating(True)
		
		
		
		if fullscrT == 0:
			self.list2.show()
			#self.goto_epn.show()
			#self.btnEpnList.hide()
			#self.label.setMinimumSize(QtCore.QSize(350, 400))
			self.tab_5.setFocus()
			#self.dockWidget_3.show()
			self.btn1.close()
			#MainWindow.showNormal()
			#MainWindow.showMaximized()
			
			#self.label.setMinimumSize(QtCore.QSize(400, 400))
			self.btn1 = Btn1(self.dockWidgetContents_3)
			self.btn1.setGeometry(QtCore.QRect(20, 55, 130, 31))
			self.btn1.setObjectName(_fromUtf8("btn1"))
			self.btn1.addItem(_fromUtf8(""))
			self.btn1.addItem(_fromUtf8(""))
			self.btn1.addItem(_fromUtf8(""))
			self.btn1.addItem(_fromUtf8(""))
			self.btn1.addItem(_fromUtf8(""))
			self.btn1.addItem(_fromUtf8(""))
			self.btn1.addItem(_fromUtf8(""))
			self.btn1.addItem(_fromUtf8(""))
			self.btn1.addItem(_fromUtf8(""))
			self.btn1.setItemText(0, _translate("MainWindow", "Select", None))
			self.btn1.setItemText(1, _translate("MainWindow", "Animejoy", None))
			self.btn1.setItemText(2, _translate("MainWindow", "Animebam", None))
			self.btn1.setItemText(3, _translate("MainWindow", "AnimePlace", None))
			self.btn1.setItemText(4, _translate("MainWindow", "SubbedAnime", None))
			self.btn1.setItemText(5, _translate("MainWindow", "DubbedAnime", None))
			self.btn1.setItemText(6, _translate("MainWindow", "AnimeHi10", None))
			self.btn1.setItemText(7, _translate("MainWindow", "KissAnime", None))
			self.btn1.setItemText(8, _translate("MainWindow", "KissDrama", None))
			self.btnOpt.hide()
			self.go_opt.hide()
			self.dockWidget_3.show()
			QtCore.QObject.connect(self.btn1, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.ka)
			self.btn1.setFocus()
			self.gridLayout.addWidget(self.list2,0,2,1,1)
			self.btn1.setStyleSheet("font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%)")
			self.buttonStyle()
			#self.horizontalLayout_7.insertWidget(0,self.btn1,0)
			#self.btnOpt.show()
			#self.go_opt.show()
		else:
			self.dockWidget_3.hide()
			#self.list2.hide()
			#self.btnEpnList.show()
			self.goto_epn.hide()
			self.horizontalLayout_7.insertWidget(1,self.btn1,0)
			self.verticalLayout_40.insertWidget(2,self.list2,0)
			self.btnOpt.show()
			self.go_opt.show()
			#self.label.setMinimumSize(QtCore.QSize(350, 400))
			#self.btnEpnList.clear()
			#self.btnEpnList.addItem(_fromUtf8(""))
			#self.btnEpnList.setItemText(0, _translate("MainWindow",name, None))
			self.listfound()
			self.list2.setCurrentRow(0)
			self.buttonStyle()
			
			self.btn1.setFocus()
	def fullscreenToggle(self):
		global fullscrT,idwMain,idw
		fullscrT = 1 - fullscrT
		#if not self.dockWidget_4.isFloating():
		#		self.dockWidget_4.setFloating(True)
		
		#
		#self.btn20.hide()
		if not MainWindow.isFullScreen():
			
			self.dockWidget_4.close()
			self.dockWidget_3.hide()
			MainWindow.showFullScreen()
			#self.tab_5.setFocus()
			#self.label.setMinimumSize(QtCore.QSize(350, 400))
			#self.chk.hide()
			#self.btn9.hide()
			
			#self.tab_5.setParent(0)
			#self.dockWidget_4.showFullScreen()
		else:
			
			
			self.dockWidget_3.show()
			MainWindow.showNormal()
			MainWindow.showMaximized()
			#self.tab_5.setFocus()
			#self.label.setMinimumSize(QtCore.QSize(350, 400))
			#self.chk.show()
			#self.btn9.hide()
			
			
	
	
	def shuffleList(self):
		global list1_items,pre_opt,opt,hdr,base_url,site,embed,base_url,finalUrlFound
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,bookmark,original_path_name
		pict_arr[:]=[]
		name_arr[:]=[]
		summary_arr[:]=[]
		#total_till=0
		browse_cnt=0
		tmp_name[:]=[]
		embed = 0
		n = []
		m = []
		
		
			
		if site == "Music" or site=="Video":
			if original_path_name:
				tmp = original_path_name[0]
				if '/' in tmp:
					p = random.sample(original_path_name,len(original_path_name))
					original_path_name[:]=[]
					original_path_name = p
					
					for i in p:
						if site=="Video":
							m.append(i.split('	')[0])
						else:
							#m.append(i.split('/')[-1])
							m.append(os.path.basename(i))
				else:
					for i in range(self.list1.count()):
						n.append(str(self.list1.item(i).text()))
					m = random.sample(n, len(n))
		
		else:
			m = random.sample(original_path_name,len(original_path_name))
			original_path_name[:]=[]
			original_path_name = m
			
		if m and bookmark == "False": 
			
			#print m
			#list1_items = m
			self.label.clear()
			self.line.clear()
			self.list1.clear()
			self.list2.clear()
			self.text.clear()
			for i in m:
				
				if site == "Local":
					k = i.split('@')[-1]
					i = k
				elif site.lower() == 'video' or site.lower() == 'music':
					pass
				else:
					if '	' in i:
						i = i.split('	')[0]
				self.list1.addItem(i)
		opt = "Random"
		
	def sortList(self):
		global list1_items,pre_opt,opt,hdr,base_url,site,embed,finalUrlFound,original_path_name
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,bookmark
		pict_arr[:]=[]
		name_arr[:]=[]
		summary_arr[:]=[]
		#total_till=0
		browse_cnt=0
		tmp_name[:]=[]
		tmp_arr = []
		embed = 0
		n = []
		m =[]
		if site == "Local":
			m = sorted(original_path_name,key = lambda x: x.split('@')[-1].lower())
			#m.sort()
			original_path_name[:]=[]
			original_path_name = m
		elif site == "Music" or site == "Video":
			if original_path_name:
				tmp = original_path_name[0]
				if '/' in tmp:
					if site == "Video":
						p = sorted(original_path_name,key = lambda x: x.split('	')[0].lower())
					else:
						p = sorted(original_path_name,key = lambda x: os.path.basename(x).lower())
					#m.sort()
					original_path_name[:]=[]
					original_path_name = p
					#print p
					for i in p:
						if site == "Video":
							m.append(i.split('	')[0])
						else:
							#m.append(i.split('/')[-1])
							m.append(os.path.basename(i))
				else:
					for i in range(self.list1.count()):
						n.append(str(self.list1.item(i).text()))
					m = list(set(n))
					m.sort()
		else:
			
			original_path_name.sort()
			m = original_path_name
		
		if m and bookmark == "False":
			
			#list1_items = m
			
			self.label.clear()
			self.line.clear()
			self.list1.clear()
			self.list2.clear()
			self.text.clear()
			for i in m:
				
				if site == "Local":
					k = i.split('@')[-1]
					i = k
				elif site.lower() == 'music' or site.lower() == 'video':
					pass
				else:
					if '	' in i:
						i = i.split('	')[0]
				self.list1.addItem(i)
		opt = "List"
		
	def deleteArtwork(self):
			global name
			#thumb = '/tmp/AnimeWatch/' + name + '.jpg'
			thumb = os.path.join(TMPDIR,name+'.jpg')
			self.label.clear()
			if os.path.isfile(thumb):
					os.remove(thumb)
				
	def copyImg(self):
		global name,site,opt,pre_opt,home,siteName,epnArrList,original_path_name
		print (site)
		print (opt)
		print (pre_opt)
		if '/' in name:
			name = name.replace('/','-')
		#picn = '/tmp/AnimeWatch/'+name+'.jpg'
		picn = os.path.join(TMPDIR,name+'.jpg')
		print (picn,'--copyimg--')
		#if not os.path.isfile(thumbnail):
		if site == "Local":
			r = self.list1.currentRow()
			name = original_path_name[r]
		if not os.path.isfile(picn):
			picn = os.path.join(home,'default.jpg')
		if os.path.isfile(picn) and opt == "History":
			#thumbnail = '/tmp/AnimeWatch/'+name+'thumbnail.jpg'
			#check again
			thumbnail = os.path.join(TMPDIR,name+'-thumbnail.jpg')
			basewidth = 450
			img = Image.open(str(picn))
			wpercent = (basewidth / float(img.size[0]))
			hsize = int((float(img.size[1]) * float(wpercent)))
			
			img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
			img.save(str(thumbnail))
			if site == "SubbedAnime" or site == "DubbedAnime":
				shutil.copy(picn,os.path.join(home,'History',site,siteName,name,'poster.jpg'))
				shutil.copy(picn,os.path.join(home,'History',site,siteName,name,'thumbnail.jpg'))
				ui.videoImage(picn,os.path.join(home,'History',site,siteName,name,'thumbnail.jpg'),os.path.join(home,'History',site,siteName,name,'fanart.jpg'),'')
			else:
				shutil.copy(picn,os.path.join(home,'History',site,name,'poster.jpg'))
				shutil.copy(picn,os.path.join(home,'History',site,name,'thumbnail.jpg'))
				ui.videoImage(picn,os.path.join(home,'History',site,name,'thumbnail.jpg'),os.path.join(home,'History',site,name,'fanart.jpg'),'')
			#self.listfound()
		elif os.path.isfile(picn) and (site == "Local" or site == "Video") and opt != "History":
			#thumbnail = '/tmp/AnimeWatch/'+name+'thumbnail.jpg'
			thumbnail = os.path.join(TMPDIR,name+'-thumbnail.jpg')
			basewidth = 450
			img = Image.open(str(picn))
			wpercent = (basewidth / float(img.size[0]))
			hsize = int((float(img.size[1]) * float(wpercent)))
			
			img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
			img.save(str(thumbnail))	
			shutil.copy(picn,os.path.join(home,'Local',name,'poster.jpg'))
			shutil.copy(picn,os.path.join(home,'Local',name,'thumbnail.jpg'))
			#self.listfound()
			ui.videoImage(picn,os.path.join(home,'Local',name,'thumbnail.jpg'),os.path.join(home,'Local',name,'fanart.jpg'),'')
		elif os.path.isfile(picn) and (site == "Music"):
			if str(self.list3.currentItem().text()) == "Artist":
				nm = name
			else:
				try:
					r = ui.list2.currentRow()
				
					nm = epnArrList[r].split('	')[2]
				except:
					nm = ""
			if nm and os.path.exists(os.path.join(home,'Music','Artist',nm)):
				picn = os.path.join(TMPDIR,nm+'.jpg')
				thumbnail = os.path.join(TMPDIR,nm+'-thumbnail.jpg')
				#picn = '/tmp/AnimeWatch/'+nm+'.jpg'
				#thumbnail = '/tmp/AnimeWatch/'+nm+'-thumbnail.jpg'
				basewidth = 450
				try:
					img = Image.open(str(picn))
					wpercent = (basewidth / float(img.size[0]))
					hsize = int((float(img.size[1]) * float(wpercent)))
					
					img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
					img.save(str(thumbnail))	
					shutil.copy(picn,os.path.join(home,'Music','Artist',nm,'poster.jpg'))
					shutil.copy(picn,os.path.join(home,'Music','Artist',nm,'thumbnail.jpg'))
					ui.videoImage(picn,os.path.join(home,'Music','Artist',nm,'thumbnail.jpg'),os.path.join(home,'Music','Artist',nm,'fanart.jpg'),'')
					#self.listfound()
				except Exception as e:
					print(e,': line 10783')
	
	def copyFanart(self):
		global name,site,opt,pre_opt,home,siteName,original_path_name,screen_height,screen_width
		print (site)
		print (opt)
		print (pre_opt)
		
		if '/' in name:
			name = name.replace('/','-')
			
		#picn = '/tmp/AnimeWatch/'+name+'.jpg'
		picn = os.path.join(TMPDIR,name+'.jpg')
		if site == "Local":
			r = self.list1.currentRow()
			name = original_path_name[r]
		if os.path.isfile(picn) and opt == "History":
			basewidth = screen_width
			img = Image.open(picn)
			wpercent = (basewidth / float(img.size[0]))
			#hsize = int((float(img.size[1]) * float(wpercent)))
			hsize = screen_height
			img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
			img.save(picn)
			if site == "SubbedAnime" or site == "DubbedAnime":
				shutil.copy(picn,os.path.join(home,'History',site,siteName,name,'fanart.jpg'))
				ui.videoImage(picn,os.path.join(home,'History',site,siteName,name,'thumbnail.jpg'),os.path.join(home,'History',site,siteName,name,'fanart.jpg'),'')
			else:
				shutil.copy(picn,os.path.join(home,'History',site,name,'fanart.jpg'))
				ui.videoImage(picn,os.path.join(home,'History',site,name,'thumbnail.jpg'),os.path.join(home,'History',site,name,'fanart.jpg'),'')
		elif os.path.isfile(picn) and (site == "Local" or site == "Video") and opt != "History":
			basewidth = screen_width
			img = Image.open(picn)
			wpercent = (basewidth / float(img.size[0]))
			#hsize = int((float(img.size[1]) * float(wpercent)))
			hsize = screen_height
			img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
			img.save(picn)
			shutil.copy(picn,os.path.join(home,'Local',name,'fanart.jpg'))
			ui.videoImage(picn,os.path.join(home,'Local',name,'thumbnail.jpg'),os.path.join(home,'Local',name,'fanart.jpg'),'')
			#ui.listfound()
		elif (site == "Music"):
			if str(self.list3.currentItem().text()) == "Artist":
					nm = name
			else:
					try:
						r = ui.list2.currentRow()
					
						nm = epnArrList[r].split('	')[2]
					except:
						nm = ""
			if nm and os.path.exists(os.path.join(home,'Music','Artist',nm)):
				#picn = '/tmp/AnimeWatch/'+nm+'.jpg'
				picn = os.path.join(TMPDIR,nm+'.jpg')
				basewidth = screen_width
				img = Image.open(picn)
				wpercent = (basewidth / float(img.size[0]))
				#hsize = int((float(img.size[1]) * float(wpercent)))
				hsize = screen_height
				img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
				img.save(picn)
				shutil.copy(picn,os.path.join(home,'Music','Artist',nm,'fanart.jpg'))
				print(picn,os.path.join(home,'Music','Artist',nm,'fanart.jpg'))
				ui.videoImage(picn,os.path.join(home,'Music','Artist',nm,'thumbnail.jpg'),os.path.join(home,'Music','Artist',nm,'fanart.jpg'),'')
			#ui.listfound()
	def copySummary(self):
		global name,site,opt,pre_opt,home,siteName,original_path_name
		print (site)
		print (opt)
		print (pre_opt)
		sumry = ''
		if site == "Local":
			r = self.list1.currentRow()
			name = str(self.list1.currentItem().text())
		if site == "Music":
			#sumry = '/tmp/AnimeWatch/'+name+'-bio.txt'
			sumry = os.path.join(TMPDIR,name+'-bio.txt')
		else:
			#sumry = '/tmp/AnimeWatch/'+name+'-summary.txt'
			sumry = os.path.join(TMPDIR,name+'-summary.txt')
		if site == "Local":
			r = self.list1.currentRow()
			name = original_path_name[r]
			print(sumry,'---',name,'--copysummary---')
		if os.path.isfile(sumry) and opt == "History":
			if site == "SubbedAnime" or site == "DubbedAnime":
				shutil.copy(sumry,os.path.join(home,'History',site,siteName,name,'summary.txt'))
			else:
				shutil.copy(sumry,os.path.join(home,'History',site,name,'summary.txt'))
		elif os.path.isfile(sumry) and (site == "Local" or site == "Video") and opt != "History":
				shutil.copy(sumry,os.path.join(home,'Local',name,'summary.txt'))
		elif (site == "Music"):
			if str(self.list3.currentItem().text()) == "Artist":
					nm = name
			else:
					try:
						r = ui.list2.currentRow()
					
						nm = epnArrList[r].split('	')[2]
					except:
						nm = ""
			if nm and os.path.exists(os.path.join(home,'Music','Artist',nm)):
				#sumry = '/tmp/AnimeWatch/'+nm+'-bio.txt'
				sumry = os.path.join(TMPDIR,nm+'-bio.txt')
				shutil.copy(sumry,os.path.join(home,'Music','Artist',nm,'bio.txt'))
		if os.path.exists(sumry):
			txt = open_files(sumry,False)
			#txt = open(sumry,'r').read()
			self.text.setText(txt)
	def showImage(self):
		global name
		#thumb = '/tmp/AnimeWatch/' + name + '.jpg'
		thumb = os.path.join(TMPDIR,name+'.jpg')
		print (thumb)
		Image.open(thumb).show()
		#subprocess.Popen(["ristretto",thumb])	
	
			
	def getTvdbEpnInfo(self,url):
		global epnArrList,site,original_path_name,finalUrlFound,hdr,home
		content = ccurl(url)
		soup = BeautifulSoup(content,'lxml')
		m=[]
		link1 = soup.find('div',{'class':'section'})
		link = link1.findAll('td')
		n = []

		for i in range(4,len(link),4):
			j = link[i].find('a').text
			k = link[i+1].find('a').text
			l = link[i+2].text
			p = link[i+3].find('img')
			if p:
				img_lnk = link[i].find('a')['href']
				
				lnk = img_lnk.split('&')
				series_id = lnk[1].split('=')[-1]
				poster_id = lnk[3].split('=')[-1]
				q = "http://thetvdb.com/banners/episodes/"+series_id+'/'+poster_id+'.jpg'
				
			else:
				q = "http:No Image"
			j = j.replace(' ','')
			k = k.replace('/','-')
			k = k.replace(':','-')
			t = j+' '+k+':'+q
			if 'special' in j.lower():
				n.append(t)
			else:
				m.append(t)
		m = m+n
		for i in m:
			print(i)
		
		for i in range(len(epnArrList)):
			if '	' in epnArrList[i]:
				j = epnArrList[i].split('	',1)[1]
				if i < len(m):
					k = m[i].split(':')[0]
				else:
					k = epnArrList[i].split('	',1)[0]
				epnArrList[i]=k+'	'+j
			else:
				j = epnArrList[i]
				if i < len(m):
					k = m[i].split(':')[0]
				else:
					k = epnArrList[i]
				epnArrList[i]=k+'	'+j
		if site=="Video":
			video_db = os.path.join(home,'VideoDB','Video.db')
			conn = sqlite3.connect(video_db)
			cur = conn.cursor()
			for r in range(len(epnArrList)):
				txt = epnArrList[r].split('	')[1]
				ep_name = epnArrList[r].split('	')[0]
				qr = 'Update Video Set EP_NAME=? Where Path=?'
				cur.execute(qr,(ep_name,txt))
			conn.commit()
			conn.close()
		elif opt == "History" or site == "Local":
			if site == "SubbedAnime" or site == "DubbedAnime":
				if os.path.exists(os.path.join(home,'History',site,siteName,name,'Ep.txt')):
					file_path = os.path.join(home,'History',site,siteName,name,'Ep.txt')
			elif site == "Local" and opt != "History":
				r = self.list1.currentRow()
				name1 = original_path_name[r]
				if os.path.exists(os.path.join(home,'Local',site,name1,'Ep.txt')):
					file_path = os.path.join(home,'Local',site,name1,'Ep.txt')
			elif site == "Local" and opt == "History":
				r = self.list1.currentRow()
				name1 = original_path_name[r]
				if os.path.exists(os.path.join(home,'History',site,name1,'Ep.txt')):
					file_path = os.path.join(home,'History',site,name1,'Ep.txt')
			else:
				if os.path.exists(os.path.join(home,'History',site,name,'Ep.txt')):
					file_path = os.path.join(home,'History',site,name,'Ep.txt')
			if os.path.exists(file_path):
				"""
				f = open(file_path,'w')
				#print (epnArrList)
				for r in range(len(epnArrList)):
					t = str(epnArrList[r])
					if r == len(epnArrList)-1:
						f.write(t)
					else:
						f.write(t+'\n')
				f.close()
				"""
				write_files(file_path,epnArrList,line_by_line=True)
		
		self.update_list2()
		
		if not self.downloadWget:
			self.downloadWget[:] = []
			self.downloadWget_cnt = 0
		else:
			running = False
			len_down = len(self.downloadWget)
			for i in range(len_down):
				if self.downloadWget[i].isRunning():
					running = True
					break
			if not running:
				self.downloadWget[:] = []
				self.downloadWget_cnt = 0
			else:
				print('--Thread Already Running--')
				return 0
		if (site != "Local" and site != "Video"):
			for r in range(len(epnArrList)):
				if finalUrlFound == True:
					if '	' in epnArrList[r]:
						newEpn = epnArrList[r].split('	')[0]
					else:
						#newEpn = (epnArrList[r]).split('/')[-1]
						newEpn = os.path.basename(epnArrList[r])
				else:
					if '	' in epnArrList[r]:
						newEpn = epnArrList[r].split('	')[0]
					else:
						newEpn = name+'-'+(epnArrList[r])
				newEpn = str(newEpn)
				newEpn = newEpn.replace('#','')
				if newEpn.startswith(self.check_symbol):
					newEpn = newEpn[1:]
				dest = os.path.join(home,"thumbnails",name,newEpn+'.jpg')
				if r < len(m):
					print(r,m[r])
					img_url= m[r].split(':')[2]
					if img_url.startswith('//'):
						img_url = "http:"+img_url
						command = "wget --user-agent="+'"'+hdr+'" '+'"'+img_url+'"'+" -O "+'"'+dest+'"'
						#self.downloadWget.append(command)
						self.downloadWget.append(downloadThread(img_url+'#'+'-o'+'#'+dest))
						self.downloadWget[len(self.downloadWget)-1].finished.connect(self.download_thread_finished)
						#self.threadPool[len(self.threadPool)-1].start()
					
			if self.downloadWget:
				length = len(self.downloadWget)
				for i in range(5):
					if i < length:
						#self.infoWget(self.downloadWget[i],i)
						self.downloadWget[i].start()
				
	def download_thread_finished(self):
		print ("Process Ended")
		self.downloadWget_cnt = self.downloadWget_cnt+1
		if self.downloadWget_cnt == 5:
			self.downloadWget = self.downloadWget[5:]
			length = len(self.downloadWget)
			self.downloadWget_cnt = 0
			for i in range(5):
				if i < length:
					self.downloadWget[i].start()
	def posterfound(self,nav):
			global name,posterManually,hdr,site,img_arr_artist
			if site == "Music":
				r = self.list3.currentRow()
				item = self.list3.item(r)
				if item:
					
					
						
					if str(self.list3.currentItem().text()) == "Artist":
						nm = str(self.list1.currentItem().text())
					else:
						try:
							r = ui.list2.currentRow()
						
							nm = epnArrList[r].split('	')[2]
						except:
							nm = ""
								
					if nm:	
						if '/' in nm:
							nm = nm.replace('/','-')
						path_name = os.path.join(home,'Music','Artist')
						if not os.path.exists(path_name):
							os.makedirs(path_name)
						art_dir = os.path.join(path_name,nm)
						if not os.path.exists(art_dir):
							os.makedirs(art_dir)
						#tmp_file = '/tmp/AnimeWatch/'+nm+'.txt'
						#if os.path.exists(tmp_file) and not img_arr_artist:
						#	f = open(tmp_file,'r')
						#	lines = f.readlines()
						#	f.close()
						#	for i in lines:
						#		i = i.replace('\n','')
						#		if i:
						#			img_arr_artist.append(i)
						img_arr_artist[:]=[]
						if not img_arr_artist:
							ma = musicArtist()
							if not nav:
								nav = nm
								nav1 = ""
							elif nav.startswith('http'):
								nav1 = nav
								nav = ""
							else:
								nav1 = ""
								nav = nav
							
							img_arr = ma.search(nav,nav1)
							print (img_arr)
							if img_arr:
								wiki = img_arr.pop()
								self.text.clear()
								self.text.lineWrapMode()
								self.text.insertPlainText((wiki))
								#tmp_wiki = '/tmp/AnimeWatch/'+nm+'-bio.txt'
								#thumb = '/tmp/AnimeWatch/' + nm + '.jpg'
								#thumb_list = '/tmp/AnimeWatch/' + nm + '.txt'
								tmp_wiki = os.path.join(TMPDIR,nm+'-bio.txt')
								thumb = os.path.join(TMPDIR,nm+'.jpg')
								thumb_list = os.path.join(TMPDIR,nm+'.txt')
								"""
								f = open(thumb_list,'w')
								for i in img_arr:
									img_arr_artist.append(i)
									f.write(str(i)+'\n')
								f.close()
								"""
								write_files(thumb_list,img_arr,line_by_line=True)
								"""
								f = open(tmp_wiki,'w')
								f.write(str(wiki))
								f.close()
								"""
								write_files(tmp_wiki,wiki,line_by_line=False)
								
								if img_arr_artist:
									url = img_arr_artist[0]
									del img_arr_artist[0]
									try:
										#subprocess.call(["curl","-o",thumb,url])
										ccurl(url+'#'+'-o'+'#'+thumb)
									except:
										#subprocess.call(["curl",'--data-urlencode',"-o",thumb,url])
										pass
									picn = thumb
									self.label.clear()
									if os.path.isfile(picn):
										img = QtGui.QPixmap(picn, "1")
										self.label.setPixmap(img)
						elif img_arr_artist:
							#thumb = '/tmp/AnimeWatch/' + nm + '.jpg'
							thumb = os.path.join(TMPDIR,nm+'.jpg')
							url = img_arr_artist[0]
							del img_arr_artist[0]
							subprocess.call(["curl","-o",thumb,url])
							ccurl(url+'#'+'-o'+'#'+thumb)
							picn = thumb
							self.label.clear()
							if os.path.isfile(picn):
								img = QtGui.QPixmap(picn, "1")
								self.label.setPixmap(img)
			else:
				if site == "Video":
					name = str(self.list1.currentItem().text())
				if nav:
					nam = "url:"+nav
				#fanart = '/tmp/AnimeWatch/' + name + '-fanart.jpg'
				#thumb = '/tmp/AnimeWatch/' + name + '.jpg'
				#fan_text = '/tmp/AnimeWatch/' + name + '-fanart.txt'
				#post_text = '/tmp/AnimeWatch/' + name + '-poster.txt'
				
				fanart = os.path.join(TMPDIR,name+'-fanart.jpg')
				thumb = os.path.join(TMPDIR,name+'.jpg')
				fan_text = os.path.join(TMPDIR,name+'-fanart.txt')
				post_text = os.path.join(TMPDIR,name+'-poster.txt')
				print (fanart)
				print (thumb)
				final_link = ""
				m = []
				if (not os.path.isfile(fan_text) or not os.path.isfile(post_text)):
					if not nav:
						nam = re.sub('Dub|Sub|subbed|dubbed','',name)
						nam = re.sub('-|_|[ ]','+',nam)
						print (nam)
						#if option != "FindAll":
						if posterManually == 1:
							scode, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Input Dialog', 'Enter Name Manually \n or prefix "url:" for direct url \n or "g:" for google Search')
							if ok and scode:
							#scode = subprocess.check_output(["zenity","--entry","--text","Enter Anime Name Manually"])
								scode = str(scode)
								nam = re.sub("\n","",scode)
								nam = nam.replace(' ','+')
								posterManually = 0
								if "g:" in nam:
									na = nam.replace('g:','')
									link = "https://www.google.co.in/search?q="+na+"+site:thetvdb.com"
									print (link)
							else:
								return 0
									
					if "g:" not in nam and 'url:' not in nam:
						link = "http://thetvdb.com/index.php?seriesname="+nam+"&fieldlocation=1&language=7&genre=Animation&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch"
						print (link)
						content = ccurl(link)
						m = re.findall('/index.php[^"]tab=[^"]*',content)
						if not m:
							link = "http://thetvdb.com/index.php?seriesname="+nam+"&fieldlocation=2&language=7&genre=Animation&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch"
							content = ccurl(link)
							m = re.findall('/index.php[^"]tab=[^"]*',content)
							if not m:
								link = "http://thetvdb.com/?string="+nam+"&searchseriesid=&tab=listseries&function=Search"
								content = ccurl(link)
								m = re.findall('/[^"]tab=series[^"]*lid=7',content)
					elif "g:" in nam:
						content = ccurl(link)
						m = re.findall('http://thetvdb.com/[^"]tab=series[^"]*',content)
						print (m)
						if m:
							m[0] = m[0].replace('http://thetvdb.com','')
							m[0] = m[0].replace('amp;','')
					elif "url:" in nam:
						url = nam.replace('url:','')
						if (".jpg" in url or ".png" in url) and "http" in url:
							#picn = "/tmp/AnimeWatch/"+name+".jpg"
							picn = os.path.join(TMPDIR,name+'.jpg')
							if not nav:
								#subprocess.call(["curl","-A",hdr,"-L","-o",picn,url])
								ccurl(url+'#'+'-o'+'#'+picn)
								self.label.clear()
								if os.path.isfile(picn):
									img = QtGui.QPixmap(picn, "1")
									self.label.setPixmap(img)
							else:
								self.videoImage(picn,thumb,fanart,'')
							return 0
						elif "http" in url:
							final_link = url
							print (final_link)
							m.append(final_link)
					if m:
						if not final_link:
						
							n = re.sub('amp;','',m[0])
							elist = re.sub('tab=series','tab=seasonall',n)
							url ="http://thetvdb.com" + n
							print (url)
							elist_url = "http://thetvdb.com" + elist
						else:
							url = final_link
						content = ccurl(url)
						soup = BeautifulSoup(content,'lxml')
						sumry = soup.find('div',{'id':'content'})
						linkLabels = soup.findAll('div',{'id':'content'})
						print (sumry)
						t_sum = re.sub('</h1>','</h1><p>',str(sumry))
						t_sum = re.sub('</div>','</p></div>',str(t_sum))
						soup = BeautifulSoup(t_sum)
						title = (soup.find('h1')).text
						title = re.sub('&amp;','&',title)
						sumr = (soup.find('p')).text
						
						try:
						
							link1 = linkLabels[1].findAll('td',{'id':'labels'})
							print (link1)
							labelId = ""
							for i in link1:
								j = i.text 
								if "Genre" in j:
									k = str(i.findNext('td'))
									
									l = re.findall('>[^<]*',k)
									
									q = ""
									for p in l:
										
										q = q + " "+p.replace('>','')
									k = q 
									
								else:
									k = i.findNext('td').text
									k = re.sub('\n|\t','',k)
								
								labelId = labelId + j +" "+k + '\n'
						except:
							labelId = ""
						#summary = title +"\n\n"+labelId +'\n' + sumr
						summary = title+'\n\n'+labelId+ sumr
						summary = re.sub('\t','',summary)
						sum_file = os.path.join(TMPDIR,name+'-summary.txt')
						"""
						f = open(sum_file,'w')
						f.write(str(summary))
						f.close()
						"""
						write_files(sum_file,summary,line_by_line=False)
						self.text.clear()
						self.text.lineWrapMode()
						self.text.insertPlainText(summary)
						fan_all = re.findall('/[^"]tab=seriesfanart[^"]*',content)
						print (fan_all)
						content1 = ""
						content2 = ""
						post_all = re.findall('/[^"]tab=seriesposters[^"]*',content)
						print (post_all)
						if fan_all:
							url_fan_all = "http://thetvdb.com" + fan_all[0]
							print (url_fan_all)
							content1 = ccurl(url_fan_all)
							m = re.findall('banners/fanart/[^"]*jpg',content1)
							m = list(set(m))
							m.sort()
							length = len(m) - 1
							print (m)
							fanart_text = os.path.join(TMPDIR,name+'-fanart.txt')
							if not os.path.isfile(fanart_text):
								f = open(fanart_text,'w')
								f.write(m[0])
								i = 1
								while(i <= length):
									if not "vignette" in m[i]:
										f.write('\n'+m[i])
									i = i + 1
								f.close()
						else:
							m = re.findall('banners/fanart/[^"]*.jpg',content)
							m = list(set(m))
							m.sort()
							length = len(m) - 1
							print (m)
							fanart_text = os.path.join(TMPDIR,name+'-fanart.txt')
							if not os.path.isfile(fanart_text) and m:
								f = open(fanart_text,'w')
								f.write(m[0])
								i = 1
								while(i <= length):
									if not "vignette" in m[i]:
										f.write('\n'+m[i])
									i = i + 1
								f.close()
						
						if post_all:
							url_post_all = "http://thetvdb.com" + post_all[0]
							print (url_post_all)
							content2 = ccurl(url_post_all)
							r = re.findall('banners/posters/[^"]*jpg',content2)
							r = list(set(r))
							r.sort()
							print (r)
							length = len(r) - 1
							
							poster_text = os.path.join(TMPDIR,name+'-poster.txt')
							
							if not os.path.isfile(poster_text):
								f = open(poster_text,'w')
								f.write(r[0])
								i = 1
								while(i <= length):
									f.write('\n'+r[i])
									i = i + 1
								f.close()
						else:
							r = re.findall('banners/posters/[^"]*.jpg',content)
							r = list(set(r))
							r.sort()
							print (r)
							length = len(r) - 1
							poster_text = os.path.join(TMPDIR,name+'-poster.txt')
							if (r) and (not os.path.isfile(poster_text)):
								f = open(poster_text,'w')
								f.write(r[0])
								i = 1
								while(i <= length):
									f.write('\n'+r[i])
									i = i + 1
								f.close()
						poster_text = os.path.join(TMPDIR,name+'-poster.txt')
						if os.path.isfile(poster_text):
							f = open(poster_text,'r')
							lines=f.readlines()
							print (lines)
							url1 = re.sub('\n|#','',lines[0])
							url = "http://thetvdb.com/" + url1
							#subprocess.call(["curl","-o",thumb,url])
							ccurl(url+'#'+'-o'+'#'+thumb)
							picn = thumb
							self.label.clear()
							if os.path.isfile(picn):
								img = QtGui.QPixmap(picn, "1")
								self.label.setPixmap(img)
							lines[0] = "#" + url1 + '\n'
							f = open(poster_text,'w')
							for i in lines:
								f.write(i)

				else:
					poster_text = os.path.join(TMPDIR,name+'-poster.txt')
					if os.path.isfile(poster_text):
						f = open(poster_text,'r')
						lines =[]
						lines=f.readlines()
						fanart_text = os.path.join(TMPDIR,name+'-fanart.txt')
						if os.path.isfile(fanart_text) and (os.stat(fanart_text).st_size != 0):
							g = open(fanart_text,'r')
							lines1 = g.readlines()
							g.close()
							g = open(fanart_text,'w')
							g.close()
							for i in lines1:
								tmp = '\n'+i
								lines.append(tmp)
						
					
						print (lines)
						f.close()
						length = len(lines)-1
						url = ""
						j = 0
						for i in lines:
							if ('#' in i) or (i == '\n'):
								print ("Hello")
							else:
								url = re.sub('\n','',i)
								url = "http://thetvdb.com/" + url
								lines[j] = "#" + i
								break
							j = j + 1
						if url:
							poster_text = os.path.join(TMPDIR,name+'-poster.txt')
							f = open(poster_text,'w')
							for i in lines:
								f.write(i)
							f.close()
							#subprocess.call(["curl","-o",thumb,url])
							ccurl(url+'#'+'-o'+'#'+thumb)
							picn = thumb
							self.label.clear()
							if os.path.isfile(picn):
								img = QtGui.QPixmap(picn, "1")
								self.label.setPixmap(img)
						
						else:
							poster_text = os.path.join(TMPDIR,name+'-poster.txt')
							f = open(poster_text,'r')
							lines=f.readlines()
							print (lines)
							f.close()
							j = 0
							for i in lines:
								if '#' in i:
									#url = i
									lines[j] = re.sub('#','',i)
								j = j + 1
							f = open(poster_text,'w')
							for i in lines:
								f.write(i)
						
			
	def launchPlayer(self):
		global mpv,indexQueue,Player,startPlayer,site,opt,pre_opt,home,home1
		startPlayer = "Yes"
		#if os.path.isfile(home+'/History/queue.m3u'):
		#	shutil.copy(home+'/History/queue.m3u',home1+'/.kodi/userdata/playlists/video/queue.m3u')
		if startPlayer == "Yes" and Player == "Default":
				if (site == "SubbedAnime" and opt == "Anime-Freak") or (site == "SubbedAnime" and pre_opt == "Anime-Freak" and opt == "History"):
					mpv = subprocess.Popen(['python2', 'mpv.py','empty'], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
				else:
					mpv = subprocess.Popen(['python2', 'mpv.py','notEmpty'], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		elif startPlayer == "Yes":
					subprocess.Popen([Player, os.path.join(home,"History","queue.m3u")], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		#elif startPlayer == "Yes" and Player == "kodi":
		#			subprocess.Popen([Player, home1+"/.kodi/userdata/playlists/video/queue.m3u"], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
				
	
	def chkMirrorTwo(self):
		global site,mirrorNo
		mirrorNo = 2
		if site == "SubbedAnime" or site == "DubbedAnime":
			self.epnfound()
		mirrorNo = 1
			
	def chkMirrorThree(self):
		global site,mirrorNo
		mirrorNo = 3
		if site == "SubbedAnime" or site == "DubbedAnime":
			self.epnfound()
		mirrorNo = 1		
		
	def chkMirrorDefault(self):
		global site,mirrorNo
		mirrorNo = 1
		if site == "SubbedAnime" or site == "DubbedAnime":
			self.epnfound()
			
	def setPreOptList(self):
		global pre_opt,opt,list1_items,site,base_url,embed,mirrorNo,siteName,category
		tmp = str(self.list3.currentItem().text())
		if site == "DubbedAnime":
			if (tmp != "List") or (tmp != "Random") or (tmp != "History"):
				opt = tmp
				code = 2
				pre_opt = tmp
				
				self.label.clear()
				self.line.clear()
				self.list1.clear()
				self.list2.clear()
				self.text.clear()
				
				
				if self.site_var:
					m = self.site_var.getCompleteList(siteName,category,opt) 
				list1_items = m
				original_path_name[:] = []
				for i in m:
					i = i.strip()
					if '	' in i:
						j = i.split(	)[0]
					else:
						j = i
					self.list1.addItem(j)
					original_path_name.append(i)
					
		elif site == "SubbedAnime":
			if (tmp != "List") or (tmp != "Random") or (tmp != "History"):
					code = 7
					opt = tmp
					pre_opt = tmp	
					
					self.label.clear()
					self.line.clear()
					self.list1.clear()
					self.list2.clear()
					self.text.clear()
					
					
					if self.site_var:
						m = self.site_var.getCompleteList(siteName,category,opt) 
					list1_items = m
					for i in m:
						i = i.strip()
						if '	' in i:
							j = i.split(	)[0]
						else:
							j = i
						self.list1.addItem(j)
						original_path_name.append(i)
			
	def setPreOpt(self):
		global pre_opt,opt,hdr,base_url,site,insidePreopt,embed,home,hist_arr,name,bookmark,status,viewMode,total_till,browse_cnt,embed,siteName
		insidePreopt = 1
		hist_arr[:]=[]
		var = (self.btn1.currentText())
		if var == "Select":
			return 0
		if bookmark == "True" and os.path.exists(os.path.join(home,'Bookmark',status+'.txt')):
			opt = "History"
			#f = open(os.path.join(home,'Bookmark',status+'.txt'),'r')
			#line_a = f.readlines()
			#f.close()
			line_a = open_files(os.path.join(home,'Bookmark',status+'.txt'),True)
			self.list1.clear()
			original_path_name[:] = []
			for i in line_a:
				i = i.replace('\n','')
				if i:
					j = i.split(':')
					print (j)
					if j[0] == "Local":
						t = j[5].split('@')[-1]
					else:
						t = j[5]
					if '	' in t:
						t = t.split('	')[0]
					self.list1.addItem(t)
					hist_arr.append(j[5])
					original_path_name.append(j[5])
					
		elif site == "SubbedAnime" or site == "DubbedAnime":
			opt = "History"
			
			self.options('history')	
		else:
			opt = "History"
			
			self.options('history')	
			
		
		        
		        
	def mark_video_list(self,mark_val,row):
		global site,epnArrList
		if site.lower() == "video":
			#row = self.list2.currentRow()
			item = self.list2.item(row)
			if item:
				i = self.list2.item(row).text()
				if mark_val == 'mark' and i.startswith(self.check_symbol):
					pass
				elif mark_val == 'unmark' and not i.startswith(self.check_symbol):
					pass
				elif mark_val == 'mark' and not i.startswith(self.check_symbol):
					#j = self.list2.item(row)
					url1 = epnArrList[row].split('	')[1]
					#self.list2.takeItem(row)
					#del j
					#self.list2.insertItem(row,self.check_symbol+i)
					item.setText(self.check_symbol+i)
					self.updateVideoCount('mark',url1)
				elif mark_val == 'unmark' and i.startswith(self.check_symbol):
					#j = self.list2.item(row)
					url1 = epnArrList[row].split('	')[1]
					#self.list2.takeItem(row)
					#del j
					i = i[1:]
					item.setText(i)
					#self.list2.insertItem(row,i)
					self.updateVideoCount('unmark',url1)
				self.list2.setCurrentRow(row)
				
	def update_playlist_file(self,file_path):
		global epnArrList
		if os.path.exists(file_path):
			"""
			f = open(file_path,'w')
			k = 0
			for i in range(self.list2.count()):
				it = epnArrList[i]
				if k == 0:
					f.write(it)
				else:
					f.write('\n'+it)
				k = k+1
			f.close()
			"""
			write_files(file_path,epnArrList,line_by_line=True)
			
	def mark_playlist(self,mark_val,row):
		global site,epnArrList,home
		music_pl = False
		if site == 'music':
			if self.list3.currentItem():
				if self.list3.currentItem().text().lower() == 'playlist':
					music_pl = True
					
		if site.lower() == "playlists" or music_pl:
			#row = self.list2.currentRow()
			item = self.list2.item(row)
			file_path = os.path.join(home,'Playlists',self.list1.currentItem().text())
			if item:
				i = str(self.list2.item(row).text())
				if mark_val == 'mark' and i.startswith(self.check_symbol):
					pass
				elif mark_val == 'unmark' and not i.startswith(self.check_symbol):
					pass
				elif mark_val == 'mark' and not i.startswith(self.check_symbol):
					#j = self.list2.item(row)
					#self.list2.takeItem(row)
					#del j
					#self.list2.insertItem(row,self.check_symbol+i)
					item.setText(self.check_symbol+i)
					epnArrList[row] = '#'+epnArrList[row]
					self.list2.setCurrentRow(row)
					self.update_playlist_file(file_path)
				elif mark_val == 'unmark' and i.startswith(self.check_symbol):
					#j = self.list2.item(row)
					#self.list2.takeItem(row)
					#del j
					i = i[1:]
					#self.list2.insertItem(row,i)
					item.setText(i)
					epnArrList[row] = epnArrList[row].replace('#','')
					self.list2.setCurrentRow(row)
					self.update_playlist_file(file_path)
					
	def get_local_file_ep_name(self):
		global site,name,siteName
		file_path = ''
		if site.lower() == "local":
			file_path = os.path.join(home,'History',site,name,'Ep.txt')
		elif site.lower() == 'subbedanime' or site.lower() == 'dubbedanime':
			file_path = os.path.join(home,'History',site,siteName,name,'Ep.txt')
		elif site.lower() == 'playlists' and self.list1.currentItem():
			file_path = os.path.join(home,'Playlists',self.list1.currentItem().text())
		elif site.lower() == 'music' and self.list3.currentItem():
			if self.list1.currentItem():
				file_path = os.path.join(home,'Playlists',self.list1.currentItem().text())
		elif site.lower() != 'video':
			file_path = os.path.join(home,'History',site,name,'Ep.txt')
		return file_path
		
	def mark_addons_history_list(self,mark_val,row):
		global opt,site,epnArrList,home,site,name,siteName,finalUrlFound,refererNeeded,path_Local_Dir
		if opt == "History" and (site.lower() !="video" and site.lower()!= 'music' and site.lower()!= 'playlists' and site.lower()!= 'none'):
			file_change = False
			#row = self.list2.currentRow()
			item = self.list2.item(row)
			if item:
				if '	' in epnArrList[row]:
					if epnArrList[row].startswith('#') and mark_val == 'unmark':
						n_epn = epnArrList[row].replace('#','')
					elif not epnArrList[row].startswith('#') and mark_val == 'mark':
						n_epn = '#'+epnArrList[row]
					else:
						return 0
			
				else:
					epn = epnArrList[row]
					if site != "Local":
						if epn.startswith('#') and mark_val == 'unmark':
							n_epn = epn[1:]
							epn = epn
						elif not epn.startswith('#') and mark_val == 'mark':
							n_epn = '#' + epn
							epn = epn
						else:
							return 0
					else:
						if epn.startswith('#') and mark_val == 'unmark':
							n_epnt = epn[1:]
							n_epn = ((epnArrList[row])).replace('#','')
						elif not epn.startswith('#') and mark_val == 'mark':
							n_epnt = epn
							n_epn = '#' + epnArrList[row]
						else:
							return 0
						epn = n_epnt
						
				file_path = self.get_local_file_ep_name()
				
				txt = item.text()
				#j = self.list2.item(row)
				#self.list2.takeItem(row)
				#del j
				
				if txt.startswith(self.check_symbol) and mark_val == 'unmark':
					txt = txt[1:]
					#self.list2.insertItem(row,txt)
					self.list2.item(row).setText(txt)
					file_change = True
				elif not txt.startswith(self.check_symbol) and mark_val == 'mark':
					#self.list2.insertItem(row,self.check_symbol+txt)
					self.list2.item(row).setText(self.check_symbol+txt)
					file_change = True
					
				if os.path.exists(file_path) and file_change:
					#f = open(file_path, 'r')
					#lines = f.readlines()
					#f.close()
					lines = open_files(file_path,True)
					if finalUrlFound == True:
						if lines[row].startswith('#') and mark_val == 'unmark':
							lines[row]=lines[row].replace('#','')
						elif not lines[row].startswith('#') and mark_val == 'mark':
							lines[row] = '#'+lines[row]
					else:
						if "\n" in lines[row]:
							lines[row] = n_epn + "\n"
							print (lines[row])
						else:
							lines[row] = n_epn
					
					epnArrList[:]=[]
					#f = open(file_path, 'w')
					for i in lines:
						#f.write(i)
						i = i.strip()
						epnArrList.append(i)
					#replace_line(file_path,epn,n_epn)
					#f.close()
					write_files(file_path,lines,line_by_line=True)
				self.list2.setCurrentRow(row)
		
		
	def watchToggle(self):
		global site,base_url,embed,epn,epn_goto,pre_opt,home,path_Local_Dir,epnArrList,opt,siteName,finalUrlFound,refererNeeded
		if opt == "History" and (site.lower() !="video" and site.lower()!= 'music' and site.lower()!= 'playlists' and site.lower()!= 'none'):
				row = self.list2.currentRow()
				item = self.list2.item(row)
				if item:
					i = (self.list2.item(row).text())
					if i.startswith(self.check_symbol):
						self.mark_addons_history_list('unmark',row)
					else:
						self.mark_addons_history_list('mark',row)
		elif site.lower() == "playlists":
			row = self.list2.currentRow()
			item = self.list2.item(row)
			if item:
				i = self.list2.item(row).text()
				if i.startswith(self.check_symbol):
					self.mark_playlist('unmark',row)
				else:
					self.mark_playlist('mark',row)
		elif site.lower() == "video":
			row = self.list2.currentRow()
			item = self.list2.item(row)
			if item:
				i = self.list2.item(row).text()
				if i.startswith(self.check_symbol):
					self.mark_video_list('unmark',row)
				else:
					self.mark_video_list('mark',row)
				
	def search_list4_options(self):
		global opt,site,name,base_url,name1,embed,pre_opt,bookmark,base_url_picn,base_url_summary
		#self.text.show()
		r = self.list4.currentRow()
		item = self.list4.item(r)
		if item:
			tmp = str(self.list4.currentItem().text())
			tmp1 = tmp.split(':')[0]
			num = int(tmp1)
			self.list1.setCurrentRow(num)
			ui.listfound()
			self.list1.setFocus()
			self.list4.hide()
			self.go_page.clear()
			#self.go_page.hide()
		#self.list4.hide()
	def search_list5_options(self):
		global opt,site,name,base_url,name1,embed,pre_opt,bookmark,base_url_picn,base_url_summary
		#self.text.show()
		r = self.list5.currentRow()
		item = self.list5.item(r)
		if item:
			tmp = str(self.list5.currentItem().text())
			tmp1 = tmp.split(':')[0]
			num = int(tmp1)
			self.list2.setCurrentRow(num)
			ui.epnfound()
			#self.list2.setFocus()
			self.list5.setFocus()
			self.goto_epn_filter_txt.clear()
			#self.go_page.clear()
			#self.goto_epn_filter_txt.hide()
		#self.list4.hide()
	def history_highlight(self):
		global opt,site,name,base_url,name1,embed,pre_opt,bookmark,base_url_picn,base_url_summary
		#self.text.show()
		print('history_highlight')
		if site!= "Music":
			self.subtitle_track.setText("SUB")
			self.audio_track.setText("A/V")
		if opt == "History" or site == "Music" or site == "Video" or site == "PlayLists":
		
			self.listfound()
		else:
			self.rawlist_highlight()


	
	def search_highlight(self):
		global opt,site,name,base_url,name1,embed,pre_opt,bookmark,base_url_picn,base_url_summary
		#self.text.show()
		r = self.list4.currentRow()
		item = self.list4.item(r)
		if item:
			tmp = str(self.list4.currentItem().text())
			tmp1 = tmp.split(':')[0]
			num = int(tmp1)
			self.list1.setCurrentRow(num)
			if opt == "History" or site == "Music":
			
				self.listfound()
			else:
				self.rawlist_highlight()
	
	def replace_lineByIndex(self,file_path,nepn,replc,index):
		global opt,site,name,pre_opt,home,bookmark,base_url,embed,status,epnArrList
		#f = open(file_path,'r')
		#lines = f.readlines()
		#f.close()
		lines = open_files(file_path,True)
		length = len(lines)
		lines[index] = replc
		if (index == length - 1) and (length > 1):
			t = lines[index-1]
			t = re.sub('\n','',t)
			lines[index-1]=t
		"""
		f = open(file_path,'w')
		for i in lines:
			f.write(i)
		f.close()
		"""
		write_files(file_path,lines,line_by_line=True)
		if 'Ep.txt' in file_path:
			#f = open(file_path,'r')
			#lines = f.readlines()
			#f.close()
			lines = open_files(file_path,True)
			epnArrList[:]=[]
			for i in lines:
				i = i.replace('\n','')
				epnArrList.append(i)
	
	
	
	def update_list2(self):
		global epnArrList,site,refererNeeded,finalUrlFound
		update_pl_thumb = True
		if not epnArrList:
			return 0
		if self.list2.isHidden():
			update_pl_thumb = False
		#if not self.scrollArea.isHidden():
		#	update_pl_thumb = False
		print(update_pl_thumb,'update_playlist_thumb')
		row = self.list2.currentRow()
		self.list2.clear()
		k = 0
		for i in epnArrList:
			i = i.strip()
			if '	' in i:
				i = i.split('	')[0]
				i = i.replace('_',' ')
				if i.startswith('#'):
					i = i.replace('#',self.check_symbol,1)
					self.list2.addItem((i))
					self.list2.item(k).setFont(QtGui.QFont('SansSerif', 10,italic=True))
				else:
					self.list2.addItem((i))
			else:
				if site == "Local" or finalUrlFound == True:
					#j = i.split('/')[-1]
					j = os.path.basename(i)
					if i.startswith('#') and j:
						j = j.replace('#',self.check_symbol,1)
				else:
					j = i
				j = j.replace('_',' ')
				if j.startswith('#'):
					j = j.replace('#',self.check_symbol,1)
					self.list2.addItem((j))	
					self.list2.item(k).setFont(QtGui.QFont('SansSerif', 10,italic=True))
				else:
					self.list2.addItem((j))
			#if self.list_with_thumbnail and update_pl_thumb:
			#	icon_name = self.get_thumbnail_image_path(k,epnArrList[k])
			#	icon_new_pixel = self.create_new_image_pixel(icon_name,128)
			#	if os.path.exists(icon_new_pixel):
			#		self.list2.item(k).setIcon(QtGui.QIcon(icon_new_pixel))
			k = k+1
		self.list2.setCurrentRow(row)
		if self.list2.count() < 30:
			QtCore.QTimer.singleShot(10, partial(self.set_icon_list2,epnArrList,self.list_with_thumbnail,update_pl_thumb))
		else:
			QtCore.QTimer.singleShot(100, partial(self.set_icon_list2,epnArrList,self.list_with_thumbnail,update_pl_thumb))
		#if self.list_with_thumbnail:
		#	thread_update = updateListThread(epnArrList)
		#	thread_update.start()
	def set_icon_list2(self,epnArr,list_thumb,update_pl):
		for k in range(len(epnArr)):
			if list_thumb and update_pl:
				icon_name = self.get_thumbnail_image_path(k,epnArr[k])
				icon_new_pixel = self.create_new_image_pixel(icon_name,128)
				if os.path.exists(icon_new_pixel):
					try:
						self.list2.item(k).setIcon(QtGui.QIcon(icon_new_pixel))
					except:
						pass
		txt_str = str(self.list1.count())+'/'+str(self.list2.count())
		self.page_number.setText(txt_str)
	def mark_History(self):
		global epnArrList,curR,opt,siteName,site,name,home
		file_path = ""
		row = self.list2.currentRow()
		if opt == "History" and site != "PlayLists":
			if site == "SubbedAnime" or site == "DubbedAnime":
				if os.path.exists(os.path.join(home,'History',site,siteName,name,'Ep.txt')):
					file_path = os.path.join(home,'History',site,siteName,name,'Ep.txt')
				
			else:
				if os.path.exists(os.path.join(home,'History',site,name,'Ep.txt')):
					file_path = os.path.join(home,'History',site,name,'Ep.txt')

			if os.path.exists(file_path):
				#f = open(file_path,'r')
				#lines = f.readlines()
				#f.close()
				lines = open_files(file_path,True)
				if '#' in epnArrList[row]:
					n_epn = epnArrList[row]
				else:
					n_epn = '#'+epnArrList[row]
				if '\n' in lines[row]:
					lines[row] = n_epn + '\n'
				else:
					lines[row]= n_epn
				epnArrList[:]=[]
				#f = open(file_path,'w')
				for i in lines:
					#f.write(i)
					i = i.strip()
					epnArrList.append(i)
				#f.close()
				write_files(file_path,lines,line_by_line=True)
			self.update_list2()
		
	def deleteHistory(self):
		global opt,site,name,pre_opt,home,bookmark,base_url,embed,status,siteName,original_path_name,video_local_stream
		if self.list1.currentItem():
			epn = self.list1.currentItem().text()
			row = self.list1.currentRow()
		else:
			return 0
		nepn = str(epn) + "\n"
		replc = ""
	
		if site == 'None':
			return 0
		if bookmark == "True" and os.path.exists(os.path.join(home,'Bookmark',status+'.txt')):
			file_path = os.path.join(home,'Bookmark',status+'.txt')
			
			row = self.list1.currentRow()
			item = self.list1.item(row)
			nam = str(item.text())
			
			if item and os.path.exists(file_path):
				self.list1.takeItem(row)
				del item
				#f = open(file_path,'r')
				#lines = f.readlines()
				#f.close()
				lines = open_files(file_path,True)
				if row < len(lines):
					del lines[row]
					length = len(lines) - 1
					"""
					j = 0
					f = open(file_path,'w')
					for i in lines:
						if j == length:
							i = i.replace('\n','')
						f.write(i)
					f.close()
					"""
					write_files(file_path,lines,line_by_line=True)
			
		elif site == "Local":
			r = ui.list3.currentRow()
			r1 = ui.list3.item(r)
			if r1:
				t_opt = str(r1.text())
				if t_opt == "All" or t_opt == "History":
					#tmp_name = str(self.list1.currentItem().text())
					index = ui.list1.currentRow()
					item = ui.list1.item(index)
					if item:
						tmp_name = original_path_name[index]
						print (tmp_name)
						if t_opt == "All":
							dir_path = os.path.join(home,'Local',tmp_name)
						else:
							dir_path = os.path.join(home,'History','Local',tmp_name)
							hist_path = os.path.join(home,'History','Local','history.txt')
						if os.path.exists(dir_path):
							shutil.rmtree(dir_path)
						ui.list1.takeItem(index)
						del item
						del original_path_name[index]
						self.list1.setCurrentRow(index)
						if t_opt == "History":
							#f = open(hist_path,'w')
							#for i in range(self.list1.count()):
							#	j = original_path_name[i]
							#	f.write(j+'\n')
							#f.close()
							write_files(hist_path,original_path_name,line_by_line=True)
		elif opt == "History":
			file_path = ''
			
			if site == "SubbedAnime" or site == "DubbedAnime":
				if os.path.exists(os.path.join(home,'History',site,siteName,'history.txt')):
					file_path = os.path.join(home,'History',site,siteName,'history.txt')
			
			else:
				if os.path.exists(os.path.join(home,'History',site,'history.txt')):
					file_path = os.path.join(home,'History',site,'history.txt')
			if not file_path:
				return 0
			row = self.list1.currentRow()
			item = self.list1.item(row)
			nam = str(item.text())
			if item:
				
				if site == "SubbedAnime" or site == "DubbedAnime":
					dir_name =os.path.join(home,'History',site,siteName,nam)
					print (dir_name	)
				else:
					dir_name =os.path.join(home,'History',site,nam)
					print (dir_name)
				if os.path.exists(dir_name):
					shutil.rmtree(dir_name)
					if video_local_stream:
						torrent_file = dir_name+'.torrent'
						if os.path.exists(torrent_file):
							os.remove(torrent_file)
				self.list1.takeItem(row)
				
				del item
				del original_path_name[row]
				length = self.list1.count() - 1
				#f = open(file_path,'w')
				#for i in range(self.list1.count()):
					
				#	fname = original_path_name[i]
				#	fname = fname.strip()
				#	if i == length:
				#		f.write(str(fname))
				#	else:
				#		f.write(str(fname)+'\n')
				#f.close()
				write_files(file_path,original_path_name,line_by_line=True)
				
			
			
			
	def create_img_url(self,path):
		m = []
		if '/watch?' in path:
			a = path.split('?')[-1]
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
			img_url="https://i.ytimg.com/vi/"+d['v']+"/hqdefault.jpg"
			return img_url
	def epn_highlight(self):
		global epnArrList,home,site
		#self.text.hide()
		#self.list4.hide()
		num = self.list2.currentRow()
		if num < 0:
			return 0
		if self.list2.currentItem() and num < len(epnArrList):
				epn_h = self.list2.currentItem().text()
				#self.goto_epn.setText(epn_h)
				inter_val = 10
				
				if '	' in epnArrList[num]:
					a = (epnArrList[num]).split('	')[0]
					path = (epnArrList[num]).split('	')[1]
				else:	
					#a = (epnArrList[num]).split('/')[-1]
					a = os.path.basename(epnArrList[num])
					path = (epnArrList[num])
				path = path.replace('#','')
				if site == "PlayLists":
					path = path.replace('"','')
				print (path)
				a1 = a
				self.text.clear()
				if site != "Music":
					self.text.setText((a1))
					#a1 = a1.replace('.','.<br>')
					#self.text.setHtml(('<html><p class="big">'+a1+'</p></html>'))
				#self.goto_epn.setText(a1)
				a1 = a1.replace('#','')
				if a1.startswith(self.check_symbol):
					a1 = a1[1:]
				#picn = home+'/thumbnails/'+a1+'.jpg'
				inter = str(inter_val)+'s'
				picnD = ''
				picn = ''
				if site == "PlayLists" or site == "Local" or site == "Video" or site == "Music":
					if site == 'PlayLists':
						playlist_dir = os.path.join(home,'thumbnails','PlayLists')
						if not os.path.exists(playlist_dir):
							os.makedirs(playlist_dir)
						if self.list1.currentItem():
							pl_n = self.list1.currentItem().text()
							playlist_name = os.path.join(playlist_dir,pl_n)
							if not os.path.exists(playlist_name):
								try:
									os.makedirs(playlist_name)
								except Exception as e:
									print(e)
									return 0
							picnD = os.path.join(playlist_name,a1)
							try:
								picn = picnD+'.jpg'
							except:
								picn = str(picnD)+'.jpg'
					else:
						if self.list1.currentItem():
							name_t = self.list1.currentItem().text()
						else:
							name_t = ''
						if self.list3.currentItem() and site == 'Music':
							if self.list3.currentItem().text() == 'Playlist':
								picnD = os.path.join(home,'thumbnails','PlayLists',name_t)
							else:
								picnD = os.path.join(home,'thumbnails',site,name_t)
						else:
							picnD = os.path.join(home,'thumbnails',site,name_t)
						print(picnD,'=picnD')
						if not os.path.exists(picnD):
							try:
								os.makedirs(picnD)
							except Exception as e:
								print(e)
								return 0
						picn = os.path.join(picnD,a1)+'.jpg'
					if (picn and not os.path.exists(picn) and 'http' not in path) or (picn and not os.path.exists(picn) and 'http' in path and 'youtube.com' in path ):
						path = path.replace('"','')
						if 'http' in path and 'youtube.com' in path and '/watch?' in path:
							path = self.create_img_url(path)
						self.threadPoolthumb.append(ThreadingThumbnail(path,picn,inter))
						self.threadPoolthumb[len(self.threadPoolthumb)-1].finished.connect(self.thumbnail_generated)
						length = len(self.threadPoolthumb)
						if length == 1:
							if not self.threadPoolthumb[0].isRunning():
								self.threadPoolthumb[0].start()
					
						
				if not picnD:
					if self.list1.currentItem():
						name_t = self.list1.currentItem().text()
					else:
						name_t = ''
					picnD = os.path.join(home,'thumbnails',name_t)
					if not os.path.exists(picnD):
						try:
							os.makedirs(picnD)
						except Exception as e:
							print(e)
							return 0
					try:
						picn = os.path.join(picnD,a1)+'.jpg'
					except:
						picn = os.path.join(picnD,str(a1))+'.jpg'
				if os.path.exists(picn):
					img = QtGui.QPixmap(picn, "1")			
					self.label.setPixmap(img)
				else:
					#self.label.clear()
					pass
				
	def thumbnail_generated(self):
		print ("Process Ended")
		self.threadPoolthumb = self.threadPoolthumb[1:]
		length = len(self.threadPoolthumb)
		if length > 0:
			if not self.threadPoolthumb[0].isRunning():
				self.threadPoolthumb[0].start()
				
	def directepn(self):
		global epn,epn_goto
		epn_goto = 1
		epn = self.goto_epn.text()
		epn = re.sub("#","",str(epn))
		self.epnfound()
	
	
	def preview(self):
		global embed, playMpv,Player,mpvplayer
		Player = str(self.chk.currentText())
		if mpvplayer:
			if mpvplayer.processId()>0 and self.tab_2.isHidden():
				mpvplayer.kill()
				self.epnfound()
		
	
	
	
	def nextp(self,val):
	
		global opt,pgn,genre_num,site,embed,mirrorNo,quality,name
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,list1_items
	
		pict_arr[:]=[]
		name_arr[:]=[]
		summary_arr[:]=[]
		#total_till=0
		browse_cnt=0
		tmp_name[:]=[]
		list1_items[:]=[]
		
		if val == "next":
			r = self.list3.currentRow()
		else:
			r = val
		item = self.list3.item(r)
		print (r)
		if item:
			opt_val = str(item.text())
			print (opt_val)
			if opt_val == "History" or opt_val == "Random" or opt_val == "List":
				return 0
		elif opt == 'Search':
			opt_val = 'Search'
		else:
			return 0
			
		print(opt_val,pgn,genre_num,name)
		
		
		self.list1.verticalScrollBar().setValue(self.list1.verticalScrollBar().minimum())
		
		try:
			
			code = 6
			pgn = pgn + 1
			if (opt != "") and (pgn >= 1):
				m = self.site_var.getNextPage(opt_val,pgn,genre_num,self.search_term)
				self.list1.clear()
				original_path_name[:] = []
				for i in m:
					i = i.strip()
					j = i
					if '	' in i:
						i = i.split('	')[0]
					self.list1.addItem(i)
					list1_items.append(i)
					original_path_name.append(j)
			#del site_var
		except:
			pass
		
	def backp(self,val):
	
		global opt,pgn,genre_num,embed,mirrorNo,quality,name
		self.list1.verticalScrollBar().setValue(self.list1.verticalScrollBar().minimum())
		if val == "back":
			r = self.list3.currentRow()
		else:
			r = val
		item = self.list3.item(r)
		if item:
			opt_val = str(item.text())
			if opt_val == "History" or opt_val == "Random" or opt_val == "List":
				return 0
		elif opt == 'Search':
			opt_val = 'Search'
		else:
			return 0
		
		
		try:
			pgn = pgn - 1
			if (opt != "") and (pgn >= 1):
				m = self.site_var.getNextPage(opt_val,pgn,genre_num,self.search_term)
				self.list1.clear()
				original_path_name[:] = []
				for i in m:
					i = i.strip()
					j = i
					if '	' in i:
						i = i.split('	')[0]
					self.list1.addItem(i)
					list1_items.append(i)
					original_path_name.append(j)
			#del site_var
		except:
			pass
					
	def gotopage(self):
		key = self.page_number.text()
		global opt,pgn,site
		if (opt != "") and (site == "KissAnime"):
			if key:
				self.list1.verticalScrollBar().setValue(self.list1.verticalScrollBar().minimum())
				pgn = int(key)
				pgn = pgn - 1
				self.nextp(-1)
				
	def label_filter_list_update(self,item_index):
		global viewMode, opt, site, bookmark, thumbnail_indicator,total_till,label_arr,browse_cnt,tmp_name,list1_items
		
		length = len(item_index)
		if not self.scrollArea.isHidden():
			length1 = len(list1_items)
		else:
			length1 = self.list2.count()
		
		print (length,'--length-filter-epn--')
		#print item_index
		if item_index:
			i = 0
			if not self.scrollArea.isHidden():
				while(i < length):
					if item_index[i] == 1:
						t = "self.label_"+str(i)+".show()"
						
						exec (t)
						t = "self.label_"+str(i+length1)+".show()"
						
						exec (t)
					else:
						t = "self.label_"+str(i)+".hide()"
						
						exec (t)
						
						t = "self.label_"+str(i+length1)+".hide()"
						
						exec (t)
					i = i+1
			else:
				while(i < length):
					if item_index[i] == 1:
						t = "self.label_epn_"+str(i)+".show()"
						
						exec (t)
						t = "self.label_epn_"+str(i+length1)+".show()"
						
						exec (t)
					else:
						t = "self.label_epn_"+str(i)+".hide()"
						
						exec (t)
						
						t = "self.label_epn_"+str(i+length1)+".hide()"
						
						exec (t)
					i = i+1
			
			
	def filter_label_list(self):
		global opt,pgn,site,list1_items,base_url,filter_on,base_url,embed,hist_arr
		print ("filter label")
		filter_on = 1
		row_history = []
		key = str(self.label_search.text()).lower()
		if not key:
			filter_on = 0
		found_item = []
		found_item_index = []
		print (opt)
		print (site)
		found_item_index[:]=[]
		if not self.scrollArea.isHidden():
			if key:
				for i in range(self.list1.count()):
					srch = str(self.list1.item(i).text()).lower()
					if key in srch:
						found_item.append(i)
						found_item_index.append(1)
					else:
						found_item_index.append(0)
			else:
				for i in range(self.list1.count()):				
						found_item_index.append(1)
		else:
			if key:
				for i in range(self.list2.count()):
					srch = str(self.list2.item(i).text()).lower()
					if key in srch:
						found_item.append(i)
						found_item_index.append(1)
					else:
						found_item_index.append(0)
			else:
				for i in range(self.list2.count()):				
						found_item_index.append(1)
				
				
		self.label_filter_list_update(found_item_index)
		
	
	def filter_list(self):
		global opt,pgn,site,list1_items,base_url,filter_on,base_url,embed,hist_arr
		print ("filter label")
		filter_on = 1
		row_history = []
		key = str(self.go_page.text()).lower()
		if not key:
			filter_on = 0
		found_item = []
		found_item_index = []
		print (opt)
		print (site)
		found_item_index[:]=[]
		
		if key:
			#self.list1.hide()
			self.list4.show()
			for i in range(self.list1.count()):
				srch = str(self.list1.item(i).text())
				srch1 = srch.lower()
				if key in srch1:
					found_item.append(str(i)+':'+srch)
					
			length = len(found_item_index)
			self.list4.clear()
			for i in found_item:
				self.list4.addItem(i)
			
			
		else:
			self.list4.clear()
			self.list4.hide()
			self.list1.show()
				
	def filter_epn_list_txt(self):
		global opt,pgn,site,list1_items,base_url,filter_on,base_url,embed,hist_arr,epnArrList
		print ("filter epn list")
		filter_on = 1
		row_history = []
		key = str(self.goto_epn_filter_txt.text()).lower()
		if not key:
			filter_on = 0
		found_item = []
		found_item_index = []
		print (opt)
		print (site)
		found_item_index[:]=[]
		
		if key:
			#self.list1.hide()
			self.list5.show()
			for i in range(len(epnArrList)):
				srch = epnArrList[i]
				
				srch1 = srch.lower()
				srch2 = str(self.list2.item(i).text())
				if key in srch1:
					found_item.append(str(i)+':'+srch2)
					
			length = len(found_item_index)
			self.list5.clear()
			for i in found_item:
				self.list5.addItem(i)
			
			
		else:
			self.list5.clear()
			self.list5.hide()
			self.list2.show()
	def ka(self):
		global site,home
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,list1_items,bookmark,total_till,thumbnail_indicator,genre_num,original_path_name,rfr_url,finalUrlFound,refererNeeded,video_local_stream
		genre_num = 0
		#total_till = 0
		if self.site_var:
			del self.site_var
			self.site_var = ''
		self.label.clear()
		self.text.clear()
		original_path_name[:]=[]
		rfr_url = ""
		finalUrlFound = False
		refererNeeded = False
		site = str(self.btn1.currentText())
		if not self.btnAddon.isHidden():
			self.btnAddon.hide()
		if not self.btnHistory.isHidden():
			self.btnHistory.hide()
		self.list3.clear()
		self.list1.clear()
		self.list2.clear()
		self.label.clear()
		self.text.clear()
		
		if site == "PlayLists":
			bookmark = "False"
			criteria = os.listdir(os.path.join(home,'Playlists'))
			criteria.sort()
			home_n = os.path.join(home,'Playlists')
			criteria = naturallysorted(criteria)
			#criteria = sorted(criteria,key = lambda x:os.path.getmtime(os.path.join(home_n,x)),reverse=True)
			original_path_name[:] = []
			for i in criteria:
				self.list1.addItem(i)
				original_path_name.append(i)
			video_local_stream = False
		elif site == "Bookmark":
			bookmark = "True"
			criteria = ['All','Watching','Completed','Incomplete',"Later",'Interesting','Music-Videos']
			bookmark_array = ['bookmark','Watching','Completed','Incomplete','Later','Interesting','Music-Videos']
			bookmark_extra = []
			for i in bookmark_array:
				f_path = os.path.join(home,'Bookmark',i+'.txt')
				if not os.path.exists(f_path):
					f = open(f_path,'w')
					f.close()
			m = os.listdir(os.path.join(home,'Bookmark'))
			for i in m:
				i = i.replace('.txt','')
				if i not in bookmark_array:
					bookmark_extra.append(i)
			self.list3.clear()
			for i in criteria:
				self.list3.addItem(i)
			for i in bookmark_extra:
				self.list3.addItem(i)
		elif site == "Select":
			site = 'None'
		elif site == "Addons":
			site = 'None'
			self.btnAddon.show()
			site = self.btnAddon.currentText()
			if self.site_var:
				del self.site_var
				self.site_var = ''
			print(type(self.site_var),site,'--addon-changed--')
			plugin_path = os.path.join(home,'src','Plugins',site+'.py')
			if os.path.exists(plugin_path):
				module = imp.load_source(site,plugin_path)
			self.site_var = getattr(module,site)(TMPDIR)
			bookmark = "False"
			if not os.path.exists(os.path.join(home,"History",site)):
				os.makedirs(os.path.join(home,"History",site))
			self.search()
		elif site == "YouTube":
			site = 'None'
			bookmark = "False"
			self.search()
		else:
			bookmark = "False"
			if not os.path.exists(os.path.join(home,"History",site)):
				os.makedirs(os.path.join(home,"History",site))
			self.search()
		
	def ka2(self):
		global site,home
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,list1_items,bookmark,total_till,thumbnail_indicator,genre_num,original_path_name,rfr_url,finalUrlFound,refererNeeded
		genre_num = 0
		#total_till = 0
		if self.site_var:
			del self.site_var
			self.site_var = ''
		self.label.clear()
		self.text.clear()
		original_path_name[:]=[]
		rfr_url = ""
		finalUrlFound = False
		refererNeeded = False
		self.list3.clear()
		self.list1.clear()
		self.list2.clear()
		self.label.clear()
		self.text.clear()
		site = (self.btnAddon.currentText())
		print(type(self.site_var),site,'--addon-changed--')
		plugin_path = os.path.join(home,'src','Plugins',site+'.py')
		if os.path.exists(plugin_path):
			module = imp.load_source(site,plugin_path)
		self.site_var = getattr(module,site)(TMPDIR)
		print(type(self.site_var),site,'--addon-changed--')
		if site == 'SubbedAnime' or site == 'DubbedAnime':
			self.btnHistory.show()
		else:
			if not self.btnHistory.isHidden():
				self.btnHistory.hide()
		bookmark = "False"
		if not os.path.exists(os.path.join(home,"History",site)):
			os.makedirs(os.path.join(home,"History",site))
		self.search()
	
	def ka1(self):
		global site,home
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,list1_items,bookmark
		
		self.label.clear()
		self.text.clear()
		site = str(self.btn30.currentText())
		if site == "Bookmark":
			bookmark = "True"
			criteria = ['All','Watching','Completed','Incomplete',"Later",'Interesting']
			self.list3.clear()
			for i in criteria:
				self.list3.addItem(i) 
		else:
			bookmark = "False"
			if not os.path.exists(os.path.join(home,"History",site)):
				os.makedirs(os.path.join(home,"History",site))
			self.search()
		
	def goto_web_directly(self,url):
		global name,nam,old_manager,new_manager,home,screen_width,quality,site,epnArrList
		print(self.web,'0')
		if not self.web:
			self.web = Browser(ui,home,screen_width,quality,site,epnArrList)
			self.web.setObjectName(_fromUtf8("web"))
			self.horizontalLayout_5.addWidget(self.web)
			print(self.web,'1')
		else:
			if QT_WEB_ENGINE:
				cur_location = self.web.url().url()
			else:
				cur_location = self.web.url().toString()
			print(cur_location,'--web--url--')
			if 'youtube' not in cur_location and QT_WEB_ENGINE:
				self.web.close()
				self.web.deleteLater()
				self.web = Browser(ui,home,screen_width,quality,site,epnArrList)
				self.web.setObjectName(_fromUtf8("web"))
				self.horizontalLayout_5.addWidget(self.web)
			print(self.web,'2')
		
		self.list1.hide()
		self.list2.hide()
		self.label.hide()
		self.dockWidget_3.hide()
		self.text.hide()
		self.frame.hide()
		self.frame1.hide()
		self.tab_2.show()
		self.goto_epn.hide()
		name = str(name)
		name1 = re.sub('-| ','+',name)
		name1 = re.sub('Dub|subbed|dubbed|online','',name1)
		key = self.line.text()
		self.line.clear()
		
		if not QT_WEB_ENGINE:
			nam = NetWorkManager()
			self.web.page().setNetworkAccessManager(nam)
		self.webStyle(self.web)
		self.web.load(QUrl(url))
		
			
	def reviewsWeb(self,srch_txt=None,review_site=None,action=None):
		global name,nam,old_manager,new_manager,home,screen_width,quality,site,epnArrList
		
		web_arr_dict = {'mal':'MyAnimeList','ap':'Anime-Planet','ans':'Anime-Source','tvdb':'TVDB','ann':'ANN','anidb':'AniDB','g':'Google','yt':'Youtube','ddg':'DuckDuckGo','reviews':'Reviews','last.fm':'last.fm','zerochan':'Zerochan'}
		
		if not review_site:
			review_site_tmp = self.btnWebReviews.currentText()
			review_site = list(web_arr_dict.keys())[list(web_arr_dict.values()).index(review_site_tmp)]
		#if action:
		#	if action == 'index_changed':
		#		if review_site:
		#			try:
		#				self.btnWebReviews_search.setPlaceholderText('Search '+web_arr_dict[review_site])
		#			except Exception as e:
		#				print(e)
		#		return 0
		#review_site = str(self.btnWebReviews.currentText())
		print(self.web,'0')
		if not self.web and review_site:
			self.web = Browser(ui,home,screen_width,quality,site,epnArrList)
			self.web.setObjectName(_fromUtf8("web"))
			self.horizontalLayout_5.addWidget(self.web)
			print(self.web,'1')
		elif self.web:
			if QT_WEB_ENGINE:
				cur_location = self.web.url().url()
			else:
				cur_location = self.web.url().toString()
			print(cur_location,'--web--url--')
			if 'yt' in review_site.lower() and 'youtube' not in cur_location and QT_WEB_ENGINE:
				self.web.close()
				self.web.deleteLater()
				self.web = Browser(ui,home,screen_width,quality,site,epnArrList)
				self.web.setObjectName(_fromUtf8("web"))
				self.horizontalLayout_5.addWidget(self.web)
			print(self.web,'2')
		
		self.list1.hide()
		self.list2.hide()
		self.dockWidget_3.hide()
		self.label.hide()
		self.text.hide()
		self.VerticalLayoutLabel.takeAt(2)
		self.frame.hide()
		
		#self.frame1.hide()
		self.tab_2.show()
		self.goto_epn.hide()
		name = str(name)
		name1 = re.sub('-| ','+',name)
		name1 = re.sub('Dub|subbed|dubbed|online','',name1)
		key = ''
		if action:
			if action == 'return_pressed':
				key = self.btnWebReviews_search.text()
				self.btnWebReviews_search.clear()
				self.tmp_web_srch = key
			elif action == 'context_menu' or action == 'search_by_name':
				key = srch_txt
			elif action == 'index_changed' or action == 'btn_pushed':
				if not self.tmp_web_srch:
					key = name1
				else:
					key = self.tmp_web_srch
			elif action == 'line_return_pressed':
				key = self.line.text()
				self.line.clear()
		else:
			key = self.line.text()
			self.line.clear()
		if key:
			name1 = str(key)
		#old_manager = self.web.page().networkAccessManager()
		pl_list = False
		new_url = ''
		if not name1:
			if self.list1.currentItem():
				name1 = self.list1.currentItem().text()
				if self.list2.currentItem() and self.btn1.currentText() == 'PlayLists':
					name1 = self.list2.currentItem().text()
					r = self.list2.currentRow()
					#try:
					finalUrl = epnArrList[r].split('	')[1]
					if 'youtube.com' in finalUrl and 'list=' in finalUrl:
						new_url = finalUrl
						pl_list = True
					#except:
					#	pass
			elif self.list2.currentItem():
				name1 = self.list2.currentItem().text()
			#name1 = name1.replace('#','')
			if name1.startswith(self.check_symbol):
				name1 = name1[1:]
		if not QT_WEB_ENGINE:
			nam = NetWorkManager()
			self.web.page().setNetworkAccessManager(nam)
		self.webStyle(self.web)
		if review_site == "ap":
			self.web.load(QUrl("http://www.anime-planet.com/anime/all?name="+name1))
		elif review_site == "mal":
			self.web.load(QUrl("http://myanimelist.net/anime.php?q="+name1))
		elif review_site == "ans":
			self.web.load(QUrl("http://www.anime-source.com/banzai/modules.php?name=NuSearch&type=all&action=search&info="+name1))
		elif review_site == "tvdb":
			self.web.load(QUrl("http://thetvdb.com/?string="+name1+"&searchseriesid=&tab=listseries&function=Search"))
		elif review_site == "anidb":
			self.web.load(QUrl("http://anidb.net/perl-bin/animedb.pl?adb.search="+name1+"&show=animelist&do.search=search"))
		elif review_site == "ann":
			self.web.load(QUrl("http://www.animenewsnetwork.com/encyclopedia/search/name?q="+name1))
		elif review_site == "g":
			self.web.load(QUrl("https://www.google.com/search?q="+name1))
		elif review_site == "ddg":
			self.web.load(QUrl("https://duckduckgo.com/?q="+name1))
		elif review_site == "yt":
			if not name1:
				name1 = 'GNU Linux FSF'
			if pl_list and new_url:
				self.web.load(QUrl(new_url))
			else:
				self.web.load(QUrl("https://m.youtube.com/results?search_query="+name1))
		elif review_site == "last.fm":
			self.web.load(QUrl("http://www.last.fm/search?q="+name1))
		elif review_site == 'zerochan':
			self.web.load(QUrl("http://www.zerochan.net/search?q="+name1))
		elif review_site == "reviews":
			self.web.setHtml('<html>Reviews:</html>')
		
		if review_site:
			try:
				self.btnWebReviews_search.setPlaceholderText('Search '+web_arr_dict[review_site])
			except Exception as e:
				print(e)
		
	def rawlist_highlight(self):
		
		global site,name,base_url,name1,embed,opt,pre_opt,mirrorNo,list1_items,list2_items,quality,row_history,home,epn,path_Local_Dir,epnArrList,bookmark,status,siteName,original_path_name,screen_height,screen_width
		#print('========raw_list_highlight==========')
		if self.list1.currentItem():
			nm = original_path_name[self.list1.currentRow()].strip()
			if '	' in nm:
				name = nm.split('	')[0]
			else:
				name = nm
		else:
			return 0
		#fanart = "/tmp/AnimeWatch/"+name+"-fanart.jpg"
		#thumbnail = "/tmp/AnimeWatch/"+name+"-thumbnail.jpg"
		cur_row = self.list1.currentRow()
		fanart = os.path.join(TMPDIR,name+'-fanart.jpg')
		thumbnail = os.path.join(TMPDIR,name+'-thumbnail.jpg')
		m = []
		epnArrList[:]=[]
		#print('========raw_list_highlight==========')
		summary = 'Summary Not Available'
		picn = 'No.jpg'
		if site == "SubbedAnime" or site == "DubbedAnime":
			if self.list3.currentItem():
				siteName = self.list3.currentItem().text()
			#r = self.list1.currentRow()
			
			file_name = os.path.join(home,'History',site,siteName,name,'Ep.txt')
			picn1 = os.path.join(home,'History',site,siteName,name,'poster.jpg')
			fanart1 = os.path.join(home,'History',site,siteName,name,'fanart.jpg')
			thumbnail1 = os.path.join(home,'History',site,siteName,name,'thumbnail.jpg')
			summary_file = os.path.join(home,'History',site,siteName,name,'summary.txt')
		elif site == "Local":
			
			name = original_path_name[cur_row]
			file_name = os.path.join(home,'Local',name,'Ep.txt')
			picn1 = os.path.join(home,'Local',name,'poster.jpg')
			fanart1 = os.path.join(home,'Local',name,'fanart.jpg')
			thumbnail1 = os.path.join(home,'Local',name,'thumbnail.jpg')
			summary_file = os.path.join(home,'Local',name,'summary.txt')
		else:
			file_name = os.path.join(home,'History',site,name,'Ep.txt')
			picn1 = os.path.join(home,'History',site,name,'poster.jpg')
			fanart1 = os.path.join(home,'History',site,name,'fanart.jpg')
			thumbnail1 = os.path.join(home,'History',site,name,'thumbnail.jpg')
			summary_file = os.path.join(home,'History',site,name,'summary.txt')
		#print "file_name="+file_name
		
		if os.path.exists(file_name) and site!="PlayLists":
			print(site,siteName,name,file_name)
			#lines = tuple(open(file_name, 'r'))
			lines = open_files(file_name,True)
				#with open(home+'/History/'+site+'/'+name+'/Ep.txt') as f:
				#items = f.readlines()
			m = []
			if site == "Local" and lines:
				for i in lines:
					i = i.strip()
					if i:
						if '	'in i:
							k = i.split('	')
							
							epnArrList.append(i)
							
							m.append(k[0])
						else:
							#k = i.split('/')[-1]
							k = os.path.basename(i)
							epnArrList.append(k+'	'+i)
							
							m.append(k)
			elif lines:
				for i in lines:
					i = i.strip()
					if i:
						epnArrList.append(i)
						m.append(i)
				
					
			picn = picn1
			fanart = fanart1
			thumbnail = thumbnail1
			
			if os.path.isfile(summary_file):
				#g = open(summary_file, 'r')
				#summary = g.read()
				#m.append(summary)
				#m = lines + tuple(picn) + tuple(summary)
				#g.close()
				summary = open_files(summary_file,False)
			
			j = 0
			
			self.text.clear()
			
			self.text.lineWrapMode()
			if site!= "Local":
				#self.text.insertPlainText('Summary of '+name +' : '+'\n')
				#self.text.insertPlainText(name +' : '+'\n')
				pass
			if summary.lower() == 'summary not available':
				summary = summary+'\n'+original_path_name[cur_row]			
			self.videoImage(picn,thumbnail,fanart,summary)
				
			if os.path.isfile(str(picn)):
				self.list2.clear()
				self.update_list2()
		
		else:
			
			if summary.lower() == 'summary not available':
				txt = original_path_name[cur_row]
				if '	' in txt:
					txt1,txt2 = txt.split('	')
					summary = summary+'\n\n'+txt1+'\n\n'+txt2
			self.text.clear()
			self.text.insertPlainText(summary)
		
			
	def searchNew(self):
		global search,name
		#site = str(self.btn1.currentText())
		if self.btn1.currentText() == "Select":
			site = "None"
			return 0
		elif (self.line.placeholderText()) == "No Search Option":
			#site = "None"
			return 0
		else:
			self.search()
			name = (self.line.text())
	def search(self):
		code = 1
		global site,base_url,embed,list1_items,opt,mirrorNo,hdr,quality,site_arr,siteName,finalUrlFound,epnArrList
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,list2_items,bookmark,refererNeeded,video_local_stream,name
		pict_arr[:]=[]
		name_arr[:]=[]
		summary_arr[:]=[]
		#total_till=0
		browse_cnt=0
		tmp_name[:]=[]
		opt = "Search"
		m=[]
		criteria = []
		
		
		
		print(site,self.btn1.currentText().lower())
		
		if site and (site not in site_arr) and self.site_var:
			print (site)
			
			self.mirror_change.hide()
			
			if self.site_var:
				criteria = self.site_var.getOptions() 
				self.list3.clear()
				print (criteria)
				tmp = criteria[-1]
				if tmp == "FinalUrl:Referer:":
					criteria.pop()
					finalUrlFound = True
					refererNeeded = True
					video_local_stream = False
				elif tmp == 'LocalStreaming':
					criteria.pop()
					video_local_stream = True
					if not self.local_ip:
						self.local_ip = get_lan_ip()
					if not self.local_port:
						self.local_port = 8001
					self.torrent_type = 'file'
				else:
					finalUrlFound = False
					refererNeeded = False
					video_local_stream = False
				for i in criteria:
					self.list3.addItem(i)
				self.line.setPlaceholderText("Search Available")
				self.line.setReadOnly(False)
				self.line.show()
				name = self.line.text()
				if name:
					self.line.clear()
					self.list1.clear()
					genre_num = 0
					try:
						self.text.setText('Wait...Loading')
						QtWidgets.QApplication.processEvents()
						m = self.site_var.search(name)
						self.search_term = name
						self.text.setText('Load Complete!')
					except:
						self.text.setText('Load Failed')
						#del site_var
						return 0
					if type(m) is list:
						original_path_name[:] = []
						for i in m:
							i = i.strip()
							j = i
							if '	' in i:
								i = i.split('	')[0]
							self.list1.addItem(i)
							original_path_name.append(j)
					else:
						self.list1.addItem("Sorry No Search Function")
				#del site_var
		elif site == "Local":
			self.mirror_change.hide()
			criteria = ["List",'History','All']
			self.list3.clear()
			for i in criteria:
				self.list3.addItem(i)
			self.line.setPlaceholderText("No Search Option")
			#self.line.hide()
			self.line.setReadOnly(True)
			refererNeeded = False
			#finalUrlFound = False
			video_local_stream = False
		elif site == "Music":
			self.mirror_change.hide()
			criteria = ['Playlist',"Artist",'Album','Title','Directory','Fav-Artist','Fav-Album','Fav-Directory','Last 50 Played','Last 50 Newly Added','Last 50 Most Played']
			self.list3.clear()
			for i in criteria:
				self.list3.addItem(i)
			self.line.setPlaceholderText("No Search Option")
			#self.line.hide()
			self.line.setPlaceholderText("Search Available")
			self.line.setReadOnly(False)
			#self.line.setReadOnly(True)
			refererNeeded = False
			video_local_stream = False
			#finalUrlFound = False
			nm = self.line.text()
			if nm:
				self.line.clear()
				self.list1.clear()
				music_db = os.path.join(home,'Music','Music.db')
				m = self.getMusicDB(music_db,'Search',nm)
				print (m)
				epnArrList[:]=[]
				self.list2.clear()
				for i in m:
					i1 = i[1]
					i2 = i[2]
					i3 = i[0]
					j = i1+'	'+i2+'	'+i3
					try:
						epnArrList.append(str(j))
					except:
						epnArrList.append(j)
					#self.list2.addItem((i1))
				self.update_list2()
				#else:
				#	self.list1.addItem("Not Found")
		elif site == "Video":
			self.mirror_change.hide()
			criteria = ['Directory','Available','History','Update','UpdateAll']
			self.list3.clear()
			for i in criteria:
				self.list3.addItem(i)
			self.line.setPlaceholderText("No Search Option")
			#self.line.hide()
			self.line.setReadOnly(True)
			refererNeeded = False
			video_local_stream = False
			#finalUrlFound = False
		elif (site == "None" and self.btn1.currentText().lower() == 'youtube') or not self.tab_2.isHidden():
			video_local_stream = False
			self.mirror_change.hide()
			self.line.setPlaceholderText("Search Available")
			self.line.setReadOnly(False)
			name_t = self.line.text()
			if name_t:
				name = name_t
				self.btnWebReviews.setCurrentIndex(8)
				self.reviewsWeb(srch_txt=name,review_site='yt',action='line_return_pressed')
			#if ui.btn1.currentText() == 'Addons' and addon_index >=0 and addon_index < ui.btnAddon.count():
			#ui.btnAddon.setCurrentIndex(addon_index)
		elif site == "DubbedAnime" or site == "SubbedAnime":
			
			video_local_stream = False
			self.mirror_change.show()
			
			if self.site_var:
				criteria = self.site_var.getOptions() 
				code = 7
				self.list3.clear()
				for i in criteria:
					self.list3.addItem(i)
				self.line.setPlaceholderText("No Search Option")
				#self.line.hide()
				self.line.setReadOnly(True)
				name = self.line.text()
				if name:
					self.line.clear()
					self.list1.clear()
					genre_num = 0
					self.text.setText('Wait...Loading')
					QtWidgets.QApplication.processEvents()
					m = self.site_var.getCompleteList(siteName,category,'Search')
					self.text.setText('Load Complete!')
					original_path_name[:] = []
					for i in m:
						i = i.strip()
						j = i
						if '	' in i:
							i = i.split('	')[0]
						self.list1.addItem(i)
						original_path_name.append(i)
		list1_items[:] = []
		if m:
			for i in m:
				list1_items.append(i)	

	def summary_write_and_image_copy(self,hist_sum,summary,picn,hist_picn):
		"""
		g = open(hist_sum, 'w')
		bin_mode = False
		try:
			g.write(summary)
		except UnicodeEncodeError as e:
			print(e,hist_sum+' will be written in binary mode')
			g.close()
			bin_mode = True
		if bin_mode:
			g = open(hist_sum,'wb')
			g.write(summary.encode('utf-8'))
			g.close()
		"""
		write_files(hist_sum,summary,line_by_line=False)
		if os.path.isfile(picn):
			shutil.copy(picn,hist_picn)
			
	def get_summary_history(self,file_name):
		summary = open_files(file_name,False)
		return summary
		"""
		summary = 'Summary Not Available'
		if os.path.exists(file_name):
			if OSNAME == 'posix':
				summary = open(file_name).read()
			else:
				try:
					f = open(file_name,encoding='utf-8',mode='r')
					summary = f.read()
					f.close()
				except:
					summary = "can't decode"
				
			return summary
		"""
			
	def listfound(self):
		global site,name,base_url,name1,embed,opt,pre_opt,mirrorNo,list1_items,list2_items,quality,row_history,home,epn,path_Local_Dir,bookmark,status,epnArrList,finalUrlFound,refererNeeded,audio_id,sub_id
		global opt_movies_indicator,base_url_picn,base_url_summary,siteName,img_arr_artist,screen_height,screen_width,video_local_stream
		img_arr_artist[:]=[]
		opt_movies_indicator[:]=[]
		
		fanart = os.path.join(TMPDIR,name+'-fanart.jpg')
		thumbnail = os.path.join(TMPDIR,name+'-thumbnail.jpg')
		summary = "Summary Not Available"
		picn = "No.jpg"
		m = []
		if bookmark == "True" and os.path.exists(os.path.join(home,'Bookmark',status+'.txt')):
			#tmp = site+':'+opt+':'+pre_opt+':'+base_url+':'+str(embed)+':'+name':'+finalUrlFound+':'+refererNeeded+':'+video_local_stream
			#f = open(os.path.join(home,'Bookmark',status+'.txt'),'r')
			#line_a = f.readlines()
			#f.close()
			line_a = open_files(os.path.join(home,'Bookmark',status+'.txt'),True)
			r = self.list1.currentRow()
			if r < 0:
				return 0
			tmp = line_a[r]
			tmp = tmp.strip()
			tmp1 = tmp.split(':')
			site = tmp1[0]
			if site == "Music" or site == "Video":
				opt = "Not Defined"
				if site == "Music":
					music_opt = tmp1[1]
				else:
					video_opt = tmp1[1]
			else:
				opt = tmp1[1]
			pre_opt = tmp1[2]
			siteName = tmp1[2]
			base_url = int(tmp1[3])
			embed = int(tmp1[4])
			name = tmp1[5]
			if site=="Local":
				name_path = name
			
			print (name)
			if len(tmp1) > 6:
				if tmp1[6] == "True":
					finalUrlFound = True
				else:
					finalUrlFound = False
				if tmp1[7] == "True":
					refererNeeded = True
				else:
					refererNeeded = False
				if len(tmp1) >=9:
					if tmp1[8] == "True":
						video_local_stream = True
					else:
						video_local_stream = False
				print (finalUrlFound)
				print (refererNeeded)
				print (video_local_stream)
			else:
				refererNeeded = False
				finalUrlFound = False
				video_local_stream = False
			print (site + ":"+opt)
			if (site != "PlayLists" and site != "Music" and site != "Video" and site!="Local" and site !="None"):
				plugin_path = os.path.join(home,'src','Plugins',site+'.py')
				if os.path.exists(plugin_path):
					if self.site_var:
						del self.site_var
						self.site_var = ''
					module = imp.load_source(site,plugin_path)
					self.site_var = getattr(module,site)(TMPDIR)
				else:
					return 0
					
		if (site != "PlayLists" and site != "Music" and site != "Video" and site!="Local" and site !="None") :
			self.list2.clear()
			if self.list1.currentItem():
				cur_row = self.list1.currentRow()
				new_name_with_info = original_path_name[cur_row].strip()
				extra_info = ''
				if '	' in new_name_with_info:
					name = new_name_with_info.split('	')[0]
					extra_info = new_name_with_info.split('	')[1]
				else:
					name = new_name_with_info
				
						
				if opt != "History":
					
					m = []
					#try:
					self.text.setText('Wait...Loading')
					QtWidgets.QApplication.processEvents()
					m,summary,picn,self.record_history,self.depth_list = self.site_var.getEpnList(name,opt,self.depth_list,extra_info,siteName,category)
					self.text.setText('Load..Complete')
					if not m:
						return 0
					#except:
					#	self.text.setText('Load Failed')
					#	return 0
					
					epnArrList[:]=[]
					for i in m:
						epnArrList.append(i)
						
					if site.lower() == 'subbedanime' or site.lower() == 'dubbedanime':
						hist_path = os.path.join(home,'History',site,siteName,'history.txt')
					else:
						hist_path = os.path.join(home,'History',site,'history.txt')
					if not os.path.isfile(hist_path):
						hist_dir,last_field = os.path.split(hist_path)
						if not os.path.exists(hist_dir):
							os.makedirs(hist_dir)
						f = open(hist_path, 'w').close()
					print(self.record_history,'--self.record_history---')
					if os.path.isfile(hist_path) and self.record_history:
						if (os.stat(hist_path).st_size == 0):
							#f = open(hist_path, 'w')
							#f.write(name)
							#f.close()
							write_files(hist_path,name,line_by_line=True)
						else:
							#f = open(hist_path, 'a')
							#lines = tuple(open(hist_path, 'r'))
							lines = open_files(hist_path,True)
							line_list = []
							for i in lines :
								i = i.strip()
								line_list.append(i)
							if new_name_with_info not in line_list:
								#f.write('\n'+name)
								write_files(hist_path,name,line_by_line=True)
							#f.close()
					
					hist_dir,last_field = os.path.split(hist_path)
					hist_site = os.path.join(hist_dir,name)
					if not os.path.exists(hist_site) and self.record_history:
						try:
							os.makedirs(hist_site)
							hist_epn = os.path.join(hist_site,'Ep.txt')
							
							write_files(hist_epn,m,line_by_line=True)
							
							hist_sum = os.path.join(hist_site,'summary.txt')
							hist_picn = os.path.join(hist_site,'poster.jpg')
							self.summary_write_and_image_copy(hist_sum,summary,picn,hist_picn)
						except Exception as e:
							print(e)
							return 0
				
				else:
					if site.lower() == 'subbedanime' or site.lower() == 'dubbedanime':
						if self.list3.currentItem() and bookmark == 'False':
							siteName = self.list3.currentItem().text()
						hist_site = os.path.join(home,'History',site,siteName,name)
					else:
						hist_site = os.path.join(home,'History',site,name)
						
					hist_epn = os.path.join(hist_site,'Ep.txt')
					print(hist_epn)
					if os.path.exists(hist_epn):
						
						#lines = tuple(open(hist_epn, 'r'))
						lines = open_files(hist_epn,True)
						m = []
						
						epnArrList[:]=[]
						for i in lines:
							i = i.strip()
							epnArrList.append(i)
							m.append(i)
								
						picn = os.path.join(hist_site,'poster.jpg')
						fanart = os.path.join(hist_site,'fanart.jpg')
						thumbnail = os.path.join(hist_site,'thumbnail.jpg')
						sum_file = os.path.join(hist_site,'summary.txt')
						#m.append(picn)
						summary = self.get_summary_history(sum_file)
						
						f_name = os.path.join(hist_site,'Ep.txt')
						if os.path.exists(f_name):
							
							#f = open(f_name,'r')
							#lines = f.readlines()
							#f.close()
							lines = open_files(f_name,True)
							if len(epnArrList) > len(lines):
								
								write_files(f_name,m,line_by_line=True)
							
							
				
				self.videoImage(picn,thumbnail,fanart,summary)
				
		elif site == "Local":
			self.list2.clear()
			if self.list1.currentItem():
				r = self.list1.currentRow()
				if bookmark == "True":
					name = name_path
				else:
					name = original_path_name[r]
				print (name)
				path_Local_Dir = (name.replace('@','/'))
				if opt != "History":
						m = []
						if original_path_name:
							r = self.list1.currentRow()
							name = original_path_name[r]
							
							file_path = os.path.join(home,'History',site,'history.txt')
							if not os.path.isfile(file_path):
								open(file_path, 'w').close()
							
							if os.path.isfile(file_path):
								#f = open(file_path, 'a')
								#f.write(name+'\n')
								#f.close()
								write_files(file_path,name,line_by_line=True)
							
							
							o = os.listdir(path_Local_Dir)
							
							o=naturallysorted(o)
							epnArrList[:]=[]
							for i in o:
								if not i.startswith('.') and (i.endswith('.mkv') or i.endswith('.mp4' ) or i.endswith('.avi') or i.endswith('.flv') ):
									j = path_Local_Dir+'/'+i
									m.append(i)
									epnArrList.append(i+'	'+j)
							picn = os.path.join(home,'Local',name,'poster.jpg')
							fanart = os.path.join(home,'Local',name,'fanart.jpg')
							thumbnail = os.path.join(home,'Local',name,'thumbnail.jpg')
							summary1 = os.path.join(home,'Local',name,'summary.txt')
							if os.path.exists(summary1):
								summary = open_files(summary1,False)
							else:
								summary = "Not Available"
							print (picn)
							self.videoImage(picn,thumbnail,fanart,summary)
				
				else:
					if os.path.exists(os.path.join(home,'History',site,name,'Ep.txt')):
						
						#lines = tuple(open(os.path.join(home,'History',site,name,'Ep.txt'), 'r'))
						#with open(home+'/History/'+site+'/'+name+'/Ep.txt') as f:
						#items = f.readlines()
						lines = open_files(os.path.join(home,'History',site,name,'Ep.txt'),True)
						m = []
						
						epnArrList[:]=[]
						for i in lines:
							i = re.sub("\n","",i)
							epnArrList.append(i)
							if (site == "Local" or finalUrlFound == True):
								j = i.split('	')[0]
								if "#" in i:
									j = "#"+j
							else:
								j = i
							m.append(j)
								
						picn = os.path.join(home,'History',site,name,'poster.jpg')
						fanart = os.path.join(home,'History',site,name,'fanart.jpg')
						thumbnail = os.path.join(home,'History',site,name,'thumbnail.jpg')
						m.append(picn)
						#try:
						#	g = open(os.path.join(home,'History',site,name,'summary.txt'), 'r')
						#	summary = g.read()
							#m = lines + tuple(picn) + tuple(summary)
						#	g.close()
						#except:
						#	summary = "Not Available"
						summary = open_files(os.path.join(home,'History',site,name,'summary.txt'),False)
						self.videoImage(picn,thumbnail,fanart,summary)
				
				
			
				if not os.path.exists(os.path.join(home,'History',site,name)):
					print (name)
					os.makedirs(os.path.join(home,'History',site,name))
					file_ep = os.path.join(home,'History',site,name+'Ep.txt')
					#f = open(os.path.join(home,'History',site,name+'Ep.txt'), 'w')
					k_arr = []
					for i in m:
						j = os.path.join(path_Local_Dir,i)
						#f.write(i+'	'+j+'\n')
						k_arr.append(i+'	'+j)
					#f.close()
					write_files(file_ep,k_arr,line_by_line=True)
					file_sum = os.path.join(home,'History',site,name,'summary.txt')
					#g = open(os.path.join(home,'History',site,name,'summary.txt'), 'w')
					#try:
					#	g.write(str(summary))
					#except:
					#	g.write(summary.encode('utf-8'))
					#g.close()
					write_files(file_sum,summary,line_by_line=False)
					if os.path.isfile(picn):
						shutil.copy(picn,os.path.join(home,'History',site,name,'poster.jpg'))
					if os.path.isfile(fanart):
						shutil.copy(fanart,os.path.join(home,'History',site,name,'fanart.jpg'))
				#self.update_list2()
				
				
		elif site == "Music":
			try:
				art_n = str(self.list1.currentItem().text())
			except:
				return 0
			music_dir = os.path.join(home,'Music')
			
								
			music_db = os.path.join(home,'Music','Music.db')
			music_file = os.path.join(home,'Music','Music.txt')
			music_file_bak = os.path.join(home,'Music','Music_bak.txt')
			if bookmark == "False":
				if not self.list3.currentItem():
					self.list3.setCurrentRow(0)
				music_opt = self.list3.currentItem().text()
					
			artist =[]
			
			#if music_opt == "Artist":
			if music_opt == "Directory":
				index = self.list1.currentRow()
				art_n = original_path_name[index]
			if music_opt == "Fav-Directory":
				index = self.list1.currentRow()
				art_n = original_path_name[index]
			if music_opt == "Playlist":
				r = self.list1.currentRow()
				item = self.list1.item(r)
				if item:
					pls = str(item.text())
					#f = open(os.path.join(home,'Playlists',pls),'r')
					#m = f.readlines()
					#f.close()
					m = open_files(os.path.join(home,'Playlists',pls),True)
					#print m
					for i in m:
						i = i.replace('\n','')
						if i:
							j = i.split('	')
							i1 = j[0]
							i2 = j[1]
							try:
								i3 = j[2]
							except:
								i3 = "None"
							artist.append(i1+'	'+i2+'	'+i3)
			else:
				m = self.getMusicDB(music_db,music_opt,art_n)
				for i in m:
					artist.append(i[1]+'	'+i[2]+'	'+i[0])
			#artist = list(set(artist))
			epnArrList[:]=[]
			self.list2.clear()
			for i in artist:
				try:
					epnArrList.append(str(i))
				except:
					epnArrList.append((i))
				
			self.musicBackground(0,'offline')
		elif site == "PlayLists":
			#self.list1.clear()
			
			self.list2.clear()
			
			r = self.list1.currentRow()
			item = self.list1.item(r)
			epnArrList[:]=[]
			if item:
				pls = self.list1.currentItem().text()
				file_path = os.path.join(home,'Playlists',str(pls))
				if os.path.exists(file_path):
					#f = open(file_path)
					#lines = f.readlines()
					#f.close()
					lines = open_files(file_path,True)
					k = 0
					for i in lines:
						i = i.replace('\n','')
						if i:	
							epnArrList.append(i)
							
		elif site == "Video":
			r = self.list1.currentRow()
			item = self.list1.item(r)
			if item:
				art_n = str(self.list1.currentItem().text())
				name = art_n
				video_dir = os.path.join(home,'VideoDB')
				
				video_db = os.path.join(video_dir,'Video.db')
				video_file = os.path.join(video_dir,'Video.txt')
				video_file_bak = os.path.join(video_dir,'Video_bak.txt')
				
				
				artist =[]
				if bookmark == "False":
					if self.list3.currentItem():
						video_opt = str(self.list3.currentItem().text())
					else:
						video_opt = 'History'
					if video_opt == "Update" or video_opt == "UpdateAll":
						video_opt = "Available"
					if video_opt == "Available" or video_opt == "History":
						index = self.list1.currentRow()
						art_n = original_path_name[index].split('	')[-1]
						#art_n = str(self.list1.currentItem().text())
						m = self.getVideoDB(video_db,"Directory",art_n)
					#if music_opt == "Artist":
					elif video_opt == "Directory":
						index = self.list1.currentRow()
						art_n = original_path_name[index].split('	')[-1]
						m = self.getVideoDB(video_db,video_opt,art_n)
				else:
					m = self.getVideoDB(video_db,"Bookmark",art_n)
				#for i in m:
				#	print i[0] + '--'+i[1] + '---'+i[2]
				for i in m:
					artist.append(i[0]+'	'+i[1])
				#artist = list(set(artist))
				#artist = naturallysorted(artist)
				epnArrList[:]=[]
				self.list2.clear()
				for i in artist:
					epnArrList.append((i))
					#print i
					#i = i.split('	')[0]
					#i = i.replace('_',' ')
					#if i.startswith('#'):
					#	i = i.replace('#',self.check_symbol,1)
					#self.list2.addItem(i)
				art_n = str(self.list1.currentItem().text())
				dir_path = os.path.join(home,'Local',art_n)
				if os.path.exists(dir_path):
					picn = os.path.join(home,'Local',art_n,'poster.jpg')
					thumbnail = os.path.join(home,'Local',art_n,'thumbnail.jpg')
					fanart = os.path.join(home,'Local',art_n,'fanart.jpg')
					summary1 = os.path.join(home,'Local',art_n,'summary.txt')
					if os.path.exists(summary1):
						#summary = open(summary1,'r').read()
						summary = open_files(summary1,False)
					else:
						summary = "Not Available"
					
					self.videoImage(picn,thumbnail,fanart,summary)
						
					print (picn)
				else:
					os.makedirs(dir_path)
		self.current_background = fanart
		self.update_list2()
		
	def set_list_thumbnail(self,k):
		global epnArrList
		if self.list_with_thumbnail:
			#for k in range(self.list2.count()):
			icon_name = self.get_thumbnail_image_path(k,epnArrList[k])
			if os.path.exists(icon_name):
				self.list2.item(k).setIcon(QtGui.QIcon(icon_name))
					
	def musicBackground(self,val,srch):
		global name,epnArrList,artist_name_mplayer,site
		
		if self.list3.currentItem() and site.lower() == 'music':
			if self.list3.currentItem().text().lower() == "artist":
				artist_mode = True
			else:
				artist_mode = False
		else:
			artist_mode = False
		print(artist_mode,'----artist--mode---')
		if artist_mode:
			music_dir_art = os.path.join(home,'Music','Artist')
			if not os.path.exists(music_dir_art):
				os.makedirs(music_dir_art)
			if self.list1.currentItem():
				if srch != "Queue":
					nm = str(self.list1.currentItem().text())
					if '/' in nm:
						nm = nm.replace('/','-')
				else:
					nm = artist_name_mplayer
				music_dir_art_name = os.path.join(home,'Music','Artist',nm)
				print(music_dir_art_name)
				if not os.path.exists(music_dir_art_name):
					os.makedirs(music_dir_art_name)
				else:
					art_list = os.listdir(music_dir_art_name)
					sumr = os.path.join(music_dir_art_name,'bio.txt')
					if os.path.exists(sumr):
						summary = open_files(sumr,False)
						
						#summary = open(sumr,'r').read()
					else:
						summary = "Not Available"
					
					poster = os.path.join(music_dir_art_name,'poster.jpg')
					fan = os.path.join(music_dir_art_name,'fanart.jpg')
					thumb = os.path.join(music_dir_art_name,'thumbnail.jpg')
					if not os.path.exists(poster) and srch != "offline":	
						#self.threadEx = ThreadingExample(name)
						self.threadPool.append( ThreadingExample(nm) )
						self.threadPool[len(self.threadPool)-1].finished.connect(lambda x=nm: self.finishedM(nm))
						#self.threadEx.start()
						self.threadPool[len(self.threadPool)-1].start()
					else:
						self.videoImage(poster,thumb,fan,summary)
		else:
			music_dir_art = os.path.join(home,'Music','Artist')
			print(music_dir_art,'--music-dir-art--')
			try:
				if srch != "Queue":
					nm = epnArrList[val].split('	')[2]
				else:
					nm = artist_name_mplayer
			except:
				nm = ""
			print (nm)
			if nm:
				if '/' in nm:
					nm = nm.replace('/','-')
				music_dir_art_name = os.path.join(home,'Music','Artist',nm)
				print(music_dir_art_name,'--music-dir-art-name--')
				if not os.path.exists(music_dir_art_name):
					os.makedirs(music_dir_art_name)
					
				else:
					art_list = os.listdir(music_dir_art_name)
					sumr = os.path.join(music_dir_art_name,'bio.txt')
					if os.path.exists(sumr):
						#summary = open(sumr,'r').read()
						summary = open_files(sumr,False)
					else:
						summary = "Not Available"
					poster = os.path.join(music_dir_art_name,'poster.jpg')
					fan = os.path.join(music_dir_art_name,'fanart.jpg')
					thumb = os.path.join(music_dir_art_name,'thumbnail.jpg')
					if not os.path.exists(poster) and srch != "offline" and artist_name_mplayer != "None" and artist_name_mplayer:	
						
						self.threadPool.append( ThreadingExample(nm) )
						self.threadPool[len(self.threadPool)-1].finished.connect(lambda x=nm: self.finishedM(nm))
						self.threadPool[len(self.threadPool)-1].start()
					else:
						self.videoImage(poster,thumb,fan,summary)
						
	def videoImage(self,picn,thumbnail,fanart,summary):
		global screen_height,screen_width
		#self.label.clear()
		try:
			if os.path.isfile(str(picn)):
				if not os.path.isfile(fanart):
					basewidth = screen_width
					try:
						img = Image.open(str(picn))
					except Exception as e:
						print(e,'Error in opening image, videoImage,---13849')
						picn = os.path.join(home,'default.jpg')
						img = Image.open(str(picn))
					wpercent = (basewidth / float(img.size[0]))
					#hsize = int((float(img.size[1]) * float(wpercent)))
					hsize = screen_height
					img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
					img.save(str(fanart))
				if not os.path.isfile(thumbnail):
					basewidth = 450
					try:
						img = Image.open(str(picn))
					except Exception as e:
						print(e,'Error in opening image, videoImage,---13861')
						picn = os.path.join(home,'default.jpg')
						img = Image.open(str(picn))
					wpercent = (basewidth / float(img.size[0]))
					hsize = int((float(img.size[1]) * float(wpercent)))
					
					img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
					img.save(str(thumbnail))
				picn = thumbnail	
				tmp = '"background-image: url('+fanart+')"'
				
				tmp1 = '"font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%)"'
				QtCore.QTimer.singleShot(100, partial(set_mainwindow_palette,fanart))
				
				#self.dockWidget_3.hide()

				img = QtGui.QPixmap(picn, "1")
				self.label.setPixmap(img)
				if not self.float_window.isHidden():
					self.float_window.setPixmap(img)
		except Exception as e:
			print(e,'--error--in processing image--VideoImage 13883')
		self.text.clear()
		if summary:
			#self.text.clear()
			self.text.insertPlainText((summary))
		else:
			self.text.insertPlainText("No Summary Available")
			
	def playlistUpdate(self):
		global home,epnArrList
		row = self.list2.currentRow()
		item = self.list2.item(row)
		if item:
			i = str(self.list2.item(row).text())
			#j = self.list2.item(row)
			#self.list2.takeItem(row)
			#del j
			if not i.startswith(self.check_symbol):
				#self.list2.insertItem(row,self.check_symbol+i)
				self.list2.item(row).setText(self.check_symbol+i)
				epnArrList[row] = '#'+epnArrList[row]
			else:
				#self.list2.insertItem(row,i)
				self.list2.item(row).setText(i)
			#self.list2.item(row).setFont(QtGui.QFont('SansSerif', 10,italic=True))
			self.list2.setCurrentRow(row)
			if self.list1.currentItem():
				file_path = os.path.join(home,'Playlists',self.list1.currentItem().text())
				"""
				if os.path.exists(file_path):
					f = open(file_path,'w')
					k = 0
					for i in range(self.list2.count()):
						#it = str(self.list2.item(i).text())
						it = epnArrList[i]
						#it = it.encode('utf8')
						if k == 0:
							f.write(it)
						else:
							f.write('\n'+it)
						k = k+1
					f.close()
				"""
				write_files(file_path,epnArrList,line_by_line=True)
				
	def get_file_name(self,row,list_widget):
		global name,site,epnArrList
		file_name_mkv = ''
		file_name_mp4 = ''
		if list_widget.item(row):
			new_epn = list_widget.item(row).text().replace('#','')
		else:
			new_epn = ''
		if new_epn.startswith(self.check_symbol):
			new_epn = new_epn[1:]
		new_epn = new_epn.replace('/','-')
		new_epn = new_epn.replace('"','')
		new_epn = re.sub('"|.mkv|.mp4','',new_epn)
		if new_epn.startswith('.'):
			new_epn = new_epn[1:]
		opt_val = self.btn1.currentText().lower()
		
		try:
			if site.lower() == 'playlists' or(site.lower() == 'music' and self.list3.currentItem().text().lower() == 'playlist'):
				try:
					title = self.list1.currentItem().text()
				except:
					title = name
			else:
				title = name
		except:
			title = epnArrList[row].split('	')[0]
			file_name_mkv = epnArrList[row].split('	')[1]
			file_name_mp4 = epnArrList[row].split('	')[1]
			print('function ',file_name_mkv,file_name_mp4,'function get_file_name')
			return file_name_mp4,file_name_mkv
			
		if site.lower() != 'video' and site.lower() != 'music' and site.lower() != 'local' and site.lower() != 'playlists' and site.lower() != 'none':
			new_epn_mkv = new_epn+'.mkv'
			new_epn_mp4 = new_epn+'.mp4'
			file_name_mkv = os.path.join(self.default_download_location,title,new_epn_mkv)
			file_name_mp4 = os.path.join(self.default_download_location,title,new_epn_mp4)
		elif site.lower() == 'playlists' or opt_val == 'youtube' or (site.lower() == 'music' and self.list3.currentItem().text().lower() == 'playlist'):
			if list_widget == self.list2:
				st = epnArrList[row].split('	')[1]
			elif list_widget == self.list6:
				st = self.queue_url_list[row].split('	')[1]
			st = st.replace('"','')
			if 'youtube.com' in st:
				new_epn_mkv = new_epn+'.mp4'
				new_epn_mp4 = new_epn+'.mp4'
				file_name_mkv = os.path.join(self.default_download_location,title,new_epn_mkv)
				file_name_mp4 = os.path.join(self.default_download_location,title,new_epn_mp4)
			else:
				#new_epn_mkv = st.split('/')[-1]
				#new_epn_mp4 = st.split('/')[-1]
				new_epn_mkv = os.path.basename(st)
				new_epn_mp4 = new_epn_mkv
				file_name_mkv = st
				file_name_mp4 = st
		elif site.lower() == 'video' or site.lower() == 'music' or site.lower() == 'local' or site.lower() == 'none':
			if not self.queue_url_list:
				file_name_mkv = epnArrList[row].split('	')[1]
				file_name_mp4 = epnArrList[row].split('	')[1]
			else:
				queue_split = self.queue_url_list[row].split('	')
				if len(queue_split) > 1:
					file_name_mkv = queue_split[1]
					file_name_mp4 = queue_split[1]
		print('function ',file_name_mkv,file_name_mp4,'function get_file_name')
		return file_name_mp4,file_name_mkv
		
		
	def play_file_now(self,file_name):
		global Player,epn_name_in_list,mpvplayer,idw,quitReally,mplayerLength,current_playing_file_path
		mplayerLength = 0
		quitReally = 'no'
		print(file_name)
		#if site.lower() != 'music' and show_hide_player == 1: 
		#	self.text.hide()
		#	self.label.hide()
		if mpvplayer.processId() == 0:
			self.initial_view_mode()
		finalUrl = file_name.replace('"','')
		#if not finalUrl.startswith('http'):
		#	self.epn_name_in_list = finalUrl.split('/')[-1]
		#self.epn_name_in_list = re.sub('.mkv|.mp4|.avi','',self.epn_name_in_list)
		finalUrl = '"'+finalUrl+'"'
		if finalUrl.startswith('"http'):
			current_playing_file_path = finalUrl.replace('"','')
			finalUrl = finalUrl.replace('"','')
		else:
			current_playing_file_path = finalUrl
		if mpvplayer.processId() > 0 and OSNAME == 'posix':
			epnShow = '"' + "Queued:  "+ self.epn_name_in_list + '"'
			if Player == "mplayer":
				t1 = bytes('\n'+'show_text '+epnShow+'\n','utf-8')
				t2 = bytes('\n'+"loadfile "+finalUrl+" replace"+'\n','utf-8')
			elif Player == 'mpv':
				t1 = bytes('\n'+'show-text '+epnShow+'\n','utf-8')
				t2 = bytes('\n'+"loadfile "+finalUrl+'\n','utf-8')
			print (finalUrl,'---hello-----')
			mpvplayer.write(t1)
			mpvplayer.write(t2)
			if self.mplayer_SubTimer.isActive():
				self.mplayer_SubTimer.stop()
			self.mplayer_SubTimer.start(2000)
			print('..function play_file_now gapless mode..')
		else:
			if mpvplayer.processId()>0:
				mpvplayer.kill()
				
			idw = str(int(self.tab_5.winId()))
			if Player == 'mpv':
				command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+finalUrl
			
			else:
				#command = "mplayer -identify -nocache -idle -msglevel all=4:statusline=5:global=6 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
				command = "mplayer -identify -idle -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
			print(command,'function play_file_now')
			self.infoPlay(command)
		if not self.external_SubTimer.isActive():
			self.external_SubTimer.start(3000)
	def is_artist_exists(self,row):
		global epnArrList
		try:
			arr = epnArrList[row].split('	')
		except:
			return False
		artist = ''
		if len(arr) >=3 :
			artist = arr[2].replace('"','')
		if artist.lower() and (artist.lower() != 'none') and not artist.startswith('http'):
			return True
		else:
			return False
	def if_file_path_exists_then_play(self,row,list_widget,play_now=None):
		global site,downloadVideo,wget,video_local_stream,artist_name_mplayer
		
		file_path_name_mp4, file_path_name_mkv = self.get_file_name(row,list_widget)
		
		if (os.path.exists(file_path_name_mp4) or os.path.exists(file_path_name_mkv)) and (site.lower() != 'video' and site.lower() != 'music' and site.lower() != 'local') and not video_local_stream:
			print('now--playing',file_path_name_mp4,file_path_name_mkv)
			if play_now:
				self.epn_name_in_list = list_widget.item(row).text().replace('#','')
				if self.epn_name_in_list.startswith(self.check_symbol):
					self.epn_name_in_list = self.epn_name_in_list[1:]
				if os.path.exists(file_path_name_mp4):
					self.play_file_now(file_path_name_mp4)
					finalUrl = file_path_name_mp4
				else:
					self.play_file_now(file_path_name_mkv)
					finalUrl = file_path_name_mkv
				finalUrl = '"'+finalUrl+'"'
				if site.lower() == 'playlists':
					if self.is_artist_exists(row):
						self.musicBackground(row,'get now')
						self.updateMusicCount('count',finalUrl)
				else:
					self.mark_addons_history_list('mark',row)
				return True
			else:
				if os.path.exists(file_path_name_mp4):
					return file_path_name_mp4
				else:
					return file_path_name_mkv
		elif site.lower() == 'music' and self.list3.currentItem() and (os.path.exists(file_path_name_mp4) or os.path.exists(file_path_name_mkv)) and not video_local_stream:
			if self.list3.currentItem().text().lower() == 'playlist':
				print('now--playing',file_path_name_mp4,file_path_name_mkv)
				if play_now:
					self.epn_name_in_list = list_widget.item(row).text().replace('#','')
					if self.epn_name_in_list.startswith(self.check_symbol):
						self.epn_name_in_list = self.epn_name_in_list[1:]
					if os.path.exists(file_path_name_mp4):
						self.play_file_now(file_path_name_mp4)
						finalUrl = file_path_name_mp4
					else:
						self.play_file_now(file_path_name_mkv)
						finalUrl = file_path_name_mkv
					if list_widget == self.list6:
						txt = self.list6.item(0).text()
						r = self.get_index_list(list_widget,txt)
						self.list2.setCurrentRow(r)
					else:
						r = row
					finalUrl = '"'+finalUrl+'"'
					self.musicBackground(r,'Search')
					self.updateMusicCount('count',finalUrl)
					return True
				else:
					if os.path.exists(file_path_name_mp4):
						return file_path_name_mp4
					else:
						return file_path_name_mkv
		elif (os.path.exists(file_path_name_mp4) or os.path.exists(file_path_name_mkv)) and (site.lower() == 'video' or site.lower() == 'music' or site.lower() == 'local' or site.lower() == 'none') and not video_local_stream:
			print('now--playing',file_path_name_mp4,file_path_name_mkv)
			if play_now:
				if list_widget.item(row):
					self.epn_name_in_list = list_widget.item(row).text().replace('#','')
				
					
				if self.epn_name_in_list.startswith(self.check_symbol):
					self.epn_name_in_list = self.epn_name_in_list[1:]
				if os.path.exists(file_path_name_mp4):
					self.play_file_now(file_path_name_mp4)
					finalUrl = file_path_name_mp4
				else:
					self.play_file_now(file_path_name_mkv)
					finalUrl = file_path_name_mkv
					
				if list_widget == self.list6:
					txt = self.list6.item(0).text()
					r = self.get_index_list(list_widget,txt)
					self.list2.setCurrentRow(r)
				else:
					r = row
					
				finalUrl = finalUrl.replace('"','')
				finalUrl = '"'+finalUrl+'"'
				if site.lower() == "music":
					print (finalUrl)
					try:
						artist_name_mplayer = epnArrList[row].split('	')[2]
						if artist_name_mplayer.lower() == "none":
							artist_name_mplayer = ""
					except:
						artist_name_mplayer = ""
					if not 'youtube.com' in finalUrl.lower():
						self.musicBackground(r,'Search')
						self.updateMusicCount('count',finalUrl)
				elif site.lower() == "video":
					self.mark_video_list('mark',row)
					self.updateVideoCount('mark',finalUrl)
				elif site.lower() == 'local':
					self.mark_addons_history_list('mark',row)
				return True
			else:
				if os.path.exists(file_path_name_mp4):
					return file_path_name_mp4
				else:
					return file_path_name_mkv
		elif wget.processId() > 0 and play_now:
			return True
		else:
			return False
			
	def get_index_list(self,list_widget,txt):
		r = 0
		txt = txt.replace('#','')
		if txt.startswith(self.check_symbol):
				txt = txt[1:]
		for i in range(self.list2.count()):
			new_txt = self.list2.item(i).text()
			new_txt = new_txt.replace('#','')
			if new_txt.startswith(self.check_symbol):
				new_txt = new_txt[1:]
			if new_txt == txt:
				r = i
				break
		return r
	def set_init_settings(self):
		
		global music_arr_setting,default_arr_setting
		if site == "Music":
			if self.list3.currentRow() >= 0:
				music_arr_setting[0]=self.list3.currentRow()
				if self.list1.currentRow() >= 0:
					music_arr_setting[1]=self.list1.currentRow()
					if self.list2.currentRow() >= 0:
						music_arr_setting[2]=self.list2.currentRow()
		else:
			if ui.btn1.currentIndex() > 0:
				default_arr_setting[0]=ui.btn1.currentIndex()
				if self.list3.currentRow() >= 0:
					default_arr_setting[1]=self.list3.currentRow()
					if self.list1.currentRow() >= 0:
						default_arr_setting[2]=self.list1.currentRow()
						if self.list2.currentRow() >= 0:
							default_arr_setting[3]=self.list2.currentRow()
				if ui.btnAddon.currentIndex() >= 0:
					default_arr_setting[4]=ui.btnAddon.currentIndex()
					
	
			
	def epnfound(self):
		global site,base_url,embed,epn,epn_goto,mirrorNo,list2_items,quality,finalUrl,home,hdr,path_Local_Dir,epnArrList,epn_name_in_list,siteName,finalUrlFound,refererNeeded,show_hide_player,show_hide_cover
		global mpv,mpvAlive,downloadVideo,indexQueue,Player,startPlayer,mpvplayer,new_epn,idw,home1,quitReally,buffering_mplayer,opt_movies_indicator,name,artist_name_mplayer,rfr_url,server,current_playing_file_path,music_arr_setting,default_arr_setting,local_torrent_file_path,video_local_stream
		buffering_mplayer="no"
		self.list4.hide()
		self.player_play_pause.setText(self.player_buttons['pause'])
		quitReally = "no"
		
		try:
			
			server._emitMeta("Play",site,epnArrList)
		except:
			pass
		
		
		
		if video_local_stream:
			tmp_pl = os.path.join(TMPDIR,'player_stop.txt')
			if os.path.exists(tmp_pl):
				os.remove(tmp_pl)
			
		if mpvplayer.processId() > 0 and (current_playing_file_path.startswith('http') or current_playing_file_path.startswith('"http')):
			mpvplayer.kill()
			if Player == 'mplayer':
				if mpvplayer.processId() > 0:
					try:
						subprocess.Popen(['killall','mplayer'])
					except Exception as e:
						print(e)
			mpvplayer = QtCore.QProcess()
	
		if epn_goto == 0 and site != "PlayLists" and downloadVideo == 0:
			epn = (self.list2.currentItem().text())
			self.epn_name_in_list = epn
			if not epn:
				return 0
			
			
			row = self.list2.currentRow()
			
			if '	' in epnArrList[row]:
				epn = (epnArrList[row]).split('	')[1]
			else:
				epn = epnArrList[row].replace('#','')
			epn = epn.replace('#','')
			if epn.startswith(self.check_symbol):
				epn = epn[1:]
		
		
		
		
				
		#self.goto_epn.clear()
		#self.goto_epn.setText(epn)
		self.set_init_settings()
		
		
		row = self.list2.currentRow()
		if self.if_file_path_exists_then_play(row,self.list2,True):
			self.initial_view_mode()
			return 0
		
		if(site != "SubbedAnime" and site!= "DubbedAnime" and site!="PlayLists" and finalUrlFound == False and site !="None" and site!= "Music" and site != "Video" and site!= "Local") :
			hist_path = os.path.join(home,'History',site,name,'Ep.txt')
			if (os.path.exists(hist_path) and (epn_goto == 0)) or (os.path.exists(hist_path) and bookmark == "True"):
					if epnArrList[row].startswith('#'):
						n_epn = epnArrList[row]
						txt = n_epn.replace('#',self.check_symbol,1)
						
					else:
						n_epn = '#'+epnArrList[row]
						file_path = hist_path
						#f = open(file_path, 'r')
						#lines = f.readlines()
						#f.close()
						lines = open_files(file_path,True)
						if "\n" in lines[row]:
							lines[row] = n_epn + "\n"
						else:
							lines[row] = n_epn
						"""
						f = open(file_path, 'w')
						for i in lines:
							f.write(i)
						f.close()
						"""
						write_files(file_path,lines,line_by_line=True)
						txt = self.check_symbol + epnArrList[row]
					txt = txt.replace('_',' ',1)
					if '	' in txt:
						txt = txt.split('	')[0]
					self.list2.item(row).setText(txt)
					
			else:
				i = str(self.list2.item(row).text())
				i = i.replace('_',' ')
				#j = self.list2.item(row)
				#self.list2.takeItem(row)
				#del j
				if not i.startswith(self.check_symbol):
					#self.list2.insertItem(row,self.check_symbol+i)
					self.list2.item(row).setText(self.check_symbol+i)
				else:
					#self.list2.insertItem(row,i)
					self.list2.item(row).setText(i)
				self.list2.item(row).setFont(QtGui.QFont('SansSerif', 10,italic=True))
				self.list2.setCurrentRow(row)
			if site != "Local":
				
				
				self.progressEpn.setFormat('Wait..')
				if video_local_stream:
					if self.thread_server.isRunning():
						if self.do_get_thread.isRunning():
							#row_file = '/tmp/AnimeWatch/row.txt'
							row_file = os.path.join(TMPDIR,'row.txt')
							f = open(row_file,'w')
							f.write(str(row))
							f.close()
							finalUrl = "http://"+self.local_ip+':'+str(self.local_port)+'/'
						else:
							finalUrl,self.do_get_thread,self.stream_session,self.torrent_handle = self.site_var.getFinalUrl(name,row,self.local_ip+':'+str(self.local_port),'Next',self.torrent_download_folder,self.stream_session,ui.list6,ui.progress,ui.tmp_download_folder)
					else:
						#self.list6.clear()
						finalUrl,self.thread_server,self.do_get_thread,self.stream_session,self.torrent_handle = self.site_var.getFinalUrl(name,row,self.local_ip+':'+str(self.local_port),'First Run',self.torrent_download_folder,self.stream_session,ui.list6,ui.progress,ui.tmp_download_folder)
					self.torrent_handle.set_upload_limit(self.torrent_upload_limit)
					self.torrent_handle.set_download_limit(self.torrent_download_limit)
					#self.do_get_thread.session_signal.connect(self.session_finished)
				else:
					finalUrl = self.site_var.getFinalUrl(name,epn,mirrorNo,quality)
				#except:
				#	print('final url not Available')
				#	return 0
				#del site_var
		elif site == "PlayLists":
			row = self.list2.currentRow()
			item = self.list2.item(row)
			if item:
				#line = str(self.list2.currentItem().text())
				arr = epnArrList[row].split('	')
				#arr[1] = '"'+arr[1]+'"'
				
				#if arr[2] == "NONE" or arr[2].startswith('"/') or arr[2].startswith('/'):
				if len(arr) > 2:
					if arr[2].startswith('http') or arr[2].startswith('"http'):
						finalUrl = []
						finalUrl.append(arr[1])
						finalUrl.append(arr[2])
						refererNeeded = True
					else:
						finalUrl = arr[1]
						refererNeeded = False
				else:
					finalUrl = arr[1]
					#finalUrl = finalUrl.decode('utf8')
					refererNeeded = False
				self.epn_name_in_list = arr[0]
				epn = self.epn_name_in_list
				self.playlistUpdate()
				if 'youtube.com' in finalUrl:
					finalUrl = get_yt_url(finalUrl,quality).strip()
		elif finalUrlFound == True:
				row_num = self.list2.currentRow()
			
				final = epnArrList[row_num]
				print (final)
				self.mark_History()
				finalUrl = []
				final = final.replace('#','')
				
				if '	' in final:
					final = final.split('	')[1]
				#final = final.decode('utf8')
				finalUrl.append(final)
				if refererNeeded == True:
					if '	' in epnArrList[row_num]:
						rfr_url = epnArrList[row_num].split('	')[2]
					finalUrl.append(rfr_url)
				if len(finalUrl) == 1:
					finalUrl = finalUrl[0]
				print (finalUrl)
				print ("++++++++++++++++++++")
		elif site == "SubbedAnime" or site == "DubbedAnime":
			if category != "Movies":
				file_path = os.path.join(home,'History',site,siteName,name,'Ep.txt')
		
				if os.path.exists(file_path) and (epn_goto == 0):
					if '#' in epnArrList[row]:
						n_epn = epnArrList[row]
						txt = n_epn.replace('#',self.check_symbol,1)
					else:
						n_epn = "#" + epnArrList[row]
						#f = open(file_path, 'r')
						#lines = f.readlines()
						#f.close()
						lines = open_files(file_path,True)
						if "\n" in lines[row]:
							lines[row] = n_epn + "\n"
						else:
							lines[row] = n_epn
						
						#f = open(file_path, 'w')
						#for i in lines:
						#	f.write(i)
						#f.close()
						write_files(file_path,lines,line_by_line=True)
						txt = self.check_symbol + epnArrList[row]
					txt = txt.replace('_',' ',1)
					self.list2.item(row).setText(txt)
					"""
					lines = tuple(open(file_path, 'r'))
					self.list2.clear()
					k = 0
					epnArrList[:]=[]
					for i in lines:
						i = i.replace('\n','')
						epnArrList.append(i)
						if '	' in i:
							i = i.split('	')[0]
							if i.startswith('#'):
								i = i.replace('#',self.check_symbol,1)
								self.list2.addItem((i))
								self.list2.item(k).setFont(QtGui.QFont('SansSerif', 10,italic=True))
							else:
								self.list2.addItem((i))
						k = k+1
					"""
			if site == "SubbedAnime":
				code = 6
			
				if base_url == 16:
				
					epn_t = epn.split(' ')[1]
					new_epn = epn.split(' ')[0]
				else:
				
					epn_t = epn
				if opt_movies_indicator:
					r = self.list2.currentRow()
					self.epn_name_in_list = self.list2.currentItem().text()
					
					if cmd:
						self.progressEpn.setFormat('Wait..')
						QtWidgets.QApplication.processEvents()
						try:
							finalUrl = self.site_var.urlResolve(epnArrList[r].split('	')[1])
						except:
							return 0
				else:
					
					if self.site_var:
						self.progressEpn.setFormat('Wait..')
						QtWidgets.QApplication.processEvents()
						try:
							finalUrl = self.site_var.getFinalUrl(siteName,name,epn,mirrorNo,category,quality) 
						except:
							return 0
				if category == "Movies" and not opt_movies_indicator and (type(finalUrl) is list):
					self.list2.clear()
					epnArrList[:]=[]
					j = 1
					for i in finalUrl:
						epnArrList.append("Part-"+str(j)+'	'+i)
						self.list2.addItem("Part-"+str(j))
						j = j+1
					opt_movies_indicator.append("Movies")
					self.list2.setCurrentRow(0)
					self.list2.setFocus()
					
					if self.site_var:
						
						
						self.progressEpn.setFormat('Wait..')
						QtWidgets.QApplication.processEvents()
						try:
							finalUrl = self.site_var.urlResolve(epnArrList[0].split('	')[1])
						except:
							return 0
					self.epn_name_in_list = name+"-"+self.list2.currentItem().text()
				
			elif site == "DubbedAnime":
				code = 5
				
				if self.site_var:
					
					self.progressEpn.setFormat('Wait..')
					QtWidgets.QApplication.processEvents()
					try:
						finalUrl = self.site_var.getFinalUrl(siteName,name,epn,mirrorNo,quality) 
					except:
						return 0
		
		elif site == "None" or site == "Music" or site == "Video" or site == "Local":
			if site == "Local" and opt == "History":
				self.mark_History()
			if '	' in epnArrList[row]:
					finalUrl = '"'+(epnArrList[row]).split('	')[1]+'"'
			else:
					finalUrl = '"'+(epnArrList[row]).replace('#','')+'"'
			#finalUrl = finalUrl.decode('utf8')
			print (finalUrl)
			i = str(self.list2.item(row).text())
			i = i.replace('_',' ')
			#j = self.list2.item(row)
			#self.list2.takeItem(row)
			#del j
			if not i.startswith(self.check_symbol):
				#self.list2.insertItem(row,self.check_symbol+i)
				self.list2.item(row).setText(self.check_symbol+i)
			else:
				#self.list2.insertItem(row,i)
				self.list2.item(row).setText(i)
			self.list2.item(row).setFont(QtGui.QFont('SansSerif', 10,italic=True))
			self.list2.setCurrentRow(row)
			
			
			
			if site == "Music":
				print (finalUrl)
				try:
					artist_name_mplayer = epnArrList[row].split('	')[2]
					if artist_name_mplayer == "None":
						artist_name_mplayer = ""
				except:
					artist_name_mplayer = ""
				if not 'youtube.com' in finalUrl.lower():
					self.updateMusicCount('count',finalUrl)
			elif site == "Video":
				self.updateVideoCount('mark',finalUrl)
			elif site == 'None' and video_local_stream:
					finalUrl = self.local_torrent_open(local_torrent_file_path)
			elif site == 'None' and self.btn1.currentText().lower() == 'youtube':
					finalUrl = finalUrl.replace('"','')
					finalUrl = get_yt_url(finalUrl,quality).strip()
					finalUrl = '"'+finalUrl+'"'
			if 'youtube.com' in finalUrl.lower():
				finalUrl = finalUrl.replace('"','')
				finalUrl = get_yt_url(finalUrl,quality).strip()
				finalUrl = '"'+finalUrl+'"'
		#f = open(home+"/History/pl.txt","a")
		#g = open(home+"/History/queue.m3u","a")
		#h = open(home1+"/.kodi/userdata/playlists/video/queue.m3u","a")
		new_epn = self.epn_name_in_list
		#f.close()
		#g.close()
		#h.close()
		
		idw = str(int(self.tab_5.winId()))
		print(self.tab_5.winId(),'----winID---',idw)
		if site != "Music":
			self.tab_5.show()
			##self.tab_5.setFocus()
		#self.tab_5.setMinimumSize(500,500)
		#idw = str(self.tab_5.winId())
		print (finalUrl)
		print ("***********")
		if site == "Local" or site == "Video" or site == "Music" or site == "None" or site == "PlayLists" and (not type(finalUrl) is list or (type(finalUrl) is list and len(finalUrl) == 1)) and downloadVideo == 0:
			if type(finalUrl) is list:
				finalUrl = finalUrl[0]
			#if '""' in finalUrl:
			finalUrl = finalUrl.replace('"','')
			if '#' in finalUrl:
				if mpvplayer.processId() > 0:
					mpvplayer.kill()
				video_url = finalUrl.split('#')[-1]
				audio_url = finalUrl.split('#')[0]
				if Player == 'mplayer':
					if mpvplayer.processId() > 0:
						try:
							subprocess.Popen(['killall','mplayer'])
						except:
							pass
					command = "mplayer -identify -idle -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+video_url+' -audiofile '+audio_url
				else:
					command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+' --audio-file='+audio_url+' '+video_url
				self.infoPlay(command)
			else:
				finalUrl = '"'+finalUrl+'"'
				try:
					finalUrl = str(finalUrl)
				except:
					finalUrl = finalUrl
				if mpvplayer.processId() > 0:
					mpvplayer.kill()
				if Player == "mpv":
					command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+finalUrl
					print (command)
					self.infoPlay(command)
				elif Player == "mplayer":
					if mpvplayer.processId() > 0:
						try:
							subprocess.Popen(['killall','mplayer'])
						except:
							pass
					quitReally = "no"
					
					idw = str(int(self.tab_5.winId()))
					if site != "Music":
						self.tab_5.show()
						##self.tab_5.setFocus()
					if finalUrl.startswith('"http'):
						command = "mplayer -identify -nocache -idle -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
					else:
						command = "mplayer -identify -nocache -idle -msglevel all=4:statusline=5:global=6 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
					print (command)
					self.infoPlay(command)
				else:
					finalUrl = finalUrl.replace('"','')
					subprocess.Popen([Player, finalUrl], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
				if site == "Music":
					self.list2.setFocus()
					r = self.list2.currentRow()
					self.musicBackground(r,'Search')
				
		else:
		
			if downloadVideo == 0 and Player == "mpv":
				if mpvplayer.processId() > 0:
					mpvplayer.kill()
				if type(finalUrl) is list:
						if finalUrlFound == True or refererNeeded == True or site=="PlayLists":	
							if refererNeeded == True:
								rfr_url = finalUrl[1]
								nepn = '"'+str(finalUrl[0])+'"'
								
								command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 --referrer "+rfr_url+" -wid "+idw+" "+nepn
							else:
								nepn = str(finalUrl[0])
								command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+nepn
							print (command)
						
						else:
						
							self.queue_url_list[:]=[]
							epnShow = finalUrl[0]
							for i in range(len(finalUrl)-1):
								#epnShow = epnShow +' '+finalUrl[i+1]
								self.queue_url_list.append(finalUrl[i+1])
							self.queue_url_list.reverse()
							command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+epnShow
							
			
						self.infoPlay(command)
					
				else:
						if '""' in finalUrl:
							finalUrl = finalUrl.replace('""','"')
						try:
							finalUrl = str(finalUrl)
						except:
							finalUrl = finalUrl
						command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+finalUrl
						self.infoPlay(command)
					#if quitReally == "no":
					#	self.mpvNextEpnList()
				##self.tab_5.setFocus()
			elif downloadVideo == 0 and Player != "mpv":
				if mpvplayer.processId() > 0:
					mpvplayer.kill()
				if type(finalUrl) is list:
					if finalUrlFound == True or site=="PlayLists":
							if refererNeeded == True:
								rfr_url = finalUrl[1]
								if Player == "mplayer":
									if mpvplayer.processId() > 0:
										try:
											subprocess.Popen(['killall','mplayer'])
										except:
											pass
									quitReally = "no"
									idw = str(int(self.tab_5.winId()))
									self.tab_5.show()
									##self.tab_5.setFocus()
									final_url = str(finalUrl[0])
									command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" -referrer "+rfr_url+" "+'"'+final_url+'"'
									print (command)
									self.infoPlay(command)
								else:
									subprocess.Popen([Player,"-referrer",rfr_url,finalUrl[0]])
							else:
								if Player == "mplayer":
									if mpvplayer.processId() > 0:
										try:
											subprocess.Popen(['killall','mplayer'])
										except:
											pass
									quitReally = "no"
									idw = str(int(self.tab_5.winId()))
									self.tab_5.show()
									##self.tab_5.setFocus()
									final_url = str(finalUrl[0])
									command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+'"'+final_url+'"'
									print (command)
									self.infoPlay(command)
								else:
									final_url = str(finalUrl[0])
									subprocess.Popen([Player,final_url])
					else:
					
							if mpvplayer.processId() > 0:
								try:
									subprocess.Popen(['killall','mplayer'])
								except:
									pass
							epnShow = finalUrl[0]
							for i in range(len(finalUrl)-1):
								#epnShow = epnShow +' '+finalUrl[i+1]
								self.queue_url_list.append(finalUrl[i+1])
							self.queue_url_list.reverse()
							command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+epnShow
							print (command)
							self.infoPlay(command)
							#self.queue_url_list.pop()

				else:
				
						print (Player)
						print ("Final Url mplayer = "+finalUrl)
						if '""' in finalUrl:
							finalUrl = finalUrl.replace('""','"')
						finalUrl = str(finalUrl)
						if Player == "mplayer":
							if mpvplayer.processId() > 0:
								try:
									subprocess.Popen(['killall','mplayer'])
								except:
									pass
							quitReally = "no"
							idw = str(int(self.tab_5.winId()))
							self.tab_5.show()
							##self.tab_5.setFocus()
							command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
							print (command)
							self.infoPlay(command)
						else:
							finalUrl = re.sub('"',"",finalUrl)
							subprocess.Popen([Player, finalUrl], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
			elif downloadVideo == 1 and refererNeeded == False:
				if type(finalUrl) is list:
					
					
						j = 0
						length = len(finalUrl)
						for i in finalUrl:
							if length == 1:
								nepn1 = new_epn
							else:
								nepn1 = new_epn + "-Part-" + str(j+1)
							subprocess.Popen(["uget-gtk","--quiet=yes","--http-user-agent="+hdr,finalUrl[j],"--filename="+nepn1+".mp4"])
							j = j+1
				else:
					
						#filename = "--filename="
						finalUrl = finalUrl.replace('"','')
						self.list2.setFocus()
						r = self.list2.currentRow()
						print(r)
						new_epn = self.list2.item(row).text()
						if new_epn.startswith(self.check_symbol):
							new_epn = new_epn.replace(self.check_symbol,'',1)
						new_epn = new_epn.replace('/','-')
						new_epn = new_epn.replace('"','')
						if new_epn.startswith('.'):
							new_epn = new_epn[1:]
						if finalUrl.endswith('.mkv'):
							new_epn = new_epn+'.mkv'
						else:
							new_epn = new_epn+'.mp4'
						if site.lower() == 'playlists':
							title = self.list1.currentItem().text()
						else:
							title = name
						folder_name = os.path.join(self.default_download_location,title)
						if not os.path.exists(folder_name):
							os.makedirs(folder_name)
						npn = os.path.join(folder_name,new_epn)
						
						if finalUrl.startswith('http'):
							#command = "wget -c --read-timeout=60 --user-agent="+'"'+hdr+'" '+'"'+finalUrl+'"'+" -O "+'"'+npn+'"'
							command = wget_string(finalUrl,npn)
							print (command)
					
							self.infoWget(command,0)
				downloadVideo = 0
			elif refererNeeded == True and downloadVideo == 1:
			
			
				rfr = "--referer="+finalUrl[1]
				print (rfr)
				url1 = re.sub('#','',finalUrl[0])
				print (url1)
				url1 = str(url1)
				#command = "wget -c --user-agent="+'"'+hdr+'" '+rfr+' "'+url1+'"'+" -O "+os.path.join(TMPDIR,new_epn)
				command = wget_string(url1,os.path.join(TMPDIR,new_epn),rfr)
				print (command)
					
				self.infoWget(command,0)
				downloadVideo = 0
		if epn_goto == 0:
			self.list2.setCurrentRow(row)
		epn_goto = 0
		if type(finalUrl) is not list:
			self.final_playing_url = finalUrl.replace('"','')
			if self.final_playing_url.startswith('http'):
				current_playing_file_path = self.final_playing_url
			else:
				current_playing_file_path = '"'+self.final_playing_url+'"'
		else:
			self.final_playing_url = finalUrl[0].replace('"','')
			if refererNeeded == True:
				rfr_url = finalUrl[1].replace('"','')
				
		if downloadVideo == 0:
			self.initial_view_mode()
		self.epn_name_in_list = self.epn_name_in_list.replace('#','')
		
	def initial_view_mode(self):
		global site,show_hide_player
		
		if site.lower() == "music" and show_hide_player == 0:
			if self.float_window.isHidden():
				self.tab_5.hide()
		else:
			self.tab_5.show()
			self.list1.hide()
			self.frame.hide()
			self.text.hide()
			self.label.hide()
			
	def local_torrent_open(self,tmp):
		global local_torrent_file_path,site
		if not self.local_ip:
			self.local_ip = get_lan_ip()
		if not self.local_port:
			self.local_port = 8001
		
		ip = self.local_ip
		port = int(self.local_port)
		if not self.thread_server.isRunning():
			self.thread_server = ThreadServer(ip,port)
			self.thread_server.start()
		print(tmp,'------------magnet-----------')
		tmp = str(tmp)
		if self.torrent_type == 'magnet' or 'magnet:' in tmp:
			
			if tmp.startswith('magnet:'):
				print('------------magnet-----------')
				path = self.torrent_download_folder
				torrent_dest = local_torrent_file_path
				print(torrent_dest,path)
				
				self.torrent_handle,self.stream_session,info = get_torrent_info_magnet(tmp,path,ui.list6,ui.progress,ui.tmp_download_folder)
				#self.handle.pause()
				file_arr = []
				ui.list2.clear()
				epnArrList[:]=[]
				for f in info.files():
					file_path = f.path
					#if '/' in f.path:
					#	file_path = file_path.split('/')[-1]
					file_path = os.path.basename(file_path)
					##Needs Verification
					epnArrList.append(file_path+'	'+path)
					ui.list2.addItem((file_path))
				self.torrent_handle.pause()
				self.torrent_handle.set_upload_limit(self.torrent_upload_limit)
				self.torrent_handle.set_download_limit(self.torrent_download_limit)
			else:
				index = int(self.list2.currentRow())
				
				cnt,cnt_limit = set_torrent_info(self.torrent_handle,index,self.torrent_download_folder,self.stream_session,ui.list6,ui.progress,ui.tmp_download_folder)
				
				self.do_get_thread = TorrentThread(self.torrent_handle,cnt,cnt_limit,self.stream_session)
				self.do_get_thread.start()
			
			
				url = 'http://'+ip+':'+str(port)+'/'
				print(url,'-local-ip-url')
			
				return url
			
		else:
			index = int(self.list2.currentRow())
			
				
			path = self.torrent_download_folder
			
			
			torrent_dest = local_torrent_file_path
			print(torrent_dest,index,path)
			
			self.torrent_handle,self.stream_session,info,cnt,cnt_limit,file_name = get_torrent_info(torrent_dest,index,path,self.stream_session,ui.list6,ui.progress,ui.tmp_download_folder)
			
			self.torrent_handle.set_upload_limit(self.torrent_upload_limit)
			self.torrent_handle.set_download_limit(self.torrent_download_limit)
			
			self.do_get_thread = TorrentThread(self.torrent_handle,cnt,cnt_limit,self.stream_session)
			self.do_get_thread.start()
			
			
			url = 'http://'+ip+':'+str(port)+'/'
			print(url,'-local-ip-url',site)
			
			return url
				
	def epnfound_return(self):
		global site,base_url,embed,epn_goto,mirrorNo,list2_items,quality,finalUrl,home,hdr,path_Local_Dir,epnArrList,epn_name_in_list,video_local_stream
		global mpv,mpvAlive,downloadVideo,indexQueue,Player,startPlayer,mpvplayer,new_epn,idw,home1,quitReally,buffering_mplayer,path_final_Url,siteName,finalUrlFound,refererNeeded,category
	
		epn = str(self.list2.currentItem().text())
		#self.epn_name_in_list = epn
		epn = epn.replace('#','')
		if epn.startswith(self.check_symbol):
			epn = epn[1:]
		row = self.list2.currentRow()
		if '	' in epnArrList[row]:
			epn = (epnArrList[row]).split('	')[1]
		else:
			epn = epnArrList[row].replace('#','')
		if site == "PlayLists":
			
			row = self.list2.currentRow()
			item = self.list2.item(row)
			if item:
				#line = str(self.list2.currentItem().text())
				arr = epnArrList[row].split('	')
				#arr[1] = '"'+arr[1]+'"'
				
				#if arr[2] == "NONE" or arr[2].startswith('"/') or arr[2].startswith('/'):
				if len(arr) > 2:
					if arr[2].startswith('http') or arr[2].startswith('"http'):
						finalUrl = []
						finalUrl.append(arr[1])
						finalUrl.append(arr[2])
						refererNeeded = True
					else:
						finalUrl = arr[1]
						refererNeeded = False
				else:
					finalUrl = arr[1]
					#finalUrl = finalUrl.decode('utf8')
					refererNeeded = False
				#self.epn_name_in_list = arr[0]
				epn = arr[0]
				self.playlistUpdate()
				if 'youtube.com' in finalUrl:
					finalUrl = get_yt_url(finalUrl,quality).strip()
		
		if (site != "SubbedAnime" and site!= "DubbedAnime" and site!="PlayLists" and finalUrlFound == False and site!= "None" and site != "Music" and site != "Video" and site !="Local"):
		
			
			if site != "Local":
				
				
				try:
					if video_local_stream:
						finalUrl = self.site_var.getFinalUrl(name,row,mirrorNo,quality)
					else:
						finalUrl = self.site_var.getFinalUrl(name,epn,mirrorNo,quality)
				except:
					return 0
				#del site_var
			elif site == "Local":
				#finalUrl = '"'+path_Local_Dir+'/'+epn+'"'
				#finalUrl = re.sub(' ','\ ',finalUrl)
				if '	' in epnArrList[row]:
					finalUrl = '"'+(epnArrList[row]).split('	')[1]+'"'
				
				else:
					finalUrl = '"'+(epnArrList[row]).replace('#','')+'"'
				#finalUrl = finalUrl.decode('utf8')
		elif finalUrlFound == True:
				row_num = self.list2.currentRow()
			
				final = epnArrList[row_num]
				print (final)
			
				finalUrl = []
				if '	' in final:
					final = final.replace('#','')
					final = final.split('	')[1]
				else:
					final=re.sub('#','',final)
				#final = final.decode('utf8')
				finalUrl.append(final)
				if refererNeeded == True:
					if '	' in epnArrList[row_num]:
						rfr_url = epnArrList[row_num].split('	')[2]
					print (rfr_url)
					finalUrl.append(rfr_url)
		elif site == "SubbedAnime" or site == "DubbedAnime":
		
			if site == "SubbedAnime":
				code = 6
			
				if base_url == 16:
				
					epn_t = epn.split(' ')[1]
					new_epn = epn.split(' ')[0]
				else:
				
					epn_t = epn
				
				
				if self.site_var:
					try:
						finalUrl = self.site_var.getFinalUrl(siteName,name,epn,mirrorNo,category,quality) 
					except:
						return 0
			elif site == "DubbedAnime":
				code = 5
				
				if self.site_var:
					try:
						finalUrl = self.site_var.getFinalUrl(siteName,name,epn,mirrorNo,quality) 
					except:
						return 0
	
		elif site=="None" or site == "Music" or site == "Video" or site == "Local":
			if '	' in epnArrList[row]:
				finalUrl = '"'+(epnArrList[row]).split('	')[1]+'"'
				
			else:
				finalUrl = '"'+(epnArrList[row]).replace('#','')+'"'
			if site == 'None' and self.btn1.currentText().lower() == 'youtube':
					finalUrl = finalUrl.replace('"','')
					finalUrl = get_yt_url(finalUrl,quality).strip()
					finalUrl = '"'+finalUrl+'"'
			if 'youtube.com' in finalUrl.lower():
				finalUrl = finalUrl.replace('"','')
				finalUrl = get_yt_url(finalUrl,quality).strip()
				finalUrl = '"'+finalUrl+'"'
			#finalUrl = finalUrl.decode('utf8')
		path_final_Url = finalUrl
		
	def epn_return(self,row):
		global site,base_url,embed,epn_goto,mirrorNo,list2_items,quality,finalUrl,home,hdr,path_Local_Dir,epnArrList,epn_name_in_list,video_local_stream
		global mpv,mpvAlive,downloadVideo,indexQueue,Player,startPlayer,mpvplayer,new_epn,idw,home1,quitReally,buffering_mplayer,path_final_Url,siteName,finalUrlFound,refererNeeded,category
		
		if self.if_file_path_exists_then_play(row,self.list2,False):
			finalUrl = self.if_file_path_exists_then_play(row,self.list2,False)
			finalUrl = finalUrl.replace('"','')
			finalUrl = '"'+finalUrl+'"'
			return finalUrl
		
		#epn = str(self.list2.currentItem().text())
		#epn_name_in_list = epn
		#epn = epn.replace('#','')
		item = self.list2.item(row)
		if item:
			epn = item.text()
			#self.epn_name_in_list = epn
			epn = epn.replace('#','')
		else:
			return 0
		if '	' in epnArrList[row]:
			epn = (epnArrList[row]).split('	')[1]
		else:
			epn = epnArrList[row].replace('#','')
		if site == "PlayLists":
			#row = self.list2.currentRow()
			item = self.list2.item(row)
			if item:
				#line = str(self.list2.currentItem().text())
				arr = epnArrList[row].split('	')
				#arr[1] = '"'+arr[1]+'"'
				
				#if arr[2] == "NONE" or arr[2].startswith('"/') or arr[2].startswith('/'):
				if len(arr) > 2:
					if arr[2].startswith('http') or arr[2].startswith('"http'):
						finalUrl = []
						finalUrl.append(arr[1])
						finalUrl.append(arr[2])
						refererNeeded = True
					else:
						finalUrl = arr[1]
						refererNeeded = False
				else:
					finalUrl = arr[1]
					#finalUrl = finalUrl.decode('utf8')
					refererNeeded = False
				#self.epn_name_in_list = arr[0]
				epn = arr[0]
				#self.playlistUpdate()
				if 'youtube.com' in finalUrl:
					finalUrl = get_yt_url(finalUrl,quality).strip()
		
		if (site != "SubbedAnime" and site!= "DubbedAnime" and site!="PlayLists" and finalUrlFound == False and site!= "None" and site != "Music" and site != "Video" and site !="Local"):
		
			
			if site != "Local":
				
				try:
					if video_local_stream:
						finalUrl = "http://"+self.local_ip+':'+str(self.local_port)+'/'
						print(finalUrl,'=finalUrl--torrent--')
						if self.thread_server.isRunning():
							if self.do_get_thread.isRunning():
								#row_file = '/tmp/AnimeWatch/row.txt'
								row_file = os.path.join(TMPDIR,'row.txt')
								f = open(row_file,'w')
								f.write(str(row))
								f.close()
								finalUrl = "http://"+self.local_ip+':'+str(self.local_port)+'/'
							else:
								finalUrl,self.do_get_thread,self.stream_session,self.torrent_handle = self.site_var.getFinalUrl(name,row,self.local_ip+':'+str(self.local_port),'Next',self.torrent_download_folder,self.stream_session,ui.list6,ui.progress,ui.tmp_download_folder)
						else:
							#self.list6.clear()
							finalUrl,self.thread_server,self.do_get_thread,self.stream_session,self.torrent_handle = self.site_var.getFinalUrl(name,row,self.local_ip+':'+str(self.local_port),'First Run',self.torrent_download_folder,self.stream_session,ui.list6,ui.progress,ui.tmp_download_folder)
						self.torrent_handle.set_upload_limit(self.torrent_upload_limit)
						self.torrent_handle.set_download_limit(self.torrent_download_limit)
					else:
						finalUrl = self.site_var.getFinalUrl(name,epn,mirrorNo,quality)
				except:
					return 0
				#del site_var
			
			
		elif finalUrlFound == True:
				row_num = row
			
				final = epnArrList[row_num]
				print (final)
			
				finalUrl = []
				if '	' in final:
					final = final.replace('#','')
					final = final.split('	')[1]
				else:
					final=re.sub('#','',final)
				finalUrl.append(final)
				if refererNeeded == True:
					if '	' in epnArrList[row_num]:
						rfr_url = epnArrList[row_num].split('	')[2]
					print (rfr_url)
					finalUrl.append(rfr_url)
		elif site == "SubbedAnime" or site == "DubbedAnime":
		
			if site == "SubbedAnime":
				code = 6
			
				if base_url == 16:
				
					epn_t = epn.split(' ')[1]
					new_epn = epn.split(' ')[0]
				else:
				
					epn_t = epn
				
				
				if self.site_var:
					try:
						finalUrl = self.site_var.getFinalUrl(siteName,name,epn,mirrorNo,category,quality) 
					except:
						return 0
			elif site == "DubbedAnime":
				code = 5
				

				if self.site_var:
					try:
						finalUrl = self.site_var.getFinalUrl(siteName,name,epn,mirrorNo,quality) 
					except:
						return 0
		
		elif site=="None" or site == "Music" or site == "Video" or site == "Local":
			if '	' in epnArrList[row]:
				finalUrl = '"'+(epnArrList[row]).split('	')[1]+'"'
				
			else:
				finalUrl = '"'+(epnArrList[row]).replace('#','')+'"'
			if site == 'None' and self.btn1.currentText().lower() == 'youtube':
					finalUrl = finalUrl.replace('"','')
					finalUrl = get_yt_url(finalUrl,quality).strip()
					finalUrl = '"'+finalUrl+'"'
			if 'youtube.com' in finalUrl.lower():
				finalUrl = finalUrl.replace('"','')
				finalUrl = get_yt_url(finalUrl,quality).strip()
				#finalUrl = '"'+finalUrl+'"'
			#finalUrl = finalUrl.decode('utf8')
		#path_final_Url = finalUrl
		return finalUrl
	
	def watchDirectly(self,finalUrl,title,quit_val):
		global site,base_url,idw,quitReally,mpvplayer,Player,epn_name_in_list,path_final_Url,current_playing_file_path,curR
		curR = 0
		if title:
			self.epn_name_in_list = title
		else:
			self.epn_name_in_list = 'No Title'
			
		title_sub_path = title.replace('/','-')
		if title_sub_path.startswith('.'):
			title_sub_path = title_sub_path[1:]
		title_sub_path = os.path.join(self.yt_sub_folder,title_sub_path+'.en.vtt')
		
		if Player=='mplayer':
			print(mpvplayer.processId(),'=mpvplayer.processId()')
			if (mpvplayer.processId()>0):
				mpvplayer.kill()
				time.sleep(1)
				if mpvplayer.processId() > 0:
					print(mpvplayer.processId(),'=mpvplayer.processId()')
					try:
						subprocess.Popen(['killall','mplayer'])
					except:
						pass
		print(mpvplayer.processId(),'=mpvplayer.processId()')
		if mpvplayer.processId() > 0:
			mpvplayer.kill()
		quitReally = quit_val
		
		self.list1.hide()
		self.text.hide()
		self.label.hide()
		self.frame.hide()
		idw = str(int(self.tab_5.winId()))
		self.tab_5.show()
		self.tab_5.setFocus()
		if '#' in finalUrl:
			video_url = finalUrl.split('#')[-1]
			audio_url = finalUrl.split('#')[0]
			if Player == 'mplayer':
				command = "mplayer -identify -idle -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+video_url+' -audiofile '+audio_url
			else:
				command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+' --audio-file='+audio_url+' '+video_url
		else:
			finalUrl = str(finalUrl)
			path_final_Url = finalUrl
			current_playing_file_path = finalUrl
			if Player == "mplayer":
				if finalUrl.startswith('/'):
					command = "mplayer -identify -nocache -idle -msglevel all=4:statusline=5:global=6 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
				else:
					command = "mplayer -identify -idle -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
			else:
				command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+finalUrl
			if os.path.exists(title_sub_path):
				if Player == 'mpv':
					command = command+' --sub-file='+title_sub_path
					print(command)
		self.infoPlay(command)
		self.tab_5.setFocus()
		
	
	
				
	def startedM(self):
		global img_arr_artist,name
		ma = musicArtist()
		print ("Process Started")
		img_arr = ma.search(name,'')
		print (img_arr)
		if img_arr:
			wiki = img_arr.pop()
			self.text.clear()
			self.text.lineWrapMode()
			self.text.insertPlainText((wiki))
			#tmp_wiki = '/tmp/AnimeWatch/'+name+'-bio.txt'
			#thumb = '/tmp/AnimeWatch/' + name + '.jpg'
			#thumb_list = '/tmp/AnimeWatch/' + name + '.txt'
			
			tmp_wiki = os.path.join(TMPDIR,name+'-bio.txt')
			thumb = os.path.join(TMPDIR,name+'.jpg')
			thumb_list = os.path.join(TMPDIR,name+'.txt')
			print('++++++++++++',thumb,'+++++++++++++')
			#f = open(thumb_list,'w')
			#for i in img_arr:
			#	img_arr_artist.append(i)
			#	f.write(str(i)+'\n')
			#f.close()
			write_files(thumb_list,img_arr_artist,line_by_line=True)
			#f = open(tmp_wiki,'w')
			#f.write(str(wiki))
			#f.close()
			write_files(tmp_wiki,wiki,line_by_line=False)
			if img_arr_artist:
				url = img_arr_artist[0]
				del img_arr_artist[0]
				
				#subprocess.call(["curl","-o",thumb,url])
				ccurl(url+'#'+'-o'+'#'+thumb)
				picn = thumb
				self.label.clear()
				if os.path.isfile(picn):
					img = QtGui.QPixmap(picn, "1")
					self.label.setPixmap(img)
		
	def finishedM(self,nm):
		global name,epnArrList,site
		#t = "File Download Complete"
		#subprocess.Popen(["notify-send",t])
		#print "Process Ended"
		if site == "Music" and self.list3.currentItem():
			#if str(self.list3.currentItem().text())=="Artist":
			#	nm = self.list1.currentItem().text()
			#else:
			#	try:
			#		r = self.list2.currentRow()
			#		nm = epnArrList[r].split('	')[2]
			#	except:
			#		nm = ""
			if nm:
				m_path = os.path.join(home,'Music','Artist',nm,'poster.jpg')
				t_path = os.path.join(home,'Music','Artist',nm,'thumbnail.jpg')
				f_path = os.path.join(home,'Music','Artist',nm,'fanart.jpg')
				b_path = os.path.join(home,'Music','Artist',nm,'bio.txt')
				tmp_nm = os.path.join(TMPDIR,nm)
				print(tmp_nm)
				if os.path.exists(tmp_nm+'.jpg'):
					shutil.copy(tmp_nm+'.jpg',m_path)
				if os.path.exists(tmp_nm+'-bio.txt'):
					shutil.copy(tmp_nm+'-bio.txt',b_path)
				if os.path.exists(b_path):
					sumr = open_files(b_path,False)
					#sumr = open(b_path,'r').read()
				else:
					sumr = "Summary Not Available"
				self.videoImage(m_path,t_path,f_path,sumr)
				self.label.show()
				self.text.show()
	def infoWgetM(self,command):
		wget = QtCore.QProcess()
		wget.started.connect(self.startedM)
		wget.finished.connect(self.finishedM)
		QtCore.QTimer.singleShot(1000, partial(wget.start, command))
	
	def start_offline_mode(self,row):
		global downloadVideo,site,name,hdr
		if not self.if_file_path_exists_then_play(row,self.list2,False):
			finalUrl = self.epn_return(row)
			referer = False
			if type(finalUrl) is not list:
				finalUrl = finalUrl.replace('"','')
			else:
				rfr = "--referer="+finalUrl[1]
				print (rfr)
				finalUrl = re.sub('#|"','',finalUrl[0])
				print (finalUrl)
				referer = True
				
			self.list2.setFocus()
			r = self.list2.currentRow()
			print(r)
			new_epn = self.list2.item(row).text()
			if new_epn.startswith(self.check_symbol):
				new_epn = new_epn[1:] 
			new_epn = new_epn.replace('/','-')
			new_epn = re.sub('"|.mkv|.mp4','',new_epn)
			if new_epn.startswith('.'):
				new_epn = new_epn[1:]
			if finalUrl.endswith('.mkv'):
				new_epn = new_epn+'.mkv'
			else:
				new_epn = new_epn+'.mp4'
			if self.list1.currentItem():
				title = self.list1.currentItem().text()
			else:
				title = name
			folder_name = os.path.join(self.default_download_location,title)
			if not os.path.exists(folder_name):
				os.makedirs(folder_name)
			npn = os.path.join(folder_name,new_epn)
			if finalUrl.startswith('http'):
				if not referer:
					#command = "wget -c --read-timeout=60 --user-agent="+'"'+hdr+'" '+'"'+finalUrl+'"'+" -O "+'"'+npn+'"'
					command = wget_string(finalUrl,npn)
				else:
					#command = "wget -c --read-timeout=60 --user-agent="+'"'+hdr+'" '+rfr+' "'+finalUrl+'"'+" -O "+'"'+npn+'"'
					command = wget_string(finalUrl,npn,rfr)
				print (command)
				self.infoWget(command,0)
		downloadVideo = 0
		
	def dataReadyW(self,p):
		global wget,new_epn,quitReally,curR,epn,opt,base_url,Player,site,sizeFile
		#wget.waitForReadyRead()
		try:
			a = str(p.readAllStandardOutput(),'utf-8').strip()
		except:
			a =''
		#sizeFile = '0'
		if "Length:" in a:
			l = re.findall('[(][^)]*[)]',a)
			if l:
				sizeFile = l[0]
			
		if "%" in a:
			m = re.findall('[0-9][^\n]*',a)
			if m:
				#print m[0]
				n = re.findall('[^%]*',m[0])
				if n:
					try:
						val = int(n[0])
					except:
						val = 0
					self.progress.setValue(val)
				try:
					out = str(m[0])+" "+sizeFile
				except:
					out = str(m[0])+" "+'0'
				#self.goto_epn.setText(out)
				self.progress.setFormat(out)
			
	
				
	def startedW(self):
		global new_epn
		self.progress.setValue(0)
		#self.goto_epn.hide()
		self.progress.show()
		
		#t = "Downloading "+new_epn+' to /tmp/AnimeWatch/'+new_epn
		#subprocess.Popen(["notify-send",t])
		print ("Process Started")
		
		
	def finishedW(self,src):
		global name,hdr,site
		#t = "File Download Complete"
		#subprocess.Popen(["notify-send",t])
		print ("Process Ended")
		self.progress.setValue(100)
		self.progress.hide()
		if self.tab_2.isHidden():
			#self.goto_epn.show()
			pass
		type_int = False
		if self.queue_url_list:
			j = 0
			for i in self.queue_url_list:
				if type(i) is int:
					type_int = True
					break
				j = j+1
			
			if type_int:
				t = self.queue_url_list[j]
				
				t1 = self.list6.item(j)
				nepn = t1.text()
				nepn = re.sub('#|"','',nepn)
				nepn = nepn.replace('/','-')
				nepn = re.sub('"|.mkv|.mp4','',nepn)
				nepn = nepn.replace('_',' ')
				self.list6.takeItem(j)
				del t1
				del self.queue_url_list[j]
				print(t,'**************row------num-----------')
				finalUrl = self.epn_return(t)
				referer = False
				if type(finalUrl) is not list:
					finalUrl = finalUrl.replace('"','')
				else:
					rfr = "--referer="+finalUrl[1]
					print (rfr)
					finalUrl = re.sub('#|"','',finalUrl[0])
					print (finalUrl)
					referer = True
				if self.list1.currentItem():
					title = self.list1.currentItem().text()
				else:
					title = name
				npn = os.path.join(self.default_download_location,title,nepn)
				if finalUrl.endswith('.mkv'):
					npn = npn+'.mkv'
				else:
					npn = npn+'.mp4'
				if finalUrl.startswith('http'):
					if not referer:
						#command = "wget -c --read-timeout=60 --user-agent="+'"'+hdr+'" '+'"'+finalUrl+'"'+" -O "+'"'+npn+'"'
						command = wget_string(finalUrl,npn)
					else:
						#command = "wget -c --read-timeout=60 --user-agent="+'"'+hdr+'" '+rfr+' "'+finalUrl+'"'+" -O "+'"'+npn+'"'
						command = wget_string(finalUrl,npn,rfr)
					print (command)
					self.infoWget(command,0)
		
		
	def infoWget(self,command,src):
		global wget
		#if not self.tab_2.isHidden():
		#	self.horizontalLayout_5.addWidget(self.progress)
		wget = QtCore.QProcess()
		wget.setProcessChannelMode(QtCore.QProcess.MergedChannels)
		
		
		wget.started.connect(self.startedW)
		wget.readyReadStandardOutput.connect(partial(self.dataReadyW,wget))
		#self.tab_5.setFocus()
		wget.finished.connect(lambda x=src : self.finishedW(src))
		QtCore.QTimer.singleShot(1000, partial(wget.start, command))
		
	def dataReady(self,p):
		global mpvplayer,new_epn,quitReally,curR,epn,opt,base_url,Player,site,wget,mplayerLength,cache_empty,buffering_mplayer,slider_clicked,fullscr,total_seek,artist_name_mplayer,layout_mode,server,new_tray_widget,video_local_stream
		global epn_name_in_list,mpv_indicator,mpv_start,idw,cur_label_num,sub_id,audio_id,current_playing_file_path,wget
		try:
			a = str(p.readAllStandardOutput(),'utf-8').strip()
			#print(a)
			if 'icy info:' in a.lower() or 'icy-title:' in a.lower():
				if 'icy info:' in a.lower():
					song_title = re.search("'[^']*",a)
					self.epn_name_in_list = song_title.group().replace("'",'')
				else:
					song_title = re.search("icy-title:[^\n]*",a)
					self.epn_name_in_list = song_title.group().replace('icy-title:','')
				print(self.epn_name_in_list,'--radio--song--')
				mplayerLength = 1
				self.epn_name_in_list = self.epn_name_in_list.strip()
				server._emitMeta('internet-radio#'+self.epn_name_in_list,site,epnArrList)
		except:
			a = ""
		#el = time.process_time() - tt
		#print(el)
		try:
			if Player == "mpv":
				#a = str(a.decode('utf-8'))
				#a = a.replace('\n','')
				#print(a)
				if "Audio_ID" in a:
					print (a)
					a_id = re.sub('[^"]*Audio_ID=','',a)
					#a_id = a.split('=')[-1]
					print (a_id)
					audio_s = (re.search('[(][^)]*',a_id))
					if audio_s:
						audio_id = (audio_s.group()).replace('(','')
					else:
						audio_id="no"
					print ("audio_id="+audio_id)
					self.audio_track.setText("A:"+str(a_id[:8]))
				if "SUB_ID" in a:
					print (a)
					#s_id = a.split('=')[-1]
					s_id = re.sub('[^"]*SUB_ID=','',a)
					sub_s = (re.search('[(][^)]*',s_id))
					if sub_s:
						sub_id = (sub_s.group()).replace('(','')
					else:
						sub_id = "no"
					print ("sub_id="+sub_id)
					self.subtitle_track.setText("Sub:"+str(s_id[:8]))
				#if not mplayerLength and mpv_start:
				#	mpvplayer.write('\n'+'print-text "Length_Seconds=${duration}"'+'\n')
				#	time.sleep(0.01)
				if "Length_Seconds=" in a and not mplayerLength and 'args=' not in a:
					print (a)
					if a.startswith(r"b'"):
						mpl = re.sub('[^"]*Length_Seconds=','',a)
						mpl = mpl.replace(r"\n'",'')
					else:
						mpl = re.sub('[^"]*Length_Seconds=','',a)
					print (mpl,'--mpl--')
					o = mpl.split(':')
					if o and len(o) == 3:
						if o[0].isdigit() and (o[1]).isdigit() and (o[2]).isdigit():
							mplayerLength = int(o[0])*3600+int(o[1])*60+int(o[2])
						else:
							mplayerLength = 0
						print (mpl)
						print (mplayerLength)
						#self.progress.setMinimum(0)
						#self.progressEpn.setMaximum(int(mplayerLength))
						self.slider.setRange(0,int(mplayerLength))
				
			
				if "AV:" in a or "A:" in a:
					#print a
					if not mpv_start:
						mpv_start.append("Start")
						try:
							npn = '"'+"Playing: "+self.epn_name_in_list.replace('#','')+'"'
							npn1 = bytes('\n'+'show-text '+npn+' 4000'+'\n','utf-8')
							mpvplayer.write(npn1)
						except:
							pass
						if MainWindow.isFullScreen() and layout_mode != "Music":
							self.gridLayout.setSpacing(0)
							if not self.frame1.isHidden():
								self.frame1.hide()
							if self.frame_timer.isActive():
								self.frame_timer.stop()
							self.frame_timer.start(1000)
							#QtGui.QApplication.processEvents()
					if "Buffering" in a and not mpv_indicator and (site != "Local" or site != "Music" or site != "Video"):
						cache_empty = "yes"
						mpv_indicator.append("cache empty") 
						print ("buffering")
						mpvplayer.write(b'\n set pause yes \n')
						if self.mplayer_timer.isActive():
							self.mplayer_timer.stop()
						self.mplayer_timer.start(5000)
						if MainWindow.isFullScreen() and layout_mode != "Music":
							self.gridLayout.setSpacing(0)
							self.frame1.show()
							if self.frame_timer.isActive():
								self.frame_timer.stop()
							self.frame_timer.start(5000)
							
					t = re.findall("AV:[^)]*[)]|A:[^)]*[)]",a)
					if not t:
						t = re.findall("AV: [^ ]*|A: [^ ]*",a)
					
					if "Cache:" in a:
						n = re.findall("Cache:[^+]*",a)
						cache_val = re.search("[0-9][^s]*",n[0]).group()
						if len(cache_val) == 1:
							cache_val = '0'+cache_val
						out = t[0] +"  "+cache_val+'s'
					else:
						out = t[0]
					
					if "Paused" in a and not mpv_indicator:
						out = "(Paused) "+out
						#self.gridLayout.setSpacing(0)
						#if not "Buffering" in a:
						#	self.player_play_pause.setText("Play")
							#print('set play button text = Play')
					elif "Paused" in a and mpv_indicator:
						out = "(Paused Caching..Wait Few Seconds) "+out
						#self.gridLayout.setSpacing(0)
						#if not "Buffering" in a:
						#	self.player_play_pause.setText("Play")
							#print('set play button text = Play')
					out = re.sub('AV:[^0-9]*|A:[^0-9]*','',out)
					if not new_tray_widget.isHidden():
						new_tray_widget.update_signal.emit(out)
					#print(out)
					#l = re.findall("[(][^%]*",t[0])
					#val = re.sub('[(]','',l[0])
					l = re.findall("[0-9][^ ]*",out)
					val1 = l[0].split(':')
					val = int(val1[0])*3600+int(val1[1])*60+int(val1[2])
					#print(val)
					if not mplayerLength:
						#print(a,self.mpv_cnt)
						#print(mplayerLength)
						
						if self.mpv_cnt > 4:
							m = re.findall('[/][^(]*',out)
							n = re.sub(' |[/]','',m[0])
							print (n)
							o = n.split(':')
							mplayerLength = int(o[0])*3600+int(o[1])*60+int(o[2])
							print (mplayerLength,"--mpvlength",a)
							#print (mplayerLength)
							self.progressEpn.setMaximum(int(mplayerLength))
							self.slider.setRange(0,int(mplayerLength))
							self.mpv_cnt = 0
						print(mplayerLength)
						self.mpv_cnt = self.mpv_cnt + 1
					#self.progressEpn.setValue(val)
					out1 = out+" ["+self.epn_name_in_list+"]"
					self.progressEpn.setFormat((out1))
					if mplayerLength == 1:
						self.slider.setValue(0)
					else:
						self.slider.setValue(val)
				if "VO:" in a or "AO:" in a or 'Stream opened successfully' in a:
				#if "AV:" not in a:
					t = "Loading: "+self.epn_name_in_list+" (Please Wait)"
					self.progressEpn.setFormat((t))
					if MainWindow.isFullScreen() and layout_mode != "Music":
						self.gridLayout.setSpacing(0)
						self.frame1.show()
						if self.frame_timer.isActive():
							self.frame_timer.stop()
						self.frame_timer.start(1000)
				#if "EndOfFile:" in a:
				#if ("Exiting" in a or "EOF code: 1" in a or "HTTP error 403 Forbidden" in a):
				if ("EOF code: 1" in a or "HTTP error 403 Forbidden" in a):
					if (self.player_setLoop_var and quitReally == 'no') or (self.list2.count() == 0):
						t2 = bytes('\n'+"loadfile "+(current_playing_file_path)+'\n','utf-8')
						mpvplayer.write(t2)
						return 0
						#curR = self.list2.currentRow()
					else:
						if not self.queue_url_list:
							if curR == self.list2.count() - 1:
								curR = 0
								if site == "Music" and not self.playerPlaylist_setLoop_var:
									r1 = self.list1.currentRow()
									it1 = self.list1.item(r1)
									if it1:
										if r1 < self.list1.count():
											r2 = r1+1
										else:
											r2 = 0
										self.list1.setCurrentRow(r2)
										self.listfound()
							else:
								curR = curR + 1
					mplayerLength = 0
					self.total_file_size = 0
					if mpv_start:
						mpv_start.pop()
					if not self.queue_url_list:
						self.list2.setCurrentRow(curR)
					#epn = self.list2.currentItem().text()
					#epn = re.sub("#","",str(epn))
					#mpvplayer.waitForReadyRead()
					if "HTTP error 403 Forbidden" in a:
						print (a)
						quitReally = "yes"
						#self.player_playlist.setText("End")
						#self.player_playlist.setToolTip('Stop After Playing Current File')
					if quitReally == "no":
						if self.tab_5.isHidden() and thumbnail_indicator:
							#p1 = "mn = ui.label_"+str(curR)+".winId()"
							#exec p1
							#idw = str(mn)
							length_1 = self.list2.count()
							q3="self.label_epn_"+str(length_1+cur_label_num)+".setText(self.epn_name_in_list)"
							exec (q3)
							QtWidgets.QApplication.processEvents()
						if site == "Local" or site == "Video" or site == "Music" or site == "PlayLists" or site == "None":
							if len(self.queue_url_list)>0 and wget.processId() == 0:
								self.getQueueInList()
							else:
								self.localGetInList()
						else:
							if len(self.queue_url_list)>0 and wget.processId() == 0:
								self.getQueueInList()
							else:
								self.getNextInList()
					elif quitReally == "yes": 
						self.list2.setFocus()
			elif Player == "mplayer":
				#print(a)
				if "PAUSE" in a:
					if buffering_mplayer != 'yes':
						self.player_play_pause.setText(self.player_buttons['play'])
						#print('set play button text = Play')
					if MainWindow.isFullScreen() and layout_mode != "Music":
						self.gridLayout.setSpacing(0)
						self.frame1.show()
						if buffering_mplayer == "yes":
							if self.frame_timer.isActive:
								self.frame_timer.stop()
							self.frame_timer.start(10000)
				if "Cache empty" in a:
					cache_empty = "yes"
					
				if "ID_VIDEO_BITRATE" in a:
					try:
						a0 = re.findall('ID_VIDEO_BITRATE=[^\n]*',a)
						print (a0[0],'--videobit')
						a1 = a0[0].replace('ID_VIDEO_BITRATE=','')
						self.id_video_bitrate=int(a1)
					except:
						self.id_video_bitrate = 0
					
				if "ID_AUDIO_BITRATE" in a:
					try:
						a0 = re.findall('ID_AUDIO_BITRATE=[^\n]*',a)
						print (a0[0],'--audiobit')
						a1 = a0[0].replace('ID_AUDIO_BITRATE=','')
						self.id_audio_bitrate=int(a1)
					except:
						self.id_audio_bitrate=0
				if "ANS_switch_audio" in a:
					print (a)
					audio_id = a.split('=')[-1]
					
					print ("audio_id="+audio_id)
					self.audio_track.setText("A:"+str(audio_id))
				if "ANS_sub" in a:
					sub_id = a.split('=')[-1]
					
					print ("sub_id="+sub_id)
					self.subtitle_track.setText("Sub:"+str(sub_id))
				
				if "ID_LENGTH" in a and not mplayerLength:
					#print a
					t = re.findall('ID_LENGTH=[0-9][^.]*',a)
					mplayerLength = re.sub('ID_LENGTH=','',t[0])
					print (mplayerLength)
					#mplayerLength = float(mplayerLength)
					mplayerLength = int(mplayerLength) *1000
					#self.progress.setMinimum(0)
					#self.progressEpn.setMaximum(int(mplayerLength))
					self.slider.setRange(0,int(mplayerLength))
					self.total_file_size = int(((self.id_audio_bitrate+self.id_video_bitrate)*mplayerLength)/(8*1024*1024*1000))
					print(self.total_file_size,' MB')
					#self.id_audio_bitrate = 0
					#self.id_video_bitrate = 0
				if ("A:" in a) or ("PAUSE" in a):
					if not mpv_start:
						mpv_start.append("Start")
						try:
							npn = '"'+"Playing: "+self.epn_name_in_list.replace('#','')+'"'
							npn1 = bytes('\n'+'osd_show_text '+str(npn)+' 4000'+'\n','utf-8')
							mpvplayer.write(npn1)
						except:
							pass
						if MainWindow.isFullScreen() and layout_mode != "Music":
							self.gridLayout.setSpacing(0)
							if not self.frame1.isHidden():
								self.frame1.hide()
							if self.frame_timer.isActive():
								self.frame_timer.stop()
							self.frame_timer.start(1000)
					if "PAUSE" in a:
						
						if "%" in a:
							#print a
							m = re.findall('[0-9]*%',a)
							c = m[-1]
						else:
							c = "0%"
						try:
							t = str(self.progressEpn.text())
						#if "Paused" in t:
						
							#t = re.sub('[(]Paused[)] | Cache: [0-9]*%|[(]Paused Caching..Wait 10s[)] ','',t)
							#t = t.replace('[(]Paused[)] | Cache: [0-9]*%|[(]Paused Caching..Wait 10s[)] ','')
							t = re.sub('[(]Paused[)] | Cache: [0-9]*%|[(]Paused Caching..Wait 5s[)] ','',t)
						except:
							t = ""
						
						if buffering_mplayer == "yes":
							print(video_local_stream,'--video--local--stream--')
							out = "(Paused Caching..Wait 5s) " + t+" Cache: "+c
							if (not self.mplayer_timer.isActive()) and (not video_local_stream):
								self.mplayer_timer.start(5000)
							#buffering_mplayer = "no"
						else:
							
							#out = "(Paused) "+t+" Cache: "+c
							out = "(Paused) "+t
						
					else:
						if "%" in a:
							#print a
							m = re.findall('[0-9]*%',a)
							try:
								c = m[3]
							except:
								c = m[-1]
						else:
							c = "0%"
					
						t = re.findall('A:[^.]*',a)
						#print t
						l = re.sub('A:[^0-9]*','',t[0])
						#l = int(l)
						l =int(l)*1000
						
						#val = int((l/mplayerLength)*100)
						#print val
						#print mplayerLength
						#self.progressEpn.setValue(int(l))
						if mplayerLength == 1:
							self.slider.setValue(0)
						else:
							self.slider.setValue(int(l))
						
						#out = str(int(l/60))+"/"+str(int(mplayerLength/60))+" ("+str(val)+")"
						#out = str(datetime.timedelta(seconds=int(l))) + " / " + str(datetime.timedelta(seconds=int(mplayerLength)))+" ["+epn_name_in_list+"]"+" Cache: "+c
						if site == "Music":
							out_time = str(datetime.timedelta(milliseconds=int(l))) + " / " + str(datetime.timedelta(milliseconds=int(mplayerLength)))
							
							out = out_time + " ["+self.epn_name_in_list+'('+artist_name_mplayer+')' +"]"
						else:
							out_time = str(datetime.timedelta(milliseconds=int(l))) + " / " + str(datetime.timedelta(milliseconds=int(mplayerLength)))
							
							out = out_time + " ["+self.epn_name_in_list+"]"
							
						if not new_tray_widget.isHidden():
							new_tray_widget.update_signal.emit(out_time)
					if (cache_empty == "yes") and (site != "Local" or site != "Music" or site != "Video"):
						#mpvplayer.write('\n'+'get_property stream_length'+'\n')
						print('---nop--error--pausing---')
						mpvplayer.write(b'\n pause \n')
						cache_empty = "no"
						buffering_mplayer = "yes"
						#mpvplayer.write('\n'+'osd_show_text Buffering'+'\n')
					if total_seek != 0:
						r = "Seeking "+str(total_seek)+'s'
						self.progressEpn.setFormat((r))
					else:
						#self.progressEpn.setFormat('')
						self.progressEpn.setFormat((out))
				if 'http' in a:
				#if "AV:" not in a:
					t = "Loading: "+self.epn_name_in_list+" (Please Wait)"
					self.progressEpn.setFormat((t))
					if MainWindow.isFullScreen() and layout_mode != "Music":
						self.gridLayout.setSpacing(0)
						self.frame1.show()
						if self.frame_timer.isActive():
							self.frame_timer.stop()
						self.frame_timer.start(1000)
				#if site=="Local":
				#if ("(End of file)" in a or "EOF code: 1" in a or "HTTP error 403 Forbidden" in a):
				if ("EOF code: 1" in a or "HTTP error 403 Forbidden" in a):
					mplayerLength = 0
					self.total_file_size = 0
					mpv_start.pop()
					#self.progressEpn.setMaximum(100)
					#self.progressEpn.setValue(0)
					#if self.player_setLoop_var:
						#quitReally == "yes"
					#	curR = self.list2.currentRow()
					#else:
						#quitReally == "no"
					if (self.player_setLoop_var and quitReally == 'no') or (self.list2.count() == 0):
						t2 = bytes('\n'+"loadfile "+(current_playing_file_path)+" replace"+'\n','utf-8')
						mpvplayer.write(t2)
						return 0
						#curR = self.list2.currentRow()
						
					else:
						if not self.queue_url_list:
							if curR == self.list2.count() - 1:
								curR = 0
								if site == "Music" and not self.playerPlaylist_setLoop_var:
									r1 = self.list1.currentRow()
									it1 = self.list1.item(r1)
									if it1:
										if r1 < self.list1.count():
											r2 = r1+1
										else:
											r2 = 0
										self.list1.setCurrentRow(r2)
										self.listfound()
							else:
								curR = curR + 1
					if not self.queue_url_list:
						self.list2.setCurrentRow(curR)
					if "HTTP error 403 Forbidden" in a:
						print (a)
						quitReally = "yes"
						#self.player_playlist.setText("End")
						#self.player_playlist.setToolTip('Stop After Playing Current File')
					#epn = self.list2.currentItem().text()
					#epn = re.sub("#","",str(epn))
					#epn = epn.replace('#','')
					#mpvplayer.waitForReadyRead()
					if quitReally == "no":
						if site == "Local" or site == "Video" or site == "Music" or site == "PlayLists" or site == "None":
							if len(self.queue_url_list)>0 and wget.processId() == 0:
								self.getQueueInList()
							else:
								self.localGetInList()
						else:
							if len(self.queue_url_list)>0 and wget.processId() == 0:
								self.getQueueInList()
							else:
								self.getNextInList()
						if self.tab_5.isHidden() and thumbnail_indicator:
							#p1 = "mn = ui.label_"+str(curR)+".winId()"
							#exec p1
							#idw = str(mn)
							length_1 = self.list2.count()
							q3="self.label_epn_"+str(length_1+cur_label_num)+".setText((self.epn_name_in_list))"
							exec (q3)
							QtWidgets.QApplication.processEvents()
						
					elif quitReally == "yes": 
						self.list2.setFocus()
		except:
			pass
		
		
				
	def started(self):
		global mpvplayer,epn,new_epn,epn_name_in_list,fullscr,mpv_start,Player,cur_label_num,epn_name_in_list,site
		if self.tab_5.isHidden() and thumbnail_indicator:
			length_1 = self.list2.count()
			q3="self.label_epn_"+str(length_1+cur_label_num)+".setText((self.epn_name_in_list))"
			exec(q3)
			QtWidgets.QApplication.processEvents()
		print ("Process Started")
		print (mpvplayer.processId())
		mpv_start =[]
		mpv_start[:]=[]
		t = "Loading: "+self.epn_name_in_list+" (Please Wait)"
		#print t
		self.progressEpn.setValue(0)
		self.progressEpn.setFormat((t))
		if MainWindow.isFullScreen() and site!="Music":
			self.superGridLayout.setSpacing(0)
			self.gridLayout.setSpacing(0)
			self.frame1.show()
			if self.frame_timer.isActive():
				self.frame_timer.stop()
			#self.frame_timer.start(1000)
		
	def finished(self):
		global quitReally,mpvplayer,mplayerLength,mpv_start
		if mpv_start:
			mpv_start.pop()
		mplayerLength = 0
		self.progressEpn.setMaximum(100)
		self.slider.setRange(0,100)
		print ("Process Ended")
		self.progressEpn.setValue(0)
		self.slider.setValue(0)
		self.progressEpn.setFormat("")
		print (mpvplayer.processId())
		#if quitReally == "no":
		#	self.mpvNextEpnList()
		
	def infoPlay(self,command):
		global mpvplayer,Player,site,new_epn
		print('--line--15662--')
		if mpvplayer.processId()>0:
			mpvplayer.kill()
		print('--line--15666--')
		mpvplayer = QtCore.QProcess()
		self.mpvplayer_val = mpvplayer
		mpvplayer.setProcessChannelMode(QtCore.QProcess.MergedChannels)
		mpvplayer.started.connect(self.started)
		mpvplayer.readyReadStandardOutput.connect(partial(self.dataReady,mpvplayer))
		#self.tab_5.setFocus()
		mpvplayer.finished.connect(self.finished)
		QtCore.QTimer.singleShot(1000, partial(mpvplayer.start, command))
	
	def adjust_thumbnail_window(self,row):
		global thumbnail_indicator
		self.epn_name_in_list = self.epn_name_in_list.replace('#','')
		if thumbnail_indicator and not self.tab_5.isHidden():
			title_num = row + ui.list2.count()
			if self.epn_name_in_list.startswith(self.check_symbol):
				newTitle = self.epn_name_in_list
			else:
				newTitle = self.check_symbol+self.epn_name_in_list
			sumry = "<html><h1>"+self.epn_name_in_list+"</h1></html>"
			q4="ui.label_epn_"+str(title_num)+".setToolTip((sumry))"
			exec (q4)
			q3="ui.label_epn_"+str(title_num)+".setText((newTitle))"
			exec (q3)
			p8="ui.label_epn_"+str(title_num)+".home(True)"
			exec (p8)
			p8="ui.label_epn_"+str(title_num)+".deselect()"
			exec (p8)
			QtWidgets.QApplication.processEvents()
			
			p1 = "ui.label_epn_"+str(row)+".y()"
			ht=eval(p1)
			
			ui.scrollArea1.verticalScrollBar().setValue(ht)
			#ui.labelFrame2.setText(self.epn_name_in_list[:20])
			ui.labelFrame2.setText(newTitle[:20])
	
	def localGetInList(self):
		global site,base_url,embed,epn,epn_goto,mirrorNo,list2_items,quality,finalUrl,curR,home,mpvplayer,buffering_mplayer,epn_name_in_list,opt_movies_indicator,audio_id,sub_id,siteName,artist_name_mplayer
		global mpv,mpvAlive,downloadVideo,indexQueue,Player,startPlayer,new_epn,path_Local_Dir,Player,mplayerLength,curR,epnArrList,fullscr,thumbnail_indicator,category,finalUrlFound,refererNeeded,server,current_playing_file_path,music_arr_setting,default_arr_setting,wget,idw
		print (self.player_setLoop_var)
		row = self.list2.currentRow()
		print('--line--15677--')
		if row > len(epnArrList) or row < 0:
			row = len(epnArrList)-1
		
		try:
			server._emitMeta("Next",site,epnArrList)
		except:
			pass
		mplayerLength = 0
		buffering_mplayer = "no"
		#external_url = False
		
		
		
		if self.if_file_path_exists_then_play(row,self.list2,True):
			self.adjust_thumbnail_window(row)
			return 0
		
		
					
		self.set_init_settings()
		
		if site != "PlayLists":
			if '	' in epnArrList[row]:
				epn = epnArrList[row].split('	')[1]
				self.epn_name_in_list = (epnArrList[row]).split('	')[0]
			else:
				epn = self.list2.currentItem().text()
				self.epn_name_in_list = str(epn)
				epn = epnArrList[row].replace('#','')
			if not epn:
				return 0
			epn = epn.replace('#','')
		else:
			#row = self.list2.currentRow()
			item = self.list2.item(row)
			if item:
				#line = str(self.list2.currentItem().text())
				
				arr = epnArrList[row].split('	')
				if len(arr) > 2:
					if arr[2].startswith('http') or arr[2].startswith('"http'):
						finalUrl = []
						finalUrl.append(arr[1])
						finalUrl.append(arr[2])
						refererNeeded = True
					else:
						finalUrl = arr[1]
						refererNeeded = False
				else:
					finalUrl = arr[1]
					refererNeeded = False
				
				
				self.epn_name_in_list = arr[0]
				epn = self.epn_name_in_list
				self.playlistUpdate()
				self.list2.setCurrentRow(row)
				#if 'youtube.com' in finalUrl:
				#	finalUrl = get_yt_url(finalUrl,quality).strip()
		
		self.adjust_thumbnail_window(row)
		
		if site=="Local":
			if opt == "History":
				self.mark_History()
			else:
				i = str(self.list2.item(row).text())
				#j = self.list2.item(row)
				#self.list2.takeItem(row)
				#del j
				if not i.startswith(self.check_symbol):
					#self.list2.insertItem(row,self.check_symbol+i)
					self.list2.item(row).setText(self.check_symbol+i)
				else:
					#self.list2.insertItem(row,i)
					self.list2.item(row).setText(i)
				self.list2.item(row).setFont(QtGui.QFont('SansSerif', 10,italic=True))
				self.list2.setCurrentRow(row)
				
			
			
			#finalUrl = '"'+path_Local_Dir+'/'+epn+'"'
			if '	' in epnArrList[row]:
				finalUrl = '"'+(epnArrList[row]).split('	')[1]+'"'
			else:
				finalUrl = '"'+(epnArrList[row]).replace('#','')+'"'
			#finalUrl = finalUrl.decode('utf8')
			print (finalUrl)
		
		
		
		elif site == "None" or site == "Music" or site == "Video" or site == 'PlayLists':
			
			if '	' in epnArrList[row]:
					finalUrl = '"'+(epnArrList[row]).split('	')[1]+'"'
			else:
					finalUrl = '"'+(epnArrList[row]).replace('#','')+'"'
			#finalUrl = finalUrl.decode('utf8')
			print (finalUrl,'--line--15803--')
			i = str(self.list2.item(row).text())
			#j = self.list2.item(row)
			#self.list2.takeItem(row)
			#del j
			if not i.startswith(self.check_symbol):
				#self.list2.insertItem(row,self.check_symbol+i)
				self.list2.item(row).setText(self.check_symbol+i)
			else:
				#self.list2.insertItem(row,i)
				self.list2.item(row).setText(i)
			self.list2.item(row).setFont(QtGui.QFont('SansSerif', 10,italic=True))
			self.list2.setCurrentRow(row)
			if 'youtube.com' in finalUrl.lower():
				finalUrl = finalUrl.replace('"','')
				finalUrl = get_yt_url(finalUrl,quality).strip()
				#if '#' in finalUrl:
				self.external_url = True
			
		new_epn = self.epn_name_in_list
	
		
		finalUrl = finalUrl.replace('"','')
		if '#' in finalUrl:
				print('---*******-------line 15825--')
				
				if '#' in finalUrl:
					video_url = finalUrl.split('#')[-1]
					audio_url = finalUrl.split('#')[0]
					if Player == 'mpv':
						finalUrl = "--audio-file="+audio_url+' '+video_url
					elif Player == 'mplayer':
						finalUrl = '-audiofile '+audio_url+' '+video_url
				if Player == 'mplayer':
					if mpvplayer.processId()>0:
						mpvplayer.kill()
						if mpvplayer.processId() > 0:
							try:
								subprocess.Popen(['killall','mplayer'])
							except:
								pass
					command = "mplayer -identify -idle -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
				else:
					command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+' '+finalUrl
					if mpvplayer.processId()>0:
						mpvplayer.kill()
						if mpvplayer.processId() > 0:
							try:
								subprocess.Popen(['killall','mpv'])
							except:
								pass
					print('---*******-------line 15849--')
				self.infoPlay(command)
				
		else:
			finalUrl = '"'+finalUrl+'"'
			try:
				finalUrl = str(finalUrl,'utf-8')
			except:
				finalUrl = finalUrl
				
			if mpvplayer.processId() > 0:
				if Player == "mplayer":
					if audio_id == "auto":
						audio_id = "0"
					if sub_id == "auto":
						sub_id = "0"
					command1 = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" -sid "+str(sub_id)+" -aid "+str(audio_id)+" "+finalUrl
					try:
						command = str(command1,'utf-8')
						#command = command.encode('utf-8')
					except:
						command = command1
					if not self.external_url:
						#try:
						epnShow = '"' + "Queued:  "+ new_epn + '"'
						t1 = bytes('\n'+'show_text '+(epnShow)+'\n','utf-8')
						t2 = bytes('\n'+"loadfile "+(finalUrl)+" replace"+'\n','utf-8')
						print (finalUrl,'---hello-----')
						
						mpvplayer.write(t1)
						mpvplayer.write(t2)
						if self.mplayer_SubTimer.isActive():
							self.mplayer_SubTimer.stop()
						self.mplayer_SubTimer.start(2000)
							
						#except:
						#	self.infoPlay(command)
					else:
						mpvplayer.write(b'\n quit \n')
						if mpvplayer.processId() > 0:
							try:
								subprocess.Popen(['killall','mplayer'])
							except:
								pass
						self.infoPlay(command)
						self.external_url = False
				elif Player == "mpv":
					command1 = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+" -sid "+str(sub_id)+" -aid "+str(audio_id)+" "+finalUrl
					try:
						command = str(command1,'utf-8')
						#command = command.encode('utf-8')
					except:
						command = command1
				
					if mpvplayer.processId()>0:
						
						try:
							epnShow = '"' + "Queued:  "+ new_epn + '"'
							t1 = bytes('\n'+'show-text '+epnShow+'\n','utf-8')
							t2 = bytes('\n'+"loadfile "+finalUrl+'\n','utf-8')
							print (finalUrl,'---hello-----')
							mpvplayer.write(t1)
							mpvplayer.write(t2)
							if self.external_url:
								#mpvplayer.write(b'\n set aid 1 \n')
								self.external_url = False
						except:
							self.infoPlay(command)
					else:
						self.infoPlay(command)
			
				print ("mpv=" + str(mpvplayer.processId()))
				if site == "Music":
					try:
						artist_name_mplayer = epnArrList[row].split('	')[2]
						if artist_name_mplayer == "None":
							artist_name_mplayer = ""
					except:
						artist_name_mplayer = ""
					self.updateMusicCount('count',finalUrl)
					r = self.list2.currentRow()
					self.musicBackground(r,'Search')
				elif site == "Video":
					self.updateVideoCount('mark',finalUrl)
				if finalUrl.startswith('"http'):
					current_playing_file_path = finalUrl.replace('"','')
				else:
					current_playing_file_path = finalUrl
			else:
				if Player == "mplayer":
					if audio_id == "auto":
						audio_id = "0"
					if sub_id == "auto":
						sub_id = "0"
					command1 = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" -sid "+str(sub_id)+" -aid "+str(audio_id)+" "+finalUrl
					try:
						command = str(command1,'utf-8')
						#command = command.encode('utf-8')
					except:
						command = command1
					
				elif Player == "mpv":
					command1 = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+" -sid "+str(sub_id)+" -aid "+str(audio_id)+" "+finalUrl
					try:
						command = str(command1,'utf-8')
						#command = command.encode('utf-8')
					except:
						command = command1
				
					
				self.infoPlay(command)
			
				print ("mpv=" + str(mpvplayer.processId()))
				if site == "Music":
					try:
						artist_name_mplayer = epnArrList[row].split('	')[2]
						if artist_name_mplayer == "None":
							artist_name_mplayer = ""
					except:
						artist_name_mplayer = ""
					self.updateMusicCount('count',finalUrl)
					r = self.list2.currentRow()
					self.musicBackground(r,'Search')
				elif site == "Video":
					self.updateVideoCount('mark',finalUrl)
				if finalUrl.startswith('"http'):
					current_playing_file_path = finalUrl.replace('"','')
				else:
					current_playing_file_path = finalUrl
	def getQueueInList(self):
		global curR,mpvplayer,site,epn_name_in_list,artist_name_mplayer,idw,sub_id,audio_id,Player,server,current_playing_file_path,quality
		try:
			t1 = self.queue_url_list[0]
			server._emitMeta("queue"+'#'+t1,site,epnArrList)
		except:
			pass
		#print(self.list6.item(0).text(),self.queue_url_list)
		if self.if_file_path_exists_then_play(0,self.list6,True):
			del self.queue_url_list[0]
			self.list6.takeItem(0)
			del t1
			return 0
		
		if site == "Local" or site == "Video" or site == "Music" or site == "PlayLists" or site == "None":
			t = self.queue_url_list[0]
			epnShow = '"'+t.split('	')[1]+'"'
			self.epn_name_in_list = t.split('	')[0]
			if self.epn_name_in_list.startswith('#'):
				self.epn_name_in_list = self.epn_name_in_list[1:]
			if site == "Music":
				artist_name_mplayer = t.split('	')[2]
				if artist_name_mplayer == "None":
					artist_name_mplayer = ""
			del self.queue_url_list[0]
			t1 = self.list6.item(0)
			self.list6.takeItem(0)
			del t1
			if not idw:
				idw = str(int(self.tab_5.winId()))
			if 'youtube.com' in epnShow.lower():
				finalUrl = epnShow.replace('"','')
				finalUrl = get_yt_url(finalUrl,quality).strip()
				epnShow = finalUrl
				self.external_url = True
		else:
			epnShow = self.queue_url_list.pop()
			curR = curR - 1
			print('--------inside getQueueInlist------')
			self.list2.setCurrentRow(curR)
			
		
		if '#' in epnShow:
			if '#' in epnShow:
				epnShow = epnShow.replace('"','')
				if mpvplayer.processId()>0:
					mpvplayer.kill()
				video_url = epnShow.split('#')[-1]
				audio_url = epnShow.split('#')[0]
				if Player == 'mpv':
					finalUrl = "--audio-file="+audio_url+' '+video_url
				elif Player == 'mplayer':
					finalUrl = '-audiofile '+audio_url+' '+video_url
			else:
				finalUrl = epnShow
			if Player == 'mplayer':
				if mpvplayer.processId() > 0:
					try:
						subprocess.Popen(['killall','mplayer'])
					except:
						pass
				command = "mplayer -identify -idle -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+finalUrl
			else:
				command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --input-conf=input.conf --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+' '+finalUrl
				if mpvplayer.processId() > 0:
					try:
						subprocess.Popen(['killall','mpv'])
					except:
						pass
			self.infoPlay(command)
		else:
			epnShowN = '"'+epnShow.replace('"','')+'"'
			if Player == "mplayer":
					
					command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -osdlevel 0 -slave -wid "+idw+" "+epnShowN
			elif Player == "mpv":
					command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+" -sid "+str(sub_id)+" -aid "+str(audio_id)+" "+epnShowN
			if mpvplayer.processId() > 0:
				epnShow = '"'+epnShow.replace('"','')+'"'
				if epnShow.startswith('"http'):
					epnShow = epnShow.replace('"','')
				t2 = bytes('\n'+"loadfile "+epnShow+" replace"+'\n','utf-8')
				print(t2)
				if Player == 'mpv':
					mpvplayer.write(t2)
					if self.external_url:
						#mpvplayer.write(b'\n set aid 1 \n')
						self.external_url = False
				elif Player == "mplayer":
					if not self.external_url:
						mpvplayer.write(t2)
						if self.mplayer_SubTimer.isActive():
							self.mplayer_SubTimer.stop()
						self.mplayer_SubTimer.start(2000)
					else:
						mpvplayer.write(b'\n quit \n')
						if mpvplayer.processId() > 0:
							try:
								subprocess.Popen(['killall','mplayer'])
							except:
								pass
						self.infoPlay(command)
						self.external_url = False
			else:
				print (command)
				self.infoPlay(command)
				self.list1.hide()
				self.frame.hide()
				self.text.hide()
				self.label.hide()
				self.tab_5.show()
			
			epnShow = epnShow.replace('"','')
			if not epnShow.startswith('http'):
				if site == "Music":
					
					self.updateMusicCount('count',epnShowN)
					self.musicBackground(0,'Queue')
				elif site == "Video":
					self.updateVideoCount('mark',epnShowN)
			if epnShow.startswith('http'):
				current_playing_file_path = epnShow
			else:
				current_playing_file_path = '"'+epnShow+'"'
		
	def getNextInList(self):
		global site,base_url,embed,epn,epn_goto,mirrorNo,list2_items,quality,finalUrl,curR,home,mpvplayer,buffering_mplayer,epn_name_in_list,opt_movies_indicator,audio_id,sub_id,siteName,rfr_url
		global mpv,mpvAlive,downloadVideo,indexQueue,Player,startPlayer,new_epn,path_Local_Dir,Player,mplayerLength,curR,epnArrList,fullscr,thumbnail_indicator,category,finalUrlFound,refererNeeded,server,current_playing_file_path,default_arr_setting,music_arr_setting,video_local_stream,wget
		
		row = self.list2.currentRow()
		self.total_file_size = 0
		mplayerLength = 0
		buffering_mplayer = "no"
		#self.queue_url_list[:]=[]
		
		try:
			server._emitMeta("Next",site,epnArrList)
		except:
			pass
		
		
		
		if self.if_file_path_exists_then_play(row,self.list2,True):
			self.adjust_thumbnail_window(row)
			return 0
		
		if site != "PlayLists":
			if '	' in epnArrList[row]:
				epn = epnArrList[row].split('	')[1]
				self.epn_name_in_list = (epnArrList[row]).split('	')[0]
			else:
				epn = str(self.list2.currentItem().text())
				self.epn_name_in_list = (epn)
				epn = epnArrList[row]
			if not epn:
				return 0
			epn = epn.replace('#','')
		else:
			row = self.list2.currentRow()
			item = self.list2.item(row)
			if item:
				line = str(self.list2.currentItem().text())
				
				arr = epnArrList[row].split('	')
					
				if arr[2].startswith('http') or arr[2].startswith('"http'):
					finalUrl = []
					finalUrl.append(arr[1])
					finalUrl.append(arr[2])
					refererNeeded = True
				else:
					finalUrl = arr[1]
					refererNeeded = False
				
				
				self.epn_name_in_list = arr[0]
				epn = self.epn_name_in_list
				self.playlistUpdate()
				self.list2.setCurrentRow(row)
				if 'youtube.com' in finalUrl:
					finalUrl = get_yt_url(finalUrl,quality).strip()
		
		self.adjust_thumbnail_window(row)
		
		self.set_init_settings()
		
		if (site != "SubbedAnime" and site!= "DubbedAnime" and site!="PlayLists" and finalUrlFound == False and site!="None" and site!="Music" and site!= "Video" and site!="Local"):
			if opt == "History":
				self.mark_History()
			else:
				i = str(self.list2.item(row).text())
				#j = self.list2.item(row)
				#self.list2.takeItem(row)
				#del j
				if not self.check_symbol in i:
					#self.list2.insertItem(row,self.check_symbol+i)
					self.list2.item(row).setText(self.check_symbol+i)
				else:
					#self.list2.insertItem(row,i)
					self.list2.item(row).setText(i)
				self.list2.item(row).setFont(QtGui.QFont('SansSerif', 10,italic=True))
				self.list2.setCurrentRow(row)
				
			if site != "Local":
				
				try:
					print(site)
				except:
					return 0
				self.progressEpn.setFormat('Wait..')
				#QtWidgets.QApplication.processEvents()
				try:
					if video_local_stream:
						if self.thread_server.isRunning():
							if self.do_get_thread.isRunning():
								finalUrl = "http://"+self.local_ip+':'+str(self.local_port)+'/'
							else:
								finalUrl,self.do_get_thread,self.stream_session,self.torrent_handle = self.site_var.getFinalUrl(name,row,self.local_ip+':'+str(self.local_port),'Already Running',self.torrent_download_folder,self.stream_session,ui.tmp_download_folder)
						else:
							finalUrl,self.thread_server,self.do_get_thread,self.stream_session,self.torrent_handle = self.site_var.getFinalUrl(name,row,self.local_ip+':'+str(self.local_port),'First Run',self.torrent_download_folder,self.stream_session,ui.tmp_download_folder)
						self.torrent_handle.set_upload_limit(self.torrent_upload_limit)
						self.torrent_handle.set_download_limit(self.torrent_download_limit)
					else:
						finalUrl = self.site_var.getFinalUrl(name,epn,mirrorNo,quality)
				except:
					print('final url not found')
					return 0
				#del site_var
			
		elif finalUrlFound == True:
				row_num = self.list2.currentRow()
			
				final = epnArrList[row_num]
				print (final)
				self.mark_History()
				finalUrl = []
				if '	' in final:
					final = final.replace('#','')
					final = final.split('	')[1]
				else:
					final=re.sub('#','',final)
				#final = final.decode('utf8')
				finalUrl.append(final)
				if refererNeeded == True:
					if '	' in epnArrList[-1]:
						rfr_url = epnArrList[-1].split('	')[1]
					else:
						rfr_url = epnArrList[-1]
					print (rfr_url)
					finalUrl.append(rfr_url)
				if len(finalUrl) == 1:
					finalUrl = finalUrl[0]
		elif site == "SubbedAnime" or site == "DubbedAnime":
			if category != "Movies":
				self.mark_History()
			if site == "SubbedAnime":
				code = 6
				if base_url == 16:
					epn_t = epn.split(' ')[1]
					new_epn = epn.split(' ')[0]
				else:
					epn_t = epn
				if opt_movies_indicator:
					r = self.list2.currentRow()
					self.epn_name_in_list = name+'-'+self.list2.currentItem().text()
					
					
					if self.site_var:
						self.progressEpn.setFormat('Wait..')
						QtWidgets.QApplication.processEvents()
						try:
							finalUrl = self.site_var.urlResolve(epnArrList[r].split('	')[1])
						except:
							return 0
				else:
					
					
					if self.site_var:
						self.progressEpn.setFormat('Wait..')
						QtWidgets.QApplication.processEvents()
						try:
							finalUrl = self.site_var.getFinalUrl(siteName,name,epn,mirrorNo,category,quality) 
						except:
							return 0
			
			elif site == "DubbedAnime":
				code = 5
				
				if self.site_var:
					self.progressEpn.setFormat('Wait..')
					QtWidgets.QApplication.processEvents()
					try:
						finalUrl = self.site_var.getFinalUrl(siteName,name,epn,mirrorNo,quality) 
					except:
						return 0
		
		elif site == "None" or site == "Music" or site == "Video" or site == "Local":
			if opt == "History" and site == "Local":
				self.mark_History()
			if '	' in epnArrList[row]:
					finalUrl = '"'+(epnArrList[row]).split('	')[1]+'"'
			else:
					finalUrl = '"'+(epnArrList[row]).replace('#','')+'"'
			#finalUrl = finalUrl.decode('utf8')
			print (finalUrl)
			i = str(self.list2.item(row).text())
			#j = self.list2.item(row)
			#self.list2.takeItem(row)
			#del j
			if not i.startswith(self.check_symbol):
				#self.list2.insertItem(row,self.check_symbol+i)
				self.list2.item(row).setText(self.check_symbol+i)
			else:
				#self.list2.insertItem(row,i)
				self.list2.item(row).setText(i)
			self.list2.item(row).setFont(QtGui.QFont('SansSerif', 10,italic=True))
			self.list2.setCurrentRow(row)
			if site == "Music":
				if 'youtube.com' not in finalUrl.lower():
					self.updateMusicCount('count',finalUrl)
			if 'youtube.com' in finalUrl.lower():
				finalUrl = finalUrl.replace('"','')
				finalUrl = get_yt_url(finalUrl,quality).strip()
				finalUrl = '"'+finalUrl+'"'
		new_epn = self.epn_name_in_list
		if site == "Local" or site == "Video" or site == "Music" or site == "None" or site == "PlayLists":
			if type(finalUrl) is list:
				finalUrl = finalUrl[0]
			finalUrl = finalUrl.replace('"','')
			finalUrl = '"'+finalUrl+'"'
			try:
				finalUrl = str(finalUrl)
			except:
				finalUrl = finalUrl
				
			if Player == "mplayer":
				if audio_id == "auto":
					audio_id = "0"
				if sub_id == "auto":
					sub_id = "0"
				command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" -sid "+str(sub_id)+" -aid "+str(audio_id)+" "+finalUrl
			elif Player == "mpv":
				command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+" -sid "+str(sub_id)+" -aid "+str(audio_id)+" "+finalUrl
			print ("mpv=" + str(mpvplayer.processId()))
			print (command)
			if mpvplayer.processId() > 0 :
				mpvplaye.kill()
			self.infoPlay(command)
			
		else:
			if type(finalUrl) is list:
				if mpvplayer:
					if mpvplayer.processId() > 0:
						if refererNeeded == "True":
							finalUrl.pop()
						epnShow = '"'+finalUrl[0]+'"'
						t2 = bytes('\n'+"loadfile "+epnShow+" replace"+'\n','utf-8')
						mpvplayer.write(t2)
						self.queue_url_list[:]=[]
						for i in range(len(finalUrl)-1):
							epnShow ='"'+finalUrl[i+1]+'"'
							self.queue_url_list.append(finalUrl[i+1])
							#t2 = str('\n'+"loadfile "+epnShow+" 1"+'\n')
							#mpvplayer.write(t2.encode('utf-8'))
							#print(t2,'---appended----')
						self.queue_url_list.reverse()
						
						print (finalUrl,'---hello-----')
						
					else:
						if finalUrlFound == True or site=="PlayLists":
							if refererNeeded == True:
								rfr_url = finalUrl[1]
								nepn = str(finalUrl[0])
								epnShow = str(nepn)
								if Player == "mplayer":
									command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" -referrer "+rfr_url+" "+nepn
								elif Player == "mpv":
									command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 --referrer "+rfr_url+" -wid "+idw+" "+nepn
							else:
								nepn = str(finalUrl[0])
								epnShow = nepn
								if Player == "mplayer":
									command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+nepn
								elif Player == "mpv":
									command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+nepn
						
						else:
							self.queue_url_list[:]=[]
							epnShow = finalUrl[0]
							for i in range(len(finalUrl)-1):
								#epnShow = epnShow +' '+finalUrl[i+1]
								self.queue_url_list.append(finalUrl[i+1])
							self.queue_url_list.reverse()
							if Player == "mpv":
								command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+epnShow
							elif Player == "mplayer":
								
								command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" "+epnShow
							#self.queue_url_list.pop()
						print (command)
						if mpvplayer.processId() > 0:
							mpvplayer.kill()
							if Player == 'mplayer':
								try:
									subprocess.Popen(['killall','mplayer'])
								except:
									pass
						self.infoPlay(command)
			else:
				#if '""' in finalUrl:
				finalUrl = finalUrl.replace('"','')
				try:
					finalUrl = str(finalUrl)
				except:
					finalUrl = finalUrl
				finalUrl = '"'+finalUrl+'"'
				if Player == "mplayer":
					if audio_id == "auto":
						audio_id = "0"
					if sub_id == "auto":
						sub_id = "0"
					command = "mplayer -idle -identify -msglevel all=4:statusline=5:global=6 -cache 100000 -cache-min 0.001 -cache-seek-min 0.001 -osdlevel 0 -slave -wid "+idw+" -sid "+sub_id+" -aid "+audio_id+" "+finalUrl
				elif Player == "mpv":
					command = "mpv --cache=auto --cache-default=100000 --cache-initial=0 --cache-seek-min=100 --cache-pause --idle -msg-level=all=v --osd-level=0 --cursor-autohide=no --no-input-cursor --no-osc --no-osd-bar --ytdl=no --input-file=/dev/stdin --input-terminal=no --input-vo-keyboard=no -video-aspect 16:9 -wid "+idw+" "+" -sid "+sub_id+" -aid "+audio_id+" "+finalUrl
				print ("mpv=" + str(mpvplayer.processId()))
				print(Player,'---------state----'+str(mpvplayer.state()))
				"""
				if mpvplayer.processId() > 0:
					#if mpvplayer.processId()>0:
					if Player == "mplayer" or Player == "mpv":
						finalUrl = finalUrl.replace('"','')
						epnShow = '"'+finalUrl+'"'
						if Player == 'mplayer':
							t2 = bytes('\n'+"loadfile "+epnShow+" replace"+'\n','utf-8')
						else:
							t2 = bytes('\n'+"loadfile "+epnShow+'\n','utf-8')
						print (t2)
						mpvplayer.write(t2)
				else:
				"""
				if mpvplayer.processId() > 0:
					mpvplayer.kill()
					if Player == 'mplayer' and mpvplayer.processId() > 0:
						try:
							subprocess.Popen(['killall','mplayer'])
						except:
							pass
				self.infoPlay(command)
				
				
	
		if type(finalUrl) is not list:
			self.final_playing_url = finalUrl.replace('"','')
			if self.final_playing_url.startswith('http'):
				current_playing_file_path = self.final_playing_url
			else:
				current_playing_file_path = '"'+self.final_playing_url+'"'
		else:
			self.final_playing_url = finalUrl[0].replace('"','')
			if refererNeeded == True:
				rfr_url = finalUrl[1].replace('"','')
	
	
	
	def play_video_url(self,player,url):
		print('hello')
	
	def getList(self):
		global nameListArr,opt
		self.list1.clear()
		#m =
		opt = "Random" 
		original_path_name[:] = []
		for i in nameListArr:
			i = i.strip()
			j = i
			if '	' in i:
				i = i.split('	')[0]
			self.list1.addItem(i)
			original_path_name.append(j)
			
	def update_playlist_original(self,pls):
		global epnArrList
		#self.list1.clear()
		self.list2.clear()
		#epnArrList[:]=[]
		file_path = pls
		#fh, abs_path = mkstemp()
		#shutil.copy(file_path,abs_path)
		if os.path.exists(file_path):
			#fh, abs_path = mkstemp()
			"""
			try:
				f = open(file_path,'w')
				j = 0
				for i in epnArrList:
					if j == 0:
						f.write(i)
					else:
						f.write('\n'+i)
					j = j+1
				f.close()
			except:
				print('Error processing playlist file, hence restoring original')
				shutil.copy(abs_path,file_path)
			"""
			write_files(file_path,epnArrList,line_by_line=True)
			self.update_list2()
			
	def update_playlist(self,pls):
		global epnArrList
		#self.list1.clear()
		
		file_path = pls
		if os.path.exists(file_path):
			index = self.btn1.findText('PlayLists')
			if index >= 0:
				self.btn1.setCurrentIndex(index)
				
		if os.path.exists(file_path) and self.btn1.currentText().lower() == 'youtube':
			self.list2.clear()
			epnArrList[:]=[]
			#f = open(file_path,'r')
			#lines = f.readlines()
			#f.close()
			lines = open_files(file_path,True)
			for i in lines:
				i = i.replace('\n','')
				if i:
					epnArrList.append(i)
					"""
					j = i.split('	')[0]
					j = j.replace('_',' ')
					if j.startswith('#'):
						j = j.replace('#',self.check_symbol,1)
					self.list2.addItem((j))
					"""
			self.update_list2()
		elif os.path.exists(file_path) and self.btn1.currentText().lower() == 'playlists':
			#pl_name = file_path.split('/')[-1]
			pl_name = os.path.basename(file_path)
			if not self.list1.currentItem():
				self.list1.setCurrentRow(0)
			if self.list1.currentItem().text() != pl_name:  
				for i in range(self.list1.count()):
					item = self.list1.item(i)
					if item.text() == pl_name:
						self.list1.setCurrentRow(i)
						break
			else:
				#f = open(file_path,'r')
				#lines = f.readlines()
				#f.close()
				lines = open_files(file_path,True)
				new_epn = lines[-1].strip()
				epnArrList.append(new_epn)
				new_epn_title = new_epn.split('	')[0]
				if new_epn_title.startswith('#'):
					new_epn_title = new_epn_title.replace('#',self.check_symbol,1)
				self.list2.addItem(new_epn_title)
				
	def options(self,val):
	
		global opt,pgn,genre_num,site,name,base_url,name1,embed,list1_items,pre_opt,mirrorNo,insidePreopt,quality,home,siteName,finalUrlFound,nameListArr,original_path_name,show_hide_playlist,show_hide_titlelist
		global pict_arr,name_arr,summary_arr,total_till,browse_cnt,tmp_name,hist_arr,list2_items,bookmark,status,viewMode,video_local_stream
		
		hist_arr[:]=[]
		pict_arr[:]=[]
		name_arr[:]=[]
		summary_arr[:]=[]
		#total_till=0
		browse_cnt=0
		tmp_name[:]=[]
		#if site != "Local":
		list2_items=[]
		list1_items[:]=[]
		
		if bookmark == "True":
			r = self.list3.currentRow()
			item = self.list3.item(r)
			if item:
				opt = item.text()
				
				if opt == "All":
					status = "bookmark"
				else:
					status = opt
				
				book_path = os.path.join(home,'Bookmark',status+'.txt')
				if not os.path.isfile(book_path):
					f = open(book_path,'w')
					f.close()
				else:
					self.setPreOpt()
		elif (site!="Local" and site != "Music" and site != "SubbedAnime" and site!= "DubbedAnime" and site!="PlayLists" and site!="Video"):
		
			print (val,'----clicked---',type(val))
			if val == "clicked":
				r = self.list3.currentRow()
				item = self.list3.item(r)
				if item:
					t_opt = str(self.list3.currentItem().text())
			elif val == "history":
				t_opt = "History"
			opt = t_opt
			self.line.clear()
			self.list1.clear()
			self.list2.clear()
			#opt = str(opt)
			if (t_opt == "Genre") and (genre_num == 0):
				self.list3.clear()
				
				
				self.text.setText('Wait...Loading')
				QtWidgets.QApplication.processEvents()
				#try:
				m = self.site_var.getCompleteList(t_opt,genre_num)
				self.text.setText('Load Complete!')
				#except:
				#	self.text.setText('Load Failed!')
				#	return 0
				genre_num = 1
				opt = t_opt
				for i in m:
					self.list3.addItem(i)
				#del site_var
			elif t_opt == "History":
				genre_num = 0
				opt = t_opt
				file_path = os.path.join(home,'History',site,'history.txt')
				if os.path.isfile(file_path):
					#lines = tuple(open(file_path, 'r'))
					lines = open_files(file_path,True)
					#lines_set = set(lines)
					#lines_set.sort()
					#out= open(home+'/History/'+site+'/history.txt', 'w')
					#for line in lines:
					#	if line.strip():
					#		out.write(line)
					#out.close()
					#lins = tuple(open(file_path, 'r'))
					lins = open_files(file_path,True)
					list1_items = []
					original_path_name[:] = []
					for i in lins:
						i = i.strip()
						j = i
						if '	' in i:
							i = i.split('	')[0]
						self.list1.addItem(i)
						list1_items.append(i)
						list2_items.append(i)
						original_path_name.append(j)
					self.forward.hide()
					self.backward.hide()
			elif (t_opt == "MostPopular") or (t_opt == "Newest") or (t_opt == "LatestUpdate"):
				genre_num = 0
				pgn = 1
				
				self.text.setText('Wait...Loading')
				QtWidgets.QApplication.processEvents()
				m = self.site_var.getCompleteList(t_opt,genre_num)
				self.text.setText('Load Complete!')
				list1_items = m
				original_path_name[:]=[]
				for i in m:
					i = i.strip()
					if '	' in i:
						j = i.split('	')[0]
					else:
						j = i
					self.list1.addItem(j)
					original_path_name.append(i)
				self.forward.show()
				self.backward.show()
			elif genre_num == 1:
					pgn = 1
					
					
					self.text.setText('Wait...Loading')
					QtWidgets.QApplication.processEvents()
					#try:
					m = self.site_var.getCompleteList(t_opt,genre_num)
					self.text.setText('Load Complete!')
					#except:
					#	return 0
					#	self.text.setText('Load Failed!')
					list1_items[:] = []
					original_path_name[:]=[]
					for i in m:
						i = i.strip()
						if '	' in i:
							j = i.split('	')[0]
						else:
							j = i
						self.list1.addItem(j)
						original_path_name.append(i)
						list1_items.append(j)
					#del site_var
					self.forward.show()
					self.backward.show()
			else:
				
				opt = t_opt
				
				
				self.text.setText('Wait...Loading')
				QtWidgets.QApplication.processEvents()
				#try:
				if video_local_stream:
					m = self.site_var.getCompleteList(t_opt,ui.list6,ui.progress,ui.tmp_download_folder)
				else:
					m = self.site_var.getCompleteList(t_opt,0)
				self.text.setText('Load Complete!')
				#except:
				#	self.text.setText('Load Failed!')
				#	return 0
					
				list1_items[:] = []
				original_path_name[:]=[]
				for i in m:
					i = i.strip()
					if '	' in i:
						j = i.split('	')[0]
					else:
						j = i
					self.list1.addItem(j)
					list1_items.append(j)
					original_path_name.append(i)
					
				#del site_var
				self.forward.hide()
				self.backward.hide()
		elif site == "SubbedAnime" or site == "DubbedAnime":
			code = 2
			
			siteName = str(self.list3.currentItem().text())
			#if insidePreopt
			if val == "clicked":
				
				opt = "Random"
			else:
				opt = "History"
			
			
			original_path_name[:]=[]
			if opt == "History":
					file_path = os.path.join(home,'History',site,siteName,'history.txt')
					if os.path.isfile(file_path):
						#lines = tuple(open(file_path, 'r'))
						lines = open_files(file_path,True)
						self.label.clear()
						self.line.clear()
						self.list1.clear()
						self.list2.clear()
						self.text.clear()
						original_path_name[:]=[]
						for i in lines:
							i = i.strip()
							if '	' in i:
								j = i.split('	')[0]
							else:
								j = i
							self.list1.addItem(j)
							original_path_name.append(i)
							
							
			if opt != "History":
				self.label.clear()
				self.line.clear()
				self.list1.clear()
				self.list2.clear()
				
				
				if self.site_var:
					self.text.setText('Wait...Loading')
					QtWidgets.QApplication.processEvents()
					try:
						m = self.site_var.getCompleteList(siteName,category,opt) 
						self.text.setText('Load Complete!')
					except:
						self.text.setText('Load Failed!')
						return 0
				list1_items[:] = []
				original_path_name[:]=[]
				for i in m:
					i = i.strip()
					if '	' in i:
						j = i.split('	')[0]
					else:
						j = i
					self.list1.addItem(j)
					original_path_name.append(i)
					list1_items.append(j)
		
		elif site=="Local":
			if insidePreopt != 1:
				opt = self.list3.currentItem().text()
			if val == "local":
				opt = self.list3.currentItem().text()
			if opt == "Random":
				if list1_items:
					list11_items = random.sample(list1_items, len(list1_items))
					
					self.line.clear()
					self.list1.clear()
					self.list2.clear()
					m = []
					for i in list11_items:
						self.list1.addItem(i)
					
			elif opt == "List":
				#print list2_items
				self.list1.clear()
				self.list2.clear()
				#self.list1.setFocus()
				original_path_name[:]=[]
				m = []
				try:
					list2_items = self.importVideoDir()
					print ("list2******************items")
					#print list2_items
					for i in list2_items:
							#k = i.split('/')[-1]
							k = i.replace('/','@')
							original_path_name.append(k)
							self.list1.addItem(k.split('@')[-1])
							m[:]=[]
							if not os.path.exists(os.path.join(home,'Local',k)):
								
								local_dir = i
								for r,d,f in os.walk(local_dir):
									for z in f:
										if z.endswith('.mp4') or z.endswith('.mkv') or z.endswith('.avi') or z.endswith('.flv'):
											m.append(os.path.join(r,z))
								if m:
									os.makedirs(os.path.join(home,'Local',k))
									#m = os.listdir(local_dir)
									m=naturallysorted(m)
									#m.sort(key=os.path.getmtime,reverse=True)
									picn = 'No.jpg'
									summary = 'Summary Not Available'
									f = open(os.path.join(home,'Local',k,'Ep.txt'), 'w')
									for j in m:
										try:
								
											
											f.write(j+'\n')
										except UnicodeEncodeError:
											pass
						
									f.close()
									m[:] = []
				except OSError:
					pass
				#list2_items = naturallysorted(list2_items)
				
			elif opt == "All":
				if os.path.exists(os.path.join(home,'Local')):
					m = os.listdir(os.path.join(home,'Local'))
					m.sort()
					list2_items = []
					self.line.clear()
					self.list1.clear()
					self.list2.clear()
					list1_items[:]=[]
					original_path_name[:]=[]
					for i in m:
						if i.startswith('@'):
							self.list1.addItem(i.split('@')[-1])
							
							list2_items.append(os.path.join(home,'Local',i))
							list1_items.append(i)
							original_path_name.append(i)
					
			elif opt == "History":
				file_path = os.path.join(home,'History',site,'history.txt')
				if os.path.isfile(file_path):
					#f = open(file_path,'r')
					#lins = f.readlines()
					lins = open_files(file_path,True)
					list2_items = []
					self.line.clear()
					self.list1.clear()
					self.list2.clear()
					list1_items[:]=[]
					original_path_name[:]=[]
					for i in lins:
						
						i = i.replace('\n','')
						if i :
							j = i.split('@')[-1]
							original_path_name.append(i)					
							self.list1.addItem(j)
							list2_items.append(i)
							list1_items.append(i)
						
		
		elif site == "Music":
			global update_start
			music_dir = os.path.join(home,'Music')
			if not os.path.exists(music_dir):
				os.makedirs(music_dir)
			music_db = os.path.join(home,'Music','Music.db')
			music_file = os.path.join(home,'Music','Music.txt')
			music_file_bak = os.path.join(home,'Music','Music_bak.txt')
			
			
			if not os.path.exists(music_db):
				
				self.creatUpdateMusicDB(music_db,music_file,music_file_bak)
				
				update_start = 1
				#self.text.clear()
			elif not update_start:
				self.text.setText('Wait..Checking New Files')
				QtWidgets.QApplication.processEvents()
				#self.updateOnStartMusicDB(music_db,music_file,music_file_bak)
				self.update_proc.started.connect(self.update_proc_started)
				self.update_proc.finished.connect(self.update_proc_finished)
				QtCore.QTimer.singleShot(1000, partial(self.updateOnStartMusicDB,music_db,music_file,music_file_bak))
				#music_thread = MusicUpdateThread(music_db,music_file,music_file_bak)
				#music_thread.start()
				#time.sleep(0.5)
				update_start = 1
				self.text.clear()
			if self.list3.currentItem():
				music_opt = str(self.list3.currentItem().text())
			else:
				music_opt = ""
			print (music_opt)
			#if music_opt == "Update":
			
			artist =[]
			if music_opt == "Playlist":
				pls = os.path.join(home,'Playlists')
				if os.path.exists(pls):
					m = os.listdir(pls)
					for i in m:
						artist.append(i)
			else:
				m = self.getMusicDB(music_db,music_opt,"")
				#print m
				for i in m:
					artist.append(i[0])
			#artist = list(set(artist))
			self.list1.clear()
			#print artist
			original_path_name[:] = []
			if music_opt == "Artist" or music_opt == "Album" or music_opt == "Title" or music_opt == "Fav-Artist" or music_opt == "Fav-Album":
				for i in artist:
					original_path_name.append(i)
					self.list1.addItem((i))
				
			elif music_opt == "Directory" or music_opt == "Fav-Directory":
				for i in artist:
					original_path_name.append(i)
					#i = i.split('/')[-1]
					i = os.path.basename(i)
					self.list1.addItem((i))
			elif music_opt == "Playlist":
				for i in artist:
					original_path_name.append(os.path.join(home,'Playlist',i))
					self.list1.addItem((i))
			else:
				artist[:]=[]
				epnArrList[:]=[]
				self.list2.clear()
					
				for i in m:
					epnArrList.append(str(i[1]+'	'+i[2]+'	'+i[0]))
					#self.list2.addItem((i[1]))
				self.update_list2()
		elif site == "Video":
			video_dir = os.path.join(home,'VideoDB')
			if not os.path.exists(video_dir):
				os.makedirs(video_dir)
			video_db = os.path.join(video_dir,'Video.db')
			video_file = os.path.join(video_dir,'Video.txt')
			video_file_bak = os.path.join(video_dir,'Video_bak.txt')
			
			if self.list3.currentItem():
				video_opt = str(self.list3.currentItem().text())
			else:
				video_opt = "History"
			print('----video-----opt',video_opt)
			if val == 'history' and video_opt == 'History':
				video_opt = "History"
			if not os.path.exists(video_db):
				self.creatUpdateVideoDB(video_db,video_file,video_file_bak)
			elif video_opt == "UpdateAll":
				self.updateOnStartVideoDB(video_db,video_file,video_file_bak,video_opt)
				video_opt = "Directory"
			elif video_opt == "Update":
				self.updateOnStartVideoDB(video_db,video_file,video_file_bak,video_opt)
				video_opt = "Directory"
			print (video_opt)
			if video_opt == 'Directory' or video_opt == 'History' or video_opt == 'Available':
				opt = video_opt
			artist = []
			print('----video-----opt',video_opt)
			if video_opt == "Available":
				m = self.getVideoDB(video_db,"Directory","")
			elif video_opt == "History":
				m = self.getVideoDB(video_db,"History","")
			else:
				m = self.getVideoDB(video_db,video_opt,"")
			#print m
			for i in m:
				artist.append(i[0]+'	'+i[1])
			#artist = list(set(artist))
			self.list1.clear()
			#print artist
			original_path_name[:] = []
			if video_opt == "Available" or video_opt == "History":
				for i in artist:
					
					ti = i.split('	')[0]
					di = i.split('	')[1]
					if os.path.exists(di):
						original_path_name.append(i)
						self.list1.addItem((ti))
			elif video_opt == "Directory":
				for i in artist:
					ti = i.split('	')[0]
					di = i.split('	')[1]
					original_path_name.append(i)
					self.list1.addItem((ti))
		elif site == "PlayLists":
			a = 0
			
		self.page_number.setText(str(self.list1.count()))
		insidePreopt = 0
		if opt == "History":
			for i in list2_items:
				hist_arr.append(i)
		
		if (viewMode == "Thumbnail" or not self.tab_6.isHidden()) and (opt == "History" or site == "Local" or bookmark=="True" or site == "PlayLists"):
			if site == "NotMentioned":
				#ui.IconViewEpn()
				#ui.scrollArea1.setFocus()
				print("PlayLists")
			else:
				self.list1.hide()
				self.list2.hide()
				self.tab_5.hide()
				self.label.hide()
				self.text.hide()
				self.frame.hide()
				self.frame1.hide()
				self.goto_epn.hide()
				self.tab_6.show()
				self.tab_2.hide()
				self.scrollArea1.hide()
				self.scrollArea.show()
				
				if opt == "History" or (site == "Local" or site == 'PlayLists') or bookmark == "True":
						i = 0
					
					
						print(total_till,2*self.list1.count()-1,'--count--')
						if total_till > 0 and not self.lock_process:
							
							if not self.scrollArea.isHidden():
								#self.scrollArea.clear()
								self.next_page('deleted')
								
							elif not self.scrollArea1.isHidden():
								#self.scrollArea1.clear()
								self.thumbnail_label_update()
						
						elif total_till == 0:
							if not self.scrollArea.isHidden():
								#self.scrollArea.clear()
								self.next_page('deleted')
							elif not self.scrollArea1.isHidden():
								#self.scrollArea1.clear()
								self.thumbnail_label_update()
					
					
		list1_items[:] = []	
		for i in range(self.list1.count()):
			list1_items.append(str(self.list1.item(i).text()))
		if opt != "History":
			nameListArr[:]=[]
			for i in range(len(original_path_name)):
				nameListArr.append(original_path_name[i])
				
		if self.list1.isHidden() and not self.list2.isHidden():
			if self.list1.count() > 0:
				self.list1.show()
				#self.frame.show()
				show_hide_titlelist = 1
				self.list2.hide()
				self.goto_epn.hide()
				show_hide_playlist = 0
		elif not self.list1.isHidden() and self.list2.isHidden():
			if self.list1.count() == 0 and self.list2.count() > 0:
				self.list1.hide()
				self.frame.hide()
				show_hide_titlelist = 0
				self.list2.show()
				#self.goto_epn.show()
				show_hide_playlist = 1
	
	
	def update_proc_started(self):
		print('checking music for new files')
		
	def update_proc_finished(self):
		print("checking for new music finished")
		
	
		
	
	def importVideoDir(self):
		global home
		
		m =[]
		o = []
		video = []
		p = []
		vid = []
		if os.path.isfile(os.path.join(home,'local.txt')):
			#f = open(os.path.join(home,'local.txt'), 'r')
			#lines_dir = f.readlines()
			#f.close()
			lines_dir = open_files(os.path.join(home,'local.txt'),True)
			for lines_d in lines_dir:
				video[:]=[]
				#lines_d = lines_d.replace('\n','')
				#if lines_d[-1] == '/':
				#	lines_d = lines_d[:-1]
				lines_d = lines_d.strip()
				dirn = os.path.normpath(lines_d)
				#dirn = lines_d
				
				video.append(dirn)
				for r,d,f in os.walk(dirn):
					for z in d:
						#print r+'/'+z
						if not z.startswith('.'):
							video.append(os.path.join(r,z))
						else:
							o.append(os.path.join(r,z))
				
				print (len(m))
				j = 0
				#f = open('/tmp/AnimeWatch/1.txt','w')
				lines = []
				for i in video:
					if os.path.exists(i):
						n = os.listdir(i)
						p[:]=[]
						for k in n:
							if k.endswith('.mp4') or k.endswith('.avi') or k.endswith('.mkv') or k.endswith('.flv'):
								p.append(os.path.join(i,k))
						if p:
							r = i
							#f.write(r+'\n')
							vid.append(str(r))
							j = j+1
						
		return vid
	
	def getVideoDB(self,music_db,queryType,queryVal):
		conn = sqlite3.connect(music_db)
		cur = conn.cursor()    
		q = queryType
		qVal = str(queryVal)
		
		if q == "Directory":
			#print (q)
			if not qVal:
				cur.execute('SELECT distinct Title,Directory FROM Video order by Title')
			else:
				#cur.execute('SELECT distinct EP_NAME,Path FROM Video Where Directory="'+qVal+'" order by EPN')
				qr = 'SELECT distinct EP_NAME,Path FROM Video Where Directory=? order by EPN'
				cur.execute(qr,(qVal,))
		elif q == "Bookmark":
			print (q)
			
			#cur.execute('SELECT EP_NAME,Path FROM Video Where Title="'+qVal+'"')
			qr = 'SELECT EP_NAME,Path FROM Video Where Title=?'
			cur.execute(qr,(qVal,))
		elif q == "History":
			print (q)
			qr = 'SELECT distinct Title,Directory FROM Video Where FileName like ? order by Title'
			#qr = 'SELECT Artist FROM Music Where Artist like "'+ '%'+str(qVal)+'%'+'"'
			print (qr)
			qv = '#'+'%'
			print (qv)
			cur.execute(qr,(qv,))
		rows = cur.fetchall()
		#for i in rows:
		#	print (i[0])
		conn.commit()
		conn.close()
		return rows
		
	def creatUpdateVideoDB(self,video_db,video_file,video_file_bak):
		lines = self.importVideo(video_file,video_file_bak)
		print (len(lines))
		lines.sort()
		if os.path.exists(video_db):
			j = 0
			epn_cnt = 0
			dir_cmp=[]
			conn = sqlite3.connect(video_db)
			cur = conn.cursor()
			for i in lines:
				#i = i.replace('\n','')
				i = i.strip()
				if i:
					w[:]=[]
					#i = str(i)
					#ti = i.split('/')[-2]
					#di = i.rsplit('/',1)[0]
					#na = i.split('/')[-1]
					i = os.path.normpath(i)
					di,na = os.path.split(i)
					ti = os.path.basename(di)
					pa = i
					if j == 0:
						dir_cmp.append(di)
					else:
						tmp = dir_cmp.pop()
						if tmp == di:
							epn_cnt = epn_cnt + 1
						else:
							epn_cnt = 0
						dir_cmp.append(di)
					w = [ti,di,na,na,pa,epn_cnt]
					try:
						cur.execute('INSERT INTO Video VALUES(?,?,?,?,?,?)',w)
						print ("Inserting")
					except:
						print (w)
						print ("Duplicate")
					j =j+1
		else:
			j = 0
			w = []
			dir_cmp = []
			epn_cnt = 0
			conn = sqlite3.connect(video_db)
			cur = conn.cursor()
			cur.execute('''CREATE TABLE Video(Title text,Directory text,FileName text,EP_NAME text,Path text primary key,EPN integer)''')
			for i in lines:
				i = i.strip()
				if i:
					w[:]=[]
					#i = str(i)
					#ti = i.split('/')[-2]
					#di = i.rsplit('/',1)[0]
					#na = i.split('/')[-1]
					#pa = i
					i = os.path.normpath(i)
					di,na = os.path.split(i)
					ti = os.path.basename(di)
					pa = i
					
					if j == 0:
						dir_cmp.append(di)
					else:
						tmp = dir_cmp.pop()
						if tmp == di:
							epn_cnt = epn_cnt + 1
						else:
							epn_cnt = 0
						dir_cmp.append(di)
					w = [ti,di,na,na,pa,epn_cnt]
					#print (w)
					#try:
					cur.execute('INSERT INTO Video VALUES(?,?,?,?,?,?)',w)
					print ("inserted:")
					print (w)
					print (j)
					
					j = j+1
					#print "Inserting"
					#except:
					#	print w
					#	print "Escaping"
		conn.commit()
		conn.close()
	
	def updateVideoCount(self,qType,qVal):
		global home
		qVal = qVal.replace('"','')
		qVal = str(qVal)
		conn = sqlite3.connect(os.path.join(home,'VideoDB','Video.db'))
		cur = conn.cursor()
		if qType == "mark":    
			#qVal = '"'+qVal+'"'
			#cur.execute("Update Music Set LastPlayed=? Where Path=?",(datetime.datetime.now(),qVal))
			print ("----------"+qVal)
			cur.execute('Select FileName,EP_NAME from Video Where Path="'+qVal+'"')
			r = cur.fetchall()
			
			print (r)
			for i in r:
				fname = i[0]
				epName = i[1]
				break
				
			if not fname.startswith('#'):
				fname = '#'+fname
				epName = '#'+epName
			#cur.execute("Update Music Set Playcount=? Where Path=?",(incr,qVal))
			
			qr = 'Update Video Set FileName=?,EP_NAME=? Where Path=?'
			cur.execute(qr,(fname,epName,qVal))
			
		elif qType == "unmark":    
			print ("----------"+qVal)
			cur.execute('Select FileName,EP_NAME from Video Where Path="'+qVal+'"')
			r = cur.fetchall()
			
			print (r)
			for i in r:
				fname = i[0]
				epName = i[1]
				break
				
			if fname.startswith('#'):
				fname = fname.replace('#','')
				epName = epName.replace('#','')
			qr = 'Update Video Set FileName=?,EP_NAME=? Where Path=?'
			cur.execute(qr,(fname,epName,qVal))
				
		
		print ("Number of rows updated: %d" % cur.rowcount)
		conn.commit()
		conn.close()
	def updateOnStartVideoDB(self,video_db,video_file,video_file_bak,video_opt):
		m_files = self.importVideo(video_file,video_file_bak)
		
		conn = sqlite3.connect(video_db)
		cur = conn.cursor()
			
		cur.execute('SELECT Path FROM Video')
		rows = cur.fetchall()
				
		conn.commit()
		conn.close()
		m_files_old = []
		for i in rows:
			m_files_old.append((i[0]))
		
		l1=len(m_files)
		l2=len(m_files_old)
		#if l1 >= l2:
		#m = list(set(m_files)-set(m_files_old))
		#else:
		m = list(set(m_files)-set(m_files_old))+list(set(m_files_old)-set(m_files))
		m.sort()
		
		m_files.sort()
		m_files_old.sort()
		#for i in m_files:
		print(l1)
		print(l2)
		w = []
		conn = sqlite3.connect(video_db)
		cur = conn.cursor()
		for i in m:
			i = i.strip()
			if i:
				
				w[:]=[]
				#i = str(i)
				#ti = i.split('/')[-2]
				#di = i.rsplit('/',1)[0]
				#na = i.split('/')[-1]
				#pa = i
				i = os.path.normpath(i)
				di,na = os.path.split(i)
				ti = os.path.basename(di)
				pa = i
					
				cur.execute('SELECT Path FROM Video Where Path="'+i+'"')
				rows = cur.fetchall()
				cur.execute('SELECT Path FROM Video Where Directory="'+di+'"')
				rows1 = cur.fetchall()
				epn_cnt = len(rows1)
				w = [ti,di,na,na,pa,epn_cnt]
				if video_opt == "UpdateAll":
					if os.path.exists(i) and not rows:
						cur.execute('INSERT INTO Video VALUES(?,?,?,?,?,?)',w)
						print ("Not Inserted, Hence Inserting File = "+i)
						print(w)
					elif not os.path.exists(i) and rows:
						cur.execute('Delete FROM Video Where Path="'+i+'"')
						print ('Deleting File From Database : '+i)
						print(w)
				elif video_opt == "Update":
					if os.path.exists(i) and not rows:
						print (i)
						cur.execute('INSERT INTO Video VALUES(?,?,?,?,?,?)',w)
						print ("Not Inserted, Hence Inserting File = "+i)
						print(w)
				
		conn.commit()
		conn.close()
		
	def importVideo(self,video_file,video_file_bak):
		global home
		m =[]
		o = []
		#fi = open(music_file,'w')
		music = []
		p = []
		m_files = []
		if os.path.isfile(os.path.join(home,'local.txt')):
			#f = open(os.path.join(home,'local.txt'), 'r')
			#lines_dir = f.readlines()
			#f.close()
			lines_dir = open_files(os.path.join(home,'local.txt'),True)
			for lines_d in lines_dir:
				if not lines_d.startswith('#'):
					music[:]=[]
					lines_d = lines_d.strip()
					#if lines_d[-1] == '/':
					#	lines_d = lines_d[:-1]
					lines_d = os.path.normpath(lines_d)
					dirn = lines_d
				
					music.append(dirn)
					for r,d,f in os.walk(dirn):
						for z in d:
							#print r+'/'+z
							if not z.startswith('.'):
								music.append(os.path.join(r,z))
							else:
								o.append(os.path.join(r,z))
					
					print (len(m))
					j = 0
					lines = []
					for i in music:
						if os.path.exists(i):
							n = os.listdir(i)
							p[:]=[]
							for k in n:
								if k.endswith('.mp4') or k.endswith('.mkv') or k.endswith('.flv') or k.endswith('.avi'):
									p.append(os.path.join(i,k))
									
									path = os.path.join(i,k)
									m_files.append(path)
							if p:
								r = i
								lines.append(r)
								j = j+1
						
		return list(set(m_files))
		
	
	def getMusicDB(self,music_db,queryType,queryVal):
		conn = sqlite3.connect(music_db)
		cur = conn.cursor()    
		q = queryType
		qVal = str(queryVal)
		#if '"' in qVal:
		#	qVal = qVal.replace('"','')
		if q == "Artist":
			if not qVal:
				cur.execute('SELECT Distinct Artist FROM Music order by Artist')
			else:
				#cur.execute('SELECT Artist,Title,Path FROM Music Where Artist="'+qVal+'"')
				qr = 'SELECT Artist,Title,Path FROM Music Where Artist=?'
				cur.execute(qr,(qVal,))
		elif q == "Album":
			if not qVal:
				cur.execute('SELECT Distinct Album FROM Music order by Album')
			else:
				#cur.execute('SELECT Artist,Title,Path FROM Music Where Album="'+qVal+'"')
				qr = 'SELECT Artist,Title,Path FROM Music Where Album=?'
				cur.execute(qr,(qVal,))
		elif q == "Title":
			if not qVal:
				cur.execute('SELECT Distinct Title FROM Music order by Title')
			else:
				qr = 'SELECT Artist,Title,Path FROM Music Where Title=?'
				cur.execute(qr,(qVal,))
				#cur.execute('SELECT Artist,Title,Path FROM Music Where Title="'+qVal+'"')
		elif q == "Directory":
			print (q)
			if not qVal:
				cur.execute('SELECT Distinct Directory FROM Music order by Directory')
			else:
				#cur.execute('SELECT Artist,Title,Path FROM Music Where Directory="'+qVal+'"')
				qr = 'SELECT Artist,Title,Path FROM Music Where Directory=?'
				cur.execute(qr,(qVal,))
		elif q == "Playlist":
			print (q)
			if not qVal:
				cur.execute('SELECT Playlist FROM Music')
			else:
				#cur.execute('SELECT Artist,Title,Path FROM Music Where Playlist="'+qVal+'"')
				qr = 'SELECT Artist,Title,Path FROM Music Where Playlist=?'
				cur.execute(qr,(qVal,))
		elif q == "Fav-Artist":
			print (q)
			if not qVal:
				cur.execute("SELECT Distinct Artist FROM Music Where Favourite='yes'")
			else:
				#cur.execute('SELECT Artist,Title,Path FROM Music Where Artist="'+qVal+'"')
				qr = 'SELECT Artist,Title,Path FROM Music Where Artist=?'
				cur.execute(qr,(qVal,))
		elif q == "Fav-Album":
			print (q)
			if not qVal:
				cur.execute("SELECT Distinct Album FROM Music Where Favourite='yes'")
			else:
				#cur.execute('SELECT Artist,Title,Path FROM Music Where Album="'+qVal+'"')
				qr = 'SELECT Artist,Title,Path FROM Music Where Album=?'
				cur.execute(qr,(qVal,))
		elif q == "Fav-Directory":
			print (q)
			if not qVal:
				cur.execute("SELECT Distinct Directory FROM Music Where Favourite='yes'")
			else:
				#cur.execute('SELECT Artist,Title,Path FROM Music Where Directory="'+qVal+'"')
				qr = 'SELECT Artist,Title,Path FROM Music Where Directory=?'
				cur.execute(qr,(qVal,))
			
		
		elif q == "Last 50 Most Played":
			print (q)
			
			cur.execute("SELECT Artist,Title,Path FROM Music order by Playcount desc limit 50")
		elif q == "Last 50 Newly Added":
			print (q)
			cur.execute("SELECT Artist,Title,Path FROM Music order by Modified desc limit 50")
		elif q == "Last 50 Played":
			print (q)
			cur.execute("SELECT Artist,Title,Path FROM Music order by LastPlayed desc limit 50")
		
		elif q == "Search":
			print (q)
			qr = 'SELECT Artist,Title,Path,Album FROM Music Where Artist like ? or Title like ? or Album like ? order by Title'
			#qr = 'SELECT Artist FROM Music Where Artist like "'+ '%'+str(qVal)+'%'+'"'
			print (qr)
			qv = '%'+str(qVal)+'%'
			print (qv)
			cur.execute(qr,(qv,qv,qv,))
		rows = cur.fetchall()
		#print rows
		#for i in rows:
		#	print i[0]
		conn.commit()
		conn.close()
		return rows
	
	def updateMusicCount(self,qType,qVal):
		global home
		qVal = qVal.replace('"','')
		qVal = str(qVal)
		conn = sqlite3.connect(os.path.join(home,'Music','Music.db'))
		cur = conn.cursor()
		if qType == "count":    
			#qVal = '"'+qVal+'"'
			#cur.execute("Update Music Set LastPlayed=? Where Path=?",(datetime.datetime.now(),qVal))
			print ("----------"+qVal)
			cur.execute('Select Playcount,Title from Music Where Path="'+qVal+'"')
			r = cur.fetchall()
			print (r)
			if not r:
				incr = 1
			else:
				print (r)
				for i in r:
					print ("count")
					print (i[0])
					incr = int(i[0])+1
			
			#cur.execute("Update Music Set Playcount=? Where Path=?",(incr,qVal))
			
			try:
				qr = 'Update Music Set LastPlayed=?,Playcount=? Where Path=?'
				q1= datetime.datetime.now()
				#qVal = '"'+qVal+'"'
				cur.execute(qr,(q1,incr,qVal))
			except:
				qr = 'Update Music Set LastPlayed=?,Playcount=? Where Path="'+qVal+'"'
				q1= datetime.datetime.now()
				#qVal = '"'+qVal+'"'
				cur.execute(qr,(q1,incr,))
				
		elif qType == "fav":
			tmp = str(self.list3.currentItem().text())
			if tmp == "Artist":
				qr = 'Update Music Set Favourite="yes" Where Artist=?'
				cur.execute(qr,(qVal,))
			elif tmp == "Album":
				qr = 'Update Music Set Favourite="yes" Where Album=?'
				cur.execute(qr,(qVal,))
			elif tmp == "Directory":
				qr = 'Update Music Set Favourite="yes" Where Directory=?'
				cur.execute(qr,(qVal,))
		print ("Number of rows updated: %d" % cur.rowcount)
		conn.commit()
		conn.close()
	def creatUpdateMusicDB(self,music_db,music_file,music_file_bak):
		self.text.setText('Wait..Tagging')	
		QtWidgets.QApplication.processEvents()
		f = open(music_file,'w')
		f.close()
		#if not os.path.exists(music_file):
		lines = self.importMusic(music_file,music_file_bak)
		#f = open(music_file,'r')
		#lines = f.readlines()
		#f.close()
		#print len(lines)
		if os.path.exists(music_db):
			conn = sqlite3.connect(music_db)
			cur = conn.cursor()
			for k in lines:
				j = k.split('	')[0]
				#i = j.replace('\n','')
				i = j.strip()
				w=self.getTaglib(str(i))
				try:
					cur.execute('INSERT INTO Music VALUES(?,?,?,?,?,?,?,?,?,?,?)',w)
					print ("Inserting")
				except:
					print (w)
					print ("Duplicate")
		else:
			t = 0
			conn = sqlite3.connect(music_db)
			cur = conn.cursor()
			cur.execute('''CREATE TABLE Music(Title text,Artist text,Album text,Directory text,Path text primary key,Playlist text,Favourite text,FavouriteOpt text,Playcount integer,Modified timestamp,LastPlayed timestamp)''')
			for k in lines:
				j = k.split('	')[0]
				#i = j.replace('\n','')
				i = j.strip()
				w=self.getTaglib(str(i))
				#print w
				try:
					cur.execute('INSERT INTO Music VALUES(?,?,?,?,?,?,?,?,?,?,?)',w)
					#print "inserted:"+ i
					#print j 
					
					t = t+1
					self.text.setText('Wait..Tagging '+str(t))
					QtWidgets.QApplication.processEvents()
					#print "Inserting"
				except:
					print (w)
					print ("Escaping")
		conn.commit()
		conn.close()
		self.text.setText('Complete Tagging '+str(t))
		QtWidgets.QApplication.processEvents()
	def getTaglib(self,path):
		t = taglib.File(path)
		#print path
		m = []
		try:
			ar = t.tags['ARTIST']
			ar1 = ar[0]
		except:
			ar1 = "Unknown"
		try:
			ti = t.tags['TITLE']
			ti1 = ti[0]
		except:
			#ti1 = path.split('/')[-1]
			ti1 = os.path.basename(path)
		
		try:
			al = t.tags['ALBUM']
			al1 = al[0]
		except:
			al1 = "Unknown"
		#dir1 = str(path).rsplit('/',1)[0]
		dir1,raw_title = os.path.split(path)
		#print dir1
		#print ar1
		#print al1
		#print ti1
		
		r = ti1+':'+ar1+':'+al1
				
		print (r)		
		
		m.append(str(ti1))
		m.append(str(ar1))
		m.append(str(al1))
		m.append(str(dir1))
		m.append(str(path))
		m.append('')
		m.append('')
		m.append('')
		m.append(0)
		m.append(os.path.getmtime(path))
		m.append(datetime.datetime.now())
		#print m
		return m
	def updateOnStartMusicDB(self,music_db,music_file,music_file_bak):
		m_files = self.importMusic(music_file,music_file_bak)
		
		conn = sqlite3.connect(music_db)
		cur = conn.cursor()
			
		cur.execute('SELECT Path,Modified FROM Music')
		rows = cur.fetchall()
				
		conn.commit()
		conn.close()
		m_files_old = []
		for i in rows:
			j = i[0]+'	'+(str(i[1])).split('.')[0]
			m_files_old.append(str(j))
		
		l1=len(m_files)
		l2=len(m_files_old)
		#if l1 >= l2:
		#	m = list(set(m_files)-set(m_files_old))
		#else:
		#	m = list(set(m_files_old)-set(m_files))
		m = list(set(m_files)-set(m_files_old))+list(set(m_files_old)-set(m_files))
		#print m
		m_files.sort()
		m_files_old.sort()
		#for i in m_files:
		#	print i
		print ("************")
		#for i in m_files_old:
		#	print i
		
		print ("_______________")
		print (m)
		print (m.sort())
		print (len(m))
		print (len(m_files))
		print (len(m_files_old))
		conn = sqlite3.connect(music_db)
		cur = conn.cursor()
		for k in m:
			j = k.split('	')
			#i = i.replace('\n','')
			i = str(j[0])
			
			cur.execute('SELECT Path FROM Music Where Path="'+(i)+'"')
			rows = cur.fetchall()
			
			if os.path.exists(i) and (k in m_files) and not rows:
				w=self.getTaglib(i)
				cur.execute('INSERT INTO Music VALUES(?,?,?,?,?,?,?,?,?,?,?)',w)
				print ("Not Inserted, Hence Inserting File = "+i)
			elif os.path.exists(i) and rows and (k in m_files):
				print ("File Modified")
				cur.execute('Delete FROM Music Where Path="'+i+'"')
				print ('Deleting File From Database : '+i)
				
				w=self.getTaglib(i)
				cur.execute('INSERT INTO Music VALUES(?,?,?,?,?,?,?,?,?,?,?)',w)
				print ("And Now Inserted File Again = "+i)
			elif not os.path.exists(i) and rows:
				cur.execute('Delete FROM Music Where Path="'+i+'"')
				print ('Deleting File From Database : '+i)
			elif os.path.exists(i) and not rows:
				cur.execute('Delete FROM Music Where Path="'+i+'"')
				print ('Deleting File From Database : '+i)
				
		conn.commit()
		conn.close()
	def importMusic(self,music_file,music_file_bak):
		global home
		
		m =[]
		o = []
		#fi = open(music_file,'w')
		music = []
		p = []
		m_files = []
		if os.path.isfile(os.path.join(home,'local.txt')):
			#f = open(os.path.join(home,'local.txt'), 'r')
			#lines_dir = f.readlines()
			#f.close()
			lines_dir = open_files(os.path.join(home,'local.txt'),True)
			for lines_d in lines_dir:
				if not lines_d.startswith('#'):
					music[:]=[]
					#lines_d = lines_d.replace('\n','')
					#if lines_d[-1] == '/':
					#	lines_d = lines_d[:-1]
					lines_d = os.path.normpath(lines_d.strip())
					dirn = lines_d
					music.append(dirn)
					for r,d,f in os.walk(dirn):
						for z in d:
							#print r+'/'+z
							if not z.startswith('.'):
								music.append(os.path.join(r,z))
							else:
								o.append(os.path.join(r,z))
					
					print (len(m))
					j = 0
					lines = []
					for i in music:
						if os.path.exists(i):
							n = os.listdir(i)
							p[:]=[]
							for k in n:
								if k.endswith('.mp3') or k.endswith('.flac') or k.endswith('.ogg') or k.endswith('.wav') or k.endswith('.aac') or k.endswith('.wma') or k.endswith('.m4a') or k.endswith('.m4b') or k.endswith('.opus') or k.endswith('.webm'):
									p.append(os.path.join(i,k))
									
									path = os.path.join(i,k)
									s = (path+'	'+(str(os.path.getmtime(path))).split('.')[0])
									#path = (i+'/'+k).encode('utf-8')
									m_files.append(s)
									#fi.write(i+'/'+k+'\n')
							if p:
								r = i
								#f.write(r+'\n')
								lines.append(r)
								j = j+1
						
		return list(set(m_files))
		
	def music_mode_layout(self):
		global layout_mode,screen_width,show_hide_cover,show_hide_player,show_hide_playlist,show_hide_titlelist,music_arr_setting,opt,new_tray_widget,tray
		#ui.VerticalLayoutLabel.takeAt(2)
		if not self.float_window.isHidden():
			tray.right_menu._detach_video()
			
		ui.music_mode_dim_show = True
		ui.list_with_thumbnail = False
		
		MainWindow.hide()
		print('Music Mode')
		layout_mode = "Music"
		print(ui.music_mode_dim,'--music--mode--')
		MainWindow.showNormal()
		MainWindow.setGeometry(ui.music_mode_dim[0],ui.music_mode_dim[1],ui.music_mode_dim[2],ui.music_mode_dim[3])
		MainWindow.show()
		ui.text.show()
		ui.label.show()
		show_hide_cover = 1
		ui.tab_5.hide()
		show_hide_player = 0
		ui.sd_hd.hide()
		ui.audio_track.hide()
		ui.subtitle_track.hide()
		ui.player_loop_file.show()
		
		cnt = ui.btn1.findText("Music")
		print(music_arr_setting,'--music-setting--')
		if cnt >=0 and cnt < ui.btn1.count():
			ui.btn1.setCurrentIndex(cnt)
			ui.list3.setCurrentRow(music_arr_setting[0])
			ui.list1.setCurrentRow(music_arr_setting[1])
			ui.list1.hide()
			ui.frame.hide()
			show_hide_titlelist = 0
			ui.list2.setCurrentRow(music_arr_setting[2])
			ui.list2.show()
			#ui.goto_epn.show()
			show_hide_playlist = 1
			ui.list2.setFocus()
		ui.buttonStyle(ui.list2)
	def video_mode_layout(self):
		global layout_mode,default_arr_setting,opt,new_tray_widget,tray
		#ui.VerticalLayoutLabel.addStretch(1)
		if not self.float_window.isHidden():
			tray.right_menu._detach_video()
		print('default Mode')
		if ui.music_mode_dim_show:
			ui.music_mode_dim = [MainWindow.pos().x(),MainWindow.pos().y(),MainWindow.width(),MainWindow.height()]
		print(ui.music_mode_dim,'--video--mode--')
		ui.music_mode_dim_show = False
		
		layout_mode = "Default"
		ui.sd_hd.show()
		ui.audio_track.show()
		ui.subtitle_track.show()
		ui.list1.show()
		#ui.frame.show()
		ui.list2.show()
		#ui.goto_epn.show()
		
		print(default_arr_setting,'--default-setting--')
		if default_arr_setting[0] > 0 and default_arr_setting[0] < ui.btn1.count():
			ui.btn1.setCurrentIndex(default_arr_setting[0])
			if ui.btn1.currentText() == 'Addons':
				ui.btnAddon.setCurrentIndex(default_arr_setting[4])
				if ui.btnAddon.currentText() == 'SubbedAnime' or ui.btnAddon.currentText() == 'DubbedAnime':
					ui.btnHistory.show()
				else:
					if not ui.btnHistory.isHidden():
						ui.btnHistory.hide()
			ui.list3.setCurrentRow(default_arr_setting[1])
			try:
				option_val = ui.list3.currentItem().text()
			except:
				option_val = "History"
			if option_val and (option_val == 'History' or option_val == 'Available' or option_val == 'Directory'):
				if option_val == 'History':
					print('--setting-history-option--')
					opt = 'History'
				else:
					opt = option_val
				ui.setPreOpt()
			ui.list1.setCurrentRow(default_arr_setting[2])
			ui.list2.setCurrentRow(default_arr_setting[3])
			ui.list2.setFocus()
			
		MainWindow.showMaximized()
		ui.buttonStyle(ui.list2)
	def _set_window_frame(self):
		global new_tray_widget
		txt = ui.window_frame
		if txt.lower() == 'false':
			MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
			ui.float_window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
			
		else:
			MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint)
			ui.float_window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint)
		MainWindow.show()
			
		
class FloatWindowWidget(QtWidgets.QWidget):
	update_signal = pyqtSignal(str)
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		global epnArrList,tray
		self.update_signal.connect(self.update_progress)
		self.remove_toolbar = True
		#self.setMaximumHeight(200)
		#self.wid = QtWidgets.QWidget(self)
		#self.wid.setMaximumSize(280,340)
		#self.wid.setMinimumSize(280,340)
		self.lay = QtWidgets.QVBoxLayout(self)
		
		#self.l = QtWidgets.QLabel(self.wid)
		#self.l.setMaximumSize(QtCore.QSize(280, 250))
		#self.l.setMinimumSize(QtCore.QSize(280, 250))
		#self.l.setText(_fromUtf8(""))
		#self.l.setScaledContents(True)
		#self.l.setObjectName(_fromUtf8("l_label"))
		
		
		self.title = QtWidgets.QLineEdit(self)
		self.title1 = QtWidgets.QLineEdit(self)
		self.title.setAlignment(QtCore.Qt.AlignCenter)
		self.title1.setAlignment(QtCore.Qt.AlignCenter)
		
		self.progress = QtWidgets.QLineEdit(self)
		self.progress.setAlignment(QtCore.Qt.AlignCenter)
		
		self.f = QtWidgets.QFrame(self)
		self.f.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.f.setFrameShadow(QtWidgets.QFrame.Raised)
		self.horiz = QtWidgets.QHBoxLayout(self.f)
		
		self.p = QtWidgets.QPushButton(self)
		self.p.setText(ui.player_buttons['play'])
		self.p.clicked.connect(ui.playerPlayPause)
		
		
		
		self.pr = QtWidgets.QPushButton(self)
		self.pr.setText(ui.player_buttons['prev'])
		self.pr.clicked.connect(ui.mpvPrevEpnList)
		
		
		self.ne = QtWidgets.QPushButton(self)
		self.ne.setText(ui.player_buttons['next'])
		self.ne.clicked.connect(ui.mpvNextEpnList)
		
		self.st = QtWidgets.QPushButton(self)
		self.st.setText(ui.player_buttons['stop'])
		self.st.clicked.connect(ui.playerStop)
		
		self.attach = QtWidgets.QPushButton(self)
		self.attach.setText(ui.player_buttons['attach'])
		self.attach.clicked.connect(tray.right_menu._detach_video)
		self.attach.setToolTip('Attach Video')
		
		self.qt = QtWidgets.QPushButton(self)
		self.qt.setText(ui.player_buttons['quit'])
		self.qt.clicked.connect(QtWidgets.qApp.quit)
		self.qt.setToolTip('Quit Player')
		
		self.lock = QtWidgets.QPushButton(self)
		self.lock.setText(ui.player_buttons['unlock'])
		self.lock.clicked.connect(lambda x=0: ui.playerLoopFile(self.lock))
		
		self.h_mode = QtWidgets.QPushButton(self)
		self.h_mode.setText('--')
		self.h_mode.setToolTip('Keep Toolbar')
		self.h_mode.clicked.connect(self.lock_toolbar)
		
		self.horiz.insertWidget(0,self.h_mode,0)
		self.horiz.insertWidget(1,self.pr,0)
		self.horiz.insertWidget(2,self.ne,0)
		self.horiz.insertWidget(3,self.p,0)
		self.horiz.insertWidget(4,self.st,0)
		self.horiz.insertWidget(5,self.lock,0)
		self.horiz.insertWidget(6,self.attach,0)
		self.horiz.insertWidget(7,self.qt,0)
		
		
		
		self.lay.insertWidget(0,self.f,0)
		#self.lay.insertWidget(3,self.l,0)
		self.lay.insertWidget(2,self.progress,0)
		self.lay.insertWidget(3,self.title,0)
		self.lay.insertWidget(4,self.title1,0)
		
		
		self.horiz.setSpacing(0)
		self.horiz.setContentsMargins(0,0,0,0)
		self.lay.setSpacing(0)
		self.lay.setContentsMargins(0,0,0,0)		
		
		#self.wid.show()
		#q4 = 'self.setStyleSheet("""font: bold 12px; color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);background-image:url("'+ui.default_background+'");""")'
		#exec (q4)
		ui.float_window_layout.insertWidget(0,self,0)
		self.hide()
		
		self.f.setStyleSheet("font: bold 15px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);height:25px;")
		#
		self.title.setStyleSheet("font:bold 10px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);height:15px;")
		self.title1.setStyleSheet("font: bold 10px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);height:15px;")
		self.progress.setStyleSheet("font: bold 10px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);height:15px;")
		
	def lock_toolbar(self):
		txt = self.h_mode.text()
		if txt == '--':
			
			self.h_mode.setText('+')
			self.h_mode.setToolTip('Remove Toolbar')
			self.remove_toolbar = False
			if ui.tab_5.float_timer.isActive():
				ui.tab_5.float_timer.stop()
			
		else:
			self.h_mode.setText('--')
			self.h_mode.setToolTip('Keep Toolbar')
			self.remove_toolbar = True
			ui.tab_5.float_timer.start(10)
			
	@pyqtSlot(str)
	def update_progress(self,var):
		self.progress.setText(var)
		
class RightClickMenuIndicator(QtWidgets.QMenu):
	def __init__(self,parent=None):
		QtWidgets.QMenu.__init__(self, "File", parent)
		global epnArrList
		
		self.l = QtWidgets.QLabel()
		self.l.setMaximumSize(QtCore.QSize(280, 250))
		self.l.setMinimumSize(QtCore.QSize(280, 250))
		self.l.setText(_fromUtf8(""))
		self.l.setScaledContents(True)
		self.l.setObjectName(_fromUtf8("l_label"))
		self.l.hide()
		
		self.h_mode = QtWidgets.QAction("&Hide", self)
		self.h_mode.triggered.connect(self._hide_mode)
		self.addAction(self.h_mode)
		self.h_mode.setFont(QtGui.QFont('SansSerif', 10,italic=False))
		
		self.m_mode = QtWidgets.QAction("&Music Mode", self)
		self.m_mode.triggered.connect(ui.music_mode_layout)
		self.addAction(self.m_mode)
		self.m_mode.setFont(QtGui.QFont('SansSerif', 10,italic=False))
		
		self.v_mode = QtWidgets.QAction("&Video Mode", self)
		self.v_mode.triggered.connect(ui.video_mode_layout)
		self.addAction(self.v_mode)
		self.v_mode.setFont(QtGui.QFont('SansSerif', 10,italic=False))
		
		self.d_vid = QtWidgets.QAction("&Detach Video", self)
		self.d_vid.triggered.connect(self._detach_video)
		self.addAction(self.d_vid)
		self.d_vid.setFont(QtGui.QFont('SansSerif', 10,italic=False))
		
		if ui.window_frame == 'true':
			self.frameless_mode = QtWidgets.QAction("&Remove Window Frame", self)
		else:
			self.frameless_mode = QtWidgets.QAction("&Allow Window Frame", self)
		self.frameless_mode.triggered.connect(self._remove_frame)
		self.addAction(self.frameless_mode)
		self.frameless_mode.setFont(QtGui.QFont('SansSerif', 10,italic=False))
		
		self.exitAction = QtWidgets.QAction("&Exit", self)
		self.exitAction.triggered.connect(QtWidgets.qApp.quit)
		self.addAction(self.exitAction)
		self.exitAction.setFont(QtGui.QFont('SansSerif', 10,italic=False))
	
		self.title = QtWidgets.QAction("Title", self)
		self.title.triggered.connect(self.info_action_icon)
		self.title.setFont(QtGui.QFont('SansSerif', 10,italic=False))
		
		self.title1 = QtWidgets.QAction("Title1", self)
		self.title1.triggered.connect(self.info_action_icon)
		self.title1.setFont(QtGui.QFont('SansSerif', 10,italic=False))
		
	
	def info_action_icon(self):
		print('clicked empty')
	def _remove_frame(self):
		txt = self.frameless_mode.text()
		m_w = False
		f_w = False
		if not MainWindow.isHidden():
			m_w = True
		if not ui.float_window.isHidden():
			f_w = True
		
		if txt.lower() == '&remove window frame':
			MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
			ui.float_window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
			self.frameless_mode.setText('&Allow Window Frame')
			ui.window_frame = 'false'
		else:
			MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint)
			ui.float_window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint)
			self.frameless_mode.setText('&Remove Window Frame')
			ui.window_frame = 'true'
		
		if m_w:
			MainWindow.show()
		if f_w:
			ui.float_window.show()
			
	def _detach_video(self):
		global new_tray_widget
		txt = self.d_vid.text()
		ui.float_window_open = True
		if txt.lower() == '&detach video':
			self.d_vid.setText('&Attach Video')
			ui.float_window_layout.insertWidget(0,ui.tab_5,0)
			ui.float_window.show()
			ui.tab_5.show()
			MainWindow.hide()
			self.h_mode.setText('&Hide')
			ui.float_window.setGeometry(ui.float_window_dim[0],ui.float_window_dim[1],ui.float_window_dim[2],ui.float_window_dim[3])
			ui.list2.setFlow(QtWidgets.QListWidget.LeftToRight)
			ui.list2.setMaximumWidth(16777215)
			new_tray_widget.lay.insertWidget(1,ui.list2,0)
		else:
			self.d_vid.setText('&Detach Video')
			ui.gridLayout.addWidget(ui.tab_5,0,1,1,1)
			ui.float_window_dim = [ui.float_window.pos().x(),ui.float_window.pos().y(),ui.float_window.width(),ui.float_window.height()]
			ui.float_window.hide()
			MainWindow.show()
			self.h_mode.setText('&Hide')
			ui.list2.setFlow(QtWidgets.QListWidget.TopToBottom)
			ui.list2.setMaximumWidth(300)
			ui.verticalLayout_50.insertWidget(0,ui.list2,0)
			
	def _hide_mode(self):
		txt = self.h_mode.text()
		if not ui.float_window.isHidden():
			ui.float_window.hide()
			self.h_mode.setText('&Show')
		elif self.d_vid.text().lower() == '&attach video':
			ui.float_window.show()
			self.h_mode.setText('&Hide')
		else:
			if txt == '&Hide':
				MainWindow.hide()
				self.h_mode.setText('&Show')
			elif txt == '&Show':
				self.h_mode.setText('&Hide')
				if ui.music_mode_dim_show:
					MainWindow.showNormal()
					MainWindow.setGeometry(ui.music_mode_dim[0],ui.music_mode_dim[1],ui.music_mode_dim[2],ui.music_mode_dim[3])
					MainWindow.show()
				else:
					MainWindow.showMaximized()
			
class SystemAppIndicator(QtWidgets.QSystemTrayIcon):
	def __init__(self,parent=None):
		global name,home
		QtWidgets.QSystemTrayIcon.__init__(self, parent)
		#self.icon = QtGui.QLabel()
		icon_img = os.path.join(home,'src','tray.png')
		self.right_menu = RightClickMenuIndicator()
		self.setContextMenu(self.right_menu)

		self.activated.connect(self.onTrayIconActivated)
		self.p = QtGui.QPixmap(24,24)
		self.p.fill(QtGui.QColor("transparent"))
		painter	= QtGui.QPainter(self.p)
		if os.path.exists(icon_img):
			self.setIcon(QtGui.QIcon(icon_img))
		else:
			self.setIcon(QtGui.QIcon(""))
		self.full_scr = 1
		del painter
	
	def mouseMoveEvent(self,event):
		global site
		pos = event.pos()
		print(pos)
	
	def onTrayIconActivated(self, reason):
		if reason == QtWidgets.QSystemTrayIcon.Trigger:
			if not ui.float_window.isHidden():
				ui.float_window.hide()
				self.right_menu.h_mode.setText('&Show')
			elif self.right_menu.d_vid.text().lower() == '&attach video':
				ui.float_window.show()
				self.right_menu.h_mode.setText('&Hide')
			else:
				if MainWindow.isHidden():
					self.right_menu.h_mode.setText('&Hide')
					if ui.music_mode_dim_show:
						MainWindow.showNormal()
						MainWindow.setGeometry(ui.music_mode_dim[0],ui.music_mode_dim[1],ui.music_mode_dim[2],ui.music_mode_dim[3])
						MainWindow.show()
					else:
						MainWindow.showMaximized()
						
				else:
					MainWindow.hide()
					self.right_menu.h_mode.setText('&Show')
			"""
			geom = self.geometry()
			x = geom.x()
			y = geom.y()
			print(x,y)
			if (x+280) > screen_width:
				t = (x+280)-screen_width
				x = x-t
			if (y+340) > screen_height:
				t = (y+40)-screen_height
				y = y-t
			new_tray_widget.setGeometry(x,y,280,340)
			"""
			
def main():
	global ui,MainWindow,tray,hdr,name,pgn,genre_num,site,name,epn,base_url,name1,embed,epn_goto,list1_items,opt,mirrorNo,mpv,queueNo,playMpv,mpvAlive,pre_opt,insidePreopt,posterManually,labelGeometry,tray,new_tray_widget
	global downloadVideo,list2_items,quality,indexQueue,Player,startPlayer,rfr_url,category,fullscr,mpvplayer,curR,idw,idwMain,home,home1,player_focus,fullscrT,artist_name_mplayer
	global pict_arr,name_arr,summary_arr,total_till,tmp_name,browse_cnt,label_arr,hist_arr,nxtImg_cnt,view_layout,quitReally,toggleCache,status,wget,mplayerLength,type_arr,playlist_show,img_arr_artist
	global cache_empty,buffering_mplayer,slider_clicked,epnArrList,interval,total_seek,iconv_r,path_final_Url,memory_num_arr,mpv_indicator,pause_indicator,icon_size_arr,default_option_arr,original_path_name
	global thumbnail_indicator,opt_movies_indicator,epn_name_in_list,cur_label_num,iconv_r_indicator,tab_6_size_indicator,viewMode,tab_6_player,audio_id,sub_id,site_arr,siteName,finalUrlFound,refererNeeded,base_url_picn,base_url_summary,nameListArr,update_start,lastDir,screen_width,screen_height,total_till_epn,mpv_start
	global show_hide_cover,show_hide_playlist,show_hide_titlelist,server,show_hide_player,layout_mode,current_playing_file_path,music_arr_setting,default_arr_setting,video_local_stream,local_torrent_file_path,wait_player
	
	
	wait_player = False
	local_torrent_file_path = ''
	path_final_Url = ''
	video_local_stream = False
	default_arr_setting = [0,0,0,0,0]
	music_arr_setting = [0,0,0]
	layout_mode = "Default"
	show_hide_player = 0
	show_hide_cover = 1
	show_hide_playlist = 1
	show_hide_titlelist = 1
	mpv_start = []
	total_till_epn = 0
	idw = ""
	update_start = 0
	nameListArr = []
	artist_name_mplayer =""
	img_arr_artist = []
	playlist_show = 1
	original_path_name = []
	siteName = ""
	finalUrlFound = False
	refererNeeded = False
	base_url_picn = ""
	base_url_summary = ""
	type_arr = ['.mkv','.mp4','.avi','.mp3','.flv','.flac']
	site_arr = ["SubbedAnime","DubbedAnime","Local","PlayLists","Bookmark","Music",'Video','YouTube','None']
	default_option_arr = ["Select","Video","Music","Local","Bookmark","PlayLists","YouTube","Addons"]
	addons_option_arr = []
	audio_id = "auto"
	sub_id = "auto"
	tab_6_player = "False"
	icon_size_arr = []
	viewMode = "List"
	tab_6_size_indicator = []
	iconv_r_indicator = []
	cur_label_num = 0
	labelGeometry = 0
	opt_movies_indicator=[]
	thumbnail_indicator=[]
	pause_indicator = []
	mpv_indicator = []
	memory_num_arr = []
	iconv_r = 4
	total_seek = 0
	interval = 0
	epnArrList = []
	slider_clicked = "no"
	buffering_mplayer = "no"
	cache_empty = "no"
	fullscrT = 0
	player_focus = 0
	mplayerLength = 0
	wget = QtCore.QProcess()
	
		
	status = "bookmark"
	toggleCache = 0
	quitReally = "no"
	view_layout = "List"
	nxtImg_cnt = 0
	hist_arr=[]
	label_arr=[]
	total_till = 0
	pict_arr=[]
	name_arr=[]
	summary_arr=[]
	browse_cnt = 0
	tmp_name=[]
	home = expanduser("~")
	home1 = home
	lastDir = home
	home = os.path.join(home,'.config','AnimeWatch')
	curR = 0
	mpvplayer = QtCore.QProcess()
	fullscr = 0
	category = "Animes"
	rfr_url = ""
	startPlayer = "Yes"
	
	Player = "mpv"
	indexQueue = 0
	quality = "sd"
	list2_items = []
	posterManually = 0
	downloadVideo = 0
	insidePreopt = 0
	pre_opt = ""
	mpvAlive = 0
	playMpv = 1
	queueNo = 0
	mpv = ""
	mirrorNo = 1
	list1_items = []
	epn_goto = 0
	epn = ""
	embed = 0
	name1 = ""
	base_url = 0
	epn = ''
	name = ''
	site = "Local"
	genre_num = 0
	opt = ""
	pgn = 1
	site_index = 0
	addon_index = 0
	option_index = -1
	name_index = -1
	episode_index = -1
	option_val = ''
	dock_opt = 1
	pos_x = 0
	pos_y = 0
	w_ht = 0
	w_wdt = 50
	old_version = (0,0,0,0)
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0"
	try:
		dbus.mainloop.pyqt5.DBusQtMainLoop(set_as_default=True)
		
	except:
		pass
	
	app = QtWidgets.QApplication(sys.argv)
	#MainWindow = QtGui.QWidget()
	screen_resolution = app.desktop().screenGeometry()
	screen_width = screen_resolution.width()
	screen_height = screen_resolution.height()
	print (screen_height,screen_width)
	MainWindow = MainWindowWidget()
	MainWindow.setMouseTracking(True)
	#MainWindow = mouseoverEvent()
	#ui = Ui_Form()
	#MainWindow.showNormal()
	#MainWindow.showMaximized()
	#Frame = QtGui.QFrame()
	#MainWindow = QMWin()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	#print(MainWindow.pos().x(),MainWindow.pos().y(),'--pos--')
	#print(MainWindow.size(),'--size--')
	#MainWindow.move(pos_x,pos_y)
	
	
	#MainWindow.showMaximized()
	
	ui.btn1.setFocus()
	ui.dockWidget_4.hide()
	#ui.text.hide()
	
	
	
	
		
	if not os.path.exists(home):
		os.makedirs(home)
	if not os.path.exists(os.path.join(home,'src')):
		src_new = os.path.join(home,'src')
		os.makedirs(src_new)
		input_conf = os.path.join(BASEDIR,'input.conf')
		if os.path.exists(input_conf):
			shutil.copy(input_conf,os.path.join(src_new,'input.conf'))
		png_n = os.path.join(BASEDIR,'1.png')
		if os.path.exists(png_n):
			shutil.copy(png_n,os.path.join(src_new,'1.png'))
		introspect_xml = os.path.join(BASEDIR,'introspect.xml')
		if os.path.exists(introspect_xml):
			shutil.copy(introspect_xml,os.path.join(src_new,'introspect.xml'))
		tray_png = os.path.join(BASEDIR,'tray.png')
		if os.path.exists(tray_png):
			shutil.copy(tray_png, os.path.join(src_new,'tray.png'))
	picn = os.path.join(home,'default.jpg')
	if not os.path.exists(picn):
		picn_1 = os.path.join(BASEDIR,'default.jpg')
		if os.path.exists(picn_1):
			shutil.copy(picn_1,picn)
			
	QtCore.QTimer.singleShot(100, partial(set_mainwindow_palette,picn))
	
	ui.buttonStyle()
	
	if not os.path.exists(os.path.join(home,'src','Plugins')):
		os.makedirs(os.path.join(home,'src','Plugins'))
		sys.path.append(os.path.join(home,'src','Plugins'))
		plugin_Dir = os.path.join(home,'src','Plugins')
		s_dir = os.path.join(BASEDIR,'Plugins')
		if not os.path.exists(s_dir):
			s_dir = os.path.join(BASEDIR,'plugins')
		if os.path.exists(s_dir):
			m_tmp = os.listdir(s_dir)
			for i in m_tmp:
				k = os.path.join(s_dir,i)
				if os.path.isfile(k) and i != "install.py" and i != "installPlugins.py" and i != '__init__':
					shutil.copy(k,plugin_Dir)
					print ("addons loading....")
						
	if os.path.exists(os.path.join(home,'config.txt')):
		#f = open(os.path.join(home,'config.txt'),'r')
		#lines = f.readlines()
		#f.close()
		lines = open_files(os.path.join(home,'config.txt'),True)
		for i in lines:
			if not i.startswith('#'):
				j = i.split('=')[-1]
				if "VERSION_NUMBER" in i:
					try:
						j = j.replace('\n','')
						j = j.replace('(','')
						j = j.replace(')','')
						j = j.replace(' ','')
						k = j.split(',')
						jr = []
						for l in k:
							jr.append(int(l))
						old_version = tuple(jr)
					except:
						pass
					#print(old_version)
				elif "FloatWindow" in i:
					try:
						j = j.replace('\n','')
						j = j.replace('[','')
						j = j.replace(']','')
						j = j.replace(' ','')
						k = j.split(',')
						ui.float_window_dim[:] = []
						for l in k:
							ui.float_window_dim.append(int(l))
						print(ui.float_window_dim)
					except:
						ui.float_window_dim = [0,0,250,200]
				elif "MusicWindowDim" in i:
					try:
						j = j.replace('\n','')
						j = j.replace('[','')
						j = j.replace(']','')
						j = j.replace(' ','')
						k = j.split(',')
						ui.music_mode_dim[:] = []
						for l in k:
							ui.music_mode_dim.append(int(l))
						print(ui.music_mode_dim,'--music--mode--dimension--set--')
					except:
						ui.music_mode_dim = [0,0,900,350]
				elif "DefaultPlayer" in i:
					
					Player = re.sub('\n','',j)
					cnt = ui.chk.findText(Player)
					if cnt >=0 and cnt < ui.chk.count():
						ui.chk.setCurrentIndex(cnt)
				elif "WindowFrame" in i:
					try:
						j = j.replace('\n','')
						ui.window_frame = str(j)
					except:
						ui.window_frame = 'true'
				elif "DockPos" in i:
					try:
						j = j.strip()
						ui.orientation_dock = str(j)
					except:
						ui.orientation_dock = 'left'
				elif "MusicModeDimShow" in i:
					try:
						j = j.replace('\n','')
						val_m = str(j)
					except:
						val_m = 'False'
					if val_m.lower() == 'true':
						ui.music_mode_dim_show = True
					else:
						ui.music_mode_dim_show = False
				elif "List_Mode_With_Thumbnail" in i:
					tmp_mode = re.sub('\n','',j)
					if tmp_mode.lower() == 'true':
						ui.list_with_thumbnail = True
						ui.list2.setStyleSheet("""QListWidget{font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;}
				QListWidget:item {height: 112px;}
				QListWidget:item:selected:active {background:rgba(0,0,0,20%);color: violet;}
				QListWidget:item:selected:inactive {border:rgba(0,0,0,30%);}
				QMenu{font: bold 12px;color:black;background-image:url('1.png');}""")
					else:
						ui.list2.setStyleSheet("""QListWidget{font: bold 12px;color:white;background:rgba(0,0,0,30%);border:rgba(0,0,0,30%);border-radius: 3px;}
				QListWidget:item {height: 30px;}
				QListWidget:item:selected:active {background:rgba(0,0,0,20%);color: violet;}
				QListWidget:item:selected:inactive {border:rgba(0,0,0,30%);}
				QMenu{font: bold 12px;color:black;background-image:url('1.png');}""")
						ui.list_with_thumbnail = False
				elif "Site_Index" in i:
					site_i = re.sub('\n','',j)
					if site_i.isdigit():
						site_index = int(site_i)
					
					print(site_index,'--site-index--')
				elif "Addon_Index" in i:
					addon_i = re.sub('\n','',j)
					if addon_i.isdigit():
						addon_index = int(addon_i)
					
					print(addon_index,'--addon-index--')
				elif "Option_Index" in i:
					opt_i = re.sub('\n','',j)
					if opt_i.isdigit():
						option_index = int(opt_i)
					
					print(option_index,'--option-index--')
				elif "Name_Index" in i:
					name_i = re.sub('\n','',j)
					if name_i.isdigit():
						name_index = int(name_i)
					
					print(name_index,'--name-index--')
				elif "Episode_Index" in i:
					epi_i = re.sub('\n','',j)
					if epi_i.isdigit():
						episode_index = int(epi_i)
					
					print(episode_index,'--episode-index--')
				elif "Option_Val" in i:
					opt_v = re.sub('\n','',j)
					option_val = opt_v
					print(option_val,'--option--')
				elif "Quality" in i:
					quality = re.sub('\n','',j)
					if quality == "hd":
						ui.sd_hd.setText("HD")
					elif quality == 'sd480p':
						ui.sd_hd.setText("480")
					else:
						ui.sd_hd.setText("SD")
				elif "Dock_Option" in i:
					dock_o = re.sub('\n','',j)
					if dock_o.isdigit():
						dock_opt = int(dock_o)
						
				elif "Show_Hide_Cover" in i:
					try:
						show_hide_cover = int(j)
						if show_hide_cover == 0:
							ui.text.hide()
							ui.label.hide()
						
					except:
						show_hide_cover = 0
				elif "Show_Hide_Playlist" in i:
					try:
						show_hide_playlist = int(j)
						if show_hide_playlist == 0:
							ui.list2.hide()
							ui.goto_epn.hide()
							
					except:
						show_hide_playlist = 0
				elif "Show_Hide_Titlelist" in i:
					try:
						show_hide_titlelist = int(j)
						if show_hide_titlelist == 0:
							ui.list1.hide()
							ui.frame.hide()
					except:
						show_hide_titlelist = 0
				elif "Show_Hide_Player" in i:
					try:
						show_hide_player = int(j)
					except:
						show_hide_player = 0
				elif "Thumbnail_Size" in i:
					j = j.replace('\n','')
					if j:
						iconv_r = int(j)
						iconv_r_indicator.append(iconv_r)
				elif "View" in i:
					viewMode = j.replace('\n','')
					if viewMode=="Thumbnail":
						ui.comboView.setCurrentIndex(2)
					elif viewMode=="List":
						ui.comboView.setCurrentIndex(1)
				elif "Layout" in i:
					layout_mode = j.replace('\n','')
				elif "POSX" in i:
					posx = re.sub('\n','',j)
					if posx.isdigit():
						pos_x = int(posx)
				elif "POSY" in i:
					pos_yy = re.sub('\n','',j)
					if pos_yy.isdigit():
						pos_y = int(pos_yy)
				elif "WHeight" in i:
					ht1 = re.sub('\n','',j)
					if ht1.isdigit():
						w_ht = int(ht1)
				elif "WWidth" in i:
					wd2 = re.sub('\n','',j)
					if wd2.isdigit():
						w_wdt = int(wd2)
				elif "Default_Mode" in i:
					def_m = re.sub('\n','',j)
					t_v = def_m.split(',')
					n = 0
					for l in range(len(t_v)):
						default_arr_setting[n] = int(t_v[l])
						n = n+1
				elif 'Music_Mode' in i:
					def_m = re.sub('\n','',j)
					t_v = def_m.split(',')
					n = 0
					for l in range(len(t_v)):
						music_arr_setting[n] = int(t_v[l])
						n = n+1
	else:
		f = open(os.path.join(home,'config.txt'),'w')
		f.write("DefaultPlayer=mpv")
		f.close()
	
	if os.path.exists(os.path.join(home,'torrent_config.txt')):
		f = open(os.path.join(home,'torrent_config.txt'),'r')
		lines = f.readlines()
		f.close()
		for i in lines:
			if not i.startswith('#'):
				j = i.split('=')[-1]
				if "TORRENT_STREAM_IP" in i:
					j = re.sub('\n','',j)
					j1 = j.split(':')
					if len(j1) == 2:
						if j1[0].lower()=='localhost' or not j1[0]:
							ui.local_ip = '127.0.0.1'
						else:
							ui.local_ip = j1[0]
						ui.local_port = int(j1[1])
					else:
						ui.local_ip = '127.0.0.1'
						ui.local_port = 8001
				elif "TORRENT_DOWNLOAD_FOLDER" in i:
					j = re.sub('\n','',j)
					if j.endswith('/'):
						j = j[:-1]
					if os.path.exists(j):
						ui.torrent_download_folder = j
					else:
						ui.torrent_download_folder = TMPDIR
				elif "TORRENT_UPLOAD_RATE" in i:
					j = re.sub('\n','',j)
					try:
						ui.torrent_upload_limit = int(j)*1024
					except:
						ui.torrent_upload_limit = 0
				elif "TORRENT_DOWNLOAD_RATE" in i:
					j = re.sub('\n','',j)
					try:
						ui.torrent_download_limit = int(j)*1024
					except:
						ui.torrent_download_limit = 0
	else:
		f = open(os.path.join(home,'torrent_config.txt'),'w')
		f.write("TORRENT_STREAM_IP=127.0.0.1:8001")
		f.write("\nTORRENT_DOWNLOAD_FOLDER="+TMPDIR)
		f.write("\nTORRENT_UPLOAD_RATE=0")
		f.write("\nTORRENT_DOWNLOAD_RATE=0")
		f.close()
		ui.local_ip = '127.0.0.1'
		ui.local_port = 8001
		
	if os.path.exists(os.path.join(home,'other_options.txt')):
		f = open(os.path.join(home,'other_options.txt'),'r')
		lines = f.readlines()
		f.close()
		for i in lines:
			j = i.split('=')[-1]
			if "LOCAL_STREAM_IP" in i:
				j = re.sub('\n','',j)
				j1 = j.split(':')
				if len(j1) == 2:
					if j1[0].lower()=='localhost' or not j1[0]:
						ui.local_ip_stream = '127.0.0.1'
					else:
						ui.local_ip_stream = j1[0]
					ui.local_port_stream = int(j1[1])
				else:
					ui.local_ip_stream = '127.0.0.1'
					ui.local_port_stream = 9001
			elif 'DEFAULT_DOWNLOAD_LOCATION' in i:
				j = re.sub('\n','',j)
				ui.default_download_location = j
	else:
		f = open(os.path.join(home,'other_options.txt'),'w')
		f.write("LOCAL_STREAM_IP=127.0.0.1:9001")
		f.write("\nDEFAULT_DOWNLOAD_LOCATION="+TMPDIR)
		f.write("\nTMP_REMOVE=no")
		f.close()
		ui.local_ip_stream = '127.0.0.1'
		ui.local_port_stream = 9001
		
	print(ui.torrent_download_limit,ui.torrent_upload_limit)
	
	arr_setting = []
	
	arr_setting.append(show_hide_titlelist)
	arr_setting.append(show_hide_playlist)
	
	if not os.path.exists(TMPDIR):
		os.makedirs(TMPDIR)
	if not os.path.exists(home):
		os.makedirs(home)
	if os.path.exists(os.path.join(home,'src')):
		os.chdir(os.path.join(home,'src'))
		#sys.path.append(os.path.join(home,'src'))
	else:
		os.chdir(BASEDIR)
	if not os.path.exists(os.path.join(home,"History")):
		os.makedirs(os.path.join(home,"History"))
	if not os.path.exists(os.path.join(home,"thumbnails")):
		os.makedirs(os.path.join(home,"thumbnails"))
	if not os.path.exists(os.path.join(home,"Local")):
		os.makedirs(os.path.join(home,"Local"))
	if not os.path.exists(os.path.join(home,"Bookmark")):
		os.makedirs(os.path.join(home,"Bookmark"))
		bookmark_array = ['bookmark','Watching','Completed','Incomplete','Later','Interesting','Music-Videos']
		for i in bookmark_array:
			bookmark_path = os.path.join(home,'Bookmark',i+'.txt')
			if not os.path.exists(bookmark_path):
				f = open(bookmark_path,'w')
				f.close()
	if not os.path.exists(os.path.join(home,"config.txt")):
		f = open(os.path.join(home,"config.txt"),"w")
		f.write("DefaultPlayer=mpv")
		f.close()
	if not os.path.exists(os.path.join(home,"Playlists")):
		os.makedirs(os.path.join(home,"Playlists"))
	if not os.path.exists(ui.yt_sub_folder):
		os.makedirs(ui.yt_sub_folder)
	if not os.path.exists(os.path.join(home,"Playlists","Default")):
		f = open(os.path.join(home,"Playlists","Default"),"w")
		f.close()
	
	#if os.path.exists('/usr/share/AnimeWatch'):
	#	sys.path.append('/usr/share/AnimeWatch')
	
	if os.path.exists(os.path.join(home,'src','Plugins')):
		sys.path.append(os.path.join(home,'src','Plugins'))
		print ("plugins")
		
		if ui.version_number > old_version:
			print(ui.version_number,'>',old_version)
			plugin_Dir = os.path.join(home,'src','Plugins')
			s_dir = os.path.join(BASEDIR,'Plugins')
			if not os.path.exists(s_dir):
				s_dir = os.path.join(BASEDIR,'plugins')
			if os.path.exists(s_dir):
				m_tmp = os.listdir(s_dir)
				for i in m_tmp:
					k = os.path.join(s_dir,i)
					if os.path.isfile(k) and i != "install.py" and i != "installPlugins.py" and i != '__init__':
						shutil.copy(k,plugin_Dir)
						print('Addons loading ....')
		
		m = os.listdir(os.path.join(home,'src','Plugins'))
		m.sort()
		for i in m:
			if i.endswith('.py'):
				i = i.replace('.py','')
				if i != 'headlessBrowser' and i != 'headlessEngine' and i!='stream' and i!='local_ip' and i!= 'headlessBrowser_webkit' and i!='installPlugins' and i != '__init__':
					addons_option_arr.append(i)
	
	
	f = open(os.path.join(home,"History","queue.m3u"),"w")
	f.write("#EXTM3U")
	f.close()
	
	for i in default_option_arr:
		ui.btn1.addItem(i)
	for i in addons_option_arr:
		ui.btnAddon.addItem(i)
	#QtWidgets.QApplication.processEvents()
	#index_site = ui.btn1.findText(site)
	
	print(site,site_index,'==site_index')
	if site_index >0 and site_index < ui.btn1.count():
		ui.btn1.setCurrentIndex(site_index)
		if ui.btn1.currentText() == 'Addons' and addon_index >=0 and addon_index < ui.btnAddon.count():
			ui.btnAddon.setCurrentIndex(addon_index)
	elif site_index == 0:
		ui.btn1.setCurrentIndex(1)
		ui.btn1.setCurrentIndex(0)
		
	if option_index < 0 and ui.list3.count() > 0:
		option_index = 0
		print(option_index,ui.list3.count(),'--list3--cnt--')
	
	if option_index >=0 and option_index < ui.list3.count():
		ui.list3.setCurrentRow(option_index)
		ui.list3.setFocus()
		if option_val and (option_val == 'History' or option_val == 'Available' or option_val == 'Directory'):
			if option_val == 'History':
				print('--setting-history-option--')
				opt = 'History'
			else:
				opt = option_val
			ui.setPreOpt()
	print(name_index,ui.list1.count())
	if name_index >=0 and name_index < ui.list1.count():
		ui.list1.setCurrentRow(name_index)
		ui.list1.setFocus()
		ui.list1_double_clicked()
	if episode_index >=0 and episode_index < ui.list2.count():
		ui.list2.setCurrentRow(episode_index)
		ui.list2.setFocus()
	print(dock_opt,'--dock-option---')
	if ui.orientation_dock == 'left':
		ui.orient_dock('left')
	else:
		ui.orient_dock('right')
	if dock_opt == 0:
		ui.dockWidget_3.hide()
	else:
		ui.dockWidget_3.show()
	
	
	print(int(MainWindow.winId()))
	#myFilter	 = MyEventFilter()
	#app.installEventFilter(myFilter)
	#gc.disable()
	#tray = SystemTrayIcon(pos_x,pos_y,w_wdt,w_ht)
	#try:
	
	platform_name = os.getenv('DESKTOP_SESSION')
	print(platform_name)
	tray = SystemAppIndicator()
	tray.show()
	new_tray_widget = FloatWindowWidget()
	if ui.window_frame == 'false':
		ui._set_window_frame()
	#except:
	#pass
	
	#try:
	server = MprisServer(ui,home,tray,new_tray_widget)
		
	#except:
	#	pass
	
	if layout_mode == "Music":
		try:
			t1 = tray.geometry().height()
		except:
			t1 = 65
			
		MainWindow.setGeometry(ui.music_mode_dim[0],ui.music_mode_dim[1],ui.music_mode_dim[2],ui.music_mode_dim[3])
		
		"""
		print(t1,'tray--geometry\n')
		if t1 > 64:
			pos_y = 22
		else:
			t2 = QtWidgets.QApplication.style().pixelMetric(QtWidgets.QStyle.PM_TitleBarHeight)
			t = t1+t2
			print(t,'--title-bar-ht--')
			pos_y = t1
		if w_wdt == screen_width:
			w_wdt = 900
			w_ht = 350
		ui.sd_hd.hide()
		ui.audio_track.hide()
		ui.subtitle_track.hide()
		ui.player_loop_file.show()
		
		#ui.options('layout_mode_music_startup')
		MainWindow.setGeometry(pos_x,pos_y,w_wdt,w_ht)
		"""
	
	else:
		ui.sd_hd.show()
		ui.audio_track.show()
		ui.subtitle_track.show()
		#ui.player_loop_file.hide()
		MainWindow.showMaximized()
	
	
	show_hide_titlelist = arr_setting[0]
	show_hide_playlist = arr_setting[1]
		
	print(arr_setting)
	
	if show_hide_playlist == 1:
		ui.list2.show()
		#ui.goto_epn.show()
	elif show_hide_playlist == 0:
		ui.list2.hide()
		ui.goto_epn.hide()
			
	if show_hide_titlelist == 1:
		ui.list1.show()
		#ui.frame.show()
	elif show_hide_titlelist == 0:
		ui.list1.hide()
		ui.frame.hide()
	
	#MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
	#if layout_mode != 'Mini':
	MainWindow.show()
	
	
	if len(sys.argv) == 2:
		t = sys.argv[1]
		print (t)
		if ("file:///" in t or t.startswith('/')) and not t.endswith('.torrent') and not 'magnet:' in t:
			quitReally="no"
			print (t)
			#new_epn = t.split('/')[-1]
			new_epn = os.path.basename(t)
			t = '"'+t+'"'
			ui.epn_name_in_list = urllib.parse.unquote(new_epn)
			t = t.replace('file:///','/')
			ui.watchDirectly(urllib.parse.unquote(t),'','no')
			ui.dockWidget_3.hide()
			site = "None"
			ui.btn1.setCurrentIndex(0)
			
			path_Local_Dir,name = os.path.split(t)
			for r,d,f in os.walk(path_Local_Dir):
				for z in f:
					if '.mkv' in z or '.mp4' in z or '.avi' in z or '.mp3' in z or '.flv' in z or '.flac' in z:
						m.append(os.path.join(r,z))
			m=naturallysorted(m)
			#print m
			epnArrList[:]=[]
			j = 0
			row = 0
			t = t.replace('"','')
			t=urllib.parse.unquote(t)
			
			e = os.path.basename(e)
			
			for i in m:
				i1 = i
				#i = i.split('/')[-1]
				i = os.path.basename(i)
				epnArrList.append(i+'	'+i1)
				ui.list2.addItem((i))
				i = i
				if i == e:
					row = j
				j =j+1
			ui.list2.setCurrentRow(row)
			curR = row
		elif t.endswith('.torrent'):
			ui.torrent_type = 'file'
			video_local_stream = True
			site = 'None'
			t = t.replace('file:///','/')
			t=urllib.parse.unquote(t)
			#print(t)
			#t = os.getcwd()+'/'+t
			print(t)
			local_torrent_file_path = t
			info = lt.torrent_info(t)
			file_arr = []
			ui.list2.clear()
			epnArrList[:]=[]
			QtWidgets.QApplication.processEvents()
			for f in info.files():
				file_path = f.path
				print(file_path)
				#if '/' in f.path:
				#	file_path = file_path.split('/')[-1]
				file_path = os.path.basename(file_path)
				epnArrList.append(file_path+'	'+t)
				ui.list2.addItem((file_path))
		elif 'magnet:' in t:
			t = re.search('magnet:[^"]*',t).group()
			site = 'None'
			ui.torrent_type = 'magnet'
			video_local_stream = True
			ui.local_torrent_open(t)
		else:
			quitReally="yes"
			#new_epn = t.split('/')[-1]
			new_epn = os.path.basename(t)
			t = '"'+t+'"'
			ui.epn_name_in_list = urllib.parse.unquote(new_epn)
			#t = t.replace('file:///','/')
			site = 'None'
			ui.watchDirectly(urllib.parse.unquote(t),'','no')
			ui.dockWidget_3.hide()
	ui.quality_val = quality
	#x = tray.showMessage
	#x('hi','hello',1)
	ret = app.exec_()
	if ui.dockWidget_3.isHidden():
		dock_opt = 0
		
	else:
		dock_opt = 1
	
	def_val = ''
	for i in default_arr_setting:
		
		def_val = def_val + str(i) + ','
		#print(def_val)
	def_val = def_val[:-1]
	
	music_val = ''
	for i in music_arr_setting:
		music_val = music_val + str(i)+','
		#print(music_val)
	music_val = music_val[:-1]
	
	#print(MainWindow.pos().x(),MainWindow.pos().y(),'--pos--')
	#print(MainWindow.size(),'--size--')
	#app.deleteLater()
	if ui.float_window_open:
		ui.float_window_dim = [ui.float_window.pos().x(),ui.float_window.pos().y(),ui.float_window.width(),ui.float_window.height()]
	if ui.music_mode_dim_show:
		ui.music_mode_dim = [MainWindow.pos().x(),MainWindow.pos().y(),MainWindow.width(),MainWindow.height()]
	if ui.list1.isHidden():
		show_hide_titlelist = 0
	else:
		show_hide_titlelist = 1
	if ui.list2.isHidden():
		show_hide_playlist = 0
	else:
		show_hide_playlist = 1
	if os.path.exists(os.path.join(home,"config.txt")):
				
		print(Player)
		f = open(os.path.join(home,"config.txt"),"w")
		f.write("VERSION_NUMBER="+str(ui.version_number))
		f.write("\nDefaultPlayer="+Player)
		f.write("\nWindowFrame="+str(ui.window_frame))
		f.write("\nFloatWindow="+str(ui.float_window_dim))
		f.write("\nDockPos="+str(ui.orientation_dock))
		f.write("\nMusicWindowDim="+str(ui.music_mode_dim))
		f.write("\nMusicModeDimShow="+str(ui.music_mode_dim_show))
		if iconv_r_indicator:
			iconv_r = iconv_r_indicator[0]
		f.write("\nThumbnail_Size="+str(iconv_r))
		f.write("\nView="+str(viewMode))
		f.write("\nQuality="+str(quality))
		f.write("\nSite_Index="+str(ui.btn1.currentIndex()))
		f.write("\nAddon_Index="+str(ui.btnAddon.currentIndex()))
		f.write("\nOption_Index="+str(ui.list3.currentRow()))
		f.write("\nOption_Val="+str(opt))
		f.write("\nName_Index="+str(ui.list1.currentRow()))
		f.write("\nEpisode_Index="+str(ui.list2.currentRow()))
		f.write("\nShow_Hide_Cover="+str(show_hide_cover))
		f.write("\nShow_Hide_Playlist="+str(show_hide_playlist))
		f.write("\nShow_Hide_Titlelist="+str(show_hide_titlelist))
		f.write("\nShow_Hide_Player="+str(show_hide_player))
		f.write("\nDock_Option="+str(dock_opt))
		f.write("\nPOSX="+str(MainWindow.pos().x()))
		f.write("\nPOSY="+str(MainWindow.pos().y()))
		f.write("\nWHeight="+str(MainWindow.height()))
		f.write("\nWWidth="+str(MainWindow.width()))
		f.write("\nLayout="+str(layout_mode))
		f.write("\nDefault_Mode="+str(def_val))
		f.write("\nList_Mode_With_Thumbnail="+str(ui.list_with_thumbnail))
		f.write("\nMusic_Mode="+str(music_val))
		
		f.close()
	if mpvplayer.processId()>0:
		mpvplayer.kill()
	if os.path.exists(TMPDIR) and '.config' not in TMPDIR:
		shutil.rmtree(TMPDIR)
	print(ret,'--Return--')
	del app
	sys.exit(ret)
	
if __name__ == "__main__":
	main()
