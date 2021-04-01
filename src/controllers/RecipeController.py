import os

from src.controllers.util import bcolors, command_input, pretty_print_recipe


def RecipeEditor(app_session):
    command = ""
    print(bcolors.HEADER + "Recipe Editor" + bcolors.ENDC)
    while command != "Exit":
        command = command_input(bcolors.BOLD + "What would you like todo?" + bcolors.ENDC,
                                ["Create", "Edit", "Delete", "Exit"])

        if command == "Edit":
            edit(app_session)

    print(bcolors.OKBLUE + "Exiting Recipe Editor" + bcolors.ENDC)


def get_users_recipes(app_session):
    user = app_session.user
    return user.Recipes


def create(app_session):
    pass


def edit(app_session):
    recipes = get_users_recipes(app_session)

    print(bcolors.BOLD + bcolors.UNDERLINE + "Edit a Recipe" + bcolors.ENDC)
    print("Please Enter the Number of the Recipe you Would Like to Edit. (Or Type \"exit\" to leave this menu")

    for idx, r in enumerate(recipes):
        print(bcolors.BOLD + str(idx) + bcolors.ENDC + '.' + " " + r.name)

    command = command_input(bcolors.BOLD + "Which Recipe?" + bcolors.ENDC,
                            list(str(x) for x in range(0, len(recipes))) + ["exit"])

    if command == "exit":
        return

    pretty_print_recipe(recipes[int(command)])

    command = ""
    while command != "Exit":
        command = command_input(bcolors.BOLD + "What would you like edit?" + bcolors.ENDC,
                                ["Info", "Steps", "Ingredients"])




def delete(app_session):
    pass
