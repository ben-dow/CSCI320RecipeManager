import os

from src.controllers.RecipeEditor import get_users_recipes
from src.controllers.SearchController import search
from src.controllers.util import bcolors, command_input, pretty_print_recipe
from src.models import Category


def cook(app_session):
    # os.system('clear')    # clear console window
    command = ""
    print(bcolors.HEADER + "Recipe Cooking Station" + bcolors.ENDC)
    while command != "Exit":
        command = command_input(bcolors.BOLD + "What would you like to do?" + bcolors.ENDC,
                                ["Cook", "ViewCookedRecipes", "Exit"])

        if command == "Cook":
            make_recipe(app_session)

        if command == "ViewCookedRecipes":
            view(app_session)

    return


def make_recipe(app_session):
    recipe_list = get_users_recipes(app_session)  # TODO: Replace with search function

    print(bcolors.BOLD + bcolors.UNDERLINE + "Cook a Recipe" + bcolors.ENDC)
    print("Please Enter the Number of the Recipe you Would Like to Cook. (Or Type \"Exit\" to leave this menu)")

    for idx, r in enumerate(recipe_list):  # print out the available choices
        print(bcolors.BOLD + str(idx) + bcolors.ENDC + '.' + " " + r.name)

    command = command_input(bcolors.BOLD + "Which Recipe?" + bcolors.ENDC,
                            list(str(x) for x in range(0, len(recipe_list))) + ["Exit"])

    if command == "Exit":
        return

    recipe = recipe_list[int(command)]  # get the recipe itself

    print(bcolors.BOLD + "Cooking Recipe:" + bcolors.ENDC)
    pretty_print_recipe(recipe)  # show info about the recipe

    # TODO: Print ingredients needed and their current quantity

    # get the scale from user input
    while command != "Exit" and scale != float():
        print("Please Enter the Scale of the Recipe. (Or \"Exit\" to leave this menu)")
        command = input(bcolors.BOLD + "Scale?" + bcolors.ENDC)

        if command == "Exit":
            return

        try:
            scale = float(command)
        except ValueError:
            print(bcolors.FAIL + "INVALID SCALE. Must be an integer or decimal number.")



    # TODO: Add error handling?
    scale = float(command)


def view(app_session):
    pass
