from pydice.dice_string.dice_string_parser_factory import DiceStringParserFactory
from pydice.dice_string.parsed_dice_string import ParsedDiceString


def parse(dice_string: str) -> ParsedDiceString:
    return DiceStringParserFactory.create_parsed_dice_string(dice_string)
