recipes_list, ingredients_list = [], []

def take_recipe():
    name = input("Name of recipe? ")
    name = name.capitalize()
    cooking_time = int(input("What is the cooking time? "))
    # a=1
    ingredients = []

    # while a != 0:
    for i in range(0,21):
        c = input("Add ingredient? (Enter nothing when done)")
        c = c.capitalize()
        if c != "":
            ingredients.append(c[:])
        elif c == "":
            break
        if i == 20:
            print("Too many ingredients")
    return {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    

n = int(input("How many recipes would you like to enter? "))

for i in range(0, n):
    recipe = take_recipe()

    for ingredient in recipe['ingredients']:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)


for recipe in recipes_list:
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Intermediate'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Hard'
    print("\n")
    print("Recipe: ", recipe['name'])
    print("Cooking Time (min): " + str(recipe['cooking_time']))
    print("Ingredients: ")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print("Difficult level: " + recipe['difficulty'])

ingredients_list.sort()
print("\n")
print("Ingredients Available Across All Recipes")
print("----------------------------------------")
for ingredient in ingredients_list:
    print(ingredient)