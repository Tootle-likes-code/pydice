import random
from dataclasses import dataclass


@dataclass
class RollResult:
    die: Die


@dataclass
class Die:
    sides: int
    minimum_roll: int = 1

    def roll(self):
        return random.randint(1, self.sides)

    @property
    def min(self):
        return self.minimum_roll

    @property
    def max(self):
        return self.sides
