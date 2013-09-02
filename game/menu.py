import pyglet
from pyglet import gl
from plib.director import director
import plib.scene

import game

menu_scene = None

def init():
	global menu_scene
	menu_scene = MenuScene()

options = ['New Game', 'Exit']

label = pyglet.text.Label('Menu',
	font_name='Times New Roman',
	font_size=36,
	x=500//2, y=300//2,
	anchor_x='center', anchor_y='center')

class MenuScene(plib.scene.Scene):
	def __init__(self):
		super(MenuScene, self).__init__()

	def draw(self):
		label.draw()

		gl.glBegin(pyglet.gl.GL_TRIANGLES)
		gl.glVertex2f(0, 0)
		gl.glVertex2f(100, 0)
		gl.glVertex2f(100, 200)
		gl.glEnd()

		#gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
		#gl.glLoadIdentity()
		#vp = director.viewport
		#gl.glBegin(pyglet.gl.GL_QUADS)
		#gl.glVertex2f(0 , 0)
		#gl.glVertex2f(vp[2], 0)
		#gl.glVertex2f(vp[2], vp[3])
		#gl.glVertex2f(0, vp[3])
		#gl.glEnd()

	def on_key_press(self, symbol, modifiers):
		super(MenuScene, self).on_key_press(symbol, modifiers)

		if symbol == pyglet.window.key.ENTER:
			director.push(game.game_scene)
		if symbol == pyglet.window.key.Q:
			director.pop()

