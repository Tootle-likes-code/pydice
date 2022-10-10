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

    @property
    @abstractmethod
    def rolled_die(self) -> Die:
        """ Gets the die being used in this roll. """


@dataclass
class DieRollResult(RollResult):
    """
    The roll result for a single Die object.
    """
    die: Die
    roll: int | None = None

    def __post_init__(self):
        if self.roll is None:
            rolls = self.die.roll()
            self.roll = rolls
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

    @property
    def rolled_die(self) -> Die:
        return self.die


@dataclass
class DiceRollResult(RollResult):
    """
    The roll result for a Dice object.
    """
    dice: Dice
    _rolls: list[int] = field(default_factory=list)

    def __post_init__(self):
        if not self._rolls:
            self._rolls = self.dice.roll()

    @property
    def die_rolls(self) -> list[int]:
        return self._rolls

    def result(self) -> int:
        return sum(self._rolls)

    def add_die_roll(self, new_value: int):
        if not self.dice.min <= new_value <= self.dice.max:
            raise ValueError('Roll must be less than min and greater than max. '
                             f'Dice Min: {self.dice.min}, Dice Max: {self.dice.max}, '
                             f'value to add: {new_value}')
        self._rolls.append(new_value)

    @property
    def rolled_die(self) -> Die:
        return self.dice.die


