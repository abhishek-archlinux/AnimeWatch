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
		global lst
		try:
			path = str(request.url().path())
		except UnicodeEncodeError:
			pass
		lower_case = path.lower()
		#lst = tuple(open("easylist.txt", 'r'))
		lst = ["doubleclick.net" ,"ads", r"||youtube-nocookie.com/gen_204?", r"youtube.com###watch-branded-actions", "imagemapurl","b.scorecardresearch.com","rightstuff.com","scarywater.net","popup.js","banner.htm","_tribalfusion","||n4403ad.doubleclick.net^$third-party",".googlesyndication.com","graphics.js","fonts.googleapis.com/css","s0.2mdn.net","server.cpmstar.com","||banzai/banner.$subdocument","@@||anime-source.com^$document","google","/pagead2.","frugal.gif","jriver_banner.png","show_ads.js",'##a[href^="http://billing.frugalusenet.com/"]',"http://jriver.com/video.html","||animenewsnetwork.com^*.aframe?","||contextweb.com^$third-party",".gutter",".iab",'http://www.animenewsnetwork.com/assets/[^"]*.jpg']
		block = False
		for l in lst:
			if lower_case.find(l) != -1:
				block = True
				break
		if block:
			print ("Skipping")
			print (request.url().path())
			return QNetworkAccessManager.createRequest(self, QNetworkAccessManager.GetOperation, QtNetwork.QNetworkRequest(QtCore.QUrl()))
		else:
			return QNetworkAccessManager.createRequest(self, op, request, device)



             
