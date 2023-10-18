import mysql.connector

# Connecting to database and setting up a cursor to perform mySQL queries
conn = mysql.connector.connect(host="localhost", user="cf-python", passwd="password")
cursor = conn.cursor()

# Creating database and table to store data
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS Recipes (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), ingredients VARCHAR(255), cooking_time INT, difficulty VARCHAR(20))"
)

# Function for calculating difficulty based on cooking time and # of ingredients
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        return "Hard"

#  Function for adding multiple ingredients to recipe
def add_ingredients():
    ingredients = []
    for i in range(0, 21):
        ingredient_added = input("Add ingredient (Enter nothing when done): ")
        ingredient_added = ingredient_added.capitalize()
        if ingredient_added != "":
            ingredients.append(ingredient_added[:])
        elif ingredient_added == "":
            break
        elif i == 20:
            print("Too many ingredients")
    return ingredients

# Function for printing recipes
def print_recipes(recipes):
    for row in recipes:
        print("\n")
        print("ID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking Time: ", row[3])
        print("Difficulty:", row[4])

# Main function for selecting different options for recipes
def main_menu(conn, cursor):
    option_choice = 0

    # Function for creating a new recipe and inserting it into a database
    def create_recipe(conn, cursor):
        name = input("Name of recipe? ")
        cooking_time = int(input("What is the cooking time? "))
        ingredients = add_ingredients()
        difficulty = calc_difficulty(cooking_time, ingredients)

        # Converting ingredients from a list to a string
        ingredients = ", ".join(ingredients)
        cursor.execute(
            "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)",
            (name, ingredients, cooking_time, difficulty),
        )
        conn.commit()
    # Function for searching all recipes that contain a specific ingredient
    def search_recipe(conn, cursor):
        # List for consolidating all unique ingredients from every recipe
        all_ingredients = []
        cursor.execute("SELECT ingredients FROM Recipes")
        results = cursor.fetchall()
        for recipe_ingredients in results:
            # Converting list of tuples back into lists to loop through and add to all_ingredients list
            items = list(recipe_ingredients)
            items = items[0].split(", ")
            for item in items:
                if item not in all_ingredients:
                    all_ingredients.append(item)
            print("\n")

        # Iterating through list and printing values with their position in list
        for position, value in enumerate(all_ingredients):
            print("Item " + str(position) + ": " + value)

        try:
            # Allows user to select ingredient using their position
            search_index = input("Select Item # from list: ")
            search_ingredient = all_ingredients[int(search_index)]
        except ValueError:
            print("Index doesn't exist - exiting.")
        except:
            print("An unexpected error occurred.")
        else:
            # Query for retreiving recipes which contain selected ingredient in their ingredients column
            query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
            search_ingredient_value = ["%" + search_ingredient + "%"]
            cursor.execute(query, search_ingredient_value)
            results = cursor.fetchall()
            print_recipes(results)

    # Function for updating an existing recipe
    def update_recipe(conn, cursor):
        # Query for all recipes and prints them
        cursor.execute("SELECT * FROM Recipes")
        results = cursor.fetchall()
        print_recipes(results)

        try:
            # Allow users to select the recipe by ID and select what column to update
            update_index = int(input("Select ID from list: "))
            column_index = input(
                "What do you want to update? \n 1. Name \n 2. Cooking Time \n 3. Ingredients\n Choose a column: "
            )

        # Error catching by type of error
        except ValueError:
            print("Index doesn't exist - exiting.")
        except:
            print("An unexpected error occurred.")
        else:
            # Updates the selected recipe with new value for name, cooking time, or ingredients
            if column_index == "1":
                new_value = input("Enter new value: ")
                query = "UPDATE Recipes SET name = %s WHERE id = %s"
                update_value = (new_value, update_index)
            elif column_index == "2":
                new_value = input("Enter new value: ")
                query = "UPDATE Recipes SET cooking_time = %s WHERE id = %s"
                update_value = (new_value, update_index)

            elif column_index == "3":
                print("Replacing old ingredients list...")
                # Uses add_ingredients function to collect new ingredients and assigns to variable ingredients
                ingredients = add_ingredients()
                new_value = ", ".join(ingredients)
                query = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
                update_value = (new_value, update_index)

            cursor.execute(query, update_value)

        # Query for the cooking time and ingredients for selected recipe
        cursor.execute(
            "SELECT cooking_time, ingredients FROM Recipes WHERE id = %s",
            (update_index,),
        )
        results = cursor.fetchall()
        # Converting list of types into a integer and list
        cooking_time = results[0][0]
        ingredients = results[0][1]
        ingredients = list(ingredients.split(","))

        # If user updates cooking time or ingredients, difficulty is re-calculated
        if column_index == "2" or column_index == "3":
            query = "UPDATE Recipes SET difficulty = %s WHERE ID = %s"
            update_value = (calc_difficulty(cooking_time, ingredients), update_index)
            cursor.execute(query, update_value)
        conn.commit()

    # Function for deleting an existing recipe
    def delete_recipe(conn, cursor):
        cursor.execute("SELECT * FROM Recipes")
        results = cursor.fetchall()
        print_recipes(results)

        try:
            # Allows user to select recipe to delete based on ID
            update_index = input("Select ID from list: ")
        except ValueError:
            print("Index doesn't exist - exiting.")
        except:
            print("An unexpected error occurred.")
        else:
            query = "DELETE FROM Recipes WHERE id = %s"
            update_value = (update_index,)
            cursor.execute(query, update_value)
        conn.commit()

    # While loop allows main menu function to loop infinitely until user is done
    while option_choice != "quit":
        option_choice = input(
            "\nMain Menu\n =====================\n Select an option: \n 1. Create a new recipe\n 2. Search for a recipe by ingredient\n 3. Update an existing recipe\n 4. Delete a recipe\n Type 'quit' to exit the program.\n Your choice: "
        )
        # Calls different functions based on user input
        if option_choice == "1":
            # adding recipes
            create_recipe(conn, cursor)
        elif option_choice == "2":
            # searching for recipes
            search_recipe(conn, cursor)
        elif option_choice == "3":
            # modifying recipes
            update_recipe(conn, cursor)
        elif option_choice == "4":
            # deleting recipes
            delete_recipe(conn, cursor)

    # Connection is closed when user is done with main menu
    conn.close()

# Initial call for main menu function
main_menu(conn, cursor)
