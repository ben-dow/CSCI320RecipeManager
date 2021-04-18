from src.controllers.util import bcolors, command_input
from src.models import DifficultyEnum, Step, RecipeIngredients, Recipe, CookedBy, Ingredient, UserPantry, User


def RecommendationController(app_session):
    command = ""
    print(bcolors.HEADER + "Recommendation System" + bcolors.ENDC)
    while command != "Exit":
        command = command_input(bcolors.BOLD + "What recommendations would you like to see?" + bcolors.ENDC,
                                ["Top Rated", "Recently Added", "In My Pantry", "For You", "Exit"])

        if command == "Top Rated":
            rated(app_session)
        if command == "Recently Added":
            recently_added(app_session)
        if command == "In My Pantry":
            in_pantry(app_session)
        if command == "For You":
            for_you(app_session)
    print(bcolors.OKBLUE + "Exiting Recipe Editor" + bcolors.ENDC)


def rated(app_session):
    recipes = app_session.session.query(Recipe).join(CookedBy).order_by(CookedBy.rating).limit(50).all()
    for idx, r in enumerate(recipes):
        print(bcolors.BOLD + str(idx) + ". " + bcolors.ENDC + r.name)


def recently_added(app_session):
    recipes = app_session.session.query(Recipe).order_by(Recipe.creation_date).limit(50).all()
    for idx, r in enumerate(recipes):
        print(bcolors.BOLD + str(idx) + ". " + bcolors.ENDC + r.name)


def in_pantry(app_session):
    recipes = app_session.session.query(Recipe).join(RecipeIngredients, Recipe.id == RecipeIngredients.recipe_id)\
        .join(UserPantry, (UserPantry.ingredient_id == RecipeIngredients.ingredient_id and
              RecipeIngredients.amount >= UserPantry.current_quantity))\
        .join(CookedBy, Recipe.id == CookedBy.recipe_id)\
        .filter().order_by(CookedBy.rating).limit(50).all()
    for idx, r in enumerate(recipes):
        print(bcolors.BOLD + str(idx) + ". " + bcolors.ENDC + r.name)


def for_you(app_session):
    recipes = app_session.session.query(Recipe).join(CookedBy)\
        .join(User, CookedBy.user_id == User.id)\
        .filter()\
        .order_by(CookedBy.rating).join(User).limit(50).all()
    for idx, r in enumerate(recipes):
        print(bcolors.BOLD + str(idx) + ". " + bcolors.ENDC + r.name)
