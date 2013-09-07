from plib import director
import font
import img
import anim
import menu
import instruct
import game
import end
import map

def init():
	font.init()
	img.init()
	anim.init()
	menu.init()
	instruct.init()
	game.init()
	map.init()
	end.init()
	director.director.push(menu.menu_scene)

def cleanup():
	pass