import random
import time

#forgive me father for I have sinned
global skull
skull = True
boy = False

class Room(object):
	def __init__(self):
		#dict of actions and the rooms they lead to
		self.next_rooms = {}
		self.rt = "base"
		self.true_name = None

	def go(self, action):
		next_room = self.next_rooms.get(action)
		if not next_room == None:
			return next_room()
		else:
			return None

	def name_room(self):
		return self.true_name+'@'+str(skull)+'@'+str(boy)

	def room_type(self):
		return self.rt

class CombatRoom1(Room):
	def __init__(self):
		self.health = 0
		self.true_name = 'combat'
		self.ph = 0
		self.bullets = 0
		self.next_rooms = {}
		self.pa = None

	def go(self, action):
		#try-except used to see if the next room is an exit or combat2 room
		try:
			next_room = self.next_rooms.get(action)
		except TypeError:
			next_room = self.next_rooms.get(action)()
		return next_room

	def name_room(self):
		return self.true_name+'@'+str(self.health)+'@'+str(self.ph)+'@'+str(self.bullets)+'@'+str(skull)+'@'+str(boy)


class CombatRoom2(CombatRoom1):
	def go(self, action):
		return self.next_rooms.get(action)(self.health, self.ph, self.bullets)

	def name_room(self):
		return self.true_name+'@'+str(self.health)+'@'+str(self.ph)+'@'+str(self.bullets)+'@'+self.pa+'@'+str(skull)+'@'+str(boy)


class TheTown1(Room):
	def __init__(self):
		self.next_rooms = {'continue': TheTown2}
		self.name = 'Tull'
		self.rt = 'continue'
		self.true_name = 'TheTown1'
		self.description = """You are Roland of Gilead,
the last in a long line of Gunslingers - 
knights with a mythic affinity for weapons
of death. Your aim is the Dark Tower. Supported by 19 beams, 
each of which is protected by a guardian, the Dark Tower holds together
the very Fabric of reality. The world you inhabit has been 
crumbling as the sinister forces of the Crimson
King work to destroy the tower. Now, you search for 
the Man in Black, an ancient evil, and a servant to
the Crimson King.\nYou hope he knows the way."""

class TheTown2(Room):
	def __init__(self):
		self.next_rooms = {'continue': TownsPeople1}
		self.name = 'Tull'
		self.rt = 'continue'
		self.true_name = 'TheTown2'
		self.description = """You've just arrived at the small town of Tull.
Unfortunately, the kindly townspeople have been
warped by the man in black. The once peace loving 
citizens are now hungry for your blood, and they
come at you in droves.
You have no choice but to fight."""

class TownsPeople1(CombatRoom1):
	def __init__(self, health=100, player_health=100, bullets=6):
		self.health = health
		self.bullets = bullets
		self.ph = player_health
		self.name = 'The Mob'
		#yesno instead of combat
		self.rt = 'combat1'
		self.true_name = 'TownsPeople1'	
		self.next_rooms = attack_dict(self.ph, self.health, self.bullets, TheTown3, TownsPeople2)
		self.ending = "The man in black travels with your soul in his pocket"

class TownsPeople2(CombatRoom2):
	def __init__(self, health=100, ph=100, bullets=6, pa=None, cmbt=True):
		self.health = health
		self.bullets = bullets
		self.rt = 'combat2'
		self.name = 'The Mob'
		self.true_name = 'TownsPeople2'
		self.attacks = ["""The towns people call for your death.
They throw debris from all sides.
Rocks, cans and gardening tools rain down.""","""The towns people surge forward!
They scream for your head as they thrust pitchforks and broomsticks"""]
		self.damages = [10, 24]
		self.chance_to_hit = [100, 50]
		self.size = 'large'
		self.pa = pa
		if cmbt:
			self.ph, self.health, self.ea, self.bullets, self.pa = combat(pa, self.attacks, self.damages, self.chance_to_hit,
							self.size, ph, health, bullets, self.name)
		else:
			self.ph, self.ea, self.health, self.bullets = ph, None, health, bullets
		self.next_rooms = {'continue':TownsPeople1}

class TheTown3(Room):
	def __init__(self):
		self.next_rooms = {'continue': TheGreatExpanse1}
		self.name = 'Tull'
		self.rt = 'continue'
		self.true_name = 'TheTown3'
		self.description = """Fifty shots. Fifty bodies full of lead.
There isn't time to mourn the dead. 
You must keep moving.
Upon the horizon you see smoke.
The Man in Black wants you to follow.
You continue onto the great expanse."""

class TheGreatExpanse1(Room):
	def __init__(self):
		self.next_rooms = {'continue': TheGreatExpanse2}
		self.name = 'The Great Expanse'
		self.rt = 'continue'
		self.true_name = 'TheGreatExpanse1'
		self.description = ' '

