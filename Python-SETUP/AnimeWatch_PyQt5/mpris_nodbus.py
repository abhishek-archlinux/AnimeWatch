import os
import sys
from PyQt5 import QtCore
import re
import PIL
from PIL import Image 
import shutil
from PyQt5.QtCore import (pyqtSlot,pyqtSignal,pyqtProperty)


class MprisServer():
	def __init__(self,ui,home,tr_ay,new_tr):
		global tray,new_tray_widget
		self.ui = ui
		self.home = home
		tray = tr_ay
		new_tray_widget = new_tr
		
	def _emitMeta(self,info,site,epnArrList):
		global tray,new_tray_widget
		art_url = self.ui.default_background
		artist = 'AnimeWatch'
		title = 'AnimeWatch'
		if epnArrList and (site == "Music" or site == "PlayLists"):
			
			try:
				queue_list = False
				if self.ui.queue_url_list:
					t2 = info.split('#')[1]
					t1 = t2.split('	')
					queue_list = True
				else:
					r = self.ui.list2.currentRow()
					print(epnArrList[r])
					t1 = epnArrList[r].split('	')
				if len(t1) > 2:
					t = t1[0]
					art = t1[2]
				else:
					t = t1[0]
					art = t
				if 'internet-radio#' in info:
					print(info,'---------_emitMeta--------')
					art = info.split('#')[1]
					t = epnArrList[self.ui.list2.currentRow()].split('	')[0]
					t = t.replace('#','')
					print(art,t)
				if (site == 'Music' and self.ui.list3.currentItem()) or (site == 'PlayLists'): 
					if ((site == 'Music' and self.ui.list3.currentItem().text().lower() == 'playlist') 
							or (site == 'PlayLists')):
						artist = art
						if artist.lower() == 'none':
							artist = t.replace('#','')
							if artist.startswith(self.ui.check_symbol):
								artist = artist[1:]
						pls = self.ui.list1.currentItem().text()
						if not queue_list:
							pls_entry = self.ui.list2.currentItem().text().replace('#','')+'.jpg'
						else:
							pls_entry = t.replace('#','')
						if pls_entry.startswith(self.ui.check_symbol):
							pls_entry = pls_entry[1:] 
						img_place = os.path.join(self.home,'thumbnails','PlayLists',pls,pls_entry)
						print(img_place,'--img--place')
						title = re.sub('.jpg','',pls_entry)
						art_u = img_place
					elif site == 'Music':
						title = t
						artist = art
						title = title.replace('#','')
						artist = artist.replace('#','')
						if title.startswith(self.ui.check_symbol):
							title = title[1:]
						if artist.startswith(self.ui.check_symbol):
							artist = artist[1:]
						art_u = os.path.join(self.home,'Music','Artist',artist,'poster.jpg')
			except:
				title = "AnimeWatch"
				artist = "AnimeWatch"
		else:
			try:
				r = self.ui.list2.currentRow()
				print(epnArrList[r])
				t1 = epnArrList[r].split('	')
				title = t1[0]
				if title.startswith(self.ui.check_symbol):
					title = title[1:]
				artist = self.ui.list1.currentItem().text()
				art_u = os.path.join(self.home,'thumbnails',artist,title+'.jpg')
				if 'internet-radio#' in info:
					print(info,'---------_emitMeta--------')
					artist = info.split('#')[1]
					title = epnArrList[self.ui.list2.currentRow()].split('	')[0]
					print(artist,title)
				title = title.replace('#','')
				#if os.path.exists(art_u):
				#	art_url = art_u
			except Exception as e:
				print(e,'--no-dus-error--')
				title = "AnimeWatch"
				artist = "AnimeWatch"
		try:
			r = self.ui.list2.currentRow()
			art_u = self.ui.get_thumbnail_image_path(r,epnArrList[r])
			if os.path.exists(art_u):
				art_url = art_u
		except Exception as e:
			print(e,'--no-dbus--error--')
		
		abs_path_thumb = art_url
		if title == artist:
			if len(title) > 38:
				title = title[:36]+'..'
				artist = '..'+artist[36:]
			else:
				artist = ''
		else:
			if len(title) > 38:
				title = title[:36]+'..'
			if len(artist) > 38:
				artist = artist[:36]+'..'
		new_tray_widget.title.setText(title)
		new_tray_widget.title1.setText(artist)
