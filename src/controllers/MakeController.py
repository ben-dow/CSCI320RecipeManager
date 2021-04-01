import os

from sqlalchemy.sql.functions import count, current_date

from src.controllers.RecipeController import get_users_recipes
from src.controllers.SearchController import search
from src.controllers.util import bcolors, command_input, pretty_print_recipe
from src.models import Category, UserPantry, Ingredient, CookedBy, Recipe

"""
NOTE: This user is a good choice for testing these functions:

id:         1676
username:   Joill1955
password:   ohmoeZ8l
"""

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
            view_cooked(app_session)

    print(bcolors.OKBLUE + "Exiting Recipe Cooker" + bcolors.ENDC)
    return


def make_recipe(app_session):
    print(bcolors.BOLD + bcolors.UNDERLINE + "Cook a Recipe" + bcolors.ENDC)    # header
    recipe_list = get_users_recipes(app_session)  # TODO: Replace with search function

    if len(recipe_list) == 0: # if no recipes, return to cook menu
        print(bcolors.FAIL + "No Recipes Found." + bcolors.ENDC)
        return

    # pick a recipe from the search criteria. TODO: Allow to search again
    for idx, r in enumerate(recipe_list):  # print out the available choices
        print(bcolors.BOLD + str(idx) + bcolors.ENDC + '.' + " " + r.name)
    print("Please Enter the Number of the Recipe you Would Like to Cook. (Or Type \"Exit\" to leave this menu)")
    command = command_input(bcolors.BOLD + "Which Recipe?" + bcolors.ENDC,
                            list(str(x) for x in range(0, len(recipe_list))) + ["Exit"])

    if command == "Exit":
        return

    # get the recipe
    print(bcolors.OKGREEN + "Cooking Recipe:" + bcolors.ENDC)
    recipe = recipe_list[int(command)]
    pretty_print_recipe(recipe)

    # TODO: Print ingredients needed and their current quantity
    print(bcolors.BOLD + "Ingredients Required" + bcolors.ENDC)
    get_quantity(app_session, recipe)

    # get the scale from user input
    scale = get_scale()
    if scale == float():    # or leave if they wanted to exit
        return

    # TODO: Check that there are enough ingredients to make the recipe; choose a different scale if not?


    # TODO: Subtract the ingredients used from the recipe, print success message

    return


# Print current quantity of ingredients
def get_quantity(app_session, recipe):
    # TODO: Get ids of ingredients needed for the recipe
    ingredient_ids = (ingr.name for ingr in recipe.Ingredients)
    for i in ingredient_ids:
        print(i)
    # get list of [(ingredient.name, ingredient.count)] from user's pantry
    ingredients = app_session.session.query(Ingredient.name, count(UserPantry.current_quantity))\
                                    .filter(UserPantry.user_id == app_session.user.id)\
                                    .filter(UserPantry.expiration_date > current_date())\
                                    .group_by(Ingredient.name).order_by(Ingredient.name.asc())
    """
    select i.name, sum(p.current_quantity) Quantity
    from ingredients as i, pantry as p
    where i.id = p.ingredient_id and p.expiration_date > CURRENT_DATE
    group by i.name
    order by i.name asc
    """
    # print each ingredient's name and current quantity
    """for name, quantity in ingredients:
        print(bcolors.BOLD + name + bcolors.ENDC + "\t" + str(quantity))
    """
    # return list of ingredients to help with editing?
    return ingredients


# gets the scale from the user, or float() if they wish to exit.
def get_scale():
    scale = float()
    command = ""
    while scale == float():
        print("Please Enter the Scale of the Recipe. (Or \"Exit\" to leave this menu)")
        command = input(bcolors.BOLD + "Scale?" + bcolors.ENDC)

        if command == "Exit":   # exit
            return float()

        try:    # check for valid input
            scale = float(command)
        except ValueError:
            print(bcolors.FAIL + "INVALID SCALE. Must be an integer or decimal number." + bcolors.ENDC)

    return scale


# View your previously cooked recipes.
def view_cooked(app_session):
    print(bcolors.BOLD + bcolors.UNDERLINE + "View Cooked Recipes" + bcolors.ENDC)

    # get cooked recipes
    cooked = app_session.session.query(Recipe.name, CookedBy.scale, CookedBy.cook_date, CookedBy.rating)\
                                .filter(CookedBy.user_id == app_session.user.id)\
                                .filter(Recipe.id == CookedBy.recipe_id).order_by(CookedBy.cook_date.desc())

    # print each recipe and its data
    idc = 1
    for name, scale, date, rating in cooked:
        if idc % 10 == 0:   # Limit the number of responses shown
            command = command_input(bcolors.OKGREEN + "Keep going?", ["Yes", "Exit"])
            if command == "Exit":
                break
        print(bcolors.BOLD + name + bcolors.ENDC)
        print("Scale: " + str(scale))
        print("Date Cooked: " + str(date))
        print("Rating:" + str(rating))

        idc += 1

    return
