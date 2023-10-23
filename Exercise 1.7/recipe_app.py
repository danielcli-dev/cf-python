from sqlalchemy import create_engine

engine = create_engine("mysql://cf-python:password@localhost/task_database")
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

Base = declarative_base()
from sqlalchemy import Column
from sqlalchemy.types import Integer, String

# Recipe class created
class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return (
            "<Recipe ID: "
            + str(self.id)
            + "-"
            + self.name
            + "-"
            + self.difficulty
            + ">"
        )

    def __str__(self):
        output = (
            "\nID: "
            + str(self.id)
            + "\nName: "
            + self.name
            + "\nIngredients: "
            + self.ingredients
            + "\nCooking Time (min): "
            + str(self.cooking_time)
            + "\nDifficulty: "
            + self.difficulty
        )
        return output

    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        elif self.ingredients:
            return self.ingredients.split(sep=", ")

    # Function for calculating difficulty based on cooking time and # of ingredients
    def calc_difficulty(self):
        if int(self.cooking_time) < 10 and len(self.return_ingredients_as_list()) < 4:
            self.difficulty = "Easy"
        elif (
            int(self.cooking_time) < 10 and len(self.return_ingredients_as_list()) >= 4
        ):
            self.difficulty = "Medium"
        elif (
            int(self.cooking_time) >= 10 and len(self.return_ingredients_as_list()) < 4
        ):
            self.difficulty = "Intermediate"
        elif (
            int(self.cooking_time) >= 10 and len(self.return_ingredients_as_list()) >= 4
        ):
            self.difficulty = "Hard"


#  Function for adding multiple ingredients to recipe
def add_ingredients():
    ingredients = []

    num_ingredients = int(input("How many ingredients would you like to enter? "))
    for _ in range(0, num_ingredients):
        ingredient_added = input("Add ingredient (Enter nothing when done): ")
        ingredient_added = ingredient_added.capitalize()
        if ingredient_added != "":
            ingredients.append(ingredient_added[:])
        elif ingredient_added == "":
            print("You entered an empty input. Function failed")
            break
    return ingredients


#  Function for displaying recipes
def print_recipes(recipes):
    for row in recipes:
        print("\n")
        print("ID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking Time: ", row[3])
        print("Difficulty:", row[4])


