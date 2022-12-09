from dataclasses import dataclass
from typing import Optional

from pydice.dice_string.dice_parser_failures import DiceParserFailure, Severity
from pydice.roll_result import RollResult


@dataclass
class ParsedDiceString:
    dice_string: str
    _failures: list[DiceParserFailure]
    roll_result: Optional[RollResult]

    @property
    def is_valid(self) -> bool:
        return Severity.ERROR not in [failure.severity for failure in self._failures] and self.roll_result is not None

    @property
    def failures(self) -> str:
        return ','.join([failure.reason for failure in self._failures])

