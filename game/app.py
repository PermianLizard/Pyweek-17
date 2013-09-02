from plib import director
import menu
import game

def init():
	menu.init()
	game.init()
	director.director.push(menu.menu_scene)

def cleanup():
	print 'cleanup!'