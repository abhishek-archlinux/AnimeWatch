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
		#print(content)
		if 'checking_browser' in content:
			if os.path.exists(self.cookie_file):
				os.remove(self.cookie_file)
			cloudfare(url,'',self.cookie_file)
			content = ccurl(url+'#-b#'+self.cookie_file)
		return content
		
	def process_page(self,url):
		content = self.ccurlN(url)
		soup = BeautifulSoup(content,'lxml')
		#print(soup.prettify())
		unit_element = soup.findAll('tr',{'class':'tlistrow trusted'})
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
		
	def getCompleteList(self,opt,genre_num,ui,tmp_dir,hist_folder):
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
		name_id = (re.search('id=[^\n]*',extra_info).group()).split('=')[1]
		url = "https://www.nyaa.se/?page=download&tid=" + name_id
		print(url)
		summary = ""
		
		torrent_dest = os.path.join(siteName,name+'.torrent')
		
		if not os.path.exists(torrent_dest):
			ccurl(url+'#'+'-o'+'#'+torrent_dest,self.cookie_file)
		
		info = lt.torrent_info(torrent_dest)
		file_arr = []
		for f in info.files():
			file_path = f.path
			file_path = os.path.basename(file_path)	
			file_arr.append(file_path)
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
