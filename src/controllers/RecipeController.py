import os

from src.controllers.util import bcolors, command_input, pretty_print_recipe, print_recipe_metadata, print_recipe_steps, \
    print_recipe_ingredients
from src.models import DifficultyEnum, Step, RecipeIngredients, Ingredient, Recipe


def RecipeController(app_session):
    command = ""
    print(bcolors.HEADER + "Recipe Editor" + bcolors.ENDC)
    while command != "Exit":
        command = command_input(bcolors.BOLD + "What would you like todo?" + bcolors.ENDC,
                                ["Create", "Edit", "Delete", "Exit"])

        if command == "Edit":
            edit(app_session)

        if command == "Create":
            create(app_session)
        if command == "Delete":
            delete(app_session)

    print(bcolors.OKBLUE + "Exiting Recipe Editor" + bcolors.ENDC)


def get_users_recipes(app_session):
    user = app_session.user
    return user.Recipes


def update_recipe_info(infoName, recipe, app_session):
    if infoName == "Name":
        newName = input(bcolors.BOLD + "Enter the new name for the recipe: " + bcolors.ENDC)
        recipe.name = newName
        print(bcolors.OKGREEN + "Change Successful" + bcolors.ENDC)
    elif infoName == "Description":
        description = input(bcolors.BOLD + "Enter the new description for the recipe: " + bcolors.ENDC)
        recipe.description = description
        print(bcolors.OKGREEN + "Change Successful" + bcolors.ENDC)
    elif infoName == "Cook Time":
        cookTime = input(bcolors.BOLD + "Enter the new description for the recipe: " + bcolors.ENDC)
        recipe.cook_time = int(cookTime)
        print(bcolors.OKGREEN + "Change Successful" + bcolors.ENDC)
    elif infoName == "Servings":
        servings = input(bcolors.BOLD + "Enter the new description for the recipe: " + bcolors.ENDC)
        recipe.servings = int(servings)
        print(bcolors.OKGREEN + "Change Successful" + bcolors.ENDC)
    elif infoName == "Difficulty":
        command = command_input("Enter the new Difficulty for the recipe: ",
                                ['easy', 'easy_medium', 'medium', 'medium_hard', 'hard'])
        if command == "easy":
            recipe.difficulty = DifficultyEnum.easy
        elif command == "easy_medium":
            recipe.difficulty = DifficultyEnum.easy_medium
        elif command == "medium":
            recipe.difficulty = DifficultyEnum.medium
        elif command == "medium_hard":
            recipe.difficulty = DifficultyEnum.medium_hard
        elif command == "hard":
            recipe.difficulty = DifficultyEnum.hard
        print(bcolors.OKGREEN + "Change Successful" + bcolors.ENDC)

def update_recipe_step(step, app_session):
    instruction = input(bcolors.BOLD + "Enter the new step instruction for the recipe: " + bcolors.ENDC)
    step.instruction = instruction


def update_ingredient_amount(ingredient, app_session):
    amount = input(bcolors.BOLD + "What amount should this be?" + bcolors.ENDC)
    ingredient.amount = float(amount)
    app_session.session.commit()


def print_ingredient_list_from_search(searchQuery, app_session):
    ingredients = app_session.session.query(Ingredient).filter(Ingredient.name.like("%" + searchQuery + "%")).all()
    for idx, i in enumerate(ingredients):
        print(bcolors.BOLD + str(idx) + ". " + str(i.name) + bcolors.ENDC)

    return ingredients


def create(app_session):
    print(bcolors.BOLD + bcolors.UNDERLINE + "Create a Recipe" + bcolors.ENDC)

    recipe = Recipe()
    app_session.user.Recipes.append(recipe)
    app_session.session.commit()

    edit_info(app_session, recipe)
    edit_ingredients(app_session, recipe)
    edit_steps(app_session,recipe)


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
        app_session.session.commit()
        print_recipe_metadata(recipe)


    if command == "Exit":
        return


def edit_steps(app_session, recipe):
    command = ""

    while command != "Exit":
        print_recipe_steps(recipe)
        command = command_input(bcolors.BOLD + "What would you like todo?\n1. Edit A Step\n2. Add a new step\n3. "
                                               "Delete a Step\n" +
                                bcolors.ENDC, ["1", "2", "3", "4", "Exit"])

        if command == "1":
            command = command_input(bcolors.BOLD + "What step would you like to edit?" + bcolors.ENDC,
                                    [str(s.step_nr) for s in recipe.Steps] + ["Exit"])
            if command != "Exit":
                update_recipe_step(recipe.Steps[int(command) - 1], app_session)
                app_session.session.commit()


        elif command == "2":
            step = Step(step_nr=len(recipe.Steps) + 1)
            recipe.Steps.append(step)
            update_recipe_step(step, app_session)
            app_session.session.commit()

        elif command == "3":
            command = command_input(bcolors.BOLD + "Which step would you like to delete?" + bcolors.ENDC,
                                    [str(s.step_nr) for s in recipe.Steps] + ["Exit"])

            if command != "Exit":
                recipe.Steps.remove(recipe.Steps[int(command) - 1])
                app_session.session.commit()


def edit_ingredients(app_session, recipe):
    command = ""
    while command != "Exit":
        print_recipe_ingredients(recipe)
        command = command_input(bcolors.BOLD + "What would you like todo?\n1. Update an Amount\n2. "
                                               "Add an Ingredient\n3. Remove an Ingredient\n" +
                                bcolors.ENDC, ["1", "2", "3", "Exit"])

        if command == "1":
            command = command_input(bcolors.BOLD + "What ingredient would you like to edit?" + bcolors.ENDC,
                                    [str(idx) for idx, i in enumerate(recipe.Ingredients)] + ["Exit"])
            if command != "Exit":
                update_ingredient_amount(recipe.Ingredients[int(command)], app_session)

        elif command == "2":  # Add an Ingredient

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

            if command == "Exit":
                break

            ingred = RecipeIngredients(Ingredient=ingredients[int(command)])
            recipe.Ingredients.append(ingred)
            update_ingredient_amount(ingred, app_session)
            app_session.session.commit()


        elif command == "3":
            command = command_input(bcolors.BOLD + "What ingredient would you like to delete?" + bcolors.ENDC,
                                    [str(idx) for idx, i in enumerate(recipe.Ingredients)] + ["Exit"])

            if command != "Exit":
                app_session.session.delete(recipe.Ingredients[int(command)])
                app_session.session.commit()

def delete(app_session):
    recipes = get_users_recipes(app_session)

    print(bcolors.BOLD + bcolors.UNDERLINE + "Delete a Recipe" + bcolors.ENDC)
    print("Please Enter the Number of the Recipe you Would Like to Delete. (Or Type \"exit\" to leave this menu")

    for idx, r in enumerate(recipes):
        print(bcolors.BOLD + str(idx) + bcolors.ENDC + '.' + " " + r.name)

    number = command_input(bcolors.BOLD + "Which Recipe?" + bcolors.ENDC,
                            list(str(x) for x in range(0, len(recipes))) + ["Exit"])

    if number == "Exit":
        return

    command = command_input(bcolors.BOLD + "Are you sure?" + bcolors.ENDC,
                            ["Yes", "No"])

    if command == "Yes":
        app_session.session.delete(recipes[int(number)])
        app_session.session.commit()
        print(bcolors.OKCYAN + "Succesfully Deleted" + bcolors.ENDC)

