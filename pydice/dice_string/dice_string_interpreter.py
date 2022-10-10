from pydice.dice_string import dice_string_parser
from pydice.roll_result import RollResult


def interpret(dice_string) -> RollResult | None:
    dice_parser = dice_string_parser.create(dice_string)
    roll_result = dice_parser.parse()

    return roll_result
