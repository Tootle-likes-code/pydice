import random
from abc import ABC, abstractmethod
from dataclasses import dataclass


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

    def roll(self) -> list[int]:
        die_roll_result = [random.randint(self.min, self.sides)]
        return die_roll_result

    @property
    def min(self) -> int:
        return self.minimum_roll

    @property
    def max(self) -> int:
        return self.sides
