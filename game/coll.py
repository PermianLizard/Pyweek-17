from plib import ecs
import phys
import ship
import planet

class CollisionEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'collision-component'

	def __init__(self, radius=0):
		super(CollisionEcsComponent, self).__init__()

		self.radius = radius
		
	def update(self, dt):
		pass


class CollisionEcsSystem(ecs.EcsSystem):

	@classmethod
	def name(cls):
		return 'collision-system'

	def __init__(self):
		super(CollisionEcsSystem, self).__init__()

	def update(self, dt):
		phys_comp_list = self.manager.comps[phys.PhysicsEcsComponent.name()]
		coll_comp_list = self.manager.comps[CollisionEcsComponent.name()]
		ship_comp_list = self.manager.comps[ship.ShipEcsComponent.name()]
		planet_comp_list = self.manager.comps[planet.PlanetEcsComponent.name()]

		entities_to_remove = set()

		entities = self.manager.entities
		for idx, eid in enumerate(entities):
			physc = phys_comp_list[idx]
			collc = coll_comp_list[idx]
			shipc = ship_comp_list[idx]
			planetc = planet_comp_list[idx]

			if physc == None or collc == None:
				continue

			for oidx, oeid in enumerate(entities):
				if eid == oeid: continue

				ophysc = phys_comp_list[oidx]
				ocollc = coll_comp_list[oidx]
				oshipc = ship_comp_list[oidx]
				oplanetc = planet_comp_list[oidx]

				if ophysc == None or ocollc == None:
					continue

				d = physc.pos.get_distance(ophysc.pos)
				coll_d = collc.radius + ocollc.radius

				if d <= coll_d:
					if not planetc:
						entities_to_remove.add(eid)
					if not oplanetc:
						entities_to_remove.add(oeid)

		for eid in entities_to_remove:
			self.manager.remove_entity(eid, CollisionEcsSystem.name(), 'collision')

	def on_pre_remove_entity(self, eid, system_name, event):
		pass
		#print 'entity %s being removed by system "%s" because of "%s"' % (eid, system_name, event)

	def __str__(self):
		return 'CollisionEcsSystem'