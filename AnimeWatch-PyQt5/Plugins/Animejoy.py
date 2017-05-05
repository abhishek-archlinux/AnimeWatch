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
import random
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup
import os.path
from subprocess import check_output
from player_functions import ccurl

def naturallysorted(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)



def replace_all(text, di):
	for i, j in di.iteritems():
		text = text.replace(i, j)
	return text


class Animejoy():
	def __init__(self,tmp):
		self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		self.tmp_dir = tmp
	def getOptions(self):
			criteria = ['Random','History','List']
			return criteria
		
	def getFinalUrl(self,name,epn,mirror,quality):
		url = "http://anime-joy.tv/watch/"+name+"/"+epn
		print(url)
		content = ccurl(url)
		try:
			m = re.findall('http:[^"]*.mp4',content)
			url = m[0]
			#print("in try url:" + url 
		except:
			m = re.findall('http://anime-joy.tv/embed[^"]*',content)
			#m = list(set(m))
		
			content = ccurl(m[0])
			
			m = re.findall('http[^"]*.mp4',content)
			#m = list(set(m))
			#print(m
			url = m[0]
		print(url)
		
		return url
	
	def search(self,name):
		strname = str(name)
		print(strname)
		url = "http://anime-joy.tv/animelist"
		content = ccurl(url)
		m = re.findall('watch/[^"]*',content)
		j=0
		search = []
		for i in m:
			i = re.sub('watch/',"",i)
			m[j] = i
			j = j + 1
		m = list(set(m))
		m.sort()
		s = []
		for i in m:
			m = re.search('[^"]*'+strname+'[^"]*',i)
			if m:
				found = m.group(0)
				s.append(found)
			
		return s
		
	def getCompleteList(self,opt,genre_num):
		url = "http://anime-joy.tv/animelist"
		content = ccurl(url)
		#print(content)
		m = re.findall('watch/[^"]*',content)
		j=0
		search = []
		for i in m:
			i = re.sub('watch/',"",i)
			m[j] = i
			j = j + 1
		m = list(set(m))
		m.sort()
		if opt == "Random":
			m = random.sample(m, len(m))
		return m
	
	def getEpnList(self,name,opt,depth_list,extra_info,siteName,category):
		url = "http://anime-joy.tv/watch/" + name
		print(url)
		summary = ""
		content = ccurl(url)
		soup = BeautifulSoup(content,'lxml')
		link = soup.findAll('div', { "class" : 'ozet' })
		link1 = soup.findAll('img')
		img=""
		for i in link:
			summary = i.text
			#summary = re.sub("\n","",summary)
		if not summary:
			summary = "Summary Not Available"
		else:
			m = re.findall(r'\\n',summary)
			print(m)
			n = re.findall(r'\\t',summary)
			for i in m:
				summary = summary.replace(i,'')
			for i in n:
				summary = summary.replace(i,'')
			print(summary)
			
		for i in link1:
			if 'src' in str(i):
				j = i['src']
				if j and '.jpg' in j:
					img = j
					img = img.replace('animejoy.tv','anime-joy.tv')
					print(img)
		#picn = "/tmp/" + name + ".jpg"
		picn = os.path.join(self.tmp_dir,name+'.jpg')
		try:
			if not os.path.isfile(picn) and img:
				#subprocess.call(["curl","-o",picn,img])
				ccurl(img+'#'+'-o'+'#'+picn)
		except:
			print("No Cover")
		m = re.findall('http://anime-joy.tv/watch/'+name+'/[^"]*',content)
		j=0
		for i in m:
			i = re.sub('http://anime-joy.tv/watch/'+name+'/',"",i)
			m[j] = i
			j = j + 1
		m=naturallysorted(m)  
		#m.append(picn)
		#m.append(summary)
		record_history = True
		return (m,summary,picn,record_history,depth_list)

