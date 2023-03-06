"""
This module handles the representation of individual die and handfuls of dice.

Classes:
========

Rollable    - The abstract base class for the dice abstractions.
Die         - The representation of a single die.
FateDie     - A representation of a Fate die.
Dice        - The representation of multiple Die.
"""

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Rollable(ABC):
    """
    An abstract representation of a die or dice.

    Properties:
    ===========
    min -> int
        The minimum result that the Rollable can produce.

    max -> int
        The maximum result that the Rollable can produce.

    Methods
    =======
    roll() -> list[int]
        Represents a single roll of the Rollable, producing a list of random numbers possible on the
        Rollable, with each value being a die result.
    """

    @abstractmethod
    def roll(self) -> list[int]:
        """
        Randomly determines what the rolled value is on the Rollable.
        :return: A list of randomly generated numbers, one for each die, that is possible to roll on
        the Rollable.
        """

    @property
    @abstractmethod
    def min(self) -> int:
        """
        The minimum value of the Rollable.
        :return:
        """

    @property
    @abstractmethod
    def max(self) -> int:
        """
        The maximum value of the Rollable.
        :return:
        """


@dataclass
class Die(Rollable):
    """
    The representation of a Polyhedral Die.  I.e. a die that starts with a number and then
    linearly increments for the number of sides.

    Attributes:
    ===========
    sides: int
        The number of sides the die has.
    minimum_roll: int = 1
        The starting value of the die object.

    Properties:
    ===========
    min -> int
        The returns the minimum_roll.

    max -> int
        The minimum roll plus the number of sides.

    Methods
    =======
    roll() -> list[int]
        Represents a single roll of the Die.
    """
    sides: int
    _minimum_roll: int = 1

    def roll(self) -> list[int]:
        """
        Returns a random roll of the die, between the min and max, placed into a list.
        The list will always have a len of 1.
        :return:
        """
        die_roll_result = [random.randint(self.min, self.max)]
        return die_roll_result

    @property
    def min(self) -> int:
        """
        Returns the minimum_roll of the die.
        :return:
        """
        return self._minimum_roll

    @property
    def max(self) -> int:
        """
        Returns the maximum value of the die, which is min + sides - 1.
        :return:
        """
        offset = 1
        return self.sides + (self.min - offset)

    def __str__(self) -> str:
        """
        Returns a string representation of the object using 'D{sides}' notation.
        :return:
        """
        base_string = f"D{self.sides}"
        if self._minimum_roll == 1:
            return base_string

        return base_string + f"[{self._minimum_roll}-{self.max}]"


@dataclass(init=False)
class FateDie(Die):
    """
    A representation of a die use in FATE and it's variations and a subclass of Die.

    Properties:
    ===========
    min -> int
        The returns the minimum_roll of -1.

    max -> int
        Returns the max value of 1.

    Methods
    =======
    roll() -> list[int]
        Represents a single roll of the FateDie.
    """

    def __init__(self):
        super().__init__(3, -1)

    def __str__(self):
        """
        Returns the string representation.
        :return: Df
        """
        return "Df"


@dataclass
class Dice(Rollable):
    """
    A representation of multiple Die objects being used at once.

    Attributes:
    ===========
    die: Die
        The Die type of this Dice.
    number_of_dice: int
        The number of dice that are rolled.

    Properties:
    ===========
    min -> int
        The minimum value the Dice can roll.
    max -> int
        The maximum value the Dice can roll.

    Methods:
    ========
    roll() -> list[int]:
        Rolls each die collecting the results together.
    """
    die: Die
    number_of_dice: int

    def roll(self) -> list[int]:
        """
        Rolls the Die for the number_of_dice and collates the results.
        :return: A list of numbers between min and max with a len of number_of_dice.
        """
        return [self.die.roll()[0] for _ in range(self.number_of_dice)]

    @property
    def min(self) -> int:
        """
        The minimum value the Dice object could roll.  I.e. The die.min * number_of_dice.
        :return:
        """
        return self.die.min * self.number_of_dice

    @property
    def max(self):
        """
        The maximum value the Dice object could roll.  I.e. The die.max * number_of_dice.
        :return:
        """
        return self.die.max * self.number_of_dice

    def __str__(self):
        """
        A string representation of the Dice using '{number_of_dice}{str(die)}'.
        See Die.__str__ for details.
        :return:
        """
        return f"{self.number_of_dice}{str(self.die)}"


if __name__ == "__main__":
    print("Welcome to Tootle's Dice app.")

    try:
        number = int(input("How many die you want to roll?\n"))
        sides = input("How many sides?\n")

        die: Die
        if sides.lower() == "f":
            die = FateDie()
        else:
            die = Die(int(sides))

        if number == 1:
            print(die.roll())
        else:
            dice = Dice(die, number)
            print(dice.roll())
    except ValueError:
        print("Wasn't given a number or f.  Sorry, can't do anything with that.")
