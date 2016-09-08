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


import subprocess

def get_yt_url(url,quality):
	final_url = ''
	try:
		import livestreamer as lvt
		s = lvt.streams(url)
		#print(s)
		try:
			if quality == 'sd':
				final_url = s['360p'].url
			elif quality == 'hd':
				final_url = s['720p'].url
			elif quality == 'sd480p':
				final_url = s['480p'].url
		except:
			#txt = str(quality) + ' quality not found, Selecting best one'
			#subprocess.Popen(['notify-send',txt])
			final_url = s['best'].url
		
	except:
		#txt = 'LiveStreamer either not found or Livestreamer could not handle stream, hence trying youtube-dl'
		#subprocess.Popen(['notify-send',txt])
		if quality == 'hd':
			try:
				final_url = subprocess.check_output(['youtube-dl','-f','22','-g',url])
			except:
				final_url = subprocess.check_output(['youtube-dl','-f','18','-g',url])
		else:
			final_url = subprocess.check_output(['youtube-dl','-f','18','-g',url])
		final_url = str(final_url,'utf-8')
	print(final_url)
	return final_url
