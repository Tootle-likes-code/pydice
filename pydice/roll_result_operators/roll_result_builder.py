"""
A module containing a builder allowing for the construction of a RollResults.

Classes:
========
RollResultBuilder - A builder pattern for RollResults and
                    their various RollResultDecorators.
"""

from pydice.die import Dice
from pydice.roll_result import RollResult, DiceRollResult
from pydice.roll_result_operators.counter_roll_result_decorator import\
    CountValuesEqualToDecorator, \
    CountValuesGreaterThanDecorator, \
    CountValuesLessThanDecorator, \
    CountValuesNotEqualToDecorator
from pydice.roll_result_operators.drop_dice_roll_result_decorators import\
    DropHighestDecorator,\
    DropLowestDecorator
from pydice.roll_result_operators.roll_result_decorators import\
    AddToRollResultDecorator, \
    SubtractFromRollResultDecorator, \
    MultiplyRollResultDecorator, \
    DivideByRollResultDecorator, \
    ExplodeDiceForTargetDecorator


class RollResultBuilder:
    """
    A builder pattern for RollResults and RollResultDecorators.

    Class Methods:
    ==============
    create_roll_result_builder(dice: Dice) -> RollResultBuilder
        Creates a new RollResultBuilder instance for fluent use.

    Methods:
    ========
    with_add_modifier(modifier: int
    """
    def __init__(self, dice: Dice):
        """
        Creates a new RolLResultBuilder.
        :param dice: The Dice to be rolled in the new RollResult.
        """
        self._dice_result = DiceRollResult(dice)

    @staticmethod
    def create_roll_result_builder(dice: Dice) -> 'RollResultBuilder':
        """
        Creates a new RollResultsBuilder object to allow the class to be called and
        the whole build to be done fluently.
        :param dice: The dice to create the RollResultBuilder with.
        :return: A new RollResultBuilder.
        """
        dice_result_builder = RollResultBuilder(dice)
        return dice_result_builder

    def with_add_modifier(self, modifier: int) -> 'RollResultBuilder':
        """
        Adds an AddToRollResultDecorator to the built Result.
        :param modifier: The value to add.
        :return: The RollResultBuilder.
        """
        self._dice_result = AddToRollResultDecorator(self._dice_result, modifier)
        return self

    def with_subtract_modifier(self, modifier: int) -> 'RollResultBuilder':
        """
        Adds an SubtractFromRollResultDecorator to the built Result.
        :param modifier: The value to subtract.
        :return: The RollResultBuilder.
        """
        self._dice_result = SubtractFromRollResultDecorator(self._dice_result, modifier)
        return self

    def with_multiply_modifier(self, modifier: int) -> 'RollResultBuilder':
        """
        Adds an MultiplyRollResultDecorator to the built Result.
        :param modifier: The value to multiply by.
        :return: The RollResultBuilder.
        """
        self._dice_result = MultiplyRollResultDecorator(self._dice_result, modifier)
        return self

    def with_divide_modifier(self, modifier) -> 'RollResultBuilder':
        """
        Adds an DivideByRollResultDecorator to the built Result.
        :param modifier: The value to divide by.
        :return: The RollResultBuilder.
        """
        self._dice_result = DivideByRollResultDecorator(self._dice_result, modifier)
        return self

    def with_exploding_modifier(self, target_number) -> 'RollResultBuilder':
        """
        Adds an ExplodeDiceForTargetDecorator to the built Result.
        :param target_number: The number that will trigger the die to explode.
        :return: The RollResultBuilder.
        """
        self._dice_result = ExplodeDiceForTargetDecorator(self._dice_result, target_number)
        return self

    def with_count_values_equal_to(self, target_number) -> 'RollResultBuilder':
        """
        Adds a CountValuesEqualToDecorator to the built Result.
        :param target_number: The number to test equality against.
        :return: The RollResultBuilder.
        """
        self._dice_result = CountValuesEqualToDecorator(self._dice_result, target_number)
        return self

    def with_count_values_greater_than(self, target_number) -> 'RollResultBuilder':
        """
        Adds a CountValuesGreaterThanDecorator to the built Result.
        :param target_number: The number to test die results are greater than against.
        :return: The RollResultBuilder.
        """
        self._dice_result = CountValuesGreaterThanDecorator(self._dice_result, target_number)
        return self

    def with_count_values_greater_than_equal_to(self, target_number) -> 'RollResultBuilder':
        """
        Adds a CountValuesGreaterThanDecorator and CountValuesEqualToDecorator to the built Result.
        :param target_number: The number to test die results against.
        :return: The RollResultBuilder.
        """
        return self.with_count_values_equal_to(target_number)\
            .with_count_values_greater_than(target_number)

    def with_count_values_less_than(self, target_number) -> 'RollResultBuilder':
        """
        Adds a CountValuesLessThanDecorator to the built Result.
        :param target_number: The number to test die results against.
        :return: The RollResultBuilder.
        """
        self._dice_result = CountValuesLessThanDecorator(self._dice_result, target_number)
        return self

    def with_count_values_less_than_equal_to(self, target_number) -> 'RollResultBuilder':
        """
        Adds a CountValuesLessThanDecorator and CountValuesEqualToDecorator to the built Result.
        :param target_number: The number to test die results against.
        :return: The RollResultBuilder.
        """
        return self.with_count_values_equal_to(target_number)\
            .with_count_values_less_than(target_number)

    def with_not_equals_to(self, target_number) -> 'RollResultBuilder':
        """
        Adds a CountValuesNotEqualToDecorator and CountValuesEqualToDecorator to the built Result.
        :param target_number: The number to test die results against.
        :return: The RollResultBuilder.
        """
        self._dice_result = CountValuesNotEqualToDecorator(self._dice_result, target_number)
        return self

    def with_drop_highest(self, number_to_drop: int) -> 'RollResultBuilder':
        """
        Adds a DropHighestDecorator to the built Result.
        :param number_to_drop: The number of dice to drop.
        :return: The RollResultBuilder.
        """
        self._dice_result = DropHighestDecorator(self._dice_result, number_to_drop)
        return self

    def with_drop_lowest(self, number_to_drop: int) -> 'RollResultBuilder':
        """
        Adds a DropLowestDecorator to the built Result.
        :param number_to_drop: The number of dice to drop.
        :return: The RollResultBuilder.
        """
        self._dice_result = DropLowestDecorator(self._dice_result, number_to_drop)
        return self

    def build(self) -> RollResult:
        """
        Finally builds the RollResult and it's decorators.
        :return: The RollResult that was constructed by this builder.
        """
        return self._dice_result
