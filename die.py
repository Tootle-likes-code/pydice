import random
from abc import ABC, abstractmethod
from dataclasses import dataclass

from roll_result import RollResult


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

    def roll(self) -> RollResult:
        roll_result = RollResult(self, random.randint(self.min, self.sides))
        return roll_result

    @property
    def min(self) -> int:
        return self.minimum_roll

    @property
    def max(self) -> int:
        return self.sides
