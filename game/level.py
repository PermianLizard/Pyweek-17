import random

from plib import vec2d

import const
import phys
import coll
import player
import planet
import ship
import base
import asteroid
import render


SUN_SIZES = [128]
PLANET_SIZES = [64]
MOON_SIZES = [24]

POSITION_ANGLES = [i for i in xrange(0, 360, 40)]

NAMES = ['Tamde', 'Yolus', 'Trogg', 'Marduk', 'Eleen', 'Silias', 'Addr', 'Aggo', 'Teim', 'Tamut', 'Beda', 'Ponni']
NUMERALS = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']

PLANETS_MIN = 9
PLANETS_MAX = 10

PLANET_DISTANCE_MIN = 600
PLANET_DISTANCE_MAX = 700

# multiplier for how big a planet's gravity radius is (compared to max distance)
GRAV_RADIUS_MOD = 1
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

			grav_radius = PLANET_DISTANCE_MIN // 8

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
			ship.ShipEcsComponent(
				rotation=90.0, 
				rotation_speed=6.0, 
				thrust_force=200.0, 
				impact_resistance=50, 
				fuel=800, 
				passengers=0, 
				health=110),
			ship.RenderShipEcsComponent()])

def create_asteroid(ecsm):
	return ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, 100, False),
			coll.CollisionEcsComponent(14), 
			asteroid.AsteroidEcsComponent(
				impact_resistance=40.0, 
				health=100),
			asteroid.RenderAsteroidEcsComponent()])

def create_base(ecsm):
	return ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, 100, False),
			coll.CollisionEcsComponent(14), 
			base.BaseEcsComponent(
				radius=65, 
				fuel_load=True, 
				crew_load=20, 
				repairs=True,
				impact_resistance=40.0, 
				health=100),
			base.RenderBaseEcsComponent()])


def create_system(ecsm, data):
	for member in data['members']:
		type = member['type']
		if type == 'sun' or type == 'planet':
			member_id = ecsm.create_entity([phys.PhysicsEcsComponent(member['x'], member['y'], member['mass'], member['static']), 
				phys.GravityEcsComponent(member['grav_radius']),
				coll.CollisionEcsComponent(member['size']),
				planet.PlanetEcsComponent(member['name']),
				planet.RenderPlanetEcsComponent()])

			satellites = member['satellites']
			for satellite in satellites:
				if satellite['type'] == 'planet':
					satellite_id = ecsm.create_entity([phys.PhysicsEcsComponent(0.0, 0.0, satellite['mass'], False), 
						phys.GravityEcsComponent(satellite['grav_radius']),
						coll.CollisionEcsComponent(satellite['size']),
						planet.PlanetEcsComponent(''),
						planet.RenderPlanetEcsComponent()])
				if satellite['type'] == 'base':
					satellite_id = ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, satellite['mass'], False),
						coll.CollisionEcsComponent(satellite['size']), 
						base.BaseEcsComponent(
							radius=satellite['service_radius'], 
							fuel_load=satellite['fuel'], 
							crew_load=satellite['crew'], 
							repairs=satellite['repair'],
							impact_resistance=satellite['impact_resistence'], 
							health=satellite['health']),
						base.RenderBaseEcsComponent()])

				if satellite['type'] == 'ship':
					satellite_id = ecsm.create_entity([phys.PhysicsEcsComponent(0, 0, satellite['mass'], False),
						coll.CollisionEcsComponent(satellite['size']), 
						player.PlayerIdentityEcsComponent(), 
						ship.ShipEcsComponent(
							rotation=satellite['rotation'], 
							rotation_speed=satellite['rotation_speed'], 
							thrust_force=satellite['thrust_force'], 
							impact_resistance=satellite['impact_resistance'], 
							fuel=satellite['fuel'], 
							passengers=satellite['passengers'], 
							health=satellite['health']),
						ship.RenderShipEcsComponent()])

				# put the satelite in orbit
				ecsm.get_system(phys.PhysicsEcsSystem.name()).set_orbit(satellite_id, 
					member_id, 
					satellite['orbit_distance'], 
					satellite['orbit_angle'], 
					satellite['orbit_clockwise'])

