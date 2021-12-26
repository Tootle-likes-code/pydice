from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from die import Die, Dice


@dataclass
class RollResult(ABC):
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


@dataclass
class RollResultDecorator(RollResult):
    roll_result: RollResult

    def result(self) -> int:
        return self.decorated.result()


@dataclass
class AddToRollResultDecorator(RollResultDecorator):
    roll_result: RollResult
    modifier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return current_result + self.modifier


@dataclass
class SubtractFromRollResultDecorator(RollResultDecorator):
    roll_result: RollResult
    modifier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return current_result - self.modifier


class MultiplyRollResultDecorator(RollResultDecorator):
    roll_result: RollResult
    multiplier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return round(current_result * self.multiplier)


class DivideByRollResultDecorator(RollResultDecorator):
    roll_result: RollResult
    divide_by: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return round(current_result / self.divide_by)
