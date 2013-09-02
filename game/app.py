from plib import director
import menu
import game

def init():
	menu.init()
	game.init()
	#director.director.push(menu.menu_scene)
	director.director.push(game.game_scene)

def cleanup():
	pass