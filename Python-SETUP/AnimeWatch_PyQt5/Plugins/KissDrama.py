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
import fileinput
import codecs
import base64
from player_functions import ccurl,naturallysorted
try:
	from headlessBrowser import BrowseUrl
except:
	from headlessBrowser_webkit import BrowseUrl
	
def cloudfare(url,quality,c):
	web = BrowseUrl(url,quality,c)

class KissDrama():
	def __init__(self,tmp):
		global tmp_working_dir
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		tmp_working_dir = tmp
		self.tmp_dir = tmp
		self.cookie_file = os.path.join(tmp,'kcookieD.txt')
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
			url = 'http://kissasian.com/Search/Drama/?keyword=' + name
			content = self.ccurlN(url)
			m = re.findall('/Drama/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Drama/', '', i)
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
		
		url = 'http://kissasian.com/Drama/' + name
		print(url)
		content = self.ccurlN(url)
		#f = open('/tmp/AnimeWatch/1.txt','w')
		#f.write(content)
		#f.close()
		epl = re.findall('/Drama/' + name +'/' +'[^"]*["?"]id[^"]*', content)
		#if not epl:
		#	epl = re.findall('[^"]*?id=[^"]*', content)
		try:
			img = re.findall('http://kissasian.com/Uploads/Etc/[^"]*.jpg', content)
			if not img:
				img = re.findall('http://cdn.myanimelist.net/[^"]*.jpg', content)	
			print(img)
			#jpgn = img[0].split('/')[-1]
			#print('Pic Name=' + jpgn
			#picn = '/tmp/AnimeWatch/' + name + '.jpg'
			picn = os.path.join(self.tmp_dir,name+'.jpg')
			print(picn)
			if img:
				#img[0]=img[0].replace('kissanime.com','kissanime.to')
				print(img[0])
			if not os.path.isfile(picn):
				#subprocess.call(['curl','-L','-b','/tmp/AnimeWatch/kcookieD.txt','-A',self.hdr,'-o',picn,img[0]])
				ccurl(img[0]+'#'+'-o'+'#'+picn,self.cookie_file)
		except:
			#picn = '/tmp/AnimeWatch/' + name + '.jpg'
			picn = os.path.join(self.tmp_dir,name+'.jpg')
		j = 0
		for i in epl:
			i = re.sub('/Drama/' + name + '/', '', i)
			epl[j] = i
			j = j + 1

		#try:
		soup = BeautifulSoup(content,'lxml')
		
		summary = ""
		summary1 = ""
		try:
			link = soup.findAll('span',{'class':'info'})
			#link = soup.findAll('div',{'class':'barContent'})
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
		#print(summary)
		#print(picn)
		epl=naturallysorted(epl)  
		#epl.append(picn)
		#epl.append(summary)
		if extra_info and epn_num:
			epl[:] = []
			epl.append(epn_num)
		record_history = True
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
		url = 'http://kissasian.com/Drama/' + name + '/' + epn
		print(url)
		sd = ''
		hd = ''
		sd480 = ''
		lnk_file = os.path.join(self.tmp_dir,'lnk.txt')
		if os.path.exists(lnk_file):
			os.remove(lnk_file)
			
		#if not os.path.isfile('/tmp/AnimeWatch/kcookieD.txt'):
		print(url,quality,self.cookie_file)
		cloudfare(url,quality,self.cookie_file)
		
		
		cnt = 0
		
		
		if os.path.exists(lnk_file):
			link = open(lnk_file).read()
			final = link
			print(link)
		else:
			final = ''
			print('No Link Available or Clear The Cache')
		
		return final
		
	def getCompleteList(self,opt,genre_num):
		
		if opt == 'Genre' and genre_num == 0:
			url = 'http://kissasian.com/DramaList/'
			content = self.ccurlN(url)
			m = re.findall('/Genre/[^"]*', content)
			m = list(set(m))
			m.sort()
			#del m[9]
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
			url = 'http://kissasian.com/DramaList/' + opt
			pgn = 1
			content = self.ccurlN(url)
			m = re.findall('/Drama/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Drama/', '', i)
				m[j] = i
				if '?id=' in i and '/' in i:
					nm,ep = i.split('/')
					m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
				j = j + 1

			return m
		if genre_num == 1:
			url = 'http://kissasian.com/Genre/' + opt
			pgn = 1
			content = self.ccurlN(url)
			m = re.findall('/Drama/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Drama/', '', i)
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
				url = 'http://kissasian.com/DramaList/' + opt + '?page=' + pgnum
			else:
				url = 'http://kissasian.com/Genre/' + opt + '?page=' + pgnum
				#print(url
			content = self.ccurlN(url)
			m = re.findall('/Drama/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Drama/', '', i)
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
				url = 'http://kissasian.com/DramaList/' + opt + '?page=' + pgnum
			else:
				url = 'http://kissasian.com/Genre/' + opt + '?page=' + pgnum
			content = self.ccurlN(url)
			m = re.findall('/Drama/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Drama/', '', i)
				m[j] = i
				if '?id=' in i and '/' in i:
					nm,ep = i.split('/')
					m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
				j = j + 1

			if m:
				return m




