"""
A collection of classes that can be used to decorate a RollResult class to transform
and modify the results of that RollResult.


Classes:
========
RollResultDecorator             - An abstract base class that defines the base decorator
                                  functionality.
AddToRollResultDecorator        - Adds a value to the RollResult.
SubtractFromRollResultDecorator - Subtracts a value from the RollResult.
MultipleRollResultDecorator     - Multiplies the RollResult by a value.
DivideByRollResultDecorator     - Divides the RollResult by a value.
ExplodeDiceForTargetDecorator   - When an individual die rolls the target number, it rolls
                                  another die, adding the die to the RollResult.
"""

from abc import ABC
from dataclasses import dataclass, field

from pydice.die import Die
from pydice.roll_result import RollResult


@dataclass
class RollResultDecorator(RollResult, ABC):
    """
    A abstract base class for sub-classing for Decorator Pattern purposes, but offering default
    properties for the subclasses to overwrite.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    roll_result: RollResult
    _result: int = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        self._result = self.roll_result.result

    @property
    def die_rolls(self) -> list[int]:
        """
        Returns the sorted RollResult.die_rolls.
        :return:
        """
        return sorted(self.roll_result.die_rolls)

    @property
    def result(self) -> int:
        """
        Returns the result of the RollResult.
        :return:
        """
        return self._result

    @property
    def rolled_die(self) -> Die:
        """
        Returns the RollResult.rolled_die
        :return:
        """
        return self.roll_result.rolled_die


@dataclass
class AddToRollResultDecorator(RollResultDecorator):
    """
    A decorator class that adds a number to the RollResult.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.
    modifier: int           - The number to be added to the RollResult.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls,
                              and the added modifier.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    modifier: int

    def __post_init__(self):
        self._result = self.roll_result.result + self.modifier


@dataclass
class SubtractFromRollResultDecorator(RollResultDecorator):
    """
    A decorator class that subtracts a number to the RollResult.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.
    modifier: int           - The number to be subtracted from the RollResult.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls,
                              and the added modifier.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    modifier: int

    def __post_init__(self):
        self._result = self.roll_result.result - self.modifier


@dataclass
class MultiplyRollResultDecorator(RollResultDecorator):
    """
    A decorator class that multiplies the RollResult by a number.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.
    multiplier: int         - The number to be multiply the RollResult by.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls,
                              and the added modifier.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    multiplier: int

    def __post_init__(self):
        self._result = round(self.roll_result.result * self.multiplier)


@dataclass
class DivideByRollResultDecorator(RollResultDecorator):
    """
    A decorator class that divides the RollResult by another number.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.
    divide_by: int          - The number to divide the RollResult by.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls,
                              and the added modifier.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    divide_by: int

    def __post_init__(self):
        self._result = round(self.roll_result.result / self.divide_by)


@dataclass
class ExplodeDiceForTargetDecorator(RollResultDecorator):
    """
    A decorator to cause rolls of n to be rolled again and added to the result.
    Values that have exploded are added where the exploded value appears.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.
    target_number: int      - The number that triggers the Die to reroll.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls,
                              and the added modifier.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    target_number: int

    def __post_init__(self):
        self._new_die_rolls: list[int] = []
        self._initialise_new_die_rolls()

        self._result = sum(self._new_die_rolls)

    def _initialise_new_die_rolls(self):
        for roll in self.roll_result.die_rolls:
            self._new_die_rolls.append(roll)
            if roll == self.target_number:
                self._explode()

    def _explode(self):
        new_value = self.roll_result.rolled_die.roll()[0]

        self._new_die_rolls.append(new_value)
        if new_value == self.target_number:
            self._explode()

    @property
    def die_rolls(self) -> list[int]:
        """ Returns the die rolls and any values that may have exploded. """
        return self._new_die_rolls
