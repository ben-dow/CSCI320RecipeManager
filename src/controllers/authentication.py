from sqlalchemy.sql.functions import current_date

from src.controllers.util import command_input, bcolors
from src.models import User

def loginInput(session):
    validUserFound = False
    while not validUserFound:
        username = input("Username: ")
        password = input("Password: ")

        user_count = session.query(User).filter(getattr(User, 'username') == username,
                                                getattr(User, "password") == password).count()
        if user_count == 1:
            user = session.query(User).filter(getattr(User, 'username') == username,
                                              getattr(User, "password") == password).one()

            user.last_access_date = current_date()
            session.commit()
            print(bcolors.OKBLUE + "Successfully Logged In" + bcolors.ENDC)
            return user
        else:
            print(bcolors.FAIL + "User and Password Combination not Found" + bcolors.ENDC)


def registerInput(session):
    valid_username = False
    while not valid_username:
        username = input("Username: ")
        password = input("Password: ")

        user = session.query(User).filter(getattr(User, 'username') == username).count()

        if user > 0:
            valid_username = False
            print(bcolors.FAIL + "Username is Already in Use" + bcolors.ENDC)
        else:
            print(bcolors.OKBLUE + "Successfully Registered!" + bcolors.ENDC)
            valid_username = True
            new_user = User(username=username, password=password, creation_date = current_date())
            session.add(new_user)
            session.commit()


def authenticate(session):
    login_or_register = command_input(bcolors.BOLD + "Would you like to Login or Register?"
                                      + bcolors.ENDC, ["Login", "Register"])

    if login_or_register == "Register":
        registerInput(session)
        print("Please Login!")

    return loginInput(session)