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


def send_notification(txt):
	if os.name == 'posix':
		subprocess.Popen(['notify-send',txt])

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
		
		if quality == 'sd480p':
			"""
			try:
				try:
					audio = subprocess.check_output(['youtube-dl','--youtube-skip-dash-manifest','-f','171','-g','--playlist-end','1',url])
				except:
					audio = subprocess.check_output(['youtube-dl','--youtube-skip-dash-manifest','-f','140','-g','--playlist-end','1',url])
				try:
					video = subprocess.check_output(['youtube-dl','--youtube-skip-dash-manifest','-f','244','-g','--playlist-end','1',url])
				except:
					video = subprocess.check_output(['youtube-dl','--youtube-skip-dash-manifest','-f','135','-g','--playlist-end','1',url])
				audio = str(audio,'utf-8').strip()
				video = str(video,'utf-8').strip()
				final_url = audio+'#'+video
			except:
				final_url = subprocess.check_output(['youtube-dl','--youtube-skip-dash-manifest','-f','18','-g','--playlist-end','1',url])
				final_url = str(final_url,'utf-8')
			"""
			final_url = subprocess.check_output(['youtube-dl','--youtube-skip-dash-manifest','-f','18','-g','--playlist-end','1',url])
			final_url = str(final_url,'utf-8')
		elif quality == 'sd':
			final_url = subprocess.check_output(['youtube-dl','--youtube-skip-dash-manifest','-f','18','-g','--playlist-end','1',url])
			final_url = str(final_url,'utf-8')
		elif quality == 'hd':
			try:
				final_url = subprocess.check_output(['youtube-dl','--youtube-skip-dash-manifest','-f','22','-g','--playlist-end','1',url])
				final_url = str(final_url,'utf-8')
			except:
				final_url = subprocess.check_output(['youtube-dl','--youtube-skip-dash-manifest','-f','18','-g','--playlist-end','1',url])
				final_url = str(final_url,'utf-8')
	except:
		txt ='Please Update livestreamer and youtube-dl'
		#subprocess.Popen(['notify-send',txt])
		send_notification(txt)
		final_url = ''
		
		
	print(final_url)
	return final_url

def get_yt_sub(url,name,dest_dir,tmp_dir):
	global name_epn, dest_dir_sub,tmp_dir_sub
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
	
	#out = "/tmp/AnimeWatch/youtube-sub"
	out = os.path.join(tmp_dir_sub,'youtube-sub')
	#sub_name = out.split('/')[-1]
	sub_name = os.path.basename(out)
	print(out,'---------output--------dest---------')
	#subprocess.call(['youtube-dl','--all-sub','--skip-download','--output',out,url])
	command = "youtube-dl --all-sub --skip-download --output "+out+" "+url
	
	
	yt_sub_process = QtCore.QProcess()
	yt_sub_process.started.connect(yt_sub_started)
	yt_sub_process.readyReadStandardOutput.connect(partial(yt_sub_dataReady,yt_sub_process))
	#self.tab_5.setFocus()
	yt_sub_process.finished.connect(yt_sub_finished)
	QtCore.QTimer.singleShot(1000, partial(yt_sub_process.start, command))

def yt_sub_started():
	print('Getting Sub')
	txt_notify = "Trying To Get External Subtitles Please Wait!"
	#subprocess.Popen(['notify-send',txt_notify])
	send_notification(txt_notify)
	
def yt_sub_dataReady(p):
	try:
		a = str(p.readAllStandardOutput(),'utf-8').strip()
		print(a)
	except:
		pass
		
def yt_sub_finished():
	global name_epn,dest_dir_sub,tmp_dir_sub
	name = name_epn
	dest_dir = dest_dir_sub
	sub_name = 'youtube-sub'
	print(name,dest_dir)
	#dir_name = '/tmp/AnimeWatch/'
	dir_name = tmp_dir_sub
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
		if i.startswith(sub_name) and i.endswith('.vtt') and os.stat(src_path).st_size != 0:
			k1 = i.rsplit('.',2)[1]
			k2 = i.rsplit('.',2)[2]
			ext = k1+'.'+k2
			sub_ext = ext+','+sub_ext
			dest_name = new_name + '.'+ ext
			dest_path = os.path.join(dest_dir,dest_name)
			shutil.copy(src_path,dest_path)
			os.remove(src_path)
			sub_avail = True
	if sub_avail:
		txt_notify = "External Subtitle "+ sub_ext+" Available\nPress Shift+J to load"
		
	send_notification(txt_notify)
