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
import sys
import urllib
import urllib3
import pycurl
from io import StringIO,BytesIO
import re
import subprocess
import os.path
from subprocess import check_output
from bs4 import BeautifulSoup
import random
from os.path import expanduser
import datetime

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
		elif curl_opt == '-Ie' or curl_opt == '-e':
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
	#c.setopt(c.URL, url)
	try:
		c.setopt(c.URL, url)
	except UnicodeEncodeError:
		c.setopt(c.URL, url.encode('utf-8'))
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
		elif curl_opt == '-e':
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

def naturallysorted(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)
	

 
class musicArtist():
	def __init__(self):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
	def getContentUnicode(self,content):
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
	def ccurlT(self,url,rfr):
		hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		#if rfr:
		#	content = subprocess.check_output(['curl','-L','-A',hdr,'-e',rfr,url])
		#else:
		#	content = subprocess.check_output(['curl','-L','-A',hdr,url])
		#hdrs = {'user-agent':self.hdr}
		#req = requests.get(url,headers=hdrs)
		#content = req.text
		#content = self.getContentUnicode(content)
		content = ccurl(url)
		return content
	def search(self,name,name_url):
		if not name_url:
			name = name.replace(' ','+')
			url = "http://www.last.fm/search?q="+name
		else:
			url = name_url
		print (url)
		wiki = ""
		if not name_url:
			#content = self.ccurl(url,'')
			#print content
			content = ccurl(url)
			soup = BeautifulSoup(content,'lxml')

			link = soup.findAll('div',{'class':'row clearfix'})
			#print link
			for i in link:
				j = i.findAll('a')
				print (j)
				for k in j:
					try:
						url = k['href']
						name = k.text
						break
					except:
						pass
			print (name)
			print (url)
		
		#url = urllib.unquote(url).decode('utf-8')
		#try:
		#	url = urllib.unquote(url).decode('utf-8')
		#except:
		#	url = urllib.unquote(url).encode('utf-8')
		if url.startswith('http'):
			url = url
		else:
			url = "http://www.last.fm" + url
		
		print (url,'--music-artist--')
		img_url = url+'/+images'
		wiki_url = url + '/+wiki'
		print (wiki_url)
		#content = self.ccurl(wiki_url,'')
		content = ccurl(wiki_url)
		soup = BeautifulSoup(content)
		link = soup.find('div',{'class':'wiki-content'})
		print (link)

		if link:
			
			wiki = link.text
			#print wiki

		#content = self.ccurl(img_url,'')
		content = ccurl(img_url)
		soup = BeautifulSoup(content,'lxml')
		link = soup.findAll('ul',{'class':'image-list'})
		img = []
		for i in link:
			j = i.findAll('img')
			for k in j:
				l = k['src']
				u1 = l.rsplit('/',2)[0]
				u2 = l.split('/')[-1]
				u = u1 + '/770x0/'+u2
				img.append(u)
		img = list(set(img))
		#print img
		print (len(img))
		img.append(wiki)
		return img
