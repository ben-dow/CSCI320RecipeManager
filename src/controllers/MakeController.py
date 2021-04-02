from datetime import date, datetime

from sqlalchemy.sql.functions import current_date

from src.controllers.PantryController import reduce_quantity_of_item
from src.controllers.SearchController import search_get_results
from src.controllers.util import bcolors, command_input, pretty_print_recipe
from src.models import CookedBy, Recipe

"""
NOTE: This user is a good choice for testing these functions:

id:         1676
username:   Joill1955
password:   ohmoeZ8l

And here is a good recipe to use as well:

recipe_id:      4020
name:           'chocolate coated spoons'
ingredients:    (103, 2167, 7456, 7705)
amounts:        (7.0,  4.0,  8.0,  7.0)
names:          ('whipping cream', 'amaretto', 'disposable spoon', 'vanilla candy coating')
"""


def cook(app_session):
    # os.system('clear')    # clear console window
    command = ""
    print(bcolors.HEADER + "Recipe Cooking Station" + bcolors.ENDC)
    while command != "Exit":
        command = command_input(bcolors.BOLD + "What would you like to do?" + bcolors.ENDC,
                                ["Cook", "View Cooked Recipes", "Exit"])

        if command == "Cook":
            make_recipe(app_session)
        if command == "View Cooked Recipes":
            view_cooked(app_session)

    print(bcolors.OKBLUE + "Exiting Recipe Cooker" + bcolors.ENDC)
    return


def make_recipe(app_session):
    print(bcolors.BOLD + bcolors.UNDERLINE + "Cook a Recipe" + bcolors.ENDC)  # header
    # recipe_list = app_session.session.query(Recipe).filter(Recipe.id == 4020)

    # get the recipe from a search
    recipe = simple_search_recipe(app_session, "Please Enter the Number of the Recipe you Would Like to Cook.")
    if recipe == None:
        return

    # get the scale from user input
    scale = get_scale()
    if scale == float():  # or leave if they wanted to exit
        return

    # get the quantity of each item
    ingr_list = get_quantity(app_session, recipe, scale)
    if not ingr_list:
        print(bcolors.FAIL + "RECIPE FAILED. No ingredients are listed for this recipe." + bcolors.ENDC)
        return
    if type(ingr_list[0]) == str:
        print(bcolors.FAIL + "RECIPE FAILED. Needs " + str(ingr_list[1]) + " more " + ingr_list[0] + "." + bcolors.ENDC)
        return

    # rate the dish
    print(bcolors.OKGREEN + "You just cooked: " + recipe.name + "!" + bcolors.ENDC)
    command = command_input(bcolors.BOLD + "On a scale from 1 to 5, how was this dish?" + bcolors.ENDC,
                            ['1', '2', '3', '4', '5'])

    # mark this moment down in history
    add_cooked_by(app_session, recipe, int(command), scale)

    # since all ingredients are guaranteed to be there, make the changes
    for ingr, amount in ingr_list:
        if not reduce_quantity_of_item(app_session, ingr, amount):
            return

    return


def simple_search_recipe(app_session, question):
    search_type = command_input(bcolors.BOLD + "How would you like to search?" + bcolors.ENDC,
                                ["By Ingredient", "By Name", "By Category", "Exit"])
    if search_type == "Exit":
        return None     # notify main to exit program

    sort_type = command_input(bcolors.BOLD + "How would you like to sort the search?" + bcolors.ENDC,
                              ["Name", "Rating", "Recent", "Exit"])
    if sort_type == "Exit":
        return None     # notify to exit program

    command = input("Search Now: ")
    if command == "Exit":
        return None     # notify to exit program

    recipe_list = search_get_results(app_session, command, search_type, sort_type)

    if recipe_list == None:  # if no recipes, return to cook menu
        print(bcolors.FAIL + "No Recipes Found." + bcolors.ENDC)
        return None

    # pick a recipe from the search criteria
    print(question + " (Or Type \"Exit\" to leave this menu)")
    command = command_input(bcolors.BOLD + "Which Recipe?" + bcolors.ENDC,
                            list(str(x) for x in range(0, recipe_list.count())) + ["Exit"])

    if command == "Exit":
        return None

    return recipe_list[int(command)]


