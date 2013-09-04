import random

from plib import vec2d

import const
import phys
import coll
import player
import planet
import ship
import render


SUN_SIZES = [120, 128]
PLANET_SIZES = [32, 40, 48, 56, 64, 72, 80, 88]
MOON_SIZES = [16, 24]

POSITION_ANGLES = [i for i in xrange(0, 360, 45)]

NAMES = ['Tamande', 'Yolus', 'Tar-ogg', 'Marduk', 'Eileen', 'Silias', 'Addren', 'Aggo', 'Teim', 'Tamut']
NUMERALS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']

PLANET_DISTANCE_MIN = 400
PLANET_DISTANCE_MAX = 600


def create_sun(ecsm, name):
	size = random.choice(SUN_SIZES)	
	mass = size * 10000

	grav_radius = PLANET_DISTANCE_MAX * 0.6

	return ecsm.create_entity([phys.PhysicsEcsComponent(-200, 0, mass, True), 
			phys.GravityEcsComponent(grav_radius),
			coll.CollisionEcsComponent(size),
			planet.PlanetEcsComponent(name),
			render.RenderPlanetEcsComponent()])


def create_planet(ecsm, name, distance, angle):
	posv = vec2d.vec2d(distance, 0)
	posv.rotate(angle)

	size = random.choice(PLANET_SIZES)	
	mass = size * 10000 # TODO density

	grav_radius = PLANET_DISTANCE_MAX * 0.9

	planet_id = ecsm.create_entity([phys.PhysicsEcsComponent(posv.x, posv.y, mass, True), 
			phys.GravityEcsComponent(grav_radius),
			coll.CollisionEcsComponent(size),
			planet.PlanetEcsComponent(name),
			render.RenderPlanetEcsComponent()])

	# give this planet some satellites
	if size >= 56:		
		moons = random.randint(0, 2)
		available_angles = POSITION_ANGLES[:]

		for mi in xrange(moons):
			size = random.choice(MOON_SIZES)	
			mass = size * 10000 # TODO density

			grav_radius = PLANET_DISTANCE_MAX // 8

			moon_id = ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, mass, False), 
				phys.GravityEcsComponent(grav_radius), # why this no work!?
				coll.CollisionEcsComponent(size),
				planet.PlanetEcsComponent(''),
				render.RenderPlanetEcsComponent()])

			distance = PLANET_DISTANCE_MAX // 4 + ((PLANET_DISTANCE_MAX // 4) * mi) - 30
			angle = random.choice(available_angles)
			available_angles.remove(angle)

			ecsm.get_system(phys.PhysicsEcsSystem.name()).set_orbit(moon_id, planet_id, distance, angle, True)


def generate(ecsm):
	available_names = NAMES[:]

	planet_ids = []
	available_angles = POSITION_ANGLES[:]

	distance = PLANET_DISTANCE_MIN * 1.5
	for planet_system_id in xrange(random.randint(9, 10)):
		if planet_system_id == 0:
			planet_id = create_sun(ecsm, 'Sol')
		else:
			distance += random.randint(PLANET_DISTANCE_MIN, PLANET_DISTANCE_MAX)
			angle = random.choice(available_angles)
			available_angles.remove(angle)
			name = random.choice(available_names)
			available_names.remove(name)
			planet_id = create_planet(ecsm, name, distance, angle)

		planet_ids.append(planet_id)