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

	def __init__(self, impact_resistance=110.0, health=300):
		super(AsteroidEcsComponent, self).__init__()

		self.impact_resistance = float(impact_resistance)
		self.health_max = health
		self.health = health

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

	def __init__(self):
		super(AsteroidEcsSystem, self).__init__()

	def receive_damage(self, eid, amount):
		ac = self.manager.get_entity_comp(eid, AsteroidEcsComponent.name())
		print 'asteroid receive damage', amount
		ac.health -= amount
		if ac.health < 0:
			ac.health = 0
			self.manager.kill_entity(eid)

	def on_entity_collision(self, e1id, e2id, impact_size, e1reflect, system_name, event):
		e1ac = self.manager.get_entity_comp(e1id, AsteroidEcsComponent.name())
		if e1ac:
			if self.manager.get_entity_comp(e2id, planet.PlanetEcsComponent.name()):
				self.manager.kill_entity(e1id)
			elif impact_size > e1ac.impact_resistance:
				damage = int(impact_size - e1ac.impact_resistance)
				if damage > 0:
					self.receive_damage(e1id, damage)
			else:
				e1pc = self.manager.get_entity_comp(e1id, phys.PhysicsEcsComponent.name())
				e1pc.vel += e1reflect

	def on_entity_kill(self, eid, system_name, event):
		pass