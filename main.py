style_path='/styles/'
vid_path='/videos/'
img_path='/images/'
output_path='/output/'

from styling import *
from utils import *
import os
import ffmpeg
def url_to_style_vid(name,url,style,res=144,img_path=img_path,vid_path=vid_path,style_path=style_path,output_path=output_path,start=0,length=10,clean=False):
    download_and_extract(name,url,res,img_path,vid_path)
    scene=name+'_{}'.format(res)
    trans_imgs(scene,style,img_path=img_path,style_path=style_path,output_path=output_path,start=start,length=length)
    v=os.getcwd()+vid_path+scene+style+'.avi'
    o=os.getcwd()+output_path+scene+'/%d.png'
    try:
        ffmpeg.input(o,start_number=start, start_number_range=length, pattern_type='sequence', framerate=25).output(v).run()
    except:
        print('already exists')

if __name__ == '__main__':
	for p in [style_path,vid_path, img_path,output_path]: #if folders do not exist, they are created
		path=os.getcwd()+p
		try:
			os.mkdir(path)
		except:
			pass