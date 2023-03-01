from abc import ABC
from dataclasses import dataclass, field

from pydice.die import Die
from pydice.roll_result import RollResult


@dataclass
class RollResultDecorator(RollResult, ABC):
    """
    A dummy class intended to be the base for decorator pattern.
    """
    roll_result: RollResult
    _result: int = field(init=False, repr=False)

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

