import sys
import urllib
import pycurl
from io import StringIO,BytesIO
import re
import subprocess
from subprocess import check_output
import random
from bs4 import BeautifulSoup
import os.path
import base64
try:
	from selenium import webdriver
except:
	pass
import requests
import time
from base64 import b64decode
import random
try:
	import jsbeautifier.unpackers.packer as packer
except:
	pass



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
		
def unshorten_url(url):
		content = (ccurl(url))
			#print(content
		try:
			
			html = content
			ysmm = re.findall(r"var ysmm =.*\;?", html)

			if len(ysmm) > 0:
				str_code = re.sub(r'var ysmm \= \'|\'\;', '', ysmm[0])
				j = 0
				l = ''
				r = ''
				for i in str_code:
					if j < len(str_code):
						l = l + str_code[j]
					
					j = j+2
				j = len(str_code) - 1
				for i in str_code:
					if j >=0 :
						r = r + str_code[j]
					
					j = j-2

				final_decode_url = b64decode(l.encode() + r.encode())[2:].decode()

				if re.search(r'go\.php\?u\=', final_decode_url):
					final_decode_url = b64decode(re.sub(r'(.*?)u=', '',final_decode_url)).decode()
		
				print(final_decode_url)
				return final_decode_url
				
			else:
				return url

		except Exception as e:
			shrink_link = url
		return shrink_link

def cloudfare(url):
			hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0"
			home1 = expanduser("~")
			#home1 = "/usr/local/share"
			pluginDir = home1+"/.config/AnimeWatch/src/Plugins"
			if not os.path.isfile('/tmp/AnimeWatch/klm.txt'):
					temp = subprocess.check_output(["phantomjs", pluginDir+"/ac.js",url])
					temp = getContentUnicode(temp)
					#print(temp
					p = re.findall('{[^}]*}',temp)
					for i in p:
						if "_cfduid" in i:
							cfd = i
						elif "cf_clearance" in i:
							cfc = i
		
					n = re.findall('value": "[^"]*|expiry": [^,]*',cfc)
					e = re.findall('value": "[^"]*|expiry": [^,]*',cfd)
					j = 0
					for i in n:
						n[j] = re.sub('value": "|expiry": ',"",i)
						j = j+1
					j = 0
					for i in e:
						e[j] = re.sub('value": "|expiry": ',"",i)
						j = j+1
					#print(n
					cookiefile = ".acb.im	TRUE	/	FALSE	"+str(e[0])+"	__cfduid	" + str(e[1]) + "\n" + ".acb.im	TRUE	/	FALSE	"+str(n[0])+"	cf_clearance	" + str(n[1])
					#print(cookiefile
					f = open('/tmp/AnimeWatch/klm.txt', 'w')
					f.write(cookiefile)
					f.close()
					cfc_val = n[1]
					cfd_val = e[1]
					#print(cfc_val
					#print(cfd_val
		
			content = (subprocess.check_output(["curl","-b","/tmp/AnimeWatch/klm.txt",'-A',hdr,url]))
			content = getContentUnicode(content)
			#print(content
			try:
				
				html = content
				ysmm = re.findall(r"var ysmm =.*\;?", html)

				if len(ysmm) > 0:
					str_code = re.sub(r'var ysmm \= \'|\'\;', '', ysmm[0])
					j = 0
					l = ''
					r = ''
					for i in str_code:
						if j < len(str_code):
							l = l + str_code[j]
						
						j = j+2
					j = len(str_code) - 1
					for i in str_code:
						if j >=0 :
							r = r + str_code[j]
						
						j = j-2

					final_decode_url = b64decode(l.encode() + r.encode())[2:].decode()

					if re.search(r'go\.php\?u\=', final_decode_url):
						final_decode_url = b64decode(re.sub(r'(.*?)u=', '',final_decode_url)).decode()
			
					print(final_decode_url)
					return final_decode_url
				
				else:
					return url

			except Exception as e:
				return url



def cloudfareUrl(url):
			hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0"
			home1 = expanduser("~")
			#home1 = "/usr/local/share"
			pluginDir = home1+"/.config/AnimeWatch/src/Plugins"
			temp = subprocess.check_output(["phantomjs", pluginDir+"/ma.js",url])
			temp = getContentUnicode(temp)
			#print(temp
			p = re.findall('{[^}]*}',temp)
			for i in p:
				if "_cfduid" in i:
					cfd = i
				elif "cf_clearance" in i:
					cfc = i

			n = re.findall('value": "[^"]*|expiry": [^,]*',cfc)
			e = re.findall('value": "[^"]*|expiry": [^,]*',cfd)
			j = 0
			for i in n:
				n[j] = re.sub('value": "|expiry": ',"",i)
				j = j+1
			j = 0
			for i in e:
				e[j] = re.sub('value": "|expiry": ',"",i)
				j = j+1
			#print(n
			cookiefile = ".masterani.me	TRUE	/	FALSE	"+str(e[0])+"	__cfduid	" + str(e[1]) + "\n" + ".masterani.me	TRUE	/	FALSE	"+str(n[0])+"	cf_clearance	" + str(n[1])
			print(cookiefile)
			f = open('/tmp/AnimeWatch/anime.txt', 'w')
			f.write(cookiefile)
			f.close()
			cfc_val = n[1]
			cfd_val = e[1]
			#print(cfc_val
			#print(cfd_val
			#content = subprocess.check_output(["curl","-b","/tmp/AnimeWatch/anime.txt",'-A',hdr,url])
			#return content
	
def shrink_url(url):
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0"
	if "linkshrink" in url:
		content = subprocess.check_output(['curl','-c','/tmp/AnimeWatch/link.txt','-b','/tmp/AnimeWatch/link.txt','-I','-L',url])
		content = getContentUnicode(content)
		content = subprocess.check_output(['curl','-c','/tmp/AnimeWatch/link.txt','-b','/tmp/AnimeWatch/link.txt','-L',url])
		content = getContentUnicode(content)
		soup = BeautifulSoup(content)
		shrink = soup.find('a',{'class':'bt'})
		shrink_link = shrink['href']
	elif "sh.st" in url:
		shrink_link = url
	elif "adf.ly" in url:
		url = re.sub('http:','https:',url)
		
		shrink_link=unshorten_url(url)
		print(shrink_link)
	
	elif "linkbucks" in url or "bc.vc" in url:
		shrink_link = url
	elif "adf.acb.im" in url:
		#shrink_link=str(cloudfare(url))
		shrink_link=str(unshorten_url(url))
	elif "mt0.org" in url:
		try:
			content = (subprocess.check_output(['curl','-A',hdr,url]))
			content = getContentUnicode(content)
			print(content)
			url = (re.search('http[^"]*index.php[^"]*',str(content))).group()
			content = (subprocess.check_output(['curl','-A',hdr,url]))
			content = getContentUnicode(content)
			print(content)
			url = (re.search('http[^"]*index.php[^"]*',str(content))).group()
		except:
			pass
		content = (subprocess.check_output(['curl','-A',hdr,'-I','-L',url]))
		content = getContentUnicode(content)
		m = re.findall('Location: [^\n]*', content)
		#print(m
		if m:
			#print(m
			final1 = m[0]
			final1 = re.sub('Location: |\r', '', final1)
			shrink_link = final1
		else:
			shrink_link = ""
	else:
		url = re.sub('http:','https:',url)
		shrink_link = unshorten_url(url)
		print(shrink_link)
	
	return shrink_link

