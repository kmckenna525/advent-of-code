from timeit import default_timer as timer
import re

start = timer()
file = open('input.txt')

possible_refs = {}
for line in file.readlines():
	split = line.strip().split(" (contains ")
	ingredients = set(split[0].split(" "))
	allergens = split[1].replace(")","").split(", ")

	for allergen in allergens:
		if allergen not in possible_refs:
			possible_refs[allergen] = ingredients
		else:
			possible_refs[allergen] = ingredients.intersection(possible_refs[allergen])
	
unknown = set(possible_refs.keys())

known_i_to_a = {}
while len(unknown) > 0:
	for (allergen, ingredients) in possible_refs.items():
		if allergen not in unknown:
			continue

		# prune newly known if present
		for ingredient in list(ingredients): # gotta copy for removable
			if ingredient in known_i_to_a:
				ingredients.remove(ingredient)
		if len(ingredients) == 1:
			ingredient = ingredients.pop()
			known_i_to_a[ingredient] = allergen
			unknown.remove(allergen)

result = ",".join(sorted(known_i_to_a.keys(), key=lambda ingredient: known_i_to_a[ingredient]))

print("Completed in %fms" % ((timer() - start) * 1000))
print("%s is the result" % result)