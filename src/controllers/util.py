
# Provide Text and Possible Options, will return the command entered when a valid one is entered
def command_input(question_text, options):
    command = ""
    while command not in options:
        if command != "":
            print(bcolors.FAIL + "INVALID COMMAND" + bcolors.ENDC)
        command = input(question_text + " (" + ",".join(options) + ") ")
    return command


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