def generate_system_data():
	# create some working data
	member_names = ['Tamde', 'Yolus', 'Trogg', 'Mar', 'Eleen', 'Silias', 'Addr', 'Aggo', 'Teim', 'Tamut', 'Beda', 'Ponni']
	member_position_angles = [i for i in xrange(0, 360, 40)]
	mass_mod = 10000
	member_padding = 1000
	member_grav_radius = member_padding // 2
	satellite_grav_radius = member_grav_radius // 2
	satellite_orbit_distance = member_grav_radius // 2
	satellite_position_angles = [i for i in xrange(0, 360, 90)]

	members = []

	# player ship
	player_ship_data = {'type': 'ship',
		'size': 14,
		'mass': 100,
		'rotation': 90.0,
		'rotation_speed': 6.0,
		'thrust_force': 200.0,
		'impact_resistance': 50.0,
		'fuel': 800,
		'passengers': 0,
		'health': 350,
		'orbit_distance': member_grav_radius * .75,
		'orbit_angle': 0,
		'orbit_clockwise': False
	}

	# sun
	members.append({'x': 0, 'y':0,
			'type': 'sun',
			'name':'Sol',
			'static': True,
			'size': 128,
			'mass': 128 * mass_mod,
			'grav_radius': member_grav_radius,
			'satellites': [player_ship_data,]
		})

	#planets 
	distance = 0
	num_planets = xrange(0, 7)
	for _ in num_planets:
		distance += member_padding

		planet_name = random.choice(member_names)
		member_names.remove(planet_name)

		# generate position
		pos = vec2d.vec2d(0, distance)
		angle = random.choice(member_position_angles)
		pos.rotate(angle)

		# member satellites
		satellites = []
		num_satellites = xrange(0, 2)
		satellite_angle_options = satellite_position_angles[:]
		for _ in num_satellites:
			satelite_angle = random.choice(satellite_angle_options)
			satellite_angle_options.remove(satelite_angle)

			satellites.append({'type': 'planet',
				'name':'Satellite',
				'size': 24,
				'mass': 24 * mass_mod,
				'grav_radius': satellite_grav_radius,
				'orbit_distance': satellite_orbit_distance,
				'orbit_angle': satelite_angle,
				'orbit_clockwise': True
			})
		# add one base satellite
		satelite_angle = random.choice(satellite_angle_options)
		satellite_angle_options.remove(satelite_angle)
		satellites.append({'type': 'base',
			'name':'Satellite',
			'size': 14,
			'mass': 300,
			'service_radius': 65,
			'fuel': True,
			'repair': True,
			'crew': 30,
			'impact_resistence': 50,
			'health': 200,
			'orbit_distance': satellite_orbit_distance,
			'orbit_angle': satelite_angle,
			'orbit_clockwise': True
		})
		members.append({'x': pos.x, 'y': pos.y,
			'type': 'planet',
			'name': planet_name,
			'static': True,
			'size': 64,
			'mass': 64 * mass_mod,
			'grav_radius': member_grav_radius,
			'satellites': satellites
		})

	data = {
		'members': members
	}

	return data

	#for planet_gen_id in xrange(random.randint(PLANETS_MIN, PLANETS_MIN + 1)):

def generate_system(ecsm):
	data = generate_system_data()
	create_system(ecsm, data)


def generate_system1(ecsm):
	available_names = NAMES[:]

	planet_ids = []

	prev_angle = None
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

			angle_options = POSITION_ANGLES[:]
			if prev_angle is not None:
				#print 'previous angle was', prev_angle
				a_idx = angle_options.index(prev_angle)
				angle_remove_range = (a_idx - 1, a_idx + 2)
				a_to_remove = []
				for ai in xrange(angle_remove_range[0], angle_remove_range[1]):
					if ai < 0:
						ai = len(angle_options) - 1
					elif ai > len(angle_options) - 1:
						ai -= len(angle_options)
					a_to_remove.append(angle_options[ai])

				for angle in a_to_remove:
					angle_options.remove(angle)

			#print angle_options

			angle = random.choice(angle_options)
			name = random.choice(available_names)
			available_names.remove(name)
			planet_ids.append(create_planet(ecsm, name, distance, angle, suppress_moons))

			prev_angle = angle

	home_planet = planet_ids[1]

	player_ship_id = create_player_ship(ecsm)
	a_id = create_asteroid(ecsm)
	b_id = create_base(ecsm)

	ecsm.get_system(phys.PhysicsEcsSystem.name()).set_orbit(player_ship_id, home_planet, 300, 0, False)

	ecsm.get_system(phys.PhysicsEcsSystem.name()).set_orbit(a_id, home_planet, 340, 30, False)

	ecsm.get_system(phys.PhysicsEcsSystem.name()).set_orbit(b_id, home_planet, 360, -30, False)