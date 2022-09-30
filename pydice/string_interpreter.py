import re

from pydice.die import Dice, Die


def interpret(dice_string):
    regex = r"(?P<number_of_dice>\d*)[dD](?P<size_of_dice>\d*)"
    result = re.match(regex, dice_string)

    if result:
        number_of_dice = result.group("number_of_dice")
        if not number_of_dice:
            number_of_dice = 1
        else:
            number_of_dice = int(number_of_dice)

        size_of_dice = int(result.group("size_of_dice"))
        dice = Dice(number_of_dice=number_of_dice, die=Die(size_of_dice))
        return dice
