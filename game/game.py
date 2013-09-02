import math
import logging
import pyglet
from pyglet import gl

from plib.director import director
from plib import scene
from plib import ecs
from plib import vec2d

import const
import phys
import coll
import player
import ship
import render


class GameEcsManager(ecs.EcsManager):
	def __init__(self):
		super(GameEcsManager, self).__init__()

		# systems
		self.add_system(phys.PhysicsEcsSystem())
		self.add_system(coll.CollisionEcsSystem())
		self.add_system(ship.ShipEcsSystem())
		self.add_system(player.PlayerEscSystem())

		# renderers
		self.add_renderer(render.GameEcsRenderer())

		# input handlers
		self.add_input_handler(player.PlayerEscInputHandler())

		# register components
		self.reg_comp_type(phys.PhysicsEcsComponent.name())
		self.reg_comp_type(phys.GravityEcsComponent.name())
		self.reg_comp_type(coll.CollisionEcsComponent.name())
		self.reg_comp_type(player.PlayerIdentityEcsComponent.name())
		self.reg_comp_type(ship.ShipEcsComponent.name())

	def init(self):
		e1 = ecsm.create_entity([phys.PhysicsEcsComponent(100, 100, 10000, False), 
				phys.GravityEcsComponent(100),
				coll.CollisionEcsComponent(12)])
		e2 = ecsm.create_entity([phys.PhysicsEcsComponent(300, 300, 10, False),
				coll.CollisionEcsComponent(12), 
				player.PlayerIdentityEcsComponent(), 
				ship.ShipEcsComponent(90.0, 6, 10.0)])
		e3 = ecsm.create_entity([phys.PhysicsEcsComponent(200, 200, 50000, True), 
				phys.GravityEcsComponent(140),
				coll.CollisionEcsComponent(24)])

		self.get_system(phys.PhysicsEcsSystem.name()).set_orbit(e1, e3, 100, 180, True)
		self.get_system(phys.PhysicsEcsSystem.name()).set_orbit(e2, e3, 100, 0, True)

		super(GameEcsManager, self).init()

game_scene = None
ecsm = None 

def init():
	global game_scene
	game_scene = GameScene()


def new_game():
	logging.debug('new game started')
	global ecsm
	ecsm = GameEcsManager()
	ecsm.init()
	ecsm.keys = director.keys


def clean_game():
	global ecsm
	ecsm.cleanup()
	ecsm.keys = None
	ecsm = None


class GameScene(scene.Scene):
	pass

	def enter(self):
		new_game()

	def exit(self):
		clean_game()

	def draw(self):
		ecsm.draw()

	def update(self, dt):
		ecsm.update(dt)

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.ESCAPE:
			director.pop()
		else:
			ecsm.on_key_press(symbol, modifiers)

	def on_key_release(self, symbol, modifiers):
		ecsm.on_key_release(symbol, modifiers)

	def on_mouse_motion(self, x, y, dx, dy):
		ecsm.on_mouse_motion(x, y, dx, dy)
	
	def on_mouse_press(self, x, y, button, modifiers):
		ecsm.on_mouse_press(x, y, button, modifiers)
	
	def on_mouse_release(self, x, y, button, modifiers):
		ecsm.on_mouse_release(x, y, button, modifiers)
	
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		ecsm.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

	def on_mouse_enter(self, x, y):
		ecsm.on_mouse_enter(x, y)
	
	def on_mouse_leave(self, x, y):
		ecsm.on_mouse_leave(x, y)
	
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		ecsm.on_mouse_scroll(x, y, scroll_x, scroll_y)