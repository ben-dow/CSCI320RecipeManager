import os

from src.controllers.util import bcolors, command_input


def RecipeEditor(app_session):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(bcolors.HEADER + "Recipe Editor" + bcolors.ENDC)
    command = ""
    while command != "Exit":    # mystery character appears for me here
        command = command_input(bcolors.BOLD + "What would you like todo?" + bcolors.ENDC,
                                ["Create", "Edit", "Delete", "Exit"])
    print(bcolors.OKBLUE + "Exiting Recipe Editor" + bcolors.ENDC)


def create():
    pass

def edit():
    pass


def delete():
    pass
