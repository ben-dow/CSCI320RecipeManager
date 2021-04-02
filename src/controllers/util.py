# Provide Text and Possible Options, will return the command entered when a valid one is entered
from src.models import Ingredient


def command_input(question_text, options):
    command = ""
    while command not in options:
        if command != "":
            print(bcolors.FAIL + "INVALID COMMAND" + bcolors.ENDC)
        command = input(question_text + " (" + ", ".join(str(x) for x in options) + ") ")
    return command


# Pantry Utils

def pretty_print_pantry(userPantry):
    print(bcolors.HEADER + "Pantry: " + bcolors.ENDC)
    for idx, item in enumerate(userPantry):
        print('\t' + bcolors.BOLD + str(item.ingredient.name) + bcolors.ENDC)


# Recipe Utils
def pretty_print_recipe(recipe):
    print(bcolors.HEADER + "Recipe: " + recipe.name + bcolors.ENDC)
    print_recipe_metadata(recipe)
    print_recipe_steps(recipe)
    print_recipe_ingredients(recipe)


def print_recipe_metadata(recipe):
    print(bcolors.BOLD + "About this Recipe" + bcolors.ENDC)
    print('\t' + bcolors.BOLD + "Name: " + bcolors.ENDC + str(recipe.name))
    print('\t' + bcolors.BOLD + "Description: " + bcolors.ENDC + str(recipe.description))
    print('\t' + bcolors.BOLD + "Difficulty: " + bcolors.ENDC + str(recipe.difficulty))
    print('\t' + bcolors.BOLD + "Servings: " + bcolors.ENDC + str(recipe.servings))
    print('\t' + bcolors.BOLD + "Cook Time: " + bcolors.ENDC + str(recipe.cook_time) + " minutes")


def print_recipe_steps(recipe):
    print(bcolors.BOLD + "Steps:" + bcolors.ENDC)
    for step in recipe.Steps:
        print('\t' + bcolors.BOLD + str(step.step_nr) + ". " + bcolors.ENDC + step.instruction)


def print_recipe_ingredients(recipe):
    print(bcolors.BOLD + "Ingredients:" + bcolors.ENDC)
    for idx, i in enumerate(recipe.Ingredients):
        print('\t' + str(idx) + ". " + i.Ingredient.name + ": " + str(i.amount))


def print_recipe_categories(recipe):
    print(bcolors.BOLD + "Categories:" + bcolors.ENDC)
    for idx, i in enumerate(recipe.Categories):
        print('\t' + str(idx) + ". " + i.category_type)

# ANSI Codes for Colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_ingredient_list_from_search(searchQuery, app_session):
    ingredients = app_session.session.query(Ingredient).filter(Ingredient.name.like("%" + searchQuery + "%")).all()
    for idx, i in enumerate(ingredients):
        print(bcolors.BOLD + str(idx) + ". " + str(i.name) + bcolors.ENDC)

    return ingredients
