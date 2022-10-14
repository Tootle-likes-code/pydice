from typing import Optional

from pydice.dice_string.dice_parser_failures import DiceParserFailure, InvalidOperator
from pydice.dice_string.dice_string_parser import ParsedDiceString
from pydice.dice_string.operators import Operator
from pydice.die import Dice
from pydice.roll_result import RollResult
from pydice.roll_result_operators.roll_result_builder import RollResultBuilder


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

    def with_operator(self, operator: Operator):
        self._operators.append(operator)
        return self

    def with_failure(self, failure: DiceParserFailure):
        self._failures.append(failure)
        return self

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
