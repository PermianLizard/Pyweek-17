from plib import director
import font
import menu
import game

def init():
	font.init()
	menu.init()
	game.init()
	#director.director.push(menu.menu_scene)
	director.director.push(game.game_scene)

def cleanup():
	pass