from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import os
import numpy as np

create_new_world = 0

inventory_blocks = []


inventory_opened = 0

try:
	world = np.load("world.npy")
except:
	print("World not found...")
	create_new_world = 1	
	world = np.zeros([60,60,60])



app = Ursina()
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
wood_texture = load_texture('assets/wood_block.png')
leave_texture = load_texture('assets/leaves_block.png')
sand_texture = load_texture('assets/sand_block.png')
cactus_texture = load_texture('assets/cactus_block.png')
planks_texture = load_texture('assets/planks_block.png')
brick_grey_texture = load_texture('assets/brick_grey_block.png')
glass_texture = load_texture('assets/glass_block.png')
furnace_texture = load_texture('assets/furnace_block.png')
crafting_texture = load_texture('assets/crafting_block.png')
grass_texture2 = load_texture('assets/grass.png')
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')
punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)
block_pick = 1

block_texture = grass_texture

window.fps_counter.enabled = False
window.exit_button.visible = False

class Inventory(Button):
	def __init__(self):
		super().__init__(
		parent = camera.ui,
		model = 'quad',
		scale = (.5, .8),
		origin = (-.5, .5),
		position = (-.3,.4),
		texture = 'white_cube',
		texture_scale = (5,8),
		color = color.dark_gray
			)
		self.item_parent = Entity(parent=self, scale=(1/5,1/8))
		
	def find_free_spot(self):                                                      
		taken_spots = [(int(e.x), int(e.y)) for e in self.item_parent.children]    
		for y in range(8):                                                         
			for x in range(5):                                                     
				if not (x,-y) in taken_spots:                                      
					return (x,-y)                                                  

	def append(self, item):
		name = item.replace('blocks/', ' ').title()
		
		blocks = Button(                                               
			parent = inventory.item_parent,			                                  
			texture = item,   
			color = color.white,                                                  
			tooltip = Tooltip('close inventory'),    
			origin = (-.5,.5),
			position = self.find_free_spot(),
			z = -.1,	
			
			)
		inventory_blocks.append(blocks)
		inventory_blocks[0].on_click = brick
		try:
			inventory_blocks[1].on_click = grey_brick
			try:
				inventory_blocks[2].on_click = cactus
				try:
					inventory_blocks[3].on_click = crafting_table
					try:
						inventory_blocks[4].on_click = dirt
						try:
							inventory_blocks[5].on_click = furnace
							try:
								inventory_blocks[6].on_click = grass
								try:
									inventory_blocks[7].on_click = leaves
									try:
										inventory_blocks[8].on_click = planks										
										try:
											inventory_blocks[9].on_click = sand
											try:
												inventory_blocks[10].on_click = stone
												try:
													inventory_blocks[11].on_click = wood
													try:
														inventory_blocks[12].on_click = glass
														try:
															inventory_blocks[39].on_click = close
														except:
															pass
													except:
														pass
												except:
													pass
											except:
												pass
										except:
											pass
									except:
										pass
								except:
									pass
							except:
								pass
						except:
							pass
					except:
						pass
				except:
					pass
			except:
				pass
				
		except:
			pass
		
		#name = item.replace('_', ' ').title()
		
		blocks.tooltip = Tooltip(name)
		blocks.tooltip.background.color = color.color(0,0,0,.8)
	
def brick():
	global block_pick, block_texture
	block_texture = brick_texture
	block_pick = 3
def grey_brick():
	global block_pick, block_texture
	block_texture = brick_grey_texture
	block_pick = 10
def cactus():
	global block_pick, block_texture
	block_texture =  cactus_texture
	block_pick = 8
def crafting_table():
	global block_pick, block_texture
	block_texture =  crafting_texture
	block_pick = 12
def dirt():
	global block_pick, block_texture
	block_texture = dirt_texture
	block_pick = 4
def furnace():
	global block_pick, block_texture
	block_texture = furnace_texture
	block_pick = 13
def grass():
	global block_pick, block_texture
	block_texture = grass_texture
	block_pick = 1
def leaves():
	global block_pick, block_texture
	block_texture =  leave_texture
	block_pick = 6
def planks():
	global block_pick, block_texture
	block_texture = planks_texture
	block_pick = 9
def sand():
	global block_pick, block_texture
	block_texture = sand_texture
	block_pick = 7
def stone():
	global block_pick, block_texture
	block_texture = stone_texture	
	block_pick = 2
def wood():
	global block_pick, block_texture
	block_texture = wood_texture
	block_pick = 5
def glass():
	global block_pick, block_texture
	block_texture = glass_texture
	block_pick = 11
def grass_other():
	global block_pick, block_texture
	block_texture = grass_texture2
	block_pick = 14


