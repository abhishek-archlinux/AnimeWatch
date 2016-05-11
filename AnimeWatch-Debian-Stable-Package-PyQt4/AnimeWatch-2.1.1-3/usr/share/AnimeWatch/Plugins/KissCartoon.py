import sys
import urllib
import urllib3
import pycurl
from io import StringIO,BytesIO
import re
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup 
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
from headlessBrowser import BrowseUrl
def cloudfare(url,quality):
	web = BrowseUrl(url,quality)
def cloudfareOld():
			home1 = expanduser("~")
			#home1 = "/usr/local/share"
			pluginDir = home1+"/.config/AnimeWatch/src/Plugins"
			temp = progressBar(["phantomjs", pluginDir+"/kac.js","http://kisscartoon.me"])
			if isinstance(temp,bytes):
				print("I'm byte")
				try:
					temp = str((temp).decode('utf-8'))
				except:
					temp = str(temp)
			else:
				print(type(temp))
				temp = str(temp)
				print("I'm unicode")
			print(temp)
			p = re.findall('{[^}]*}',temp)
			for i in p:
				if "_cfduid" in i:
					cfd = i
				elif "cf_clearance" in i:
					cfc = i
				elif "ASP.NET" in i:
					asp = i
			n = re.findall('value": "[^"]*|expiry": [^,]*',cfc)
			e = re.findall('value": "[^"]*|expiry": [^,]*',cfd)
			a = re.findall('value": "[^"]*|expiry": [^,]*',asp)
			j = 0
			for i in n:
				n[j] = re.sub('value": "|expiry": ',"",i)
				j = j+1
			j = 0
			for i in e:
				e[j] = re.sub('value": "|expiry": ',"",i)
				j = j+1
			j = 0
			for i in a:
				a[j] = re.sub('value": "|expiry": ',"",i)
				j = j+1
			cookiefile = ".kisscartoon.me	TRUE	/	FALSE	"+str(e[0])+"	__cfduid	" + str(e[1]) + "\n" + "kisscartoon.me	FALSE	/	FALSE	0	ASP.NET_SessionId	"+str(a[0])+"\n"+".kisscartoon.me	TRUE	/	FALSE	"+str(n[0])+"	cf_clearance	" + str(n[1])
			f = open('/tmp/AnimeWatch/kcookieC.txt', 'w')
			f.write(cookiefile)
			f.close()
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
	c.setopt(c.FOLLOWLOCATION, True)
	c.setopt(c.USERAGENT, hdr)
	curl_opt = ''
	picn_op = ''
	nUrl = url
	if '#' in url:
		curl_opt = nUrl.split('#')[1]
		url = nUrl.split('#')[0]
		if curl_opt == '-o':
			picn_op = nUrl.split('#')[2]
			
			
	if os.path.exists('/tmp/AnimeWatch/kcookieC.txt'):
		c.setopt(c.COOKIEFILE, '/tmp/AnimeWatch/kcookieC.txt')
	else:
		print('inside ccurl')
		cloudfare(url,'')
		c.setopt(c.COOKIEFILE, '/tmp/AnimeWatch/kcookieC.txt')
	url = str(url)
	c.setopt(c.URL, url)
	storage = BytesIO()
	if curl_opt == '-o':
		f = open(picn_op,'wb')
		c.setopt(c.WRITEDATA, f)
		c.perform()
		c.close()
		f.close()
	else:
		if curl_opt == '-I':
			c.setopt(c.NOBODY, 1)
			c.setopt(c.HEADERFUNCTION, storage.write)
		else:
			c.setopt(c.WRITEFUNCTION, storage.write)
		c.perform()
		c.close()
		content = storage.getvalue()
		content = getContentUnicode(content)
		return content

def progressBar(cmd):
	
	content = subprocess.check_output(cmd)
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
	
	return (content)


