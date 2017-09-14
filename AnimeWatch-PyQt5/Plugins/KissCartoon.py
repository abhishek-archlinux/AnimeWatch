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
import inspect
import ipaddress
import json
from player_functions import ccurl, naturallysorted
from player_functions import send_notification, get_hls_path

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
                    '--cookie-end-pt=_gat', '--cookie-domain-name=kimcartoon.me', 
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
                    
            if get_link:
                cookie_found = True
                lnk_file = os.path.join(tmp_dir, 'lnk.txt')
                if os.path.isfile(lnk_file):
                    os.remove(lnk_file)
                hls_exec = [
                    hls_path, url, '--use-cookie-file='+cookie, 
                    '--output=false', '--tmp-dir='+tmp_dir, '--js-file='+js, 
                    '--block-request=.ads, ads., revcontent, .bebi, scorecard, .css', 
                    '--show-window=800x600', '--timeout=30', '--js-progress', 
                    '--js-progress-log=http', 
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

class KissCartoon():
    def __init__(self, tmp):
        global tmp_working_dir
        self.pg_num = 1
        tmp_working_dir = tmp
        self.tmp_dir = tmp
        self.cookie_file = os.path.join(tmp, 'kcookieC.txt')
        if not os.path.exists(self.cookie_file):
            f = open(self.cookie_file, 'w')
            f.close()
        self.js_template = """
        var v = document.getElementById('selectQuality');
        if (v != null){
        var elem = ;
        var val = "";
        var val_length = v.length;
        for(var i=0;i<val_length;i++){
            console.log(v[i]);
            var z = v[i].value;
            var y = v[i].text;
            if (y==elem){val = z;break;}
            }
        if(val==''){val=v[0].value}
        $kissenc.decrypt(val);
        }else{
            var st = document.getElementById("divContentVideo");
            if (st != null){
                console.log(st);
                var srch = st.getElementsByTagName("iframe");
                console.log(srch);
                var sch = srch.item(0).getAttribute("src");
                console.log(sch);
                sch;
            }
        }
        """
        self.js_file = os.path.join(tmp, 'kc.js')
        
    def getOptions(self):
            criteria = ['MostPopular', 'Newest', 'LatestUpdate', 'Genre', 'History', 'newversion']
            return criteria
            
    def ccurlN(self, url):
        content = ccurl(url+'#-b#'+self.cookie_file)
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
        
    def search(self, name):
        if name != '':
            url = 'http://kimcartoon.me/Search/Cartoon/?keyword=' + name
            content = self.ccurlN(url)
            m = re.findall('/Cartoon/[^"]*', content)
            m = list(set(m))
            m.sort()
            j = 0
            for i in m:
                i = re.sub('/Cartoon/', '', i)
                m[j] = i
                if '?id=' in i and '/' in i:
                    nm, ep = i.split('/')
                    m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
                j = j + 1
            return m
    def getEpnList(self, name, opt, depth_list, extra_info, siteName, category):
        if extra_info == '-1':
            arr = []
            return (arr, 'Instructions', 'No.jpg', False, depth_list)
        else:
            epn_num = ''
            if extra_info:
                name, epn_num = name.rsplit('--', 1) 
            
            url = 'http://kimcartoon.me/Cartoon/' + name
            print(url)
            content = self.ccurlN(url)
            soup = BeautifulSoup(content)
            #f = open('/tmp/AnimeWatch/1.txt', 'w')
            #f.write(content)
            #f.close()
            epl = re.findall('/Cartoon/' + name + '[^"]*["?"]id[^"]*', content)
            #if not epl:
            #	epl = re.findall('[^"]*?id=[^"]*', content)
            try:
                img = re.findall('http://kimcartoon.me/Uploads/Etc/[^"]*.jpg', content)
                img_src = ''
                if not img:
                    img_src = soup.find('link', {'rel':'image_src'})
                    if img_src and 'href' in str(img_src):
                        img_link = img_src['href']
                        if not img_link.startswith('http'):
                            if img_link.startswith('/'):
                                img_link = 'http://kimcartoon.me'+img_link
                            else:
                                img_link = 'http://kimcartoon.me/'+img_link
                else:
                    img_link = img[0]
                print(img, img_src, img_link)
                picn = os.path.join(self.tmp_dir, name+'.jpg')
                print(picn)
                if not os.path.isfile(picn):
                    if img:
                        ccurl(img_link+'#'+'-o'+'#'+picn, self.cookie_file)
                    elif img_src:
                        ccurl(img_link+'#'+'-o'+'#'+picn)
            except:
                #picn = '/tmp/AnimeWatch/' + name + '.jpg'
                picn = os.path.join(self.tmp_dir, name+'.jpg')
            j = 0
            for i in epl:
                i = re.sub('/Cartoon/' + name + '/', '', i)
                epl[j] = i
                j = j + 1

            #try:
            soup = BeautifulSoup(content, 'lxml')
            
            summary = ""
            summary1 = ""
            try:
                link = soup.findAll('span', {'class':'info'})
                #link = soup.findAll('div', {'class':'barContent'})
                for i in link:
                    l = (i.text).lower()
                    if "genres" in l or "other name" in l or "country" in l or "date aired" in l or 'status' in l:
                        
                        k = i.findPrevious('p')
                        if 'status' in l:
                            t = k.text
                            t = re.sub('"', '', t)
                            t = re.sub('Views:[^"]*', '', t)
                            summary = summary + t
                        else: 
                            summary = summary + k.text
                    if "summary" in l:
                        j = i.findNext('p')
                        if j:
                            summary1 = j.text
                    
                summary = summary + summary1
                summary = re.sub('\r', '', summary)
                summary = re.sub('\n\n', '\n', summary)
            except:
                summary = 'Summary Not Available'
            epl=naturallysorted(epl)  
            if extra_info and epn_num:
                epl[:] = []
                epl.append(epn_num)
            record_history = True
            return (epl, summary, picn, record_history, depth_list)
    def urlResolve(self, txt):
        m =[]
        
        if isinstance(txt, bytes):
            print("I'm byte")
            content = str((txt).decode('utf-8'))
        else:
            print(type(txt))
            content = str(txt)
            print("I'm unicode")
        n = content.split('\n')
        for i in n:
            j = i.split(':')
            if len(j) > 2:
                if 'Location' in j[0]:
                    k = j[1].replace(' ', '')
                    k = k +':'+j[2]
                    k = k.replace('\r', '')
                    print (k)
                    m.append(k)
        return m
        
    def resolve_link(self, url, quality, qd):
        content = ccurl(url)
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
        if '--' in name and 'id=' in name:
            name = name.split('--')[0]
        url = 'http://kimcartoon.me/Cartoon/' + name + '/' + epn
        print(url)
        quality_dict = {'sd':'360p', 'hd':'720p', 'best':'1080p', 'sd480p':'480p'}
        js = re.sub(
            'var elem =[^;]*;', 'var elem = "{0}";'.format(quality_dict[quality]), 
            self.js_template)
        print(js)
        with open(self.js_file, 'w') as f:
            f.write(js)
        lnk_file = os.path.join(self.tmp_dir, 'lnk.txt')
        if os.path.exists(lnk_file):
            os.remove(lnk_file)
        beta_server = False
        
        if mirror == 2:
            url = url+'&s=beta'
        elif mirror == 3:
            url = url+'&s=rapid'
            content = self.ccurlN(url)
            all_l = re.findall('\$kissenc.decrypt[^\)]*\)', content)
            print(all_l)
            if all_l:
                with open(self.js_file, 'w') as f:
                    f.write(all_l[0])
        print(self.js_template)
        if not os.path.isfile(self.cookie_file):
            final_lnk = cloudfare(
                url, cookie=self.cookie_file, get_link=True, tmp_dir=self.tmp_dir, 
                show_window=True, quality=quality_dict[quality], js=self.js_file, 
                get_cookie=True)
        else:
            final_lnk = cloudfare(
                url, cookie=self.cookie_file, get_link=True, tmp_dir=self.tmp_dir, 
                show_window=True, quality=quality_dict[quality], js=self.js_file)
        if 'rapidvideo' in final_lnk:
            final_lnk = self.resolve_link(final_lnk, quality, quality_dict)
        if final_lnk:
            chk_mir = final_lnk.split('/')[2]
            if ':' in chk_mir:
                chk_mir = chk_mir.split(':')[0]
            try:
                final = []
                ipaddress.ip_address(chk_mir)
                beta_server = True
                if not url.endswith('&s=beta'):
                    url = url+'&s=beta'
                final.append(final_lnk)
                final.append(url)
                final.append('referer sent')
            except Exception as e:
                print(e, '--319--')
                final = ''
                
            if not beta_server:
                content = ccurl(final_lnk+'#'+'-I')
                m = re.findall('Location: [^\n]*', content)
                if m:
                    final = m[-1]
                    final = re.sub('Location: |\r', '', final)
                else:
                    final = final_lnk
        else:
            final = ''
            msg = 'No Link Available. Try Clearing Cache or select Alternate Mirror by pressing keys 1 or 2'
            send_notification(msg)
        return final
        
    def getCompleteList(self, opt, genre_num):
        instr = "Press . or > for next page	-1"
        m = []
        opt_arr = ['genre', 'mostpopular', 'newest', 'latestupdate', 'history']
        new_opt_arr = ['Genre', 'MostPopular', 'Newest', 'LatestUpdate', 'History']
        self.pg_num = 1
        if opt == 'Genre':
            url = 'http://kimcartoon.me/CartoonList/'
            content = self.ccurlN(url)
            m = re.findall('/Genre/[^"]*', content)
            m = list(set(m))
            m.sort()
            m.pop()
            j = 0
            for i in m:
                i = re.sub('/Genre/', '', m[j])
                m[j] = i
                j = j + 1
            m.append('<--')
            m.append(0)
        elif opt == 'History':
            print('History')
            m.append(1)
        elif opt == '<--':
            opt_arr.append('<--')
            m = new_opt_arr
            m.append(0)
        elif opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate':
            url = 'http://kimcartoon.me/CartoonList/' + opt
            pgn = 1
            content = self.ccurlN(url)
            m = re.findall('/Cartoon/[^"]*', content)
            m = list(set(m))
            m.sort()
            j = 0
            for i in m:
                i = re.sub('/Cartoon/', '', i)
                m[j] = i
                if '?id=' in i and '/' in i:
                    nm, ep = i.split('/')
                    m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
                j = j + 1
            m.append(instr)
            m.append(1)
        elif opt.lower() not in opt_arr:
            url = 'http://kimcartoon.me/Genre/' + opt
            pgn = 1
            content = self.ccurlN(url)
            m = re.findall('/Cartoon/[^"]*', content)
            m = list(set(m))
            m.sort()
            j = 0
            for i in m:
                i = re.sub('/Cartoon/', '', i)
                m[j] = i
                if '?id=' in i and '/' in i:
                    nm, ep = i.split('/')
                    m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
                j = j + 1
            m.append(instr)
            m.append(1)
        return m
        
    def getNextPage(self, opt, pgn, genre_num, name):
        if prev_pg:
            self.pg_num -= 1
        else:
            self.pg_num += 1
        if opt and self.pg_num >= 1:
            pgnum = str(self.pg_num)
            if (opt == 'MostPopular' or opt == 'Newest' or opt == 'LatestUpdate'):
                url = 'http://kimcartoon.me/CartoonList/' + opt + '?page=' + pgnum
            else:
                url = 'http://kimcartoon.me/Genre/' + opt + '?page=' + pgnum
                #print(url
            content = self.ccurlN(url)
            m = re.findall('/Cartoon/[^"]*', content)
            m = list(set(m))
            m.sort()
            j = 0
            for i in m:
                i = re.sub('/Cartoon/', '', i)
                m[j] = i
                if '?id=' in i and '/' in i:
                    nm, ep = i.split('/')
                    m[j] = nm+'--'+ep+'	'+'Newest Episode: '+ep
                j = j + 1

            if m:
                return m
                
    def getPrevPage(self, opt, pgn, genre_num, name):
        if opt and self.pg_num >= 1:
            m = self.getNextPage(opt, pgn, genre_num, name, prev_pg=True)
            return m

