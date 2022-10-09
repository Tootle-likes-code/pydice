from pydice.die import Dice
from pydice.roll_result import RollResult, DiceRollResult, AddToRollResultDecorator, SubtractFromRollResultDecorator, \
    CountValuesEqualToDecorator, MultiplyRollResultDecorator, \
    DivideByRollResultDecorator, ExplodeDiceForTargetDecorator, CountValuesGreaterThanDecorator, \
    CountValuesLessThanDecorator


class DiceResultBuilder:
    def __init__(self, dice: Dice):
        self._dice_result = DiceRollResult(dice)

    @staticmethod
    def create_dice_result_builder(dice: Dice):
        dice_result_builder = DiceResultBuilder(dice)
        return dice_result_builder

    def with_add_modifier(self, modifier):
        self._dice_result = AddToRollResultDecorator(self._dice_result, int(modifier))
        return self

    def with_subtract_modifier(self, modifier):
        self._dice_result = SubtractFromRollResultDecorator(self._dice_result, int(modifier))
        return self

    def with_multiply_modifier(self, modifier):
        self._dice_result = MultiplyRollResultDecorator(self._dice_result, int(modifier))
        return self

    def with_divide_modifier(self, modifier):
        self._dice_result = DivideByRollResultDecorator(self._dice_result, int(modifier))
        return self

    def with_exploding_modifier(self, modifier):
        self._dice_result = ExplodeDiceForTargetDecorator(self._dice_result, int(modifier))
        return self

    def with_count_values_equal_to(self, target_number):
        self._dice_result = CountValuesEqualToDecorator(self._dice_result, target_number)
        return self

    def with_count_values_greater_than(self, target_number):
        self._dice_result = CountValuesGreaterThanDecorator(self._dice_result, target_number)
        return self

    def with_count_values_greater_than_equal_to(self, target_number):
        self._dice_result = CountValuesGreaterThanDecorator(
            CountValuesEqualToDecorator(
                self._dice_result, target_number
            ), target_number
        )
        return self

    def with_count_values_less_than(self, target_number):
        self._dice_result = CountValuesLessThanDecorator(self._dice_result, target_number)
        return self

    def build(self) -> RollResult:
        return self._dice_result
