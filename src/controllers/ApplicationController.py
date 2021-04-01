from src.controllers.RecipeController import RecipeController
from src.controllers.MakeController import cook
from src.controllers.PantryController import pantry_manager
from src.controllers.SearchController import search
from src.controllers.authentication import authenticate
from src.controllers.util import bcolors, command_input


def functionality_flow(app_session):
    command = command_input(bcolors.BOLD + "What would you like todo?" + bcolors.ENDC,
                            ["Search", "Cook", "RecipeEditor", "Pantry", "Logout"])

    # Emulate a Switch Statement
    options = {
        "Search": search,
        "Cook": cook,
        "RecipeEditor": RecipeController,
        "Pantry": pantry_manager,
    }
    if command == "Logout":
        app_session.logout = True
    else:
        options[command](app_session)


def mainApplicationFlow(session):
    print(bcolors.HEADER + "Welcome to the Recipe Manager Application" + bcolors.ENDC)
    appSession = authenticate(session)

    while not appSession.logout:
        functionality_flow(appSession)

    print(bcolors.OKGREEN + "Successfully Logged Out! Come again!" + bcolors.ENDC)
