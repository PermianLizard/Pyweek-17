import math
import pyglet
from pyglet import gl

from plib import vec2d
from plib import ecs

import const
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

	def draw(self):
		ppc = self.manager.get_entity_comp(self.player_entity_id, phys.PhysicsEcsComponent.name())
		if ppc:
			self.tx = -ppc.pos.x + const.WIDTH / 2
			self.ty = -ppc.pos.y + const.HEIGHT / 2

		gl.glPushMatrix()
		gl.glLoadIdentity()
		gl.glTranslatef(self.tx, self.ty, 0.0)

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

		gl.glPopMatrix()