from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from die import Die, Dice


@dataclass
class RollResult(ABC):
    @abstractmethod
    @property
    def die_rolls(self) -> list[int]:
        pass

    @abstractmethod
    def result(self) -> int:
        pass


@dataclass
class DieRollResult(RollResult):
    die: Die
    roll: int

    @property
    def die_rolls(self) -> list[int]:
        die_roll_as_list = [self.roll]
        return die_roll_as_list

    def result(self) -> int:
        return self.roll


@dataclass
class DiceRollResult(RollResult):
    dice: Dice
    rolls: list[DieRollResult] = field(init=False)

    @property
    def die_rolls(self) -> list[int]:
        die_roll_results = [result.roll for result in self.rolls]
        return die_roll_results

    def result(self) -> int:
        pass

    def add_roll(self, result: DieRollResult):
        self.rolls.append(result)

