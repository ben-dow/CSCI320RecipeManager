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
              RecipeIngredients.amount <= UserPantry.current_quantity))\
        .join(CookedBy, Recipe.id == CookedBy.recipe_id)\
        .filter().order_by(CookedBy.rating).limit(50).all()
    for idx, r in enumerate(recipes):
        print(bcolors.BOLD + str(idx) + ". " + bcolors.ENDC + r.name)


def for_you(app_session):
    """
    This is SQL code that works, having trouble with translating it to python.
     - USER_ID would be the app_session user.
     - It only works for some users; user 4470 has the most recipes (and therefore
        neighbors). User 7108 works well too.
     - Note the last and second nested queries are just the User-CookedBy relationship
        table.

    select r.name, c1.rating from recipes as r, cookedby as c1
    where r.id = c1.recipe_id and c1.user_id in (
        --Find the users who make the same recipes as you
        select c2.user_id from cookedby as c2
        where c2.user_id <> USER_ID and c2.recipe_id in (
            --Recipes cooked by the specified user
            select c3.recipe_id
            from cookedby as c3
            where user_id = 7108))
    --Prevent it from recommending something you have already cooked
    and c1.recipe_id not in (
        --Recipes cooked by the specified user
        select c4.recipe_id from cookedby as c4
        where user_id = 7108)
    order by c1.rating desc

    Here is some python code that doesn't work
        user_cooked = app_session.session.query(CookedBy.recipe_id).filter(CookedBy.user_id == app_session.user.id)
        neighbors = app_session.session.query(CookedBy.user_id).filter(CookedBy.user_id != app_session.user.id)\
            .filter(CookedBy.recipe_id in user_cooked)y
        recipes = app_session.session.query(Recipe).join(neighbors.recipe_id == Recipe.id).limit(50).all()
    """
    recipes = app_session.session.query(Recipe).join(CookedBy, Recipe.id == CookedBy.recipe_id)\
        .join(User, CookedBy.user_id == User.id)\
        .filter()\
        .order_by(CookedBy.rating).join(User).limit(50).all()
    for idx, r in enumerate(recipes):
        print(bcolors.BOLD + str(idx) + ". " + bcolors.ENDC + r.name)
