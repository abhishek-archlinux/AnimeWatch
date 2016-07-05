"""
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
import sys
from PyQt5 import QtCore, QtGui,QtNetwork,QtWidgets,QtWebEngineWidgets,QtWebEngineCore

from PyQt5.QtNetwork import QNetworkAccessManager

class NetWorkManager(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
	
	def __init__(self,parent):
		super(NetWorkManager, self).__init__(parent)
		
	def interceptRequest(self,info):
		#print('hello network')
		#print(info)
		t = info.requestUrl()
		urlLnk = t.url()
		
		
		lower_case = urlLnk.lower()
		
		lst = ["doubleclick.net" ,"ads",'facebook','.aspx', r"||youtube-nocookie.com/gen_204?", r"youtube.com###watch-branded-actions", "imagemapurl","b.scorecardresearch.com","rightstuff.com","scarywater.net","popup.js","banner.htm","_tribalfusion","||n4403ad.doubleclick.net^$third-party",".googlesyndication.com","graphics.js","fonts.googleapis.com/css","s0.2mdn.net","server.cpmstar.com","||banzai/banner.$subdocument","@@||anime-source.com^$document","/pagead2.","frugal.gif","jriver_banner.png","show_ads.js",'##a[href^="http://billing.frugalusenet.com/"]',"http://jriver.com/video.html","||animenewsnetwork.com^*.aframe?","||contextweb.com^$third-party",".gutter",".iab",'http://www.animenewsnetwork.com/assets/[^"]*.jpg','revcontent']
		block = False
		for l in lst:
			if lower_case.find(l) != -1:
				block = True
				#info.block(True)
				#print(m,'---blocking----')
				break
		if block:
			info.block(True)
			#print(m,'---blocking----')
			
			
		






             
