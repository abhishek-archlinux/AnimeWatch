# AnimeWatch
AnimeWatch Player acts as Front End for mpv and mplayer. It is not full fledge frontend like smplayer, but it tries to incorporate many new features which are normally absent from any media player frontend designed for linux.

It tries to be a simple media manager for your audio and video collection with special emphasis on your anime collection, along with powerful playing capabilities of mpv and mplayer. You can organise your anime collection properly into various groups and categories such as watching,incomplete etc.. You can create your own group also for any special category in the bookmark section.  It will also keep track of number of episodes that you have watched in a series. It will also manage history ,and you will have complete control over it.

You can fetch fanart and posters from TVDB website. If proper match is not found then you can directly go to the website using inbuilt browser. In the inbuilt browser right click has been tweaked, so that when when you find relevant url of fanart ,poster or anime; you can directly right click on the option to save it as fanart or poster or find anime info. In the same way you can find Episode Names or thumbnails of the anime. If you are in Music section then you can use the inbuilt browser to get artist information and poster directly from Last.fm, if default perfect match is not found.

User can make as many playlists as possible. It is possible to merge various playlists and you can create playlist of both audio and video.

Users can see their entire collection in Thumbnail mode in Grid Layout, once your collection is ready with appropriate fanart or posters. Use this thumbnail mode if you have more than 2 GB of RAM. Otherwise your system may slow down. 

In thumbnail mode, Thumbnails of local video files are automatically generated with the help of 'ffmpegthumbnailer'.You can watch video in thumbnail mode itself by right clicking and selecting appropriate option. If you don't like generated thumbnail then right click it and select another.

It supports certain D-bus functionalities. Therefore if you have created global keyboard shortcuts for play/pause,Next,Previous or Stop then they can work with this player also. 

It is possible also to change default background image by simply replacing '~/.config/AnimeWatch/default.jpg' with another wallpaper of your choice and rename it to 'default.jpg' 

It is not very powerful music organizer, but provide certain decent functionalities. When using with mplayer, it's cpu usage is just 1-2 % which makes it very ideal for low end machines.

#Addon (Plugins) Structure

In this player, a weak addon structure has been created, so that one can write addon for viewing video contents of various sites directly on this player,similar to Kodi or Plex, so that you don't have to deal with horrible flash player of the web. Currently it supports certain anime sites. By default it shows SD video, if you select HD then whenever available it tries to pick up HD video. If multiple mirrors are available you will be notified about it and then you can select different mirror if default mirror fails.These extra addons are in the directory 'Plugins', which will be loaded once the application is started. These addons are optional and before using them please check copyright and licencing laws of your country. If viewing contents of these anime sites is not allowed in your country, then use it at your own risk. Author of the AnimeWatch player is not at all related to any of these anime sites or their content provider. And these addons are also not core part of the player, they are completely optional,it's decision of the user of this application to download and keep these addons or not. These addons will only feed videos of the website directly to desktop player without downloading. There is no warrantee or guarantee on these addons. They can become dead if the site on which they are depending becomes dead or changes it's source. After install, these addons will be in the directory '~/.config/AnimeWatch/src/Plugins'. If your country does not allow viewing contents of these anime sites, then you can simply delete contents of the 'Plugins' folder.

Most of the above things are possible in KODI or Plex . But I wanted some simple player with either mpv or mplayer as backend with decent media management functionality and addon structure. Therefore, I decided to create the application.

This player is made only for GNU/Linux systems.
It is developed mainly on Arch Linux and Tested on both Arch and Ubuntu 14.04.

#Dependencies and Installation:
(This player is mainly written in pyqt4 and python3)

python3

python-pyqt4

python-requests

python-urllib3

python-pillow

python-beautifulsoup4

python-lxml

python-pip

python-pycurl

python-psutil

curl

wget

ffmpegthumbnailer

phantomjs

libnotify

pytaglib

jsbeautifier(optional: required for resolving certain links)

