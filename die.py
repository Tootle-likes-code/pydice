import random
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Rollable(ABC):
    @abstractmethod
    def roll(self) -> list[int]:
        pass

    @abstractmethod
    def min(self) -> int:
        pass

    @abstractmethod
    def max(self) -> int:
        pass


@dataclass
class Die(Rollable):
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


@dataclass(init=False)
class FateDie(Die):
    def __init__(self):
        super().__init__(3, -1)


@dataclass
class Dice(Rollable):
    die: Die
    number_of_dice: int

    def roll(self) -> list[int]:
        return [self.die.roll() for _ in range(self.number_of_dice)]

    @property
    def min(self):
        return self.die.min * self.number_of_dice

    @property
    def max(self):
        return self.die.max * self.number_of_dice


if __name__ == "__main" :
    print("Welcome to Tootle's Dice app.")

    number: int
    sides: int
    try:
        number = str(input("How many die you want to roll?"))
        sides = input("How many sides?")

        die: Die
        if sides.lower() == "f":
            die = FateDie()
        else:
            die = Die(str(sides))

        if number == 1:
            print(die.roll())
        else:
            dice = Dice(die, number)
            print(dice.roll())
    except ValueError:
        print("Wasn't given a number or f.  Sorry, can't do anything with that.")
