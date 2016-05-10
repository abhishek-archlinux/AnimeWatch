import urllib 
import sys
import pycurl
from io import StringIO,BytesIO
import re
import subprocess
from subprocess import check_output
import random
from bs4 import BeautifulSoup
import os.path
#from PyQt5 import QtCore, QtGui,QtWidgets
#from PyQt5.QtWidgets import QInputDialog
"""
class DlgBox(QtWidgets.QWidget):
	
	def __init__(self,i,j):
		super(DlgBox, self).__init__()
		self.itemR=j
		self.items=i
		self.setItem()
	def setItem(self):    
		
		item, ok = QtWidgets.QInputDialog.getItem(self, "QInputDialog.getItem()","Both Subbed And Dubbed Available", self.items, 0, False)
		if ok and item:
		    self.itemR=item
	def returnItem(self):
		return self.itemR
"""
def replace_all(text, di):
	for i, j in di.iteritems():
		text = text.replace(i, j)
	return text
	
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
		elif curl_opt == '-e':
			#c.setopt(c.FOLLOWLOCATION, True)
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
			#c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
		c.perform()
		c.close()
		content = storage.getvalue()
		content = getContentUnicode(content)
		return content



class Animebam():
	def __init__(self):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
	def getOptions(self):
			criteria = ['List','Random','History']
			return criteria
	def getFinalUrl(self,name,epn,mirror,quality):
		epn1 = epn.rsplit('-',1)[0]
		optcode = epn.rsplit('-',1)[1]
		url = "http://www.animebam.net/" + epn1
		print(url)
		content = ccurl(url)
		m = re.findall('/embed/[^"]*',content)
		print(m)

		referer = []
		j = 0
		for i in m:
			referer.append('http://www.animebam.net' + i)

		print(referer)

		length = len(m)

		rfr = referer[0]
		
		if optcode == "dubbed": 
			rfr = referer[-1]
		elif optcode == "subbed":
			rfr = referer[0]
		url = rfr
		content = ccurl(url)
		m = re.findall('http://[^"]*.mp4',content)
		print(m)
		if m:
			url = m[0]
			rfr = referer[0]
			content = ccurl(url+'#'+'-e'+'#'+rfr)
		m = re.findall('http://[^"]*',content)
		print(m)
		
		if m:
			return m[0]
		#subprocess.Popen(["smplayer","-add-to-playlist",m[0]]) 
	def search(self,name):
		url = "http://www.animebam.net/search?search=" + name
		content = ccurl(url)
		m = re.findall('/series/[^"]*',content)
		#print m
		j=0
		for i in m:
			m[j]=re.sub("/series/","",i)
			j = j+1
		return m
	def getCompleteList(self,opt,genre_num):
		url = "http://www.animebam.net/series"
		content = ccurl(url)
		#print(content)
		m = re.findall('/series/[^"]*',(content))
		#print m
		j=0
		for i in m:
			m[j]=re.sub("/series/","",i)
			j = j+1
		if opt == "Random":
			m = random.sample(m, len(m))
		return m
	def urlResolve(self,txt):
		m =[]
		
		if isinstance(txt,bytes):
			print("I'm byte")
			content = str((txt).decode('utf-8'))
		else:
			print (type(txt))
			content = str(txt)
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
	def getEpnList(self,name,opt):
		url = "http://www.animebam.net/series/" + name
		img = []
		summary = ""
		content = ccurl(url)
		soup = BeautifulSoup(content)
		link = soup.find('p',{'class':'ptext'})
		if link:
			summary = link.text
		link = soup.findAll('img')
		for i in link:
			if 'src' in str(i):
				j = i['src']
				if 'jpg' in j or 'jpeg' in j:
					img_src = j
					if 'http' not in img_src:
						img_src = 'http:'+img_src
					img.append(img_src)
		"""
		m = re.findall('ptext">[^"]*',content)
		img = re.findall('http[^"]*.jpg|http[^"]*.jpeg',content)
		"""
		print(img)
		
		picn = "/tmp/AnimeWatch/" + name + ".jpg"
		try:
			if not os.path.isfile(picn):
				#subprocess.call(["curl",'-L','-A',self.hdr,'-o',picn,img[0]])
				ccurl(img[0]+'#'+'-o'+'#'+picn)
		except:
			print("No Cover")
		
		if not summary:
			summary = "No Summary Available"
		n = re.findall(name+'-[^"]*',content)
		n=naturallysorted(n)  
		m = []
		sub = soup.findAll('i',{'class':'btn-xs btn-subbed'})
		if sub:
			for i in n:
				m.append(i+'-subbed')
		dub = soup.findAll('i',{'class':'btn-xs btn-dubbed'})
		if dub:
			for i in n:
				m.append(i+'-dubbed')
		m.append(picn)
		m.append(summary)
		return m
