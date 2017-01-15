import os
import shutil

BASEDIR,BASEFILE = os.path.split(os.path.abspath(__file__))
print(BASEDIR,BASEFILE,os.getcwd())

par_dir,cur_dir = os.path.split(BASEDIR)
src_dir = os.path.join(par_dir,'AnimeWatch-PyQt5')
dest_dir = os.path.join(BASEDIR,'AnimeWatch_PyQt5')
if os.path.exists(dest_dir):
	shutil.rmtree(dest_dir)
shutil.copytree(src_dir,dest_dir)