class TheGreatExpanse2(Room):
	def __init__(self):
		self.next_rooms = {'continue': TheManInBlack1}
		self.name = 'The Great Expanse'
		self.rt = 'continue'
		self.true_name = 'TheGreatExpanse2'
		self.description = ' '

class TheManInBlack1(CombatRoom1):
	def __init__(self, health=100, player_health=100, bullets=6):
		self.health = health
		self.bullets = bullets
		self.ph = player_health
		self.name = 'The Man In Black'
		self.rt = 'combat1'
		self.true_name = 'TheManInBlack1'	
		self.next_rooms = attack_dict(self.ph, self.health, self.bullets, TheGreatExpanse3, TheManInBlack2)
		self.ending = "The man in black travels with your soul in his pocket"

class TheManInBlack2(CombatRoom2):
	def __init__(self, health=100, ph=100, bullets=6, pa=None, cmbt=True):
		self.health = health
		self.bullets = bullets
		self.rt = 'combat2'
		self.name = 'The Man In Black'
		self.true_name = 'TheManInBlack2'
		self.attacks = [""" """,""" """]
		self.damages = [10, 24]
		self.chance_to_hit = [100, 50]
		self.size = 'small'
		self.pa = pa
		if cmbt:
			self.ph, self.health, self.ea, self.bullets, self.pa = combat(pa, self.attacks, self.damages, self.chance_to_hit,
							self.size, ph, health, bullets, self.name)
		else:
			self.ph, self.ea, self.health, self.bullets = ph, None, health, bullets
		self.next_rooms = {'continue':TheManInBlack1}

class TheGreatExpanse3(Room):
	def __init__(self):
		self.next_rooms = {'yes': TheGreatExpanseSkull, 'no':TheGreatExpanseNoSkull}
		self.name = 'The Great Expanse'
		self.rt = 'yesno'
		self.true_name = 'TheGreatExpanse3'
		self.description = ' '

class TheGreatExpanseSkull(Room):
	def __init__(self):
		global skull
		skull = True
		self.next_rooms = {'continue': TheBeach1}
		self.name = 'The Great Expanse'
		self.rt = 'continue'
		self.true_name = 'TheGreatExpanseSkull'
		self.description = ' '

class TheGreatExpanseNoSkull(Room):
	def __init__(self):
		global skull
		skull = False
		self.next_rooms = {'continue': TheBeach1}
		self.name = 'The Great Expanse'
		self.rt = 'continue'
		self.true_name = 'TheGreatExpanseSkull'
		self.description = ' '

class TheBeach1(Room):
	def __init__(self):
		self.next_rooms = {'wait':TheBeach2, 'open':JakeDoor1}
		self.name = 'The Beach'
		self.rt = 'show_room'
		self.true_name = 'TheBeach1'
		self.description = ' '

class TheBeach2(Room):
	def __init__(self):
		self.next_rooms = {'continue':Lobstrocities1}
		self.name = 'The Beach'
		self.rt = 'continue'
		self.true_name = 'TheBeach2'
		self.description = ' '

class Lobstrocities1(CombatRoom1):
	def __init__(self, health=100, player_health=100, bullets=6):
		self.health = health
		self.bullets = bullets
		self.ph = player_health
		self.name = 'Lobstrocities'
		self.rt = 'combat1'
		self.true_name = 'Lobstrocities1'	
		self.next_rooms = attack_dict(self.ph, self.health, self.bullets, Lobstrocities3, Lobstrocities2)
		self.ending = "CHANGE THIS"

class Lobstrocities2(CombatRoom2):
	def __init__(self, health=100, ph=100, bullets=6, pa=None, cmbt=True):
		self.health = health
		self.bullets = bullets
		self.rt = 'combat2'
		self.name = 'Lobstrocities'
		self.true_name = 'Lobstrocities2'
		self.attacks = [""" """,""" """]
		self.damages = [10, 24]
		self.chance_to_hit = [100, 50]
		self.size = 'large'
		self.pa = pa
		if cmbt:
			self.ph, self.health, self.ea, self.bullets, self.pa = combat(pa, self.attacks, self.damages, self.chance_to_hit,
							self.size, ph, health, bullets, self.name)
		else:
			self.ph, self.ea, self.health, self.bullets = ph, None, health, bullets
		self.next_rooms = {'continue':Lobstrocities1}

class Lobstrocities3(Room):
	def __init__(self):
		self.next_rooms = {'yes':JakeDoor1, 'no':TheBeach3}
		self.name = 'The Beach'
		self.rt = 'yesno'
		self.true_name = 'Lobstrocities3'
		self.description = ' '

class JakeDoor1(Room):
	def __init__(self):
		self.next_rooms = {'continue':JakeDoor2}
		self.name = 'The Door'
		self.rt = 'continue'
		self.true_name = 'JakeDoor1'
		self.description = ' '

