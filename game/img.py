import os
import pyglet

from pyglet.image.codecs.png import PNGImageDecoder

import start

IMG_HUD = 'hud.png'

img_name_list = [IMG_HUD,]
img_dict = {}

def init():
	PATH = os.path.join(start.DATA_PATH, 'images')

	for img_name in img_name_list:
		img_dict[img_name] = pyglet.image.load(os.path.join(PATH, img_name), decoder=PNGImageDecoder())

def get(name):
	return img_dict[name]