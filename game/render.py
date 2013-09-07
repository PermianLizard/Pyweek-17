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
import base
import asteroid

import starfield


def rect_rect_intersect(x1, y1, w1, h1, x2, y2, w2, h2):
	if x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1:
		return False
	return True

def clamp(value, min, max):
	if value < min:
		return min
	if value > max:
		return max
	return value

def circle_rect_intersect(cx, cy, cr, rx, ry, rw, rh):
	closestX = clamp(cx, rx, rx + rw)
	closestY = clamp(cy, ry, ry + rh)

	distanceX = cx - closestX
	distanceY = cy - closestY

	distanceSquared = (distanceX ** 2) + (distanceY ** 2);
	return distanceSquared < cr ** 2

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


class RenderEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'render-component'

	def process(self):
		pass

	def __init__(self):
		super(RenderEcsComponent, self).__init__()

		#self.spr = pyglet.sprite.Sprite(img.get(img.IMG_SHIP))

	def __str__(self):
		return 'RenderEcsComponent'


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

		#self.hud_sprite = pyglet.sprite.Sprite(img.get(img.IMG_HUD))
		#self.hud_sprite.x = 0
		#self.hud_sprite.y = 0


		self.fuel_label = pyglet.text.Label('',
				font_name=font.FONT_MONO.name,
				font_size=12,
				x=20, y=const.HEIGHT - 10,
				anchor_x='left', anchor_y='top',
				color=(0, 255, 0, 255))

		self.health_label = pyglet.text.Label('',
				font_name=font.FONT_MONO.name,
				font_size=12,
				x=20, y=const.HEIGHT - 35,
				anchor_x='left', anchor_y='top',
				color=(0, 255, 0, 255))

		self.rescued_label = pyglet.text.Label('',
				font_name=font.FONT_MONO.name,
				font_size=12,
				x=20, y=const.HEIGHT - 60,
				anchor_x='left', anchor_y='top',
				color=(0, 255, 0, 255))

		self.starfield = starfield.Starfield((0, 0, const.WIDTH, const.HEIGHT), 400)

	def on_create_entity(self, eid, system_name, event):
		planet_comp_list = self.manager.comps[planet.PlanetEcsComponent.name()]
		rend_plan_comp_list = self.manager.comps[planet.RenderPlanetEcsComponent.name()]

		entities = self.manager.entities
		for idx, eid in enumerate(entities):
			pass
			#planetc = planet_comp_list[idx]
			#if planetc:
			#	rpc = rend_plan_comp_list[idx]

	def draw(self):
		phys_comp_list = self.manager.comps[phys.PhysicsEcsComponent.name()]
		grav_comp_list = self.manager.comps[phys.GravityEcsComponent.name()]
		coll_comp_list = self.manager.comps[coll.CollisionEcsComponent.name()]
		planet_comp_list = self.manager.comps[planet.PlanetEcsComponent.name()]
		ship_comp_list = self.manager.comps[ship.ShipEcsComponent.name()]
		base_comp_list = self.manager.comps[base.BaseEcsComponent.name()]
		aster_comp_list = self.manager.comps[asteroid.AsteroidEcsComponent.name()]
		rend_plan_comp_list = self.manager.comps[planet.RenderPlanetEcsComponent.name()]
		rend_ship_comp_list = self.manager.comps[ship.RenderShipEcsComponent.name()]
		rend_base_comp_list = self.manager.comps[base.RenderBaseEcsComponent.name()]
		rend_aster_comp_list = self.manager.comps[asteroid.RenderAsteroidEcsComponent.name()]

		entities = self.manager.entities

		player_alive = False
		if self.player_entity_id in entities:
			player_alive = True

			ppc = self.manager.get_entity_comp(self.player_entity_id, phys.PhysicsEcsComponent.name())
			psc = self.manager.get_entity_comp(self.player_entity_id, ship.ShipEcsComponent.name())

			if ppc:
				self.tx = ppc.pos.x - const.WIDTH / 2
				self.ty = ppc.pos.y - const.HEIGHT / 2

		tx = self.tx
		ty = self.ty
		area = (tx, ty, const.WIDTH, const.HEIGHT)

		#img.get(img.IMG_BG).blit(0, 0)

		gl.glPointSize( 1 );
		self.starfield.draw(tx, ty)

		gl.glPushMatrix()
		gl.glLoadIdentity()
		gl.glTranslatef(-tx, -ty, 0.0)		

		for idx, eid in enumerate(entities):
			shipc = ship_comp_list[idx]
			basec = base_comp_list[idx]
			asterc = aster_comp_list[idx]
			planetc = planet_comp_list[idx]
			physc = phys_comp_list[idx]
			collc = coll_comp_list[idx]

			#if eid == self.player_entity_id:
			#	print physc.pos.x, physc.pos.y, collc.radius, tx, tx
			#	print circle_rect_intersect(physc.pos.x, physc.pos.y, collc.radius, tx, tx, const.WIDTH, const.HEIGHT)

			#clipping
			if not circle_rect_intersect(physc.pos.x, physc.pos.y, collc.radius, tx, ty, const.WIDTH, const.HEIGHT):
				continue

			if shipc:
				rsc = rend_ship_comp_list[idx]
				rsc.process()

				#draw_circle(physc.pos.x, physc.pos.y, collc.radius, None, gl.GL_POLYGON, (1, 1, 0, 1))

				ship_sprite = rsc.spr
				ship_sprite.x = physc.pos.x
				ship_sprite.y = physc.pos.y
				ship_sprite.rotation = -shipc.rotation
				ship_sprite.draw()				

				#dir_radians = math.radians(shipc.rotation)
				#dirv = vec2d.vec2d(math.cos(dir_radians), math.sin(dir_radians))
				#dirv.length = collc.radius
				#gl.glColor3f(1, 0, 0, 1)
				#gl.glBegin(gl.GL_LINES)
				#gl.glVertex2f(physc.pos.x, physc.pos.y)
				#gl.glVertex2f(physc.pos.x + dirv.x, physc.pos.y + dirv.y)
				#gl.glEnd()

			elif basec:
				rbc = rend_base_comp_list[idx]	

				draw_circle(physc.pos.x, physc.pos.y, collc.radius, None, gl.GL_POLYGON, (1, 0, 0, 1))

				draw_circle(physc.pos.x, physc.pos.y, basec.radius, None, gl.GL_LINES, (1, 0, 0, 1))

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

			elif asterc:
				rac = rend_aster_comp_list[idx]
				draw_circle(physc.pos.x, physc.pos.y, collc.radius, None, gl.GL_POLYGON, (0, 1, 0, 1))

		gl.glPopMatrix()

		# interface
		if player_alive:
			nav_circle_radius = (const.HEIGHT - 100) // 2
			draw_circle(const.WIDTH // 2, const.HEIGHT // 2, nav_circle_radius, 12, gl.GL_LINE_LOOP, (1, 1, 0, 1))

			self.fuel_label.text = 'Fuel:' + str(psc.fuel) + ' / ' + str(psc.fuel_max)
			self.health_label.text = 'Ship:' + str(psc.health) + ' / ' + str(psc.health_max)
			self.rescued_label.text = 'Rescued:' + str(psc.passengers)

			self.fuel_label.draw()
			self.health_label.draw()
			self.rescued_label.draw()


		# draw the HUD
		#self.hud_sprite.draw()