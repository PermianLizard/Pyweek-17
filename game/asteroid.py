import math
from plib import vec2d
from plib import ecs
import phys

class AsteroidEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'asteroid-component'

	def __init__(self):
		super(AsteroidEcsComponent, self).__init__()

	def __str__(self):
		return 'AsteroidEcsComponent'

class AsteroidEcsSystem(ecs.EcsSystem):
	@classmethod
	def name(cls):
		return 'asteroid-system'

	#def create_random(self, x, y, direction_angle, speed):
	#	return ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, 10, False),
	#		coll.CollisionEcsComponent(14), 
	#		asteroid.AsteroidEcsComponent(),
	#		render.RenderShipEcsComponent()])

	def __init__(self):
		super(AsteroidEcsSystem, self).__init__()

	def on_entity_collision(self, e1id, e2id, system_name, event):
		e1ac = self.manager.get_entity_comp(e1id, AsteroidEcsComponent.name())
		e2ac = self.manager.get_entity_comp(e2id, AsteroidEcsComponent.name())

		if e1ac:
			self.manager.mark_entity_for_deletion(e1id)

		if e2ac:
			self.manager.mark_entity_for_deletion(e2id)