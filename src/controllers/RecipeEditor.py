import os

from src.controllers.util import bcolors, command_input


def RecipeEditor(app_session):
    command = ""
    while command != "Exit":
        command = command_input(bcolors.BOLD + "What would you like todo?" + bcolors.ENDC,
                                ["Create", "Edit", "Delete", "Exit"])
    print(bcolors.OKBLUE + "Exiting Recipe Editor" + bcolors.ENDC)


def create():
    pass

def edit():
    pass


def delete():
    pass
