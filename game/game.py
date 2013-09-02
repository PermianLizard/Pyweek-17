import math
import logging
import pyglet
from pyglet import gl

from plib.director import director
from plib import scene
from plib import ecs
from plib import vec2d

import phys
import coll
import player
import ship


### TEMP ###
def get_num_circle_segments(r):
	return int(10 * math.sqrt(r))

def draw_circle(cx, cy, r, num_segments=None, mode=gl.GL_POLYGON, color=(1, 1, 1, 1)):
	if not num_segments:
		num_segments = get_num_circle_segments(r)

	theta = 2 * math.pi / float(num_segments)
	tangetial_factor = math.tan(theta)
	radial_factor = math.cos(theta)

	x = float(r)
	y = 0.0

	gl.glColor3f(color[0], color[1], color[2], color[3])
	gl.glBegin(mode)
	for i in xrange(num_segments):
		gl.glVertex2f(x + cx, y + cy)

		tx = y * -1
		ty = x

		x += tx * tangetial_factor
		y += ty * tangetial_factor

		x *= radial_factor
		y *= radial_factor
	gl.glEnd()


class GameEcsManager(ecs.EcsManager):
	def __init__(self):
		super(GameEcsManager, self).__init__()

		# systems
		self.add_system(phys.PhysicsEcsSystem())
		self.add_system(coll.CollisionEcsSystem())
		self.add_system(ship.ShipEcsSystem())
		self.add_system(player.PlayerEscSystem())

		# renderers
		self.add_renderer(GameEcsRenderer())

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


class GameEcsRenderer(ecs.EcsRenderer):

	@classmethod
	def name(cls):
		return 'game-renderer'

	def __init__(self):
		super(GameEcsRenderer, self).__init__()

	def draw(self):
		phys_comp_list = self.manager.comps[phys.PhysicsEcsComponent.name()]
		grav_comp_list = self.manager.comps[phys.GravityEcsComponent.name()]
		coll_comp_list = self.manager.comps[coll.CollisionEcsComponent.name()]
		ship_comp_list = self.manager.comps[ship.ShipEcsComponent.name()]

		entities = self.manager.entities
		for idx, eid in enumerate(entities):
			pc = phys_comp_list[idx]
			gc = grav_comp_list[idx]
			cc = coll_comp_list[idx]
			sc = ship_comp_list[idx]

			if pc and cc:
				draw_circle(pc.pos.x, pc.pos.y, cc.radius)

				if gc and gc.gravity_radius:
					draw_circle(pc.pos.x, pc.pos.y, gc.gravity_radius, None, gl.GL_LINE_LOOP)

				if sc:
					dir_radians = math.radians(sc.rotation)
					dirv = vec2d.vec2d(math.cos(dir_radians), math.sin(dir_radians))
					dirv.length = cc.radius

					draw_circle(pc.pos.x, pc.pos.y, 5, None, gl.GL_POLYGON, (1, 0, 0, 1))
					gl.glColor3f(1, 0, 0, 1)
					gl.glBegin(gl.GL_LINES)
					gl.glVertex2f(pc.pos.x, pc.pos.y)
					gl.glVertex2f(pc.pos.x + dirv.x, pc.pos.y + dirv.y)
					gl.glEnd()

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