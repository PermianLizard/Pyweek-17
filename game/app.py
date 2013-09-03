from plib import director
import font
import img
import menu
import game
import map

def init():
	font.init()
	img.init()
	menu.init()
	game.init()
	map.init()
	#director.director.push(menu.menu_scene)
	director.director.push(game.game_scene)

def cleanup():
	pass