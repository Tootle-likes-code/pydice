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

    @property
    @abstractmethod
    def result(self) -> int:
        """
        Returns the final calculated result for Rolling these rolls.
        :return:
        """

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
            self.roll = rolls[0]
        self._rolls = [self.roll]

    @property
    def die_rolls(self) -> list[int]:
        die_roll_as_list = self._rolls
        return die_roll_as_list

    @property
    def result(self) -> int:
        return self.roll

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

    @property
    def result(self) -> int:
        return sum(self._rolls)

    @property
    def rolled_die(self) -> Die:
        return self.dice.die
