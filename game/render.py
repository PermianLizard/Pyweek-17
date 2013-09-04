import math
import pyglet
import random
from pyglet import gl

from plib import vec2d
from plib import ecs

import font
import img
import const
import phys
import coll
import player
import planet
import ship

import starfield


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


class RenderShipEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'render-ship-component'

	def __init__(self):
		super(RenderShipEcsComponent, self).__init__()

	def __str__(self):
		return 'RenderShipEcsComponent'


class RenderPlanetEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'render-planet-component'

	def __init__(self):
		super(RenderPlanetEcsComponent, self).__init__()

	def __str__(self):
		return 'RenderPlanetEcsComponent'


class GameEcsRenderer(ecs.EcsRenderer):

	@classmethod
	def name(cls):
		return 'game-renderer'

	def __init__(self):
		super(GameEcsRenderer, self).__init__()
		self.player_entity_id = None

	def init(self):
		self.player_entity_id = None

		player_comp_list = self.manager.comps[player.PlayerIdentityEcsComponent.name()]
		for idx, eid in enumerate(self.manager.entities):
			if player_comp_list[idx]:
				self.player_entity_id = eid

		self.tx = 0.0
		self.ty = 0.0

		self.hud_sprite = pyglet.sprite.Sprite(img.get(img.IMG_HUD))
		self.hud_sprite.x = 0
		self.hud_sprite.y = 0

		self.starfield = starfield.Starfield((0, 0, const.WIDTH, const.HEIGHT), 200)

	def on_create_entity(self, eid, system_name, event):
		planet_comp_list = self.manager.comps[planet.PlanetEcsComponent.name()]
		rend_plan_comp_list = self.manager.comps[RenderPlanetEcsComponent.name()]

		entities = self.manager.entities
		for idx, eid in enumerate(entities):
			planetc = planet_comp_list[idx]

			if planetc:
				rpc = rend_plan_comp_list[idx]

	def draw(self):
		ppc = self.manager.get_entity_comp(self.player_entity_id, phys.PhysicsEcsComponent.name())
		if ppc:
			self.tx = ppc.pos.x - const.WIDTH / 2
			self.ty = ppc.pos.y - const.HEIGHT / 2

		tx = self.tx
		ty = self.ty
		area = (tx, ty, const.WIDTH, const.HEIGHT)

		gl.glPointSize( 1.5 );
		self.starfield.draw(tx, ty)

		gl.glPushMatrix()
		gl.glLoadIdentity()
		gl.glTranslatef(-tx, -ty, 0.0)

		phys_comp_list = self.manager.comps[phys.PhysicsEcsComponent.name()]
		grav_comp_list = self.manager.comps[phys.GravityEcsComponent.name()]
		coll_comp_list = self.manager.comps[coll.CollisionEcsComponent.name()]
		planet_comp_list = self.manager.comps[planet.PlanetEcsComponent.name()]
		ship_comp_list = self.manager.comps[ship.ShipEcsComponent.name()]
		rend_plan_comp_list = self.manager.comps[RenderPlanetEcsComponent.name()]
		rend_ship_comp_list = self.manager.comps[RenderShipEcsComponent.name()]

		entities = self.manager.entities
		for idx, eid in enumerate(entities):
			shipc = ship_comp_list[idx]
			planetc = planet_comp_list[idx]

			physc = phys_comp_list[idx]
			collc = coll_comp_list[idx]

			if shipc:
				rsc = rend_ship_comp_list[idx]	

				draw_circle(physc.pos.x, physc.pos.y, collc.radius, None, gl.GL_POLYGON, (1, 1, 0, 1))

				dir_radians = math.radians(shipc.rotation)
				dirv = vec2d.vec2d(math.cos(dir_radians), math.sin(dir_radians))
				dirv.length = collc.radius

				gl.glColor3f(1, 0, 0, 1)
				gl.glBegin(gl.GL_LINES)
				gl.glVertex2f(physc.pos.x, physc.pos.y)
				gl.glVertex2f(physc.pos.x + dirv.x, physc.pos.y + dirv.y)
				gl.glEnd()

			elif planetc:
				rpc = rend_plan_comp_list[idx]

				draw_circle(physc.pos.x, physc.pos.y, collc.radius)

				if planetc.pname:
					label = pyglet.text.Label(planetc.pname,
	                          font_name=font.FONT_MONO.name,
	                          font_size=12,
	                          x=physc.pos.x, y=physc.pos.y, #  + collc.radius + 5
	                          anchor_x='center', anchor_y='center',
	                          color=(0, 255, 0, 255))
					label.draw()

				gc = grav_comp_list[idx]
				if gc and gc.gravity_radius:
					draw_circle(physc.pos.x, physc.pos.y, gc.gravity_radius, None, gl.GL_LINE_LOOP)

		gl.glPopMatrix()

		# draw the HUD
		#self.hud_sprite.draw()