"""
A module for collecting and handling the results of Rollable objects.

Mutations can be added by sub-classing RollResultDecorator.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from pydice.die import Die, Dice


@dataclass
class RollResult(ABC):
    """
    Abstracted class for containing the results of a roll.
    """

    @property
    @abstractmethod
    def die_rolls(self) -> list[int]:
        """
        Returns a raw list of the raw Rollable Rolls in this object.
        :return:
        """

    @abstractmethod
    def result(self) -> int:
        """
        Returns the final calculated result for Rolling these rolls.
        :return:
        """

    @abstractmethod
    def add_die_roll(self, new_value: int) -> None:
        """ Adds a new result to the roll result."""


@dataclass
class DieRollResult(RollResult):
    """
    The roll result for a single Die object.
    """
    die: Die
    roll: int

    def __post_init__(self):
        self._rolls = [self.roll]

    @property
    def die_rolls(self) -> list[int]:
        die_roll_as_list = self._rolls
        return die_roll_as_list

    def result(self) -> int:
        return self.roll

    def add_die_roll(self, new_value: int) -> None:
        if not self.die.min <= new_value <= self.die.max:
            raise ValueError(f"Roll must be less than min and greater than max. "
                             f"Die Min: {self.die.min}, Die Max: {self.die.max}, "
                             f"value to add: {new_value}")
        self._rolls.append(new_value)


@dataclass
class DiceRollResult(RollResult):
    """
    The roll result for a Dice object.
    """
    dice: Dice
    rolls: list[int] = field(default_factory=list)

    @property
    def die_rolls(self) -> list[int]:
        return self.rolls

    def result(self) -> int:
        return sum(self.rolls)

    def add_die_roll(self, new_value: int):
        self.rolls.append(new_value)


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


@dataclass
class AddToRollResultDecorator(RollResultDecorator):
    """
    A decorator to add a modifier to the base result.
    """
    roll_result: RollResult
    modifier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return current_result + self.modifier


@dataclass
class SubtractFromRollResultDecorator(RollResultDecorator):
    """
    A decorator to subtract a modifier to the base result.
    """
    roll_result: RollResult
    modifier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return current_result - self.modifier


@dataclass
class MultiplyRollResultDecorator(RollResultDecorator):
    """
    A decorator to multiply the base result by a multiplier.
    """
    roll_result: RollResult
    multiplier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return round(current_result * self.multiplier)


@dataclass
class DivideByRollResultDecorator(RollResultDecorator):
    """
    A decorator to divide the base result by a multiplier.
    """
    roll_result: RollResult
    divide_by: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return round(current_result / self.divide_by)
