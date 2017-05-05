"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
from player_functions import ccurl,naturallysorted
try:
	from headlessBrowser import BrowseUrl
except:
	from headlessBrowser_webkit import BrowseUrl
	
def cloudfare(url,quality,c):
	web = BrowseUrl(url,quality,c)

class KissCartoon():
	def __init__(self,tmp):
		global tmp_working_dir
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		tmp_working_dir = tmp
		self.tmp_dir = tmp
		self.cookie_file = os.path.join(tmp,'kcookieC.txt')
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
			url = 'http://kimcartoon.me/Search/Cartoon/?keyword=' + name
			content = self.ccurlN(url)
			m = re.findall('/Cartoon/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Cartoon/', '', i)
				m[j] = i
				if '?id=' in i and '/' in i:
					nm,ep = i.split('/')
					m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
				j = j + 1

			return m
	def getEpnList(self,name,opt,depth_list,extra_info,siteName,category):
		if extra_info == '-1':
			arr = []
			return (arr,'Instructions','No.jpg',False,depth_list)
		else:
			epn_num = ''
			if extra_info:
				name,epn_num = name.rsplit('--',1) 
			
			url = 'http://kimcartoon.me/Cartoon/' + name
			print(url)
			content = self.ccurlN(url)
			soup = BeautifulSoup(content)
			#f = open('/tmp/AnimeWatch/1.txt','w')
			#f.write(content)
			#f.close()
			epl = re.findall('/Cartoon/' + name + '[^"]*["?"]id[^"]*', content)
			#if not epl:
			#	epl = re.findall('[^"]*?id=[^"]*', content)
			try:
				img = re.findall('http://kimcartoon.me/Uploads/Etc/[^"]*.jpg', content)
				img_src = ''
				if not img:
					img_src = soup.find('link',{'rel':'image_src'})
					if img_src and 'href' in str(img_src):
						img_link = img_src['href']
						if not img_link.startswith('http'):
							if img_link.startswith('/'):
								img_link = 'http://kimcartoon.me'+img_link
							else:
								img_link = 'http://kimcartoon.me/'+img_link
				else:
					img_link = img[0]
				print(img,img_src,img_link)
				picn = os.path.join(self.tmp_dir,name+'.jpg')
				print(picn)
				if not os.path.isfile(picn):
					if img:
						ccurl(img_link+'#'+'-o'+'#'+picn,self.cookie_file)
					elif img_src:
						ccurl(img_link+'#'+'-o'+'#'+picn)
			except:
				#picn = '/tmp/AnimeWatch/' + name + '.jpg'
				picn = os.path.join(self.tmp_dir,name+'.jpg')
			j = 0
			for i in epl:
				i = re.sub('/Cartoon/' + name + '/', '', i)
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
			epl=naturallysorted(epl)  
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
		url = 'http://kimcartoon.me/Cartoon/' + name + '/' + epn
		print(url)
		sd = ''
		hd = ''
		sd480 = ''
		lnk_file = os.path.join(self.tmp_dir,'lnk.txt')
		if os.path.exists(lnk_file):
			os.remove(lnk_file)
		#if quality == 'best':
		#	quality = 'hd'
		#if not os.path.isfile('/tmp/AnimeWatch/kcookieD.txt'):
		cloudfare(url,quality,self.cookie_file)
		
		if os.path.exists(lnk_file):
			link = open(lnk_file).read()
			final = link
			print(link)
		else:
			final = ''
			print('No Link Available or Clear The Cache')
		return final
		
	def getCompleteList(self,opt,genre_num):
		instr = "Press . or > for next page	-1"
		m = []
		opt_arr = ['genre','mostpopular','newest','latestupdate','history']
		if opt == 'Genre' and genre_num == 0:
			url = 'http://kimcartoon.me/CartoonList/'
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

		if opt == 'History':
			print('History')
		elif opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate':
			url = 'http://kimcartoon.me/CartoonList/' + opt
			pgn = 1
			content = self.ccurlN(url)
			m = re.findall('/Cartoon/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Cartoon/', '', i)
				m[j] = i
				if '?id=' in i and '/' in i:
					nm,ep = i.split('/')
					m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
				j = j + 1
			m.append(instr)
		if genre_num == 1 or opt.lower() not in opt_arr:
			url = 'http://kimcartoon.me/Genre/' + opt
			pgn = 1
			content = self.ccurlN(url)
			m = re.findall('/Cartoon/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Cartoon/', '', i)
				m[j] = i
				if '?id=' in i and '/' in i:
					nm,ep = i.split('/')
					m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
				j = j + 1
			m.append(instr)
		return m
	def getNextPage(self,opt,pgn,genre_num,name):
		
		if opt != '' and pgn >= 1:
			pgnum = str(pgn)
			if (opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate'):
				url = 'http://kimcartoon.me/CartoonList/' + opt + '?page=' + pgnum
			else:
				url = 'http://kimcartoon.me/Genre/' + opt + '?page=' + pgnum
				#print(url
			content = self.ccurlN(url)
			m = re.findall('/Cartoon/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Cartoon/', '', i)
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
				url = 'http://kimcartoon.me/CartoonList/' + opt + '?page=' + pgnum
			else:
				url = 'http://kimcartoon.me/Genre/' + opt + '?page=' + pgnum
			content = self.ccurlN(url)
			m = re.findall('/Cartoon/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Cartoon/', '', i)
				m[j] = i
				if '?id=' in i and '/' in i:
					nm,ep = i.split('/')
					m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
				j = j + 1

			if m:
				return m




