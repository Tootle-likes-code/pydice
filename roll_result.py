"""
A module for collecting and handling the results of Rollable objects.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from die import Die, Dice


@dataclass
class RollResult(ABC):
    """
    Abstracted class for containing the results of a roll.
    """
    @property
    @abstractmethod
    def die_rolls(self) -> list[int]:
        """
        Returns a raw list of the raw Rollable Rolls in this object.
        :return:
        """

    @abstractmethod
    def result(self) -> int:
        """
        Returns the final calculated result for Rolling these rolls.
        :return:
        """


@dataclass
class DieRollResult(RollResult):
    """
    The roll result for a single Die object.
    """
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
    """
    The roll result for a Dice object.
    """
    dice: Dice
    rolls: list[DieRollResult] = field(default_factory=list)

    @property
    def die_rolls(self) -> list[int]:
        die_roll_results = [roll for roll in self.rolls]
        return die_roll_results

    def result(self) -> int:
        pass

    def add_roll(self, result: DieRollResult):
        """
        Adds a new DieRollResult to this object for use in calculations.
        :param result: The new DieRollResult to add.
        """
        self.rolls.append(result)


@dataclass
class RollResultDecorator(RollResult, ABC):
    """
    A dummy class intended to be the base for decorator pattern.
    """
    roll_result: RollResult

    @property
    def die_rolls(self) -> list[int]:
        return self.roll_result.die_rolls


@dataclass
class AddToRollResultDecorator(RollResultDecorator):
    """
    A decorator to add a modifier to the base result.
    """
    roll_result: RollResult
    modifier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return current_result + self.modifier


@dataclass
class SubtractFromRollResultDecorator(RollResultDecorator):
    """
    A decorator to subtract a modifier to the base result.
    """
    roll_result: RollResult
    modifier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return current_result - self.modifier


@dataclass
class MultiplyRollResultDecorator(RollResultDecorator):
    """
    A decorator to multiply the base result by a multiplier.
    """
    roll_result: RollResult
    multiplier: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return round(current_result * self.multiplier)


@dataclass
class DivideByRollResultDecorator(RollResultDecorator):
    """
    A decorator to divide the base result by a multiplier.
    """
    roll_result: RollResult
    divide_by: int

    def result(self) -> int:
        current_result = self.roll_result.result()
        return round(current_result / self.divide_by)
