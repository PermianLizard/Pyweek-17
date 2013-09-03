import os
import pyglet

import start

FONT_PATH = None

MONO = None

def init():
	global FONT_PATH
	FONT_PATH = os.path.join(os.path.abspath(start.DATA_PATH), 'fonts')

	pyglet.font.add_file(os.path.join(os.path.abspath(FONT_PATH), 'Mono.ttf'))
	global MONO
	MONO = pyglet.font.load('mono 07_56')
	print MONO.name