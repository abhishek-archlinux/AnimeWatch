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




import libtorrent as lt
import time
import sys
from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import pyqtSlot,pyqtSignal,QObject
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import os
import subprocess,re
from player_functions import send_notification
import select
import base64
import ssl

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
	
	protocol_version = 'HTTP/1.1'
	
	def do_HEAD(self):
		global handle,ses,info,cnt,cnt_limit,file_name,torrent_download_path
		global tmp_dir_folder,content_length
		#print(handle,ses,info)
		print('--head--',content_length)
		self.send_response(200)
		self.send_header('Content-type','video/mp4')
		self.send_header('Content-Length', str(content_length))
		self.send_header('Accept-Ranges', 'bytes')
		self.send_header('Connection', 'close')
		self.end_headers()
	
	def get_the_content(self,get_bytes):
		global handle,ses,info,cnt,cnt_limit,file_name,torrent_download_path
		global tmp_dir_folder,httpd,media_server_key,client_auth_arr
		
		tmp_file = os.path.join(tmp_dir_folder,'row.txt')
		tmp_seek_file = os.path.join(tmp_dir_folder,'seek.txt')
		tmp_pl_file = os.path.join(tmp_dir_folder,'player_stop.txt')
		
		if os.path.exists(tmp_file):
			content = open(tmp_file).read()
			try:
				fileIndex = int(content)
				i = 0
				for f in info.files():
					if fileIndex == i:
						fileStr = f
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
				tmp = ''
				for i in range(info.num_pieces()):
					tmp = tmp+':'+str(handle.piece_priority(i))
				print(tmp)
				print ('starting', handle.name())
				#handle.set_sequential_download(True)
				cnt = pr.piece
				cnt_limit = pr.piece+n_pieces
				cnt1 = cnt
				file_name = os.path.join(torrent_download_path,fileStr.path)
			except Exception as e:
				print(e)
		
		length = info.piece_length()
		complete_file = False
		if not os.path.exists(file_name):
			dir_name,sub_file = os.path.split(file_name)
			if not os.path.exists(dir_name):
				os.makedirs(dir_name)
			f = open(file_name,'wb')
			f.close()
		else:
			if (os.path.exists(file_name) and 
					os.stat(file_name).st_size == content_length):
				complete_file = True
				
		self.send_response(200)
		self.send_header('Content-type','video/mp4')
		self.send_header('Content-Length', str(content_length))
		self.send_header('Accept-Ranges', 'bytes')
		size_field = 'bytes {0}-{1}/{1}'.format(str(get_bytes),str(content_length))
		self.send_header('Content-Range', size_field)
		self.send_header('Connection', 'close')
		self.end_headers()
		
		f = open(file_name,'rb')
		if get_bytes:
			new_piece = int(get_bytes/length)+1
			print(new_piece,get_bytes,length)
			i = cnt+new_piece
			if i > cnt_limit -3:
				i = cnt
			print(new_piece,'--new_piece--',i,get_bytes,content_length)
		else:
			i = cnt
		total = 0
		
		print(file_name,i,cnt,cnt_limit,'---file--download---path--')
		t = 0
		content = 0
		pri_lowered = False
		cnt_arr = []
		for l in range(10):
			cnt_arr.append(i+l)
			if l == 0:
				handle.piece_priority(l,7)
			else:
				handle.piece_priority(l,6)
		tm = 0
		with open(file_name,'rb') as f:
			content = b'0'
			while content:
				try:
					if handle.have_piece(i):
						if get_bytes:
							f.seek(get_bytes)
							get_bytes = 0
						content = f.read(length)
						try:
							self.wfile.write(content)
						except Exception as e:
							print(e)
							break
						i = i+1
						print(i,'=i piece')
						handle.piece_priority(i,7)
					else:
						time.sleep(1)
						d = 0
						for l in cnt_arr:
							if handle.have_piece(l):
								d = d+1
						if d >= 5:
							o = cnt_arr[-1]
							cnt_arr[:]=[]
							for l in range(10):
								if i+l < cnt_limit:
									cnt_arr.append(i+l)
									handle.piece_priority(i+l,6)
							print(cnt_arr)
						#print("seeking i={0},cnt={1},get_bytes={2},
						#pri_lowered={3}".format(i,cnt,get_bytes,pri_lowered))
						handle.piece_priority(i,7)
						#print(cnt_arr)
						if get_bytes and not pri_lowered:
							k = cnt
							while k < i:
								handle.piece_priority(k,1)
								print(k,' lowered')
								k = k+1
							pri_lowered = True
					if ses.is_paused() or os.path.exists(tmp_pl_file):
						break
				except Exception as e:
					print(e)
					break
		if os.path.exists(tmp_pl_file):
			os.remove(tmp_pl_file)
		if os.path.exists(tmp_file):
			os.remove(tmp_file)
			
	def do_GET(self):
		global handle,ses,info,cnt,cnt_limit,file_name,torrent_download_path
		global tmp_dir_folder,httpd,media_server_key,client_auth_arr
		#data = self.request.recv(1024).strip()
		#print(data,'--requests--')
		#print(handle,ses,info)
		print('do_get')
		print(self.headers)
		try:
			get_bytes = int(self.headers['Range'].split('=')[1].replace('-',''))
		except Exception as e:
			get_bytes = 0
		print(get_bytes,'--get--bytes--')
		
		if media_server_key:
			key_en = base64.b64encode(bytes(media_server_key,'utf-8'))
			key = (str(key_en).replace("b'",'',1))[:-1]
			new_key = 'Basic '+key
			cli_key = self.headers['Authorization'] 
			print(cli_key,new_key)
			client_addr = str(self.client_address[0])
			print(client_addr,'--cli--')
			print(client_auth_arr,'--auth--')
			if not cli_key and (not client_addr in client_auth_arr):
				print('authenticating...')
				txt = 'Nothing'
				print ("send header")
				self.send_response(401)
				self.send_header('WWW-Authenticate', 'Basic realm="Auth"')
				self.send_header('Content-type', 'text/html')
				self.send_header('Content-Length', len(txt))
				self.end_headers()
				try:
					self.wfile.write(b'Nothing')
				except Exception as e:
					print(e)
			elif (cli_key == new_key) or (client_addr in client_auth_arr):
				self.get_the_content(get_bytes)
			else:
				self.send_header('Content-type','text/html')
				txt = b'You are not authorized to access the content'
				self.send_header('Content-Length', len(txt))
				self.send_header('Connection', 'close')
				self.end_headers()
				try:
					self.wfile.write(txt)
				except Exception as e:
					print(e)
		else:
			self.get_the_content(get_bytes)
		
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	pass
	
