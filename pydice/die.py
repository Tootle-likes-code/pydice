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
        base_string = f"D{self.sides}"
        if self._minimum_roll == 1:
            return base_string

        return base_string + f"[{self._minimum_roll}-{self.max}]"


@dataclass(init=False)
class FateDie(Die):
    """
    A representation of a die use in FATE and it's variations.
    """

    def __init__(self):
        super().__init__(3, -1)

    def __str__(self):
        return f"Df"


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

    def __str__(self):
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
