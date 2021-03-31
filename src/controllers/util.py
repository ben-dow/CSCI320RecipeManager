# Provide Text and Possible Options, will return the command entered when a valid one is entered
def command_input(question_text, options):
    command = ""
    while command not in options:
        if command != "":
            print(bcolors.FAIL + "INVALID COMMAND" + bcolors.ENDC)
        command = input(question_text + " (" + ",".join(str(x) for x in options) + ") ")
    return command


def pretty_print_recipe(recipe):
    print(bcolors.BOLD + "Name: " + bcolors.ENDC + str(recipe.name))
    print(bcolors.BOLD + "Description+: " + bcolors.ENDC + str(recipe.description))
    print(bcolors.BOLD + "Difficulty: " + bcolors.ENDC + str(recipe.difficulty))
    print(bcolors.BOLD + "Cook Time: " + bcolors.ENDC + str(recipe.cook_time) + " minutes")


# ANSI Codes for Colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
