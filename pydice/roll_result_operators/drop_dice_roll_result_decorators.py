"""
This module contains further RollResultDecorators, focusing upon dropping
dice from the RollResult.

Classes:
========
DropDiceDecorator       - The Base Class that expands upon the RollResultDecorator.
DropLowestDecorator     - Drops a number of the lowest rolled from the RollResult.
DropHighestDecorator    - Drops a number of the highest rolled from the RollResult.
"""
from abc import ABC
from dataclasses import dataclass
from typing import ClassVar

from pydice.roll_result_operators.roll_result_decorators import RollResultDecorator


@dataclass
class DropDiceDecorator(RollResultDecorator, ABC):
    """
    An abstract base class for RollResultDecorators that defines decorators that drops
    a number of results from the RollResult.

    Class Attributes:
    =================
    minimum_drop: int       - The minimum number of die allowed to be dropped.  Any less
                              than this number will fail.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls,
                              and the added modifier.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    minimum_drop: ClassVar[int] = 1

    @property
    def result(self) -> int:
        """ Returns the sum of the die rolls. """
        return sum(self.die_rolls)


@dataclass
class DropLowestDecorator(DropDiceDecorator):
    """
    A decorator that drops a number of the lowest results from the RollResult.

    Class Attributes:
    =================
    minimum_drop: int       - The minimum number of die allowed to be dropped.  Any less
                              than this number will fail.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.
    number_to_drop: int     - The number of dice to drop.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls,
                              and the added modifier.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    number_to_drop: int = 1

    def __post_init__(self):
        if self.number_to_drop < self.minimum_drop:
            raise ValueError(f"Cannot drop less than {self.minimum_drop}.  "
                             f"Attempted to drop {self.number_to_drop}")

    @property
    def die_rolls(self) -> list[int]:
        """ Returns the newly reduced list of die values. """
        return sorted(self.roll_result.die_rolls)[self.number_to_drop:]


@dataclass
class DropHighestDecorator(DropDiceDecorator):
    """
    A decorator that drops a number of the highest results from the RollResult.

    Class Attributes:
    =================
    minimum_drop: int       - The minimum number of die allowed to be dropped.  Any less
                              than this number will fail.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.
    number_to_drop: int     - The number of dice to drop.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls,
                              and the added modifier.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    number_to_drop: int = 1

    def __post_init__(self):
        if self.number_to_drop < self.minimum_drop:
            raise ValueError(f"Cannot drop less than {self.minimum_drop}.  Attempted "
                             f"to drop {self.number_to_drop}")

    @property
    def die_rolls(self) -> list[int]:
        """ Returns the newly reduced list of die values. """
        dice_to_drop = self.number_to_drop * -1
        return sorted(self.roll_result.die_rolls)[:dice_to_drop]
