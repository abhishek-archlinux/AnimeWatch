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
import urllib
import pycurl
from io import StringIO, BytesIO
import re
import subprocess
from subprocess import check_output
from bs4 import BeautifulSoup 
import os
import os.path
import time
import shutil
from tempfile import mkstemp
from shutil import move
from os import remove, close
from os.path import expanduser
import base64
import platform
import json
import inspect
import ipaddress
from player_functions import ccurl, naturallysorted
from player_functions import send_notification, get_hls_path

hls_path, frozen_file = get_hls_path()


def cloudfare(url, quality=None, cookie=None, get_link=None, get_cookie=None, 
            tmp_dir=None, js=None, show_window=None, get_raw_link=None, end_pt=None):
    print(hls_path, tmp_dir, cookie, end_pt)
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
                    '--cookie-end-pt='+end_pt, '--cookie-domain-name=9anime.to', 
                    '--wait-for-cookie', '--output=false', '--tmp-dir='+tmp_dir, 
                    '--block-request=.ads, ads., revcontent, .bebi, scorecard'
                    ]
                if not frozen_file:
                    hls_exec = [sys.executable, '-B'] + hls_exec
                print(hls_exec, '-----------')
                if os.name == 'posix':
                    p = subprocess.call(hls_exec)
                else:
                    p = subprocess.call(hls_exec, shell=True)
                cookie_found = True
                
            if get_link:
                cookie_found = True
                lnk_file = os.path.join(tmp_dir, 'lnk.txt')
                if os.path.isfile(lnk_file):
                    os.remove(lnk_file)
                hls_exec = [
                    hls_path, url, '--use-cookie-file='+cookie, 
                    '--output=false', '--tmp-dir='+tmp_dir, 
                    '--block-request=.ads, ads., revcontent, .bebi, scorecard, .css', 
                    '--get-link='+get_raw_link
                    ]
                if not frozen_file:
                    hls_exec = [sys.executable, '-B'] + hls_exec
                    
                if os.name == 'posix':
                    p = subprocess.call(hls_exec)
                else:
                    p = subprocess.call(hls_exec, shell=True)
                
                if os.path.exists(lnk_file):
                    with open(lnk_file, 'r') as f:
                        lnk_found = f.read()
                        lnk_found = lnk_found.strip()
            if get_cookie and not get_link:
                return cookie_found
            else:
                return lnk_found

