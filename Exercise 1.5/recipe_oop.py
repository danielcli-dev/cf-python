class Recipe(object):
    all_ingredients = []
    recipes_list = []

    def __init__(self, name, ingredients=[], cooking_time=0):
        self.name = name
        self.ingredients = []
        self.cooking_time = cooking_time

        if cooking_time < 10 and len(ingredients) < 4:
            self.difficulty = 'Easy'
        elif cooking_time< 10 and len(ingredients) >= 4:
            self.difficulty = 'Medium'
        elif cooking_time >= 10 and len(ingredients) < 4:
            self.difficulty = 'Intermediate'
        elif cooking_time >= 10 and len(ingredients) >= 4:
            self.difficulty = 'Hard'

    def __str__(self):
        # print("\n")
        # print("Recipe: ", self.name)
        # print("Cooking Time (min): " + str(self.cooking_time))
        # print("Ingredients: ")
        # for ingredient in self.ingredients:
        #     print(ingredient)
        # print("Difficulty level: " + self.difficulty)

        mystring = "\n".join(map(str,self.ingredients))
        output = "\nRecipe: " + str(self.name) + \
        "\nCooking Time (min): " + str(self.cooking_time) + \
        "\nIngredients:\n" + str(mystring) + \
        "\nDifficulty level: " + str(self.difficulty)

        return output
    def set_name(self, name):
        self.name = name

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    def get_name(self):
        return self.name

    def get_cooking_time(self):
        output = str(self.cooking_time)
        return output

    def get_ingredients(self):
        return self.ingredients

    def get_difficulty(self):
        if not self.difficulty:
            self.calculate_difficulty()

    def add_ingredients(self, *items):
        for item in items:
            self.ingredients.append(item)
        self.update_all_ingredients()

    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return True
        else:
            return False

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)

    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "Hard"

    def recipe_search(data, search_term):
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe)


tea = Recipe(
    "Tea",
)
tea.add_ingredients("Tea leaves", "Sugar", "Water")
tea.set_cooking_time(5)
tea.calculate_difficulty()
Recipe.recipes_list.append(tea)
print(tea)

coffee = Recipe(
    "Coffee",
)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
coffee.calculate_difficulty()
Recipe.recipes_list.append(coffee)
print(coffee)

cake = Recipe(
    "Cake",
)
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)
cake.calculate_difficulty()
Recipe.recipes_list.append(cake)
print(cake)

banana_smoothie = Recipe(
    "Banana Smoothie",
)
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)
banana_smoothie.calculate_difficulty()
Recipe.recipes_list.append(banana_smoothie)
print(banana_smoothie)

print("\nRecipe Search for Water")
Recipe.recipe_search(Recipe.recipes_list, "Water")
print("\nRecipe Search for Sugar")
Recipe.recipe_search(Recipe.recipes_list, "Sugar")
print("\nRecipe Search for Bananas")
Recipe.recipe_search(Recipe.recipes_list, "Bananas")