class JakeDoor2(Room):
	def __init__(self):
		self.next_rooms = {'yes':TakeJake, 'no':DontTakeJake}
		self.name = 'The Door'
		self.rt = 'yesno'
		self.true_name = 'JakeDoor2'
		self.description = ' '

class TakeJake(Room):
	def __init__(self):	
		global boy
		boy = True
		self.next_rooms = {'continue':TheBeach3}
		self.name = 'The Door'
		self.rt = 'continue'
		self.true_name = 'TakeJake'
		self.description = ' '

class DontTakeJake(Room):
	def __init__(self):	
		global boy
		boy = False
		self.next_rooms = {'continue':TheBeach3}
		self.name = 'The Door'
		self.rt = 'continue'
		self.true_name = 'DontTakeJake'
		self.description = ' '

class TheBeach3(Room):
	def __init__(self):
		self.next_rooms = {'continue':TheBeach4}
		self.name = 'The Beach'
		self.rt = 'continue'
		self.true_name = 'TheBeach3'
		self.description = ' '

class TheBeach4(Room):
	def __init__(self):
		self.next_rooms = {'forest':Forest1, 'door':VampDoor1}
		self.name = 'The Beach'
		self.rt = 'show_room'
		self.true_name = 'TheBeach4'
		self.description = ' '

class Forest1(Room):
	def __init__(self):
		self.next_rooms = {'continue':Forest2}
		self.name = 'The Forest'
		self.rt = 'continue'
		self.true_name = 'Forest1'
		self.description = ' '

class Forest2(Room):
	def __init__(self):
		self.next_rooms = {'continue':Shardik1}
		self.name = 'The Forest'
		self.rt = 'continue'
		self.true_name = 'Forest2'
		self.description = ' '

class Shardik1(CombatRoom1):
	def __init__(self, health=100, player_health=100, bullets=6):
		self.health = health
		self.bullets = bullets
		self.ph = player_health
		self.name = 'Shardik'
		self.rt = 'combat1'
		self.true_name = 'Shardik1'	
		self.next_rooms = attack_dict(self.ph, self.health, self.bullets, ShardikDies, Shardik2)
		self.ending = "CHANGE THIS"	

class Shardik2(CombatRoom2):
	def __init__(self, health=100, ph=100, bullets=6, pa=None, cmbt=True):
		self.health = health
		self.bullets = bullets
		self.rt = 'combat2'
		self.name = 'Shardik'
		self.true_name = 'Shardik2'
		self.attacks = [""" """,""" """]
		self.damages = [10, 24]
		self.chance_to_hit = [100, 50]
		self.size = 'large'
		self.pa = pa
		if cmbt:
			self.ph, self.health, self.ea, self.bullets, self.pa = combat(pa, self.attacks, self.damages, self.chance_to_hit,
							self.size, ph, health, bullets, self.name)
		else:
			self.ph, self.ea, self.health, self.bullets = ph, None, health, bullets
		self.next_rooms = {'continue':Shardik1}

class ShardikDies(Room):
	def __init__(self):
		self.next_rooms = {'continue':Death}
		self.name = 'The Forest'
		self.rt = 'continue'
		self.true_name = 'ShardikDies'
		self.description = ' '

class VampDoor1(Room):
	def __init__(self):
		self.next_rooms = {'continue':VampDoor2}
		self.name = 'The Dixie Pig'
		self.rt = 'continue'
		self.true_name = 'VampDoor1'
		self.description = ' '

class VampDoor2(Room):
	def __init__(self):
		print(skull)
		if skull:
			self.next_rooms = {'continue':VampDoorWin}
		else:
			self.next_rooms = {'continue':VampDoorLose}
		self.name = 'The Dixie Pig'
		self.rt = 'continue'
		self.true_name = 'VampDoor2'
		self.description = ' '

class VampDoorWin(Room):
	def __init__(self):
		self.next_rooms = {'continue':MonoRail1}
		self.name = 'The Dixie Pig'
		self.rt = 'continue'
		self.true_name = 'VampDoorWin'
		self.description = ' '

class VampDoorLose(Room):
	def __init__(self):
		self.next_rooms = {'continue':Death}
		self.name = 'The Dixie Pig'
		self.rt = 'continue'
		self.true_name = 'VampDoorLose'
		self.description = ' '

class MonoRail1(Room):
	def __init__(self):
		self.next_rooms = {'continue':Death}
		self.name = 'The Metropolis'
		self.rt = 'continue'
		self.true_name = 'MonoRail1'
		self.description = ' '	


class Death(Room):
	def __init__(self):
		#once you get is working delete self.next_rooms
