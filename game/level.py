import random

from plib import vec2d

import const
import phys
import coll
import player
import planet
import ship
import asteroid
import render


SUN_SIZES = [120, 128]
PLANET_SIZES = [56, 64, 72, 80]
#PLANET_SIZES = [32, 40, 48, 56, 64, 72, 80, 88]
MOON_SIZES = [16, 24]

POSITION_ANGLES = [i for i in xrange(0, 360, 45)]

NAMES = ['Tamande', 'Yolus', 'Tar-ogg', 'Marduk', 'Eileen', 'Silias', 'Addren', 'Aggo', 'Teim', 'Tamut']
NUMERALS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']

PLANETS_MIN = 6
PLANETS_MAX = 7

PLANET_DISTANCE_MIN = 400
PLANET_DISTANCE_MAX = 600

# multiplier for how big a planet's gravity radius is (compared to max distance)
GRAV_RADIUS_MOD = 0.9
# min size of planets that have moons
MIN_MOON_PLANET_SIZE = 56

# multiplier giving a planet's mass (relative to its size)
MASS_MOD = 10000

def create_sun(ecsm, name):
	size = random.choice(SUN_SIZES)	
	mass = size * MASS_MOD

	grav_radius = PLANET_DISTANCE_MAX * GRAV_RADIUS_MOD

	return ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, mass, True), 
			phys.GravityEcsComponent(grav_radius),
			coll.CollisionEcsComponent(size),
			planet.PlanetEcsComponent(name),
			planet.RenderPlanetEcsComponent()])

def create_planet(ecsm, name, distance, angle, suppress_moons=False):
	posv = vec2d.vec2d(distance, 0)
	posv.rotate(angle)

	size = random.choice(PLANET_SIZES)	
	mass = size * MASS_MOD # TODO density

	grav_radius = PLANET_DISTANCE_MAX * GRAV_RADIUS_MOD

	planet_id = ecsm.create_entity([phys.PhysicsEcsComponent(posv.x, posv.y, mass, True), 
			phys.GravityEcsComponent(grav_radius),
			coll.CollisionEcsComponent(size),
			planet.PlanetEcsComponent(name),
			planet.RenderPlanetEcsComponent()])

	# give this planet some satellites
	if size >= MIN_MOON_PLANET_SIZE and not suppress_moons:		
		moons = random.randint(0, 2)
		available_angles = POSITION_ANGLES[:]

		for mi in xrange(moons):
			size = random.choice(MOON_SIZES)	
			mass = size * MASS_MOD # TODO density

			grav_radius = PLANET_DISTANCE_MAX // 8

			moon_id = ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, mass, False), 
				phys.GravityEcsComponent(grav_radius), # why this no work!?
				coll.CollisionEcsComponent(size),
				planet.PlanetEcsComponent(''),
				planet.RenderPlanetEcsComponent()])

			distance = PLANET_DISTANCE_MAX // 3 + ((PLANET_DISTANCE_MAX // 3) * mi) - 30
			angle = random.choice(available_angles)
			available_angles.remove(angle)

			ecsm.get_system(phys.PhysicsEcsSystem.name()).set_orbit(moon_id, planet_id, distance, angle, True)

	return planet_id

def create_player_ship(ecsm):
	return ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, 100, False),
			coll.CollisionEcsComponent(14), 
			player.PlayerIdentityEcsComponent(), 
			ship.ShipEcsComponent(90.0, 6, 500.0),
			ship.RenderShipEcsComponent()])

def create_asteroid(ecsm):
	return ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, 1000, False),
			coll.CollisionEcsComponent(14), 
			asteroid.AsteroidEcsComponent(),
			asteroid.RenderAsteroidEcsComponent()])

def generate_system(ecsm):
	available_names = NAMES[:]

	available_angles = POSITION_ANGLES[:]

	planet_ids = []

	distance = PLANET_DISTANCE_MIN * 1.5 # place a little further away from the sun
	for planet_gen_id in xrange(random.randint(PLANETS_MIN, PLANETS_MIN + 1)):
		# sun
		if planet_gen_id == 0:
			planet_ids.append(create_sun(ecsm, 'Sol'))
		# planets
		else:
			suppress_moons = False
			if planet_gen_id == 1:
				suppress_moons = True
			distance += random.randint(PLANET_DISTANCE_MIN, PLANET_DISTANCE_MAX)
			angle = random.choice(available_angles)
			available_angles.remove(angle)
			name = random.choice(available_names)
			available_names.remove(name)
			planet_ids.append(create_planet(ecsm, name, distance, angle, suppress_moons))

	home_planet = planet_ids[1]

	player_ship_id = create_player_ship(ecsm)
	a_id = create_asteroid(ecsm)

	ecsm.get_system(phys.PhysicsEcsSystem.name()).set_orbit(player_ship_id, home_planet, 300, 0, False)

	ecsm.get_system(phys.PhysicsEcsSystem.name()).set_orbit(a_id, home_planet, 340, 0, False)