class ThreadServer(QtCore.QThread):
	
	def __init__(self,ip,port,key=None,client_arr=None,https_conn=None,cert_file=None):
		global thread_signal,media_server_key,client_auth_arr
		QtCore.QThread.__init__(self)
		self.ip = ip
		self.port = int(port)
		media_server_key = key
		client_auth_arr = client_arr
		self.https_allow = https_conn
		self.cert_file = cert_file
		
	def __del__(self):
		self.wait()                        
	
	def run(self):
		global httpd
		print('starting server...')
		server_address = (self.ip,self.port)
		try:
			httpd = ThreadedHTTPServer(server_address, testHTTPServer_RequestHandler)
			if self.https_allow and self.cert_file:
				if os.path.exists(self.cert_file):
					httpd.socket = ssl.wrap_socket(
						httpd.socket,certfile=self.cert_file,
						ssl_version=ssl.PROTOCOL_TLSv1_1)
		except:
			txt = 'Your local IP changed..or port is blocked\n..Trying to find new IP'
			#subprocess.Popen(['notify-send',txt])
			send_notification(txt)
			self.ip = get_ip()
			txt = 'Your New Address is '+self.ip + '\n Please restart the player'
			#subprocess.Popen(['notify-send',txt])
			send_notification(txt)
			change_config_file(self.ip,self.port)
			server_address = (self.ip,self.port)
			httpd = ThreadedHTTPServer(server_address, testHTTPServer_RequestHandler)
		print('running server...at..'+self.ip+':'+str(self.port))
		httpd.serve_forever()

