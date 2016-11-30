"""
Copyright (C) 2016 kanishka-linux kanishka.linux@gmail.com

This file is part of AnimeWatch.

AnimeWatch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

AnimeWatch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with AnimeWatch.  If not, see <http://www.gnu.org/licenses/>.



"""

from PyQt5 import QtCore
from functools import partial
import subprocess
import shutil
import os
from tempfile import mkstemp
from player_functions import send_notification


def get_yt_url(url,quality):
	final_url = ''
	url = url.replace('"','')
	m = []
	if '/watch?' in url:
		a = url.split('?')[-1]
		b = a.split('&')
		if b:
			for i in b:
				j = i.split('=')
				k = (j[0],j[1])
				m.append(k)
		else:
			j = a.split('=')
			k = (j[0],j[1])
			m.append(k)
		d = dict(m)
		print(d,'----dict--arguments---generated---')
		try:
			url = 'https://m.youtube.com/watch?v='+d['v']
		except:
			pass
	try:
		if os.name == 'posix':
			if quality == 'sd480p':
				final_url = subprocess.check_output(
							['youtube-dl','--youtube-skip-dash-manifest','-f',
							'18','-g','--playlist-end','1',url])
				final_url = str(final_url,'utf-8')
			elif quality == 'sd':
				final_url = subprocess.check_output(
							['youtube-dl','--youtube-skip-dash-manifest','-f',
							'18','-g','--playlist-end','1',url])
				final_url = str(final_url,'utf-8')
			elif quality == 'hd':
				try:
					final_url = subprocess.check_output(
								['youtube-dl','--youtube-skip-dash-manifest',
								'-f','22','-g','--playlist-end','1',url])
					final_url = str(final_url,'utf-8')
				except:
					final_url = subprocess.check_output(
								['youtube-dl','--youtube-skip-dash-manifest',
								'-f','18','-g','--playlist-end','1',url])
					final_url = str(final_url,'utf-8')
		else:
			if quality == 'sd480p':
				final_url = subprocess.check_output(
							['youtube-dl','--youtube-skip-dash-manifest','-f',
							'18','-g','--playlist-end','1',url],shell=True)
				final_url = str(final_url,'utf-8')
			elif quality == 'sd':
				final_url = subprocess.check_output(
							['youtube-dl','--youtube-skip-dash-manifest','-f',
							'18','-g','--playlist-end','1',url],shell=True)
				final_url = str(final_url,'utf-8')
			elif quality == 'hd':
				try:
					final_url = subprocess.check_output(
								['youtube-dl','--youtube-skip-dash-manifest',
								'-f','22','-g','--playlist-end','1',url],
								shell=True)
					final_url = str(final_url,'utf-8')
				except:
					final_url = subprocess.check_output(
								['youtube-dl','--youtube-skip-dash-manifest',
								'-f','18','-g','--playlist-end','1',url],
								shell=True)
					final_url = str(final_url,'utf-8')
	except Exception as e:
		print(e,'--error in processing youtube url--')
		txt ='Please Update youtube-dl'
		#subprocess.Popen(['notify-send',txt])
		send_notification(txt)
		final_url = ''
		
		
	print(final_url)
	return final_url

def get_yt_sub(url,name,dest_dir,tmp_dir):
	global name_epn, dest_dir_sub,tmp_dir_sub,TMPFILE
	name_epn = name
	dest_dir_sub = dest_dir
	tmp_dir_sub = tmp_dir
	final_url = ''
	url = url.replace('"','')
	m = []
	if '/watch?' in url:
		a = url.split('?')[-1]
		b = a.split('&')
		if b:
			for i in b:
				j = i.split('=')
				k = (j[0],j[1])
				m.append(k)
		else:
			j = a.split('=')
			k = (j[0],j[1])
			m.append(k)
		d = dict(m)
		print(d,'----dict--arguments---generated---')
		try:
			url = 'https://m.youtube.com/watch?v='+d['v']
		except:
			pass
	fh,TMPFILE = mkstemp(suffix=None,prefix='youtube-sub')
	dir_name,sub_name = os.path.split(TMPFILE)
	print(TMPFILE,'--output-dest--',dest_dir_sub,'--',dir_name,' ---',sub_name)
	command = "youtube-dl --all-sub --skip-download --output "+TMPFILE+" "+url
	print(command)
	
	yt_sub_process = QtCore.QProcess()
	yt_sub_process.started.connect(yt_sub_started)
	yt_sub_process.readyReadStandardOutput.connect(partial(yt_sub_dataReady,yt_sub_process))
	yt_sub_process.finished.connect(yt_sub_finished)
	QtCore.QTimer.singleShot(1000, partial(yt_sub_process.start, command))

def yt_sub_started():
	print('Getting Sub')
	txt_notify = "Trying To Get External Subtitles Please Wait!"
	send_notification(txt_notify)
	
def yt_sub_dataReady(p):
	try:
		a = str(p.readAllStandardOutput(),'utf-8').strip()
		print(a)
	except:
		pass
		
def yt_sub_finished():
	global name_epn,dest_dir_sub,tmp_dir_sub,TMPFILE
	name = name_epn
	dest_dir = dest_dir_sub
	dir_name,sub_name = os.path.split(TMPFILE)
	print(dir_name,sub_name)
	m = os.listdir(dir_name)
	new_name = name.replace('/','-')
	if new_name.startswith('.'):
		new_name = new_name[1:]
	sub_avail = False
	sub_ext = ''
	txt_notify = 'No Subtitle Found'
	for i in m:
		#j = os.path.join(dir_name,i)
		src_path = os.path.join(dir_name,i)
		if (i.startswith(sub_name) and i.endswith('.vtt') 
				and os.stat(src_path).st_size != 0):
			k1 = i.rsplit('.',2)[1]
			k2 = i.rsplit('.',2)[2]
			ext = k1+'.'+k2
			sub_ext = ext+','+sub_ext
			dest_name = new_name + '.'+ ext
			print(dest_name)
			dest_path = os.path.join(dest_dir,dest_name)
			print(src_path,dest_path)
			if os.path.exists(src_path):
				shutil.copy(src_path,dest_path)
				os.remove(src_path)
				sub_avail = True
	if sub_avail:
		txt_notify = "External Subtitle "+ sub_ext+" Available\nPress Shift+J to load"
	if os.path.exists(TMPFILE):
		os.remove(TMPFILE)
	send_notification(txt_notify)
