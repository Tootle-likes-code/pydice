from abc import ABC
from dataclasses import dataclass

from pydice.roll_result import RollResultDecorator


class CounterRollResultDecorator(RollResultDecorator, ABC):
    """
    A dummy class for RollResultDecorator that identifies the class as one that should continue the
    count from the previous count, to facilitate counting chains.
    """


@dataclass
class CountValuesEqualToDecorator(CounterRollResultDecorator):
    """
    A decorator that counts all roll results of n.
    """
    target_number: int

    def result(self) -> int:
        """
        Counts the roll results that match the target number.  If the prior roll_result was a
        CounterRollResultDecorator, then it will add its count to that value.
        :return: The number of rolls that equal the target number.
        """
        count = sum(1 for roll in self.roll_result.die_rolls if roll == self.target_number)
        return self.roll_result.result() + count \
            if isinstance(self.roll_result, CounterRollResultDecorator) else count


@dataclass
class CountValuesGreaterThanDecorator(CounterRollResultDecorator):
    """
    A decorator that counts all roll results greater than n.
    """
    target_number: int

    def result(self) -> int:
        """
        Counts the roll results that are greater than the target number.
        If the prior roll_result was a CounterRollResultDecorator,
        then it will add its count to that value.
        :return: Then number of rolls that are greater than the target number.
        """
        count = sum(1 for roll in self.roll_result.die_rolls if roll > self.target_number)
        return self.roll_result.result() + count \
            if isinstance(self.roll_result, CounterRollResultDecorator) else count


@dataclass
class CountValuesLessThanDecorator(CounterRollResultDecorator):
    """
    A decorator that counts all roll results less than n.
    """
    target_number: int

    def result(self) -> int:
        count = sum(1 for roll in self.roll_result.die_rolls if roll < self.target_number)
        return self.roll_result.result() + count \
            if isinstance(self.roll_result, CounterRollResultDecorator) else count


@dataclass
class CountValuesNotEqualToDecorator(CounterRollResultDecorator):
    """
    A decorator that counts all roll results that do not equal n.
    """
    target_number: int

    def result(self) -> int:
        count = sum(1 for roll in self.roll_result.die_rolls if roll != self.target_number)
        return self.roll_result.result() + count \
            if isinstance(self.roll_result, CounterRollResultDecorator) else count
