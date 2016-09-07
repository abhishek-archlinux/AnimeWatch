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
