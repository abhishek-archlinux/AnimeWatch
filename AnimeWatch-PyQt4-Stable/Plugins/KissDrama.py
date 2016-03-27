from PyQt4 import QtCore, QtGui
import sys
import urllib
import pycurl
from io import StringIO
import re
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup 
import os.path
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
import time
import shutil
from tempfile import mkstemp
from shutil import move
from os import remove, close
from os.path import expanduser
import fileinput
import codecs
import base64
def cloudfare():
			home1 = expanduser("~")
			#home1 = "/usr/local/share"
			pluginDir = home1+"/.config/AnimeWatch/src/Plugins"
			temp = progressBar(["phantomjs", pluginDir+"/kad.js","http://kissasian.com"])
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
			cookiefile = ".kissasian.com	TRUE	/	FALSE	"+str(e[0])+"	__cfduid	" + str(e[1]) + "\n" + "kissasian.com	FALSE	/	FALSE	0	ASP.NET_SessionId	"+str(a[0])+"\n"+".kissasian.com	TRUE	/	FALSE	"+str(n[0])+"	cf_clearance	" + str(n[1])
			f = open('/tmp/AnimeWatch/kcookieD.txt', 'w')
			f.write(cookiefile)
			f.close()
def ccurl(url):
	global hdr
	hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
	MainWindow = QtGui.QWidget()
	progress = QtGui.QProgressDialog("Please Wait", "Cancel", 0, 100, MainWindow)
	progress.setWindowModality(QtCore.Qt.WindowModal)
	progress.setAutoReset(True)
	progress.setAutoClose(True)
	progress.setMinimum(0)
	progress.setMaximum(100)
	progress.resize(300,100)
	progress.setWindowTitle("Loading, Please Wait!")
	progress.show()
	progress.setValue(0)
	content = subprocess.check_output(['curl','-b','/tmp/AnimeWatch/kcookieD.txt','-L','-A',hdr,url]) 
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
	"""
	c = pycurl.Curl()
	c.setopt(c.USERAGENT, hdr)
	if os.path.isfile('/tmp/AnimeWatch/kcookieD.txt'):
		c.setopt(c.COOKIEFILE, '/tmp/AnimeWatch/kcookieD.txt')
	url = str(url)
	c.setopt(c.URL, url)
	storage = StringIO()
	c.setopt(c.WRITEFUNCTION, storage.write)
	c.perform()
	c.close()
	content = storage.getvalue()
	"""
	progress.setValue(100)
	progress.hide()
	return (content)

def progressBar(cmd):
	MainWindow = QtGui.QWidget()
	progress = QtGui.QProgressDialog("Please Wait", "Cancel", 0, 100, MainWindow)
	progress.setWindowModality(QtCore.Qt.WindowModal)
	progress.setAutoReset(True)
	progress.setAutoClose(True)
	progress.setMinimum(0)
	progress.setMaximum(100)
	progress.resize(300,100)
	progress.setWindowTitle("Loading, Please Wait!")
	progress.show()
	progress.setValue(0)
	#content = cmd
	#print(content
	#content = ccurl(cmd,"")
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
	progress.setValue(100)
	progress.hide()
	#print(content
	return (content)


