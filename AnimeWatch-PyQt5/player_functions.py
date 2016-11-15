import os
import shutil
from tempfile import mkstemp

def write_files(file_name,content,line_by_line):
	fh, tmp_new_file = mkstemp()
	file_exists = False
	if os.path.exists(file_name):
		file_exists = True
		shutil.copy(file_name,tmp_new_file)
		print('copying ',file_name,' to ',tmp_new_file)
	try:
		if type(content) is list:
			bin_mode = False
			f = open(file_name,'w')
			j = 0
			for i in range(len(content)):
				fname = content[i].strip()
				if j == 0:
					try:
						f.write(fname)
					except UnicodeEncodeError as e:
						print(e,file_name+' will be written in binary mode')
						bin_mode = True
						f.close()
						break
				else:
					try:
						f.write('\n'+fname)
					except UnicodeEncodeError as e:
						print(e,file_name+' will be written in binary mode')
						bin_mode = True
						f.close()
						break
				j = j+1
			if not bin_mode:
				f.close()
			else:
				f = open(file_name,'wb')
				j = 0
				for i in range(len(content)):
					fname = content[i].strip()
					if j == 0:
						f.write(fname.encode('utf-8'))
					else:
						f.write(('\n'+fname).encode('utf-8'))
					j = j+1
				f.close()
		else:
			if line_by_line:
				content = content.strip()
				if not os.path.exists(file_name) or (os.stat(file_name).st_size == 0):
					f = open(file_name,'w')
					bin_mode = False
					try:
						f.write(content)
					except UnicodeEncodeError as e:
						print(e,file_name+' will be written in binary mode')
						f.close()
						bin_mode = True
						
					if bin_mode:
						f = open(file_name,'wb')
						f.write(content.encode('utf-8'))
						f.close()
				else:
					f = open(file_name,'a')
					bin_mode = False
					try:
						f.write('\n'+content)
					except UnicodeEncodeError as e:
						print(e,file_name+' will be written in binary mode')
						f.close()
						bin_mode = True
						
					if bin_mode:
						f = open(file_name,'ab')
						f.write(('\n'+content).encode('utf-8'))
						f.close()
					
					
			else:
				f = open(file_name, 'w')
				bin_mode = False
				try:
					f.write(content)
				except UnicodeEncodeError as e:
					print(e,file_name+' will be written in binary mode')
					f.close()
					bin_mode = True
				if bin_mode:
					f = open(file_name,'wb')
					f.write(content.encode('utf-8'))
					f.close()
	except Exception as e:
		print(e,'error in handling file, hence restoring original')
		if file_exists:
			shutil.copy(tmp_new_file,file_name)
			print('copying ',tmp_new_file,' to ',file_name)
		
