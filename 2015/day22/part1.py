from timeit import default_timer as timer
import re
import math
from queue import PriorityQueue

start = timer()
file = open('input.txt')

class Spell:
	def __init__(self, cost):
		self.cost = cost

	def __str__(self):
		return  "%s(%d)" % (self.__class__.__name__, self.cost)

	def __repr__(self):
		return  "%s(%d)" % (self.__class__.__name__, self.cost)

	def cast(self, gamestate):
		# no op, override this
		return

	def apply(self, gamestate):
		# no op, override this
		return

	def isvalid(self, gamestate):
		return gamestate.playermana >= self.cost


class MagicMissile(Spell):
	def cast(self, gamestate):
		gamestate.bosshealth -= 4


class Drain(Spell):
	def cast(self, gamestate):
		gamestate.bosshealth -= 2
		gamestate.playerhealth += 2


class Shield(Spell):
	def cast(self, gamestate):
		gamestate.shieldtime = 6
		gamestate.playerarmor = 7

	def isvalid(self, gamestate):
		return Spell.isvalid(self, gamestate) and gamestate.shieldtime <= 0

	def apply(self, gamestate):
		if gamestate.shieldtime > 0:
			gamestate.shieldtime -= 1
			if gamestate.shieldtime == 0:
				self.expire(gamestate)

	def expire(self, gamestate):
		gamestate.playerarmor = 0


class Poison(Spell):
	def cast(self, gamestate):
		gamestate.poisontime = 6

	def isvalid(self, gamestate):
		return Spell.isvalid(self, gamestate) and gamestate.poisontime <= 0

	def apply(self, gamestate):
		if gamestate.poisontime > 0:
			gamestate.bosshealth -= 3
			gamestate.poisontime -= 1


class Recharge(Spell):
	def cast(self, gamestate):
		gamestate.rechargetime = 5

	def isvalid(self, gamestate):
		return Spell.isvalid(self, gamestate) and gamestate.rechargetime <= 0

	def apply(self, gamestate):
		if gamestate.rechargetime > 0:
			gamestate.playermana += 101
			gamestate.rechargetime -= 1


class Player:
	def __init__(self, hp, damage, armor, mana = 0):
		self.hp = hp
		self.damage = damage
		self.armor = armor
		self.mana = mana

	def __str__(self):
		return  str((self.hp, self.damage, self.armor, self.mana))

	def __repr__(self):
		return  str((self.hp, self.damage, self.armor, self.mana))

	def practical_damage(self, armor):
		return max(self.damage - armor, 1)


# data class for each state node
class GameState:
	def __init__(self, playerhealth, playermana, playerarmor, bosshealth, shieldtime = 0, poisontime = 0, rechargetime = 0):
		self.playerhealth = playerhealth
		self.playermana = playermana
		self.playerarmor = playerarmor
		self.bosshealth = bosshealth
		self.shieldtime = shieldtime
		self.poisontime = poisontime
		self.rechargetime = rechargetime
		self.playerwin = False
		self.bosswin = False

	@property
	def astuple(self):
		return (
			self.playerhealth, 
			self.playermana, 
			self.playerarmor, 
			self.bosshealth, 
			self.shieldtime, 
			self.poisontime, 
			self.rechargetime)
	

	def __str__(self):
		return  str(self.astuple)

	def __repr__(self):
		return  str(self.astuple)

	def __hash__(self):
		 return hash(self.astuple)

	def __eq__(self, other):
		return self.astuple == other.astuple

	def copy(self):
		return GameState(
			self.playerhealth,
			self.playermana,
			self.playerarmor,
			self.bosshealth,
			self.shieldtime, 
			self.poisontime,
			self.rechargetime)


def valid_spells(spells, gamestate):
	for spell in spells:
		if spell.isvalid(gamestate):
			yield spell


def playround(gamestate, opponent, spells, spellchoice):
	# PLAYER TURN
	# cast chosen spell
	gamestate.playermana -= spellchoice.cost
	spellchoice.cast(gamestate)

	# player win?
	if gamestate.bosshealth <= 0:
		gamestate.playerwin = True
		return

	# BOSS TURN
	# apply effects
	for spell in spells:
		spell.apply(gamestate)

	# player win?
	if gamestate.bosshealth <= 0:
		gamestate.playerwin = True
		return

	# boss attack
	gamestate.playerhealth -= opponent.practical_damage(gamestate.playerarmor)

	# boss win?
	if gamestate.playerhealth <= 0:
		gamestate.bosswin = True

	# NEXT PLAYER TURN (stop at spell choice)
	# apply effects
	for spell in spells:
		spell.apply(gamestate)


spells = [
	MagicMissile(53),
	Drain(73),
	Shield(113),
	Poison(173),
	Recharge(229)
]

# instead of input file, hardcoding
boss = Player(51, 9, 0)
player = Player(50, 0, 0, 500)
gamestate = GameState(player.hp, player.mana, player.armor, boss.hp)

seen = {} # gamestate: (distance, spells)
unseen = PriorityQueue() # (distance, spells used thus far, state)
unseen.put((0, [], gamestate)) 
while not unseen.empty():
	dist, spell_list, gamestate = unseen.get()
	if len(spell_list) > 0:
		# update gamestate if not the first one and check if done with branch or everything
		playround(gamestate, boss, spells, spell_list[-1])
		if gamestate.playerwin:
			result = dist
			break
		if gamestate.bosswin:
			continue

	if gamestate in seen and seen[gamestate][0] <= dist:
		# gamestate has already existed at a lower or equal cost
		continue

	seen[gamestate] = (dist, spell_list)

	for spell in valid_spells(spells, gamestate):
		nextlist = list(spell_list)
		nextlist.append(spell)
		unseen.put((dist + spell.cost, nextlist, gamestate.copy()))


print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)