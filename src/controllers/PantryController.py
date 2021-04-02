from src.controllers.util import bcolors, command_input, pretty_print_pantry, print_ingredient_list_from_search
from src.models import Category, UserPantry, Ingredient, CookedBy, Recipe
from sqlalchemy import select


def pantry(app_session):
    command = ""
    print(bcolors.HEADER + "Update Your Pantry" + bcolors.ENDC)
    while command != "exit":
        command = command_input(bcolors.BOLD + "What do you want to do with your pantry?" + bcolors.ENDC,
                                ["add", "remove", "view", "exit"])
        if command == "add":
            add(app_session)
        if command == "remove":
            remove(app_session)
        if command == "view":
            view(app_session)


def get_users_pantry(app_session):
    user = app_session.user
    pantry = user.Pantry
    return pantry


def view(app_session):
    pretty_print_pantry(app_session.user.Pantry)


def add(app_session):
    pantry = get_users_pantry(app_session)

    print(bcolors.BOLD + bcolors.OKCYAN + "Add ingredient(s)" + bcolors.ENDC)

    command = ""
    newSearch = True
    ingredients = []
    while newSearch:
        ingredients = print_ingredient_list_from_search(
            input(bcolors.BOLD + "Search for an Ingredient: " + bcolors.ENDC), app_session)

        command = command_input(bcolors.BOLD + "Which ingredient would you like?" +
                                bcolors.ENDC, [str(idx) for idx, i in enumerate(ingredients)] +
                                ["New Search", "Exit"])
        newSearch = (command == "New Search")

    purchase_date = input("Purchase Date (MM/DD/YYYY): ")
    expiration_date = input("Expiration Date (MM/DD/YYYY): ")
    quantity_bought = input('Quantity Bought: ')

    new_ingredient = UserPantry(ingredient_id=ingredients[int(command)].id, expiration_date=expiration_date,
                                purchase_date=purchase_date, quantity_bought=float(quantity_bought), current_quantity=float(quantity_bought))
    app_session.user.Pantry.append(new_ingredient)
    app_session.session.commit()

    print(bcolors.OKGREEN + "Successfully Added!" + bcolors.ENDC)


def remove(app_session):
    pantry = get_users_pantry(app_session)
    print(pantry)

    print(
        bcolors.BOLD + "Please enter the number of the ingredient you want to remove. Type \"exit\" to close the Pantry Manager.")
    command = ""
    for idx, r in enumerate(pantry):
        print(bcolors.BOLD + str(idx) + bcolors.ENDC + '.' + " " + str(r.ingredient.name))
    command = command_input(
        bcolors.BOLD + "Select the ingredient you want to remove (or type exit to leave this menu)" + bcolors.ENDC,
        ["exit"])
    if command == "exit":
        return

    if command != "exit":
        pass


def reduce_quantity_of_item(app_session, ingredientObject, reduceByQuantity):
    user_pantry = app_session.user.Pantry

    for i in user_pantry:
        if i.ingredient_id == ingredientObject.id:
            if i.current_quantity > reduceByQuantity:
                i.current_quantity = i.current_quantity - reduceByQuantity
                app_session.session.commit()
                return True
    return False

# todo
# function for adding items to pantry
# function for removing items to pantry