mpv or mplayer (having both is good option, for streaming video mpv is the best because it's seeking capability within live stream is very efficient and it's buffer management is also very good, and for listening music mplayer is very cost-effective. Cpu usage is just 1 to 2 % when playing music with mplayer. When playing local video files mplayer cpu utilization always remains 4-5 % point less than that of mpv atleast on my system)

#In arch installation.

sudo pacman -S python python-pyqt4 python-requests python-urllib3 python-pillow python-beautifulsoup4 python-lxml python-psutil python-pip curl wget libnotify mpv mplayer phantomjs ffmpegthumbnailer sqlite3

(pytaglib is available in AUR but I preferred to install it from pip)

sudo pip install pytaglib jsbeautifier

#In ubuntu 14.04, default python points to python 2.7, hence for installing dependencies use following command

sudo apt-get install python3 python3-pyqt4 python3-requests python3-urllib3 python3-pil python3-bs4 python3-lxml python3-psutil python3-taglib python3-pip curl wget libnotify-bin mpv mplayer phantomjs ffmpegthumbnailer sqlite3

sudo pip3 install jsbeautifier (optional)

#Once Dependencies are installed Download the folder. Goto AnimeWatch Directory. Open Terminal in the directory and use following command:

#In Arch:

python install.py

#In Ubuntu 14.04:

python3 install.py

During Installation,it will ask for root password for copying AnimeWatch.desktop file in directory “/usr/share/applications/” , so that application launcher can become visible in menu “Sound & Video” or "Multimedia" section. If you don't want to give root password then press 'ctrl+c' and cancel the copying process, and manually copy file '~/.config/AnimeWatch/AnimeWatch.desktop' to the directory '/usr/share/applications/'

All other configuration files will be created in "~/.config/AnimeWatch/"

If Application Launcher in the menu is not working or programme is crashing then directly go to "~/.config/AnimeWatch/src/", open terminal there and run "python3 animeWatch.py" or "python animeWatch.py" as per your default python setup. If there is some problem in installation, then you will get idea about it, whether it is missing dependency or something else, or you can report the error as per the message in terminal.

#Brief Documentation:

If everything goes well and if you are able to open the player, then you will come across Three Columns.

First Column, At the Leftmost, is the 'Settings' column. Just click on the library, and add paths to your media. You can choose either mpv or mplayer. Default is mpv.

I've little bit tweaked mplayer functionality especially relating to it's buffer management. If you are on low bandwidth network and mplayer goes out of cache, then it keep on stuttering but does not stop. But I've written small wrapper around mplayer, now as soon as it goes out of buffer, it will stop for 5 seconds. When it stops for filling the buffer, you can pause it manually for larger duration. In normal mplayer functioning, once it starts stuttering due to lack of cache, it is also difficult to pause manually. I really don't know, why developers of mplayer don't pay attention to this simple problem. In this regard, mpv has done really excellent job.
It's your choice which player to choose.

If you are still not satisfied with mpv or mplayer, then you can also launch any of the external player such as vlc,smplayer or kodi. Currently the AnimeWatch supports only these three external players apart from mpv and mplayer, which are internal.

Middle column, is the “Title Column”, It will consists of name of the series.
Last Column to the extreme right, is the “Playlist column”, which will contain playlist items which will be played sequentially in the default mode, you will just have to select entry and press enter or double click.

#KeyBoard Shortcuts:

Once video is opened, if it not focussed then take mouse pointer over the video. It will set focus on the video. Once the video is focussed, most of the mpv and mplayer shortcuts will work. There is no volume slider, it's volume will be in sync with global volume. So global volume key will work. If you've setup d-bus shortcut keys for play/pause/next/previous then they will also work.

There is no fullscreen button and play/pause button. People have to use keyboard shortcuts(f:fullscreen; spacebar:play/pause). It is not full fledge front end, the player has been written with different aim in mind. Therefore, i've tried to reduce buttons as much as possible so as not to clutter the interface, especially with respect to player. But if you still feel the need for more buttons then you can select smplayer or vlc or kodi from settings menu, or you can request the feature. If it does not clutters the interface more, then I'll think about adding it.

