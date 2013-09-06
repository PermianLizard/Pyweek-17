import math
from plib import vec2d
from plib import ecs
import phys

class PlanetEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'planet-component'

	def __init__(self, pname):
		super(PlanetEcsComponent, self).__init__()
		self.pname = pname

	def __str__(self):
		return 'PlanetEcsComponent'


class RenderPlanetEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'render-planet-component'

	def __init__(self):
		super(RenderPlanetEcsComponent, self).__init__()

	def __str__(self):
		return 'RenderPlanetEcsComponent'