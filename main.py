style_path='/styles/'
vid_path='/videos/'
img_path='/images/'
output_path='/output/'

import os
import sys
import getopt
import ffmpeg
import requests


def url_to_style_vid(name,url,style,res=144,img_path=img_path,vid_path=vid_path,style_path=style_path,output_path=output_path,length=10,clean=True):
    download_and_extract(name,url,res,img_path,vid_path)
    scene=name+'_{}'.format(res)
    trans_imgs(scene,style,img_path=img_path,style_path=style_path,output_path=output_path,length=length)
    v=os.getcwd()+vid_path+scene+style+'.avi'
    o=os.getcwd()+output_path+scene+'/%d.png'
    try:
        ffmpeg.input(o,start_number=0, start_number_range=length, pattern_type='sequence', framerate=framerate).output(v).run()
    except:
        print('already exists')

if __name__ == '__main__':
	for p in [style_path,vid_path, img_path,output_path]: #if folders do not exist, they are created
		path=os.getcwd()+p
		try:
			os.mkdir(path)
		except:
			pass
	try:
		opts, args = getopt.getopt(sys.argv[1:],"ihdn:u:s:r:l:c",["name=","url=","style=","resolution=","length=","clean="])
	except getopt.GetoptError:
		print('main.py -n <name> -u <url_video>')
		print('main.py -h for help')
		sys.exit()
	name='name'
	url='-1'
	style='astro.png'
	res=144
	length=10
	clean=True
	for opt, arg in opts:
		if opt =='-d':
			print('style = {} resolution = {}p length = {} seconds clean = {}'.format(style,res,length,clean))
		if opt =='-i':
			print('style imgs:')
			for f in os.listdir(os.getcwd()+style_path):
				print(f)
		if opt == '-h':
			print('main.py --name=<name> --url=<url_video> --style=<img.png> --resolution=<144,720,etc>  --length=<length in seconds> --clean=<t/f/T/F/True/False/true/false>')
			print('main.py -d for default values')
			print('main.py -i to list style imgs')
			sys.exit()
		if opt in ('-n','--name'):
			name=arg
		if opt in ('-u','--url'):
			try:
				requests.get(arg)
			except:
				try:
					requests.get('http://{}'.format(arg))
				except:
					print('invalid url')
					sys.exit()
			url = arg
		if opt in ("-s","--style"):
			if arg not in set(os.listdir(os.getcwd()+style_path)):
				print('invalid style image, main.py -i to list style imgs')
				sys.exit()
			else:
				style=arg
		if opt in ('-r','--resolution'):
			if int(arg) not in (144,240,360,480,720,1080):
				print('invalid resolution, try one of 144,240,360,480,720,1080')
				sys.exit()
			else:
				res=int(arg)
		if opt in ('-l','--length'):
			try:
				length=int(arg)
			except:
				print('invalid length, must be integer')
				sys.exit()
		if opt in ('-c','--clean'):
			if arg in ('t','T','True','true'):
				clean=True
			elif arg in ('f','F','False','false'):
				clean=False
			else:
				print('invalid clean, must be t/f/T/F/True/False/true/false')
				sys.exit()


	from styling import *
	from utils import *
	url_to_style_vid(name,url,style,res=res,img_path=img_path,vid_path=vid_path,style_path=style_path,output_path=output_path,length=length,clean=clean)