import sys
import urllib
import urllib3
import pycurl
from io import StringIO,BytesIO
import re
import random
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup
import os.path
from subprocess import check_output
try:
	import libtorrent as lt
except:
	pass
from stream import ThreadServer,TorrentThread,get_torrent_info,get_torrent_info_magnet
from PyQt4 import QtGui
import shutil
#from hurry.filesize import size

def naturallysorted(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

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
		elif curl_opt == '-Ie':
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
	c.setopt(c.URL, url)
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

def replace_all(text, di):
	for i, j in di.iteritems():
		text = text.replace(i, j)
	return text





class Torrent():
	def __init__(self):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
	def getOptions(self):
			criteria = ['Open','History','LocalStreaming']
			return criteria
		
	def getFinalUrl(self,name,epn,local_ip,status,path_folder,session,ui):
		
		index = int(epn)
		ip_n = local_ip.rsplit(':',1)
		ip = ip_n[0]
		port = int(ip_n[1])
		if status.lower() =='first run':
			thread_server = ThreadServer(ip,port)
			thread_server.start()
			#ses = set_torrent_session()
		path = path_folder
		
		home = os.path.expanduser('~')+'/.config/AnimeWatch/History/Torrent/'
		torrent_dest = home+name+'.torrent'
		print(torrent_dest,index,path)
		
		
		handle,ses,info,cnt,cnt_limit,file_name = get_torrent_info(torrent_dest,index,path,session,ui)
		torrent_thread = TorrentThread(handle,cnt,cnt_limit,ses)
		torrent_thread.start()
		
		
		url = 'http://'+ip+':'+str(port)+'/'
		print(url,'-local-ip-url')
		if status.lower() == 'first run':
			return url,thread_server,torrent_thread,ses,handle
		else:
			return url,torrent_thread,ses,handle
		
		
	def search(self,name):
		m = ['Not Available']
		return m
		
	def getCompleteList(self,opt,ui):
		m = ['Not Able To Open']
		if opt == 'Open':
			MainWindow = QtGui.QWidget()
			item, ok = QtGui.QInputDialog.getText(MainWindow, 'Input Dialog', 'Enter Torrent Url or Magnet Link or local torrent file path')
			if ok and item:
				if (item.startswith('http') or item.startswith('/')) and item.endswith('.torrent'):
					home = os.path.expanduser('~')+'/.config/AnimeWatch/History/Torrent/'
					name1 = item.split('/')[-1].replace('.torrent','')
					torrent_dest1 = '/tmp/AnimeWatch/'+name1+'.torrent'
					if not os.path.exists(torrent_dest1):
						if item.startswith('http'):
							ccurl(item+'#'+'-o'+'#'+torrent_dest1)
						else:
							shutil.copy(item,torrent_dest1)
					if os.path.exists(torrent_dest1):
						info = lt.torrent_info(torrent_dest1)
						name = info.name()
						torrent_dest = home+name+'.torrent'
						shutil.copy(torrent_dest1,torrent_dest)
					m = [name]
				elif item.startswith('magnet:'):
					
					torrent_handle,stream_session,info = get_torrent_info_magnet(item,'/tmp/AnimeWatch',ui)
					torrent_file = lt.create_torrent(info)
					
					home = os.path.expanduser('~')+'/.config/AnimeWatch/History/Torrent/'
					name = info.name()
					torrent_dest = home+name+'.torrent'
					
					with open(torrent_dest, "wb") as f:
						f.write(lt.bencode(torrent_file.generate()))
						
					torrent_handle.pause()
					stream_session.pause()
					m = [name]
		return m
	
	def getEpnList(self,name,opt):
		summary = ""
		home = os.path.expanduser('~')+'/.config/AnimeWatch/History/Torrent/'
		torrent_dest = home+name+'.torrent'
		info = lt.torrent_info(torrent_dest)
		file_arr = []
		for f in info.files():
			file_path = f.path
			if '/' in f.path:
				file_path = file_path.split('/')[-1]
				
			file_arr.append(file_path)
		
		file_arr.append('No.jpg')
		file_arr.append('Not Available')
		return file_arr

	def getNextPage(self,opt,pgn,genre_num,name):
		m = ['Nothing']
		return m
