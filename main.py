import getopt
import sys

from pydice.dice_string.dice_string_interpreter import interpret

if __name__ == "__main__":
    options, arguments = getopt.getopt(sys.argv[1:], "d:h", ["dice_string=", "help"])

    for o, a in options:
        if o in ("-h", "--help"):
            print("Welcome to pydice's interpreter!")
            print("In order to run this, you will need a dice string and need to use either '-d <dice_string>' or "
                  "'--dice_string=<dice_string>' e.g. '-d 1d20+4'")
            print()
            print("For more information, see https://github.com/Tootle-likes-code/pydice/blob/main/README.md for more "
                  "details.")
            sys.exit()
        if o in ("-d", "--dice"):
            dice_string = a
            result = interpret(a)
            print(f"Rolled {dice_string}")
            print(f"Roll values: {result.die_rolls}")
            print(f"Result: {result.result()}")
            sys.exit()