def naturallysorted(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

def replace_all(text, di):
	for (i, j,) in di.iteritems():
		text = text.replace(i, j)

	return text



class KissCartoon():
	def __init__(self):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		
	def getOptions(self):
			criteria = ['MostPopular','Newest','LatestUpdate','Genre','History']
			return criteria
			
	def ccurlN(self,content,url):
		if 'checking_browser' in content:
			if os.path.exists('/tmp/AnimeWatch/kcookieC.txt'):
				os.remove('/tmp/AnimeWatch/kcookieC.txt')
			content = ccurl(url)
		return content
		
	def search(self,name):
		
		if name != '':
			url = 'http://kisscartoon.me/Search/Cartoon/?keyword=' + name
			content = ccurl(url)
			content = self.ccurlN(content,url)
			m = re.findall('/Cartoon/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Cartoon/', '', i)
				m[j] = i
				j = j + 1

			return m
	def getEpnList(self,name,opt):
		
		url = 'http://kisscartoon.me/Cartoon/' + name
		print(url)
		content = ccurl(url)
		content = self.ccurlN(content,url)
		f = open('/tmp/AnimeWatch/1.txt','w')
		f.write(content)
		f.close()
		epl = re.findall('/Cartoon/' + name + '[^"]*["?"]id[^"]*', content)
		#if not epl:
		#	epl = re.findall('[^"]*?id=[^"]*', content)
		try:
			img = re.findall('http://kisscartoon.me/Uploads/Etc/[^"]*.jpg', content)
			if not img:
				img = re.findall('http://cdn.myanimelist.net/[^"]*.jpg', content)	
			print(img)
			#jpgn = img[0].split('/')[-1]
			#print('Pic Name=' + jpgn
			picn = '/tmp/AnimeWatch/' + name + '.jpg'
			print(picn)
			if img:
				#img[0]=img[0].replace('kissanime.com','kissanime.to')
				print(img[0])
			if not os.path.isfile(picn):
				#subprocess.call(['curl','-L','-b','/tmp/AnimeWatch/kcookieC.txt','-A',self.hdr,'-o',picn,img[0]])
				ccurl(img[0]+'#'+'-o'+'#'+picn)
		except:
			picn = '/tmp/AnimeWatch/' + name + '.jpg'
		j = 0
		for i in epl:
			i = re.sub('/Cartoon/' + name + '/', '', i)
			epl[j] = i
			j = j + 1

		#try:
		soup = BeautifulSoup(content)
		
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
			summary = 'Not Available'
		print(summary)
		print(picn)
		epl=naturallysorted(epl)  
		epl.append(picn)
		epl.append(summary)
		return epl
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
		
		url = 'http://kisscartoon.me/Cartoon/' + name + '/' + epn
		print(url)
		sd = ''
		hd = ''
		sd480 = ''
		lnk_file = '/tmp/AnimeWatch/lnk.txt'
		if os.path.exists(lnk_file):
			os.remove(lnk_file)
			
		#if not os.path.isfile('/tmp/AnimeWatch/kcookieD.txt'):
		cloudfare(url,quality)
		
		
		cnt = 0
		
		if os.path.exists(lnk_file):
			link = open(lnk_file).read()
			final = link
			print(link)
		else:
			final = ''
			print('No Link Available or Clear The Cache')
		
		
		"""
		content = ccurl(url)
		print(content)
		soup = BeautifulSoup(content)
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
		
		if not sd:
			if sd480:
				sd = sd480
			elif hd:
				sd = hd
		#content = subprocess.check_output(['curl','-b','/tmp/AnimeWatch/kcookieC.txt','-L','-I','-A',self.hdr,sd])
		content = ccurl(sd+'#'+'-I')
		m = self.urlResolve(content)
		#print(m
		if m:
			#print(m
			final = m[-1]
		
		print(final)
		"""
		return final
		
	def getCompleteList(self,opt,genre_num):
		
		if opt == 'Genre' and genre_num == 0:
			url = 'http://kisscartoon.me/CartoonList/'
			content = ccurl(url)
			content = self.ccurlN(content,url)
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
			url = 'http://kisscartoon.me/CartoonList/' + opt
			pgn = 1
			content = ccurl(url)
			content = self.ccurlN(content,url)
			m = re.findall('/Cartoon/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Cartoon/', '', i)
				m[j] = i
				j = j + 1

			return m
		if genre_num == 1:
			url = 'http://kisscartoon.me/Genre/' + opt
			pgn = 1
			content = ccurl(url)
			content = self.ccurlN(content,url)
			m = re.findall('/Cartoon/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Cartoon/', '', i)
				m[j] = i
				j = j + 1

			return m
	def getNextPage(self,opt,pgn,genre_num):
		
		if opt != '' and pgn >= 1:
			pgnum = str(pgn)
			if (opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate'):
				url = 'http://kisscartoon.me/CartoonList/' + opt + '?page=' + pgnum
			else:
				url = 'http://kisscartoon.me/Genre/' + opt + '?page=' + pgnum
				#print(url
			content = ccurl(url)
			content = self.ccurlN(content,url)
			m = re.findall('/Cartoon/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Cartoon/', '', i)
				m[j] = i
				j = j + 1

			if m:
				return m
	def getPrevPage(self,opt,genre_num):
		
		if opt != '' and pgn >= 1:
			pgnum = str(pgn)
			if genre_num == 0:
				url = 'http://kisscartoon.me/CartoonList/' + opt + '?page=' + pgnum
			else:
				url = 'http://kisscartoon.me/Genre/' + opt + '?page=' + pgnum
			content = ccurl(url)
			content = self.ccurlN(content,url)
			m = re.findall('/Cartoon/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Cartoon/', '', i)
				m[j] = i
				j = j + 1

			if m:
				return m




