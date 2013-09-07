import math
import pyglet
from plib import vec2d
from plib import ecs

import phys
import render
import coll
import planet

class AsteroidEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'asteroid-component'

	def __init__(self, impact_resistance=110.0):
		super(AsteroidEcsComponent, self).__init__()

		self.impact_resistance = float(impact_resistance)

	def __str__(self):
		return 'AsteroidEcsComponent'


class RenderAsteroidEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'render-asteroid-component'

	def __init__(self):
		super(RenderAsteroidEcsComponent, self).__init__()

	def __str__(self):
		return 'RenderAsteroidEcsComponent'


class AsteroidEcsSystem(ecs.EcsSystem):
	@classmethod
	def name(cls):
		return 'asteroid-system'

	def create_random(self, x, y, direction_angle, speed):
		return ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, 10, False),
			coll.CollisionEcsComponent(14), 
			asteroid.AsteroidEcsComponent(),
			render.RenderAsteroidEcsComponent()])

	def __init__(self):
		super(AsteroidEcsSystem, self).__init__()

	def on_entity_collision(self, e1id, e2id, impact_size, e1reflect, system_name, event):
		e1ac = self.manager.get_entity_comp(e1id, AsteroidEcsComponent.name())
		if e1ac:
			if self.manager.get_entity_comp(e2id, planet.PlanetEcsComponent.name()):
				self.manager.kill_entity(e1id)
			elif impact_size > e1ac.impact_resistance:
				self.manager.kill_entity(e1id)
			else:
				e1pc = self.manager.get_entity_comp(e1id, phys.PhysicsEcsComponent.name())
				e1pc.vel += e1reflect

	def on_entity_kill(self, eid, system_name, event):
		pass

def get_circle_closest_point(pos, cpos, cradius):
	dv = math.sqrt(math.pow(cpos.x - pos.x, 2) + math.pow(cpos.y - pos.y, 2))
	cx = cpos.x + (cradius * (pos.x - cpos.x) / dv)
	cy = cpos.y + (cradius * (pos.y - cpos.y) / dv)

	return vec2d.vec2d(cx, cy)