import pickle

def display_recipe(recipe):
    print("\n")
    print("Recipe: ", recipe['name'])
    print("Cooking Time (min): " + str(recipe['cooking_time']))
    print("Ingredients: ")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print("Difficult level: " + recipe['difficulty'])

def search_ingredient(data):
    for position, value in enumerate(data['all_ingredients']):
        print("Item " + str(position) + ": " + value) 

    try:
        ingredient_index = input("Select number from list: ")
        ingredient_searched = data['all_ingredients'][int(ingredient_index)]
    except ValueError:
        print("Index doesn't exist - exiting.")
    except:
        print("An unexpected error occurred.")
    else:
        for recipe in data['recipes_list']:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)
        
file_name = input("What file are you storing in?")

try:
    with open(file_name, 'rb') as my_file:
        data = pickle.load(my_file)
except FileNotFoundError:
    print("File doesn't exist - exiting.")
except:
    print("An unexpected error occurred.")
else:
    search_ingredient(data)