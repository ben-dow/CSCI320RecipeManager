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

    select distinct r1.name, c1.rating from recipes as r1
    join cookedby c1 on r1.id = c1.recipe_id
    where c1.user_id in (
        select distinct c_f.user_id from cookedby as c_f
        join (
            select r_u.id from recipes as r_u
            join cookedby as c_u on r_u.id = c_u.recipe_id
            where c_u.user_id = USER_ID)
        as r_u2 on c_f.recipe_id = r_u2.id
        and c_f.user_id <> USER_ID)
    and r1.id not in (
        select r_u.id from recipes as r_u
        join cookedby as c_u on r_u.id = c_u.recipe_id
        where c_u.user_id = USER_ID)
    order by c1.rating desc
    """
    user_cooked = app_session.session.query(Recipe.id).join(CookedBy, Recipe.id == CookedBy.recipe_id)\
                    .filter(CookedBy.user_id == app_session.user.id).all()
    friends = app_session.session.query(CookedBy.user_id).join(Recipe, CookedBy.recipe_id == Recipe.id)\
                    .filter(CookedBy.recipe_id.in_(user_cooked), CookedBy.user_id != app_session.user.id).all()
    rec_recipes = app_session.session.query(Recipe).join(CookedBy, CookedBy.recipe_id == Recipe.id)\
                    .filter((CookedBy.user_id.in_(friends)), Recipe.id.notin_(user_cooked))\
                    .order_by(CookedBy.rating).limit(50).all()
    for idx, r in enumerate(rec_recipes):
        print(bcolors.BOLD + str(idx) + ". " + bcolors.ENDC + r.name)
