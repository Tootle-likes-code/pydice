import re
from re import Match

from pydice.dice_result_builder import DiceResultBuilder, FateDiceResultBuilder
from pydice.die import Dice, Die
from pydice.roll_result import RollResult


def _build_fate_roll_result(result: Match) -> RollResult:
    fate_dice_builder = FateDiceResultBuilder.create_fate_dice_result_builder()

    if result.group("add_modifier") is not None:
        fate_dice_builder.with_add_modifier(result.group("add_modifier"))

    return fate_dice_builder.build()


def _interpret_fate_dice(dice_string) -> RollResult | None:
    regex = r"[dD][fF](?:\+(?P<add_modifier>\d*))?"
    result = re.match(regex, dice_string)

    if result:
        return _build_fate_roll_result(result)


def _get_dice(result: Match) -> Dice:
    number_of_dice = result.group("number_of_dice")
    if not number_of_dice:
        number_of_dice = 1
    else:
        number_of_dice = int(number_of_dice)

    size_of_dice = int(result.group("size_of_dice"))
    dice = Dice(number_of_dice=number_of_dice, die=Die(size_of_dice))
    return dice


def _build_roll_result(result: Match) -> RollResult:
    dice = _get_dice(result)
    builder = DiceResultBuilder.create_dice_result_builder(dice)

    if result.group("add_modifier") is not None:
        add_modifier = result.group("add_modifier")
        builder.with_add_modifier(add_modifier)

    return builder.build()


def _interpret_general_dice(dice_string) -> RollResult | None:
    regex = r"(?P<number_of_dice>\d*)[dD](?P<size_of_dice>\d*)(?:\+(?P<add_modifier>\d*))?"
    result = re.match(regex, dice_string)

    if result:
        return _build_roll_result(result)


def interpret(dice_string) -> RollResult | None:
    if "df" in dice_string:
        return _interpret_fate_dice(dice_string)

    return _interpret_general_dice(dice_string)
