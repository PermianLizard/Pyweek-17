import os
import pyglet

import start

IMG_HUD = 'hud.png'
IMG_SHIP = 'ship.png'

img_name_list = [IMG_HUD, IMG_SHIP]
img_center_list = [True, True]
img_dict = {}

def init():
	PATH = os.path.join(start.DATA_PATH, 'images')

	for idx, img_name in enumerate(img_name_list):
		img = pyglet.image.load(os.path.join(PATH, img_name))
		if img_center_list[idx]:
			img.anchor_x = img.width // 2
			img.anchor_y = img.height // 2
		img_dict[img_name] = img

def get(name):
	return img_dict[name]