def naturallysorted(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

def replace_all(text, di):
	for (i, j,) in di.iteritems():
		text = text.replace(i, j)

	return text



class KissDrama():
	def __init__(self):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:37.0) Gecko/20100101 Firefox/37.0'
		
	def getOptions(self):
			criteria = ['MostPopular','Newest','LatestUpdate','Genre','History']
			return criteria
	def search(self,name):
		if not os.path.isfile('/tmp/AnimeWatch/kcookieD.txt'):
			cloudfare()
		if name != '':
			url = 'http://kissasian.com/Search/Drama/?keyword=' + name
			content = ccurl(url)
			m = re.findall('/Drama/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Drama/', '', i)
				m[j] = i
				j = j + 1

			return m
	def getEpnList(self,name,opt):
		if not os.path.isfile('/tmp/AnimeWatch/kcookieD.txt'):
			cloudfare()
		url = 'http://kissasian.com/Drama/' + name
		print(url)
		content = ccurl(url)
		f = open('/tmp/AnimeWatch/1.txt','w')
		f.write(content)
		f.close()
		epl = re.findall('/Drama/' + name + '[^"]*?id[^"]*', content)
		#if not epl:
		#	epl = re.findall('[^"]*?id=[^"]*', content)
		try:
			img = re.findall('http://kissasian.com/Uploads/Etc/[^"]*.jpg', content)
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
				subprocess.call(['curl','-L','-b','/tmp/AnimeWatch/kcookieD.txt','-A',self.hdr,'-o',picn,img[0]])
		except:
			picn = '/tmp/AnimeWatch/' + name + '.jpg'
		j = 0
		for i in epl:
			i = re.sub('/Drama/' + name + '/', '', i)
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
		if not os.path.isfile('/tmp/AnimeWatch/kcookieD.txt'):
			cloudfare()
		url = 'http://kissasian.com/Drama/' + name + '/' + epn
		print(url)
		if not os.path.isfile('/tmp/AnimeWatch/kcookieD.txt'):
			cloudfare(url)
		#f = open('/tmp/AnimeWatch/kcookie.txt','r')
		#lines = f.readlines()
		#f.close()
		#lin = str(lines[1]).split("	")
		#val = lin[6][:-1]
		#t = lin[4]
		##content = progressBar(["phantomjs", "phantom.js",url,val,t,"--load-images=false"])
		#content = subprocess.check_output(["phantomjs", "phantom.js",url,val,t,"--load-images=false"])
		content = ccurl(url)
		print(content)
		soup = BeautifulSoup(content)
		#f = open('/tmp/AnimeWatch/k.txt','w')
		#f.write(content)
		#f.close()
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
			elif '=m18' in i:
				sd = i
			elif '=m22' in i:
				hd = i
		
		if quality == "hd" and hd:
			sd = hd
		if not sd:
			sd = hd
		content = subprocess.check_output(['curl','-b','/tmp/AnimeWatch/kcookieD.txt','-L','-I','-A',self.hdr,sd])
		m = self.urlResolve(content)
		#print(m
		if m:
			#print(m
			final = m[-1]
		
		print(final)
		return final
		
	def getCompleteList(self,opt,genre_num):
		if not os.path.isfile('/tmp/AnimeWatch/kcookieD.txt'):
			cloudfare()
		if opt == 'Genre' and genre_num == 0:
			url = 'http://kissasian.com/DramaList/'
			content = ccurl(url)
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
			url = 'http://kissasian.com/DramaList/' + opt
			pgn = 1
			content = ccurl(url)
			m = re.findall('/Drama/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Drama/', '', i)
				m[j] = i
				j = j + 1

			return m
		if genre_num == 1:
			url = 'http://kissasian.com/Genre/' + opt
			pgn = 1
			content = ccurl(url)
			m = re.findall('/Drama/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Drama/', '', i)
				m[j] = i
				j = j + 1

			return m
	def getNextPage(self,opt,pgn,genre_num):
		if not os.path.isfile('/tmp/AnimeWatch/kcookieD.txt'):
			cloudfare()
		if opt != '' and pgn >= 1:
			pgnum = str(pgn)
			if (opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate'):
				url = 'http://kissasian.com/DramaList/' + opt + '?page=' + pgnum
			else:
				url = 'http://kissasian.com/Genre/' + opt + '?page=' + pgnum
				#print(url
			content = ccurl(url)
			m = re.findall('/Drama/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Drama/', '', i)
				m[j] = i
				j = j + 1

			if m:
				return m
	def getPrevPage(self,opt,genre_num):
		if not os.path.isfile('/tmp/AnimeWatch/kcookieD.txt'):
			cloudfare()
		if opt != '' and pgn >= 1:
			pgnum = str(pgn)
			if genre_num == 0:
				url = 'http://kissasian.com/DramaList/' + opt + '?page=' + pgnum
			else:
				url = 'http://kissasian.com/Genre/' + opt + '?page=' + pgnum
			content = ccurl(url)
			m = re.findall('/Drama/[^"]*', content)
			m = list(set(m))
			m.sort()
			j = 0
			for i in m:
				i = re.sub('/Drama/', '', i)
				m[j] = i
				j = j + 1

			if m:
				return m




