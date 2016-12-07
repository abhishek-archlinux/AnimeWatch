import os
import sys
from PyQt5 import QtCore
import re
import PIL
from PIL import Image 
import shutil
from PyQt5.QtCore import (pyqtSlot,pyqtSignal,pyqtProperty)

try:
	import dbus
	import dbus.service
	import dbus.mainloop.pyqt5
except:
	pass
	
AW_MPRIS_BUS_NAME = 'org.mpris.MediaPlayer2.animewatch'
MPRIS_OBJECT_PATH = '/org/mpris/MediaPlayer2'
MPRIS_MEDIAPLAYER_INTERFACE = 'org.mpris.MediaPlayer2'
MPRIS_MEDIAPLAYER_PLAYER_INTERFACE = 'org.mpris.MediaPlayer2.Player'

class MprisServer(dbus.service.Object):
	def __init__(self,ui,home,tr_ay,new_tr):
		global tray,new_tray_widget
		tray = tr_ay
		new_tray_widget = new_tr
		bus = dbus.service.BusName(
		    AW_MPRIS_BUS_NAME,
		    bus=dbus.SessionBus())
		super().__init__(bus, MPRIS_OBJECT_PATH)
		
		self._properties = dbus.Dictionary({
            'DesktopEntry': 'AnimeWatch',
            'Identity': 'animewatch',
            
}, signature='sv')
		
		
		self._player_properties = dbus.Dictionary({
            'Metadata': dbus.Dictionary({
                
                'mpris:artUrl': '',
                'xesam:artist': ['None'],
                'xesam:title': 'None',
                
                'xesam:album': 'None'
            }, signature='sv', variant_level=1),
            
            'CanGoNext': True,
            'CanGoPrevious': True,
            'CanPause': True,
	    'CanPlay': True,
             'CanControl': True,
             'CanStop': True,
}, signature='sv', variant_level=2)

		self.ui = ui
		self.home = home

	@dbus.service.method(MPRIS_MEDIAPLAYER_PLAYER_INTERFACE,
				 in_signature='', out_signature='')
	def Play(self):
		print ("Play Song")
		self.ui.playerPlayPause()
			
			
	@dbus.service.method(MPRIS_MEDIAPLAYER_PLAYER_INTERFACE,
				 in_signature='', out_signature='')
	def Pause(self):
		print ("PlayPause Song")
		self.ui.playerPlayPause()

	@dbus.service.method(MPRIS_MEDIAPLAYER_PLAYER_INTERFACE,
				 in_signature='', out_signature='')
	def Next(self):
		print ("Next Song")		
		self.ui.mpvNextEpnList()
				

	@dbus.service.method(MPRIS_MEDIAPLAYER_PLAYER_INTERFACE,
				 in_signature='', out_signature='')
	def Previous(self):
		print ("Previous Song")
		self.ui.mpvPrevEpnList()
				

	@dbus.service.method(MPRIS_MEDIAPLAYER_PLAYER_INTERFACE,
                         in_signature='', out_signature='')
	def PlayPause(self):
		print ("PlayPause Song")
		self.ui.playerPlayPause()


	@dbus.service.method(MPRIS_MEDIAPLAYER_PLAYER_INTERFACE,
				 in_signature='', out_signature='')
	def Stop(self):
		self.ui.playerStop()

	@dbus.service.signal(dbus.PROPERTIES_IFACE,
				 signature='sa{sv}as')
	def PropertiesChanged(self, interface, changed_properties,
				  invalidated_properties=[]):
		pass

	@pyqtSlot(str,str,list)
	def _emitMeta(self,info,site,epnArrList):
		global tray,new_tray_widget
		print(type(tray),type(new_tray_widget),type(site),type(epnArrList))
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
				if ((site == 'Music' and self.ui.list3.currentItem()) 
						or (site == 'PlayLists')): 
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
			except Exception as e:
				print(e,'--mpris-dbus-error--')
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
			except:
				title = "AnimeWatch"
				artist = "AnimeWatch"
		try:
			r = self.ui.list2.currentRow()
			art_u = self.ui.get_thumbnail_image_path(r,epnArrList[r])
			if os.path.exists(art_u):
				art_url = art_u
		except Exception as e:
			print(e,'--no--art--url--or-path--')
		
		art_url_name = '256px.'+os.path.basename(art_url)
		path_thumb,new_title = os.path.split(art_url)
		abs_path_thumb = os.path.join(path_thumb,art_url_name)
		try:
			if not os.path.exists(abs_path_thumb) and os.path.exists(art_url):
				basewidth = 256
				img = Image.open(str(art_url))
				wpercent = (basewidth / float(img.size[0]))
				#hsize = int((float(img.size[1]) * float(wpercent)))
				hsize = 256
				img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
				img.save(str(abs_path_thumb))
		except Exception as e:
			print(e,"--image--can't be processed--")
		
		props = dbus.Dictionary({'Metadata': dbus.Dictionary({
		    'xesam:artist': artist,
		'mpris:artUrl': abs_path_thumb,
		    
		    'xesam:title': title,
		}, signature='sv')}, signature='sv')
		self._player_properties.update(props)

		self.PropertiesChanged(MPRIS_MEDIAPLAYER_PLAYER_INTERFACE,
				       props, [])

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
		
			
	@dbus.service.method(dbus.INTROSPECTABLE_IFACE,
				 in_signature='', out_signature='s')
	def Introspect(self):
		
		path = os.path.join(self.home,'src','introspect.xml')
		print(path,'---path---')
		if os.path.exists(path):
			content = open(path,'r').read()
		else:
			content = ''
		return content
		
	@dbus.service.method(dbus.PROPERTIES_IFACE,
                         in_signature='ss', out_signature='v')
	def Get(self, interface, prop):
		return self.GetAll(interface)[prop]

	@dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ssv')
	def Set(self, interface, prop, value):
		self._player_properties[prop] = value

	@dbus.service.method(dbus.PROPERTIES_IFACE,
				 in_signature='s', out_signature='a{sv}')
	def GetAll(self, interface):
		if interface == MPRIS_MEDIAPLAYER_PLAYER_INTERFACE:
		    return self._player_properties
		elif interface == MPRIS_MEDIAPLAYER_INTERFACE:
		    return self._properties
		else:
		    raise dbus.exceptions.DBusException(
			'com.example.UnknownInterface',
			'The Foo object does not implement the %s interface'
			% interface
	)

