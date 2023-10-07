import pickle

recipes_list, all_ingredients = [], []

def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return 'Easy'
    elif cooking_time< 10 and len(ingredients) >= 4:
        return 'Medium'
    elif cooking_time >= 10 and len(ingredients) < 4:
        return 'Intermediate'
    elif cooking_time >= 10 and len(ingredients) >= 4:
        return 'Hard'
    
def take_recipe():
    name = input("Name of recipe? ")
    name = name.capitalize()
    cooking_time = int(input("What is the cooking time? "))
    ingredients = []

    for i in range(0,21):
        c = input("Add ingredient? (Enter nothing when done)")
        c = c.capitalize()
        if c != "":
            ingredients.append(c[:])
        elif c == "":
            break
        if i == 20:
            print("Too many ingredients")
    difficulty = calc_difficulty(cooking_time, ingredients)

    return {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients, 'difficulty': difficulty}    




file_name = input("What file are you storing in?")

try:
    with open(file_name, 'rb') as my_file:
        data = pickle.load(my_file)
        print(data)
except FileNotFoundError:
    print("File doesn't exist - exiting.")
    data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}
except:
    print("An unexpected error occurred.")
    data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}
else:
    my_file.close()

finally:
    recipes_list, all_ingredients = data['recipes_list'], data['all_ingredients']
    # print("\n")
    # print("Recipe: ", recipe['name'])
    # print("Cooking Time (min): " + str(recipe['cooking_time']))
    # print("Ingredients: ")
    # for ingredient in recipe['ingredients']:
    #     print(ingredient)
    # print("Difficult level: " + recipe['difficulty'])


n = int(input("How many recipes would you like to enter? "))

for i in range(0, n):
    recipe = take_recipe()

    for ingredient in recipe['ingredients']:
        if not ingredient in all_ingredients:
            all_ingredients.append(ingredient)

    recipes_list.append(recipe)

data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

my_file = open(file_name, 'wb')
pickle.dump(data, my_file)
my_file.close()

# ingredients_list.sort()
# print("\n")
# print("Ingredients Available Across All Recipes")
# print("----------------------------------------")
# for ingredient in ingredients_list:
#     print(ingredient)