# Print current quantity of ingredients
def get_quantity(app_session, recipe, scale=1):
    # below is the SLQ statement to run. Returns all ingredients from a recipe and their quantity in a user's pantry
    """
    select ri.recipe_id, ri.ingredient_id, sum(p.current_quantity)
    from recipe_ingredients as ri
        left outer join pantry as p
        on ri.ingredient_id = p.ingredient_id and user_id = 1676
        and p.expiration_date > current_date
    where ri.recipe_id = 4944
    group by ri.recipe_id, ri.ingredient_id
    order by ri.ingredient_id
    """

    p_dict = {}
    for p in app_session.user.Pantry:
        if p.expiration_date > date.today():
            if p.ingredient_id not in p_dict:
                p_dict.setdefault(p.ingredient_id, p.current_quantity)
            else:
                p_dict[p.ingredient_id] = p_dict.get(p.ingredient_id) + p.current_quantity

    ingr_list = []
    for ingr in recipe.Ingredients:
        if ingr.ingredient_id in p_dict:
            required_amount = p_dict[ingr.ingredient_id] - ingr.amount * scale
            if required_amount > 0:
                ingr_list.append([ingr.Ingredient, ingr.amount * scale])
            else:
                return [ingr.Ingredient.name, abs(required_amount)]
        else:       # if not enough ingredient, returns offending party's name name and the deficit
            return [ingr.Ingredient.name, ingr.amount * scale]

    return ingr_list


# gets the scale from the user, or float() if they wish to exit.
def get_scale():
    scale = float()
    command = ""
    while scale == float():
        print("Please Enter the Scale of the Recipe. (Or \"Exit\" to leave this menu)")
        command = input(bcolors.BOLD + "Scale? " + bcolors.ENDC)

        if command == "Exit":  # exit
            return float()

        try:  # check for valid input
            scale = float(command)
        except ValueError:
            print(bcolors.FAIL + "INVALID SCALE. Must be an integer or decimal number." + bcolors.ENDC)

    return scale


# add a new row in the CookedBy table
def add_cooked_by(app_session, recipe, rating, scale):
    cb = app_session.user.CookedBy # get list of user's past recipes

    new_cooked_by = CookedBy(recipe_id=recipe.id, user_id=app_session.user.id, rating=rating, scale=scale,
                             cook_date=date.today())    # create row for this recipe

    for i in cb:    # delete previous instances of this recipe
        if (i.recipe_id == recipe.id) & (app_session.user.id == i.user_id):
            app_session.session.delete(i)

    app_session.user.CookedBy.append(new_cooked_by)  # add the new row, commit it
    app_session.session.commit()
    return


# View your previously cooked recipes.
def view_cooked(app_session):
    print(bcolors.BOLD + bcolors.UNDERLINE + "View Cooked Recipes" + bcolors.ENDC)

    # get cooked recipes
    cooked = app_session.session.query(Recipe.name, CookedBy.scale, CookedBy.cook_date, CookedBy.rating) \
        .filter(CookedBy.user_id == app_session.user.id) \
        .filter(Recipe.id == CookedBy.recipe_id).order_by(CookedBy.cook_date.desc())

    # print each recipe and its data
    idc = 1
    for name, scale, date, rating in cooked:
        # print the metadata
        print(bcolors.BOLD + name + bcolors.ENDC)
        print("Scale: " + str(scale))
        print("Date Cooked: " + str(date))
        print("Rating:" + str(rating))
        # Limit the number of responses shown
        if idc % 10 == 0:
            command = command_input(bcolors.OKGREEN + "Keep going?", ["Yes", "Exit"])
            if command == "Exit":
                return
        idc += 1

    return
