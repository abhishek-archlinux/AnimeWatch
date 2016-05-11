import urllib
import urllib3
import sys
import pycurl
from io import StringIO,BytesIO
import re
import subprocess
from subprocess import check_output
import random
from bs4 import BeautifulSoup  
import os.path
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
		elif curl_opt == '-Ie':
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
	


class AnimePlace():
	def __init__(self):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
	def getOptions(self):
			criteria = ['Random','History','Subbed','Dubbed',"Movies"]
			return criteria
	def search(self,name):
		return name
	def getFinalUrl(self,name,epn,mirror,quality):
	
			url = "http://theanimeplace.co/" + epn + '/'
			content = ccurl(url)
			soup = BeautifulSoup(content)
			link = soup.findAll('iframe')
			url = link[0]['src']
			print(url)

		
			if "play" in url:
				content = ccurl(url)
				soup = BeautifulSoup(content)
				link = soup.findAll('form')
				action = link[0]['action']

				mir = re.sub('/frame.php',"",action)
				  
				link = soup.findAll('input', { "name" : 'v' })
				v = link[0]['value']

				link = soup.findAll('input', { "name" : 'w' })
				w = link[0]['value']

				link = soup.findAll('input', { "name" : 'h' })
				h = link[0]['value']

				link = soup.findAll('input', { "name" : 'submit' })
				submit = link[0]['value']
				submit = re.sub(" ","+",submit)
				pre = action + "?v=" + v + "&w=" + w + "&h=" + h + "&submit=" + submit
				content = ccurl(pre)
				url1 = re.findall("/file.php[^']*&res=",content)

				final = mir + url1[0]
				print(final)
				#scode = subprocess.check_output(["zenity","--entry","--text","Select Size from Dropdown Menu","--entry-text", "360P","480P","720P"])
				#size = re.sub("\n","",scode)
				final = final + "360P"
				print(final)
			else:
				content = ccurl(url)
				soup = BeautifulSoup(content)
				link = soup.findAll('form')
				action = link[0]['action']
				if 'ubox_frame' in action:
					mir = re.sub('/ubox_frame.php',"",action)
				elif 'xframe.php' in action:
					mir = re.sub('/xframe.php',"",action)
				link = soup.findAll('input', { "name" : 'v' })
				v = link[0]['value']

				link = soup.findAll('input', { "name" : 'w' })
				w = link[0]['value']

				link = soup.findAll('input', { "name" : 'h' })
				h = link[0]['value']
				
				link = soup.findAll('input', { "name" : 's_id' })
				s_id = link[0]['value']

				link = soup.findAll('input', { "name" : 'submit' })
				submit = link[0]['value']
				submit = re.sub(" ","+",submit)
				pre = action + "?v=" + v + "&w=" + w + "&h=" + h + "&s_id=" + s_id + "&submit=" + submit
				print(pre)
				content = ccurl(pre)
				url1 = re.findall("/ubox_file.php[^']*",content)
				if not url1:
					url1 = re.findall("/xfile.php[^']*",content)
				final = mir + url1[0]
				print(final)

			print("Mirror: " + mir)
			#content = (subprocess.check_output(["curl","-I","-A",self.hdr,final]))
			content = ccurl(final+'#'+'-I')
			
			location = re.findall("Location:[^\n]*",content)
			location1 = ""
			if location:
				location1 = re.sub('Location: ','',location[0])
				location1 = re.sub('\r','',location1)
			else:
				final = mir + url[0]
				final = re.sub("&res=","",final)
				print(final)
				#content = (subprocess.check_output(["curl","-I","-A",self.hdr,final]))
				content = ccurl(final+'#'+'-I')
				
				location = re.findall("Location:[^\n]*",content)
				location1 = ""
				if location:
					location1 = re.sub('Location: ','',location[0])
					location1 = re.sub('\r','',location1)
			
			final = mir + '/' + location1
			print(final)
			#print(url
			""" 
			content = subprocess.check_output(["curl","-I","-L","-A",hdr,final])
			sizeArr = re.findall("Content-Length:[^\n]*",content)
			if sizeArr:
				size1 = re.sub("Content-Length:","",sizeArr[0])
				size1 = re.sub("\r| ","",size1)
				size2 = int(size1)/(1024*1024)
				print("Size = " + str(size2) + "M"
			"""
			return final
			#subprocess.Popen(["smplayer", "-add-to-playlist",final])
	
	def getEpnList(self,name,opt):
		url = "http://theanimeplace.co/watch/" + name + "/"
		print(url)
		content = ccurl(url)
		img = re.findall('http[^"]*.jpg|http[^"]*.jpeg',content)
		picn = "/tmp/AnimeWatch/" + name + ".jpg"
		try:
			if not os.path.isfile(picn):
				#subprocess.call(["curl","-A",self.hdr,"-o",picn,img[0]])
				ccurl(img[0]+'#'+'-o'+'#'+picn)
		except:
			print("No Cover")
		soup = BeautifulSoup(content)
		m = soup.findAll('p')
		print(m)
		try:
			summary = str(m[2].text)
		except:
			summary = "No Summary Available"
		#replc = {'</span>':'', '<p>':'','<br/>':'','</p>':'','<br />':'','<span >':'','</div>':'','<div>':'','<span>':'','<div id=':''}
		#summary = replace_all(sumry, replc)
		m = re.findall('href="http://theanimeplace.co/[^"]*episode[^"]*', content)
		link = soup.findAll('div',{ 'id':"ep_list_s"})
		m[:]=[]
		for i in link:
			a = i.findAll('a')
			for j in a:
				if 'href' in str(j):
					k = (j['href']).split('/')
					print(k[-2])
					m.append(k[-2])
		print("opt=" + opt)
		if opt == "Movies":
			m.append(name)
		j=0
		for i in m:
			i = re.sub('href="http://theanimeplace.co/',"",i)
			i = re.sub('/',"",i)
			m[j] = i
			j = j+1
		#if opt != "Random":
		m=naturallysorted(m)
		m.append(picn)
		m.append(summary)
		return m
		  
	def getCompleteList(self,opt,genre_num):
		opt = opt.lower()
		if opt == "random":
			url1="http://theanimeplace.co/anime-series-list/?type=subbed"
			url2="http://theanimeplace.co/anime-series-list/?type=dubbed"
			content1 = ccurl(url1)
			content2 = ccurl(url2)
			content = content1 + content2
		elif opt == "movies":
			url1 = "http://theanimeplace.co/watch/movies-dubbed/"
			url2 = "http://theanimeplace.co/watch/movies-subbed/"
			content1 = ccurl(url1)
			content2 = ccurl(url2)
			content = content1 + content2
		else:
			url = "http://theanimeplace.co/anime-series-list/?type="+opt
			content = ccurl(url)
		if opt != "movies":	
			m = re.findall('watch/[^"]*', content)
			j=0
			for i in m:
				i = re.sub('watch/',"",i)
				m[j] = i
				j = j+1
		else:
			m = re.findall('http://theanimeplace.co/[^"]*english[^/]*', content)
			j=0
			for i in m:
				i = re.sub('http://theanimeplace.co/',"",i)
				i = re.sub('/',"",i)
				m[j] = i
				j = j+1
		if opt == "random":
			m = random.sample(m, len(m))
		
		return m
