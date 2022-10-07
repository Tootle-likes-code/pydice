import re
from abc import ABC, abstractmethod

from pydice.dice_result_builder import DiceResultBuilder
from pydice.die import Dice, Die
from pydice.operators import Operator, OperatorFactory
from pydice.roll_result import RollResult

_base_dice_regex = re.compile(r"\d*d\d.", re.IGNORECASE)
_extract_dice_regex = re.compile(r"(?P<number_of_dice>\d*)d(?P<dice_size>\d+)", re.IGNORECASE)


class DiceStringParser(ABC):
    def __init__(self, dice: Dice, operators: list[Operator] = None):
        self.dice = dice
        self._operators: list[Operator] = operators if operators is not None else []

    @abstractmethod
    def parse(self) -> RollResult | None:
        pass


class DefaultDiceStringParser(DiceStringParser):
    def __init__(self, dice: Dice, operators: list[Operator] = None):
        super().__init__(dice, operators)

    def parse(self) -> RollResult | None:
        builder = DiceResultBuilder.create_dice_result_builder(self.dice)
        for operator in self._operators:
            if operator is None:
                return None
            builder = operator.add(builder)

        return builder.build()


class FateDiceStringParser(DiceStringParser):
    def parse(self) -> RollResult | None:
        pass


class StorytellerDiceStringParser(DiceStringParser):
    def parse(self) -> RollResult | None:
        pass


def _get_dice(dice_string: str) -> Dice | None:
    dice_match = re.match(_extract_dice_regex, dice_string)

    if dice_match:
        number_of_dice = int(dice_match.group("number_of_dice")) if \
            "number_of_dice" in dice_match.groupdict().keys() \
            and dice_match.group("number_of_dice") != '' \
            else 1
        dice_size = int(dice_match.group("dice_size"))

        return Dice(Die(dice_size), number_of_dice)


def _get_operator_string(dice_string):
    modifiers = re.split(_base_dice_regex, dice_string)
    return modifiers[1]


def _split_operators(operator_string) -> list[Operator]:
    operator = ""
    operators: list[Operator] = []
    for i in range(len(operator_string)):
        character = operator_string[i:i + 1][0]
        if character.isnumeric():
            built_operator = OperatorFactory.get_operator(operator, int(character))
            operators.append(built_operator)
            operator = ""
        else:
            operator += character

    return operators


def _get_operators(dice_string) -> list[Operator]:
    operator_string = _get_operator_string(dice_string)
    return _split_operators(operator_string)


def create(dice_string: str) -> DiceStringParser | None:
    dice_match = re.match(_extract_dice_regex, dice_string)
    if not dice_match:
        return

    try:
        dice = _get_dice(dice_string)
        operators = _get_operators(dice_string)

        return DefaultDiceStringParser(dice, operators)
    except IndexError:
        return None
