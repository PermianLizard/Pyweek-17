import pyglet
from pyglet import gl
from plib.director import director
import plib.scene

import instruct
import game
import font
import const
import starfield

menu_scene = None

def init():
	global menu_scene
	menu_scene = MenuScene()


class MenuScene(plib.scene.Scene):
	def __init__(self):
		super(MenuScene, self).__init__()

		self.menu_label = pyglet.text.Label('SYSTEM EVACUATION',
				font_name=font.FONT_MONO.name,
				font_size=32,
				x=20, y=const.HEIGHT - 10,
				anchor_x='left', anchor_y='top',
				color=(255, 255, 255, 255))

		self.options_label = pyglet.text.Label('<S> Start Game\n<I> Instructions\n<X> Exit',
				font_name=font.FONT_MONO.name,
				font_size=18,
				multiline=True,
				width=400,
				x=20, y=const.HEIGHT - 100,
				anchor_x='left', anchor_y='top',
				color=(255, 255, 255, 255))

		self.starfield = starfield.Starfield((0, 0, const.WIDTH, const.HEIGHT), 400)
		self.ty = 0


	def draw(self):
		self.ty -= 1
		self.starfield.draw(0, self.ty)

		self.menu_label.draw()
		self.options_label.draw()

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

		if symbol == pyglet.window.key.S:
			director.push(game.game_scene)
		if symbol == pyglet.window.key.I:
			director.push(instruct.instruct_scene)
		if symbol == pyglet.window.key.X:
			director.pop()

