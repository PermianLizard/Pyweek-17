import os
import pyglet

import start

print pyglet.resource.path

FONT_PATH = None

FONT_MONO = None

def init():
	global FONT_PATH
	FONT_PATH = os.path.join(os.path.abspath(start.DATA_PATH), 'fonts')

	pyglet.font.add_file(os.path.join(os.path.abspath(FONT_PATH), 'Mono.ttf'))
	global FONT_MONO
	FONT_MONO = pyglet.font.load('mono 07_56')
	print FONT_MONO.name