class TorrentThread(QtCore.QThread):
	session_signal = pyqtSignal(str)
	progress_signal = pyqtSignal(str,int)
	progress_signal_end = pyqtSignal(str)
	def __init__(self,v1,v2,v3,v4,row=None,from_client=None):
		QtCore.QThread.__init__(self)
		self.handle = v1
		self.cnt = v2
		self.cnt_limit = v3
		self.session = v4
		if row:
			self.current_index = row
		else:
			self.current_index = 0
		self.from_client = from_client
		self.start_next = False
		self.session_signal.connect(session_finished)
		self.progress_signal.connect(print_progress)
		self.progress_signal_end.connect(print_progress_complete)
	def __del__(self):
		self.wait()                        
	
	def process_next(self):
		global handle,info,ses,new_cnt,new_cnt_limit,total_size_content
		global torrent_download_path
		self.current_index = self.current_index + 1
		fileIndex = int(self.current_index)
		i = 0
		fileStr = None
		file_exists = False
		for f in info.files():
			if fileIndex == i:
				fileStr = f
				handle.file_priority(i,7)
			i += 1
		try:
			new_path = os.path.join(torrent_download_path,fileStr.path)
			new_size = fileStr.size
			if os.path.exists(new_path) and os.stat(new_path).st_size == new_size:
				file_exists = True
		except Exception as err_val:
			print(err_val,'--312--stream.py--')
			file_exists = True
		if fileStr and not file_exists:
			s = self.handle.status()
			if (s.progress *100) >= 100:
				handle.force_recheck()
				print('--force--rechecking--')
			print (fileStr.path)
			total_size_content = str(int(fileStr.size/(1024*1024)))+'M'
			pr = info.map_file(fileIndex,0,fileStr.size)
			print(pr.length,info.piece_length(),info.num_pieces())
			n_pieces = pr.length / info.piece_length() + 1 
			print(n_pieces)
			n_pieces = int(n_pieces)
			for i in range(info.num_pieces()):
				if i in range(pr.piece,pr.piece+n_pieces):
					if i in range(pr.piece,pr.piece+10):
						if i == pr.piece:
							handle.piece_priority(i,7)
						else:
							handle.piece_priority(i,6)
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
			self.start_next = False
			
	def run(self):
		global new_cnt,new_cnt_limit,total_size_content
		cnt1 = self.cnt
		cnt_limit = self.cnt_limit
		s = self.handle.status()
		
		while (not self.session.is_paused()):
			#print(self.session.is_paused())
			s = self.handle.status()
			#print('hello',s)
			state_str = ['queued', 'checking', 'downloading metadata',
						'DOWNLOADING', 'finished', 'seeding', 'allocating', 
						'checking fastresume']
			#print ('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % \
			#	(s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
			#	s.num_peers, state_str[s.state]),)
			#sys.stdout.flush()
			if not self.handle.is_seed():
				out = str(int(s.progress*100))+'%'
			else:
				out = 'SEEDING'
			out_percent = int(s.progress*100)
			
			#print(out)
			TD = str(int(s.total_download/(1024*1024)))+'M'
			TU = str(int(s.total_upload/(1024*1024)))+'M'
			TDR = u'\u2193'+str(int(s.download_rate/1024)) + 'K' + '('+TD+')'
			TUR = u'\u2191'+str(int(s.upload_rate/1024)) + 'K'+'('+TU+')'
			#TD_ALL = str(int(s.all_time_download/(1024*1024)))+'M'
			out1 = str(out)+' '+total_size_content+' '+TDR +' '+TUR+' '+'P:'+str(s.num_peers)
			if s.state == 1:
				out1 = 'Checking Please Wait: '+str(out)
			self.progress_signal.emit(out1,out_percent)
			if self.from_client:
				print(out1,out_percent,'from_client=',self.from_client,'start_next=',self.start_next)
			#print(h.have_piece(cnt))
			if cnt1+3 < cnt_limit:
				if self.handle.have_piece(cnt1) and self.handle.have_piece(cnt1+1):
					#print(cnt1,cnt1+1,7,'--cnt--downloaded--')
					self.handle.piece_priority(cnt1+2,7)
					self.handle.piece_priority(cnt1+3,7)
					cnt1 = cnt1+4
			
			if (s.progress * 100)>=99 and (s.state != 1):
				if self.from_client:
					print(self.start_next)
					if not self.start_next:
						self.start_next = True
						self.process_next()
					print(self.start_next)
				else:
					self.session_signal.emit('..Starting Next Download..')
					time.sleep(5)
			
			if self.handle.is_seed():
				print('Download Complete, Entered into seeding mode')
				#break
			time.sleep(1)
			
		
		print (self.handle.name(), 'complete')
		self.progress_signal_end.emit('complete')
		#progress.setValue(100)
		#progress.hide()
		#self.session_signal.emit('..Finished..')
		
