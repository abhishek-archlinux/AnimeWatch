import sys
import urllib
import urllib3
import pycurl
from io import StringIO,BytesIO
import re
import subprocess
from subprocess import check_output
import random
from bs4 import BeautifulSoup  
import os.path
try:
	import jsbeautifier.unpackers.packer as packer
except:
	pass

def naturallysorted(l):
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

def replace_all(text, di):
	for i, j in di.iteritems():
		text = text.replace(i, j)
	return text
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
def ccurlNew(url):
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
		
def ccurl(url,value):
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0"
	
	c = pycurl.Curl()
	if value == "no_redir":
		print("no redirect")
	else:
		c.setopt(c.FOLLOWLOCATION, True)
	c.setopt(c.USERAGENT, hdr)
	if value != "" and value != "no_redir":
		post_data = {'id': value}
		post_d = urllib.parse.urlencode(post_data)
		c.setopt(c.POSTFIELDS,post_d)
	#if rfr != "":
	 # c.setopt(pycurl.REFERER, rfr)
	url = str(url)
	c.setopt(c.URL, url)
	
	storage = BytesIO()
	c.setopt(c.WRITEDATA, storage)
	c.perform()
	c.close()
	content = storage.getvalue()
	content = getContentUnicode(content)
	return (content)
	
def simplyfind(i):
	content = ccurl(i,"")
	#replc = {' ':'%20', '[':'%5B', ']':'%5D','!':'%21'}
	m = re.findall('["]http://[^"]*.mp4[^"]*|["]http://[^"]*.flv[^"]*|["]https://redirector[^"]*|["]https://[^"]*.mp4', content)
	m1 = re.findall("[']http://[^']*.mp4[^']*|[']http://[^']*.flv[^']*|[']https://redirector[^']*|[']https://[^']*.mp4", content)
	print(m)
	if m:
		found = m[0]
		found = found[1:]
		found = str(urllib.parse.unquote(found))
		#found = replace_all(found, replc)
	elif m1:
		found = m1[0]
		found = found[1:]
		found = str(urllib.parse.unquote(found))
		#found = replace_all(found, replc)
	else:
		found = ""
	return found

def findurl(url):
	final = ""
	hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
	print('--------findurl-----',url)
	if "myvidstream" in str(url):
		#print("myvidstream="+url
		packed = ''
		content = ccurl(url,"")
		final = mp4starUrl(content,'myvidstream')
		"""
		soup = BeautifulSoup(content,'lxml')
		link = soup.findAll('script',{'type':'text/javascript'})
		for i in link:
			if 'myvidstream' in i.text:
				#print(i.text)
				packed = i.text
				break
		if packed:
			val = packer.unpack(packed)
			print(val)
			soup = BeautifulSoup(val,'lxml')
			m = (re.search('file[^)]*',val)).group()
			print(m)
			if m:
				n = re.search("http[^']*",m).group()
				if n:
					print(n)
					final = n
					final = re.sub(' |"','',final)
					final = re.sub("'",'',final)
					fi = final.split('\\')
					if fi:
						final = fi[0]
		"""
	elif 'mp4star' in str(url) or 'justmp4' in str(url):
		final = mp4star(url) 
	elif "vidup" in str(url):
		m = re.findall('http://[^"]*&bg',url)
		m1 = re.sub('&bg*','',m[0])
		final = simplyfind(m1)
	elif 'uploadcrazy' in str(url):
		print('------Inside Uploadcrazy----')
		content = ccurlNew(url)
		#print(content+'\n')
		print('-------------uploadcrazy---------')
		m = re.findall('file: "http[^"]*uploadcrazy.net[^"]*mp4[^"]*',content)
		if m:
			final = re.sub('file: "','',m[0])
		else:
			final = ""
	
	elif "yourupload" in str(url):
			i = url.replace(r'#038;','')
			#content = subprocess.check_output(["curl","-L","-A",hdr,i])
			content = ccurl(i,'')
			m = re.findall("file: 'http://[^']*video.mp4",content)
			print(m)
			if m:
				url = re.sub("file: '","",m[0])
			else:
				url = ""
				print("File Does Not exist")
			print(url)
			#content = (subprocess.check_output(["curl","-L","-I","-A",hdr,"-e",i,url]))
			content = ccurlNew(url+'#'+'-Ie'+'#'+i)
			if "Location:" in content:
				m = re.findall('Location: [^\n]*',content)
				found = re.sub('Location: |\r','',m[-1])
				print(found)
				url = found
			return url
	elif "vidkai" in str(url):
		content = ccurl(url,'')
		#print(content
		soup = BeautifulSoup(content)
		
		src = soup.find('source')['src']
		if src:
			#content = (subprocess.check_output(['curl','-I','-L','-A',hdr,src]))
			#print(content
			content = ccurlNew(src+'#'+'-I')
			
			if "Location:" in content:
				m = re.findall('Location: [^\n]*',content)
				final = re.sub('Location: |\r','',m[-1])
				print(final)
			else:
				final = ""
	
	elif "uploadc" in str(url):
		content = ccurl(url,'')
		replc = {' ':'%20', '[':'%5B', ']':'%5D','!':'%21'}
		m = re.findall("[']http://[^']*.mp4",content)
		print(m)
		if m:
			#final = replace_all(m[0], replc)
			final = str(urllib.parse.unquote(m[0]))
			final = re.sub("[']",'',final)
			final = final + "?start=0"
			print(final)
	return final