def naturallysorted(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

def progressBar(cmd):
	
	content = subprocess.check_output(cmd)
	content = getContentUnicode(content)
	
	return (content)

def ccurl(url):
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0"
	
	
	content = (subprocess.check_output(['curl','-L','-A',hdr,url]))
	content = getContentUnicode(content)
	
	return content

def ccurl_setcookie(url):
	
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0"
	c = pycurl.Curl()
	c.setopt(c.FOLLOWLOCATION, True)
	c.setopt(c.USERAGENT, hdr)
	c.setopt(c.COOKIEJAR, '/tmp/AnimeWatch/cookie.txt')
	url = str(url)
	c.setopt(c.URL, url)
	storage = BytesIO()
	c.setopt(c.WRITEFUNCTION, storage.write)
	c.perform()
	c.close()
	content = storage.getvalue()
	content = getContentUnicode(content)
	
	return (content)

def ccurl_cookie(url):
	
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0"
	c = pycurl.Curl()
	c.setopt(c.FOLLOWLOCATION, True)
	c.setopt(c.USERAGENT, hdr)
	c.setopt(c.COOKIEFILE, '/tmp/AnimeWatch/cookie.txt')
	url = str(url)
	c.setopt(c.URL, url)
	storage = BytesIO()
	c.setopt(c.WRITEFUNCTION, storage.write)
	c.perform()
	c.close()
	content = storage.getvalue()
	content = getContentUnicode(content)
	
	return (content)
	
def ccurlM(url):
	
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0"
	c = pycurl.Curl()
	c.setopt(c.FOLLOWLOCATION, True)
	c.setopt(c.USERAGENT, hdr)
	if os.path.exists('/tmp/AnimeWatch/anime.txt'):
		c.setopt(c.COOKIEFILE, '/tmp/AnimeWatch/anime.txt')
	url = str(url)
	c.setopt(c.URL, url)
	storage = BytesIO()
	c.setopt(c.WRITEFUNCTION, storage.write)
	c.perform()
	c.close()
	content = storage.getvalue()
	content = getContentUnicode(content)
	
	return (content)

def ccurlPost(url,value):
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0"
	
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
	c.setopt(c.WRITEFUNCTION, storage.write)
	c.perform()
	c.close()
	content = storage.getvalue()
	content = getContentUnicode(content)
	
	return (content)

def replace_all(text, di):
	for i, j in di.iteritems():
		text = text.replace(i, j)
	return text
	
def findurl(i):
	hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0"
	found = ""
	print(i)
	global qualityVideo
	if "solidfiles" in i:
			content = (subprocess.check_output(['curl','-L','-A',hdr,i]))
			content = getContentUnicode(content)
			soup = BeautifulSoup(content)
			link = soup.find('div',{'class':'buttons'})
			#link = soup.find('div',{'id':'ddl-row'})
			#print(link
			link1 = link.find('a')
			found = link1['href']
			return found
	elif "mediafire" in i:
			
			
			
			content = (subprocess.check_output(['curl','-L','-A',hdr,i]))
			content = getContentUnicode(content)
			print(content)
			final1 = re.findall('kNO = "[^"]*',content)
			if final1:
				found = re.sub('kNO = "',"",final1[0])
				return found
		
			"""
			content = subprocess.check_output(['plowdown','--skip-final','--printf=FORMAT',i])
			print(content
			final1 = re.findall('File URL: [^\n]*',content)
			if final1:
				found = re.sub('File URL: "',"",final1[0])
				return found
			"""
	elif "tusfiles" in i:
			"""
			plugin_path = os.path.expanduser('~')+"/.config/AnimeWatch/src/Plugins/phantom1.js"
			content = (subprocess.check_output(['phantomjs',plugin_path,i]))
			content = getContentUnicode(content)
			#print(content
			final1 = re.findall('embed id="[^>]*',content)
			if final1:
				found1 = re.findall('src="https[^"]*',final1[0])
				if found1:
					found = re.sub('src="',"",found1[0])
					return found
			"""
			found = ''
			content = ccurl(i)
			soup = BeautifulSoup(content,'lxml')
			link = soup.findAll('textarea')
			print(link)
			k = ''
			for i in link:
				if 'iframe' in str(i).lower():
					j = i.find('iframe')
					if j:
						k = j['src']
					else:
						j = i.find('IFRAME')
						if j:
							k = j['SRC']
			if k:
				content = ccurl(k)
				soup = BeautifulSoup(content,'lxml')
				link = soup.findAll('script',{'type':'text/javascript'})
				for i in link:
					if 'tusfiles' in i.text:
						#print(i.text)
						packed = i.text
				if packed:
					val = packer.unpack(packed)
					print(val)
					soup = BeautifulSoup(val,'lxml')
					link = soup.find('param',{'name':'src'})['value']
					print(link)
					if link:
						found = link
					else:
						found = ''
			return found
	elif "embedupload" in i:
			content = ccurl(i)
			m = re.findall('http://www.embedupload.com/\?MF=[^"]*',content)
			if m:
				content = ccurl(m[0])
				n = re.findall('http://www.mediafire.com/\?[^<]*',content)
				if n:
					#print(n
					final1 = re.sub('\t','',n[0])
					print(final1)
					plugin_path = os.path.expanduser('~')+"/.config/AnimeWatch/src/Plugins/phantom1.js"
					content = (subprocess.check_output(['phantomjs',plugin_path,final1]))
					content = getContentUnicode(content)
					#print(content
					final2 = re.findall('kNO = "[^"]*',content)
					if final2:
						found = re.sub('kNO = "',"",final2[0])
						return found
	elif "mirrorcreator" in i:
		content = (subprocess.check_output(['plowlist',i]))
		content = getContentUnicode(content)
		url = re.findall('http[^"]*solidfiles[^\n]*',content)
		if url:
			content = (subprocess.check_output(['curl','-L','-A',hdr,url[0]]))
			content = getContentUnicode(content)
			soup = BeautifulSoup(content)
			link = soup.find('div',{'class':'btns'})
			#print(link
			link1 = link.find('a')
			found = link1['href']
			return found
	elif "videoweed" in i:
		found = ""
		return found
	elif "videowing" in i or "easyvideo" in i:
		content = ccurl(i)
		soup = BeautifulSoup(content)
		link = soup.findAll('script')
		print(link)
		print(len(link))
		if link:
			val = link[-1].text
			m = re.search('eval\([^\*]*',val)
			val1 = m.group()
			r = packer.unpack(val1)
			print(r	)
			if "videowing" in i:
				r1 = re.findall('"url":"https[^"]*',r)
				print(r1)
				if not r1:
					r1 = re.findall('"url":"http[^"]*',r)
				if r1:
					url = re.sub('"url":"','',r1[0])
					url = str(urllib.parse.unquote(url))
					url = url.replace('\\','')
					print(url)
			elif "easyvideo" in i:
				r1 = re.findall('\{url:"https[^"]*',r)
				print(r1)
				if not r1:
					r1 = re.findall('\{url:"http[^"]*',r)

				if r1:
					url = re.sub('\{url:"','',r1[0])
					url = str(urllib.parse.unquote(url))
					url = url.replace('\\','')
					print(url)
			
			
			
			
			content = (subprocess.check_output(['curl','-L','-I','-A',hdr,url]))
			content = getContentUnicode(content)
			if "Location:" in content:
				m = re.findall('Location: [^\n]*',content)
				found = re.sub('Location: |\r','',m[-1])
			else:
				found = url
		else:
			found = ""
		return found
	elif "myvidstream" in i:
			packed = ''
			final = ""
			content = ccurl(i)
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
			link = re.findall('eval[(][^"]*.split',content)
			print(len(link))
			req = str(link[1])
			print(req)
			m = re.findall('/[a-z]/[^/]/[a-z]',req)
			print(m)
			if m:
				l = m[0].split('/')
				num = l[2]
				print(num)
			i = req.split('|')
			k = 0
			for j in i:
				if "video" == str(j):
					flv = i[k+1]
					if not flv:
						flv = i[k+2]
					if "srv" in flv:
						server = flv
					elif "flvplayer" == flv:
						server = ""
					else:
						server = flv
				if 'mp4' == str(j) or "flv" == str(j):
					icode = i[k+1]
				k = k+1 
			print(str(num))
			print(icode)
			if not server:
				#final = "http://myvidstream.net/files/"+num+"/"+icode+"/video.mp4?start=0"
				final = "http://myvidstream.net:182/d/"+icode+"/video.mp4?start=0"
			else:
				#final = "http://"+server+".myvidstream.net/files/"+num+"/"+icode+"/video.mp4?start=0"
				final = "http://"+server+".myvidstream.net:182/d/"+icode+"/video.mp4"
			print(final)
			"""
			return final
	elif "mp4upload" in i:
			content = ccurl(i)
			if 'mp4upload' in i:
				m = re.findall("'file': 'http://[^']*mp4upload.com[^']*video.mp4",content)
			else:
				m = re.findall("'file': 'http://[^']*video.mp4",content)
			print(m)
			if m:
				url = re.sub("'file': '","",m[0])
			else:
				url = ""
				print("File Does Not exist")
			print(url)
			return url
	elif "uploadcrazy" in i or "vidcrazy" in i:
			content = ccurl(i)
			m = re.findall('file: "http[^"]*uploadcrazy.net[^"]*mp4[^"]*',content)
			if m:
				url = re.sub('file: "','',m[0])
				
			else:
				url = ""
			return url
	elif "yourupload" in i:
			#content = subprocess.check_output(["curl","-L","-A",hdr,i])
			content = ccurl(i)
			m = re.findall("file: 'http://[^']*video.mp4",content)
			print(m)
			if m:
				url = re.sub("file: '","",m[0])
			else:
				url = ""
				print("File Does Not exist")
			print(url)
			content = (subprocess.check_output(["curl","-L","-I","-A",hdr,"-e",i,url]))
			content = getContentUnicode(content)
			if "Location:" in content:
				m = re.findall('Location: [^\n]*',content)
				found = re.sub('Location: |\r','',m[-1])
				print(found)
				url = found
			return url
	elif "mp4star" in i or "justmp4" in i:
			content = (subprocess.check_output(["curl","-L","-I","-A",hdr,i]))
			content = getContentUnicode(content)
			found = ""
			if "Location:" in content:
				m = re.findall('Location: [^\n]*',content)
				found = re.sub('Location: |\r','',m[-1])
				print(found)
			if found:
				content = ccurl(found)
				m = re.findall('value="[^"]*',content)
			
				value = re.sub('value="',"",m[0])
				#print(value
				
				content = ccurlPost(found,value)
			else:
				content = ccurl(i)
	
				m = re.findall('value="[^"]*',content)
			
				value = re.sub('value="',"",m[0])
				#print(value
				
				content = ccurlPost(i,value)
				
			#print(content
			#m = re.findall('https[^"]*googleusercontent[^"]*',content)
			if 'mp4star' in i:
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
					content = (subprocess.check_output(["curl","-L","-I","-A",hdr,m[0]]))
				else:
					content = (subprocess.check_output(["curl","-L","-I","-A",hdr,m[-1]]))
				content = getContentUnicode(content)
				if "Location:" in content:
					m = re.findall('Location: [^\n]*',content)
					found = re.sub('Location: |\r','',m[-1])
					print(found)
				
			url = str(urllib.parse.unquote(found))
			return url
	elif "vidkai" in i:
		#print("*********vid********kai"
		content = ccurl(i)
		#print(content
		soup = BeautifulSoup(content)
		src = soup.find('source')['src']
		
		content = (subprocess.check_output(['curl','-I','-L','-A',hdr,src]))
		content = getContentUnicode(content)
		#print(content
		if "Location:" in content:
			m = re.findall('Location: [^\n]*',content)
			found = re.sub('Location: |\r','',m[-1])
			print(found)
			return found
		else:
			return ""
	elif "arkvid" in i:
		content = ccurl(i)
		soup = BeautifulSoup(content)
		src = soup.find('source')['src']
		if 'http' not in src:
			src = "http:"+src
			print(src)
		return src
		
	elif "videonest" in i:
		
		content = ccurl(i)
		a1 = re.findAll('file:"http[^"]*.mp4',content)
		if a1:
			src = re.sub('file:"','',a1[0])
		else:
			return ""
		content = (subprocess.check_output(['curl','-L','-I','-A',hdr,src]))
		content = getContentUnicode(content)
		if "Location:" in content:
			m = re.findall('Location: [^\n]*',content)
			found = re.sub('Location: |\r','',m[0])
			return found	
				
	elif ("playbb" in i) or ("playpanda" in i) or ("video44" in i):
			content = ccurl(i)
			
			m = re.findall("url: 'http[^']*",content)
			n = re.sub("url: '",'',m[0])
			
			if m:
				#n = re.sub("url: '",'',m[0])
				#print(n
				found = str(urllib.parse.unquote(n))
				print(found)
				content1 = (subprocess.check_output(['curl','-L','-I','-A',hdr,found]))
				content1 = getContentUnicode(content1)
				if "Location:" in content1:
					m = re.findall('Location: [^\n]*',content1)
					found = re.sub('Location: |\r','',m[0])
					print(found)
					return found
				else:
					m1 = re.findall('_url = "http[^"]*',content)
					if m1:
						n1 = re.sub('_url = "','',m1[0])
						found = str(urllib.parse.unquote(n1))
						print(found)
						content2 = (subprocess.check_output(['curl','-L','-I','-A',hdr,found]))
						content2 = getContentUnicode(content2)
						if "Location:" in content2:
							m = re.findall('Location: [^\n]*',content2)
							found = re.sub('Location: |\r','',m[-1])
							print(found)
							return found
	else:
			content = ccurl(i)
			m = re.findall('["]http://[^"]*.mp4[^"]*|["]http://[^"]*.flv[^"]*|["]https://redirector[^"]*|["]https://[^"]*.mp4', content)
			m1 = re.findall("[']http://[^']*.mp4[^']*|[']http://[^']*.flv[^']*|[']https://redirector[^']*|[']https://[^']*.mp4", content)
			print(m)
			if m:
				found = m[0]
				#found = found[1:]
				found = str(urllib.parse.unquote(found))
			elif m1:
				found = m1[0]
				#found = found[1:]
				found = str(urllib.parse.unquote(found))
			else:
				found = ""
				return found
			found = found.replace('"','')
			found = found.replace("'",'')
			print(found)
			try:
				if type(found) is list:
					found1 = found[0]
				else:
					found1 = found
				content = (subprocess.check_output(['curl','-I','-A',hdr,found1]))
				content = getContentUnicode(content)
				if ('video/mp4' in content) or ('video/x-flv' in content):
					return found1
				else:
					
					content = (subprocess.check_output(['curl','-I','-A',hdr,found1]))
					content = getContentUnicode(content)
					m = re.findall('Location: [^\n]*',content)
					found = re.sub('Location: |\r','',m[0])
					content = (subprocess.check_output(['curl','-I','-A',hdr,found]))
					content = getContentUnicode(content)
					if ('video/mp4' in content) or ('video/x-flv' in content):
						return found
					else:
						found =""
						return found
			except:
				return found
	
class SubbedAnime():
	def __init__(self):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
		
	def getOptions(self):
			criteria = ['Anime1','Anime44','AnimePlus','AnimeWow','Animehere','GoodAnime','AnimeNet','AnimeMax','AnimeStream','Animefun','Animegalaxy','Animebox','Anime-Freak','AnimeBaka','AnimeHQ','AnimeSquare','Animeget','AnimeAll','AnimeMix']
			return criteria
			
	def getCompleteList(self,siteName,category,opt):
			
		if siteName == "Anime44": 
			if opt == "Search":
			  url = "http://www.animenova.org/anime/search?key=" + name
			else:
				if category == "Movies":
					url = "http://www.animenova.org/category/anime-movies"
				else:
			  		url = "http://www.animenova.org/anime-list"
		elif siteName == "Animegalaxy":
			url = "http://www.chia-anime.tv/index/"
		elif siteName == "Animeget":
			url = "http://www.animeget.io/full-anime-list/"
		elif siteName == "Animehere":
			if category == "Movies":
				url = "http://www.animehere.com/anime-movie.html"
			else:
				url = "http://www.animehere.com/anime-all.html"
		elif siteName == "AnimePlus":
			if category == "Movies":
				url = "http://www.animeplus.tv/anime-movies"
			else:
				url = "http://www.animeplus.tv/anime-show-list"
			tmp_content = ccurl_setcookie(url)
		elif siteName == "AnimeWow":
			if category == "Movies":
				url = "http://www.animewow.org/movies"
			else:
				url = "http://www.animewow.org/anime"
		elif siteName == "Animebox":
			url = "http://www.animebox.tv/category"
		elif siteName == "AnimeHQ":
			url = "http://moetube.net/explore"
		elif siteName == "GoodAnime":
			url = "http://www.goodanime.net/new-anime-list"
		elif siteName == "Anime-Freak":
			url = "http://www.anime-freak.org/anime-list/"
		elif siteName == "AnimeBaka":
			url = "http://animebaka.tv/browse/shows"
		elif siteName == "Animefun":
			url = "http://animeonline.one/category/anime-list/"
		elif siteName == "AnimeNet":
			url = "http://www.watch-anime.net/anime-list-all/"
			urlM = "http://www.watch-anime.net/anime-movies/"
		elif siteName == "AnimeMax":
			url = "http://gogocartoon.net/anime-list.html"
		elif siteName == "AnimeStream":
			url = "http://www.ryuanime.com/animelist.php"
		elif siteName == "AnimeMix":
			url = "http://www.animechiby.com/index/"
		elif siteName == "AnimeSquare":
			url = "http://www.masterani.me/"
			#if not os.path.isfile('/tmp/AnimeWatch/anime.txt'):
			#	cloudfareUrl(url)
			#content = subprocess.check_output(["curl","-c","/tmp/AnimeWatch/anime.txt",'-b','/tmp/AnimeWatch/anime.txt','-A',hdr,url])
			url = "http://www.masterani.me/api/anime-all"
		elif siteName == "Anime1":
			url = "http://www.anime1.com/content/list/"
		elif siteName == "AnimeAll":
			if category == "Movies":
				url = "http://www.watchanimeshows.net/movies-list/"
			else:
				url = "http://www.watchanimeshows.net/anime-shows/"
			
		print(url)
		if siteName != "AnimePlus":
			
			if siteName == "AnimeNet":
				content1 = ccurl(urlM)
				content2 = ccurl(url)
			elif siteName == "AnimeSquare":
				 content = ccurlM(url)
			#elif siteName == "Anime1":
			#	hdrs = {'user-agent':self.hdr}
			#	req = requests.get(url,headers=hdrs)
			#	content = req.text
			else:
				content = ccurl(url)
		else:
			content = ccurl_cookie(url)
		if siteName == "Anime44":
			m = []
			soup = BeautifulSoup(content)
			if category == "Movies":
				link = soup.findAll('div',{'id':'videos'})
			else:
				link = soup.findAll('table',{'id':'series_grid'})
			for i in link:
				a = i.findAll('a')
				for j in a:
					if 'href' in str(j):
						k = (j['href']).split('/')
						m.append(k[-1])
			if opt == "Random":
				m = random.sample(m, len(m))
		
		elif siteName == "Animeget" or siteName == "Animegalaxy":
			if siteName == "Animeget":
				m = re.findall('http://www.animeget.io/anime/[^"]*',content)
			else:
				m = re.findall('http://www.chia-anime.tv/episode/[^"]*/',content)
			#print(m
			#del m[0:50]
			#m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				if siteName == "Animeget":
					i = re.sub('http://www.animeget.io/anime/',"",i)
				else:
					i = re.sub('http://www.chia-anime.tv/episode/',"",i)
				i = re.sub('/',"",i)
				m[j] = i
				j = j + 1
			if opt == "Random":
				m = random.sample(m, len(m))
			
		elif siteName == "Animehere":
			m = []
			soup = BeautifulSoup(content)
			link = soup.findAll('dl')
			for i in link:
				j = i.findAll('a')
				for k in j:
					if 'href' in str(k) and "#" not in str(k):
						l = (k['href']).split('/')
						p = l[-1].split('.')
						m.append(p[0])
			if opt == "Random":
				m = random.sample(m, len(m))

		elif siteName == "AnimePlus":
			m = []
			soup = BeautifulSoup(content)
			link = soup.findAll('table',{'class':'series_index'})
			for i in link:
				a = i.findAll('a')
				for j in a:
					if 'href' in str(j):
						k = (j['href']).split('/')
						m.append(k[-1])
			
			if opt == "Random":
				m = random.sample(m, len(m))
		elif siteName == "AnimeWow":
			m = re.findall('http://www.animewow.org/watch-[^"]*',content)
			#print(m
			#del m[0:50]
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('http://www.animewow.org/watch-',"",i)
				#i = re.sub('',"",i)
				m[j] = i
				j = j + 1
			if opt == "Random":
				m = random.sample(m, len(m))
		elif siteName == "Animebox":
			m = re.findall('http://www.animebox.tv/videos/category/[^"]*',content)
			#print(m
			#del m[0:50]
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('http://www.animebox.tv/videos/category/',"",i)
				i = re.sub('/',"",i)
				#i = re.sub('',"",i)
				i = str(i)
				m[j] = i
				j = j + 1
			if opt == "Random":
				m = random.sample(m, len(m))	
		elif siteName == "AnimeHQ":
			m = []
			soup = BeautifulSoup(content)
			link = soup.findAll('div',{'class':'serieslisted'})
			for i in link:
				j = i.find('a')['href']
				j = j.replace('/anime/','')
				k = j.split('/')
				m.append(k[1]+'-'+k[0])
			
			if opt == "Random":
				m = random.sample(m, len(m))
		elif siteName == "GoodAnime":
			m = re.findall('category/[^"]*', content)
			m = list(set(m))
			m.sort()
			j=0
			for i in m:
				i = re.sub("category/","",i)
				m[j] = i
				j = j+1
			if opt == "Random":
				m = random.sample(m, len(m))	
		elif siteName == "Anime-Freak":
			m = re.findall('http://www.anime-freak.org/anime-stream/[^/]*', content)
			m = list(set(m))
			m.sort()
			j=0
			for i in m:
				i = re.sub("http://www.anime-freak.org/anime-stream/","",i)
				m[j] = i
				j = j+1
			if opt == "Random":
				m = random.sample(m, len(m))	
		elif siteName == "AnimeBaka":
			m = []
			soup = BeautifulSoup(content)
			link = soup.findAll('div',{'id':'list'})
			for i in link:
				a = i.findAll('a')
				for j in a:
					if 'href' in str(j):
						k = (j['href']).split('/')
						m.append(k[-1])
			if opt == "Random":
				m = random.sample(m, len(m))
		elif siteName == "Animefun":
			m = []
			arr = re.findall('a href="/category/anime-list/[^"]*',content)
		
			for i in arr:
				if '[?]' in i or 'html' in i:
					pass
				else:
					tmp = re.sub('a href="/category/anime-list/','',i)
					if tmp:
						tmp =tmp.replace('/','')
						m.append(tmp)
		
			m = random.sample(m, len(m))
		elif siteName == "AnimeNet":
			m = []
			soup = BeautifulSoup(content2)
			link = soup.findAll('li')
			for i in link:
				j = i.findAll('a')
				for k in j:
					tmp = k['href'].split('/')[-2]
					if tmp :
						m.append(tmp)

			soup = BeautifulSoup(content1)
			link = soup.findAll('li')
			for i in link:
				j = i.findAll('a')
				for k in j:
					tmp = k['href'].split('/')[-2]
					if tmp :
						m.append(tmp)
			m = random.sample(m, len(m))
		elif siteName == "AnimeMax":
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

		
			m = random.sample(m, len(m))
		
		elif siteName == "AnimeStream":
			m = []
			soup = BeautifulSoup(content)
			link = soup.findAll('div',{'id':'animeList'})
			print(link)
			for i in link:
				j = i.findAll('a')
				for k in j:
					if 'href' in str(k):
						tmp = k['href'].split('/')[-2]
						if tmp :
							m.append(tmp)

		
			m = random.sample(m, len(m))
		elif siteName == "AnimeSquare":
			m = []
			n = re.findall('"episode_count":[^,]*,"slug":"[^"]*"',content)
			for i in n:
				p = re.sub('"episode_count":|"slug":|"',"",i)
				m.append(p)
			
		
			#m = random.sample(m, len(m))
		elif siteName == "AnimeMix":
			m = []
			#content = open('1.txt','r').read()
			soup = BeautifulSoup(content)
			link = soup.findAll('ul',{'class':'links'})
			index = 0
			for i in link :
				j = i.findAll('a')
				for k in j:
					if 'href' in str(k):
						l = k['href'].split('/')[-2]
						m.append(l)
						#print(l + " :index "+str(index)
						index = index + 1
			m = list(set(m))
			m.sort()
			#m = random.sample(m, len(m))
		elif siteName == "Anime1":
			m = []
			#content = open('1.txt','r').read()
			soup = BeautifulSoup(content)
			link = soup.findAll('ul',{'class':'anime-list'})
			index = 0
			for i in link :
				j = i.findAll('a')
				for k in j:
					if 'href' in str(k):
						l = k['href'].split('/')[-1]
						m.append(l)
						#print(l + " :index "+str(index)
						index = index + 1
			m = list(set(m))
			#m.sort()
			if opt == "Random":
				m = random.sample(m, len(m))
				
		elif siteName == "AnimeAll":
			m = []
			#content = open('1.txt','r').read()
			
			soup = BeautifulSoup(content)
			link = soup.findAll('ul',{'class':'animelist'})
			#print(link
			index = 0
			for i in link :
				j = i.findAll('li')
				for k in j:
					l = k.findAll('a')
					for r in l:
						
						if 'href' in str(r):
							t = r['href'].split('/')[-2]
							m.append(t)
			
			
			if opt == "Random":
				m = random.sample(m, len(m))
		return m

	def getEpnList(self,siteName,name,embed,category):
		url = ""
		if siteName == "Anime44":
			url = "http://www.animenova.org/category/" + name
			base = "http://www.animenova.org/"
		elif siteName == "Animegalaxy":
			url = "http://www.chia-anime.tv/episode/" + name + '/'
			base = "http://www.chia-anime.tv/"
		elif siteName == "Animeget":
			url = "http://www.animeget.io/anime/" + name + '/'
			base = "http://www.animeget.io/anime/"
		elif siteName == "Animehere":
			url = "http://www.animehere.com/anime/" + name + ".html"
			base = "http://www.animehere.com/"
		elif siteName == "AnimePlus":
			url = "http://www.animeplus.tv/" + name
			base = "http://www.animeplus.tv/"
		elif siteName == "AnimeWow":
			url = "http://www.animewow.org/watch-" + name 
			base = "http://www.animewow.org/"
		elif siteName == "Animebox":
			url = "http://www.animebox.tv/videos/category/" + name
			base = "http://www.animebox.tv/video/"
		elif siteName == "AnimeHQ":
			new_name = name.rsplit('-',1)[0]
			new_c = name.split('-')[-1]
			url = "http://moetube.net/anime/" + new_c + '/' + new_name
			base = "http://moetube.net/watch/"
		elif siteName == "GoodAnime":
			url = "http://www.goodanime.net/category/" + name
			base = "http://www.goodanime.net/"
		elif siteName == "Anime-Freak":
			url = "http://www.anime-freak.org/anime-stream/" + name + '/'
			base = "http://www.anime-freak.org/anime-stream/"
		elif siteName == "AnimeBaka":
			url = "http://animebaka.tv/anime/" + name + '/'
			base = "http://animebaka.tv/anime/"
		elif siteName == "Animefun":
			
			url = "http://animeonline.one/category/anime-list/" + name+'/'
			base = "http://animeonline.one/"
		elif siteName == "AnimeNet":
			url = "http://www.watch-anime.net/" + name + "/"
			base = "http://www.watch-anime.net/"
		elif siteName == "AnimeMax":
			url = "http://gogocartoon.net/category-anime/" + name 
			base = "http://gogocartoon.net/"
		elif siteName == "AnimeStream":
			url = "http://www.ryuanime.com/watch-anime/" + name + '/' 
			base = "http://www.ryuanime.com/"
		elif siteName == "AnimeSquare":
			name1 = name.split(',',1)[1]
			epncnt = name.split(',',1)[0]
			url = "http://www.masterani.me/anime/info/" + name1 
			base = "http://www.masterani.me/anime/"
			print(url)
		elif siteName == "AnimeMix":
			if embed == 0:
				url = "http://www.animechiby.com/tag/" + name + '/'
			elif embed == 1:
				url = "http://www.animechiby.com/" + name + '/'
			base = "http://www.animechiby.com/"
		elif siteName == "Anime1":
			url = "http://www.anime1.com/watch/" + name 
			base = "http://www.anime1.com/watch/"
		elif siteName == "AnimeAll":
			if category == "Movies":
				url = "http://www.watchanimeshows.net/watch-movie/" + name+'/' 
				base = "http://www.watchanimeshows.net/watch-movie/"
			else:
				url = "http://www.watchanimeshows.net/watch-anime/" + name+'/' 
				base = "http://www.watchanimeshows.net/watch-anime/"
		if siteName != "AnimePlus":
			if siteName == "AnimeMix" and embed == 2:
				content = "<html>Hello World</html>"
			elif siteName == "AnimeSquare":
				content = ccurlM(url)
			else:
				content = ccurl(url)
		else:
			content = ccurl_cookie(url)
		#content = ccurl(url)
		soup = BeautifulSoup(content)
		summary = ""
		#print(link
		print(url)
		if (siteName == "Anime44") or (siteName == "AnimePlus") or (siteName == "AnimeWow"):
			link = soup.findAll('div', { "id" : 'series_details' })
			for i in link:
				summary = i.text
				#summary = re.sub('\n\n','\n',summary)
				#summary = re.sub('\n\n','',summary)
				summary = re.sub('  |   |    |     |      |       |        ',"",summary)
				summary = re.sub('\n\n\n',"\n",summary)
				summary = re.sub('\n\n',"\n",summary)
				summary = re.sub(':\n'," : ",summary)
				summary = re.sub(':[^"]\n'," : ",summary)
				summary = re.sub(' \n'," ",summary)
				summary = re.sub('[^.]*Category :',"\nCategory :",summary)
				summary = summary[1:]
				
		elif siteName == "Animehere":
			link = soup.findAll('section', { "class" : 'info' })
			for i in link:
				summary = i.text
				#summary = re.sub('\n\n','\n',summary)
				#summary = re.sub('\n\n','',summary)
				summary = re.sub('"',"",summary)
				summary = re.sub('var[^"]*;',"",summary)
				summary = re.sub('\n\n\n',"\n",summary)
				summary = re.sub('\n\n',"\n",summary)
				summary = re.sub('\n'," ",summary)
				summary = re.sub('   ',"",summary)
				summary = re.sub(':\n',":",summary)
				summary = re.sub('\n',"",summary)
				summary = re.sub('Summary',"\nSummary",summary)
				summary = re.sub('Genre',"\nGenre",summary)
				#summary = re.sub('\n[^"]*[a-zA-Z0-9]'," ",summary)
				#summary = re.sub(' ',"",summary)
				summary=summary[1:]
		elif siteName == "Animefun":
			img = []
			link = soup.findAll('div', { "class" : 'box-info-summary' })
			for i in link:
				summary = i.text
				#summary = re.sub('\n\n','\n',summary)
				#summary = re.sub('\n\n','',summary)
				#summary = re.sub('"',"",summary)
				#summary = re.sub('var[^"]*;',"",summary)
				summary = summary[1:]
				summary = re.sub('\n\n\n',"\n",summary)
				summary = re.sub('\n\n',"\n",summary)
				
				
				#summary = re.sub('Summary',"\nSummary",summary)
				#summary = re.sub('Genre',"\nGenre",summary)
				#summary = re.sub('\n[^"]*[a-zA-Z0-9]'," ",summary)
				#summary = re.sub(' ',"",summary)
				#summary=summary[1:]
			try:
				link = soup.find('div',{ 'class':'box-info-cover'})
				img_src = link.find('img')['src']
				print(img_src+'***********')
				if ' ' in img_src:
					img_src = re.sub(" ","%20",img_src)
				print(img_src)
				if img_src:
					img.append(img_src)
				print(img)
			except:
				img[:]=[]
		elif siteName == "Animeget" or siteName == "Animegalaxy":
			genre = ""
			summary = ""
			link = soup.findAll('span', { "class" : "info" })
			for i in link:
				summary = i.text
			link = soup.findAll('div', { "class" : "dm" } )
			for i in link:
				if "Genres:" in i.text:
					genre = i.text
					genre = genre[:-1]
			summary = name + "\n" + summary + "\n" + genre
		elif siteName == "Animebox":
			link = soup.find('div',{'id':'main-content'})
			links = link.findAll('p')
			img_links = link.find('img')
			summary = ""
			j = 1
			for i in links:	
				summary = summary + i.text + '\n'
				j = j+1
				if j == 4:
					break
			if img_links:
				img1 = "http://animebox.tv"+img_links['src']
		elif siteName == "AnimeNet":
			link = soup.find('div',{'class':'det'})
			link1 = link.findAll('p')
			for i in link1:
				summary = summary + i.text
			print(summary)
		elif siteName == "Anime1":
			summary = ""
			img = []
			link = soup.find('div',{'class':'detail-left'})
			k = 0
			if link:
				link1 = link.findAll('span')
				for i in link1:
					summary = summary + i.text + '\n'
					k = k+1
					if k == 4:
						break
			
			
			link = soup.find('div',{'class':'detail-cover'})
			link1 = link.find('a')
			if link1:
				i = link1.find('img')
				img.append(i['src'])
			print(summary)
		elif siteName == "AnimeAll":
			summary = ""
			img = []
			m = []
			n = []
			
			soup = BeautifulSoup(content)
			link = soup.findAll('div',{'class':'row'})
			for i in link:
				j = i.findAll('p')
				l = i.findAll('img')
				for k in j:
					m.append(k.text)
				for p in l:
					n.append(p['src'])


			
			if m and len(m) > 1:
				m = m[:-1]
				m = list(set(m))
				print(len(m))
				if len(m) == 2:
					print(m[1])
					summary = m[1]
			
			if n:
				n = list(set(n))
				img.append(n[0])
			
			
			
		elif siteName == "AnimeBaka":
			link = soup.findAll('span',{'itemprop':"description"})
			for i in link:
				summary = i.text
			summary = re.sub('\n\n','\n',summary)
			summary = re.sub('\n\n','',summary)
			#summary = summary[1:]
			print(summary)
		elif siteName == "AnimeHQ":
			img_hq = ''
			link = soup.findAll('div', {'id' : 'desc'})
			if link:
				summary = link[0].text
				"""
				summary = re.sub('\n\n','\n',summary)
				summary = re.sub('\n\n','',summary)
				summary = re.sub('Genres:','\nGenres:',summary)
				#summary = re.sub('Synopsis:\n','Synopsis:',summary)
				#summary = re.sub('Synopsis:[^\n]*\n','Synopsis:',summary)
				summary = re.sub('[^\n]*Synopsis:[^a-zA-Z0-9]*','Synopsis : ',summary)
				#summary = re.sub('\n',' ',summary)
				summary=summary[1:]
				"""
			img_l = soup.find('div',{'id':'img'})
			if img_l:
				img_hq = img_l.find('img')['src']
		elif siteName == "Anime-Freak":
			l = re.findall('http://www.animeboy.info/anime-info/[^"]*',content)
			if l:
				content1 = ccurl(l[0])
			soup = BeautifulSoup(content1)
			m =[]
			link = soup.findAll('body')
			for i in link:
				k = i.text
			m = re.findall('Genre[^$]*Anime Info',k)
			if m:
				genre = re.sub('Anime Info','',m[0])
			else:
				genre = ""
			n = re.findall('Plot Summary[^$]*Screen shots',k)
			if not n:
				n = re.findall('Plot Summary[^$]*var[ ]',k)
			if n:
				info = re.sub('Screen shots|var[ ]','',n[0])
			else:
				info = ""

			summary = name + '\n' + genre + '\n' + info
			print(summary)
		elif siteName == "GoodAnime":
			summary = ""
			link = soup.findAll('div',{ 'class':'catdescription'})
			img = []
			print(link)
			if link:
				img1 = link[0].find('img')
				if img1:
					img.append(img1['src'])
				j = 0
				for i in link:
					summary = summary + link[j].text
					j = j+1
		elif siteName == "AnimeMax":
			summary = ""
			link = soup.find('div',{ 'class':'anime_info_body_bg'})
			img = []
			summary = link.text
		
		elif siteName == "AnimeStream":
			summary = ""
			link = soup.find('div',{ 'class':'postbg'})
			img = []
			summary = link.text
		elif siteName == "AnimeMix":
			summary = ""
			img = []
			if embed == 1:
				
				link = soup.find('div',{ 'id':'content'})
				summary = link.text
				summary = re.sub('var cpmstar[^#]*','',summary)
				link1 = link.find('img')
				if link1:
					image = link1['src']
					img.append(image)
			elif embed == 0:
				img.append("No.jpg")
			elif embed == 2:
				img.append("No.jpg")
				
		elif siteName == "AnimeSquare":
			try:
				link = soup.find('div',{ 'class':'info'})
				link1 = link.findAll('p')
				emb = ""
				for i in link1:
					if 'Episodes' in i.text:
						emb = i.text
						break
				if emb:
					emb = emb.replace('Episodes','')
					emb = emb.replace(' ','')
					embed = int(emb)
				summary = ""
				link = soup.find('div',{ 'class':'synopsis'})
				img = []
				summary = link.text
				link = soup.find('div',{ 'class':'title'})
				link1 = link.find('h1')
				title = link1.text
				desc = link.find('div',{ 'class':'description'})
				descr = desc.text
				summary = title + " (" + descr + ")\n" + summary 
			except:
				pass 
		if not summary:
			summary = "Summary Not Available"
		try:
			if (siteName == "Anime44") or (siteName == "AnimePlus") or (siteName == "AnimeWow"):
				img = re.findall(base+'images/series/big/[^"]*.jpg',content)
			elif siteName == "Animehere":
				img = re.findall('/res/covers/[^"]*.jpg[^"]*|/images/[^"]*.jpg',content)
				img[0] = "http://www.animehere.com" + img[0]
			elif siteName == "Animeget" or siteName == "Animegalaxy":
				img = re.findall('http[^"]*.jpg|http[^"]*jpeg',content)
			elif siteName == "Animebox":
				img =[]
				img.append(img1)
			elif siteName == "AnimeHQ":
				img = []
				if img_hq:
					img.append(img_hq)
				else:
					img = re.findall('http[^"]*.jpg|http[^"]*jpeg|http[^"]*png',content)
				print(img[0])
			elif siteName == "AnimeStream":
				img = re.findall('/[^"]*.jpg',content)
				img[0] = "http://www.ryuanime.com" + img[0]
			elif siteName == "AnimeSquare":
				img = re.findall('http[^"]*.jpg[^"]*',content)
				print(img)
				
			elif siteName == "AnimeNet":
				img = []
				link = soup.find('div',{ 'class':'anm_ifo'})
				print(link)
				img_src = link.find('img')['src']
				if ' ' in img_src:
					img_src = re.sub(" ","%20",img_src)
				print(img_src)
				if img_src:
					img.append(img_src)
			elif siteName == "GoodAnime":
				
				#img = re.findall('images/[^"]*.jpg',content)
				#img[0] = "http://www.goodanime.net/"+img[2]
				if img:
					if not 'http://' in img[0]:
						img1 = re.findall('images/[^"]*.jpg',img[0])
						if img1:
							img[0] = base+img1[0]
					print(img)
			elif siteName == "Anime-Freak" or siteName == "AnimeBaka":
				img = re.findall('http[^"]*.jpg|http[^"]*jpeg',content)
				if not img:
					img = re.findall('//[^"]*.jpg',content)
					img[0] = "http:" + img[0]
			
				
			elif siteName == "AnimeMax":
				img = []
				link = soup.find('div',{ 'class':'anime_info_body_bg'})
				img_src = link.find('img')['src']
				if ' ' in img_src:
					img_src = re.sub(" ","%20",img_src)
				print(img_src)
				if img_src:
					img.append(img_src)
			#print(img
			#if img[0] != "No.jpg":
			#jpgn = img[0].split("/")[-1]
			#print("Pic Name=" + jpgn
			picn = "/tmp/AnimeWatch/" + name + ".jpg"
			if not img:
				img[0] = "No.jpg"
				picn = "No.jpg"
			
			print(picn)
		
			if not os.path.isfile(picn) and '#' not in picn:
				print(img[0])
				subprocess.call(["curl","-A",self.hdr,"-L","-o",picn,img[0]])
			else:
				print("No Image")
		except:
			picn = "No.jpg"
		j=0
		
		
		if (siteName == "Anime-Freak"):
			m = re.findall(base+'[^/]*[^"]*', content)
		elif (siteName == "Anime1"):
			soup = BeautifulSoup(content)
			link = soup.findAll('ul',{'class':'anime-list'})
			m = []
			k = 0 
			for i in link:
				link1 = i.findAll('a')
				for j in link1:
					if 'href' in str(j):
						final = j['href'].split('/')[-1]
						print(final + " :index "+str(k))
						m.append(final)
						k = k+1
		elif (siteName == "AnimeSquare"):
			m = []
			epn_n = ""
			epn_n = int(epncnt)
			if not epn_n:
				epn_n = 0	
			i = 1
			while(i <= epn_n):
				m.append(str(i))
				i = i+1
		elif (siteName == "AnimeAll"):
			m1 =[]
			m2 =[]
			m=[]
			soup = BeautifulSoup(content)
			link = soup.findAll('div',{'class':'toggles'})
			for i in link:
				j = i.findAll('a')
				for k in j:
					if 'href' in str(k) and '#' not in str(k):
						l = k['href'].split('/')
						p = l[-2]+'-'+l[-3]
						dub_sub = l[-3].lower()
						if 'sub' in dub_sub:
							m1.append(p)
						else:
							m2.append(p)
						

			m1 = naturallysorted(m1)
			m2 = naturallysorted(m2)
			m[:]=[]
			m = m1+m2
			
		elif (siteName == "AnimeMix"):
			m = []
			if embed == 0:
				content = (subprocess.check_output(['curl','-L','-A',self.hdr,url]))
				content = getContentUnicode(content)
				soup = BeautifulSoup(content)
				link = soup.findAll('div',{'class':'post_content'})
				m = []
				k = 0 
				for i in link:
					link1 = i.find('a')
					final = link1['href'].split('/')[-2]
					print(final + " :index "+str(k))
					m.append(final)
					k = k+1
				m.insert(0,"LINK:")
			elif embed == 1:
				print("hello")
				m =[]
				m[:]=[]
				content = (subprocess.check_output(['curl','-L','-A',self.hdr,str(url)]))
				content = getContentUnicode(content)
				soup = BeautifulSoup(content)
				link = []
				link = soup.findAll('div',{'class':'su-spoiler-title'})
				if link:
					for i in link:
						tmp = str(i.text)
						s_text = re.search('a-zA-Z0-9[^"]*',tmp)
						#if s_text:
						m.append(s_text)
						
						#j = i.findNext('input',{'class':'button-auto'})
						r = i.findNext('p')
						if r:
							q = r.findAll('input',{'class':'button-auto'})
							if not q:
								q = r.findAll('input',{'type':'button'})
							for j in q:
								if 'value' in str(j) and 'onclick' in str(j):
										
									val = j['onclick']
									m.append(j['value']+'#'+(re.search("http[^']*",val)).group())
									#k = j.findNextSiblings()
									#if k:
									#	for l in k:
									#		if 'value' in str(l) and 'onclick' in str(l):
									#			val = l['onclick']
									#			m.append(l['value']+'#'+(re.search("http[^']*",val)).group())
											
				t_links = len(m) - len(link)
				linkC = soup.findAll('p')
				print(linkC)
				n=[]
				n[:]=[]
				if linkC:
					for t in linkC:
						linkB = t.findAll('input')
						for j in linkB:
							if 'value' in str(j) and 'onclick' in str(j):
								q = j.findPrevious('p')
								q_text = str(q.text)
								if not q_text:
									q = q.findPrevious('p')
									q_text = str(q.text)
								s = re.search('a-zA-Z0-9[^"]*',q_text)
								if s:
									print("hello")
									n.append(q_text)
								if not s:
									q = j.findPrevious('div',{'class':'su-spoiler-title'})
									if q:
										n.append(str(q.text))
								val = j['onclick']
								n.append(j['value']+'#'+(re.search("http[^']*",val)).group())
				if m:
					if not m[0]:
						m[0] = name
				if not m:
					m.append(name)
				#if len(n) > t_links:
				m.append('Links')
				m=m+n
				
				
				
				
				
				m.insert(0,"LINK:INFO")
			elif "#" in name:
				#print(mir_output
				#output = subprocess.check_output(["bash","-c","./mirror.sh"])
				#forward = str(raw_input("Enter Next Link Index\n"))
				#print(forward
				#forward_link = str(mir[int(forward)-1])
				#individual_epn = "False"
				#for i in epn_v:
				#	if "Episode" in i:
				#		individual_epn = "True"
				#		break
				
				output = re.sub('\n','',name)
				forward_link = output.split('#')[1]
				output1 = output.split('#')[0]
				output1 = output1.replace(' ','-')
				print(forward_link,'----')
				if forward_link.endswith('.jpg'):
					forward_link = forward_link.replace('.jpg','')
					print(forward_link,'.jpg removed')
				if '=http' in forward_link:
					forward_link = forward_link.split('=')[-1]
					print(forward_link,'--split--')
				if "linkbucks" in forward_link or "bc.vc" in forward_link or "qqc.co" in forward_link or "urlbeat.net" in forward_link:
					if "linkbucks" in forward_link or "qqc.co" in forward_link or "urlbeat.net" in forward_link:
						content = (subprocess.check_output(['curl','-I','-L',forward_link]))
						content = getContentUnicode(content)
						m = re.findall('Location: [^\n]*', content)
						#print(m
						if m:
							#print(m
							final1 = m[0]
							final1 = re.sub('Location: |\r', '', final1)
							print(final1)
					else:
						final1 = forward_link
					profile = os.path.expanduser('~')+'/.mozilla/firefox/webdriver'
					ff_profile = webdriver.FirefoxProfile(profile)
					browser = webdriver.Firefox(ff_profile)
					browser.get(final1)
					time.sleep(15)
					content = str(browser.page_source)
					#print(content
					browser.close()
		
			
				else:
					final1 = ''
					if "adf.ly" in forward_link:
						forward_link = re.sub('http:','https:',forward_link)
						final1= unshorten_url(forward_link)
			
					elif "q.gs" in forward_link:
						#final1 = cloudfare(forward_link)
						final1=unshorten_url(forward_link)
						print(final1)
					elif "adf.acb.im" in forward_link:
						#final1 = cloudfare(forward_link)
						final1= unshorten_url(forward_link)
						print(final1)
					elif "lnk.acb.im" in forward_link:
						final1= forward_link
						print(final1)
					elif "mt0.org" in forward_link:
						final1= shrink_url(forward_link)
						print(final1)
					else:
			
						content = (subprocess.check_output(['curl','-I','-L',forward_link]))
						content = getContentUnicode(content)
						m = re.findall('Location: [^\n]*', content)
						#print(m
						if m:
							#print(m
							final1 = m[0]
							final1 = re.sub('Location: |\r', '', final1)
							print(final1)
					if not final1:
						final1 = forward_link
					#content = open('1.txt','r').read()
					hdr = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0"
					
					content = (subprocess.check_output(['curl','-L','-A',self.hdr,final1]))
					content = getContentUnicode(content)
				m = []
				m[:]=[]
				soup = BeautifulSoup(content)
				link = soup.find('table')
				table1 = str(link)
				t_n = re.findall('<div class="title"[^#]*</table>',table1)
				k =''
				for i in t_n:
					l = re.sub('\t|\r|-|\n','',i)
					j = re.sub('</div><br />|</div><br/>','</div><p>',l)
				
					k = re.sub('</a>','</a></p>',j)
					k = re.sub('</a></p><br />|</a></p><br/>','</a></p><p>',k)
					#k = re.sub('\n','',k)
					#print(k
				if k:
					soup = BeautifulSoup(k)
					link = soup.findAll('p')
					for i in link:
						if 'href' in str(i):
							l=i.text.split('=')[0]
							l = re.sub(' ','-',l) 
							j = i.find('a')
							k = j['href']
							print(l + ' '+ k )
							m.append(l+' '+k)
				else:
					m.append(output1+' '+forward_link)
				m.insert(0,"LINK:FINAL")
		elif (siteName == "AnimeMax"):
			m = []
			link = soup.find('ul',{'id':'episode_page'})
			epstart = int(link.find('a')['ep_start'])
			epend = int(link.find('a')['ep_end'])
			if not epstart:
				epstart = 0
			if not epend:
				epend = 0
			i = epstart
			while(i<=epend):
				ep_n = name+"-episode-"+str(i)+"-anime"
				m.append(ep_n)
				i = i+1	
		elif (siteName == "AnimeNet"):
			m = []
			link = soup.findAll('li')
			for i in link:
				j = i.findAll('a')
				for k in j:
					tmp = k['href'].split('/')[-2]
					if tmp and (tmp != "anime-list-all" and tmp != "anime-movies" and tmp != "most-popular"):
						m.append(tmp)
		elif (siteName == "AnimeStream"):
			m = []
			link = soup.find('ul',{ "id":"anime-episode-list-sub"})
			if link:
				j = link.findAll('a')
				for k in j:
					tmp = k['href'].split('/')[-1]
					if tmp:
						m.append("Subbed-"+tmp)
			link = soup.find('ul',{ "id":"anime-episode-list-dub"})
			if link:
				j = link.findAll('a')
				for k in j:
					tmp = k['href'].split('/')[-1]
					if tmp:
						m.append("Dubbed-"+tmp)
		elif (siteName == "Animefun"):
			m = []
			mydivs = soup.findAll("ul", { "class" : "list-episode" })
			for i in mydivs:
				j = i.findAll('a')
				for k in j:
					links = k['href'].split('/')[-2]
					m.append(links)
			print(m)
			"""
			t = int(m[0].split('-')[-1])
			m[:] = []
			while(t > 0):
				epn = "episode-"+str(t)
				m.append(epn)
				t = t -1
			"""
		elif (siteName == "AnimeBaka"):
			m = []
			link = soup.findAll('tbody')
			for i in link:
				a = i.findAll('a')
				for j in a:
					if 'href' in str(j):
						k = (j['href']).split('/')
						m.append(k[-1])
			print(m)
			print(len(m))
		elif (siteName == "AnimeWow") or (siteName == "AnimePlus") or (siteName == "Anime44") or (siteName == "Animegalaxy") or (siteName == "Animehere") or (siteName == "GoodAnime") or (siteName == "Animeget"):
			m=[]
			if category == "Movies" and siteName == "Anime44":
				m.append(name)
			if siteName == "Animehere":
				link = soup.findAll('section',{ 'class':'date-list'})
			elif siteName == "GoodAnime":
				link = soup.findAll('div',{ 'class':'postlist'})
			elif siteName == "Animeget":
				link = soup.findAll('div',{ 'class':'abso'})
			elif siteName == "Animegalaxy":
				#link = soup.findAll('div',{ 'class':'post'})
				link = soup.findAll('a',{ 'itemprop':'url'})
			else:
				link = soup.findAll('div',{ 'id':'videos'})
			if siteName == "Animegalaxy":
				for i in link:
					m.append(i['href'])
			else:
				for i in link:
						
						j = i.findAll('a')
						for k in j:
							m.append(k['href'])
							print(k['href'])
			
		elif (siteName == "Animebox"):
			m = re.findall(base + '[^"]*', content)
			if not m:
				m = re.findall(base +'[^"]*ova[^"]*', content)
				if not m:
					m = re.findall(base + '[^"]*episode[^"]*', content)
		elif (siteName == "AnimeHQ"):
			soup = BeautifulSoup(content)
			link = soup.findAll('li')
			m = []
			for i in link:
				j = i.find('a')
				if j and 'href' in str(j):
					k = j.text
					if 'Episode' in k:
						print(k)
						l = re.findall('[0-9][^ ]*',k)
						if l and len(l) == 2:
							m.append(l[0])
							m.append(l[1])
			print(m)

			lower = int(m[0])
			upper = int(m[-1])
			m[:]=[]
			for i in range(lower,upper+1):
				m.append(str(i))
				
			print(m)
			
		n = []
		nxt = ""
		for i in m:
			if siteName != "AnimeHQ" and siteName != "AnimeHQ" and siteName != "Anime-Freak" and siteName != "AnimeBaka" and siteName != "Animeget" and siteName != "Animegalaxy" and siteName != "AnimeMix" and siteName != "GoodAnime" and siteName != "Animebox" and siteName != "AnimeAll":
				i = re.sub(base,"",i)
				i = re.sub("/","",i)
				i = re.sub(".html","",i)
				prev = i
				if ('share=' not in i) and (prev != nxt) :
					n.append(i)
					nxt = i
			elif siteName == "AnimeHQ":
					i = re.sub("/watch/","",i)
					n.append(i)
			elif siteName == "AnimeWow":
					i = re.sub(base,"",i)
					n.append(i)
			elif siteName == "GoodAnime":
					i = i.split('/')[-1]
					n.append(i)
			elif siteName == "Anime-Freak":
					k = i.split('/')
					i = k[-1]
					i = re.sub(".html","",i)
					if i:
						n.append(i)
			elif siteName == "Animeget":
					i = re.sub(base,"",i)
					i = re.sub("/","",i)
					n.append(i) 
			elif siteName == "Animegalaxy":
					k = i.split('/')
					print(k)
					if len(k) >3:
						j = k[-2]
						if "chia-anime" not in j:
							n.append(j) 
			elif siteName == "Animebox":
					k = i.split('/')
					i = k[-1]+'-'+k[-2]
					if i:
					 	n.append(i)
		if siteName != "AnimeBaka" and siteName != "AnimeMix" and siteName != "AnimeAll":
			m = n	
		if siteName != "AnimeMix" and siteName != "AnimeAll":   
			m = list(set(m))
			#m.sort()
			m=naturallysorted(m)
			
		if m and (siteName == "Anime44" or siteName == "Animehere" or siteName == "AnimePlus" or siteName == "AnimeWow" or siteName == "GoodAnime") and category!="Movies":
			if siteName == "AnimePlus":
				tmp = m[0].split('-')[-2]
			else:
				tmp = m[0].split('-')[-1]
			try:
				num = int(tmp)
			except:
				num = 0
			if num > 1:
				arr = m[0].split('-')
				if siteName == "AnimePlus":
					arr.pop()
				try:
					t_name = arr[0]
				except:
					t_name = ""
				i = 1
				while(i<len(arr)-1):
					t_name = t_name+'-'+arr[i]
					i = i+1
				i = 1
				new_arr=[]
				while(i<num):
					if siteName == "AnimePlus":
						new_arr.append(t_name+'-'+str(i)+'-online')
					else:
						new_arr.append(t_name+'-'+str(i))
					i = i+1
				m[:0]=new_arr
		m.append(picn)
		m.append(summary)
		return m
		
	def getNextPage(self,name,pgn):
		if (pgn >= 1):
			pgnum = str(pgn)
			if pgn == 1:
				url = "http://www.animenova.org/category/" + name
			else:
				url = "http://www.animenova.org/category/" + name + '/page/' + pgnum
				print(url)
				content = ccurl(url)
				m = re.findall('http://www.animenova.org/[^"]*episode[^"]*', content)
				m = list(set(m))
				m.sort()
				j=0
				for i in m:
					i = re.sub("http://www.animenova.org/","",i)
					m[j] = i
					j = j+1
			return m
	
	def getFinalUrl(self,siteName,name,epn,mirrorNo,category,quality):
		global qualityVideo
		qualityVideo = quality
		if siteName == "Anime44":
			url = "http://www.animenova.org/" + epn
		elif siteName == "Animegalaxy":
			url = "http://www.chia-anime.tv/" + epn + '/'
		elif siteName == "Animeget":
			url = "http://www.animeget.io/episode/" + epn
		elif siteName == "Animehere":
			url = "http://www.animehere.com/" + epn + ".html"
		elif siteName == "AnimePlus":
			url = "http://www.animeplus.tv/" + epn
			if not os.path.isfile('/tmp/AnimeWatch/cookie.txt'):
					subprocess.call(["curl","-A",self.hdr,"-c","/tmp/AnimeWatch/cookie.txt","-I","http://www.animeplus.tv"])
		elif siteName == "AnimeWow":
			url = "http://www.animewow.org/" + epn
		elif siteName == "Animebox":
			epn = (epn)
			new_epn = epn.rsplit('-',1)[0]
			epn_c = epn.split('-')[-1]
			url = "http://www.animebox.tv/video/" + epn_c+'/'+new_epn + "/"
			print(url)
		elif siteName == "AnimeHQ":
			new_name = name.rsplit('-',1)[0]
			new_c = name.split('-')[-1]
			url = "http://moetube.net/watch/" + new_c+'/'+new_name + "/" + epn
			print('url=',url)
		elif siteName == "GoodAnime":
			url = "http://www.goodanime.net/" + epn
		elif siteName == "Anime-Freak":
			url = "http://www.anime-freak.org/anime-stream/" + name + '/' + epn + '.html'
		elif siteName == "AnimeBaka":
			url = "http://animebaka.tv/watch/" +name+'/'+ epn
		elif siteName == "Animefun":
			url = "http://animeonline.one/" + epn +'/'
		elif siteName == "AnimeNet":
			url = "http://www.watch-anime.net/" +name+'/'+ epn +'/'
		elif siteName == "AnimeMax":
			url = "http://gogocartoon.net/" + epn
		elif siteName == "AnimeStream":
			if "Subbed" in epn:
				epn = re.sub('Subbed-',"",epn)
				url = "http://www.ryuanime.com/watch/subbed/episode/"+epn
			elif "Dubbed" in epn:
				epn = re.sub('Dubbed-',"",epn)
				url = "http://www.ryuanime.com/watch/dubbed/episode/"+epn
		elif siteName == "AnimeSquare":
			name1 = name.split(',',1)[1]
			epncnt = name.split(',',1)[0]
			url = "http://www.masterani.me/anime/watch/" + name1+"/" + epn
			#if not os.path.isfile('/tmp/AnimeWatch/anime.txt'):
			#	cloudfareUrl(url)
		elif siteName == "Anime1":
			url = "http://www.anime1.com/watch/"+name+"/" + epn
		elif siteName == "AnimeAll":
			epn1=epn.rsplit('-',1)[0]
			epn2=epn.rsplit('-',1)[1]
			url = "http://www.watchanimeshows.net/"+epn2+'/'+epn1+'/'
			print(url)
		elif siteName == "AnimeMix":
			url = epn.split(' ')[1]
		print(url)
		
		if siteName == "Animeget" or siteName == "Animegalaxy":
				content = ccurl(url)
				final = ""
				soup = BeautifulSoup(content)
				if siteName == "Animeget":
					link = soup.findAll('iframe')
				else:
					link = soup.findAll('a',{'id':'download'})
				link1 = soup.findAll('div',{'id':'video44'})
				for i in link1:
					a = i.findAll('a')
					for j in a:
						k = j['href']
						t = k.split('/')
						num = t[-1]
						if siteName == "Animeget":
							final1 = "http://www.animeget.io/watch/" + t[-3] +'/' + num + '/'
						else:
							final1 = "http://www.chia-anime.tv/view/" + t[-3] +'/' + num + '/'
						print(final1)
				print(len(link))
				j = 0
				m = []
				if link:
					for i in link:
						if siteName == "Animeget":
							print(i['src'])
							m.append(i['src'])
						else:
							print(i['href'])
							m.append(i['href'])
				if m:
					print(m[0])
					content = ccurl(m[0])
					links = re.findall('http[^"]*.mp4',content)
					if links:
						final = links[0]
						print(final)
					if not final:
						content = ccurl(final1)
						final2 = re.findall('http://[^"]*video44[^"]*',content)
						if final2:
							final = findurl(final2[0])
			
		elif siteName == "Animebox":
			content = ccurl(url)
			m = re.findall('http[^"]*hash[^"]*',content)
			print(m)
			if m:
				content = ccurl(m[0])
				n = re.findall('http[^"]*hash[^"]*mp4[^"]*',content)
				print(n)
				if n:
					final = n[0]
		elif siteName == "AnimeAll":
			m =[]
			n = []
			o = []
			final = ''
			mirrorNo = mirrorNo - 1
			content = ccurl(url)
			soup = BeautifulSoup(content,'lxml')
			link = soup.findAll('iframe',{'id':'embed'})
			if not link:
				url_v =''
				n_v = ''
				id_v = ''
				link1 = soup.findAll('script',{'type':'text/javascript'})
				for i in link1:
					j = i.text
					if 'var datas' in j:
						var_datas = j
						break
				m_v = re.findall("n: '[^']*|id: '[^']*|url:[^,]*",var_datas)
				print(m_v)
				for i in m_v:
					if 'n:' in i:
						n_v = re.sub("n: |'",'',i)
					elif 'id:' in i:
						id_v = re.sub("id: |'",'',i)
					elif 'url: ' in i:
						url_v = re.sub('url: |"','',i)
				url_n = url_v+'?n='+n_v+'&id='+id_v
				print (url_n)
				if url_n:
					content = ccurl(url_n)
					soup = BeautifulSoup(content,'lxml')
					link = soup.findAll('iframe',{'id':'embed'})
			for i in link:
				j = i['src']
				if "vidcrazy" in j or "uploadcrazy" in j or "auengine" in j:
					m.append(j)
				elif "videoweed" in j:
					print("")
				elif "mp4upload" in j:
					o.append(j)
				else:
					n.append(j)
			if qualityVideo == "hd":
				m = o+m+n
			else:
				m = m+o+n
			print(m)
			
			if mirrorNo == 0:
				for i in range(len(m)):
					msg = "Total " + str(len(m)) + " Mirrors, Selecting Mirror "+str(mirrorNo + 1)
					subprocess.Popen(["notify-send",msg]) 
					final = findurl(str(m[i]))
					print(i)
					print(final)
					if final:
						print(final)
						break
			else:
				msg = "Total " + str(len(m)) + " Mirrors, Selecting Mirror "+str(mirrorNo + 1)
				subprocess.Popen(["notify-send",msg])
				final = findurl(str(m[mirrorNo]))
				 
		elif siteName == "AnimeSquare":
			content = ccurl(url)
			soup = BeautifulSoup(content)
			content1 = soup.findAll('script',{'type':'text/javascript'})
			final = ""
			for i in content1:
				#print (i.text)
				if 'mirrors:' in i.text:
					content11 = (i.text)
			m = re.findall('"quality"[^,]*|"embed_id"[^,]*|"embed_prefix"[^,]*',content11)
			#print(m)
			for i in range(len(m)):
				m[i] = re.sub('"|embed_id":|embed_prefix":|quality":','',m[i])
				m[i] = re.sub("'",'',m[i])
				m[i] = m[i].replace('[\\]','')
			#print(m)
			n = []
			for i in m:
				
				if '/' in i:
					#print (i)
					j = i.split('\\')
					#print(j)
					nm = j[0]
					for k in range(len(j)-1):
						nm = nm + j[k+1]
					#print(nm)
					n.append(nm)
				else:
					#print(i)
					n.append(i)
			sd_arr =[]
			hd_arr =[]
			for i in range(0,len(n),3):
				if '480' in n[i+1]:
					sd_arr.append(n[i+2]+n[i])
				elif '720' in n[i+1]:
					hd_arr.append(n[i+2]+n[i])

			print(sd_arr)
			print(hd_arr)
			
			
			total_cnt = 0
			final_sd_hd_arr =[]
			if quality == 'sd' and sd_arr:
				url = sd_arr[mirrorNo-1]
				total_cnt = len(sd_arr)
				final_sd_hd_arr = sd_arr
			elif quality == 'hd' and hd_arr:
				url = hd_arr[mirrorNo-1]
				total_cnt = len(hd_arr)
				final_sd_hd_arr = hd_arr
			elif quality == 'hd' and not hd_arr:
				url = sd_arr[mirrorNo-1]
				total_cnt = len(sd_arr)
				final_sd_hd_arr = sd_arr
				quality = 'sd'
			print(url)
			msg = "Total " + str(len(sd_arr)) + " SD Mirrors And \n"+ str(len(hd_arr)) + " HD Mirrors+\n"+'Selecting '+str(quality) + " Mirror No. " + str(mirrorNo)
			subprocess.Popen(["notify-send",msg]) 
			
			if mirrorNo == 1:
				for i in range(len(final_sd_hd_arr)):
					msg = 'Selecting '+str(quality) + " Mirror No. " + str(i+1)
					subprocess.Popen(["notify-send",msg]) 
					url = final_sd_hd_arr[i]
					if 'mp4upload' in url and not url.endswith('.html'):
						url = url+'.html'
					final = findurl(url)
					if final:
						break
					
						
			else:
				url = final_sd_hd_arr[mirrorNo-1]
				if 'mp4upload' in url and not url.endswith('.html'):
					url = url+'.html'
				final = findurl(url)
			
		elif siteName == "AnimeMix":
			
			if "adf.acb.im" in url:
				#shrink_link=str(cloudfare(url))
				shrink_link=str(unshorten_url(url))
			elif "q.gs" in url:
				shrink_link=str(unshorten_url(url))
			else:
				shrink_link = shrink_url(str(url))

	
	
			if "mediafire" in shrink_link or "embedupload" in shrink_link or "solidfiles" in shrink_link or "mirrorcreator" in shrink_link or "tusfiles" in shrink_link:
				final = findurl(shrink_link)
			else:
				content = (subprocess.check_output(['curl','-I','-L',shrink_link]))
				content = getContentUnicode(content)
				#print(content
				m = []
				m[:] = []
				m = re.findall('Location: [^\n]*', content)
				print(m)
				if m:
					#print(m
					final1 = m[0]
					final1 = re.sub('Location: |\r', '', final1)
					print(final1)
					final = findurl(final1)
			
		elif siteName == "AnimeStream":
			content = ccurl(url)
			soup = BeautifulSoup(content)
			
			link = soup.find('div',{'id':'content'})
			print(link)
			final1 = link.find('iframe')['src']
			if not final1:
				final1 = link.find('IFRAME')['SRC']
			final = findurl(final1)
		elif siteName == "Anime1":
			content = ccurl(url)
			m = re.findall('file: "[^"]*',content)
			if m:
				final = re.sub('file: "','',m[0])
				final = re.sub(' ','%20',final)
			else:
				"No Url"
		elif siteName == "AnimeMax":
			final = ''
			content = ccurl(url)
			soup = BeautifulSoup(content,'lxml')
			link = soup.find('div',{'class':'anime_video_body_watch'})
			sd = ''
			hd = ''
			sd480 = ''
			if link:
				link2 = link.find('iframe')
				if link2:
					if 'src' in str(link2):
						link1 = link2['src']
						print(link1,'---')
						if link1:
							content1 = ccurl(link1)
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
				
				content = (subprocess.check_output(['curl','-L','-I','-A',self.hdr,final_q]))
				content = getContentUnicode(content)
				print(content)
				m = re.findall('Location: https[^\n]*', content)
				#print(m
				if m:
					#print(m
					final = m[0]
					final = re.sub('Location: |\r', '', final)
			else:
				final = ''
			
			
			
			
		elif siteName == "AnimeNet":
			finalArr = []
			content = ccurl(url)
			soup = BeautifulSoup(content)
			link = soup.findAll('iframe')
			print(link)
			for i in link:
				j = i['src']
				if "video44" in j or "playpanda" in j or "easyvideo" in j or "yourupload" in j or "playbb" in j or "auengine" in j or "play44" in j:
					j = re.sub('amp;','',j)
					finalArr.append(j)
			print(finalArr)
			if mirrorNo == 1:
				for i in finalArr:
					final1 = findurl(i)
					print(final1)
					if final1:
						final = final1
						break
			else:
				final1 = findurl(finalArr[mirrorNo-1])
				if final1:
					final = final1
		elif siteName == "Animefun":
			content = ccurl(url)
			arr =[]
			final =""
			m = []
			link2 =[]
			soup = BeautifulSoup(content)
			link = soup.find('div',{'id':'video_inner'})
			if link:
				link1 = link.findAll('iframe')
				if link1:
					for i in link1:
						link2.append(i['src'])
				link4 = re.findall('src="http[^"]*mp4upload[^"]*',content)
				for i in link4:
					i = re.sub('src="',"",i)
					link2.append(i)
			else:
				link1 = ""
				link2 = ""
				
			
			if link2:
				print(link2)
				mirrorNo = mirrorNo - 1
				if mirrorNo < len(link2):
					link3 = link2[mirrorNo]
				else:
					link3 = link2[0]
				if "mp4upload" in link3:
					final = findurl(link3)
				else:
					content = ccurl(link3)
					soup = BeautifulSoup(content)
					j = soup.find('source')
					if j:
						tmp = j['src']
						arr.append(tmp)
					final1 = arr[0]
					print(final1)
					content = (subprocess.check_output(["curl","-A",self.hdr,"-I",final1]))
					content = getContentUnicode(content)
					print(content)
					m[:]=[]
					m = re.findall('https[^\n]*', content)
					#print(m
					if m:
						#print(m
						final = m[0]
						final = re.sub('\r', '', final)
		
		elif siteName == "AnimeBaka":
			content = ccurl(url)
			soup = BeautifulSoup(content)
			
			final1 = re.findall('data-src="[^"]*',content)
			final2 = re.sub('data-src="','',final1[0])
			print(final2)
			code = final2.split('/')[-1]
			final3 = "https://bakavideo.tv/get/files.embed?f="+code
			print(final3)
			content = ccurl(final3)
			m = re.findall('"content":"[^"]*',content)
			content = re.sub('"content":"','',m[0])
			#content = content.decode("base64")
			content = str(base64.b64decode(content).decode('utf-8'))
			print(content)
			soup = BeautifulSoup(content)
			final = soup.find('source')['src']
			print("Beautifulsoup="+final)
			
		elif siteName == "Anime-Freak":
				content = ccurl(url)
				m = []
				soup = BeautifulSoup(content)
				link1 = soup.find('div',{'id':'play_options'})
				link = link1.findAll('a')
				j = 0
				for i in link:
					k = i['href']
					if not "gogoupload" in str(k) and not "javascript" in str(k):
						m.append(k.replace(' ','+'))
					j = j+1
					if j == 2:
						break
					#print(i.text + "----" + urllib.unquote(k).decode('utf8')
				
				print(m)
				if not m:
					n = re.findall("http://www.anime-freak.org/anime_player.php[^']*",content)
					if n:
						tmp = re.sub('[ ]','+',n[0])
						m.append(tmp)
					
				print(m)
				print(len(m))
				final=[]
				i = 0
				for i in m:
					content = ccurl(i)
					#server = i.split('/')[2]
					#print(server
					n = re.findall('http://[^"]*',content)
					if n:
						lnk = n[0]
						print(lnk)
						k = lnk.split('/')
						server = k[2]
						content = ccurl(lnk)
						arr = re.findall("[']fname=[^']*",content)
						if arr:
							url1 = arr[0]
							print(url1)
							url2 = re.findall('ddata[^"]*&uid',url1)
							url3 = re.sub('&uid','',url2[0])
							final1 = "http://" + server + "/" + url3
							final1 = str(urllib.parse.unquote(final1))
							url4 = re.sub('[+]','%20',final1)
							final1 = url4
							print(final1)
							final.append(final1)
		elif siteName == "AnimeHQ":
			content = ccurl(url)
			soup = BeautifulSoup(content)
			"""
			#link = soup.find('div',{'id':'vidholder'})
			link = soup.find('div',{'id':'moaroptions'})
			#link1 = link.find('source')['src']
			link2 = link.findAll('a')
			for i in link2:
				if 'href' in str(i):
					k = i['href']
					link1 = 'http://moetube.net'+k
					if 'download' in k:
						break
			print(link1)
			"""
			glink1 = re.findall("var glink = '[^']*",content)
			glink = re.sub("var glink = '",'',glink1[0])
			print(glink)
			url1 = urllib.parse.quote(url)
			link1 = "https://docs.google.com/get_video_info?eurl="+url1+"&authuser=&docid="+glink
			print(link1)
			content = (subprocess.check_output(['curl','-L','-A',self.hdr,link1]))
			content = getContentUnicode(content)
			content = urllib.parse.unquote(content)
			#print(content)
			cont1 = content.split('|')
			#print(cont1)
			sd =""
			hd =""
			sd480 =""
			sd44 =""
			for i in range(len(cont1)):
				if 'itag=18' in cont1[i]:
					sd = cont1[i]
					break
					
			for i in range(len(cont1)):
				if 'itag=22' in cont1[i]:
					hd = cont1[i]
					break
			for i in range(len(cont1)):
				if 'itag=35' in cont1[i]:
					sd480 = cont1[i]
					break
			for i in range(len(cont1)):
				if 'itag=44' in cont1[i]:
					sd44 = cont1[i]
					break
			print(sd)
			print(hd)
			print(sd480)
			print(sd44)
			
			final_cnt = 0
			final_quality = ''
			if sd:
				final_cnt = final_cnt+1
				final_quality = final_quality + 'SD '
			if sd44:
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
			
			if quality == 'sd':
				link1 = sd
			elif quality == "sd480p":
				if sd480:
					link1 = sd480
				elif sd:
					link1 = sd
			elif quality == 'hd':
				if hd:
					link1 = hd
				elif sd480:
					link1 = sd480
				elif sd:
					link1 = sd
				
			content = (subprocess.check_output(['curl','-I','-L','-A',self.hdr,link1]))
			content = getContentUnicode(content)
			
			m = re.findall('Location: [^\n]*',content)
			if m:
				final = re.sub('Location: |\r','',m[-1])
			else:
				final = link1
			print(final)
		elif (siteName == "AnimeWow") or (siteName == "AnimePlus") or (siteName == "Anime44") or (siteName == "Animegalaxy") or (siteName == "Animehere") or (siteName == "GoodAnime"):
			
			print(epn)
			#print("Pre_Opt="+pre_opt
			#print("Opt="+opt
			opt = category
			if (siteName == "AnimeWow" and opt == "History" and category == "Movies"):
				opt = "Movies"
			if (siteName == "Anime44" or siteName == "AnimePlus" or siteName == "Animegalaxy" or siteName == "Animehere" or siteName == "AnimeWow") and category == "Movies":
				opt = "Movies"
			if opt == "Movies":
				if siteName != "AnimePlus":
					content = ccurl(url)
				else:
					content = ccurl_cookie(url)
				soup = BeautifulSoup(content)
				if siteName != "Animehere":
					link = soup.findAll('ul',{ 'class':'ver_list'})
				else:
					link = soup.findAll('ul',{ 'class':'version cfix'})
				mir =[]
				mirror_n =""
				for i in link:
					a = i.findAll('a')
					for k in a:
						if siteName != "Animehere":
							mir.append(k['href'])
						else:
							mir.append("http://www.animehere.com"+k['href'])
							print(mir)
				if not mir or len(mir) == 1:
					mirror = mirrorNo
					mirror_n= "NO"
				else:
					mirror = mirrorNo
				if mirror == 1:
					if siteName != "Animehere":
						link = soup.findAll('div',{ 'class':'vmargin'})
						if not link:
							link = soup.findAll('div',{ 'id':'streams'})
					else:
						link = soup.findAll('div',{ 'id':'playbox'})
					l = 0
					final = []
					m =[]
					for i in link:
							a = i.findAll('iframe')
							for k in a:
								m.append(k['src'])
								l = l + 1
							print(m)
					if mirror_n == "NO":
						return m
					if m:
						final1 = findurl(m[0])
						if not final1:
								if mir:
									url = mir[1]
									final = []
									print(url)
									if siteName != "AnimePlus":
										content = ccurl(url)
									
									else:
										content = ccurl_cookie(url)
									soup = BeautifulSoup(content)
									if siteName != "Animehere":
										link = soup.findAll('div',{ 'class':'vmargin'})
										if not link:
											link = soup.findAll('div',{ 'id':'streams'})
									else:
										link = soup.findAll('div',{ 'id':'playbox'})
									l = 0
									n = []
									for i in link:
										a = i.findAll('iframe')
										for k in a:
											n.append(k['src'])
										print(n)
									return n
						else:
							return m
					
					
				else:
					
					
			
					if mir:
						url = mir[mirrorNo-1]
						final = []
						print(url)
						if siteName != "AnimePlus":
							content = ccurl(url)
						
						else:
							content = ccurl_cookie(url)
						soup = BeautifulSoup(content)
						if siteName != "Animehere":
							link = soup.findAll('div',{ 'class':'vmargin'})
							if not link:
								link = soup.findAll('div',{ 'id':'streams'})
						else:
							link = soup.findAll('div',{ 'id':'playbox'})
						l = 0
						n = []
						for i in link:
							a = i.findAll('iframe')
							for k in a:
								n.append(k['src'])
							print(n)
						return n
						
							
						
			else:
				if siteName != "AnimePlus":
					content = ccurl(url)
				else:
					content = ccurl_cookie(url)
				soup = BeautifulSoup(content)
				if siteName == "Animehere":
					link = soup.findAll('div',{'id':'playbox'})	
				elif siteName == "GoodAnime":
					link = soup.findAll('div',{'class':'postcontent'})
				
				else:
					link = soup.findAll('div',{'id':'streams'})
				print(len(link))
				j = 0
				arr =[]
				for i in link:
					a = i.findAll('iframe')
					for k in a:
						arr.append(k['src'])
				j = 1
				length = len(arr)
				while (j <= length):		
					mirrorNo = mirrorNo - 1
					print(arr)
					msg = "Total " + str(len(arr)) + " Mirrors, Selecting Mirror "+str(mirrorNo + 1)
					subprocess.Popen(["notify-send",msg]) 
					final = findurl(arr[mirrorNo])
					if final:
						break
					j = j + 1
					mirrorNo = j
			print(final)
			print(mirrorNo)
		return final
		
	def urlResolve(self,url):
		final = findurl(url)
		if final:
			return final
		else:
			return 0
		 