def change_config_file(ip,port):
	config_file = os.path.join(
			os.path.expanduser('~'),'.config','AnimeWatch',
			'torrent_config.txt')
	new_ip = 'TORRENT_STREAM_IP='+ip+':'+str(port)
	content = open(config_file,'r').read()
	content = re.sub('TORRENT_STREAM_IP=[^\n]*',new_ip,content)
	f = open(config_file,'w')
	f.write(content)
	f.close()
	
def get_ip():
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

@pyqtSlot(str)
def print_progress_complete(var_str):
	global progress,ses
	progress.setValue(100)
	progress.hide()

@pyqtSlot(str,int)
def print_progress(var_str,var_int):
	global progress
	progress.setValue(var_int)		
	progress.setFormat(var_str)
	#if progress.isHidden():
	#	progress.show()
		
@pyqtSlot(str)
def session_finished(var):
	global ui,handle,info,ses,new_cnt,new_cnt_limit,total_size_content
	print(var,'--session-finished--')
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
				total_size_content = str(int(fileStr.size/(1024*1024)))+'M'
			except:
				return 0
			pr = info.map_file(fileIndex,0,fileStr.size)
			print(pr.length,info.piece_length(),info.num_pieces())
			n_pieces = pr.length / info.piece_length() + 1 
			print(n_pieces)
			n_pieces = int(n_pieces)
			for i in range(info.num_pieces()):
				if i in range(pr.piece,pr.piece+n_pieces):
					if i in range(pr.piece,pr.piece+10):
						if i == pr.piece:
							handle.piece_priority(i,7)
						else:
							handle.piece_priority(i,6)
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
			g = os.path.basename(g)
	
def set_torrent_info(v1,v2,v3,session,u,p_bar,tmp_dir,key=None,client_arr=None):
	global handle,ses,info,cnt,cnt_limit,file_name,ui,progress,tmp_dir_folder
	global media_server_key,client_auth_arr
	media_server_key = key
	client_auth_arr = client_arr
	
	progress = p_bar
	tmp_dir_folder = tmp_dir
	progress.setValue(0)
	progress.show()
	ui = u
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
			new_path = os.path.join(v3,f.path)
			new_size = f.size
			if os.path.exists(new_path) and os.stat(new_path).st_size == new_size:
				handle.file_priority(i,1)
			else:
				handle.file_priority(i,0)
		i = i+1
		
	print (fileStr.path)
	file_name = os.path.join(path,fileStr.path)
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
			if i in range(pr.piece,pr.piece+10):
				if i == pr.piece:
					handle.piece_priority(i,7)
				else:
					handle.piece_priority(i,6)
			elif i == pr.piece+n_pieces-1:
				handle.piece_priority(i,7)
			else:
				handle.piece_priority(i,1)

	print ('starting', handle.name())
	handle.set_sequential_download(True)

	tmp = ''
	for i in range(info.num_pieces()):
		tmp = tmp+':'+str(handle.piece_priority(i))
	print(tmp)
	
	cnt = pr.piece
	cnt_limit = pr.piece+n_pieces
	cnt1 = cnt
	if ses.is_paused():
		ses.resume()
	handle.resume()
	return cnt,cnt_limit
		
