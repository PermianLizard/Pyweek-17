from plib import director
import font
import img
import anim
import menu
import game
import end
import map

def init():
	font.init()
	img.init()
	anim.init()
	menu.init()
	game.init()
	map.init()
	end.init()
	#director.director.push(menu.menu_scene)
	director.director.push(game.game_scene)
	#director.director.push(end.victory_scene)

def cleanup():
	pass