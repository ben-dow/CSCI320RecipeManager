from src.controllers.util import bcolors, command_input


def pantry(app_session):
    command = ""
    print(bcolors.HEADER + "Update Your Pantry" + bcolors.ENDC)
    while command != "exit":
        command = command_input(bcolors.BOLD + "What do you want to do with your pantry?" + bcolors.ENDC,
                                ["add", "remove"])
        if command == "add":
            add(app_session)
        if command == "remove":
            remove(app_session)



def get_users_pantry(app_session): ## Struggling to figure out how to
    user = app_session.user
    pantry = user.UserPantry
    return pantry



def add(app_session):
    pantry = get_users_pantry(app_session)


    command=""
    print(bcolors.BOLD + "Add ingredient(s)" + bcolors.ENDC)
    print("Enter (or exit)")
    command = command_input(bcolors.BOLD + "Enter the ingredients you'd like to add" + bcolors.ENDC,
                            ["exit"])
    if command == "exit":
        return
    if command != "exit":
        pass

def remove(app_session):
    pantry = get_users_pantry(app_session)

    print(bcolors.BOLD + "Please enter the number of the ingredient you want to remove. Type \"exit\" to close the Pantry Manager.")
    command=""
    for idx, r in enumerate(pantry):
        print(bcolors.BOLD + str(idx) + bcolors.ENDC + '.' + " " + str(r.join(Ingredient).name))
    command = command_input(bcolors.BOLD + "Select the ingredient you want to remove (or type exit to leave this menu)" + bcolors.ENDC,
                             ["exit"])
    if command == "exit":
        return

    if command !="exit":
        pass

#todo
#function for adding items to pantry
#function for removing items to pantry

