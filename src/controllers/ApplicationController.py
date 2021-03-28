from src.controllers.authentication import authenticate
from src.controllers.util import bcolors


def mainApplicationFlow(session):
    print(bcolors.HEADER + "Welcome to the Recipe Manager Application" + bcolors.ENDC)
    user = authenticate(session)
