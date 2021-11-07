import random
from dataclasses import dataclass

from roll_result import RollResult


@dataclass
class Die:
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
