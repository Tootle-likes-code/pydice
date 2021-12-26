"""
This module handles the representation of individual die and handfuls of dice.
"""


import random
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Rollable(ABC):
    """
    An abstract representation of a die or dice.
    """
    @abstractmethod
    def roll(self) -> list[int]:
        """
        Randomly determines what the rolled value is on the Rollable.
        :return: A randomly generated number that is possible to roll on the Rollable.
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
    """
    sides: int
    minimum_roll: int = 1

    def __post_init__(self):
        offset = 1
        self._maximum_roll = self.sides + (self.min - offset)

    def roll(self) -> list[int]:
        die_roll_result = [random.randint(self.min, self._maximum_roll)]
        return die_roll_result

    @property
    def min(self) -> int:
        return self.minimum_roll

    @property
    def max(self) -> int:
        return self._maximum_roll

    def __str__(self) -> str:
        return f"D{self.sides}"


@dataclass(init=False)
class FateDie(Die):
    """
    A representation of a die use in FATE and it's variations.
    """
    def __init__(self):
        super().__init__(3, -1)


@dataclass
class Dice(Rollable):
    """
    A representation of multiple Die objects being used at once.
    """
    die: Die
    number_of_dice: int

    def roll(self) -> list[int]:
        return [self.die.roll()[0] for _ in range(self.number_of_dice)]

    @property
    def min(self):
        return self.die.min * self.number_of_dice

    @property
    def max(self):
        return self.die.max * self.number_of_dice


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
