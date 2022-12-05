import re
from typing import Optional

from pydice.dice_string.dice_parser_failures import DiceParserFailure, InvalidDice, UnfinishedOperator
from pydice.dice_string.operators import Operator
from pydice.dice_string.parsed_dice_string import ParsedDiceString
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
        self._operators.extend(operators)
        return self

    def with_failure(self, failure: DiceParserFailure):
        self._failures.append(failure)
        return self

    def with_dice_failure(self):
        failure = InvalidDice(self._dice_string)
        return self.with_failure(failure)

    def with_unfinished_operator(self, unfinished_operator):
        failure = UnfinishedOperator(unfinished_operator)
        return self.with_failure(failure)

    def build(self) -> ParsedDiceString:
        self._build_roll_result()
        return ParsedDiceString(self._dice_string, self._failures, self._roll_result)

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