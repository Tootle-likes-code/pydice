import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Rollable(ABC):
    @abstractmethod
    def roll(self) -> list[int]:
        pass

    @property
    def min(self) -> int:
        pass

    @property
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

