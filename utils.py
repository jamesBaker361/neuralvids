from pytube import YouTube
# misc
import os
from pathlib import Path
import shutil
import math
import datetime
import cv2
import tensorflow as tf

img_path='./images/'
vid_path='./videos/'

Path(vid_path).mkdir(parents=True, exist_ok=True)
Path(img_path).mkdir(parents=True, exist_ok=True)

def download(name, itag,tube,vid_path=vid_path): 
    '''saves pytube object as name_itag.mp4 in default video path'''
    try:
        os.rename(tube.streams.get_by_itag(itag).download(vid_path),'{}{}.mp4'.format(vid_path,name))
    except:
        pass
    return('{}.mp4'.format(name))

def download_from_url(name,url,res=144,vid_path=vid_path):
    '''
    from url, finds the right video given the resolution and downloads it
    '''
    tube=YouTube(url)
    itag=-1
    for s in tube.streams:
        if s.mime_type=='video/mp4' and s.resolution==str(res)+'p':
            itag=s.itag
            break
    if itag==-1:
        print('Invalid res {}'.format(res))
        return('')
    try:
        return(download(name+'_{}'.format(res),itag,tube=tube,vid_path=vid_path))
    except:
        return(name+'_{}'.format(res))
    
def video_to_frames(video_name,limit=1000,folder_name=None,path=None,img_path=img_path,vid_path=vid_path):
    '''extract first limit frames from a video @ in vid_path or at different_path and save to img_path/folder_name/ 
    directory as 'x.png' where x is the frame index. if name not given, saves name=video_name
    '''
    if folder_name==None:
        folder_name=video_name[:video_name.rfind('.mp4')]
    if path==None:
        path='{}{}'.format(vid_path,video_name)
    vidcap = cv2.VideoCapture(path)
    count = 0
    Path('{}{}'.format(img_path,folder_name)).mkdir(parents=True, exist_ok=True)
    while vidcap.isOpened()and count <limit:
        success, image = vidcap.read()
        if success:
            cv2.imwrite('{}{}/{}.png'.format(img_path,folder_name,count), image)
            count += 1
        else:
            print('error on frame {}'.format(count))
            break
    cv2.destroyAllWindows()
    vidcap.release()
    print('{} saved to {}{}'.format(path,img_path,folder_name))
    
def download_and_extract(name,url,res=144,img_path=img_path,vid_path=vid_path):
    '''combines download_from_url and video_to_frames
    '''
    video_name=download_from_url(name,url,res)
    print(video_name)
    video_to_frames(video_name,img_path=img_path,vid_path=vid_path)
    
def load_img(name,img_path=img_path,max_dim=1024):
    '''
    loads image @ img_path/name to a tensor
    '''
    img = tf.io.read_file('{}{}'.format(img_path,name))
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim
    new_shape = tf.cast(shape * scale, tf.int32)
    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img