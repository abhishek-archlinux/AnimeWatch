import sys
import urllib
import urllib3
import pycurl
from io import StringIO,BytesIO
import re
import random
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup
import os.path
from subprocess import check_output
import shutil
import json
try:
	from headlessBrowser import BrowseUrl
except:
	from headlessBrowser_webkit import BrowseUrl

def cloudfare(url,quality):
	web = BrowseUrl(url,quality)

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
	
def ccurl(url,value,code):
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
	
	if value:
		if code == 1:
			print('-----code==1---')
			post_data = {'genrename': value}
		elif code == 2:
			post_data = {'station': value}
		elif code == 5:
			post_data = {'id': value}
		post_d = urllib.parse.urlencode(post_data)
		c.setopt(c.POSTFIELDS,post_d)
	if code == 3:
		c.setopt(c.HTTPHEADER,['ICY Metadata: 1'])
		
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
		#print(content)
		return content

def replace_all(text, di):
	for i, j in di.iteritems():
		text = text.replace(i, j)
	return text





class Shoutcast():
	def __init__(self):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
	def getOptions(self):
			criteria = ['History','Genre','Anime','JPOP']
			return criteria
		
	def getFinalUrl(self,name,epn,mir,quality):
		return epn
		
	def process_page(self,content):
		content = re.sub(r'\\',"-",content)
		print(content)
		#f = open('/tmp/tmp.txt','w')
		#f.write(content)
		#f.close()
		try:
			l = json.loads(content)
		except:
			o = re.findall('{[^}]*}',content)
			l = []
			for i in o:
				print(i)
				try:
					j = json.loads(i)
					print(j['ID'],j['Name'])
					l.append(j)
				except:
					pass
					print('----------------------error---------------')
		s = []
		for i in l:
			try:
				print(i['ID'],i['Name'],i['Bitrate'],i['Listeners'])
				s.append(i['Name'].replace('/','-')+'\nid='+str(i['ID'])+' Bitrate='+str(i['Bitrate'])+' Listeners='+str(i['Listeners'])+'\n')
			except:
				pass
		return s
		
	def search(self,name):
		strname = str(name)
		print(strname)
		if name.lower() == 'tv':
			m = self.getCompleteList(name.upper(),1)
		else:
			url = "https://www.shoutcast.com/Home/BrowseByGenre"
			content = ccurl(url,name,1)
			m = self.process_page(content)
		return m
		
	def getCompleteList(self,opt,genre_num):
		if opt == 'Genre' and genre_num == 0:
			url = "http://www.shoutcast.com/"
			content = ccurl(url,"",1)
			m = re.findall('Genre[^"]name[^"]*',content)
			#print m
			j = 0
			for i in m:
				m[j] = re.sub('Genre[^"]name=','',i)
				m[j] = re.sub("[+]|%20",' ',m[j])
				j = j+1
			m.sort()
			print(m)
			n = ["History","Genre","TV"]
			m = n + m
		elif opt == 'History':
			a =0
		elif opt == 'TV':
			name = []
			track = []
			aformat = []
			listeners = []
			bitrate = []
			idr = []
			url = "http://thugie.nl/streams.php"
			content = ccurl(url,"",4)
			soup = BeautifulSoup(content)
			tmp = soup.prettify()
			#m = soup.findAll('div',{'class':'boxcenterdir fontstyle'})
			#soup = BeautifulSoup(tmp)
			m = []
			links = soup.findAll('div',{'class':'dirOuterDiv1 clearFix'})
			for i in links:
				j = i.findAll('a')
				q = i.find_next('h2')
				g = i.find_next('h4')
				z = g.find_next('h4')
				for k in j:
					idr.append(k['href'].split('=')[-1][:-1])
				l = i.text
				n = re.findall('Station:[^"]*',l)
				p = re.sub('Playing','\nPlaying',n[0])
				p=p.rstrip()
				a = p.split('\n')
				name.append(a[0].split(":")[1])
				track.append(a[1].split(':')[1])
				aformat.append(q.text)
				listeners.append(g.text)
				bitrate.append(z.text)
			for i in range(len(idr)):
				m.append(name[i].strip().replace('/','-')+'-TV\nid='+str(idr[i]).replace('\\','')+' Bitrate='+str(bitrate[i])+' Listeners='+str(listeners[i])+'\n')
		else:
			url = "https://www.shoutcast.com/Home/BrowseByGenre"
			content = ccurl(url,opt,1)
			m = self.process_page(content)
		print(opt,url)
		return m
	
	def getEpnList(self,name,opt):
		nm = name.rsplit('-',1)
		#name = nm[0]
		name_id = nm[1]
		name = nm[0]
		file_arr = []
		id_station = int(name_id)
		station_url = ''
		if opt == "TV" or '-TV' in name:
			url = "http://thugie.nl/streams.php?tunein="+str(id_station)
			content = ccurl(url,'',1)
			final = re.findall('http://[^\n]*',content)
			station_url = final[0].rstrip()
			if 'stream.nsv' not in station_url:
				#print "Hello" + station_url
				station_url = str(station_url.rstrip()+";stream.nsv")
			
			
		else:
			url = "https://www.shoutcast.com/Player/GetStreamUrl"
			content = ccurl(url,id_station,2)
			m = re.findall('http://[^"]*',content)
			station_url = str(m[0])
		file_arr.append(name+'	'+station_url+'	'+'NONE')
		file_arr.append('No.jpg')
		file_arr.append('Not Available')
		return file_arr

	def getNextPage(self,opt,pgn,genre_num,name):
		m = []
		return m
