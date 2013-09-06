import math
import pyglet
from plib import vec2d
from plib import ecs

import phys
import img
import planet


class ShipEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'ship-component'

	def __init__(self, rotation=0.0, rotation_speed=0, thrust_force=0.0):
		super(ShipEcsComponent, self).__init__()

		self.rotation = float(rotation)
		self.thrust_force = float(thrust_force)
		self.rotation_speed = float(rotation_speed)

	def __str__(self):
		return 'ShipEcsComponent'


class RenderShipEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'render-ship-component'

	def __init__(self):
		super(RenderShipEcsComponent, self).__init__()

		self.spr = pyglet.sprite.Sprite(img.get(img.IMG_SHIP))

	def __str__(self):
		return 'RenderShipEcsComponent'


class ShipEcsSystem(ecs.EcsSystem):
	@classmethod
	def name(cls):
		return 'ship-system'

	def __init__(self):
		super(ShipEcsSystem, self).__init__()

	def turn_left(self, eid):
		sc = self.manager.get_entity_comp(eid, ShipEcsComponent.name())
		sc.rotation += sc.rotation_speed

	def turn_right(self, eid):
		sc = self.manager.get_entity_comp(eid, ShipEcsComponent.name())
		sc.rotation -= sc.rotation_speed

	def thrust_forward(self, eid):
		sc = self.manager.get_entity_comp(eid, ShipEcsComponent.name())
		pc = self.manager.get_entity_comp(eid, phys.PhysicsEcsComponent.name())

		if not sc or not pc: return
		
		dir_radians = math.radians(sc.rotation)
		dirv = vec2d.vec2d(math.cos(dir_radians), math.sin(dir_radians))
		dirv.length = sc.thrust_force

		pc.apply_force(dirv.x, dirv.y)

	def on_entity_collision(self, e1id, e2id, e1reflect, system_name, event):
		e1sc = self.manager.get_entity_comp(e1id, ShipEcsComponent.name())
		e2sc = self.manager.get_entity_comp(e2id, ShipEcsComponent.name())

		if e1sc:
			if self.manager.get_entity_comp(e2id, planet.PlanetEcsComponent.name()):
				self.manager.kill_entity(e1id)

			e1pc = self.manager.get_entity_comp(e1id, phys.PhysicsEcsComponent.name())
			e1pc.vel += e1reflect

		#	if (e1pc.vel - e2pc.vel).length > 40:
		#		self.manager.kill_entity(e1id)

	def on_entity_kill(self, eid, system_name, event):
		pass