def mp4star(url):
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0"
	
	global qualityVideo
	m = []
	#content = (subprocess.check_output(["curl","-L","-I","-A",hdr,url]))
	content = ccurlNew(url+'#'+'-I')
	found = ""
	if isinstance(content,bytes):
		print("I'm byte")
		content = str((content).decode('utf-8'))
	else:
		print(type(content))
		content = str(content)
		print("I'm unicode")
	if "Location:" in content:
		m = re.findall('Location: [^\n]*',content)
		found = re.sub('Location: |\r','',m[-1])
		print(found)
	if found:
		#content = ccurl(found,'')
		#content = (subprocess.check_output(["curl","-A",hdr,found]))
		content = ccurlNew(found)
		
		m = re.findall('value="[^"]*',content)
	
		value = re.sub('value="',"",m[0])
		#print(value
		
		#content = (subprocess.check_output(["curl","-A",hdr,'-d','id='+'"'+value+'"',found]))
		content = ccurl(found,value)
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
		#content = ccurl(found,value)
	else:
		content = ccurl(url,'')

		m = re.findall('value="[^"]*',content)
	
		value = re.sub('value="',"",m[0])
		#print(value
		
		content = ccurl(url,value)
		
	#print(content
	#m = re.findall('https[^"]*googleusercontent[^"]*',content)
	if 'mp4star' in url:
		m = re.findall('https[^"]*redirector[^"]*',content)
	else:
		m = re.findall("file: 'http[^']*",content)
		n = []
		for i in m:
			i = i.replace("file: '",'')
			n.append(i)
		m[:]=[]
		m = n
	print(m)
	if m:
		#content = ccurl(m[0],"")
		if qualityVideo == "sd":
			#content = (subprocess.check_output(["curl","-L","-I","-A",hdr,m[0]]))
			content = ccurlNew(m[0]+'#'+'-I')
		else:
			#content = (subprocess.check_output(["curl","-L","-I","-A",hdr,m[-1]]))
			content = ccurlNew(m[-1]+'#'+'-I')
		
		if "Location:" in content:
			m = re.findall('Location: [^\n]*',content)
			found = re.sub('Location: |\r','',m[-1])
			print(found)
	else:
		url1 = mp4starUrl(content,'mp4star')
		print(url1,'**********')
		content = ccurlNew(url1+'#'+'-I')
		if "Location:" in content:
			m = re.findall('Location: [^\n]*',content)
			found = re.sub('Location: |\r','',m[-1])
			print(found)
	url = str(urllib.parse.unquote(found))
	return url


