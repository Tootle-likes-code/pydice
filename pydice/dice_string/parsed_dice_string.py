"""
A module for containing dice strings that have been converted into
a pydice format for use.

Classes:
========
ParsedDiceString - A class that represents a dice string in pydice terms.
"""

from dataclasses import dataclass
from typing import Optional

from pydice.dice_string.dice_parser_failures import DiceParserFailure, Severity
from pydice.roll_result import RollResult


@dataclass
class ParsedDiceString:
    """
    A representation of a Dice String whilst also creating a RollResult.

    Attributes:
    ===========
    dice_string: str - The dice string that this ParsedDiceString represents.
    roll_result: Optional[RollResult] - The generated RollResult, if a valid one could be created.

    Properties:
    ===========
    is_valid -> bool - Returns if the ParsedDiceString was valid.
    failures -> str - Returns the failures from parsing the Dice string as a comma seperated list.
    """
    dice_string: str
    _failures: list[DiceParserFailure]
    roll_result: Optional[RollResult]

    @property
    def is_valid(self) -> bool:
        """
        Returns if the ParsedDiceString is valid.
        :return:
        """
        return Severity.ERROR not in [failure.severity for failure in self._failures] \
            and self.roll_result is not None

    @property
    def failures(self) -> str:
        """
        Returns the failures that occurred in the creation of this ParsedDiceString, with each error
        being separated by a comma.
        :return:
        """
        return ','.join([failure.reason for failure in self._failures])
