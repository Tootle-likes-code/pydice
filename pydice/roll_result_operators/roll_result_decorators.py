from abc import ABC
from dataclasses import dataclass

from pydice.die import Die
from pydice.roll_result import RollResult


@dataclass
class RollResultDecorator(RollResult, ABC):
    """
    A dummy class intended to be the base for decorator pattern.
    """
    roll_result: RollResult

    @property
    def die_rolls(self) -> list[int]:
        return self.roll_result.die_rolls

    def add_die_roll(self, new_value: int) -> None:
        self.roll_result.add_die_roll(new_value)

    @property
    def rolled_die(self) -> Die:
        return self.roll_result.rolled_die


@dataclass
class AddToRollResultDecorator(RollResultDecorator):
    """
    A decorator to add a modifier to the base result.
    """
    modifier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return current_result + self.modifier


@dataclass
class SubtractFromRollResultDecorator(RollResultDecorator):
    """
    A decorator to subtract a modifier to the base result.
    """
    modifier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return current_result - self.modifier


@dataclass
class MultiplyRollResultDecorator(RollResultDecorator):
    """
    A decorator to multiply the base result by a multiplier.
    """
    multiplier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return round(current_result * self.multiplier)


@dataclass
class DivideByRollResultDecorator(RollResultDecorator):
    """
    A decorator to divide the base result by a multiplier.
    """
    divide_by: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return round(current_result / self.divide_by)


@dataclass
class ExplodeDiceForTargetDecorator(RollResultDecorator):
    """
    A decorator to cause rolls of n to be rolled again and added to the result.
    """
    target_number: int

    def __post_init__(self):
        self._rolled_results: list[int] = []

    def result(self) -> int:
        if len(self._rolled_results) > 0:
            return sum(i for i in self._rolled_results)

        for i in self.roll_result.die_rolls:
            self._rolled_results.append(i)

            if i == self.target_number:
                self._explode()

        return sum(i for i in self._rolled_results)

    def _explode(self):
        new_value = self.roll_result.rolled_die.roll()

        self._rolled_results.append(new_value)
        if new_value == self.target_number:
            self._explode()
