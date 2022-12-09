from pydice.dice_string import dice_string_parser
from pydice.dice_string.parsed_dice_string import ParsedDiceString


def interpret(dice_string) -> ParsedDiceString:
    parsed_dice_string = dice_string_parser.parse(dice_string)

    return parsed_dice_string
