import random
import time


class Room(object):
	def __init__(self, skull, boy):
		#dict of actions and the rooms they lead to
		self.next_rooms = {}
		self.rt = "base"
		self.true_name = None
		self.skull = skull
		self.boy = boy

	def go(self, action):
		#used to find the next room in the current room's
		#dictionary given an action
		next_room = self.next_rooms.get(action)
		if not next_room == None:
			return next_room(self.skull, self.boy)
		else:
			return None

	def name_room(self):
		#returns a string containing the room's relevant values
		#values are passed like this because flask's sessions
		#object only handles strings
		return self.true_name+'@'+str(self.skull)+'@'+str(self.boy)

	def room_type(self):
		#returns the type of room
		#types used in this module are 
		#yesno - takes a yes or a no as input
		#continue - only has a continue option
		#show_room - has an open player typed input
		#combat1 - the first stage in combat, where the player chooses their attack
		#combat2 - the second stage in combat, shows the result of player and enemy attacks
		return self.rt

class InstantDeathRoom(Room):
	'''used when an incorrect input should result in a path 
	to a separate room instead of a repeat of the same room, 
	like if the player needed to answer an instant death riddle'''
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.fail_room = Death

	def go(self, action):
		next_room = self.next_rooms.get(action)
		if not next_room == None:
			return next_room(self.skull, self.boy)
		else:
			return self.fail_room(self.skull, self.boy)

class CombatRoom1(Room):
	def __init__(self, skull, boy):
		self.health = 0
		self.true_name = 'combat'
		self.ph = 0
		self.bullets = 0
		self.next_rooms = {}
		self.pa = None
		self.skull = skull
		self.boy = boy

	def go(self, action):
		#try-except used to see if the next room is an exit or combat2 room
		try:
			next_room = self.next_rooms.get(action)
		except TypeError:
			next_room = self.next_rooms.get(action)(self.skull, self.boy)
		return next_room

	def name_room(self):
		#returns a string with relevant values for use in flask sessions
		return self.true_name+'@'+str(self.health)+'@'+str(self.ph)+'@'+str(self.bullets)+'@'+str(self.skull)+'@'+str(self.boy)


class CombatRoom2(CombatRoom1):
	def go(self, action):
		return self.next_rooms.get(action)(self.skull, self.boy, self.health, self.ph, self.bullets)

	def name_room(self):
		#returns a string with relevant values for use in flask sessions
		return self.true_name+'@'+str(self.health)+'@'+str(self.ph)+'@'+str(self.bullets)+'@'+self.pa+'@'+str(self.skull)+'@'+str(self.boy)

'''the map of the rooms is as follows:
TheTown1 -> TownsPeople -> ManInBlack ->TheGreatExpanse ->TheBeach -> Lobstrocities
															V  				  |
 Thewaystation < TheMonorail < TheBeach < Vampdoor<-TheBeach <-JakesDoor <----|
		V			Death < TheForest<---------------|   ^--------------------|
TheFieldofRoses > TheCrimsonKing > TheDarkTower > TheTown1
You need to get the skull to beat the vampire in the second door
You need the boy to beat the CrimsonKing
If you choose to go into the forest you die whether you beat the bear or not'''