def get_torrent_info_magnet(v1,v3,u,p_bar,tmp_dir):
	global handle,ses,info,cnt,cnt_limit,file_name,ui,progress,tmp_dir_folder
	ui = u
	progress = p_bar
	tmp_dir_folder = tmp_dir
	progress.setValue(0)
	progress.show()
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

def set_new_torrent_file_limit(
				v1,v2,v3,session,u,p_bar,tmp_dir,key=None,client_arr=None):
	global handle,ses,info,cnt,cnt_limit,file_name,ui,torrent_download_path
	global progress,tmp_dir_folder,content_length
	global media_server_key,client_auth_arr
	media_server_key = key
	client_auth_arr = client_arr
	content_length = 0
	ui = u
	progress = p_bar
	tmp_dir_folder = tmp_dir
	
	torr_arr = ses.get_torrents()
	for i in torr_arr:
		print(i.name())
	
	i=0
	fileIndex = int(v2)
	
	for f in info.files():
		if fileIndex == i:
			fileStr = f
		else:
			new_path = os.path.join(v3,f.path)
			new_size = f.size
		i = i+1
	
	print (fileStr.path)
	file_name = os.path.join(v3,fileStr.path)
	torrent_download_path = v3
	file_arr =[]
	for f in info.files():
		file_arr.append(f.path)
		i += 1

	for i in file_arr:
		print(i)
	
	content_length = fileStr.size
	pr = info.map_file(fileIndex,0,fileStr.size)
	print(pr.length,info.piece_length(),info.num_pieces())
	n_pieces = pr.length / info.piece_length() + 1 
	print(n_pieces)
	n_pieces = int(n_pieces)

	cnt = pr.piece
	cnt_limit = pr.piece+n_pieces
	cnt1 = cnt
	
	print('\n',cnt,cnt_limit,file_name,'---get--torrent--info\n')
	
	
def get_torrent_info(v1,v2,v3,session,u,p_bar,tmp_dir,key=None,client=None):
	global handle,ses,info,cnt,cnt_limit,file_name,ui,torrent_download_path
	global progress,total_size_content,tmp_dir_folder,content_length
	global media_server_key,client_auth_arr
	media_server_key = key
	client_auth_arr = client
	content_length = 0
	ui = u
	progress = p_bar
	tmp_dir_folder = tmp_dir
	progress.setValue(0)
	progress.show()
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
	
	print(ses.get_torrents(),'torrents_list')
	torr_arr = ses.get_torrents()
	for i in torr_arr:
		print(i.name())
	
	i=0
	fileIndex = int(v2)
	file_found = False
	for f in info.files():
		file_exists = False
		new_path = os.path.join(v3,f.path)
		new_size = f.size
		if os.path.exists(new_path) and os.stat(new_path).st_size == new_size:
			file_exists = True
		if fileIndex == i:
			fileStr = f
			handle.file_priority(i,7)
			if file_exists:
				file_found = True
		else:
			if file_exists:
				handle.file_priority(i,1)
			else:
				handle.file_priority(i,0)
		i = i+1
	
	print (fileStr.path)
	file_name = os.path.join(v3,fileStr.path)
	torrent_download_path = v3
	file_arr =[]
	for f in info.files():
		file_arr.append(f.path)
		i += 1

	for i in file_arr:
		print(i)
		
	content_length = fileStr.size
	print(content_length,'content-length')
	total_size_content = str(int(content_length/(1024*1024)))+'M'
	
	pr = info.map_file(fileIndex,0,fileStr.size)
	print(pr.length,info.piece_length(),info.num_pieces())
	n_pieces = pr.length / info.piece_length() + 1 
	print(n_pieces)
	n_pieces = int(n_pieces)
	for i in range(info.num_pieces()):
		if i in range(pr.piece,pr.piece+n_pieces):
			if i in range(pr.piece,pr.piece+10):
				if i == pr.piece:
					handle.piece_priority(i,7)
				else:
					handle.piece_priority(i,6)
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
	
	print('\n',cnt,cnt_limit,file_name,'---get--torrent--info\n')
	
	if ses.is_paused():
		ses.resume()
	handle.resume()
	
	return handle,ses,info,cnt,cnt_limit,file_name

