"""
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




import libtorrent as lt
import time
import sys
from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import pyqtSlot,pyqtSignal,QObject
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import os

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
	
	
		
	def do_GET(self):
		global handle,ses,info,cnt,cnt_limit,file_name,torrent_download_path
		print(handle,ses,info)
		if os.path.exists('/tmp/AnimeWatch/row.txt'):
			content = open('/tmp/AnimeWatch/row.txt').read()
			try:
				fileIndex = int(content)
				i = 0
				for f in info.files():
					if fileIndex == i:
						fileStr = f
						handle.file_priority(i,7)
					
					i += 1
				try:
					print (fileStr.path)
				except:
					return 0
				
				pr = info.map_file(fileIndex,0,fileStr.size)
				print(pr.length,info.piece_length(),info.num_pieces())
				n_pieces = pr.length / info.piece_length() + 1 
				print(n_pieces)
				n_pieces = int(n_pieces)
				for i in range(info.num_pieces()):
					if i in range(pr.piece,pr.piece+n_pieces):
						if i == pr.piece:
							handle.piece_priority(i,7)
						elif i == pr.piece+1:
							handle.piece_priority(i,7)
						elif i == pr.piece+2:
							handle.piece_priority(i,1)
						elif i == pr.piece+n_pieces-1:
							handle.piece_priority(i,7)
						else:
							handle.piece_priority(i,1)
				tmp = ''
				for i in range(info.num_pieces()):
					tmp = tmp+':'+str(handle.piece_priority(i))
				print(tmp)
				print ('starting', handle.name())
				handle.set_sequential_download(True)

				cnt = pr.piece
				cnt_limit = pr.piece+n_pieces
				cnt1 = cnt
				file_name = torrent_download_path +'/'+ fileStr.path
			except:
				pass
		self.send_response(200)
		if file_name.endswith('.mkv'):
			self.send_header('Content-type','video/x-matroska')
		else:
			self.send_header('Content-type','video/mp4')
			
		self.end_headers()
		
		length = info.piece_length()
		if not os.path.exists(file_name):
			if '/' in file_name:
				dir_name = file_name.rsplit('/',1)[0]
				if not os.path.exists(dir_name):
					os.makedirs(dir_name)
			f = open(file_name,'wb')
			f.close()
		
		
		
		f = open(file_name,'rb')
		i = cnt
		total = 0
		
		print(file_name,i,cnt,cnt_limit,'---file--download---path--')
		
		while i < cnt_limit:
			if handle.have_piece(i) and handle.have_piece(i+1):
				#print('--reading---')
				content = f.read(2*length)
				try:
					self.wfile.write(content)
				except:
					break
				i = i+2
				total = total + 2*length
			else:
				if total > 2*length:
					print(i,'--get--')
					handle.piece_priority(i,7)
					handle.piece_priority(i+1,7)
				time.sleep(2)
				if ses.is_paused() or os.path.exists('/tmp/AnimeWatch/player_stop.txt'):
					break
		
		
		f.close()
		if os.path.exists('/tmp/AnimeWatch/player_stop.txt'):
			os.remove('/tmp/AnimeWatch/player_stop.txt')
		if os.path.exists('/tmp/AnimeWatch/row.txt'):
			os.remove('/tmp/AnimeWatch/row.txt')
		return 0
		
	
		
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass

class ThreadServer(QtCore.QThread):
	
	def __init__(self,ip,port):
		global thread_signal
		QtCore.QThread.__init__(self)
		self.ip = ip
		self.port = int(port)
	def __del__(self):
		self.wait()                        
	
	def run(self):
		print('starting server...')
		server_address = (self.ip,self.port)
		httpd = ThreadedHTTPServer(server_address, testHTTPServer_RequestHandler)
		print('running server...at..'+self.ip+':'+str(self.port))
		httpd.serve_forever()
		

class TorrentThread(QtCore.QThread):
	session_signal = pyqtSignal(str)
	def __init__(self,v1,v2,v3,v4):
		QtCore.QThread.__init__(self)
		self.handle = v1
		self.cnt = v2
		self.cnt_limit = v3
		self.session = v4
		self.session_signal.connect(session_finished)
	def __del__(self):
		self.wait()                        
	
	def run(self):
		global ui,new_cnt,new_cnt_limit
		cnt1 = self.cnt
		cnt_limit = self.cnt_limit
		s = self.handle.status()
		while (not self.session.is_paused()):
			#print(self.session.is_paused())
			s = self.handle.status()
			
			state_str = ['queued', 'checking', 'downloading metadata', \
				'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
			print ('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % \
				(s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
				s.num_peers, state_str[s.state]),)
			sys.stdout.flush()
			
			#print(h.have_piece(cnt))
			if cnt1+3 < cnt_limit:
				if self.handle.have_piece(cnt1) and self.handle.have_piece(cnt1+1):
					print(cnt1,cnt1+1,7,'--cnt--downloaded--')
					self.handle.piece_priority(cnt1+2,7)
					self.handle.piece_priority(cnt1+3,7)
					cnt1 = cnt1+4
			
			if (s.progress * 100)>=99:
				self.session_signal.emit('..Starting Next Download..')
				#self.session.pause()
				time.sleep(5)
			
			if self.handle.is_seed():
				print('Download Complete, Entering into seeding mode')
				break
			time.sleep(1)
			

		print (self.handle.name(), 'complete')
		#self.session_signal.emit('..Finished..')
		
@pyqtSlot(str)
def session_finished(var):
	#from animeWatch import ui
	global ui,handle,info,ses,new_cnt,new_cnt_limit
	print(var,'--session-finished--')
	#print(ui.local_file_index)
	
	if ui.count() > 0:
		
		item = ui.item(0)
		if item:
			txt = item.text()
			if txt.startswith('Queue Empty:'):
				return 0
			ui.takeItem(0)
			del item
			indx = txt.split(':')[-1]
			fileIndex = int(indx)
			i = 0
			s = handle.status()
			if (s.progress *100) >= 100:
				handle.force_recheck()
				print('--force--rechecking--')
			for f in info.files():
				if fileIndex == i:
					fileStr = f
					handle.file_priority(i,7)
				
				i += 1
			try:
				print (fileStr.path)
			except:
				return 0
			
			
			pr = info.map_file(fileIndex,0,fileStr.size)
			print(pr.length,info.piece_length(),info.num_pieces())
			n_pieces = pr.length / info.piece_length() + 1 
			print(n_pieces)
			n_pieces = int(n_pieces)
			for i in range(info.num_pieces()):
				if i in range(pr.piece,pr.piece+n_pieces):
					if i == pr.piece:
						handle.piece_priority(i,7)
					elif i == pr.piece+1:
						handle.piece_priority(i,7)
					elif i == pr.piece+2:
						handle.piece_priority(i,1)
					elif i == pr.piece+n_pieces-1:
						handle.piece_priority(i,7)
					else:
						handle.piece_priority(i,1)
			tmp = ''
			for i in range(info.num_pieces()):
				tmp = tmp+':'+str(handle.piece_priority(i))
			print(tmp)
			print ('starting', handle.name())
			handle.set_sequential_download(True)

			new_cnt = pr.piece
			new_cnt_limit = pr.piece+n_pieces
			cnt1 = cnt
			
			
			g = fileStr.path
			if '/' in g:
				print(g.split('/')[-1])
			else:
				print(g)
			
	
def set_torrent_info(v1,v2,v3,session):
	global handle,ses,info,cnt,cnt_limit,file_name
	i=0
	handle = v1
	fileIndex = int(v2)
	path = v3
	ses = session
	info = handle.get_torrent_info()
	for f in info.files():
		if fileIndex == i:
			fileStr = f
			handle.file_priority(i,7)
		else:
			handle.file_priority(i,0)
		i += 1
		
	print (fileStr.path)
	file_name = path+'/'+fileStr.path
	file_arr =[]
	for f in info.files():
		file_arr.append(f.path)
		i += 1


	for i in file_arr:
		print(i)

	

	pr = info.map_file(fileIndex,0,fileStr.size)
	print(pr.length,info.piece_length(),info.num_pieces())
	n_pieces = pr.length / info.piece_length() + 1 
	print(n_pieces)
	n_pieces = int(n_pieces)
	for i in range(info.num_pieces()):
		if i in range(pr.piece,pr.piece+n_pieces):
			if i == pr.piece:
				handle.piece_priority(i,7)
			elif i == pr.piece+1:
				handle.piece_priority(i,7)
			elif i == pr.piece+2:
				handle.piece_priority(i,1)
			elif i == pr.piece+n_pieces-1:
				handle.piece_priority(i,7)
			else:
				handle.piece_priority(i,1)
		else:
			#if not handle.have_piece(i):
			handle.piece_priority(i,0)


	print ('starting', handle.name())
	handle.set_sequential_download(True)

	cnt = pr.piece
	cnt_limit = pr.piece+n_pieces
	cnt1 = cnt
	if ses.is_paused():
		ses.resume()
	handle.resume()
	return cnt,cnt_limit
		
def get_torrent_info_magnet(v1,v3):
	global handle,ses,info,cnt,cnt_limit,file_name
	#print(v1,'------------hello----------info---')
	sett = lt.session_settings()
	sett.user_agent = 'qBittorrent v3.3.5'
	sett.always_send_user_agent = True
	fingerprint = lt.fingerprint('qB',3,3,5,0)
	ses = lt.session(fingerprint)

	ses.listen_on(40000, 50000)
	ses.set_settings(sett)
	
	
	handle = lt.add_magnet_uri(ses,v1,{'save_path':v3})
	i = 0
	while (not handle.has_metadata()):
		time.sleep(1)
		i = i+1
		print('finding metadata')
		if i > 300:
			print('No Metadata Available')
			break
	info = handle.get_torrent_info()

	handle.set_sequential_download(True)
	print(handle.trackers())
	
	return handle,ses,info

def get_torrent_info(v1,v2,v3,session,u):
	global handle,ses,info,cnt,cnt_limit,file_name,ui,torrent_download_path
	ui = u
	if not session:
		sett = lt.session_settings()
		sett.user_agent = 'qBittorrent v3.3.5'
		sett.always_send_user_agent = True
		fingerprint = lt.fingerprint('qB',3,3,5,0)
		ses = lt.session(fingerprint)

		ses.listen_on(40000, 50000)
		ses.set_settings(sett)
	else:
		ses = session
	#print(ses.get_settings())
	
	
	if v1.startswith('magnet:'):
		handle = lt.add_magnet_uri(ses,v1,{'save_path':v3})
		i = 0
		while (not handle.has_metadata()):
			time.sleep(1)
			i = i+1
			if i > 60:
				print('No Metadata Available')
				break
		info = handle.get_torrent_info()
	else:
		info = lt.torrent_info(v1)
		#print(info)

		#sett = ses.get_settings()
		#print(sett)
		#print(sett['user_agent'],sett['upload_rate_limit'])
		
		handle = ses.add_torrent({'ti': info, 'save_path': v3})

	handle.set_sequential_download(True)
	print(handle.trackers())
	
	
	i=0
	fileIndex = int(v2)
	for f in info.files():
		if fileIndex == i:
			fileStr = f
			handle.file_priority(i,7)
		else:
			handle.file_priority(i,0)
		i += 1
	
	print (fileStr.path)
	file_name = v3+'/'+fileStr.path
	torrent_download_path = v3
	file_arr =[]
	for f in info.files():
		file_arr.append(f.path)
		i += 1


	for i in file_arr:
		print(i)

	
	content_length = fileStr.size
	print(content_length,'content-length')
	pr = info.map_file(fileIndex,0,fileStr.size)
	print(pr.length,info.piece_length(),info.num_pieces())
	n_pieces = pr.length / info.piece_length() + 1 
	print(n_pieces)
	n_pieces = int(n_pieces)
	for i in range(info.num_pieces()):
		if i in range(pr.piece,pr.piece+n_pieces):
			if i == pr.piece:
				handle.piece_priority(i,7)
			elif i == pr.piece+1:
				handle.piece_priority(i,7)
			elif i == pr.piece+2:
				handle.piece_priority(i,1)
			elif i == pr.piece+n_pieces-1:
				handle.piece_priority(i,7)
			else:
				handle.piece_priority(i,1)
		else:
			handle.piece_priority(i,0)

	
	print ('starting', handle.name())
	handle.set_sequential_download(True)

	cnt = pr.piece
	cnt_limit = pr.piece+n_pieces
	cnt1 = cnt
	
	print('\n',cnt,cnt_limit,file_name,'---get--torrent--info\n')

	
	if ses.is_paused():
		ses.resume()
	handle.resume()
	
	return handle,ses,info,cnt,cnt_limit,file_name

