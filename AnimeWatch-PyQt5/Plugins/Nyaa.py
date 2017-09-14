"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import urllib.parse
import pycurl
from io import StringIO, BytesIO
import re
import random
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup
import os.path
from subprocess import check_output
from player_functions import send_notification, ccurl, get_hls_path
try:
    import libtorrent as lt
    from stream import ThreadServer, TorrentThread, get_torrent_info
except:
    notify_txt = 'python3 bindings for libtorrent are broken\
                  Torrent Streaming feature will be disabled'
    send_notification(notify_txt)
import shutil

hls_path, frozen_file = get_hls_path()

def cloudfare(url, quality=None, cookie=None, get_link=None, get_cookie=None, 
            tmp_dir=None, js=None, show_window=None):
    if hls_path is None:
        web = BrowseUrl(url, quality, cookie)
    else:
        cookie_found = False
        lnk_found = None
        if get_cookie or get_link:
            if get_cookie:
                if cookie:
                    if os.path.exists(cookie):
                        os.remove(cookie)
                hls_exec = [
                    hls_path, url, '--set-cookie-file='+cookie, 
                    '--cookie-end-pt=_gat', '--cookie-domain-name=nyaa.si', 
                    '--wait-for-cookie', '--output=false', '--tmp-dir='+tmp_dir, 
                    '--block-request=.ads, ads., revcontent, .bebi, scorecard', 
                    ]
                if not frozen_file:
                    hls_exec = [sys.executable, '-B'] + hls_exec
                if os.name == 'posix':
                    p = subprocess.call(hls_exec)
                else:
                    p = subprocess.call(hls_exec, shell=True)
                cookie_found = True
                    
            if get_cookie and not get_link:
                return cookie_found
            else:
                return lnk_found

class Nyaa():
    
    def __init__(self, tmp):
        self.hdr = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
        self.tmp_dir = tmp
        self.cookie_file = os.path.join(tmp, 'nyaa.txt')
        if not os.path.exists(self.cookie_file):
            f = open(self.cookie_file, 'w')
            f.close()
            
    def getOptions(self):
            criteria = [
                'Date', 'Seeders', 'Leechers', 'Downloads',
                'History', 'LocalStreaming', 'newversion'
                ]
            return criteria
    
    def ccurlN(self, url):
        content = ccurl(url+'#-b#'+self.cookie_file)
        #print(content)
        if 'checking_browser' in content:
            if os.path.exists(self.cookie_file):
                os.remove(self.cookie_file)
            if hls_path:
                ans = cloudfare(
                        url, cookie=self.cookie_file, get_cookie=True, 
                        tmp_dir=self.tmp_dir)
            else:
                cloudfare(
                    url, cookie=self.cookie_file, get_cookie=True, 
                    tmp_dir=self.tmp_dir)
            content = ccurl(url+'#-b#'+self.cookie_file)
        return content
        
    def process_page(self, url):
        content = self.ccurlN(url)
        soup = BeautifulSoup(content, 'lxml')
        #print(soup.prettify())
        unit_element = soup.findAll('td', {'colspan':'2'})
        #print(unit_element[0])
        s = []
        for i in unit_element:
            try:
                element = i.findAll('a')
                for index in element:
                    et = index['href']
                    if '#comment' not in et:
                        elem = index
                        j = elem['title']
                        try:
                            k = elem['href'].split('/')[-1]
                        except:
                            k = 'Download Not Available'
                        break
                td = i.findNext('td', {'class':'text-center'})
                sz = td.findNext('td', {'class':'text-center'})
                dt = sz.findNext('td', {'class':'text-center'})
                se = dt.findNext('td', {'class':'text-center'})
                le = se.findNext('td', {'class':'text-center'})
                down = le.findNext('td', {'class':'text-center'})
                try:
                    tmp = j.replace('_', ' ')+'	id='+k+'|Size='+sz.text+'|Seeds='+se.text+'|Leechers='+le.text+'|Total Downloads='+down.text
                except:
                    tmp = 'Not Available'
                print(tmp)
                s.append(tmp)
            except Exception as e:
                print(e, '--98---')
            
        return s
        
    def search(self, name):
        strname = str(name)
        print(strname)
        url = "https://nyaa.si/?f=0&c=1_2&s=seeders&o=desc&q="+str(strname)
        m = self.process_page(url)
        return m
        
    def getCompleteList(self, opt, genre_num, ui, tmp_dir, hist_folder):
        global tmp_working_dir
        instr = "Press . or > for next page	-1"
        tmp_working_dir = tmp_dir
        if opt == 'Date':
            url = 'https://nyaa.si/?c=1_2'
        elif opt == 'Seeders':
            url = 'https://nyaa.si/?c=1_2&s=seeders&o=desc'
        elif opt == 'Leechers':
            url = 'https://nyaa.si/?c=1_2&s=leechers&o=desc'
        elif opt == 'Downloads':
            url = 'https://nyaa.si/?c=1_2&s=downloads&o=desc'
        print(opt, url)
        m = self.process_page(url)
        m.append(instr)
        m.append(1)
        return m
    
    def getEpnList(self, name, opt, depth_list, extra_info, siteName, category):
        if extra_info == '-1':
            arr = []
            return (arr, 'Instructions', 'No.jpg', False, depth_list)
        else:
            print(extra_info)
            name_id = (re.search('id=[^|]*', extra_info).group()).split('=')[1]
            url = "https://nyaa.si/download/" + name_id + '.torrent'
            print(url)
            summary = ""
            
            torrent_dest = os.path.join(siteName, name+'.torrent')
            
            if not os.path.exists(torrent_dest):
                ccurl(url+'#'+'-o'+'#'+torrent_dest, self.cookie_file)
            
            info = lt.torrent_info(torrent_dest)
            file_arr = []
            for f in info.files():
                file_path = f.path
                file_path = os.path.basename(file_path)	
                file_arr.append(file_path)
            record_history = True
            return (file_arr, 'Summary Not Available', 'No.jpg', record_history, depth_list)

    def getNextPage(self, opt, pgn, genre_num, name):
        if opt == 'Date':
            url = 'https://nyaa.si/?c=1_2'
        elif opt == 'Seeders':
            url = 'https://nyaa.si/?c=1_2&s=seeders&o=desc'
        elif opt == 'Leechers':
            url = 'https://nyaa.si/?c=1_2&s=leechers&o=desc'
        elif opt == 'Downloads':
            url = 'https://nyaa.si/?c=1_2&s=downloads&o=desc'
        elif opt == 'Search':
            url = "https://nyaa.si/?f=0&c=1_2&s=seeders&o=desc&q="+str(name)
        url = url + '&p='+str(pgn)
        print(url)
        m = self.process_page(url)
        return m
