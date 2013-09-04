import math
import logging
import pyglet
from pyglet import gl

from plib.director import director
from plib import scene
from plib import ecs
from plib import vec2d

import const
import map
import phys
import coll
import player
import planet
import ship
import render
import level


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
		self.reg_comp_type(planet.PlanetEcsComponent.name())
		self.reg_comp_type(ship.ShipEcsComponent.name())
		self.reg_comp_type(render.RenderPlanetEcsComponent.name())
		self.reg_comp_type(render.RenderShipEcsComponent.name())

	def init(self):

		level.generate(ecsm)

		player_ship = ecsm.create_entity([phys.PhysicsEcsComponent(300, 300, 10, False),
				coll.CollisionEcsComponent(12), 
				player.PlayerIdentityEcsComponent(), 
				ship.ShipEcsComponent(90.0, 6, 10.0),
				render.RenderShipEcsComponent()])
		#self.get_system(phys.PhysicsEcsSystem.name()).set_orbit(player_ship, planet1, 120, 0, True)

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
	ecsm.keys = director.keys
	ecsm.setup_handlers()
	ecsm.init()


def clean_game():
	global ecsm
	ecsm.cleanup()
	ecsm.keys = None
	ecsm = None


class GameScene(scene.Scene):

	def __init__(self):
		super(GameScene, self).__init__()

	def enter(self):
		new_game()
		self.paused = False

	def exit(self):
		clean_game()

	def draw(self):
		ecsm.draw()

	def update(self, dt):
		if not self.paused:
			ecsm.update(dt)

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.ESCAPE:
			director.pop()
		elif symbol == pyglet.window.key.P:
			self.paused = not self.paused
		elif symbol == pyglet.window.key.TAB:
			director.push(map.map_scene)
		elif not self.paused:
			ecsm.on_key_press(symbol, modifiers)

	def on_key_release(self, symbol, modifiers):
		if not self.paused:
			ecsm.on_key_release(symbol, modifiers)

	def on_mouse_motion(self, x, y, dx, dy):
		if not self.paused:
			ecsm.on_mouse_motion(x, y, dx, dy)
	
	def on_mouse_press(self, x, y, button, modifiers):
		if not self.paused:
			ecsm.on_mouse_press(x, y, button, modifiers)
	
	def on_mouse_release(self, x, y, button, modifiers):
		if not self.paused:
			ecsm.on_mouse_release(x, y, button, modifiers)
	
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if not self.paused:
			ecsm.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

	def on_mouse_enter(self, x, y):
		if not self.paused:
			ecsm.on_mouse_enter(x, y)
	
	def on_mouse_leave(self, x, y):
		if not self.paused:
			ecsm.on_mouse_leave(x, y)
	
	def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
		if not self.paused:
			ecsm.on_mouse_scroll(x, y, scroll_x, scroll_y)