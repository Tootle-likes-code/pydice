import re
from re import Match
from typing import Optional, Pattern

from pydice.dice_string.dice_parser_failures import DiceParserFailure, InvalidDice
from pydice.dice_string.dice_string_parser import ParsedDiceString
from pydice.dice_string.operators import Operator, OperatorFactory
from pydice.die import Dice, Die, FateDie
from pydice.roll_result import RollResult
from pydice.roll_result_operators.roll_result_builder import RollResultBuilder

_fate_regex = re.compile(r"df", re.IGNORECASE)
_storyteller_regex = re.compile(r"(?P<number_of_dice>\d+)st", re.IGNORECASE)
_base_dice_regex = re.compile(r"(?:\d*d\d.)|(?:\d+st)|(?:df)", re.IGNORECASE)
_extract_dice_regex = re.compile(r"(?P<number_of_dice>\d*)d(?P<dice_size>\d+)", re.IGNORECASE)

fate_dice = Dice(FateDie(), 4)
d10 = Die(10)


class ParsedDiceStringBuilder:

    @staticmethod
    def create_parsed_dice_string(dice_string: str):
        return ParsedDiceStringBuilder(dice_string)

    def __init__(self, dice_string: str):
        self._dice_string = dice_string
        self._dice: Dice | None = None
        self._operators: list[Operator] = []
        self._roll_result: Optional[RollResult] = None
        self._failures: list[DiceParserFailure] = []

    def with_dice(self, dice: Dice):
        self._dice = dice
        return self

    def with_fate_dice(self):
        self._dice = fate_dice
        return self

    def with_storyteller_dice(self, number_of_dice: int):
        self._dice = Dice(d10, number_of_dice)

    def with_operators(self, operators: list[Operator]):
        self._operators = operators
        return self

    def with_failure(self, failure: DiceParserFailure):
        self._failures.append(failure)
        return self

    def with_dice_failure(self):
        failure = InvalidDice(self._dice_string)
        return self.with_failure(failure)

    def build(self) -> ParsedDiceString:
        self._build_roll_result()
        return ParsedDiceString(self._dice_string, self._dice, self._operators, self._failures, self._roll_result)

    def _build_roll_result(self):
        if not self._can_build_result():
            return
        builder = RollResultBuilder.create_roll_result_builder(self._dice)
        for operator in self._operators:
            if operator is None:
                continue
            builder = operator.add(builder)

        self._roll_result = builder.build()

    def _can_build_result(self) -> bool:
        return self._dice is not None and (failure.invalidates for failure in self._failures)


class DiceStringParserFactory:
    @staticmethod
    def create_parsed_dice_string(dice_string):
        factory = DiceStringParserFactory(dice_string)

        factory._extract()

    def __init__(self, dice_string):
        self._dice_string = dice_string
        self._builder = ParsedDiceStringBuilder.create_parsed_dice_string(dice_string)

    def _extract(self):
        self._extract_dice()
        self._extract_operators()

    def _extract_dice(self):
        extracted_special_dice = self._extract_reserved_dice()
        if extracted_special_dice:
            return

        self._extract_generic_dice()

    def _extract_reserved_dice(self) -> bool:
        if self._check_string_for_dice(_fate_regex):
            self._builder.with_fate_dice()
            return True

        storyteller_match = self._check_string_for_dice(_storyteller_regex)
        if storyteller_match:
            self._create_storyteller_dice(storyteller_match)
            return True

        return False

    def _check_string_for_dice(self, dice_regex: Pattern) -> Match:
        match = re.match(dice_regex, self._dice_string)

        return match

    def _create_storyteller_dice(self, storyteller_match: Match) -> None:
        number_of_dice = int(storyteller_match.group("number_of_dice"))
        self._builder.with_storyteller_dice(number_of_dice)
        self._builder.with_operators(OperatorFactory.get_storyteller_operators())

    def _extract_generic_dice(self):
        dice_match = re.match(_extract_dice_regex, self._dice_string)
        if not dice_match:
            self._builder.with_dice_failure()
            return

        number_of_dice = int(dice_match.group("number_of_dice")) if \
            "number_of_dice" in dice_match.groupdict().keys() \
            and dice_match.group("number_of_dice") != '' \
            else 1
        dice_size = int(dice_match.group("dice_size"))

        self._builder.with_dice(Dice(Die(dice_size), number_of_dice))

    def _extract_operators(self) -> None:
        operator_string = self._get_operator_string()
        if not operator_string:
            return
        self._builder.with_operators(OperatorFactory.get_operators(operator_string))

    def _get_operator_string(self):
        modifiers = re.split(_base_dice_regex, self._dice_string)
        return modifiers[1] if len(modifiers) > 1 else None
