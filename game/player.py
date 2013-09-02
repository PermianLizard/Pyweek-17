import pyglet
from plib import ecs
import ship


class PlayerIdentityEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'player-identity-component'

	def __init__(self):
		super(PlayerIdentityEcsComponent, self).__init__()


class PlayerEscInputHandler(ecs.EcsInputHandler):

	@classmethod
	def name(cls):
		return 'player-input-handler'

	def __init__(self):
		super(PlayerEscInputHandler, self).__init__()
		self.player_entity_id = None

	def init(self):
		self.player_entity_id = None

		player_comp_list = self.manager.comps[PlayerIdentityEcsComponent.name()]
		for idx, eid in enumerate(self.manager.entities):
			if player_comp_list[idx]:
				self.player_entity_id = eid

	def on_key_press(self, symbol, modifiers):
		if self.player_entity_id:
			# TODO: player action here
			if symbol == pyglet.window.key.LEFT:
				pass
			elif symbol == pyglet.window.key.RIGHT:
				pass


class PlayerEscSystem(ecs.EcsSystem):

	@classmethod
	def name(cls):
		return 'player-system'

	def __init__(self):
		super(PlayerEscSystem, self).__init__()
		self.player_entity_id = None

	def init(self):
		self.player_entity_id = None

		player_comp_list = self.manager.comps[PlayerIdentityEcsComponent.name()]
		for idx, eid in enumerate(self.manager.entities):
			if player_comp_list[idx]:
				self.player_entity_id = eid

	def update(self, dt):
		if self.manager.keys[pyglet.window.key.LEFT]:
			self.manager.get_system(ship.ShipEcsSystem.name()).turn_left(self.player_entity_id)
		elif self.manager.keys[pyglet.window.key.RIGHT]:
			self.manager.get_system(ship.ShipEcsSystem.name()).turn_right(self.player_entity_id)
		elif self.manager.keys[pyglet.window.key.UP]:
			self.manager.get_system(ship.ShipEcsSystem.name()).thrust_forward(self.player_entity_id)