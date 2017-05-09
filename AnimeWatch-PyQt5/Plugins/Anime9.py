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
import platform
import json
from player_functions import ccurl,naturallysorted,send_notification

try:
	from headlessBrowser import BrowseUrl
except:
	from headlessBrowser_webkit import BrowseUrl
	
def cloudfare(url,quality,cookie,end_point,get_cookie,dm):
	web = BrowseUrl(url,quality,cookie,end_point=end_point,get_cookie=get_cookie,domain_name=dm)

class Anime9():
	
	def __init__(self,tmp):
		global tmp_working_dir
		self.tmp_dir = tmp
		tmp_working_dir = tmp
		self.cookie_file = os.path.join(tmp,'cookie9.txt')
			
	def getOptions(self):
			criteria = ['MostPopular','Newest','LatestUpdate','Series','Movies','Ongoing','Genre','History']
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
		
		if name:
			if not os.path.isfile(self.cookie_file):
				new_url = 'https://9anime.to/'
				print(new_url)
				cloudfare(new_url,'sd',self.cookie_file,'user-info',True,'9anime.to')
			url = 'https://9anime.to/search?keyword=' + name
			arr = self.parse_page(url,cookie=self.cookie_file)
			if len(arr) == 1:
				print(arr,'--76---')
				if arr[0] == 'get_cookie':
					if os.path.isfile(self.cookie_file):
						os.remove(self.cookie_file)
					new_url = 'https://9anime.to/'
					print(new_url)
					cloudfare(new_url,'sd',self.cookie_file,'user-info',True,'9anime.to')
					url = 'https://9anime.to/search?keyword=' + name
					arr = self.parse_page(url,cookie=self.cookie_file)
			return arr
			
	def getEpnList(self,name,opt,depth_list,extra_info,siteName,category):
		if extra_info == '-1':
			arr = []
			return (arr,'Instructions','No.jpg',False,depth_list)
		else:
			base_url = 'https://9anime.to'
			url = extra_info
			print(url,'--74--')
			content = ccurl(url)
			soup = BeautifulSoup(content,'lxml')
			arr = []
			
			m = soup.findAll('div',{'class':'server row'})
			p = 0
			index = 0
			for i in m:
				index = 0
				j = i.findAll('li')
				if p == 0:
					for k in j:
						l = k.find('a')
						n = l.text+'	'+os.path.join(base_url,l['href'])
						arr.append(n)
				else:
					for k in j:
						l = k.find('a')
						try:
							n = os.path.join(l['href'].split('/')[-1])
						except Exception as e:
							print(e,'--84--')
							n = 'NONE'
						arr[index] = arr[index]+'::'+n
						index = index + 1
				p = p +1
			record_history = True
			display_list = True
			summary = 'Not Available'
			picn = 'No.jpg'
			
			try:
				m = soup.find('h1',{'class':'title'})
				pic_url = m.findNext('img')['src']
				l = m.findNext('div',{'id':'info'})
				summary = m.text.strip()+'\n'+l.text.strip()
				picn = os.path.join(self.tmp_dir,name+'.jpg')
				if not os.path.exists(picn):
					ccurl(pic_url+'#'+'-o'+'#'+picn)
				print(picn,'--98--')
			except Exception as e:
				print(e)
			return (arr,summary,picn,record_history,depth_list)
	
	def get_epn_url(self,name,epn,mirror,quality):
		final = ''
		new_epn = epn.split('/')[-1]
		if '::' in new_epn:
			id_arr = new_epn.split('::')
			print(id_arr,mirror)
			if mirror <= len(id_arr):
				epn_id = id_arr[mirror-1]
			else:
				epn_id = id_arr[0]
		else:
			epn_id = new_epn
		if not os.path.isfile(self.cookie_file):
			new_url = 'https://9anime.to'+epn.split('::')[0]
			print(new_url)
			cloudfare(new_url,quality,self.cookie_file,'watching',True,'9anime.to')
		url = 'https://9anime.to/ajax/episode/info?id='+epn_id+'&update=0'
		content = ccurl(url+'#-b#'+self.cookie_file)
		l = json.loads(content)
		for i in l:
			print(i,l[i])
			if i == 'grabber':
				_api = l[i]
			if i == 'params':
				_id = l[i]['id']
				_token = l[i]['token']
				_opt = l[i]['options']
		nurl = '?id={0}&token={1}&options={2}&mobile=0'.format(_id,_token,_opt)
		return (_api,nurl)
	
	def getFinalUrl(self,name,epn,mirror,quality):
		try:
			_api,nurl = self.get_epn_url(name,epn,mirror,quality)
		except Exception as e:
			print(e,'--158--')
			if os.path.isfile(self.cookie_file):
				os.remove(self.cookie_file)
			_api,nurl = self.get_epn_url(name,epn,mirror,quality)
			
		url = os.path.join(_api,nurl)
		print(url)

		content = ccurl(url)

		arr = []
		try:
			l = json.loads(content)
		except Exception as e:
			print(e)
			content = content.replace('}{',',')
			#print(content)
			try:
				l = json.loads(content)
			except Exception as e:
				print(e)
				l = []
		if l:
			for i in l:
				#print(i)
				if i == 'data':
					for k in l[i]:
						try:
							j = (k['label'],k['file'])
						except Exception as e:
							print(e)
							j = ('no-label','no-file')
						arr.append(j)
		else:
			m = re.findall('"file":"http[^"]*',content)
			print(m)
			for i in m:
				i = i.replace('"file":"','')
				k = ('no-label','no-file')
				if 'itag=18' in i:
					k = ('360p',i)
				elif 'itag=22' in i:
					k = ('720p',i)
				elif 'itag=59' in i:
					k = ('480p',i)
				elif 'itag=37' in i:
					k = ('1080p',i)
				arr.append(k)
		if arr:
			d = dict(arr)
			print(d)
			if quality == 'sd' and '360p' in d:
				final = d['360p']
			elif quality == 'sd480p':
				if '480p' in d:
					final = d['480p']
				else:
					final = d['360p']
			elif quality == 'hd':
				if '720p' in d:
					final = d['720p']
				elif '480p' in d:
					final = d['480p']
				else:
					final = d['360p']
			elif quality == 'best':
				if '1080p' in d:
					final = d['1080p']
				elif '720p' in d:
					final = d['720p']
				elif '480p' in d:
					final = d['480p']
				else:
					final = d['360p']
		if final:
			content = ccurl(final+'#'+'-I')
			m = re.findall('Location: [^\n]*',content)
			if m:
				#print(m)
				final = re.sub('Location: |\r','',m[-1])
		return final
	
	def parse_page(self,url,cookie=None):
		if cookie is None:
			content = ccurl(url)
		else:
			content = ccurl(url+'#-b#'+cookie)
		soup = BeautifulSoup(content,'lxml')
		arr = []
		m = soup.findAll('div',{'class':'item'})
		for i in m:
			k = i.find('a')['href']
			try:
				l = i.find('img')['alt']
				if l.startswith('.'):
					l = l[1:]
				if '/' in l:
					l = l.replace('/','-')
			except Exception as e:
				print(e)
				l = ''
			n = l+'	'+k
			arr.append(n)
		if not arr:
			if 'make sure your browser supports cookie' in content:
				arr.append('get_cookie')
		return arr
	
	def getCompleteList(self,opt,genre_num):
		m = []
		instr = "Press . or > for next page	-1"
		opt_arr = [
			'genre','mostpopular','newest','latestupdate',
			'history','series','movies','ongoing'
			]
		if opt == 'Genre' and genre_num == 0:
			url = 'https://9anime.to'
			content = ccurl(url)
			m = re.findall('/genre/[^"]*', content)
			m = list(set(m))
			m.sort()
			del m[9]
			m.pop()
			j = 0
			for i in m:
				i = re.sub('/genre/', '', m[j])
				m[j] = i
				j = j + 1
		if opt == 'History':
			print('History')
		elif (opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate' 
				or opt == 'Series' or opt == 'Ongoing' or opt == 'Movies'):
			new_opt = 'newest'
			if opt.lower() == 'mostpopular':
				new_opt = 'most-watched'
			elif opt.lower() == 'newest':
				new_opt = 'newest'
			elif opt.lower() == 'latestupdate':
				new_opt = 'updated'
			elif opt.lower() == 'series':
				new_opt = 'tv-series'
			elif opt.lower() == 'movies':
				new_opt = 'movies'
			elif opt.lower() == 'ongoing':
				new_opt = 'ongoing'
			url = 'https://9anime.to/'+new_opt
			m = self.parse_page(url)
			m.append(instr)
		if genre_num == 1 or opt.lower() not in opt_arr:
			url = 'https://9anime.to/genre/' + opt
			m = self.parse_page(url)
			m.append(instr)
		return m
		
	def getNextPage(self,opt,pgn,genre_num,name):
		if opt and pgn >= 1:
			pgnum = str(pgn)
			if (opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate' 
					or opt == 'Series' or opt == 'Ongoing' or opt == 'Movies'):
				new_opt = 'newest'
				if opt.lower() == 'mostpopular':
					new_opt = 'most-watched'
				elif opt.lower() == 'newest':
					new_opt = 'newest'
				elif opt.lower() == 'latestupdate':
					new_opt = 'updated'
				elif opt.lower() == 'series':
					new_opt = 'tv-series'
				elif opt.lower() == 'movies':
					new_opt = 'movies'
				elif opt.lower() == 'ongoing':
					new_opt = 'ongoing'
				url = 'https://9anime.to/'+new_opt+'?page='+pgnum
			else:
				url = 'https://9anime.to/genre/' + opt + '?page=' + pgnum
			arr = self.parse_page(url)
			return arr
				
	def getPrevPage(self,opt,pgn,genre_num,name):
		arr = self.getNextPage(opt,pgn,genre_num,name)
		return arr




