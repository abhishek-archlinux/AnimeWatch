import sys
import urllib.parse
import pycurl
from io import StringIO,BytesIO
import re
import random
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup
import os.path
from subprocess import check_output
from player_functions import send_notification,ccurl
try:
	import libtorrent as lt
	from stream import ThreadServer,TorrentThread,get_torrent_info
except:
	notify_txt = 'python3 bindings for libtorrent are broken\nTorrent Streaming feature will be disabled'
	send_notification(notify_txt)

import shutil
#from hurry.filesize import size
try:
	from headlessBrowser import BrowseUrl
except:
	from headlessBrowser_webkit import BrowseUrl

def cloudfare(url,quality,nyaa_c):
	web = BrowseUrl(url,quality,nyaa_c)

class Nyaa():
	def __init__(self,tmp):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		self.tmp_dir = tmp
		self.cookie_file = os.path.join(tmp,'nyaa.txt')
		if not os.path.exists(self.cookie_file):
			f = open(self.cookie_file,'w')
			f.close()
	def getOptions(self):
			criteria = ['Date','Seeders','Leechers','Downloads','History','LocalStreaming']
			return criteria
	
	def ccurlN(self,url):
		content = ccurl(url+'#-b#'+self.cookie_file)
		if 'checking_browser' in content:
			if os.path.exists(self.cookie_file):
				os.remove(self.cookie_file)
			cloudfare(url,'',self.cookie_file)
			content = ccurl(url+'#-b#'+self.cookie_file)
		return content
	
	def getFinalUrl(self,name,epn,local_ip,status,path_folder,session,ui,progress,tmp_dir):
		#nm = name.rsplit('-',1)
		#name = nm[0]
		#name_id = nm[1]
		global tmp_working_dir
		tmp_working_dir = tmp_dir
		index = int(epn)
		ip_n = local_ip.rsplit(':',1)
		ip = ip_n[0]
		port = int(ip_n[1])
		if status.lower() =='first run':
			thread_server = ThreadServer(ip,port)
			thread_server.start()
			#ses = set_torrent_session()
		path = path_folder
		
		#home = os.path.expanduser('~')+'/.config/AnimeWatch/History/Nyaa/'
		#torrent_dest = home+name+'.torrent'
		
		home = os.path.join(os.path.expanduser('~'),'.config','AnimeWatch','History','Nyaa')
		torrent_dest = os.path.join(home,name+'.torrent')
		
		#home1 = os.path.expanduser('~')+'/.config/AnimeWatch/src/Plugins/stream.py'
		print(torrent_dest,index,path)
		
		#handle,ses,info,cnt,cnt_limit,file_name = get_torrent_info(torrent_dest,index,path)
		#print(get_torrent_info(torrent_dest,index,path))
		#print('---before--error---164---')
		handle,ses,info,cnt,cnt_limit,file_name = get_torrent_info(torrent_dest,index,path,session,ui,progress,tmp_dir)
		#print('---line--error---166---')
		torrent_thread = TorrentThread(handle,cnt,cnt_limit,ses)
		torrent_thread.start()
		
		#p = subprocess.Popen(['python',home1,ip,str(port),torrent_dest,str(index),path])
		
		url = 'http://'+ip+':'+str(port)+'/'
		print(url,'-local-ip-url',status)
		if status.lower() == 'first run':
			return url,thread_server,torrent_thread,ses,handle
		else:
			return url,torrent_thread,ses,handle
		
	def process_page(self,url):
		content = self.ccurlN(url)
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
				tmp = j.text.replace('_',' ')+'	id='+k+'\nSize='+l.text+'\nSeeds='+m.text+'\nLeechers='+n.text+'\nTotal Downloads='+o.text
			except:
				tmp = 'Not Available'
			print(tmp)
			s.append(tmp)
			
		return s
		
	def search(self,name):
		strname = str(name)
		print(strname)
		url = "https://www.nyaa.se/?page=search&cats=1_37&sort=2&term="+strname
		m = self.process_page(url)
		return m
		
	def getCompleteList(self,opt,genre_num,ui,tmp_dir):
		global tmp_working_dir
		tmp_working_dir = tmp_dir
		if opt == 'Date':
			url = 'https://www.nyaa.se/?cats=1_37'
		elif opt == 'Seeders':
			url = 'https://www.nyaa.se/?cats=1_37&sort=2'
		elif opt == 'Leechers':
			url = 'https://www.nyaa.se/?cats=1_37&sort=3'
		elif opt == 'Downloads':
			url = 'https://www.nyaa.se/?cats=1_37&sort=4'
		print(opt,url)
		m = self.process_page(url)
		return m
	
	def getEpnList(self,name,opt,depth_list,extra_info,siteName,category):
		print(extra_info)
		#nm = name.rsplit('-',1)
		#name = nm[0]
		name_id = (re.search('id=[^\n]*',extra_info).group()).split('=')[1]
		url = "https://www.nyaa.se/?page=download&tid=" + name_id
		print(url)
		summary = ""
		#home = os.path.expanduser('~')+'/.config/AnimeWatch/History/Nyaa/'
		#torrent_dest = home+name+'.torrent'
		
		home = os.path.join(os.path.expanduser('~'),'.config','AnimeWatch','History','Nyaa')
		torrent_dest = os.path.join(home,name+'.torrent')
		
		if not os.path.exists(torrent_dest):
			ccurl(url+'#'+'-o'+'#'+torrent_dest,self.cookie_file)
		
		info = lt.torrent_info(torrent_dest)
		file_arr = []
		for f in info.files():
			file_path = f.path
			#if '/' in f.path:
			#	file_path = file_path.split('/')[-1]
			file_path = os.path.basename(file_path)	
			file_arr.append(file_path)
		
		
		#file_arr.append('No.jpg')
		#file_arr.append('Summary Not Available')
		record_history = True
		return (file_arr,'Summary Not Available','No.jpg',record_history,depth_list)

	def getNextPage(self,opt,pgn,genre_num,name):
		if opt == 'Date':
			url = 'https://www.nyaa.se/?cats=1_37'
		elif opt == 'Seeders':
			url = 'https://www.nyaa.se/?cats=1_37&sort=2'
		elif opt == 'Leechers':
			url = 'https://www.nyaa.se/?cats=1_37&sort=3'
		elif opt == 'Downloads':
			url = 'https://www.nyaa.se/?cats=1_37&sort=4'
		elif opt == 'Search':
			url = "https://www.nyaa.se/?page=search&cats=1_37&sort=2&term="+str(name)
		url = url + '&offset='+str(pgn)
		print(url)
		m = self.process_page(url)
		return m
