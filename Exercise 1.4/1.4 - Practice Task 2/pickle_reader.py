import pickle

recipe = { 'name': 'Tea', 'cooking_time':5, 'ingredients': ['tea leaves','water','sugar'],'difficulty':'Easy'}

my_file = open("recipe_binary.bin", "wb")

pickle.dump(recipe, my_file)

my_file.close()

with open('recipe_binary.bin','rb') as my_file:
    recipe = pickle.load(my_file)

print("Recipe details -")
print("Name: " + recipe["name"])
print("Ingredients: ", end="")
print(*([x.capitalize() for x in recipe["ingredients"]]), sep=', ')
print("Cooking Time: " + str(recipe["cooking_time"]) + " minutes")
print("Difficulty: " + recipe["difficulty"])
