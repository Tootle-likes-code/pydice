import re
from abc import ABC, abstractmethod
from re import Match, Pattern

from pydice.roll_result_operators.roll_result_builder import RollResultBuilder
from pydice.die import Dice, Die, FateDie
from pydice.dice_string.operators import Operator, OperatorFactory
from pydice.roll_result import RollResult

_fate_regex = re.compile(r"df", re.IGNORECASE)
_storyteller_regex = re.compile(r"(?P<number_of_dice>\d+)st", re.IGNORECASE)
_base_dice_regex = re.compile(r"(?:\d*d\d.)|(?:\d+st)|(?:df)", re.IGNORECASE)
_extract_dice_regex = re.compile(r"(?P<number_of_dice>\d*)d(?P<dice_size>\d+)", re.IGNORECASE)


class DiceStringParser(ABC):
    def __init__(self, dice: Dice, operators: list[Operator] = None):
        self.dice = dice
        self._operators: list[Operator] = operators if operators is not None else []

    @abstractmethod
    def parse(self) -> RollResult:
        pass


class DefaultDiceStringParser(DiceStringParser):
    def __init__(self, dice: Dice, operators: list[Operator] = None):
        super().__init__(dice, operators)

    def parse(self) -> RollResult | None:
        builder = RollResultBuilder.create_roll_result_builder(self.dice)
        for operator in self._operators:
            if operator is None:
                return None
            builder = operator.add(builder)

        return builder.build()


def _check_string_for_dice(dice_regex: Pattern, dice_string: str) -> Match:
    match = re.match(dice_regex, dice_string)

    return match


def _create_fate_dice():
    return Dice(FateDie(), 4)


def _create_storyteller_dice(storyteller_match: Match) -> (Dice, str):
    number_of_dice = storyteller_match.group("number_of_dice")
    dice = Dice(Die(10), int(number_of_dice))
    return dice, "=10>=7"


def _check_specialty_dice(dice_string: str) -> (Dice, str):
    if _check_string_for_dice(_fate_regex, dice_string):
        return _create_fate_dice()

    storyteller_match = _check_string_for_dice(_storyteller_regex, dice_string)
    if storyteller_match:
        return _create_storyteller_dice(storyteller_match)


def _construct_dice_from_string(dice_match: Match) -> Dice | None:
    number_of_dice = int(dice_match.group("number_of_dice")) if \
        "number_of_dice" in dice_match.groupdict().keys() \
        and dice_match.group("number_of_dice") != '' \
        else 1
    dice_size = int(dice_match.group("dice_size"))

    return Dice(Die(dice_size), number_of_dice)


def _get_dice(dice_string: str) -> (Dice, str):
    specialty_dice = _check_specialty_dice(dice_string)
    if specialty_dice:
        return specialty_dice

    dice_match = re.match(_extract_dice_regex, dice_string)
    if not dice_match:
        return

    return _construct_dice_from_string(dice_match), ""


def _get_operator_string(dice_string):
    modifiers = re.split(_base_dice_regex, dice_string)
    return modifiers[1]


def _split_operators(operator_string) -> list[Operator]:
    operator = ""
    value = ""
    operators: list[Operator] = []
    for i in range(len(operator_string)):
        character = operator_string[i:i + 1][0]
        if character.isnumeric():
            if i != len(operator_string) and operator_string[i + 1:i + 2].isnumeric():
                value = character
                continue
            value += character
            built_operator = OperatorFactory.get_operator(operator, int(value))
            if built_operator is not None:
                operators.append(built_operator)
            operator = ""
            value = ""
        else:
            operator += character

    return operators


def _get_operators(dice_string: str, dice_based_operators: str = "") -> list[Operator]:
    operator_string = _get_operator_string(dice_string)
    operator_string = dice_based_operators + operator_string
    return _split_operators(operator_string)


def create(dice_string: str) -> DiceStringParser | None:
    dice = _get_dice(dice_string)
    dice_based_operators = ""

    if not dice:
        return
    if isinstance(dice, tuple):
        dice, dice_based_operators = dice

    operators = _get_operators(dice_string, dice_based_operators)

    return DefaultDiceStringParser(dice, operators)