def mp4starUrl(content,site):
	
	global qualityVideo
	soup = BeautifulSoup(content,'lxml')
	m = soup.findAll('script,{"type":"text/javascript"}')
	if not m:
		m = soup.findAll('script')
	for i in m:
		if site == 'myvidstream':
			if 'eval(' in i.text and 'myvidstream' in i.text and ('https' in i.text or 'http' in i.text):
				print(i.text)
				content = i.text
				break
		else:
			if 'eval(' in i.text and ('https' in i.text or 'http' in i.text):
				print(i.text)
				content = i.text
				break
				
	print("-------------------------------------------")
	#print(content)
	print("-------------------------------------------")
	m = re.findall("'[^']*",content)
	#print(m)

	for i in m:
		if '|' in i and ('https' in i or 'http' in i):
			i = i.replace("'",'')
			print(i)
			t = i
			print('\n****')
	m = t.split('|')
	#print(m)
	j = 0
	k = 'a'
	l = 'A'
	print(chr(ord(k)+1))
	arr = ['0','1','2','3','4','5','6','7','8','9']

	for i in range(26):
		arr.append(chr(ord(k)))
		k = chr(ord(k)+1)
		
	for i in range(26):
		arr.append(chr(ord(l)))
		l = chr(ord(l)+1)
	print(arr)

	length = len(arr)
	k = arr[0]
	l = arr[0]
	j = 0
	n = 0
	p = 0
	d = []
	k = 100
	d1 = []
	for i in range(len(m)):
		if not(m[i]):
			k = k+1
		if i%length == 0 and i:
			p = p+1
			n = 0
			j = p
		if p == 0:
			if not m[i]:
				r = (k,arr[j])
				r1 = (arr[j],k)
			else:
				r = (m[i],arr[j])
				r1 = (arr[j],m[i])
			j = j+1
		else:
			if not m[i]:
				r = (k,arr[j])
				r1 = (arr[j],k)
			else:
				r = (m[i],arr[j]+arr[n])
				r1 = (arr[j]+arr[n],m[i])
			n = n+1
		d.append(r)
		d1.append(r1)
	m = dict(d)
	di = dict(d1)
	print(di)
	#print(di)
	if site == 'mp4star':
		n = m['https']
		v = m['file']
		n1 = m['http']
		o = re.findall(v+"[^:]*:[^']"+n1+"[^']*",content)
		print(o)
		if o:
			if len(o) == 1:
				u1 = o[0]
			else:
				if qualityVideo == 'sd':
					u1 = o[0]
				else:
					u1 = o[-1]
			print(o)
			u = re.sub(v+'[^:]*:','',o[0])
		else:
			print(v,n)
			o = re.findall(v+"[^:]*:[^']'"+n+"[^']*",content)
			print(o)
			if o:
				if len(o) == 1:
					u1 = o[0]
				else:
					if qualityVideo == 'sd':
						u1 = o[0]
					else:
						u1 = o[-1]
				u = re.sub(v+"[^']*",'',u1)
				u = u.replace("'",'')
	
	
	elif site == 'myvidstream':
		v = m['file']
		n1 = m['http']
		o = re.findall("'"+v+'[^)]*',content)
		print(o)
		if o:
			print(o)
			u = re.sub("'"+v+'[^,]*','',o[0])
			u = u.replace("'",'')
			u = u.replace(",",'')
	else:
		n = m['https']
		v = m['url']
		n1 = m['http']
		o = re.findall('"'+v+'[^:]*:'+'"'+n1+'[^"]*',content)
		if o:
			print(o)
			u = re.sub('"'+v+'[^:]*:','',o[0])
		else:
			o = re.findall('"'+v+'[^:]*:'+'"'+n+'[^"]*',content)
			if o:
				print(o)
				u = re.sub('"'+v+'[^:]*:','',o[0])
	
	u = u.replace('\\','')
	
	#u = re.sub('["?"]|"','',u)
	print(u)
	r = re.findall('[0-9a-zA-Z][^\.|\%|\/|\-|\=|\:|\?|\&]*',u)
	print(r)
	url = ""
	token = ''
	found = False
	special_arr = ['.','%','-','=','/','?',':','&']
	i = 0
	token_index = 0
	l = 0
	#print(di['c'])
	while (i < len(u)):
		#print(i)
		token = ""
		found = False
		#print(url)
		if u[i] in special_arr:
			url = url+u[i]
		else:
			j = i
			while(j <= len(u)):
				token = token + u[j]
				if token in r:
					#print(token)
					found = True
					try:
						url = url+di[token]
					except:
						url = url+token
					token_index = j+1
					break
				j = j+1
		
		if found:
			i = token_index
		else:
			i = i+1
		l = l+1
		if l > 200:
			break
		print(l)
	print(url)
	url = re.sub('"','',url)
	url = re.sub("'",'',url)
	u = urllib.parse.unquote(url)
	print(u)
	return(u)

