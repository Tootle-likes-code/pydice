from abc import ABC, abstractmethod

from pydice.die import Dice, FateDie
from pydice.roll_result import RollResult, DiceRollResult, AddToRollResultDecorator


class DiceResultBuilder:
    def __init__(self, dice: Dice):
        self._dice_result = DiceRollResult(dice)

    @staticmethod
    def create_dice_result_builder(dice):
        dice_result_builder = DiceResultBuilder(dice)
        return dice_result_builder

    def with_add_modifier(self, modifier):
        self._dice_result = AddToRollResultDecorator(self._dice_result, int(modifier))
        return self

    def build(self) -> RollResult:
        return self._dice_result


class FateDiceResultBuilder:
    fate_dice = Dice(FateDie(), 4)

    def __init__(self):
        self._dice_result = DiceRollResult(self.fate_dice)

    @staticmethod
    def create_fate_dice_result_builder():
        fate_dice_result_builder = FateDiceResultBuilder()
        return fate_dice_result_builder

    def with_add_modifier(self, modifier):
        self._dice_result = AddToRollResultDecorator(self._dice_result, int(modifier))

    def build(self) -> RollResult:
        return self._dice_result
