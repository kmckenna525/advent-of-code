from timeit import default_timer as timer
import re
import math

start = timer()
file = open('input.txt')

WEAPON = 0
ARMOR = 1
RING = 2


class Item:
	def __init__(self, slot, cost, damage, armor):
		self.slot = slot
		self.cost = cost
		self.damage = damage
		self.armor = armor

	def __str__(self):
		return  "%d: %d" % (self.slot, self.cost)

	def __repr__(self):
		return  "%d: %d" % (self.slot, self.cost)


class Player:
	def __init__(self, hp, damage, armor):
		self.hp = hp
		self.damage = damage
		self.armor = armor

	def __str__(self):
		return  "%d" % (self.val)

	def __repr__(self):
		return str(self.val)

	def practical_damage(self, opponent):
		return max(self.damage - opponent.armor, 1)

	def would_win(self, opponent):
		if self.practical_damage(opponent) == 0:
			return False
		if opponent.practical_damage(self) == 0:
			return True

		myturns = math.ceil(opponent.hp / float(self.practical_damage(opponent)))
		theirturns = math.ceil(self.hp / float(opponent.practical_damage(self)))
		return myturns <= theirturns

def player_from_items(items):
	damage = 0
	armor = 0
	for item in items:
		if item == None:
			continue
		damage += item.damage
		armor += item.armor

	return Player(100, damage, armor)

def cost(items):
	total = 0
	for item in items:
		if item == None:
			continue
		total += item.cost
	return total


shop = [
	[
		Item(WEAPON, 8, 4, 0),
		Item(WEAPON, 10, 5, 0),
		Item(WEAPON, 25, 6, 0),
		Item(WEAPON, 40, 7, 0),
		Item(WEAPON, 74, 8, 0),
	],
	[
		None, 
		Item(ARMOR, 13, 0, 1),
		Item(ARMOR, 31, 0, 2),
		Item(ARMOR, 53, 0, 3),
		Item(ARMOR, 75, 0, 4),
		Item(ARMOR, 102, 0, 5),
	],
	[
		None, 
		Item(RING, 25, 1, 0),
		Item(RING, 50, 2, 0),
		Item(RING, 100, 3, 0),
		Item(RING, 20, 0, 1),
		Item(RING, 40, 0, 2),
		Item(RING, 80, 0, 3),
	]
]

# instead of input file, hardcoding
boss = Player(103, 9, 2)

result = 180 + 102 + 74 # all most expensive items
for weapon in shop[WEAPON]:
	for armor in shop[ARMOR]:
		for ring1 in shop[RING]:
			for ring2 in shop[RING]:
				if ring1 is not None and ring1 == ring2:
					continue
				items = [weapon, armor, ring1, ring2]
				player = player_from_items(items)
				if player.would_win(boss):
					itemscost = cost(items)
					if itemscost < result:
						result =  itemscost



print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)