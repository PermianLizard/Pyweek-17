import pyglet
from pyglet import gl

from plib.director import director
from plib import scene

import const
import game
import font

import phys
import coll
import player
import planet
import ship
import render

map_scene = None

ZOOM = 0.09

def init():
	global map_scene
	map_scene = MapScene()

class MapScene(scene.Scene):

	def __init__(self):
		super(MapScene, self).__init__()

	def enter(self):
		pass

	def exit(self):
		pass

	def draw(self):
		ecsm = game.ecsm

		phys_comp_list = ecsm.comps[phys.PhysicsEcsComponent.name()]
		grav_comp_list = ecsm.comps[phys.GravityEcsComponent.name()]
		coll_comp_list = ecsm.comps[coll.CollisionEcsComponent.name()]
		planet_comp_list = ecsm.comps[planet.PlanetEcsComponent.name()]
		ship_comp_list = ecsm.comps[ship.ShipEcsComponent.name()]
		rend_plan_comp_list = ecsm.comps[render.RenderPlanetEcsComponent.name()]
		rend_ship_comp_list = ecsm.comps[render.RenderShipEcsComponent.name()]

		entities = ecsm.entities

		player_entity_id = ecsm.get_system(player.PlayerEscSystem.name()).player_entity_id
		player_physc = ecsm.get_entity_comp(player_entity_id, phys.PhysicsEcsComponent.name())

		gl.glPushMatrix()
		gl.glLoadIdentity()

		if player_physc:
			gl.glTranslatef((-player_physc.pos.x * ZOOM) + const.WIDTH // 2, (-player_physc.pos.y * ZOOM) + const.HEIGHT // 2, 0.0)
		else:
			gl.glTranslatef(const.WIDTH // 2, const.HEIGHT // 2, 0.0)

		for idx, eid in enumerate(entities):
			shipc = ship_comp_list[idx]
			planetc = planet_comp_list[idx]

			physc = phys_comp_list[idx]
			collc = coll_comp_list[idx]

			# show planet
			if planetc:
				rpc = rend_plan_comp_list[idx]
				render.draw_circle(physc.pos.x * ZOOM, physc.pos.y * ZOOM, collc.radius * ZOOM)

				if planetc.pname:
					label = pyglet.text.Label(planetc.pname,
	                          font_name=font.FONT_MONO.name,
	                          font_size=9,
	                          x=physc.pos.x * ZOOM, y=physc.pos.y * ZOOM - ((collc.radius + 100) * ZOOM ), #  + collc.radius + 5
	                          anchor_x='center', anchor_y='center',
	                          color=(0, 255, 0, 255))
					label.draw()

		# show player position
		
		if player_physc:
			render.draw_circle(player_physc.pos.x * ZOOM, player_physc.pos.y * ZOOM, 30 * ZOOM, color=(1, 0, 0, 1))

		gl.glPopMatrix()

	def update(self, dt):
		pass

	def on_key_press(self, symbol, modifiers):
		if symbol == pyglet.window.key.ESCAPE:
			director.pop()
		#elif symbol == pyglet.window.key.P:
		#	self.paused = not self.paused
		#elif not self.paused:
		#	ecsm.on_key_press(symbol, modifiers)

	def on_mouse_press(self, x, y, button, modifiers):
		pass