from plib import ecs
import phys

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

		entities_to_remove = set()

		entities = self.manager.entities
		for idx, eid in enumerate(entities):
			pc = phys_comp_list[idx]
			cc = coll_comp_list[idx]

			if pc == None or cc == None:
				continue

			for oidx, oeid in enumerate(entities):
				if eid == oeid: continue

				opc = phys_comp_list[oidx]
				occ = coll_comp_list[oidx]

				if opc == None or occ == None:
					continue

				d = pc.pos.get_distance(opc.pos)
				coll_d = cc.radius + occ.radius

				if d <= coll_d:
					entities_to_remove.add(eid)
					entities_to_remove.add(oeid)

		for eid in entities_to_remove:
			self.manager.remove_entity(eid, CollisionEcsSystem.name(), 'collision')

	def on_pre_remove_entity(self, eid, system_name, event):
		pass
		#print 'entity %s being removed by system "%s" because of "%s"' % (eid, system_name, event)

	def __str__(self):
		return 'CollisionEcsSystem'