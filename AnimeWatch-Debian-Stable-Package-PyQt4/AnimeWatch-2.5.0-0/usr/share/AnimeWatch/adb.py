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
from PyQt4 import QtCore, QtGui,QtNetwork

from PyQt4.QtNetwork import QNetworkAccessManager
from PyQt4.QtWebKit import QWebView

class NetWorkManager(QNetworkAccessManager):
	def __init__(self):
		super(NetWorkManager, self).__init__()
   
	def createRequest(self, op, request, device = None ):
		global block_list
		try:
			path = str(request.url().toString())
		except UnicodeEncodeError:
			path = str(request.url().path())
			pass
		lower_path = path.lower()
		#lst = tuple(open("easylist.txt", 'r'))
		block_list = ["doubleclick.net" ,"ads", r"||youtube-nocookie.com/gen_204?", r"youtube.com###watch-branded-actions", "imagemapurl","b.scorecardresearch.com","rightstuff.com","scarywater.net","popup.js","banner.htm","_tribalfusion","||n4403ad.doubleclick.net^$third-party",".googlesyndication.com","graphics.js","fonts.googleapis.com/css","s0.2mdn.net","server.cpmstar.com","||banzai/banner.$subdocument","@@||anime-source.com^$document","/pagead2.","frugal.gif","jriver_banner.png","show_ads.js",'##a[href^="http://billing.frugalusenet.com/"]',"http://jriver.com/video.html","||animenewsnetwork.com^*.aframe?","||contextweb.com^$third-party",".gutter",".iab",'http://www.animenewsnetwork.com/assets/[^"]*.jpg','revcontent']
		block = False
		for l in block_list:
			if l in lower_path:
				block = True
				break
		if block:
			print ("Skipping")
			print (path)
			return QNetworkAccessManager.createRequest(self, QNetworkAccessManager.GetOperation, QtNetwork.QNetworkRequest(QtCore.QUrl()))
		else:
			return QNetworkAccessManager.createRequest(self, op, request, device)



             
