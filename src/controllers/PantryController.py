from src.controllers.util import bcolors, command_input, pretty_print_pantry, print_ingredient_list_from_search
from src.models import Category, UserPantry, Ingredient, CookedBy, Recipe
from sqlalchemy import select


def pantry(app_session):
    command = ""
    print(bcolors.HEADER + "Update Your Pantry" + bcolors.ENDC)
    while command != "Exit":
        command = command_input(bcolors.BOLD + "What do you want to do with your pantry?" + bcolors.ENDC,
                                ["add", "remove", "reduce", "view", "Exit"])
        if command == "add":
            add(app_session)
        if command == "remove":
            remove(app_session)
        if command == "reduce":
            reduce(app_session)
        if command == "view":
            view(app_session)


def get_users_pantry(app_session):
    user = app_session.user
    pantry = user.Pantry
    return pantry


def get_reduction():
    reduction = float()
    while reduction == float():
        print("How much do you want to reduce?")
        command = input(bcolors.BOLD + "Reduction: " + bcolors.ENDC)

        if command == "Exit":  # exit
            return float()

        try:  # check for valid input
            reduction = float(command)
            if reduction < 0:
                reduction = float()     # must be greater than zero
        except ValueError:
            print(bcolors.FAIL + "INVALID AMOUNT. Must be an integer or decimal number." + bcolors.ENDC)

    return reduction


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


def reduce(app_session):
    pantry = get_users_pantry(app_session)
    print(pantry)

    print(
        bcolors.BOLD + "Please enter the number of the ingredient you want to reduce. "
                       "Type \"Exit\" to close the Pantry Manager.")
    command = ""
    for idx, r in enumerate(pantry):
        print(bcolors.BOLD + str(idx) + bcolors.ENDC + '.' + " " + str(r.ingredient.name))
    while command != "Exit":
        command = command_input(
            bcolors.BOLD + "Select the ingredient you want to reduce. Type \"Exit\" to leave this menu."
            + bcolors.ENDC, list(str(x) for x in range(0, len(pantry))) + ["Exit"])
        if command != "Exit":
            p = pantry[int(command)]
            print(bcolors.BOLD + "Current quantity of " + str(p.ingredient.name) + ": " + bcolors.ENDC
                  + str(p.current_quantity))
            reduction = get_reduction()
            if reduction == float():                        # exit to pantry menu
                return
            if reduce_quantity_of_item(app_session, p.ingredient_id, reduction):
                print(bcolors.BOLD + "New quantity of " + str(p.ingredient.name) + ": " + bcolors.ENDC
                      + str(p.current_quantity))
            else:
                print(bcolors.FAIL + "Reduction failed." + bcolors.ENDC)
    return


def remove(app_session):
    pantry = get_users_pantry(app_session)
    print(pantry)

    print(
        bcolors.BOLD + "Please enter the number of the ingredient you want to remove. "
                       "Type \"exit\" to close the Pantry Manager.")
    command = ""
    for idx, r in enumerate(pantry):
        print(bcolors.BOLD + str(idx) + bcolors.ENDC + '.' + " " + str(r.ingredient.name))
    command = command_input(
        bcolors.BOLD + "Select the ingredient you want to remove (or type exit to leave this menu)" + bcolors.ENDC,
        ["exit"])
    if command == "exit":
        return

    if command != "exit":
        app_session.session.delete(pantry[int(command)])
        app_session.session.commit()
        print(bcolors.OKCYAN + "Successfully Deleted" + bcolors.ENDC)


def reduce_quantity_of_item(app_session, ingredient_id, reduceByQuantity):
    user_pantry = app_session.user.Pantry
    scraps = []  # to aggregate multiple ingredient objects together and decrease from them all
    scraps_aggregate = 0

    for i in user_pantry:
        if i.ingredient_id == ingredient_id:          # if correct ingredient, update scraps list and quantity
            scraps.append(i)
            scraps_aggregate += i.current_quantity
            if scraps_aggregate >= reduceByQuantity:        # if total quantity > amount, begin reducing it
                for scrap in scraps:                        # todo: all but the last scrap is guaranteed to be deleted.
                    if scrap.current_quantity > reduceByQuantity:                       # if some left over, remove it
                        scrap.current_quantity = i.current_quantity - reduceByQuantity
                    else:                                   # if none left over, then it's zero.
                        scraps_aggregate -= scrap.current_quantity
                        scrap.current_quantity = 0
                        #app_session.session.delete(scrap)
                app_session.session.commit()
                return True

    return False


# todo
# function for adding items to pantry
# function for removing items to pantry

# TODO: add func to clear out pantry (empty, expired)