class Anime9():
    
    def __init__(self, tmp):
        global tmp_working_dir
        self.tmp_dir = tmp
        tmp_working_dir = tmp
        self.cookie_file = os.path.join(tmp, 'cookie9.txt')
        self.pg_num = 1
            
    def getOptions(self):
            criteria = [
                'MostPopular', 'Newest', 'LatestUpdate', 'Series',
                'Movies', 'Ongoing', 'Genre', 'History', 'newversion'
                ]
            return criteria
            
    def ccurlN(self, url):
        content = ccurl(url+'#-b#'+self.cookie_file)
        if 'checking_browser' in content:
            if os.path.exists(self.cookie_file):
                os.remove(self.cookie_file)
            cloudfare(url, '', self.cookie_file)
            content = ccurl(url+'#-b#'+self.cookie_file)
        return content
        
    def search(self, name):
        
        if name:
            if not os.path.isfile(self.cookie_file):
                new_url = 'https://9anime.to/'
                print(new_url)
                cloudfare(new_url, quality='sd', cookie=self.cookie_file, end_pt='user-info', get_cookie=True, tmp_dir=self.tmp_dir)
            url = 'https://9anime.to/search?keyword=' + name
            arr = self.parse_page(url, cookie=self.cookie_file)
            if len(arr) == 1:
                print(arr, '--76---')
                if arr[0] == 'get_cookie':
                    if os.path.isfile(self.cookie_file):
                        os.remove(self.cookie_file)
                    new_url = 'https://9anime.to/'
                    print(new_url)
                    cloudfare(new_url, quality='sd', cookie=self.cookie_file, end_pt='user-info', get_cookie=True, tmp_dir=self.tmp_dir)
                    url = 'https://9anime.to/search?keyword=' + name
                    arr = self.parse_page(url, cookie=self.cookie_file)
            return arr
            
    def getEpnList(self, name, opt, depth_list, extra_info, siteName, category):
        if extra_info == '-1':
            arr = []
            return (arr, 'Instructions', 'No.jpg', False, depth_list)
        else:
            base_url = 'https://9anime.to'
            url = extra_info
            print(url, '--74--')
            content = ccurl(url)
            soup = BeautifulSoup(content, 'lxml')
            arr = []
            
            m = soup.findAll('div', {'class':'server row'})
            p = 0
            index = 0
            print(m, len(m))
            for i in m:
                index = 0
                j = i.findAll('li')
                if p == 0:
                    for k in j:
                        l = k.find('a')
                        n = l.text+'	'+os.path.join(base_url, l['href'])
                        arr.append(n)
                else:
                    for k in j:
                        l = k.find('a')
                        try:
                            n = os.path.join(l['href'].split('/')[-1])
                        except Exception as e:
                            print(e, '--84--')
                            n = 'NONE'
                        try:
                            arr[index] = arr[index]+'::'+n
                        except Exception as e:
                            print(e, '--121---')
                        index = index + 1
                p = p +1
            record_history = True
            display_list = True
            summary = 'Not Available'
            picn = 'No.jpg'
            
            try:
                m = soup.find('h1', {'class':'title'})
                pic_url = m.findNext('img')['src']
                l = m.findNext('div', {'id':'info'})
                summary = m.text.strip()+'\n'+l.text.strip()
                picn = os.path.join(self.tmp_dir, name+'.jpg')
                if not os.path.exists(picn):
                    ccurl(pic_url+'#'+'-o'+'#'+picn)
                print(picn, '--98--')
            except Exception as e:
                print(e)
            return (arr, summary, picn, record_history, depth_list)
    
    def get_epn_url(self, name, epn, mirror, quality):
        final = ''
        new_epn = epn.split('/')[-1]
        if '::' in new_epn:
            id_arr = new_epn.split('::')
            print(id_arr, mirror)
            if mirror <= len(id_arr):
                epn_id = id_arr[mirror-1]
            else:
                epn_id = id_arr[0]
        else:
            epn_id = new_epn
        if not os.path.isfile(self.cookie_file):
            new_url = 'https://9anime.to'+epn.split('::')[0]
            print(new_url)
            cloudfare(new_url, quality=quality, cookie=self.cookie_file, end_pt='watching', get_cookie=True, tmp_dir=self.tmp_dir)
        url = 'https://9anime.to/ajax/episode/info?id='+epn_id+'&update=0'
        content = ccurl(url+'#-b#'+self.cookie_file)
        l = json.loads(content)
        _target_found = False
        for i in l:
            print(i, l[i])
            if i == 'grabber':
                _api = l[i]
            if i == 'params':
                try:
                    _id = l[i]['id']
                    _token = l[i]['token']
                    _opt = l[i]['options']
                except Exception as e:
                    print(e, '--172--')
            if i == 'target':
                _target = l[i]
                if 'mycloud' in _target or 'openload' in _target:
                    _target_found = True
        if _target_found:
            nurl = _target
            if not nurl.startswith('http'):
                _target = re.search('[a-zA-Z0-9][^"]*', _target).group()
                nurl = 'https://'+_target+'&autostart=true'
            _api = None
            print(nurl)
        else:
            nurl = '?id={0}&token={1}&options={2}&mobile=0'.format(_id, _token, _opt)
        return (_api, nurl)
    
    def get_direct_grabber(self, url):
        _ts = '0'
        _val = '0'
        link_split = url.split('?')[-1]
        link_arr = link_split.split('&')
        for i in link_arr:
            if i.startswith('ts='):
                _ts = i
            elif i.startswith('_='):
                _val = i
        content = ccurl(url+'#-b#'+self.cookie_file)
        l = json.loads(content)
        _target_found = False
        for i in l:
            print(i, l[i])
            if i == 'grabber':
                _api = l[i]
            if i == 'params':
                try:
                    _id = l[i]['id']
                    _token = l[i]['token']
                    _opt = l[i]['options']
                except Exception as e:
                    print(e, '--172--')
            if i == 'target':
                _target = l[i]
                if 'mycloud' in _target or 'openload' in _target or 'rapidvideo' in _target:
                    _target_found = True
        if _target_found:
            nurl = _target
            if not nurl.startswith('http'):
                _target = re.search('[a-zA-Z0-9][^"]*', _target).group()
                nurl = 'https://'+_target+'&autostart=true'
            _api = None
            print(nurl)
        else:
            nurl = '?{0}&{1}id={2}&token={3}&options={4}&mobile=0'.format(_ts, _val, _id, _token, _opt)
        return (_api, nurl)
    
    def get_old_server(self, _api, nurl, quality):
        final = ''
        #url = os.path.join(_api, nurl)
        if nurl.startswith('?'):
            nurl = nurl[1:]
        url = _api + '&' + nurl
        print(url)

        content = ccurl(url)

        arr = []
        try:
            l = json.loads(content)
        except Exception as e:
            print(e)
            content = content.replace('}{', ', ')
            #print(content)
            try:
                l = json.loads(content)
            except Exception as e:
                print(e)
                l = []
        if l:
            for i in l:
                #print(i)
                if i == 'data':
                    for k in l[i]:
                        try:
                            j = (k['label'], k['file'])
                        except Exception as e:
                            print(e)
                            j = ('no-label', 'no-file')
                        arr.append(j)
        else:
            m = re.findall('"file":"http[^"]*', content)
            print(m)
            for i in m:
                i = i.replace('"file":"', '')
                k = ('no-label', 'no-file')
                if 'itag=18' in i:
                    k = ('360p', i)
                elif 'itag=22' in i:
                    k = ('720p', i)
                elif 'itag=59' in i:
                    k = ('480p', i)
                elif 'itag=37' in i:
                    k = ('1080p', i)
                arr.append(k)
        if arr:
            d = dict(arr)
            print(d)
            if quality == 'sd' and '360p' in d:
                final = d['360p']
            elif quality == 'sd480p':
                if '480p' in d:
                    final = d['480p']
                else:
                    final = d['360p']
            elif quality == 'hd':
                if '720p' in d:
                    final = d['720p']
                elif '480p' in d:
                    final = d['480p']
                else:
                    final = d['360p']
            elif quality == 'best':
                if '1080p' in d:
                    final = d['1080p']
                elif '720p' in d:
                    final = d['720p']
                elif '480p' in d:
                    final = d['480p']
                else:
                    final = d['360p']
        if final:
            content = ccurl(final+'#'+'-I')
            m = re.findall('Location: [^\n]*', content)
            if m:
                #print(m)
                final = re.sub('Location: |\r', '', m[-1])
        
        return final
    
    def get_quality_dict(self, d, quality):
        final = ''
        if quality == 'sd' and '360p' in d:
            final = d['360p']
        elif quality == 'sd480p':
            if '480p' in d:
                final = d['480p']
            else:
                final = d['360p']
        elif quality == 'hd':
            if '720p' in d:
                final = d['720p']
            elif '480p' in d:
                final = d['480p']
            else:
                final = d['360p']
        elif quality == 'best':
            if 'best' in d:
                final = d['best']
            elif '1080p' in d:
                final = d['1080p']
            elif '720p' in d:
                final = d['720p']
            elif '480p' in d:
                final = d['480p']
            else:
                final = d['360p']
        return final
    
    def get_new_server(self, nurl, quality):
        final = ''
        if 'mycloud' in nurl:
            content = ccurl(nurl)
            tlink = re.search('"file":"[^"]*', content).group()
            link = tlink.replace('"file":"', '', 1)
            if 'http' not in link:
                link = 'https://' + re.search('[a-zA-Z0-9][^"]*', link).group()
            pre_link = link.rsplit('/', 1)[0]
            print(link, pre_link, '--310--')
            content = ccurl(link)
            arr = content.split('\n')
            if '#EXTM3U' in arr[0]:
                arr = arr[1:]
            j = 0
            quality_tuple = []
            for i in arr:
                i = i.strip()
                if i.startswith('#'):
                    link_new = arr[j+1]
                    if i.endswith('x360'):
                        val = ('360p', link_new)
                    elif i.endswith('x480'):
                        val = ('480p', link_new)
                    elif i.endswith('x720'):
                        val = ('720p', link_new)
                    elif i.endswith('x1080'):
                        val = ('1080p', link_new)
                    quality_tuple.append(val)
                j = j + 1
            if quality_tuple:
                quality_dict = dict(quality_tuple)
                tfinal = self.get_quality_dict(quality_dict, quality)
                if tfinal:
                    if tfinal.startswith('/'):
                        tfinal = tfinal[1:]
                    final = pre_link + '/' + tfinal
                print(pre_link, tfinal)
        elif 'rapidvideo' in nurl:
            qd = {'sd':'360p', 'hd':'720p', 'best':'1080p', 'sd480p':'480p'}
            content = ccurl(nurl)
            m = re.findall('sources": \[[^\]]*]', content)
            print(m)
            new_dict = {}
            lb = qd[quality]
            if m:
                nl = m[0].replace('sources": ', '')
                ld = json.loads(nl)
                for i in ld:
                    print(i)
                    key = i['label']
                    val = i['file']
                    new_dict.update({key:val})
                final = new_dict.get(lb)
                if not final and new_dict:
                    if quality == 'best':
                        if '720p' in new_dict:
                            final = new_dict.get('720p')
                        elif '480p' in new_dict:
                            final = new_dict.get('720p')
                        elif '360' in new_dict:
                            final = new_dict.get('360p')
                    if quality == 'hd' and not final:
                        if '480p' in new_dict:
                            final = new_dict.get('720p')
                        elif '360p' in new_dict:
                            final = new_dict.get('360p')
                    if quality == 'sd480p' and not final:
                        if '360p' in new_dict:
                            final = new_dict.get('360p')
        return final 
    
    def getFinalUrl(self, name, epn, mirror, quality):
        new_epn = epn.split('/')[-1]
        if '::' in new_epn:
            id_arr = new_epn.split('::')
            print(id_arr, mirror)
            if mirror <= len(id_arr):
                epn_id = id_arr[mirror-1]
            else:
                epn_id = id_arr[0]
        else:
            epn_id = new_epn
            
        new_url = 'https://9anime.to'+epn.split('::')[0]
        print(new_url)
        
        lnk_file = os.path.join(self.tmp_dir, 'lnk.txt')
        for i in range(0, 2):
            if os.path.exists(lnk_file):
                os.remove(lnk_file)
            if os.path.isfile(self.cookie_file):
                cloudfare(
                    new_url, quality=quality, cookie=self.cookie_file, get_link=True, 
                    get_raw_link='episode/info?', tmp_dir=self.tmp_dir, end_pt='watching')
            else:
                cloudfare(
                    new_url, quality=quality, cookie=self.cookie_file, get_link=True, 
                    get_raw_link='episode/info?', tmp_dir=self.tmp_dir, end_pt='watching', 
                    get_cookie=True)
            if os.path.exists(lnk_file):
                link = open(lnk_file).readlines()
                link = link[0].strip()
                print('----------link', '>>>>>>>>', link)
                final = ''
                try:
                    _api, nurl = self.get_direct_grabber(link)
                    if _api is None:
                        final = self.get_new_server(nurl, quality)
                    else:
                        final = self.get_old_server(_api, nurl, quality)
                except Exception as e:
                    print(e, '--473--')
                if final:
                    break
                else:
                    if os.path.isfile(self.cookie_file):
                        os.remove(self.cookie_file)
                    print('--no-final-url-- trying again--')
                print('try:{0}'.format(i))
        return final
    
    def parse_page(self, url, cookie=None):
        if cookie is None:
            content = ccurl(url)
        else:
            content = ccurl(url+'#-b#'+cookie)
        soup = BeautifulSoup(content, 'lxml')
        arr = []
        m = soup.findAll('div', {'class':'item'})
        for i in m:
            k = i.find('a')['href']
            try:
                l = i.find('img')['alt']
                if l.startswith('.'):
                    l = l[1:]
                if '/' in l:
                    l = l.replace('/', '-')
            except Exception as e:
                print(e)
                l = ''
            n = l+'	'+k
            arr.append(n)
        if not arr:
            if 'make sure your browser supports cookie' in content:
                arr.append('get_cookie')
        return arr
    
    def getCompleteList(self, opt, genre_num):
        m = []
        
        instr = "Press . or > for next page	-1"
        opt_arr = [
            'genre', 'mostpopular', 'newest', 'latestupdate', 
            'history', 'series', 'movies', 'ongoing'
            ]
        self.pg_num = 1
        if opt == 'Genre':
            url = 'https://9anime.to'
            content = ccurl(url)
            m = re.findall('/genre/[^"]*', content)
            m = list(set(m))
            m.sort()
            m.pop()
            j = 0
            for i in m:
                i = re.sub('/genre/', '', m[j])
                m[j] = i
                j = j + 1
            m.append('<--')
            m.append(0)
        elif opt == 'History':
            print('History')
        elif opt == '<--':
            opt_arr.append('<--')
            m = ['Genre', 'MostPopular', 'Newest', 'LatestUpdate', 
                'History', 'Series', 'Movies', 'Ongoing']
            m.append(0)
        elif (opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate' 
                or opt == 'Series' or opt == 'Ongoing' or opt == 'Movies'):
            new_opt = 'newest'
            if opt.lower() == 'mostpopular':
                new_opt = 'most-watched'
            elif opt.lower() == 'newest':
                new_opt = 'newest'
            elif opt.lower() == 'latestupdate':
                new_opt = 'updated'
            elif opt.lower() == 'series':
                new_opt = 'tv-series'
            elif opt.lower() == 'movies':
                new_opt = 'movies'
            elif opt.lower() == 'ongoing':
                new_opt = 'ongoing'
            url = 'https://9anime.to/'+new_opt
            m = self.parse_page(url)
            m.append(instr)
            m.append(1)
            
        if opt.lower() not in opt_arr:
            url = 'https://9anime.to/genre/' + opt
            m = self.parse_page(url)
            m.append(instr)
            m.append(1)
        return m
        
    def getNextPage(self, opt, pgn, genre_num, name, prev_pg=None):
        if prev_pg:
            self.pg_num -= 1
        else:
            self.pg_num += 1
        print(self.pg_num, opt, prev_pg, '--pg--num--')
        if opt and self.pg_num >= 1:
            pgnum = str(pgn)
            if (opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate' 
                    or opt == 'Series' or opt == 'Ongoing' or opt == 'Movies'):
                new_opt = 'newest'
                if opt.lower() == 'mostpopular':
                    new_opt = 'most-watched'
                elif opt.lower() == 'newest':
                    new_opt = 'newest'
                elif opt.lower() == 'latestupdate':
                    new_opt = 'updated'
                elif opt.lower() == 'series':
                    new_opt = 'tv-series'
                elif opt.lower() == 'movies':
                    new_opt = 'movies'
                elif opt.lower() == 'ongoing':
                    new_opt = 'ongoing'
                url = 'https://9anime.to/'+new_opt+'?page='+str(self.pg_num)
            else:
                url = 'https://9anime.to/genre/' + opt + '?page=' + str(self.pg_num)
            print(url)
            arr = self.parse_page(url)
            return arr
                
    def getPrevPage(self, opt, pgn, genre_num, name):
        print('---602--------')
        arr = self.getNextPage(opt, pgn, genre_num, name, prev_pg=True)
        return arr