def uploadcrazy(url):
	content = ccurl(url,"")
	m = re.findall('file: "http[^"]*uploadcrazy.net[^"]*mp4[^"]*',content)
	if m:
		url = re.sub('file: "','',m[0])
	else:
		url = ""
	return url
	
	
class DubbedAnime():
	def __init__(self):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		
	def getOptions(self):
			criteria = ['Cartoon','CartoonMax','Movies','Dubcrazy','Animetycoon','Cartoon-World','AnimeStatic','AniDub']
			return criteria
	def getContent(self,content):
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
	def getFinalUrl(self,siteName,name,epn,mirrorNo,quality):
		global qualityVideo
		qualityVideo = quality
		final = ''
		if siteName == "Cartoon-World" or siteName == "Cartoon" or siteName == "Movies":
				
				url = "http://www.cartoon-world.tv/" + epn + "/"
				
				
				content = ccurl(url,"")
				print(url)
				m = []
				soup = BeautifulSoup(content)
				link = soup.findAll('iframe')
				print(link)
				for i in link:
						if 'vidcrazy' in i['src'] or 'uploadcrazy' in i['src'] or 'mp4star' in i['src'] or 'justmp4' in i['src'] or 'gotvb8' in i['src'] or 'vidkai' in i['src']:
								m.append(i['src'])
				print(m)
				length = len(m)
				j = 1
				while (j <= length):		
						mirrorNo = mirrorNo - 1
						msg = "Total " + str(len(m)) + " Mirrors, Selecting Mirror "+str(mirrorNo + 1)
						subprocess.Popen(["notify-send",msg])
						src = m[mirrorNo]
						print(src)
						if 'vidcrazy' in src or 'uploadcrazy' in src:
							final = uploadcrazy(src)
						elif 'vidkai' in src:
							final = findurl(src)
						else:
							final = mp4star(src)
						if final:
							break
						j = j + 1
						mirrorNo = j	
		elif siteName == "Animetycoon":
				
				url = "http://www.animetycoon.net/" + epn + "/"
				content = ccurl(url,"")
				print(url)
				final = ""
				m = re.findall('http://[^"]*uploadcrazy[^"]*|http://[^"]*vidkai[^"]*|http://[^"]*justmp4[^"]*|http://[^"]*mp4star[^"]*',content)
				print(m)
				if len(m) == 1:
					final = findurl(m[0])
				else:
					mirrorNo = mirrorNo - 1
					print(m[mirrorNo])
					if mirrorNo < len(m):
						print(m[mirrorNo],'---',len(m))
						final = findurl(m[mirrorNo])
				
				
			
				
		elif siteName == "Dubcrazy":
				url = "http://www.dubbedanimeonline.pw/" + epn + "/"
				content = ccurl(url,"")
				print(url)
				m = []
				n =[]
				soup = BeautifulSoup(content)
				m = re.findall('http://[^"]*embed[^"]*',content)
				if m:
					content = ccurl(m[0],"")
					#n = re.findall('https://redirector[^"]*',content)
					#print(n
					soup = BeautifulSoup(content)
					link = soup.find('video')
					link1 = link.findAll('source')
					for i in link1:
						n.append(i['src'])
					if n:
						if len(n) == 1:
							src = n[0]
						else:
							
							if qualityVideo == 'hd':
								src = n[0]
							else:
								src = n[-1]
						#content = (subprocess.check_output(['curl','-L','-I','-A',self.hdr,src]) )
						#content = self.getContent(content)
						content = ccurlNew(src+'#'+'-I')
						t = re.findall('https[^\n]*', content)
						#print(m
						if m:
							#print(m
							final = t[0]
							final = re.sub('\r', '', final)
		elif siteName == "AniDub":
				url = "http://www.watchcartoononline.com/" + epn
				print(url)
				content = ccurl(url,"")
				m = re.findall('["]http://[^"]*embed[^"]*',content)
				print(m)
				n = []
				for i in m:
					j= i[1:]
					print(j)
					replc = {' ':'%20', '[':'%5B', ']':'%5D','!':'%21'}
					#j = replace_all(j, replc)
					j = str(urllib.parse.unquote(j))
					n.append(j)
				print(n)
				post = 'confirm="Click Here to Watch Free!!"'
				for i in n:
					#content = (subprocess.check_output(['curl','-d',post,i]))
					#content = self.getContent(content)
					content = ccurlNew(i+'#'+'-d'+'#'+post)
					print(content)
					m = re.findall('file:[^"]*"http[^"]*',content)
					if m:
						final1 = re.findall('http://[^"]*',m[0])
						if final1:
							print(final1[0])
							k = final1[0]
							replc = {' ':'%20', '[':'%5B', ']':'%5D','!':'%21'}
							#k = replace_all(k, replc)
							#k = str(urllib.parse.unquote(k))
							#k = re.sub(' ','%20',k)
							k = re.sub('\n','',k)
							#content = (subprocess.check_output(['curl','-L',"-I",k]))
							#content = self.getContent(content)
							content = ccurlNew(k+'#'+'-I')
							print('----------------',content,'-------------------')
							
							n = re.findall('Location: [^\n]*',content)
							final = re.sub('Location: |\r','',n[-1])
							print(final)
							
							
							#final = replace_all(n[0], replc)
							#final = str(urllib.parse.unquote(n[0]))
							#final = re.sub('\r|\n','',n[0])
							final = re.sub(' ','%20',final)
							if final:
								break
		elif siteName == "AnimeStatic":
				url = "http://www.animestatic.co/" + epn + '/'
				print(url)
				content = ccurl(url,"")
				m = re.findall('["]http://[^"]*embed[^"]*',content)
				print(m)
				n = []
				for i in m:
					j= i[1:]
					n.append(j)
				print(n)
				mirrorNo = mirrorNo -1 
				for i in n:
					url = n[mirrorNo]
					final = findurl(url)
					if final:
						break
					mirrorNo = mirrorNo + 1
		elif siteName == "CartoonMax":
			final = ''
			url = "http://gogocartoon.us/" + epn
			print(url,'----------')
			content = ccurl(url,"")
			soup = BeautifulSoup(content,'lxml')
			#link = soup.find('div',{'class':'anime_video_body_watch'})
			#if not link:
			link = soup.find('div',{'class':'anime_video_body_watch_items_2'})
			sd = ''
			hd = ''
			sd480 = ''
			if link:
				link2 = link.find('iframe')['src']
				if link2:
					if 'src' in str(link2):
						link1 = link2['src']
						print(link1,'---')
						if link1:
							content1 = ccurl(link1,'')
							soup = BeautifulSoup(content1,'lxml')
							links = soup.findAll('source')
							for i in links:
								if 'src' in str(i):
									j = i['src']
									if 'itag=22' in j:
										hd = j
									elif 'itag=18' in j:
										sd = j
									elif 'itag=59' in j:
										sd480 = j
									elif 'itag=43' in j:
										sd = j
				print (sd)
				print(sd480)
				print(hd)
				
			if not sd and not hd and not sd480:
				soup = BeautifulSoup(content,'lxml')
				link = soup.find('select',{'id':'selectQuality'})
				if link:
					link1 = link.findAll('option')
					for i in link1:
						j = i['value']
						if 'itag=18' in j:
							sd = j
						elif 'itag=22' in j:
							hd = j
						elif 'itag=37' in j:
							full_hd = j
						elif '=m18' in j:
							sd = j
						elif '=m22' in j:
							hd = j
							
						
			final_cnt = 0
			final_quality = ''
			if sd:
				final_cnt = final_cnt+1
				final_quality = final_quality + 'SD '
			if sd480:
				final_cnt = final_cnt+1
				final_quality = final_quality + '480P '
			if hd:
				final_cnt = final_cnt+1
				final_quality = final_quality + 'HD '
				
			msg = "Total " + str(final_cnt) + " Quality Video Available "+final_quality+" Selecting "+str(quality) + " Quality"
			subprocess.Popen(["notify-send",msg])
			
			if quality == "sd":
				final_q = sd
			elif quality == 'sd480p':
				final_q = sd480
			elif quality == 'hd':
				final_q = hd
			if not final_q and sd:
				final_q = sd
			print(final_q)
			if final_q:
				
				#content = (subprocess.check_output(['curl','-L','-I','-A',self.hdr,final_q]))
				#content = self.getContent(content)
				content = ccurlNew(final_q+'#'+'-I')
				print(content)
				m = re.findall('Location: https[^\n]*', content)
				#print(m
				if m:
					#print(m
					final = m[0]
					final = re.sub('Location: |\r', '', final)
			else:
				final = ''
		return final
		
	def getCompleteList(self,siteName,category,opt):
		content = ""
		
		if siteName == "Cartoon-World":
			
			url = "http://www.cartoon-world.tv/anime-list/"
		elif siteName == "Movies":
				url = "http://www.cartoon-world.tv/movie-list/"
		elif siteName == "Cartoon":
				url = "http://www.cartoon-world.tv/cartoon-list/"
		elif siteName == "Dubcrazy":
			if category == "Movies":
				url = "http://www.dubbedanimeonline.pw/dubbed-movies-list/"
			else:
				url = "http://www.dubbedanimeonline.pw/dubbed-anime-list/"
		elif siteName == "Animetycoon":
			url = "http://www.animetycoon.net/full-index/"
		elif siteName == "AniDub":
			if category == "Movies":
				url = "http://www.watchcartoononline.com/movie-list"
			else:
				url = "http://www.watchcartoononline.com/dubbed-anime-list" 
				urlc = "http://www.watchcartoononline.com/cartoon-list"
		elif siteName == "AnimeStatic":
			if category == "Movies":
				url = "http://www.animestatic.co/anime-movies/"
			else:
				url = "http://www.animestatic.co/anime-list/"
		elif siteName == "CartoonMax":
			url = "http://gogocartoon.us/cartoon-list.html"
		print(url)
		if siteName == "Animetycoon" or siteName == "AnimeStatic":
			#hdrs = {'user-agent':self.hdr}
			#req = requests.get(url,headers=hdrs)
			#content = str(req.text)
			content = ccurlNew(url)
		else:
			content = ccurl(url,"")
		soup = BeautifulSoup(content)
		if siteName == "Cartoon-World" or siteName == "Movies" or siteName == "Cartoon" or siteName == "Dubcrazy" or siteName == "Animetycoon":
				if siteName == "Cartoon-World" or siteName == "Cartoon" or siteName == "Animetycoon" or siteName == "Movies":
					m = re.findall('watch/[^"]*', content)
				else:
					m = re.findall('view/[^"]*', content)
				#m = list(set(m))
				#m.sort()
				j=0
				for i in m:
					if siteName == "Cartoon-World" or siteName == "Cartoon" or siteName == "Animetycoon" or siteName == "Movies":
						i = re.sub("watch/","",i)
					else:
						i = re.sub("view/","",i)
					i = re.sub("/","",i)
					m[j] = i
					j = j+1
				if opt == 7:
					strnamr = str(name)
					s = []
					for i in m:
						m = re.search('[^"]*'+strname+'[^"]*',i)
						if m:
							found = m.group(0)
							s.append(found)
					m = s
		elif siteName == "AniDub" or siteName == "AnimeStatic":
				m = []
				if siteName == "AniDub" and category != "Movies":
					content1 = ccurl(urlc,"")
					soup1 = BeautifulSoup(content1)
					link1 = soup1.findAll('div',{'id':'ddmcc_container'})
					link2 = soup.findAll('div',{'id':'ddmcc_container'})
					link = link1 + link2
				else:
					link = soup.findAll('div',{'id':'ddmcc_container'})
				for i in link:
					a = i.findAll('a')
					for j in a:
						if 'href' in str(j):
							k=(j['href']).split('/')
							if siteName == "AniDub":
								if k[-1]:
									m.append(k[-1])
							else:
								if k[-2]:
									m.append(k[-2])
		elif siteName == "CartoonMax":
			m = []
			soup = BeautifulSoup(content)
			link = soup.findAll('div',{'class':'anime_list_body'})
			#print(link
			for i in link:
				j = i.findAll('a')
				for k in j:
					tmp = k['href'].split('/')[-1]
					if tmp :
						m.append(tmp)

		if opt == "Random":
			m = random.sample(m, len(m))
		return m
	
	def getEpnList(self,siteName,name,category):
		if siteName == "Cartoon-World" or siteName == "Cartoon" or siteName == "Movies":
			base = "http://www.cartoon-world.tv/"
			url = base+ "watch/" + name+"/"
		elif siteName == "Dubcrazy":
			base = "http://www.dubbedanimeonline.pw/"
			url = base+ "view/" + name+"/" 
		elif siteName == "Animetycoon":
			base = "http://www.animetycoon.net/"
			url = base+ "watch/" + name+"/"
		elif siteName == "AniDub":
			base = "http://www.watchcartoononline.com/"
			if category == "Movie":
					url = "http://www.watchcartoononline.com/" + name
			else:
					url = "http://www.watchcartoononline.com/anime/" + name
		elif siteName == "AnimeStatic":
			base = "http://www.animestatic.co/"
			if category == "Movies": 
				url = "http://www.animestatic.co/" + name + '/'
			else:
				url = "http://www.animestatic.co/anime/" + name + '/'
		elif siteName == "CartoonMax":
			url = "http://gogocartoon.us/category/" + name 
			base = "http://gogocartoon.us/"
			
		
		print(url)
		#if base_url == 0:
		#content = subprocess.check_output(['curl','-A',hdr,url]) 
		#else:
		#	content = ccurl(url,"no_redir")
		if siteName == "Cartoon-World" or siteName == "Cartoon" or siteName == "Movies":
			#content = (subprocess.check_output(['curl','-A',self.hdr,url]))
			#content = self.getContent(content)
			content = ccurlNew(url+'#'+'-L')
		else:
			"""
			hdrs = {'user-agent':self.hdr}
			req = requests.get(url,headers=hdrs)
			summary = ""
			content = req.text
			"""
			#content = (subprocess.check_output(['curl','-A',self.hdr,url]))
			#content = self.getContent(content)
			content = content = ccurlNew(url+'#'+'-L')
		soup = BeautifulSoup(content)
		if siteName == "Cartoon-World" or siteName == "Cartoon" or siteName == "Movies":
	
				link1 = soup.findAll('div',{'class':'ani-row'})
				print(link1)
				try:
					img1 = link1[0].find('img',{'class':'anime'})
					print(img1)
					img = img1['src']
					if not "http://" in img:
						img2 = re.findall('/images/[^"]*',img)
						img = "http://www.cartoon-world.tv"+img2[0]
						print(img)
					
					picn = "/tmp/AnimeWatch/"+name+'.jpg'
					if not os.path.isfile(picn) and img:
						#subprocess.call(["curl","-A",self.hdr,"-L","-o",picn,img])
						ccurlNew(img+'#'+'-o'+'#'+picn)
				except:
					picn = "No.jpg"
					img = ""
				try:
					summary=str(link1[1])
				
					summary = re.sub('</table>','</table><div class="desc">',summary)
					summary = re.sub('</div>','</div></div>',summary)
					print(summary)
					soup = BeautifulSoup(summary)

					info = soup.findAll('td',{'class':'ani-table-ans'})

					summary = info[0].text+'\nType: '+ info[1].text+ '\nAired: ' + info[2].text + '\nGenre: ' + info[3].text+soup.find('div',{'class':'desc'}).text 
				except:
					summary = "No Summary Available"
				
		
		elif siteName == "AniDub" or siteName == "AnimeStatic":
			m = []
			if category == "Movies":
				m.append(name)
			else:
				if siteName == "AniDub":
					link = soup.findAll('div',{'class':'menustyle'})
				else:
					link = soup.findAll('ul',{ 'class':'eps eps-list'})
				for i in link:
					a = i.findAll('a')
					for j in a:
							k=(j['href']).split('/')
							if siteName == "AniDub":
								m.append(k[-1])
							else:
								m.append(k[-2])
		
			if siteName == "AniDub":
				img = []
				link = soup.findAll('div',{'class':'katcont'})		 	
				for i in link:
					summary = re.sub('\n','',i.text)
				img = re.findall('http[^"]*.jpg',content)
				
			elif siteName == "AnimeStatic":
				link = soup.find("div",{ "class":"deskripsi"})
				summary = ""
				img = []
				if link:
					
					sumr= link.find('p')
					summary = sumr.text
					#summary = re.sub('Genres[^\n]*\n','Genres : ',summary)
					#summary = re.sub('Title[^\n]*\n','Title : ',summary)
					#summary = re.sub('Rating[^\n]*\n','Rating : ',summary)
					#summary = re.sub('[)]','',summary)
					#summary = re.sub('[,][^"]\n','\n',summary)
				link = soup.find('div',{'class':'imganime'})
				if link:
					img1 = link.find('img')
					if img1:
						img.append(img1['src'])
					
			picn = "/tmp/AnimeWatch/" + name + ".jpg"
			if not os.path.isfile(picn) and img:
				#subprocess.call(["curl","-A",self.hdr,"-L","-o",picn,img[0]])
				ccurlNew(img[0]+'#'+'-o'+'#'+picn)
		elif siteName == "Animetycoon":
			img =[]
			#text = str(text)
			#print(text
			try:
				text = soup.find('article')
				text1 = text.find('p')
				summary = text1.text
				try:
					img1 = text.find('img')['src']
					if 'http' not in img1:
						img1 = 'http:' + img1
					img.append(img1)
				except:
					img = re.findall('//[^"]*posters/[^"]*.jpg',content)
					img[0] = "http:" + img[0]
				picn = "/tmp/AnimeWatch/" + name + ".jpg"
				if not os.path.isfile(picn):
					#subprocess.call(["curl","-L","-o",picn,img[0]])
					ccurlNew(img[0]+'#'+'-o'+'#'+picn)
				
			except: 
				summary = "No Summary Available"
				picn = "No"
		elif siteName == "CartoonMax":
				m = []
				link = soup.find('ul',{'id':'episode_page'})
				if link:
					epstart = int(link.find('a')['ep_start'])
					epend = int(link.find('a')['ep_end'])
					if not epstart:
						epstart = 0
					if not epend:
						epend = 0
					i = epstart
					while(i<=epend):
						ep_n = name+"-episode-"+str(i)
						m.append(ep_n)
						i = i+1	
				else:
					link = soup.find('div',{'class':'anime_info_episodes'})
				
					link1 = link.findAll('a')
					for i in link1:
						k = i['href'].split('/')[-1]
						m.append(k)
				summary = ""
				link = soup.find('div',{ 'class':'anime_info_body_bg'})
				img = []
				summary = link.text
			
				img_src = link.find('img')['src']
				if ' ' in img_src:
					img_src = re.sub(" ","%20",img_src)
				print(img_src)
				if img_src:
					img.append(img_src)
				picn = "/tmp/AnimeWatch/" + name + ".jpg"
				if not os.path.isfile(picn):
					#subprocess.call(["curl","-A",self.hdr,"-L","-o",picn,img[0]])
					ccurlNew(img[0]+'#'+'-o'+'#'+picn)
		elif siteName == "Dubcrazy":
			
					
			try:
				summary = ""
				link = soup.findAll('div',{'class':'main_container'})
				#print(link
				for i in link:
					j = i.findAll('p')
					for k in j:
						summary = k.text
				
				img = "http://www.dubbedanimeonline.pw/images/" + name+".jpg"
				print(img)
				picn = "/tmp/AnimeWatch/" + name + ".jpg"
				if not os.path.isfile(picn):
					#subprocess.call(["curl","-A",self.hdr,"-L","-o",picn,img])
					ccurlNew(img+'#'+'-o'+'#'+picn)
			except:
				summary = "No Summary Available"
				picn = "No"
			#print(img
		if siteName != "AniDub" and siteName != "CartoonMax": 
			fi = base + name+ '[^"]*/'
			m = re.findall(fi, content)
			j=0
			for i in m:
				i = re.sub(base,"",i)
				m[j] = i[:-1]
				j = j + 1
		m=naturallysorted(m)
		m.append(picn)
		m.append(summary)
		return m

