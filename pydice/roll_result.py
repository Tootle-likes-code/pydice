"""
This module handles a snapshot of a Rollable.roll in the various forms.

Classes:
========

RollResult - The Base class for all RollResult objects.
DieRollResult - A class for handling a single Die class as a RollResult.
DiceRollResult - A class for handling a Dice class as a RollResult.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydice.die import Die, Dice


@dataclass
class RollResult(ABC):
    """
    Abstract base class for containing the results of a roll, intended to be overriden
    by subclasses.

    Properties:
    ===========
    die_rolls -> list[int]  - A read-only property. Returns a list of the rolled values.
    result -> int           - A read-only property. The result of the Rollable.
    rolled_die -> Die       - A read-only property. Returns the Die used in the RollResult.
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
    A representation of an individual Die roll.  As such all attributes are hidden and only
    exposed by read-only properties.

    This object can be used to create the initial roll it represents as well by not providing
    the roll result.

    Properties:
    ===========
    die -> Die              - A read-only property. Returns the Die that this object is used for.
    die_rolls -> list[int]  - A read-only property. Returns a list of the rolled values.
    result -> int           - A read-only property. The result of the Rollable.
    rolled_die -> Die       - A read-only property. Returns the Die used in the RollResult.
    """

    def __init__(self, die: Die, roll: int | None = None):
        """
        Creates a DieRollResult.  If no roll value is provided, then the Die.roll() is called
        to initialise this class.

        :param die: The Die rolled.
        :param roll: The result of that die.
        """
        self._die: Die = die
        if roll is None:
            self._roll = self.die.roll()[0]
        else:
            self._roll = roll

    @property
    def die(self) -> Die:
        """ Returns the Die used to create the object. """
        return self._die

    @property
    def die_rolls(self) -> list[int]:
        """ Returns the roll value in a list. """
        die_roll_as_list = [self._roll]
        return die_roll_as_list

    @property
    def result(self) -> int:
        """ Returns the roll of the die this time. """
        return self._roll

    @property
    def rolled_die(self) -> Die:
        """ Returns the Die being rolled. """
        return self.die


@dataclass
class DiceRollResult(RollResult):
    """
    A representation of an individual Dice roll.  As such all attributes are hidden and only
    exposed by read-only properties.

    This object can be used to create the initial roll it represents as well by not providing
    the roll result.

    Properties:
    ===========
    dice -> Dice            - A read-only property. Returns the DiCe that this object is used for.
    die_rolls -> list[int]  - A read-only property. Returns a list of the rolled values.
    result -> int           - A read-only property. The result of the Rollable.
    rolled_die -> Die       - A read-only property. Returns the Die used in the given Dice.
    """

    def __init__(self, dice: Dice, rolls: list[int] | None = None):
        """
        Creates a DiceRollResult.  If no rolls are provided, then the dice provided will be rolled
        to trigger them.
        :param dice: The Dice that were rolled for this RollResult.
        :param rolls: The results of those dice.
        """
        self._dice = dice
        if rolls:
            self._rolls = rolls
        else:
            self._rolls = self._dice.roll()

    @property
    def dice(self) -> Dice:
        """ Returns the Dice used in this RollResult. """
        return self._dice

    @property
    def die_rolls(self) -> list[int]:
        """ Returns the roll value in a list. """
        return self._rolls

    @property
    def result(self) -> int:
        """ Returns the roll of the die this time. """
        return sum(self._rolls)

    @property
    def rolled_die(self) -> Die:
        """ Returns the Die being rolled. """
        return self._dice.die