#		self.next_rooms = {}
		self.name = 'You Died'
		self.rt = 'end'
		self.true_name = 'Death'
		self.description = """You made it this far, but the tower is farther.
And as you died, the world moved on"""


def combat(pa, attacks, dmgs, chances, size, ph, eh, bu, enemy_name):
	#find enemy attack
	attack_idx = random.randint(0, len(attacks)-1)
	chance = chances[attack_idx]
	roll = random.randint(1,100)
	if roll > chance:
		damage = 0
		attack = f"{enemy_name} misses!"
	else:
		damage = dmgs[attack_idx]
		attack = attacks[attack_idx]

	#find damage to enemy and resulting bullets
	player_damage=0
	if pa == 'reload':
		bu = 6
		pa = 'That nimble reloading trick.'
	elif bu <=0:
		pa = 'Your chambers are empty gunslinger.'
		bu = 0
		player_damage=0
	elif pa == 'aimshot':
		player_damage = 100
		bu -= 1
		pa = random.choice(["I do not aim with my hand. I aim with my eye.",
						"I do not shoot with my hand. I shoot with my mind.",
						"I do not kill with my gun. I kill with my heart."])
	else:
		pa = 'You see? Size defeats us.'
		if size == 'large':
			player_damage=bu*9
		else:
			player_damage=bu*6
		bu=0

	return ph-damage, eh-player_damage, attack, bu, pa

def attack_dict(ph, eh, bu, end_room, combat_room2):
	return {'You Died':Death(), 'You Won':end_room(), 'aimshot':combat_room2(eh, ph, bu,'aimshot',cmbt=False),
							'reload':combat_room2(eh, ph, bu,'reload', cmbt=False),
							'rapidfire':combat_room2(eh, ph, bu,'rapidfire', cmbt=False)}

def load_room(name):
	#room names have the form 'name.player_health.enemy_health' if 
	#a combat room or just 'name' if a regular room
	def str2bool(string):
		if string == 'False':
			return False
		elif string == 'True':
			return True

	values = name.split('@')
	name = values[0]
	print(values)
	print(name)
	room_dict = {"TheTown1":TheTown1(), "TheTown2":TheTown2(), "Death":Death(), "TownsPeople1":TownsPeople1(),
					"TownsPeople2":TownsPeople2(), "TheTown3":TheTown3(), "TheGreatExpanse1":TheGreatExpanse1(),
					"TheGreatExpanse2":TheGreatExpanse2(), "TheManInBlack1":TheManInBlack1(),
					"TheManInBlack2":TheManInBlack2(), "TheGreatExpanse3":TheGreatExpanse3(),
					"TheGreatExpanseSkull":TheGreatExpanseSkull(), "TheGreatExpanseNoSkull":TheGreatExpanseNoSkull(),
					"TheBeach1":TheBeach1(), "TheBeach2":TheBeach2(), "TheBeach3":TheBeach3(), "TheBeach4":TheBeach4(),
					"Lobstrocities1":Lobstrocities1(), "Lobstrocities2":Lobstrocities2(), "Lobstrocities3":Lobstrocities3(),
					"JakeDoor1":JakeDoor1(), "JakeDoor2":JakeDoor2(), "TakeJake":TakeJake(), "DontTakeJake":DontTakeJake(),
					"Forest1":Forest1(), "Forest2":Forest2(), "Shardik1":Shardik1(), "Shardik2":Shardik2(),
					"ShardikDies":ShardikDies(), "VampDoor1":VampDoor1(), "VampDoor2":VampDoor2(), "VampDoorWin":VampDoorWin(),
					"VampDoorLose":VampDoorLose(), "MonoRail1":MonoRail1()}
	combat_rooms = {"TownsPeople1":TownsPeople1, "TownsPeople2":TownsPeople2, "TheManInBlack1":TheManInBlack1,
					"TheManInBlack2":TheManInBlack2, "Lobstrocities1":Lobstrocities1, "Lobstrocities2":Lobstrocities2,
					"Lobstrocities3":Lobstrocities3, "Shardik1":Shardik1, "Shardik2":Shardik2}
	test_room = room_dict.get(name)

	global skull
	global boy

	if test_room.rt == 'combat1':
		skull, boy = str2bool(values[4]), str2bool(values[5])
		return combat_rooms.get(name)(float(values[1]), float(values[2]), float(values[3]))
	elif test_room.rt == 'combat2':
		skull, boy = str2bool(values[5]), str2bool(values[6])
		return combat_rooms.get(name)(float(values[1]), float(values[2]), float(values[3]),
										values[4])
	else:
		skull, boy = str2bool(values[1]), str2bool(values[2])

	return room_dict.get(name)
#need to give everyroom parameters for skull and boy
#and make room_dict like combat_room, maybe delete globals


START = "VampDoor1@True@False"
