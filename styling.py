import tensorflow as tf
import tensorflow_hub as hub
from utils import *
from PIL import Image
import numpy as np
import os

output_path='./output/'
style_path='./styles/'

hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1')
framerate=25

def tensor_to_image(tensor): #converts tensor to PIL Image, hub_module works on tensors
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return Image.fromarray(tensor)

def trans_imgs(scene,style_src,img_path=img_path,style_path=style_path,output_path=output_path,length=-1,hub_module=hub_module):
    '''
    given a scene, which represents a director @ img_path/scene, 
    and a style img @ style_path/style
    , transforms all the images in img_path/scene by applying style and saves them to output_path/scene 
    '''
    try:
        os.mkdir(output_path+scene)
    except:
        pass
    start=0
    if length<0:
        length=len(fnmatch.filter(os.listdir(img_path+scene), '*.png'))-start
    else:
        length=length*framerate
    style=load_img(style_src,img_path=style_path)
    for x in range(start,start+length):
        target=load_img(scene+'/{}.png'.format(x))
        i=hub_module(tf.constant(target), tf.constant(style))[0]
        tensor_to_image(i).save(output_path+scene+'/{}.png'.format(x))