def main_menu():
    option_choice = 0

    # Function for creating a new recipe and inserting it into a database
    def create_recipe():
        name = input("Name of recipe? ")
        cooking_time = input("What is the cooking time? ")
        ingredients = add_ingredients()

        # Converting ingredients from a list to a string
        ingredients = ", ".join(ingredients)
        if len(name) <= 50 and cooking_time.isnumeric():
            recipe_entry = Recipe(
                name=name, cooking_time=cooking_time, ingredients=ingredients
            )
            recipe_entry.calc_difficulty()
            session.add(recipe_entry)
            session.commit()
        else:
            print("The name and cooking time are incorrectly formatted")

    def view_all_recipes():
        all_recipes = session.query(Recipe).all()
        if not all_recipes:
            print("No entries found")
            return None
        elif all_recipes:
            for i in all_recipes:
                print(i)

    # Function for searching all recipes that contain a specific ingredient
    def search_by_ingredients():
        # List for consolidating all unique ingredients from every recipe
        all_ingredients = []

        if session.query(Recipe).count() == 0:
            print("No entries found")
            return None
        results = session.query(Recipe.ingredients).all()
        for ingredient_tuple in results:
            ingredient_list = list(ingredient_tuple)
            for ingredient_string in ingredient_list:
                ingredient_separated = ingredient_string.split(", ")
                for ingredient in ingredient_separated:
                    if ingredient not in all_ingredients:
                        all_ingredients.append(ingredient)

        # Iterating through list and printing values with their position in list
        for position, value in enumerate(all_ingredients):
            print("Item " + str(position) + ": " + value)

        try:
            # Allows user to select ingredient using their position
            search_index = input(
                "Select Item # from list (Separate multiple items by one space): "
            )
        except ValueError:
            print("Index doesn't exist - exiting.")
        except:
            print("An unexpected error occurred.")
        else:
            # Query for retreiving recipes which contain selected ingredient in their ingredients column
            search_indexes = search_index.split(" ")
            search_ingredients = []
            for index in search_indexes:
                search_ingredient = all_ingredients[int(index)]
                if search_ingredient not in search_ingredients:
                    search_ingredients.append(search_ingredient)
            conditions = []
            for search_ingredient in search_ingredients:
                like_term = "%" + search_ingredient + "%"
                conditions.append(Recipe.ingredients.like(like_term))
            filtered_recipes = session.query(Recipe).filter(*conditions).all()
            print("=" * 15 + "\nRecipes Found \n" + "=" * 15)

            for i in filtered_recipes:
                print(i)

    # Function for updating an existing recipe
    def edit_recipe():
        # Query for all recipes and prints them
        if session.query(Recipe).count() != 0:
            results = session.query(Recipe.id, Recipe.name).all()
            for i in results:
                print("ID: " + str(i[0]) + " " * 3 + "Recipe: " + i[1])
        else:
            print("No entries found")
            return None
        try:
            # Allow users to select the recipe by ID and select what column to update
            update_index = int(input("\nSelect ID from list: "))
            recipe_to_edit = (
                session.query(Recipe).filter(Recipe.id == update_index).one()
            )
            print("1. Name: ", recipe_to_edit.name)
            print("2. Cooking Time: ", recipe_to_edit.cooking_time)
            print("3. Ingredients: ", recipe_to_edit.ingredients)
            column_index = input("\nSelect which attribute you want to update? \n")

        # Error catching by type of error
        except ValueError:
            print("Index doesn't exist - exiting.")
        except:
            print("An unexpected error occurred.")
        else:
            # Updates the selected recipe with new value for name, cooking time, or ingredients
            if column_index == "1":
                new_value = input("Enter new value: ")
                recipe_to_edit.name = new_value

            elif column_index == "2":
                new_value = input("Enter new value: ")
                recipe_to_edit.cooking_time = new_value
            elif column_index == "3":
                print("Replacing old ingredients list...")
                # Uses add_ingredients function to collect new ingredients and assigns to variable ingredients
                ingredients = add_ingredients()
                new_value = ", ".join(ingredients)
                recipe_to_edit.ingredients = new_value

            # If user updates cooking time or ingredients, difficulty is re-calculated
            if column_index == "2" or column_index == "3":
                recipe_to_edit.calc_difficulty()
            session.commit()
            print(recipe_to_edit)

    # Function for deleting an existing recipe
    def delete_recipe():
        # Query for all recipes and prints them
        if session.query(Recipe).count() != 0:
            results = session.query(Recipe.id, Recipe.name).all()
            for i in results:
                print("ID: " + str(i[0]) + " " * 3 + "Recipe: " + i[1])
        else:
            return None
        try:
            # Allows user to select recipe to delete based on ID
            update_index = input("Select ID from list: ")
            recipe_to_delete = (
                session.query(Recipe).filter(Recipe.id == update_index).one()
            )
            confirm_delete = input("Are you sure you want to delete? (y/n): ")
        except ValueError:
            print("Index doesn't exist - exiting.")
        except:
            print("An unexpected error occurred.")
        else:
            if confirm_delete == "y":
                session.delete(recipe_to_delete)
                session.commit()

    # While loop allows main menu function to loop infinitely until user is done
    while option_choice != "quit":
        option_choice = input(
            "\nMain Menu\n =====================\n Select an option: \n 1. Create a new recipe\n 2. View all recipes\n 3. Search for a recipe by ingredients\n 4. Edit an existing recipe\n 5. Delete a recipe\n Type 'quit' to exit the program.\n Your choice: "
        )
        # Calls different functions based on user input
        if option_choice == "1":
            # adding recipes
            create_recipe()
        elif option_choice == "2":
            # view recipes
            view_all_recipes()
        elif option_choice == "3":
            # searching for recipes
            search_by_ingredients()
        elif option_choice == "4":
            # modifying recipes
            edit_recipe()
        elif option_choice == "5":
            # deleting recipes
            delete_recipe()
        elif option_choice == "quit":
            print("Thank you for using this app!")
        else:
            print("Unacceptable input. Please try again")
    session.close()
    engine.dispose()
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
main_menu()
