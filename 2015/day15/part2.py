from timeit import default_timer as timer
import re

teaspoons = 100
calories_target = 500

class Ingredient:
	def __init__(self, info):
		self.name = info["name"]
		stats = {}
		stats["capacity"] = int(info["capacity"])
		stats["durability"] = int(info["durability"])
		stats["flavor"] = int(info["flavor"])
		stats["texture"] = int(info["texture"])
		self.calories = int(info["calories"])
		self.stats = stats

	def __str__(self):
		return  "%s" % (self.name)

	def __repr__(self):
		return  "%s" % (self.name)

def score(amounts):
	totals = {}
	for (ingredient, amt) in amounts.items():
		if amt == 0:
			continue
		for (stat, val) in ingredient.stats.items():
			if stat not in totals:
				totals[stat] = 0
			totals[stat] += val * amt

	score = 1
	for (stat, val) in totals.items():
		if val < 0:
			return 0
		score *= val
	return score

def calories(amounts):
	total = 0
	for (ingredient, amt) in amounts.items():
		total += amt * ingredient.calories
	return total

def permute(items, n):
	if len(items) == 1:
		return [{items[0]:n}]

	permutations = []
	item = items[0]
	items.pop(0)
	for i in range(0, n + 1):
		for permutation in permute(items, n - i):
			new = { item: i }
			new.update(permutation)
			# tiny optimization - skip recipes that already surpassed our calorie limit
			if calories(new) > calories_target:
				continue
			permutations.append(new)
	items.insert(0, item)
	return permutations


start = timer()
file = open('input.txt')

pattern = r"(?P<name>\w+): capacity (?P<capacity>-?\d+), durability (?P<durability>-?\d+), flavor (?P<flavor>-?\d+), texture (?P<texture>-?\d+), calories (?P<calories>-?\d+)";
ingredients = []
for line in file.readlines():
	matches = re.match(pattern, line)
	data = matches.groupdict();
	ingredients.append(Ingredient(data))
	

best = 0
recipe = None
for permutation in permute(ingredients, teaspoons):
	if calories(permutation) != calories_target:
		continue
	total = score(permutation)
	# print (permutation, total)
	if total > best:
		best = total
		recipe = permutation

result = best

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)