class ShoppingList(object):
    # initializes the data attributes list_name and shopping_list
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []
    # procedural attributes/methods for adding or removing items from shopping_list list
    def add_item(self, item):
        # if statement to prevent doubling items
        if not item in self.shopping_list:
            self.shopping_list.append(item)
    def remove_item(self, item):
        self.shopping_list.remove(item)
    # method for printing shopping list
    def view_list(self):
        print(self.shopping_list)
# create object from ShoppingList class
pet_store_list = ShoppingList("Pet Store Shopping List")
# calling methods for adding and removing items from list
pet_store_list.add_item('dog food')
pet_store_list.add_item('frisbee')
pet_store_list.add_item('bowl')
pet_store_list.add_item('collars')
pet_store_list.add_item('flea collars')
pet_store_list.remove_item('flea collars')
pet_store_list.add_item('frisbee')
# calling method for printing shopping list
pet_store_list.view_list()

