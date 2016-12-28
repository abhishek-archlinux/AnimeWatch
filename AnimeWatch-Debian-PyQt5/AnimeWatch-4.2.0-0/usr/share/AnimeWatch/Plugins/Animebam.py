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
from player_functions import ccurl

def replace_all(text, di):
	for i, j in di.iteritems():
		text = text.replace(i, j)
	return text
	
def naturallysorted(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)
	

class Animebam():
	def __init__(self,tmp):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		self.tmp_dir = tmp
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

		rfr = 'http://www.animebam.net/jwplayer/jwplayer.flash.swf'
		if m:
			url = 'http://www.animebam.net' + m[0]
		else:
			url = ''
		print(url)
		if url:
			content = ccurl(url)
		else:
			content = ''
		try:
			pre = re.search('file: "/play[^"]*',content).group()
			pre = pre.replace('file: "','')
			print(pre)
			url = 'http://www.animebam.net' + pre
			content = ccurl(url+'#'+'-Ie'+'#'+rfr)
			final = ''
			#print(content)
			if "Location:" in content:
				m = re.findall('Location: [^\n]*',content)
				print(m)
				final = re.sub('Location: |\r','',m[-1])
		except Exception as e:
			print(e,'--error--in--resolving--url--')
			final= ''
		return final
		"""
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
		"""
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
	def getEpnList(self,name,opt,depth_list,extra_info,siteName,category):
		url = "http://www.animebam.net/series/" + name
		img = []
		summary = ""
		content = ccurl(url)
		soup = BeautifulSoup(content,'lxml')
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
		
		print(img)
		
		#picn = "/tmp/AnimeWatch/" + name + ".jpg"
		picn = os.path.join(self.tmp_dir,name+'.jpg')
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
		#m.append(picn)
		#m.append(summary)
		record_history = True
		return (m,summary,picn,record_history,depth_list)