#Player Shortcuts(once video is focussed, if it's not focussed take mouse cursor over the playing video):

q : quit

spacebar: play/pause

f : fullscreen

w : decrease size

e : increase size

r : move subtitle up

t : move subtitle down

i : show file size

j : toggle Subtitle

k : toggle audio

m : show video file name

. (remember '>' key) : next file in the playlist or queue

, (remember '<' key) : previous file in the playlist

right : 10s+

left  : 10s-

Up    : 60s+

Down  : 60s-

PgUp  : 300s+

PgDown : 300s-

0 : 90s+

9 : 5s- 

a : change aspect ratio (works with mpv: default aspect is 16:9 for mpv)


for mplayer set aspect in ~/.mplayer/config, all the properties of the mplayer global config file will be taken by the internal mplayer.

Some important parameters that you should set in '~/.mplayer/config' are as follows:

http-header-fields="User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:43.0) Gecko/20100101 Firefox/43.0" {or any other user-agent}

aspect="16:9"

ass=true

cache=100000

cache-min=0.001

cache-seek-min=0.001 

prefer-ipv4=yes

ao=pulse

vo=gl

You can change the parameters as per your choice.

Similarly, most of the properties of mpv global config file '~/.mpv/config/' will work with this player. If possible you should add following line in mpv config file.

user-agent="Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:43.0) Gecko/20100101 Firefox/43.0" {or any other user-agent}

ao=pulse 

vo=opengl {or anything that works on your system}

#Some global Shortcuts:
L : show/hide Player

g : show/hide Settings column

shift+f: fullscreen Application not the player

ctrl+x : show/hide Browser

ctrl+z : show/hide Thumbnail mode (Thumbnail Mode is memory consuming, hence use it carefully if you have very big library collection)

Escape : Hide/Show Everything

Right,Left: set focus alternate between Option column, Title column and Playlist column (If Player is not Playing Anything)

#Title Column:(if Title list is focussed)

h : show history (history of watched series)

Delete : delete particular item of history

r : randomize the list(if you want random series)

t : sort the Title List

PgUp: Move Entry UP

PgDown: Move Entry Down

#Playlist Column:(If playlist column is focussed)

q : queue the item

Delete : delete particular entry

1 – 9 : select mirror Number (up to 9)

s : select SD quality

h : select HD quality

w : toggle watch/unwatch

PgUp: Move Entry UP

PgDown: Move Entry Down

#Thumbnail Mode:

= : increase size of Thumbnails

- : decrease size of Thumbnails

#Thumbnail mode occupies pretty good memory. If you want to get out of thumbnail mode and free up the memory then click 'close' button which is available in thumbnail mode.

#Apart from shortcuts:
You can explore Right click menu of both Playlist Column and Title List Column for getting TVDB, Last.fm profiles for your collection either manually or automatically. If you are getting some problem while setting profiles from TVDB or Last.fm , or having problems accessing addons,then empty the cache directory '/tmp/AnimeWatch/', This option is available with right click menu of Title List and Playlist column also.

#Other Things for convenience:

Please Enable Vertical Scrolling of Touchpad, because there are no scrollbars in this app, because they were looking very ugly in the total setup.

In LXDE you can insert following command in autostart file to enable vertical scrolling

'synclient VertEdgeScroll=1'

In LXDE, for setting global shortcuts for: Play,Pause,Next,Previous; assign keyboard shortcuts to following commands in Openbox lxde-rc.xml

1. bash -c 'player=$(qdbus-qt4 org.mpris.* | grep MediaPlayer2 | head -n 1); qdbus-qt4 $player /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next'

2. bash -c 'player=$(qdbus-qt4 org.mpris.* | grep MediaPlayer2 | head -n 1); qdbus-qt4 $player /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous'

3. bash -c 'player=$(qdbus-qt4 org.mpris.* | grep MediaPlayer2 | head -n 1); qdbus-qt4 $player /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause'


#Few ScreenShots
![Sample](/Images/Video.png)