import sys
import urllib
import pycurl
from io import StringIO,BytesIO
import re
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup 
import os
import os.path
import time
import shutil
from tempfile import mkstemp
from shutil import move
from os import remove, close
from os.path import expanduser
import base64
import platform
from player_functions import ccurl,naturallysorted

try:
	from headlessBrowser import BrowseUrl
except:
	from headlessBrowser_webkit import BrowseUrl
	
def cloudfare(url,quality,cookie):
	web = BrowseUrl(url,quality,cookie)

class KissAnime():
	def __init__(self,tmp):
		global tmp_working_dir
		self.tmp_dir = tmp
		tmp_working_dir = tmp
		self.cookie_file = os.path.join(tmp,'kcookie.txt')
		if not os.path.exists(self.cookie_file):
			f = open(self.cookie_file,'w')
			f.close()
	def getOptions(self):
			criteria = ['MostPopular','Newest','LatestUpdate','Genre','History']
			return criteria
			
	def ccurlN(self,url):
		content = ccurl(url+'#-b#'+self.cookie_file)
		if 'checking_browser' in content:
			if os.path.exists(self.cookie_file):
				os.remove(self.cookie_file)
			cloudfare(url,'',self.cookie_file)
			content = ccurl(url+'#-b#'+self.cookie_file)
		return content
		
	def search(self,name):
		
		if name != '':
			url = 'http://kissanime.ru/Search/Anime/?keyword=' + name
			content = self.ccurlN(url)
				
			m = re.findall('/Anime/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Anime/', '', i)
				m[j] = i
				if '?id=' in i and '/' in i:
					nm,ep = i.split('/')
					m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
				j = j + 1

			return m
	def getEpnList(self,name,opt,depth_list,extra_info,siteName,category):
			
		epn_num = ''
		if extra_info:
			name,epn_num = name.rsplit('--',1) 
			
		url = 'http://kissanime.ru/Anime/' + name
		print(url)
		content = self.ccurlN(url)
		epl = re.findall('/Anime/' + name + '[^"]*["?"]id[^"]*', content)
		try:
			img = re.findall('https://kissanime.ru/Uploads/Etc/[^"]*.jpg', content)
			if not img:
				img = re.findall('http://cdn.myanimelist.net/[^"]*.jpg', content)	
			print(img)
			picn = os.path.join(self.tmp_dir,name+'.jpg')
			print(picn)
			if img:
				print(img[0])
			if not os.path.isfile(picn):
				ccurl(img[0]+'#'+'-o'+'#'+picn,self.cookie_file)
		except:
			picn = os.path.join(self.tmp_dir,name+'.jpg')
		j = 0
		for i in epl:
			i = re.sub('/Anime/' + name + '/', '', i)
			epl[j] = i
			j = j + 1

		
		soup = BeautifulSoup(content,'lxml')
		summary = ""
		summary1 = ""
		try:
			link = soup.findAll('span',{'class':'info'})
			for i in link:
				l = (i.text).lower()
				if "genres" in l or "other name" in l or "country" in l or "date aired" in l or 'status' in l:
					
					k = i.findPrevious('p')
					if 'status' in l:
						t = k.text
						t = re.sub('"','',t)
						t = re.sub('Views:[^"]*','',t)
						summary = summary + t
					else: 
						summary = summary + k.text
				if "summary" in l:
					j = i.findNext('p')
					if j:
						summary1 = j.text
				
			summary = summary + summary1
			summary = re.sub('\r','',summary)
			summary = re.sub('\n\n','\n',summary)
		except:
			summary = 'Summary Not Available'
			
		epl=naturallysorted(epl)  
		if extra_info and epn_num:
			epl[:] = []
			epl.append(epn_num)
			
		record_history = True
		display_list = True
		return (epl,summary,picn,record_history,depth_list)
	def urlResolve(self,txt):
		m =[]

		if isinstance(txt,bytes):
			print("I'm byte")
			content = str((txt).decode('utf-8'))
		else:
			print(type(txt))
			content = str(txt)
			print("I'm unicode")
		n = content.split('\n')
		for i in n:
			j = i.split(':')
			if len(j) > 2:
				if 'Location' in j[0]:
					k = j[1].replace(' ','')
					k = k +':'+j[2]
					k = k.replace('\r','')
					print (k)
					m.append(k)
		return m
	
	
	def getFinalUrl(self,name,epn,mirror,quality):
		if '--' in name and 'id=' in name:
			name = name.split('--')[0]
		url = 'http://kissanime.ru/Anime/' + name + '/' + epn
		print(url)
		sd = ''
		hd = ''
		sd480 = ''
		full_hd = ''
		content = self.ccurlN(url)
		soup = BeautifulSoup(content,'lxml')
		m = soup.findAll('select',{'id':'selectQuality'})
		print(m)
		arr = []
		for i in m:
			j = i.findAll('option')
			for k in j:
				l = k['value']
				arr.append(str(base64.b64decode(l).decode('utf-8')))
		print(arr)
		for i in arr:
			if 'itag=18' in i:
				sd = i
			elif 'itag=22' in i:
				hd = i
			elif 'itag=37' in i:
				full_hd = i
			elif 'itag=59' in i:
				sd480 = i
			elif '=m18' in i:
				sd = i
			elif '=m22' in i:
				hd = i
		
		if quality == "hd" and hd:
			sd = hd
		elif quality == 'sd480p' and sd480:
			sd = sd480
		elif quality == 'best':
			if full_hd:
				sd = full_hd
			elif hd:
				sd = hd
			elif sd480:
				sd = sd480
		if not sd:
			if sd480:
				sd = sd480
			elif hd:
				sd = hd
		print(sd+'#'+'-I')
		content = ccurl(sd+'#'+'-I')
		print(content)
		m = self.urlResolve(content)
		if m:
			final = str(m[-1])
			print(final)
		return final
		
	def getCompleteList(self,opt,genre_num):
		
		if opt == 'Genre' and genre_num == 0:
			url = 'http://kissanime.ru/AnimeList/'
			content = self.ccurlN(url)
			
			
			m = re.findall('/Genre/[^"]*', content)
			m = list(set(m))
			m.sort()
			del m[9]
			m.pop()
			j = 0
			for i in m:
				i = re.sub('/Genre/', '', m[j])
				m[j] = i
				j = j + 1

			return m
		if opt == 'History':
			print('History')
		elif opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate':
			url = 'http://kissanime.ru/AnimeList/' + opt
			pgn = 1
			content = self.ccurlN(url)
			
			
			m = re.findall('/Anime/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Anime/', '', i)
				m[j] = i
				if '?id=' in i and '/' in i:
					nm,ep = i.split('/')
					m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
				j = j + 1

			return m
		if genre_num == 1:
			url = 'http://kissanime.ru/Genre/' + opt
			pgn = 1
			content = self.ccurlN(url)
			m = re.findall('/Anime/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Anime/', '', i)
				m[j] = i
				if '?id=' in i and '/' in i:
					nm,ep = i.split('/')
					m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
				j = j + 1

			return m
	def getNextPage(self,opt,pgn,genre_num,name):
		
		if opt != '' and pgn >= 1:
			pgnum = str(pgn)
			if (opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate'):
				url = 'http://kissanime.ru/AnimeList/' + opt + '?page=' + pgnum
			else:
				url = 'http://kissanime.ru/Genre/' + opt + '?page=' + pgnum
				#print(url
			content = self.ccurlN(url)
			m = re.findall('/Anime/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Anime/', '', i)
				m[j] = i
				if '?id=' in i and '/' in i:
					nm,ep = i.split('/')
					m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
				j = j + 1

			if m:
				return m
	def getPrevPage(self,opt,pgn,genre_num,name):
		
		if opt != '' and pgn >= 1:
			pgnum = str(pgn)
			if genre_num == 0:
				url = 'http://kissanime.ru/AnimeList/' + opt + '?page=' + pgnum
			else:
				url = 'http://kissanime.ru/Genre/' + opt + '?page=' + pgnum
			content = self.ccurlN(url)
			m = re.findall('/Anime/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Anime/', '', i)
				m[j] = i
				if '?id=' in i and '/' in i:
					nm,ep = i.split('/')
					m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
				j = j + 1

			if m:
				return m




