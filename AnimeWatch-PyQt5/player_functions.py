import os
import shutil
from tempfile import mkstemp
import urllib
import urllib3
import pycurl
from io import StringIO,BytesIO
import subprocess

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'

def send_notification(txt):
	if os.name == 'posix':
		subprocess.Popen(['notify-send',txt])

def open_files(file_path,lines_read=True):
	if os.path.exists(file_path):
		if lines_read:
			lines = []
			try:
				try:
					f = open(file_path,'r')
					lines = f.readlines()
					f.close()
				except:
					f = open(file_path,encoding='utf-8',mode='r')
					lines = f.readlines()
					f.close()
			except:
				pass
				
		else:
			lines = ''
			try:
				try:
					f = open(file_path,'r')
					lines = f.read()
					f.close()
				except:
					f = open(file_path,encoding='utf-8',mode='r')
					lines = f.read()
					f.close()
			except:
				lines = "Can't Decode"
	else:
		if lines_read:
			lines = []
		else:
			lines = 'Not Available'
	return lines

def write_files(file_name,content,line_by_line):
	fh, tmp_new_file = mkstemp()
	file_exists = False
	if os.path.exists(file_name):
		file_exists = True
		shutil.copy(file_name,tmp_new_file)
		print('copying ',file_name,' to ',tmp_new_file)
	try:
		if type(content) is list:
			bin_mode = False
			f = open(file_name,'w')
			j = 0
			for i in range(len(content)):
				fname = content[i].strip()
				if j == 0:
					try:
						f.write(fname)
					except UnicodeEncodeError as e:
						print(e,file_name+' will be written in binary mode')
						bin_mode = True
						f.close()
						break
				else:
					try:
						f.write('\n'+fname)
					except UnicodeEncodeError as e:
						print(e,file_name+' will be written in binary mode')
						bin_mode = True
						f.close()
						break
				j = j+1
			if not bin_mode:
				f.close()
			else:
				f = open(file_name,'wb')
				j = 0
				for i in range(len(content)):
					fname = content[i].strip()
					if j == 0:
						f.write(fname.encode('utf-8'))
					else:
						f.write(('\n'+fname).encode('utf-8'))
					j = j+1
				f.close()
		else:
			if line_by_line:
				content = content.strip()
				if not os.path.exists(file_name) or (os.stat(file_name).st_size == 0):
					f = open(file_name,'w')
					bin_mode = False
					try:
						f.write(content)
					except UnicodeEncodeError as e:
						print(e,file_name+' will be written in binary mode')
						f.close()
						bin_mode = True
						
					if bin_mode:
						f = open(file_name,'wb')
						f.write(content.encode('utf-8'))
						f.close()
				else:
					f = open(file_name,'a')
					bin_mode = False
					try:
						f.write('\n'+content)
					except UnicodeEncodeError as e:
						print(e,file_name+' will be written in binary mode')
						f.close()
						bin_mode = True
						
					if bin_mode:
						f = open(file_name,'ab')
						f.write(('\n'+content).encode('utf-8'))
						f.close()
					
					
			else:
				f = open(file_name, 'w')
				bin_mode = False
				try:
					f.write(content)
				except UnicodeEncodeError as e:
					print(e,file_name+' will be written in binary mode')
					f.close()
					bin_mode = True
				if bin_mode:
					f = open(file_name,'wb')
					f.write(content.encode('utf-8'))
					f.close()
	except Exception as e:
		print(e,'error in handling file, hence restoring original')
		if file_exists:
			shutil.copy(tmp_new_file,file_name)
			print('copying ',tmp_new_file,' to ',file_name)
	if os.path.exists(tmp_new_file):
		os.remove(tmp_new_file)

def wget_string(url,dest,rfr=None):
	hdr = USER_AGENT
	if not rfr:
		if os.name == 'posix':
			command = "wget -c --read-timeout=60 --user-agent="+'"'+hdr+'" '+'"'+url+'"'+" -O "+'"'+dest+'"'
		else:
			command = "wget -c --no-check-certificate --read-timeout=60 --user-agent="+'"'+hdr+'" '+'"'+url+'"'+" -O "+'"'+dest+'"'
	else:
		if os.name == 'posix':
			command = "wget -c --read-timeout=60 --user-agent="+'"'+hdr+'" '+rfr+' "'+url+'"'+" -O "+'"'+dest+'"'
		else:
			command = "wget -c --no-check-certificate --read-timeout=60 --user-agent="+'"'+hdr+'" '+rfr+' "'+url+'"'+" -O "+'"'+dest+'"'
	return command
	
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




def ccurl(url,external_cookie=None):
	hdr = USER_AGENT
	if 'youtube.com' in url:
		hdr = 'Mozilla/5.0 (Linux; Android 4.4.4; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'
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
		elif curl_opt == '-Icb' or curl_opt == '-bc' or curl_opt == '-b' or curl_opt == '-Ib':
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
	if os.name != 'posix':
		c.setopt(c.SSL_VERIFYPEER,False)
	if curl_opt == '-o':
		c.setopt(c.FOLLOWLOCATION, True)
		c.setopt(c.USERAGENT, hdr)
		try:
			f = open(picn_op,'wb')
			c.setopt(c.WRITEDATA, f)
		except:
			return 0
		
		try:
			c.perform()
			c.close()
		except:
			print('failure in obtaining image try again')
			pass
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
		elif curl_opt == '-b':
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
			c.setopt(c.COOKIEFILE,cookie_file)
		else:
			c.setopt(c.FOLLOWLOCATION, True)
			c.setopt(c.USERAGENT, hdr)
			c.setopt(c.WRITEDATA, storage)
		try:
			c.perform()
			c.close()
			content = storage.getvalue()
			content = getContentUnicode(content)
		except:
			print('curl failure try again')
			content = ''
		return content
