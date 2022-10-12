import re
from re import Match, Pattern

from pydice.dice_string.dice_parse_errors import DiceParseError
from pydice.dice_string.operators import Operator, OperatorFactory
from pydice.die import Dice, Die, FateDie
from pydice.roll_result import RollResult
from pydice.roll_result_operators.roll_result_builder import RollResultBuilder

_fate_regex = re.compile(r"df", re.IGNORECASE)
_storyteller_regex = re.compile(r"(?P<number_of_dice>\d+)st", re.IGNORECASE)
_base_dice_regex = re.compile(r"(?:\d*d\d.)|(?:\d+st)|(?:df)", re.IGNORECASE)
_extract_dice_regex = re.compile(r"(?P<number_of_dice>\d*)d(?P<dice_size>\d+)", re.IGNORECASE)


class DiceStringParser:
    def __init__(self, dice_string: str):
        self._dice: Dice
        self._operators: list[Operator] = []
        self.dice_string = dice_string
        self._parse_dice_string()

    def _parse_dice_string(self) -> None:
        self._extract_dice()
        self._get_operators()

    def _extract_dice(self) -> None:
        is_specialty_dice = self._check_specialty_dice()
        if is_specialty_dice:
            return

        self._extract_default_dice()

    def _check_specialty_dice(self) -> bool:
        if self._check_string_for_dice(_fate_regex):
            self._create_fate_dice()
            return True

        storyteller_match = self._check_string_for_dice(_storyteller_regex)
        if storyteller_match:
            self._create_storyteller_dice(storyteller_match)
            return True

        return False

    def _check_string_for_dice(self, dice_regex: Pattern) -> Match:
        match = re.match(dice_regex, self.dice_string)

        return match

    def _create_fate_dice(self):
        self._dice = Dice(FateDie(), 4)

    def _create_storyteller_dice(self, storyteller_match: Match) -> None:
        number_of_dice = storyteller_match.group("number_of_dice")
        self._dice = Dice(Die(10), int(number_of_dice))
        self._operators = self._operators + OperatorFactory.get_storyteller_operators()

    def _extract_default_dice(self) -> None:
        dice_match = re.match(_extract_dice_regex, self.dice_string)
        if not dice_match:
            raise DiceParseError(self.dice_string)

        number_of_dice = int(dice_match.group("number_of_dice")) if \
            "number_of_dice" in dice_match.groupdict().keys() \
            and dice_match.group("number_of_dice") != '' \
            else 1
        dice_size = int(dice_match.group("dice_size"))

        self._dice = Dice(Die(dice_size), number_of_dice)

    def _get_operator_string(self):
        modifiers = re.split(_base_dice_regex, self.dice_string)
        return modifiers[1]

    def _get_operators(self) -> None:
        operator_string = self._get_operator_string()
        self._operators = self._operators + OperatorFactory.get_operators(operator_string)

    def parse(self) -> RollResult | None:
        builder = RollResultBuilder.create_roll_result_builder(self._dice)
        for operator in self._operators:
            if operator is None:
                return None
            builder = operator.add(builder)

        return builder.build()


def create(dice_string: str) -> DiceStringParser | None:
    return DiceStringParser(dice_string)
