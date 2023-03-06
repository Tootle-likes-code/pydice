"""
Receives dices strings and then converts them into ParsedDiceStrings.

Functions:
==========
interpret(dice_string: str) -> ParsedDiceString
    Takes a Dice String and processes it into a ParsedDiceString.
"""

from pydice.dice_string import dice_string_parser
from pydice.dice_string.parsed_dice_string import ParsedDiceString


def interpret(dice_string: str) -> ParsedDiceString:
    """
    Converts a dice string into a ParsedDiceString.
    :param dice_string: A string representation of a Dice Pool and it's modifiers.
    :return:
    """
    parsed_dice_string = dice_string_parser.parse(dice_string)

    return parsed_dice_string
