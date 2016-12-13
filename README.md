# AnimeWatch

AnimeWatch Player acts as Front End for mpv and mplayer. It is not full fledge frontend like smplayer or vlc, but it tries to incorporate many new features which are normally absent from most of the media player frontend designed for GNU/linux systems.

## Index

[Features](#features)

[Normal Mode](#normal-mode)

[Playing Mode](#playing-mode)

[Thumbnail Mode](#thumbnail-mode)

[Minimal Music Player](#minimal-music-player)

[Detached Video Mode](#detached-video-mode)

[Torrent Streaming Player] (#torrent-streaming)

[Media Server](#media-server)

[YouTube Player](#youtube-support)

[Addons (Plugins) Structure] (#addon-structure)

[Dependencies and Installation](#dependencies-and-installation)

[Troubleshooting](#troubleshooting)

[Brief Documentation](#documentation)

## Features

1.  Combine Audio-Video Player and Manager with special emphasis on Anime collection.

2.  Bookmark and categorize series in the library (like Watching, Incomplete, Interesting etc..).

3.  Good audio-video management functionalities using sqlite3.

4.  Custom Addons Support for viewing content of various sites directly on the player.

5.  Support for downloading fanart/posters and other information such as summary or biography from internet sites such as TVDB and last.fm.

6.  Thumbnail Grid Mode Support.

7.  Internal web browser with custom right click menu for manually downloading desired fanart and poster for library collection.

8.  System Tray Support (Current tray icon is temporary which may change in future).

9.  Proper MPRIS2 support and integration with sound menu applet.

10. Custom Playlist and queueing support.

11. Remembers most of the last settings, and can opens up directly last watched series in the library.

12. Special Minimal Mode Music Player for listening only music (Available in System Tray context menu).

13. Proper History Manager for both addons and local content.

14. Bookmark support for both Audio, Video and Addons.

15. mplayer/mpv internal player.

16. Better buffer management for mplayer on low bandwidth network.

17. Support for opening video in external players like vlc, smplayer or kodi.

18. Torrent streaming player.

19. Media Server capability.

20. Youtube wrapper using qtwebengine/qtwebkit.

21. Detached Video Mode

## Normal Mode 
######[Index](#index)
![AnimeWatch](/Images/Video.png)

## Playing Mode
######[Index](#index)
![AnimeWatch](/Images/Watch.png)

It tries to be a simple media manager for your audio and video collection with special emphasis on your anime collection, along with powerful playing capabilities of mpv and mplayer. You can organise your anime collection properly into various groups and categories such as watching,incomplete etc.. You can create your own group also for any special category in the bookmark section.  It will also keep track of number of episodes that you have watched in a series. It will also manage history ,and you will have complete control over it.

You can fetch fanart and posters from TVDB website. If proper match is not found then you can directly go to the website using inbuilt browser. In the inbuilt browser right click has been tweaked, so that when when you find relevant url of fanart ,poster or anime; you can directly right click on the option to save it as fanart or poster or find anime info. In the same way you can find Episode Names or thumbnails of the anime. If you are in Music section then you can use the inbuilt browser to get artist information and poster directly from Last.fm, if default perfect match is not found.

User can make as many playlists as possible. It is possible to merge various playlists. Users can combine local audio, local video and external url into the playlist.

## Thumbnail Mode
######[Index](#index)
![AnimeWatch](/Images/Thumbnail.png)

Users can see their entire collection in Thumbnail mode in Grid Layout, once your collection is ready with appropriate fanart or posters. Use this thumbnail mode if you have more than 2 GB of RAM. Otherwise your system may slow down. 

In thumbnail mode, Thumbnails of local video files are automatically generated with the help of 'ffmpegthumbnailer'.You can watch video in thumbnail itself by selecting right mode from 2 to 4. If you don't like generated thumbnail then you can change it by right clicking and selecting appropriate option from the context menu.

## Minimal Music Player
######[Index](#index)
![AnimeWatch](/Images/Music.png)

It supports certain D-bus functionalities. Therefore if you have created global keyboard shortcuts for play/pause,Next,Previous or Stop then they can work with this player also. 

It is not very powerful music organizer, but provide certain decent functionalities. When using with mplayer, it's cpu usage is just 1-2 % which makes it very ideal for low end machines.

## Detached Video Mode
######[Index](#index)
![AnimeWatch](/Images/Detached_Mode.png)

The Player contains Detached video mode, which can be activated by right clicking tray icon and selecting appropriate entry.
In this mode, video will be detached from the main application window and can float anywhere on the desktop. By default it has titlebar, which users can remove by activating frameless mode from system tray context menu. Users can make this detached video of any size and can position it anywhere on the desktop which will remain above all the windows. In lightweight desktop sessions like LXDE there is very simple sound menu applet which does not integrate music and any other extra functionalities. By using this mode, it is possible to use it as a system tray widget with many advance features with which you can quickly control your media (both audio and video) which is being played in the player, similar to sound menu applet of Unity or GNOME.

## Torrent Streaming
######[Index](#index)
Torrent Streaming feature has been included since version 2.5.0-0. Now it is possible to play audio/video torrent directly with this player similar to any streaming media. By default the torrent will stream at 'http://127.0.0.1:8001', which is loop-back address of your local machine. You can change this default streaming IP and port location by manually editing 'torrent_config.txt' file located in '~/.config/AnimeWatch'. If you set 'TORRENT_STREAM_IP' field to your local network IP address which normally starts with something like '192.168.x.y' (You can check default ip using 'ifconfig' command), then it is possible to access the playing media from any device on your local network. For example, if the media is being played at computer A with TORRENT_STREAM_IP set to your default local ip address '192.168.1.1:8001', then you can access that media from computer B on the same network by simply connecting to 'http://192.168.2.1:8001'. If you have mplayer or mpv installed on computer B , then you can simply type the command 'mplayer http://192.168.2.1:8001' on that computer, to access the media which is being streamed on computer A. 

In 'torrent_config.txt' you can set some other fields like upload , download rate in (KBps) and default download location.

Now with inclusion of torrent streaming feature, it's possible to write addons based on torrenting capability.

For opening torrents within this player, goto Addons->Torrent->Open and enter torrent file name or torent url or magnet link inside the input dialog box, and then select appropriate entry which will appear in either Title list or Playlist. Your list of visited torrents will be accessible from the 'History' section. 

Alternatively, Torrent file can be directly played by opening it with AnimeWatch using right-click context menu. If you've installed AnimeWatch using .deb or AUR package, then you can use command 'anime-watch path_to.torrent' to open torrent file, or 'anime-watch magnet_link' for opening magnet links. Those who have installed the player using common method, have to use the command 'python -B ~/.config/AnimeWatch/src/animeWatch.py path_to.torrent_or_magnet_link'.

This feature is based on libtorrent-rasterbar {which is being used by bittorrent clients like qBittorrent and deluge} and it's python3 bindings. If you've installed latest version of libtorrent-rasterbar then python3 bindings are included along with it. In systems where older version of libtorrent-rasterbar is installed (for example in Ubuntu 14.04) , users need to install python3-libtorrent to use this feature.  

If you are using mpv as backend for watching streaming torrent then it might be possible that seeking within the stream won't work. Therefore, in order to enable seeking within torrent stream forcibly using mpv, open '~/.mpv/config' file and insert line 'force-seekable=yes' into it. Seeking within torrent is not perfect, and sometime playback stops. In such case, first focus the video by taking mouse pointer over the video and press key 'q' to quit the current playing instance, and then restart the video again. If you click 'Stop' button in the AnimeWatch player, then along with quitting current playing instance, it will stop Torrent also. Therefore, if you want torrent to continue, and only restart of the the internal player then use key 'q'.

If torrent contains multiple files then users can enqueue the desired files by selecting appropriate entry in Playlist column and pressing 'key q'.
 
Note: Key 'q' used on playing video will quit the playing instance, and the same key 'q' used on playlist column will queue the item.

## Media Server
######[Index](#index)
From version 2.6.0-0, it's possible to use AnimeWatch player as media server. The media server functionality can be started by clicking 'More' button, and selecting 'Start Media Server' option. By default media server will start on 'http://127.0.0.1:9001' i.e. default loop-back address of your machine. In order to use it as media server which can be accessed from any device on the same local network, you have to change this loop-back address '127.0.0.1' to your local network address which normally starts with '192.168.x.y'. You can check, default local network address using cli tools like 'ifconfig' on any gnu/linux based systems. Once you know local network address of your server, then manually edit '~/.config/AnimeWatch/other_options.txt' file and change the field "LOCAL_STREAM_IP" appropriately with local network address. Once you've set up the 'LOCAL_STREAM_IP' field properly, then you should be able to access the current playlist on the AnimeWatch, from any device on the network. 

For example, if server address is set to '192.168.1.1:9001', then you should be able to access the current selected file in the playlist at the address 'http://192.168.1.1:9001/play'. Next and previous files in the playlist can be accessed using url's 'http://192.168.1.1:9001/next' and 'http://192.168.1.1:9001/prev' respectively.

Note: You need to use separate port number for media server and torrent streaming feature. Port number along with local IP for torrent streaming feature needs to be set in 'torrent_config.txt' (TORRENT_STREAM_IP field) and that of media server in 'other_options.txt' (LOCAL_STREAM_IP field). 
Default Settings: 'TORRENT_STREAM_IP=127.0.0.1:8001' and 'LOCAL_STREAM_IP=127.0.0.1:9001'. In default settings one can't access local media from another computer. Users need to change default loopback address to local ip address. Users have to set local IP address and port once only. If local IP address of the media server changes dynamically next time, then the AnimeWatch application will try to find out new address automatically. If the application can't find new address then users have to manually change the config files again.

## YouTube Support
######[Index](#index)
![AnimeWatch](/Images/YT.png)

This player provides a wrapper around youtube site using qtwebengine (since version 2.8.0-0). If your GNU/linux distro does not package qtwebengine, then it will fallback to qtwebkit, which is slower compared to qtwebengine for rendering web pages. Users need to install youtube-dl for directly playing youtube videos on this player. In this wrapper users will get complete functionality of youtube site, but with better control over video and playlist. Users can add any youtube video url into the local playlist or they can import entire youtube playlist as local playlist. It also supports downloading youtube subtitles/captions (If available). If subtitles are availble and downloaded by the player, then usesrs need to press 'Shift+J' (Focus the player by taking mouse pointer over the playing video, before using this shortcut key combination) to load the subtitles into the player. It also supports offline mode, if users have fluctuating internet connection. Before using offline mode users need to add youtube url into local playlist.

## Addon Structure
######[Index](#index)
In this player, a weak addon structure has been created, so that one can write addon for viewing video contents of various sites directly on this player,similar to Kodi or Plex, so that you don't have to deal with horrible flash player of the web. Currently it supports certain anime sites. By default it shows SD video, if you select HD then whenever available it tries to pick up HD video. If multiple mirrors are available you will be notified about it and then you can select different mirror if default mirror fails.These extra addons are in the directory 'Plugins', which will be loaded once the application is started. These addons are optional and before using them please check copyright and licencing laws of your country. If viewing contents of these anime sites is not allowed in your country, then use it at your own risk. Author of the AnimeWatch player is not at all related to any of these anime sites or their content provider. And these addons are also not core part of the player, they are completely optional,it's decision of the user of this application to download and keep these addons or not. These addons will only feed videos of the website directly to desktop player without downloading. There is no warrantee or guarantee on these addons. They can become dead if the site on which they are depending becomes dead or changes it's source. After install, these addons will be in the directory '~/.config/AnimeWatch/src/Plugins'. If your country does not allow viewing contents of these anime sites, then you can simply delete contents of the 'Plugins' folder.

Most of the above things are possible in KODI or Plex . But I wanted some simple player with either mpv or mplayer as backend with decent media management functionality and addon structure. Therefore, I decided to create the application.

This player is made mainly for GNU/Linux systems. But probably it should work on BSD and other Unix-like systems, if dependencies are satisfied. ~~And one thing is sure it can't work on Windows.~~From version 4.0 onwards the player might work on Windows too if dependencies are satisfied. 

It is developed mainly on Arch Linux and Tested on both Arch and Ubuntu 14.04(PyQt4 version) and ubuntu 16.04(PyQt5 version).

## Dependencies and Installation
######[Index](#index)

1. For Arch Linux users, AnimeWatch is available in AUR as [animewatch-pyqt4](https://aur.archlinux.org/packages/animewatch-pyqt4) , [animewatch-pyqt5](https://aur.archlinux.org/packages/animewatch-pyqt5) and [animewatch-pyqt5-git](https://aur.archlinux.org/packages/animewatch-pyqt5-git) (thanks to Arch linux forum member **sesese9**). Arch users can install it using 'yaourt' or any other conventional method. Addons of pyqt4 and pyqt5 version are incompatible. Hence whenever user upgrade pyqt4 version to pyqt5 or downgrade pyqt5 version to pyqt4, then they have to manually remove '~/.config/AnimeWatch/src/' directory, before restart of newly upgraded or downgraded version. Otherwise player won't load addons or might even crash.  

2. Ubuntu or Debian based distro users can directly go to Release section or package directory,download appropriate .deb package and install it using
 
		sudo gdebi pkg_name.deb. 

   If 'gdebi' is not installed then install it using 

		'sudo apt-get install gdebi'. 

   **gdebi** will resolve all the dependencies while installing the package. Normally **dpkg -i** is used for installing .deb package in Debian based distros, but 'dpkg' won't install dependencies automatically, which users have to install manually as per instructions given below. Hence try to use **gdebi** for convenience. Ubuntu 14.04 users also have to install 'python3-dbus.mainloop.qt' for MPRIS2 support. ~~Pyqt5 version is not available for Ubuntu, since qt5-webengine is not availbale on it. Currently there are no significant featurewise differences between pyqt5 and pyqt4 version, there are only structural differences. Users won't notice any significant variation between the two while using.~~. PyQt5 version is now available for Ubuntu 16.04 (from version number 2.8.0-0 onwards) which uses qtwebkit in fallback mode if qtwebengine is not available. For removing the package use 'sudo apt-get remove animewatch'. PyQt5 version won't work on Ubuntu 14.04.

   Note: From version number 2.8.0-0 onwards, only PyQt5 version will be available. It is difficult to maintain two different versions (i.e. PyQt4 and PyQt5) of the same programme. AnimeWatch 2.7.0-0 was the last PyQt4 release. All the subsequent release will be PyQt5 only.

3. Using **setup.py** located in **Python-SETUP** directory: 
   
   First clone the repository then execute following commands.

		$ cd Python-SETUP
		$ python setup.py sdist (or python3 setup.py sdist)
		$ cd dist
		$ sudo pip3 install 'pkg_available_in_directory'
	
	pip3 will essentially install most of the python-based dependencies along with the package. Users only have to install non-python based dependencies such as mplayer/mpv,ffmpegthumbnailer,libtorrent and curl/wget manually. On windows ffmpegthumbnailer is not available, hence thumbnails will be generated by either mpv or mplayer itself.
	
	Note: GNU/Linux distros should install PyQt5 and other python based dependencies from their own repositories using their native package manager instead of using pip, in order to avoid conflicting files or other dependecies problems due to differing naming schemes of the package. They should remove or comment out the 'install_requires' field in the setup.py, before using this method.
	
	Once application is installed, launch the application using command **animewatch** from the terminal.

4. Common Method: Users have to manually install all the dependencies listed below. Then they should clone the repository and go to AnimeWatch-PyQt5 or AnimeWatch-PyQt4-Stable directory. Open terminal in that directory and run 'python3 install.py' (or 'python install.py' if default python points to python3). Application launcher will be created in '~/.local/share/applications/'.
Or they can simply click on (or execute using command line) **'animewatch-start'** shell script located in the directory to start the player directly **without copying files anywhere**.


#Dependencies
######[Index](#index)

**Minimum Dependencies on GNU/Linux:** 

python3 {Main Language}

python-pyqt5 (Main GUI Builder)

python-pillow {For Image Processing}

python-beautifulsoup4 {For scrapping webpage}

python-lxml {Internal parser used in beautifulsoup4 for advance features}

python-pycurl (or curl or wget alternative) {Main library for fetching web pages}

pytaglib or mutagen (required for Tagging of audio files)

sqlite3 (for managing local music and video database, Addons are not managed by it. Addons are managed using files.)

mpv or mplayer. (for playing media)

ffmpegthumbnailer(Thumbnail Generator for Local Files)

**For extra features such as Youtube support, torrent streaming, MPRIS D-Bus support and desktop notifications:**

libtorrent-rasterbar {since version 2.5.0-0, For Torrent Streaming Support}

python3-libtorrent (for Ubuntu 14.04 and 16.04, since version 2.5.0-0)

youtube-dl {for YouTube Support}

python3-dbus {for MPRIS DBus support}

libnotify(required for Desktop Notification)

curl or wget {In case pycurl doesn't work}

python-psutil

python-pyqt4 (for PyQt4 version, which is not maintained now. AnimeWatch-2.7.0-0 was the last pyqt4 release)

**Dependencies installation in Arch for pyqt5 version.**

sudo pacman -S python python-pyqt5 qt5-webengine python-dbus python-pycurl python-urllib3 python-pillow python-beautifulsoup4 python-lxml python-psutil curl libnotify mpv mplayer ffmpegthumbnailer sqlite3 libtorrent-rasterbar youtube-dl wget

**In ubuntu 14.04, default python points to python 2.7, hence for installing dependencies use following command**

In ubuntu 14.04 only pyqt4 version can work

sudo apt-get install python3 python3-pyqt4 python3-pycurl python3-urllib3 python3-pil python3-bs4 python3-lxml python3-psutil python3-taglib curl libnotify-bin mpv mplayer ffmpegthumbnailer sqlite3 python3-libtorrent


~~PyQt5 version can't work on Ubuntu since qt5-webengine is not available on it as dependency.~~

AnimeWatch-PyQt5 from version number 2.8.0-0 onwards can be installed on ubuntu (16.04 or higher) or any other distro which does not package qt5-webengine. In case qt5-webengine is not packaged in the distro, it will use qtwebkit in fallback mode.

**Dependencies installation in Ubuntu 16.04**

sudo apt-get install python3 python3-pyqt5 python3-pycurl python3-urllib3 python3-pil python3-bs4 python3-lxml python3-psutil python3-taglib curl wget libnotify-bin mpv mplayer ffmpegthumbnailer sqlite3 python3-libtorrent python3-livestreamer youtube-dl python3-dbus.mainloop.pyqt5 python3-pyqt5.qtwebkit python3-dbus

**Once Dependencies are installed Download the Appropriate folder (AnimeWatch-PyQt5 or AnimeWatch-PyQt4-Stable) containing 'install.py' file. Open Terminal in the directory and use following command:**

**In Arch:**

python install.py

**In Ubuntu 14.04,16.04:**

python3 install.py

Application Launcher will be created as "~/.local/share/applications/AnimeWatch.desktop"

All other configuration files will be created in "~/.config/AnimeWatch/"

**Uninstall**

Simply remove the application launcher '~/.local/share/applications/AnimeWatch.desktop' and clear the directory '~/.config/AnimeWatch/src/'. If you want to remove all configuration files also, then simply delete directory '~/.config/AnimeWatch/'. Once you delete the configuration directory, all the settings will be lost.


## Troubleshooting
######[Index](#index)

1. If you've installed the Application using .deb or .pkg.tar.xz package or using PKGBUILD, and somehow application launcher in the menu is not working, then open terminal and launch the application using command 'anime-watch' or 'python -B /usr/share/AnimeWatch/animeWatch.py' or 'python3 -B /usr/share/AnimeWatch/animeWatch.py'.

2. If addons are not working after some time or fanart/poster are not fetched properly, then try clearing the cache directory '~/.config/AnimeWatch/tmp/'. If users have some problems in using qtwebengine, then try clearing cache directory for qtwebengine '~/.config/AnimeWatch/Cache/'.

3. If application is crashing after certain update, then it might be possible that it may be due to incompatibility or mismatch between addons of different versions, or certain configuration issues or addition/deletion of certain addons. In such cases remove config file '~/.config/AnimeWatch/src/config.txt' manually, and then restart the application. If removing only config file doesn't work then remove both addons directory '~/.config/AnimeWatch/src/' and config file '~/.config/AnimeWatch/src/config.txt' manually, and then restart the application.

4. In order to update addons manually , download or clone the github AnimeWatch directory, then go to github 'AnimeWatch-PyQt5/Plugins' directory (or AnimeWatch-PyQt4-Stable/Plugins depending upon which version you've installed) , you will find 'installPlugins.py' file there, open terminal in the directory, run the command 'python installPlugins.py' or 'python3 installPlugins.py'. It will update the addons. Or simply copy content of github 'Plugins' directory (except installPlugins.py file) into '~/.config/AnimeWatch/src/Plugins'.

5. If the status text of the player fluctuates a lot due to frequent changes in cache text duration, while using mpv as backend, then you need to set 'cache-secs' field properly in '~/.mpv/config' file. Sample fields and their values required to be set up in '~/.mpv/config' or '~/.mplayer/config' for better performance are listed in the Documentation section. 

6. Sometimes application launcher does not launch the application because of some configuration issues in .desktop file. In such cases try changing 'Terminal=True' to 'Terminal=false' in the file '/usr/share/applications/AnimeWatch.desktop'. If it does not solve the problem then open terminal and execute the command 'anime-watch' to see the error output.

7. In Plsma 5.8, the application does not close even after clicking on close button on title bar or using ALT+F4. Therefore, plasma users have to exit application by right clicking the tray icon and selecting the exit option, or using exit button in player itself. Tray icon remains hidden in the plasma panel, which users need to first un-hide by manually adjusting plasma tray settings. 

8. On Windows if 'lxml' can't be installed using pip then try finding binary available for it from other sources on the internet.

9. On Windows, If fetching of web pages is very slow using pycurl, then try changing pycurl to 'curl' or 'wget' in 'other_options.txt' file located in '~\.config\AnimeWatch' folder.

####Troubleshooting for common method

1. If Application Launcher in the menu is not working or programme is crashing then directly go to "~/.config/AnimeWatch/src/", open terminal there and run "python3 animeWatch.py" or "python animeWatch.py" as per your default python setup. If there is some problem in installation, then you will get idea about it, whether it is missing dependency or something else, or you can report the error as per the message in terminal.

2. If you do not find application launcher in the menu then try copying manually "~/.config/AnimeWatch/AnimeWatch.desktop" to either "~/.local/share/applications/" or "/usr/share/applications/"

3. In LXDE, XFCE or Cinnamon ,any new entry of launcher in '~/.local/share/applications/' is instantly shown in Start Menu (In the case of this player, entry will be shown either in Multimedia or Sound & Video). In Ubuntu Unity you will have to either logout and login again or reboot to see the entry in Unity dash Menu.

## Documentation
######[Index](#index)

If everything goes well and if you are able to open the player, then you will come across Three Columns.

First Column, At the Leftmost, is the 'Settings' column. Just click on the library, and add paths to your media. You can choose either mpv or mplayer. Default is mpv.

I've little bit tweaked mplayer functionality especially relating to it's buffer management. If you are on low bandwidth network and mplayer goes out of cache, then it keep on stuttering but does not stop. But I've written small wrapper around mplayer, now as soon as it goes out of buffer, it will stop for 5 seconds. When it stops for filling the buffer, you can pause it manually for larger duration. In normal mplayer functioning, once it starts stuttering due to lack of cache, it is also difficult to pause manually. I really don't know, why developers of mplayer don't pay attention to this simple problem. In this regard, mpv has done really excellent job.
It's your choice which player to choose.

If you are still not satisfied with mpv or mplayer, then you can also launch any of the external player such as vlc,smplayer or kodi. Currently the AnimeWatch supports only these three external players apart from mpv and mplayer, which are internal.

Middle column, is the “Title Column”, It will consists of name of the series.
Last Column to the extreme right, is the “Playlist column”, which will contain playlist items which will be played sequentially in the default mode, you will just have to select entry and press enter or double click.

###KeyBoard Shortcuts:

Once video is opened, if it not focussed then take mouse pointer over the video. It will set focus on the video. Once the video is focussed, most of the mpv and mplayer shortcuts will work. There is no volume slider, it's volume will be in sync with global volume. So global volume key will work. If you've setup d-bus shortcut keys for play/pause/next/previous then they will also work.

There is no fullscreen button. People have to use keyboard shortcut(f:fullscreen). It is not full fledge front end, the player has been written with different aim in mind. Therefore, i've tried to reduce buttons as much as possible so as not to clutter the interface, especially with respect to player. But if you still feel the need for more buttons or full fledged UI then you can select smplayer or vlc or kodi from settings menu instead of mpv or mplayer. 

###Player Shortcuts(once video is focussed, if it's not focussed take mouse pointer over the playing video):

q : quit

spacebar: play/pause

f : fullscreen

w : decrease size

e : increase size

r : move subtitle up

t : move subtitle down

i : show file size

j : toggle Subtitle

Shift+j: If available, Load external subtitles from folder '~/.config/AnimeWatch/External-Subtitle'. (Staring name of external-subtitle file should match name in the playlist entry)

k : toggle audio

L : Show/Hide Player Controls

m : show video file name

. (remember '>' key) : next file in the playlist or queue

, (remember '<' key) : previous file in the playlist

right : 10s+

left  : 10s-

Up    : 60s+

Down  : 60s-

PgUp  : 300s+

PgDown : 300s-

] : 90s+

[ : 5s-

0 : volume up

9 : volume down 

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

cache-secs=120

###Some global Shortcuts:
Shift + L : show/hide Player

shift + G : show/hide Settings column

Shift + F: fullscreen Application not the player

Ctrl + X : show/hide Browser

Ctrl + Z : show/hide Thumbnail mode for Title list (Thumbnail Mode is memory consuming, hence use it carefully if you have very big library collection)

Shift + Z : show/hide Thumbnail mode for playlist column.

Escape : show/hide Everything

Right,Left: set focus alternate between Option column, Title column and Playlist column (If Player is not Playing Anything)

Ctrl+1 to Ctrl+8 : Change aspect ratio of background image

###Title Column:(if Title list is focussed)

h : show history (history of watched series)

Delete : delete particular item of history

r : randomize the list(if you want random series)

t : sort the Title List

PgUp: Move Entry UP

PgDown: Move Entry Down

ctrl+Right : Get Info from TVDB 

c : copy fanart

shift+c : copy summary

ctrl+c : copy poster

###Playlist Column:(If playlist column is focussed)

q : queue the item

Delete : delete particular entry

1 – 9 : select mirror Number (up to 9)

s : select SD quality

h : select HD quality

b : select SD480p quality

w : toggle watch/unwatch

o : start offline mode (If offline mode is already activated then pressing 'o' will enqueue items for offline viewing)

Right: play the item within thumbnail located in the leftmost corner but keep both playlist and title list visible. (can be used as preview mode)

Left: show title list if it's hidden

Return: play the item and hide title list but keep the playlist visible

BackSpace: Go To title list if title list is hidden

PgUp: Move Entry UP

PgDown: Move Entry Down

Ctrl+Up : Move to first entry

Ctrl+Down: Move to last entry

###Thumbnail Mode:

'=' (Remember '+' key) : increase size of Thumbnails

'-' : decrease size of Thumbnails

###Summary Text Browser

Ctrl+A : to select and save save edited summary.

###Thumbnail mode occupies pretty good memory. If you want to get out of thumbnail mode and free up the memory then click 'close' button which is available in the mode.

###Apart from shortcuts:
You can explore Right click menu of both Playlist Column and Title List Column for getting TVDB, Last.fm profiles for your collection either manually or automatically. If you are getting some problem while setting profiles from TVDB or Last.fm , or having problems accessing addons,then empty the cache directory '~/.config/AnimeWatch/tmp', This option is available with right click menu of Title List and Playlist column also.

###Other Things for convenience:

1. Please Enable Vertical Scrolling of Touchpad, because there are no scrollbars in this application, because they were looking very ugly in the total setup.

   In LXDE you can insert following command in autostart file to enable vertical scrolling

	synclient VertEdgeScroll=1

2. In LXDE, for setting global shortcuts for: Play,Pause,Next,Previous; assign keyboard shortcuts to following commands in Openbox lxde-rc.xml.

	1. bash -c 'player=$(qdbus-qt4 org.mpris.* | grep MediaPlayer2 | head -n 1); qdbus-qt4 $player /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause'
	
	2. bash -c 'player=$(qdbus-qt4 org.mpris.* | grep MediaPlayer2 | head -n 1); qdbus-qt4 $player /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next'

	3. bash -c 'player=$(qdbus-qt4 org.mpris.* | grep MediaPlayer2 | head -n 1); qdbus-qt4 $player /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous'


3. It is possible also to change default background image by simply replacing '~/.config/AnimeWatch/default.jpg' with another wallpaper of your choice and rename it to 'default.jpg'. This default image is important only when appropriate Fanart is not found. Once a fanart is found for particular entry, the default background image will change to it.

4. Instead of pycurl, it's possible to use directly either curl or wget for fetching web pages. Users need to edit 'GET_LIBRARY' field in the '~/.config/AnimeWatch/other_options.txt' and change it to either 'curl' or 'wget'. 

5. If users want to remove temporary directory automatically once the programme quits, then they should edit 'TMP_REMOVE' field in the '~/.config/AnimeWatch/other_options.txt' and change it to 'yes' from 'no'.

6. By default, the background image follows fit to screen mode without thinking about original aspect ratio of the image. If user want to change it to fit to width or fit to height, then they should try Ctrl+2 or Ctrl+3 global key combination. Users can also try Ctrl+4 to Ctrl+8 shortcuts, to experiment with various available background image modes.
