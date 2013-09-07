import math
import pyglet
from plib import vec2d
from plib import ecs

import phys
import img
import planet
import coll
import ship


class BaseEcsComponent(ecs.EcsComponent):

	LOAD_COOLDOWN_MAX = 10

	@classmethod
	def name(cls):
		return 'base-component'

	def __init__(self, radius, fuel_load=200, impact_resistance=110.0, health=300):
		super(BaseEcsComponent, self).__init__()

		self.radius = float(radius)
		self.fuel_load = fuel_load

		self.impact_resistance = float(impact_resistance)
		self.health_max = health
		self.health = health

		self.load_cooldown = 0

	def __str__(self):
		return 'BaseEcsComponent'


class RenderBaseEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'render-base-component'

	def __init__(self):
		super(RenderBaseEcsComponent, self).__init__()

		#self.spr = pyglet.sprite.Sprite(img.get(img.IMG_SHIP))

	def __str__(self):
		return 'RenderBaseEcsComponent'


class BaseEcsSystem(ecs.EcsSystem):
	@classmethod
	def name(cls):
		return 'base-system'

	def __init__(self):
		super(BaseEcsSystem, self).__init__()

	def receive_damage(self, eid, amount):
		bc = self.manager.get_entity_comp(eid, BaseEcsComponent.name())
		print 'base receive damage', amount
		bc.health -= amount
		if bc.health < 0:
			bc.health = 0
			self.manager.kill_entity(eid)

	def update(self, dt):
		# check for a ship in our radius
		phys_comp_list = self.manager.comps[phys.PhysicsEcsComponent.name()]
		coll_comp_list = self.manager.comps[coll.CollisionEcsComponent.name()]
		ship_comp_list = self.manager.comps[ship.ShipEcsComponent.name()]
		base_comp_list = self.manager.comps[BaseEcsComponent.name()]

		entities = self.manager.entities

		for idx, eid in enumerate(entities):
			basec = base_comp_list[idx]

			if basec:
				physc = phys_comp_list[idx]

				for oidx, oeid in enumerate(entities):
					if idx == oidx: continue
					shipc = ship_comp_list[oidx]

					if shipc:
						ophysc = phys_comp_list[oidx]
						if (physc.pos - ophysc.pos).length < basec.radius:

							if basec.load_cooldown > 0:
								basec.load_cooldown -= 1
							else:
								basec.load_cooldown = BaseEcsComponent.LOAD_COOLDOWN_MAX

								if basec.fuel_load:
									basec.fuel_load -= 1
									self.manager.get_system(ship.ShipEcsSystem.name()).award_fuel(oeid, 1)

	def on_entity_collision(self, e1id, e2id, impact_size, e1reflect, system_name, event):
		e1bc = self.manager.get_entity_comp(e1id, BaseEcsComponent.name())
		if e1bc:
			if self.manager.get_entity_comp(e2id, planet.PlanetEcsComponent.name()):
				self.manager.kill_entity(e1id)
			elif impact_size > e1bc.impact_resistance:
				damage = int(impact_size - e1bc.impact_resistance)
				if damage > 0:
					self.receive_damage(e1id, damage)
			else:
				e1pc = self.manager.get_entity_comp(e1id, phys.PhysicsEcsComponent.name())
				e1pc.vel += e1reflect