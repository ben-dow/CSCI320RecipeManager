from src.controllers.CreateController import create
from src.controllers.MakeController import make
from src.controllers.PantryController import pantry
from src.controllers.SearchController import search
from src.controllers.authentication import authenticate
from src.controllers.util import bcolors, command_input


def help():
    pass


def functionality_flow(app_session):
    command = command_input(bcolors.BOLD + "What would you like todo?" + bcolors.ENDC, ["Search", "Make", "Create", "Pantry", "Help", "Logout"])

    options = {
        "Search": search,
        "Make": make,
        "Create": create,
        "Pantry": pantry,
        "Help": help,
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