class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grass_texture):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			scale = 0.5)

	def input(self,key):
		global inventory_opened
		if self.hovered:
			if key == 'right mouse down':
				pos = self.position + mouse.normal
				punch_sound.play()
				if block_pick == 1: 
										
					voxel = Voxel(position = pos, texture = grass_texture)
					#print(pos)					
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
					#print(world[int(pos[0]), int(pos[1]), int(pos[2])])					
				if block_pick == 2: 
									
					voxel = Voxel(position = pos, texture = stone_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
				if block_pick == 3: 
					
					voxel = Voxel(position = pos, texture = brick_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
				if block_pick == 4: 
					
					voxel = Voxel(position = pos, texture = dirt_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
				if block_pick == 5: 
					
					voxel = Voxel(position = pos, texture = wood_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
				if block_pick == 6: 
					
					voxel = Voxel(position = pos, texture = leave_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
				if block_pick == 7: 
					
					voxel = Voxel(position = pos, texture = sand_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
				if block_pick == 8: 
					
					voxel = Voxel(position = pos, texture = cactus_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
				if block_pick == 9: 
					
					voxel = Voxel(position = pos, texture = planks_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
				if block_pick == 10: 
					
					voxel = Voxel(position = pos, texture = brick_grey_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
				if block_pick == 11: 
					
					voxel = Voxel(position = pos, texture = glass_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
				if block_pick == 12: 
					
					voxel = Voxel(position = pos, texture = crafting_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick
				if block_pick == 13: 
					
					voxel = Voxel(position = pos, texture = furnace_texture)
					world[int(pos[0]), int(pos[1]), int(pos[2])] = block_pick

			if key == 'left mouse down':
				pos = self.position
				world[int(pos[0]), int(pos[1]), int(pos[2])] = 0
				#print(world[int(pos[0]), int(pos[1]), int(pos[2])])
				punch_sound.play()				
				destroy(self)
				
			

def update():
	global block_pick, inventory_opened, inventory,block_texture
	block.texture = block_texture

	if held_keys['left mouse']:
		hand.active()
	else:
		hand.passive()
	if held_keys['right mouse']:
		block.active()
	else:
		block.passive()
		
	if held_keys['e']: 
		np.save("world.npy", world)
		print("World saved...")
	
	if held_keys['i']:
		inventory_opened = 1	
		inventory_blocks.clear() 
		try:
			destroy(inventory)
			#destroy(add_item_button)
			inventory = Inventory()
			add_item()
			mouse.locked = False 
			mouse.visible = True
			mouse.enabled = True		
			
			#add_button()
			
			
		except:
			inventory = Inventory()    
			add_item()
			
			mouse.locked = False 
			mouse.visible = True
			mouse.enabled = True
			
			#add_button()
		
	if held_keys['c']:
		inventory_opened = 0	
		close()
		mouse.locked = True 
		mouse.visible = False
		mouse.enabled = True
		
	
	

class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 150,
			double_sided = True)

class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = Vec3(150,-20,0),
			position = Vec2(0.9,-0.6))
	def active(self):
		self.position = Vec2(0.8,-0.5)

	def passive(self):
		self.position = Vec2(0.9,-0.6)
			
class Block(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/block',
			texture = block_texture,
			scale = 0.2,
			rotation = Vec3(20,220,0),
			position = Vec2(-0.6,-0.4))
	def active(self):
		self.position = Vec2(-0.5,-0.3)

	def passive(self):
		self.position = Vec2(-0.6,-0.4)
	

if create_new_world == 1:
	for z in range(20):
		for x in range(20):
			voxel = Voxel(position = (x,0,z))
			world[x,0,z] = 1
else:
	for x in range(40):
		for y in range(40):
			for z in range(40):
				if world[x, y, z] == 1:
					texture = grass_texture
				if world[x, y, z] == 2:
					texture = stone_texture
				if world[x, y, z] == 3:
					texture = brick_texture
				if world[x, y, z] == 4:
					texture = dirt_texture
				if world[x, y, z] == 5:
					texture = wood_texture
				if world[x, y, z] == 6:
					texture = leave_texture
				if world[x, y, z] == 7:
					texture = sand_texture
				if world[x, y, z] == 8:
					texture = cactus_texture
				if world[x, y, z] == 9:
					texture = planks_texture
				if world[x, y, z] == 10:
					texture = brick_grey_texture
				if world[x, y, z] == 11:
					texture = glass_texture
				if world[x, y, z] == 12:
					texture = crafting_texture
				if world[x, y, z] == 13:
					texture = furnace_texture
				if world[x,y,z] != 0:
					voxel = Voxel(position = (x,y,z), texture = texture)

inventory_opened = 0

		   

if __name__ == '__main__':	 
	sky = Sky()
	hand = Hand()
	
	block = Block()
	block.texture = block_texture
	
	if inventory_opened == 1:
		block.texture = block_texture
		inventory = Inventory() 
		
		
	if inventory_opened == 0:
		block.texture = block_texture
		Player = FirstPersonController(origin_y = -.5, origin_x = 5)
		Player.jump_height = 1
		Player.mouse_sensitivity = Vec2(40, 40)
	
	def add_item():
		global inventory_opened, inventory
		
		if inventory_opened == 1:
			#inventory = ['grass block', 'stone block', 'brick_block', 'dirt_block', 'grey brick block', 'cactus block', 'crafting_table', 'furnace block', 'glass block', 'leaves block', 'planks block', 'sand block', 'wood block']
			inventory.append('blocks/brick block')
			inventory.append('blocks/grey brick block')
			inventory.append('blocks/cactus block')
			inventory.append('blocks/crafting table')
			inventory.append('blocks/dirt block')
			inventory.append('blocks/furnace')
			inventory.append('blocks/grass block')
			inventory.append('blocks/leaves block')
			inventory.append('blocks/planks block')
			inventory.append('blocks/sand block')
			inventory.append('blocks/stone block')
			inventory.append('blocks/wood block')
			inventory.append('blocks/glass block')
			for empty in range(26):
				inventory.append('blocks/ ')
			inventory.append('blocks/close (c)')
			
			
			
	def close():
		global add_item_button
		destroy(inventory)
		inventory_opened = 0
		mouse.locked = True 
		mouse.visible = False
		mouse.enabled = True
		block.texture = block_texture
		'''
		if inventory_opened == 0:
			player = FirstPersonController(jump_height = 1, )
	
			'''
		
		
				
	for i in range(1):
		add_item()        
	
	                                        

	app.run()





