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
from stream import ThreadServer,TorrentThread,get_torrent_info
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





class Nyaa():
	def __init__(self):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
	def getOptions(self):
			criteria = ['Date','Seeders','Leechers','Downloads','History','LocalStreaming']
			return criteria
		
	def getFinalUrl(self,name,epn,local_ip,status,path_folder,session):
		nm = name.rsplit('-',1)
		name = nm[0]
		name_id = nm[1]
		index = int(epn)
		ip_n = local_ip.rsplit(':',1)
		ip = ip_n[0]
		port = int(ip_n[1])
		if status.lower() =='first run':
			thread_server = ThreadServer(ip,port)
			thread_server.start()
			#ses = set_torrent_session()
		path = path_folder
		
		home = os.path.expanduser('~')+'/.config/AnimeWatch/History/Nyaa/'
		torrent_dest = home+name+'.torrent'
		#home1 = os.path.expanduser('~')+'/.config/AnimeWatch/src/Plugins/stream.py'
		print(torrent_dest,index,path)
		
		#handle,ses,info,cnt,cnt_limit,file_name = get_torrent_info(torrent_dest,index,path)
		#print(get_torrent_info(torrent_dest,index,path))
		#print('---before--error---164---')
		handle,ses,info,cnt,cnt_limit,file_name = get_torrent_info(torrent_dest,index,path,session)
		#print('---line--error---166---')
		torrent_thread = TorrentThread(handle,cnt,cnt_limit,ses)
		torrent_thread.start()
		
		#p = subprocess.Popen(['python',home1,ip,str(port),torrent_dest,str(index),path])
		
		url = 'http://'+ip+':'+str(port)+'/'
		print(url,'-local-ip-url')
		if status.lower() == 'first run':
			return url,thread_server,torrent_thread,ses,handle
		else:
			return url,torrent_thread,ses,handle
		
	def process_page(self,url):
		content = ccurl(url)
		soup = BeautifulSoup(content,'lxml')
		#print(soup.prettify())
		unit_element = soup.findAll('tr',{'class':'trusted tlistrow'})
		#print(unit_element[0])
		s = []
		for i in unit_element:
			j = i.find('td', {'class':'tlistname'})
			try:
				k = i.find('td', {'class':'tlistdownload'}).find('a')['href']
				k = k.split('=')[-1]
			except:
				k = 'Download Not Available'
			l = i.find('td', {'class':'tlistsize'})
			m = i.find('td', {'class':'tlistsn'})
			n = i.find('td', {'class':'tlistln'})
			o = i.find('td', {'class':'tlistdn'})
			try:
				tmp = j.text.replace('_',' ')+'\nid='+k+' sz='+l.text+' se='+m.text+' le='+n.text+' dl='+o.text+'\n'
			except:
				tmp = 'Not Available'
			print(tmp)
			s.append(tmp)
			
		return s
		
	def search(self,name):
		strname = str(name)
		print(strname)
		url = "http://www.nyaa.se/?page=search&cats=1_37&sort=2&term="+strname
		m = self.process_page(url)
		return m
		
	def getCompleteList(self,opt,genre_num):
		if opt == 'Date':
			url = 'http://www.nyaa.se/?cats=1_37'
		elif opt == 'Seeders':
			url = 'http://www.nyaa.se/?cats=1_37&sort=2'
		elif opt == 'Leechers':
			url = 'http://www.nyaa.se/?cats=1_37&sort=3'
		elif opt == 'Downloads':
			url = 'http://www.nyaa.se/?cats=1_37&sort=4'
			
		m = self.process_page(url)
		return m
	
	def getEpnList(self,name,opt):
		nm = name.rsplit('-',1)
		name = nm[0]
		name_id = nm[1]
		url = "http://www.nyaa.se/?page=download&tid=" + name_id
		print(url)
		summary = ""
		home = os.path.expanduser('~')+'/.config/AnimeWatch/History/Nyaa/'
		torrent_dest = home+name+'.torrent'
		if not os.path.exists(torrent_dest):
			ccurl(url+'#'+'-o'+'#'+torrent_dest)
		
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
		if opt == 'Date':
			url = 'http://www.nyaa.se/?cats=1_37'
		elif opt == 'Seeders':
			url = 'http://www.nyaa.se/?cats=1_37&sort=2'
		elif opt == 'Leechers':
			url = 'http://www.nyaa.se/?cats=1_37&sort=3'
		elif opt == 'Downloads':
			url = 'http://www.nyaa.se/?cats=1_37&sort=4'
		elif opt == 'Search':
			url = "http://www.nyaa.se/?page=search&cats=1_37&sort=2&term="+str(name)
		url = url + '&offset='+str(pgn)
		print(url)
		m = self.process_page(url)
		return m