class TheTown1(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': TheTown2}
		self.name = 'Tull'
		self.rt = 'continue'
		self.true_name = 'TheTown1'
		self.description = """You are Roland of Gilead, the last in a long line of Gunslingers - 
knights with a mythic affinity for weapons of death. 
Your aim is the Dark Tower. 
Supported by 19 beams, each of which is protected by a guardian, 
the Dark Tower holds together the very Fabric of reality.
The world you inhabit has been crumbling as the sinister forces of the Crimson King work to destroy the Tower. 
Now, you search for the Man in Black, an ancient evil, and a servant to the Crimson King.
\nYou hope he knows the way."""

class TheTown2(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': TownsPeople1}
		self.name = 'Tull'
		self.rt = 'continue'
		self.true_name = 'TheTown2'
		self.description = """You've just arrived at the small town of Tull.
Unfortunately, the kindly townspeople have been warped by the man in black. 
The once peace loving citizens are now hungry for your blood, and they come at you in droves.
You have no choice but to fight."""


class TownsPeople1(CombatRoom1):
	def __init__(self, skull, boy, health=100, player_health=100, bullets=6):
		super().__init__(skull, boy)
		self.health = health
		self.bullets = bullets
		self.ph = player_health
		self.name = 'The Mob'
		#yesno instead of combat
		self.rt = 'combat1'
		self.true_name = 'TownsPeople1'	
		self.next_rooms = attack_dict(skull, boy, self.ph, self.health, self.bullets, TheTown3, TownsPeople2)
		self.ending = "The man in black travels with your soul in his pocket."
		self.playerwin = "You fire your shot, and the last townsperson keels over."

class TownsPeople2(CombatRoom2):
	def __init__(self, skull, boy, health=100, ph=100, bullets=6, pa=None, cmbt=True):
		super().__init__(skull, boy)
		self.health = health
		self.bullets = bullets
		self.rt = 'combat2'
		self.name = 'The Mob'
		self.true_name = 'TownsPeople2'
		self.attacks = ["""The towns people call for your death.
They throw debris from all sides.
Rocks, cans and gardening tools rain down.""","""The towns people surge forward!
They scream for your head as they thrust pitchforks and broomsticks."""]
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
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
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
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': TheGreatExpanse2}
		self.name = 'The Great Expanse'
		self.rt = 'continue'
		self.true_name = 'TheGreatExpanse1'
		self.description = """You've been walking for weeks.
The desert heat drys your mouth, but you do not die. 
The Tower wont allow it. 
Upon a dune you see a small fire tended to by a cloaked figure.
As you approach, the Man in Black looks up."""

class TheGreatExpanse2(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': TheManInBlack1}
		self.name = 'The Great Expanse'
		self.rt = 'continue'
		self.true_name = 'TheGreatExpanse2'
		self.description = """You sit by the fire.
The Man in Black pulls out a deck of tarot cards.
From this deck he draws three:
The magician, The Devil, and The Bear.
\'The bear is protection, Gunslinger.
The devil will stop at nothing to stop you.
And the magician is the key to Tower\'
The Man in black stands.
\'Yet these are just paper. 
Your travels end with me\'"""

class TheManInBlack1(CombatRoom1):
	def __init__(self, skull, boy, health=100, player_health=100, bullets=6):
		super().__init__(skull, boy)
		self.health = health
		self.bullets = bullets
		self.ph = player_health
		self.name = 'The Man In Black'
		self.rt = 'combat1'
		self.true_name = 'TheManInBlack1'	
		self.next_rooms = attack_dict(skull, boy, self.ph, self.health, self.bullets, TheGreatExpanse3, TheManInBlack2)
		self.ending = "The man in black travels with your soul in his pocket"
		self.playerwin = "Your vision blurs as you fall to your knees."

class TheManInBlack2(CombatRoom2):
	def __init__(self, skull, boy, health=100, ph=100, bullets=6, pa=None, cmbt=True):
		super().__init__(skull, boy)
		self.health = health
		self.bullets = bullets
		self.rt = 'combat2'
		self.name = 'The Man In Black'
		self.true_name = 'TheManInBlack2'
		if self.ph < 30:
			self.attacks = ["""The man in black laughs as a murder of crows descends.
The birds, black as night, peck and tear at any exposed area.""",
							"""The man in black sends a crossbow bolt straight towards your eye!
You reach to your face, but there's nothing there..."""]
			self.damages = [20, 29]
			self.chance_to_hit = [100, 50]
		else:
			self.attacks = ["""The man in black chants strange words.\n
Your vision clouds as you collapse to the ground.\n
The last thing you hear is laughter."""]
			self.damages = [30]
			self.chances_to_hit = [100]
		self.size = 'small'
		self.pa = pa
		if cmbt:
			self.ph, self.health, self.ea, self.bullets, self.pa = combat(pa, self.attacks, self.damages, self.chance_to_hit,
							self.size, ph, health, bullets, self.name)
		else:
			self.ph, self.ea, self.health, self.bullets = ph, None, health, bullets
		self.next_rooms = {'continue':TheManInBlack1}

class TheGreatExpanse3(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'yes': TheGreatExpanseSkull, 'no':TheGreatExpanseNoSkull,
							'y':TheGreatExpanseSkull, 'n':TheGreatExpanseNoSkull}
		self.name = 'The Great Expanse'
		self.rt = 'yesno'
		self.true_name = 'TheGreatExpanse3'
		self.description = """When you awake,
your hair is longer and your skin is blistered.
You don't know how long you've been out.
Beside you is a bag, occupied only by a human skull.
The skull is covered in ruins, and a voice whispers when your hand nears it.
Do you keep it?"""

class TheGreatExpanseSkull(Room):
	def __init__(self, skull, boy):
		skull = True
		super().__init__(skull, boy)
		self.next_rooms = {'continue': TheBeach1}
		self.name = 'The Great Expanse'
		self.rt = 'continue'
		self.true_name = 'TheGreatExpanseSkull'
		self.description = """You pick up the skull and tie it to your waist.
Far in the distance you can see the Tower.
Hundreds of miles away, it's obscured by atmospheric haze.
This is the closest you've ever been"""

class TheGreatExpanseNoSkull(Room):
	def __init__(self, skull, boy):
		skull = False
		super().__init__(skull, boy)
		self.next_rooms = {'continue': TheBeach1}
		self.name = 'The Great Expanse'
		self.rt = 'continue'
		self.true_name = 'TheGreatExpanseSkull'
		self.description = """You leave the cursed thing.
Far in the distance you can see the Tower.
Hundreds of miles away, it's obscured by atmospheric haze.
This is the closest you've ever been"""

class TheBeach1(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'wait':TheBeach2, 'open':JakeDoor1,
							'open the door':JakeDoor1,
							'open door':JakeDoor1,
							'wait for the morning':TheBeach2,
							'wait for morning':TheBeach2}
		self.name = 'The Beach'
		self.rt = 'show_room'
		self.true_name = 'TheBeach1'
		self.description = """The sands seem endless, yet suddenly 
a vast ocean appears before you.
You continue along the beach, towards the Tower.
The waves crash ominously. The dark waters
obscure the horrors that lie beneath.
Time moves slowly, but eventually, you find something.
A door.
Do you wait for morning, or open the door?"""

class TheBeach2(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':TheBeach21}
		self.name = 'The Beach'
		self.rt = 'continue'
		self.true_name = 'TheBeach2'
		self.description = """You decide to wait for the morning. 
After laying down your few belongings, you drift off into sleep.
You wake up suddenly. 
Strange clicking sounds seem to come from the waves. 
You ready your revolver."""			

class TheBeach21(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':Lobstrocities1}
		self.name = 'The Beach'
		self.rt = 'continue'
		self.true_name = 'TheBeach21'
		self.description = """Horrifying monstrosities emerge from the deep.
Reminiscent of gigantic, upright lobsters, the horrors seem to be asking questions.
Dad-uh-chuck? Did-uh-chim? Dud-a-chum? 
It's a chorus of nonsense. 
The monsters slowly advance, pincers waving in the air."""	

class Lobstrocities1(CombatRoom1):
	def __init__(self, skull, boy, health=250, player_health=100, bullets=6):
		super().__init__(skull, boy)
		self.health = health
		self.bullets = bullets
		self.ph = player_health
		self.name = 'Lobstrocities'
		self.rt = 'combat1'
		self.true_name = 'Lobstrocities1'	
		self.next_rooms = attack_dict(skull, boy, self.ph, self.health, self.bullets, Lobstrocities3, Lobstrocities2)
		self.ending = """The Lobstrocities overwhelm you. 
Their wicked pincers rend your flesh. 
They soon scuttle back into the ocean, leaving only a pile of bones in their wake."""
		self.playerwin = "Giant lobster corpses litter the ground. The circle breaks."
class Lobstrocities2(CombatRoom2):
	def __init__(self, skull, boy, health=250, ph=100, bullets=6, pa=None, cmbt=True):
		super().__init__(skull, boy)
		self.health = health
		self.bullets = bullets
		self.rt = 'combat2'
		self.name = 'Lobstrocities'
		self.true_name = 'Lobstrocities2'
		self.attacks = ["""The horrors advance, wary of your handcannon, but hungry for your flesh. 
A lobstrocity attacks from behind, snipping at your leg.""",
"""The monstosities encircle you. 
The only way to escape is to put them down. 
A creature shoots it's claw forward, snapping at your free hand.""",
"""The lobsters chuckle and their circle tightens.
They seem to be communicating."""]
		self.damages = [15+int((250-self.health)/10), 15+int((250-self.health)/10), 0]
		self.chance_to_hit = [80, 70, 100]
		self.size = 'large'
		self.pa = pa
		if cmbt:
			self.ph, self.health, self.ea, self.bullets, self.pa = combat(pa, self.attacks, self.damages, self.chance_to_hit,
							self.size, ph, health, bullets, self.name)
		else:
			self.ph, self.ea, self.health, self.bullets = ph, None, health, bullets
		self.next_rooms = {'continue':Lobstrocities1}

class Lobstrocities3(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'yes':JakeDoor1, 'no':TheBeach3}
		self.name = 'The Beach'
		self.rt = 'yesno'
		self.true_name = 'Lobstrocities3'
		self.description = """You've beaten them back. 
The remaining stragglers scurry into the waves. 
Their strange questions float on the surface of the water until the last lobstrocity disappears.
The door remains, and it's almost morning. 
Will you open it?"""

class JakeDoor1(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':JakeDoor2}
		self.name = 'The Door'
		self.rt = 'continue'
		self.true_name = 'JakeDoor1'
		self.description = """The door stands menacingly in the sand.
The red paint looks fresh, and nothing lies behind.
You open the door, it leads to a large room in a victorian mansion. 
Technologies unknown to you decorate the walls, and balls of pure light hang from the ceiling.
In the center of the room sits a boy of about fourteen, drawing with pencils.
Pieces of art, stunning in their realism, are scattered across the floor. 
You ask him where his parents are."""

class JakeDoor2(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'yes':TakeJake, 'no':DontTakeJake}
		self.name = 'The Door'
		self.rt = 'yesno'
		self.true_name = 'JakeDoor2'
		self.description = """\'They've been gone for days\' he says. 
You ask him what his name is.
\'Jake\' he says. 
The name stirs something inside you, and you feel as though you're about to remember something important.
Do you take the boy with you?"""

class TakeJake(Room):
	def __init__(self, skull, boy):
		boy1 = True
		super().__init__(skull, boy1)
		self.next_rooms = {'continue':TheBeach3}
		self.name = 'The Door'
		self.rt = 'continue'
		self.true_name = 'TakeJake'
		self.description = """You ask if the boy wants to come with you. 
Afterall, some doors have deeper meanings. 
He nods in affirmation as he picks up his pencils. 
You take him through the door, and arrive back at the beach."""

class DontTakeJake(Room):
	def __init__(self, skull, boy):
		boy1 = False
		super().__init__(skull, boy1)
		self.next_rooms = {'continue':TheBeach3}
		self.name = 'The Door'
		self.rt = 'continue'
		self.true_name = 'DontTakeJake'
		self.description = """You tell the boy to leave the house, and find his parents.
This place is too big for a lone child. 
You turn on your heel and quickly leave out through the door to arrive back at the beach"""

class TheBeach3(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':TheBeach4}
		self.name = 'The Beach'
		self.rt = 'continue'
		self.true_name = 'TheBeach3'
		self.description = """You turn around to look back at the door. 
You find it has been replaced by the same long expanse. 
All that's left is a small indentation in the sand. 
You continue along the beach, until, in the distance, you see a tree."""

class TheBeach4(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'forest':Forest1, 'door':VampDoor1,
							'into the forest':Forest1,
							'go into the forest':Forest1,
							'through the door':VampDoor1,
							'go through the door':VampDoor1}
		self.name = 'The Beach'
		self.rt = 'show_room'
		self.true_name = 'TheBeach4'
		self.description = """A few hours later, you're standing on the edge of a forest. 
Thick vines hang from garguantuan branches that completely obscure the sun. 
Yet, before you, stands another door.
This door is far more forebodeing. 
Jet black paint peels off of a sunbleached wooden frame. 
The knob appears to have been rusted from the marine air.
Do you go through the door, or into the forest?"""

class Forest1(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':Forest2}
		self.name = 'The Forest'
		self.rt = 'continue'
		self.true_name = 'Forest1'
		self.description = """The forest consumes you. 
Light peaks through open spots in the trees, and unnatural noises spring from the shadows.
As you walk, the earth begins to shake in rhythm.
You hear ageless trunks being snapped, each emitting sounds akin to small explosions."""

class Forest2(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':Shardik1}
		self.name = 'The Forest'
		self.rt = 'continue'
		self.true_name = 'Forest2'
		self.description = """You stay quiet, but feel the sounds grow louder and louder.
Suddenly, a gargantuan bear emerges from the trees, a line of destruction left in its path. 
The bear unleashes an earthshattering roar as it approaches"""

class Shardik1(CombatRoom1):
	def __init__(self, skull, boy, health=300, player_health=100, bullets=6):
		super().__init__(skull, boy)
		self.health = health
		self.bullets = bullets
		self.ph = player_health
		self.name = 'Shardik'
		self.rt = 'combat1'
		self.true_name = 'Shardik1'	
		self.next_rooms = attack_dict(skull, boy, self.ph, self.health, self.bullets, ShardikDies, Shardik2)
		self.ending = """Shardik's rage consumes him, as he consumes you."""	
		self.playerwin = """Your final shot pierces the injured bear's top jaw from below."""
class Shardik2(CombatRoom2):
	def __init__(self, skull, boy, health=300, ph=100, bullets=6, pa=None, cmbt=True):
		super().__init__(skull, boy)
		self.health = health
		self.bullets = bullets
		self.rt = 'combat2'
		self.name = 'Shardik'
		self.true_name = 'Shardik2'
		self.attacks = ["""The great bear swings, but you dive just in time.
The bear becoms enraged.""",
						"""The great bean swings, but you're too slow!
The great bear crunches 
you under its paw.""", """The bear slams it's body on the ground, but you jumped out of the way. 
Just in time.""",
"""The bear smashes to the earth, and catches you in its shockwave."""]
		self.damages = [0, 15+int((300-health)/10), 0, 20+int((300-health)/15)]
		self.chance_to_hit = [0, 100, 0, 100]
		self.size = 'large'
		self.pa = pa
		if cmbt:
			self.ph, self.health, self.ea, self.bullets, self.pa = combat(pa, self.attacks, self.damages, self.chance_to_hit,
							self.size, ph, health, bullets, self.name)
		else:
			self.ph, self.ea, self.health, self.bullets = ph, None, health, bullets
		self.next_rooms = {'continue':Shardik1}

class ShardikDies(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':Death}
		self.name = 'The Forest'
		self.rt = 'continue'
		self.true_name = 'ShardikDies'
		self.description = """The great bear falls to the ground dead, a metal gadget sits atop its head.
A thunderous crack breaks the silence. 
Shards from the sky fall to the ground as the world shakes. 
You realize, too late, that you have just destroyed a guardian of the Tower.
With the bear's death, the Tower crumbles. 
As reality breaks, you fall to your knees, defeated."""

class VampDoor1(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':VampDoor2}
		self.name = 'The Dixie Pig'
		self.rt = 'continue'
		self.true_name = 'VampDoor1'
		self.description = """You open the door with a creak. 
Warm light flows from torches and the scent of fresh cooked meat permeates the air. 
A group of ancient warriors sits around a table. 
All are drinking and laughing.
You walk through, and the door slams shut behind you. 
No longer is the hall filled with invitation, but instead a deep sense of dread. 
The torches have been replaced with moonbeams, and the smell of rot fills your nose. 
A single figure remains at the head of the table. 
He rises."""

class VampDoor2(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		print(self.skull)
		if self.skull:
			self.next_rooms = {'continue':VampDoorWin}
		else:
			self.next_rooms = {'continue':VampDoorLose}
		self.name = 'The Dixie Pig'
		self.rt = 'continue'
		self.true_name = 'VampDoor2'
		self.description = """\'Your will is strong Gunslinger, but your faith is weak.
The Tower will crumble, and we will rebuild in its place.\'
The figure rushes forward. The moonlight glints off his too-large teeth. 
His claws reach for your throat as you reach for your gun."""

class VampDoorWin(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':MonoRail1}
		self.name = 'The Dixie Pig'
		self.rt = 'continue'
		self.true_name = 'VampDoorWin'
		self.description = """The Man in Black's skull vibrates with energy.
As the monster collides with you, the skull explodes with light.
The creature shrinks back, and howls in pain. 
As it cowers, you run back towards the door."""

class VampDoorLose(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':Death}
		self.name = 'The Dixie Pig'
		self.rt = 'continue'
		self.true_name = 'VampDoorLose'
		if boy:
			self.description = """The creature is too fast. 
He slaps the gun from your hand and bares down into your throat.
You look towards Jake and wish that you had never brought him into this. 
He looks on in horror, and as the monster finishes you off, he moves onto the boy."""
		else:
			self.description = """The creature is too fast, he slaps the gun from your hand and bares
down into your throat."""

class MonoRail1(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':MonoRail2}
		self.name = 'The Metropolis'
		self.rt = 'continue'
		self.true_name = 'MonoRail1'
		self.description = """You burst through, but neither forest nor beach remain to greet you.
All that remains are the ruins of a great city.
Ripped newspapers and trash litter the ground.
In the distance you hear a faint hum, like that of a powerline. 
You hike towards the sound.
After hours of wandering through the winding streets, you arrive at what appears to be a futuristic train.
Shaped like a silver bullet, the train car hovers over a magnetic rail. 
As you approach, it comes to life."""

class MonoRail2(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': BlaineRiddle1}
		self.name = 'The Metropolis'
		self.rt = 'continue'
		self.true_name = 'MonoRail2'
		self.description = """\'Blaine the Train here!\' an oddly cheery voice hums.
\'Next stop, Can'-Ka No Rey!\'
A name in the old tongue, meaning 'field of roses'.
A powerful name, one which is intertwined with the Dark Tower in legend. 
As the doors open, you step aboard. 
After you take your seat, the train explodes from the station."""

class BlaineRiddle1(InstantDeathRoom):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.fail_room = BlaineEnding
		self.next_rooms = {'silence': BlaineRiddle2, 'quiet':BlaineRiddle2}
		self.name = 'Blaine the Train'
		self.rt = 'show_room'
		self.true_name = 'BlaineRiddle1'
		self.description = """The cheery voice fills the cabin. \'Hi! I'm Blaine the train, and I looove riddles!\'.
The train accelerates suddenly, pushing you back into your seat. 
You can barely lift your arm. 
\'Let's play a game! Answer all three of my riddles, and we'll stop at the waystation! 
Otherwise, well, I guess this'll be my last one-way trip!\'
\'Here's one! NO SOONER SPOKEN THAN BROKEN, WHAT IS IT\'
The car picks up speed."""

class BlaineRiddle2(InstantDeathRoom):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.fail_room = BlaineEnding
		self.next_rooms = {'bullet': BlaineRiddle3, 'a bullet':BlaineRiddle3}
		self.name = 'The Monorail'
		self.rt = 'show_room'
		self.true_name = 'BlaineRiddle2'
		self.description = """The train slows down, it was getting hard to breathe.
\'Wow! Good job! Here's another one! 
IN A TUNNEL OF DARKNESS LAYS A BEAST OF IRON. 
IT CAN ONLY ATTACK WHEN PULLED BACK. 
WHAT IS IT?\'"""

class BlaineRiddle3(InstantDeathRoom):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.fail_room = BlaineEnding
		self.next_rooms = {'a jar': MonoRail3, 'ajar':MonoRail3, 
							'when its ajar':MonoRail3, 'when its a jar':MonoRail3}
		self.name ='The Monorail'
		self.rt = 'show_room'
		self.true_name = 'BlaineRiddle3'
		self.description = """The train slows further! 
As you gain control of your arms, you reach for your gun, but an electric current courses
through your body. 
\'Now's not the time for that Gunslinger!
Now's the time for riddles! WHEN IS A DOOR NOT A DOOR?\'"""

class BlaineEnding(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue':Death}
		self.name = 'The Monorail'
		self.rt = 'continue'
		self.true_name = 'BlaineEnding'
		self.description = """The train jerks forwards! 
You can't hold on any longer. 
Your world goes black."""

class MonoRail3(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': Waystation1}
		self.name = 'The Monorail'
		self.rt = 'continue'
		self.true_name = 'MonoRail3'
		self.description = """The train slows to a crawl. As you reach a platform,
Blaine blares through the speakers once more.
\'Wow! You really are good, Gunslinger! 
My friend Eddie taught me that last one, almost had me stumped.\'
The doors slide open, and you step out. 
Around you is an old wooden waystation. 
To the North, the horizon is covered in red, and the Tower looms."""

class Waystation1(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': Waystation2}
		self.name = 'The Waystation'
		self.rt = 'continue'
		self.true_name = 'Waystation1'
		if boy:
			self.description = """You walk for days, the boy by your side. 
He's constantly scribbling in his notebook. 
Beaches, monsters and a rose that holds the universe in its petals. 
They seem to jump out of the page.
The Tower looms in the distance, but it never seems to get any closer."""
		else:
			self.description = """You walk for days.
The Tower looms in the distance, but it never seems to get any closer."""

class Waystation2(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': FieldOfRoses1}
		self.name = 'The Waystation'
		self.rt = 'continue'
		self.true_name = 'Waystation2'
		self.description = """Weeks crawl by. 
As you approach Can'-Ka No Rey, a deep sadness fills your body. 
And as you reach the edge of the field, it becomes almost unbearable."""

class FieldOfRoses1(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': FieldOfRoses2}
		self.name = 'Can-Ka No Rey'
		self.rt = 'continue'
		self.true_name = 'FieldOfRoses1'
		self.description = """Can'-Ka No Rey is there before you. Millions of roses
surround the Tower and dominate your eyesight. 
Their smell lifts your spirits. 
The Tower is so close. 
Its black spire pierces through the sky.
You approach the tower. 
Once you reach the top, it'll all be over."""

class FieldOfRoses2(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		if boy:
			self.next_rooms = {'continue': FieldOfRoses3}
			self.description = ' '
		else:
			self.next_rooms = {'continue': CrimsonKing1}
			self.description = ' '
		self.name = 'Can-Ka No Rey'
		self.rt = 'continue'
		self.true_name = 'FieldOfRoses2'
		self.description = """A shriek pierces the air. 
\'HAIL, GUNSLINGER\'
You look up. 
On a balcony jutting from the edifice sits a hunched figure, cloaked in red. 
He laughs, and chills move up your spine."""

class CrimsonKing1(CombatRoom1):
	def __init__(self, skull, boy, health=100, player_health=100, bullets=6):
		super().__init__(skull, boy)
		self.health = health
		self.bullets = bullets
		self.ph = player_health
		self.name = 'The Crimson King'
		self.rt = 'combat1'
		self.true_name = 'CrimsonKing1'	
		self.next_rooms = attack_dict(skull, boy, self.ph, self.health, self.bullets, Death, CrimsonKing2)
		self.ending = """You die gasping for air as the spiders fill your body.
With your last bit of strength you look towards the tower.
Everything goes black.	"""	


class CrimsonKing2(CombatRoom2):
	def __init__(self, skull, boy, health=100, ph=100, bullets=6, pa=None, cmbt=True):
		super().__init__(skull, boy)
		self.health = health
		self.bullets = bullets
		self.rt = 'combat2'
		self.name = 'The Crimson King'
		self.true_name = 'CrimsonKing2'
		if boy:
			self.attacks = ["""Spiders as big as your fist rise from the grass, heir black abdomens swollen with venom. 
Thousands swarm you and the boy.
There is no escape. """]
		else:
			self.attacks = ["""Spiders as big as your fist rise from the grass, heir black abdomens swollen with venom. 
Thousands swarm your body.\n 
There is no escape. """]
		self.damages = [100]
		self.chance_to_hit = [100]
		self.size = 'small'
		self.pa = pa
		if cmbt:
			self.ph, self.health, self.ea, self.bullets, self.pa = combat(pa, self.attacks, self.damages, self.chance_to_hit,
							self.size, ph, health, bullets, self.name)
		else:
			self.ph, self.ea, self.health, self.bullets = ph, None, health, bullets
		self.next_rooms = {'continue':CrimsonKing1}

class FieldOfRoses3(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': FieldOfRoses4}
		self.name = 'Can-Ka No Rey'
		self.rt = 'continue'
		self.true_name = 'FieldOfRoses3'
		self.description = """You turn towards the boy. 
He draws vigorously and the figure on the ledge comes to life on his page. 
His eyes look into you, and you look into the void.
The boy erases his drawing. 
You turn back to the balcony."""

class FieldOfRoses4(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': TheTower1}
		self.name = 'Can-Ka No Rey'
		self.rt = 'continue'
		self.true_name = 'FieldOfRoses4'
		self.description = """There's noone there."""

class TheTower1(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': TheTower2}
		self.name = 'The Tower'
		self.rt = 'continue'
		self.true_name = 'TheTower1'
		self.description = """With the Crimson King gone, you approach the Dark Tower.
You must reach the top, therein lies your salvation.
The winding steps number into the thousands.
They take you past rooms filled with memories. 
Dead lovec ones beckon you. 
You carry on."""

class TheTower2(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': TheTower3}
		self.name = 'The Tower'
		self.rt = 'continue'
		self.true_name = 'TheTower2'
		self.description = """The people you've killed haunt you through the open doorways. 
Still, you climb.
You see your Father, your Mother, your Best Friend.
Their eyes fill with tears as you approach.
Yet you continue."""

class TheTower3(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': TheTower4}
		self.name = 'The Tower'
		self.rt = 'continue'
		self.true_name = 'TheTower3'
		self.description = """You climb for years while the Tower sustains you.
Finally, you reach the last room.
Your hand shakes. You open it."""

class TheTower4(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': Final}
		self.name = 'The Tower'
		self.rt = 'continue'
		self.true_name = 'TheTower4'
		self.description = """Light fills the tower! 
You see through your stories.
The countless lives you've lived flash before your eyes.
Always, you search for the tower. 
Sometimes you reach it, other times not. 
But eventually, you always end up back here."""

class Final(Room):
	def __init__(self, skull, boy):
		super().__init__(skull, boy)
		self.next_rooms = {'continue': TheTown2}
		self.name = 'The Desert'
		self.rt = 'continue'
		self.true_name = 'Final'
		self.description = """You wake up in the desert.
The Tower dominates your mind.
You get up and walk."""

class Death(Room):
	def __init__(self,skull, boy):
		skull = False
		boy = False
		super().__init__(skull, boy)
		self.name = 'you died'
		self.rt = 'end'
		self.true_name = 'Death'
		self.description = """You made it this far, but the tower is farther.
And as you died, the world moved on"""


def combat(pa, attacks, dmgs, chances, size, ph, eh, bu, enemy_name):
	#find enemy attack
	attack_idx = int(random.randint(0, len(attacks)-1))
	chance = chances[attack_idx]
	roll = int(random.randint(1,100))
	if roll > chance:
		damage = 0
		attack = f"{enemy_name} misses!"
	else:
		damage = dmgs[attack_idx]
		attack = attacks[attack_idx]

	#find damage to enemy and resulting amount of bullets
	player_damage= 0
	if pa == 'reload':
		bu = 6
		pa = 'That nimble reloading trick.'
	elif bu <=0:
		pa = 'Your chambers are empty gunslinger.'
		bu = 0
		player_damage=0
	elif pa == 'aimshot':
		player_damage = 19+int(random.randint(0,7))
		bu -= 1
		pa = random.choice(["I do not aim with my hand. I aim with my eye.",
						"I do not shoot with my hand. I shoot with my mind.",
						"I do not kill with my gun. I kill with my heart."])
	else:
		pa = 'You see? Size defeats us.'
		if size == 'large':
			#rapidfire does more damage if the enemy is large
			player_damage=bu*9
		else:
			player_damage=bu*6
		bu=0

	#return new values based on chosen player attack
	#and enemy attack
	return ph-damage, eh-player_damage, attack, bu, pa

def attack_dict(sk, by, ph, eh, bu, end_room, combat_room2):
	#used to find the parameters for the combat2 rooms
	#used in the Combat1Class
	return {'you died':Death(sk, by), 'you won':end_room(sk, by), 
							'aimshot':combat_room2(sk, by, eh, ph, bu,'aimshot',cmbt=False),
							'reload':combat_room2(sk, by, eh, ph, bu,'reload', cmbt=False),
							'rapidfire':combat_room2(sk, by, eh, ph, bu,'rapidfire', cmbt=False)}

def load_room(name):
	#room names have the form 'name.player_health.enemy_health' if 
	#a combat room or just 'name' if a regular room
	def str2bool(string):
		if string == 'False':
			return False
		elif string == 'True':
			return True

	#takes relevant values from the string holding them
	values = name.split('@')
	name = values[0]
	
	#dictionary of all the rooms, used to create an instance with the values taken from the input name
	room_dict = {"TheTown1":TheTown1, "TheTown2":TheTown2, "Death":Death, "TownsPeople1":TownsPeople1,
					"TownsPeople2":TownsPeople2, "TheTown3":TheTown3, "TheGreatExpanse1":TheGreatExpanse1,
					"TheGreatExpanse2":TheGreatExpanse2, "TheManInBlack1":TheManInBlack1,
					"TheManInBlack2":TheManInBlack2, "TheGreatExpanse3":TheGreatExpanse3,
					"TheGreatExpanseSkull":TheGreatExpanseSkull, "TheGreatExpanseNoSkull":TheGreatExpanseNoSkull,
					"TheBeach1":TheBeach1, "TheBeach2":TheBeach2, "TheBeach3":TheBeach3, "TheBeach4":TheBeach4,
					"Lobstrocities1":Lobstrocities1, "Lobstrocities2":Lobstrocities2, "Lobstrocities3":Lobstrocities3,
					"JakeDoor1":JakeDoor1, "JakeDoor2":JakeDoor2, "TakeJake":TakeJake, "DontTakeJake":DontTakeJake,
					"Forest1":Forest1, "Forest2":Forest2, "Shardik1":Shardik1, "Shardik2":Shardik2,
					"ShardikDies":ShardikDies, "VampDoor1":VampDoor1, "VampDoor2":VampDoor2, "VampDoorWin":VampDoorWin,
					"VampDoorLose":VampDoorLose, "MonoRail1":MonoRail1, "MonoRail2":MonoRail2, "BlaineRiddle1":BlaineRiddle1,
					"BlaineRiddle2":BlaineRiddle2, "BlaineRiddle3":BlaineRiddle3, 'BlaineEnding':BlaineEnding, 
					"MonoRail3": MonoRail3, "Waystation1":Waystation1, "Waystation2": Waystation2, 
					"FieldOfRoses1":FieldOfRoses1, "FieldOfRoses2":FieldOfRoses2, "FieldOfRoses3":FieldOfRoses3,
					"FieldOfRoses4":FieldOfRoses4, "CrimsonKing1":CrimsonKing1,
					"CrimsonKing2":CrimsonKing2, "TheTower1":TheTower1, "TheTower2":TheTower2, "TheTower3":TheTower3, 
					"TheTower4":TheTower4, "Final":Final, "TheBeach21":TheBeach21}

	#parameters are placeholders used to tell what kind of room it is
	test_room = room_dict.get(name)(False, False)

	if test_room.rt == 'combat1':
		skull, boy = str2bool(values[4]), str2bool(values[5])
		return room_dict.get(name)(skull, boy, float(values[1]), float(values[2]), float(values[3]))
	elif test_room.rt == 'combat2':
		
		skull, boy = str2bool(values[5]), str2bool(values[6])
		return room_dict.get(name)(skull, boy, float(values[1]), float(values[2]), float(values[3]),
										values[4])
	else:
		skull, boy = str2bool(values[1]), str2bool(values[2])

	return room_dict.get(name)(skull, boy)
#need to give everyroom parameters for skull and boy
#and make room_dict like combat_room, maybe delete globals

#global variables (booleans) are stored as strings because that's
#all that flask sessions can handle
START = "TheTown1@False@False"


