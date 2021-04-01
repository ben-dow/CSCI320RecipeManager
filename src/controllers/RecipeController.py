import os

from src.controllers.util import bcolors, command_input, pretty_print_recipe, print_recipe_metadata


def RecipeController(app_session):
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


def update_recipe_info(infoName, recipe, app_session):
    if infoName == "Name":
        newName = input(bcolors.BOLD + "Enter the new name for the recipe: " + bcolors.ENDC)
        recipe.name = newName
        app_session.session.commit()
        print(bcolors.OKGREEN + "Change Successful" + bcolors.ENDC)
    elif infoName == "Description":
        description = input(bcolors.BOLD + "Enter the new description for the recipe: " + bcolors.ENDC)
        recipe.description = description
        app_session.session.commit()
        print(bcolors.OKGREEN + "Change Successful" + bcolors.ENDC)
    elif infoName == "CookTime":
        cookTime = input(bcolors.BOLD + "Enter the new description for the recipe: " + bcolors.ENDC)
        recipe.cook_time = int(cookTime)
        app_session.session.commit()
        print(bcolors.OKGREEN + "Change Successful" + bcolors.ENDC)
    elif infoName == "Servings":
        servings = input(bcolors.BOLD + "Enter the new description for the recipe: " + bcolors.ENDC)
        recipe.cook_time = int(servings)
        app_session.session.commit()
        print(bcolors.OKGREEN + "Change Successful" + bcolors.ENDC)
    elif infoName == "Difficulty":
        command = command_input("Enter the new Difficulty for the recipe: ", ['easy', 'easy_medium', 'medium', 'medium_hard', 'hard'])
        # recipe.difficulty = int(servings)
        # app_session.session.commit()
        print(bcolors.OKGREEN + "Change Successful" + bcolors.ENDC)
    if infoName in ["Name", "Description", "CookTime", "Servings", "Difficulty"]:
        print_recipe_metadata(recipe)


def create(app_session):
    pass


def edit(app_session):
    recipes = get_users_recipes(app_session)

    print(bcolors.BOLD + bcolors.UNDERLINE + "Edit a Recipe" + bcolors.ENDC)
    print("Please Enter the Number of the Recipe you Would Like to Edit. (Or Type \"exit\" to leave this menu")

    for idx, r in enumerate(recipes):
        print(bcolors.BOLD + str(idx) + bcolors.ENDC + '.' + " " + r.name)

    command = command_input(bcolors.BOLD + "Which Recipe?" + bcolors.ENDC,
                            list(str(x) for x in range(0, len(recipes))) + ["Exit"])

    if command == "Exit":
        return

    recipe = recipes[int(command)]
    pretty_print_recipe(recipe)

    options = {
        "Info": edit_info,
        "Steps": edit_steps,
        "Ingredients": edit_ingredients
    }
    command = ""
    while command != "Exit":
        command = command_input(bcolors.BOLD + "What would you like edit?" + bcolors.ENDC,
                                ["Info", "Steps", "Ingredients", "Exit"])
        if command != "Exit":
            options[command](app_session, recipe)


def edit_info(app_session, recipe):
    print_recipe_metadata(recipe)

    command = ""
    while command != "Exit":
        command = command_input(bcolors.BOLD + "Which Piece of Information Would You Like to Edit?" + bcolors.ENDC,
                                ["Name", "Description", "Difficulty", "Servings", "Cook Time", "Exit"])
        update_recipe_info(command, recipe, app_session)

    if command == "Exit":
        return


def edit_steps():
    pass


def edit_ingredients():
    pass


def delete(app_session):
    pass
