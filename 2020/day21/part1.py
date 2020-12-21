from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

possible_refs = {}
all_ingredients = set()
all_ingredients_raw = []
for line in file.readlines():
	split = line.strip().split(" (contains ")
	ingredients = set(split[0].split(" "))
	allergens = split[1].replace(")","").split(", ")

	all_ingredients_raw.extend(ingredients)
	all_ingredients.update(ingredients)

	for allergen in allergens:
		if allergen not in possible_refs:
			possible_refs[allergen] = ingredients
		else:
			possible_refs[allergen] = ingredients.intersection(possible_refs[allergen])
	
all_possible = set()
for (allergen, ingredients) in possible_refs.items():
	all_possible.update(ingredients)

impossible = all_ingredients.difference(all_possible)

result = 0
for ingredient in all_ingredients_raw:
	if ingredient in impossible:
		result += 1

print("Completed in %fms" % ((timer() - start) * 1000))
print("%d is the result" % result)