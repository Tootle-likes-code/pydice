from pydice.die import Dice
from pydice.roll_result import RollResult, DiceRollResult, AddToRollResultDecorator


class DiceResultBuilder:
    def __init__(self, dice: Dice):
        self._dice = DiceRollResult(dice)

    @staticmethod
    def create_dice_result_builder(dice):
        dice_result_builder = DiceResultBuilder(dice)
        return dice_result_builder

    def with_add_modifier(self, modifier):
        self._dice = AddToRollResultDecorator(self._dice, modifier)
        return self

    def build(self) -> RollResult:
        return self._dice
