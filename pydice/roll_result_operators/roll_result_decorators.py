from abc import ABC
from dataclasses import dataclass, field
from typing import ClassVar

from pydice.die import Die
from pydice.roll_result import RollResult


@dataclass
class RollResultDecorator(RollResult, ABC):
    """
    A dummy class intended to be the base for decorator pattern.
    """
    roll_result: RollResult
    _result: int = field(init=False, repr=False, compare=False)

    @property
    def die_rolls(self) -> list[int]:
        return sorted(self.roll_result.die_rolls)

    def add_die_roll(self, new_value: int) -> None:
        self.roll_result.add_die_roll(new_value)

    @property
    def result(self) -> int:
        return self._result

    @property
    def rolled_die(self) -> Die:
        return self.roll_result.rolled_die


@dataclass
class AddToRollResultDecorator(RollResultDecorator):
    """
    A decorator to add a modifier to the base result.
    """
    modifier: int

    def __post_init__(self):
        self._result = self.roll_result.result + self.modifier


@dataclass
class SubtractFromRollResultDecorator(RollResultDecorator):
    """
    A decorator to subtract a modifier to the base result.
    """
    modifier: int

    def __post_init__(self):
        self._result = self.roll_result.result - self.modifier


@dataclass
class MultiplyRollResultDecorator(RollResultDecorator):
    """
    A decorator to multiply the base result by a multiplier.
    """
    multiplier: int

    def __post_init__(self):
        self._result = round(self.roll_result.result * self.multiplier)


@dataclass
class DivideByRollResultDecorator(RollResultDecorator):
    """
    A decorator to divide the base result by a multiplier.
    """
    divide_by: int

    def __post_init__(self):
        self._result = round(self.roll_result.result / self.divide_by)


@dataclass
class ExplodeDiceForTargetDecorator(RollResultDecorator):
    """
    A decorator to cause rolls of n to be rolled again and added to the result.
    Values that have exploded are added where the exploded value appears.
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
        return self._new_die_rolls


@dataclass
class DropDiceDecorator(RollResultDecorator, ABC):
    """
    Root Class for all attempts to drop dice.
    """
    minimum_drop: ClassVar[int] = 1

    @property
    def result(self) -> int:
        return sum(self.die_rolls)


@dataclass
class DropLowestDecorator(DropDiceDecorator):
    """
    A decorator that reduces the number of dice results by a specified number, keeping only
    the highest values.
    """
    number_to_drop: int = 1

    def __post_init__(self):
        if self.number_to_drop < self.minimum_drop:
            raise ValueError(f"Cannot drop less than {self.minimum_drop}.  Attempted to drop {self.number_to_drop}")

    @property
    def die_rolls(self) -> list[int]:
        return sorted(self.roll_result.die_rolls)[self.number_to_drop:]

@dataclass
class DropHighestDecorator(DropDiceDecorator):
    """
    A decorator that reduces the number of die rolled by a specified number, keeping only the lowest values.
    """
    number_to_drop: int = 1
    minimum_drop: ClassVar[int] = 1

    def __post_init__(self):
        if self.number_to_drop < self.minimum_drop:
            raise ValueError(f"Cannot drop less than {self.minimum_drop}.  Attempted to drop {self.number_to_drop}")

    @property
    def die_rolls(self) -> list[int]:
        dice_to_drop = self.number_to_drop * -1
        return sorted(self.roll_result.die_rolls)[:dice_to_drop]
