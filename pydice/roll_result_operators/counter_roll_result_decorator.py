"""
RollResultDecorators that count values from within the RollResult before.

They specifically will reset the result of the roll to the count.

Classes:
========
CounterRollResultDecorator      - An abstract class intended to facilitate counting chains.
CountValuesEqualToDecorator     - Counts all values that are equal to a given value.
CountValuesGreaterThanDecorator - Counts all values that are greater than a given value.
CountValuesLessThanDecorator    - Counts all values that are less than a given value.
CountValuesNotEqualToDecorator  - Counts all values that are not equal a particular value.
"""

from abc import ABC
from dataclasses import dataclass

from pydice.roll_result_operators.roll_result_decorators import RollResultDecorator


class CounterRollResultDecorator(RollResultDecorator, ABC):
    """
    A base class expanding on the RollResultDecorator, intending to be subclassed.

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


@dataclass
class CountValuesEqualToDecorator(CounterRollResultDecorator):
    """
    A decorator that counts all roll results of n.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.
    target_number: int      - The number that rolls have to be equal to, in order to be counted.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    target_number: int

    def __post_init__(self):
        count = sum(1 for roll in self.roll_result.die_rolls if roll == self.target_number)
        self._result = self.roll_result.result + count \
            if isinstance(self.roll_result, CounterRollResultDecorator) else count


@dataclass
class CountValuesGreaterThanDecorator(CounterRollResultDecorator):
    """
    A decorator that counts all roll results greater than n.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.
    target_number: int      - The number that rolls have to be greater than, in order to be counted.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    target_number: int

    def __post_init__(self):
        count = sum(1 for roll in self.roll_result.die_rolls if roll > self.target_number)
        self._result = self.roll_result.result + count \
            if isinstance(self.roll_result, CounterRollResultDecorator) else count


@dataclass
class CountValuesLessThanDecorator(CounterRollResultDecorator):
    """
    A decorator that counts all roll results greater than n.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.
    target_number: int      - The number that rolls have to be less than, in order to be counted.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    target_number: int

    def __post_init__(self):
        count = sum(1 for roll in self.roll_result.die_rolls if roll < self.target_number)
        self._result = self.roll_result.result + count \
            if isinstance(self.roll_result, CounterRollResultDecorator) else count


@dataclass
class CountValuesNotEqualToDecorator(CounterRollResultDecorator):
    """
    A decorator that counts all roll results not equal to n.

    Attributes:
    ===========
    roll_result: RollResult - The RollResult to decorate.
    target_number: int      - The number that rolls have to be not equal to, in order to be counted.

    Properties
    ==========
    die_rolls: list[int]    - A read-only property that retrieves the RollResult.die_rolls.
    result: int             - A read-only property that returns result of the rolls.
    rolled_die: Die         - A read-only property that returns the Die rolled
                              in the RollResult.
    """
    target_number: int

    def __post_init__(self):
        count = sum(1 for roll in self.roll_result.die_rolls if roll != self.target_number)
        self._result = self.roll_result.result + count \
            if isinstance(self.roll_result, CounterRollResultDecorator) else count
