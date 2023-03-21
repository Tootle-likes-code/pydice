"""
This Module contains knowledge on all of the Dice String operators and how they
are applied in terms of RollResultBuilders.

Classes:
========

Operator                    - The base class for all of the actual operators.
AddOperator                 - An Operator for handling Addition operations.
SubtractOperator            - An Operator for handling Subtraction operations.
MultiplyOperator            - An Operator for handling Multiplication operations.
DivideOperator              - An Operator for handling Division operations.
ExplodingOperator           - An Operator for handling Exploding dice.
EqualToOperator             - An Operator for comparing is die rolls are equal to another value.
NotEqualToOperator          - An Operator for comparing is die rolls are not equal to another value.
EqualToOperator             - An Operator for comparing is die rolls are equal to another value.
EqualToOperator             - An Operator for comparing is die rolls are equal to another value.
GreaterThanOperator         - An Operator for comparing is die rolls are greater than another value.
GreaterThanEqualToOperator  - An Operator for comparing is die rolls are greater than
                                or equal to another value.
LessThanOperator            - An Operator for comparing is die rolls are less than another value.
LessThanEqualToOperator     - An Operator for comparing is die rolls are less than
                                or equal to another value.
DropHighestOperator         - An Operator for handling the removal of the highest n rolls.
DropLowestOperator          - An Operator for handling the removal of the lowest n rolls.

Variables:
==========
ACCEPTED_OPERATORS: dict[str, Operator]
    Contains the lowercase dice string mapping to an operator class for that dice string.

Functions:
==========
get_operator(operator: str, value: int) -> Operator
    Takes a dice string for an operator and returns an Operator for it loaded with the value.
get_storyteller_operators() -> list[Operator]
    Returns the Operators required for the Storyteller systems.
"""

# pylint: disable=too-few-public-methods

from abc import abstractmethod, ABC
from dataclasses import dataclass

from pydice.roll_result_operators.roll_result_builder import RollResultBuilder


@dataclass
class Operator(ABC):
    """
    Instructions on how to add this Operation to the RollResult via the
    RollResultBuilder for this particular operation.

    Attributes:
    ===========
    value: int
        The number associated with the Operator.

    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct method to add the steps
        required for this Operation.
    """
    value: int

    @abstractmethod
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to add the
        steps required for this Operation.
        :param builder: The builder to be operated on.
        :return: The updated builder.
        """

class AddOperator(Operator):
    """
    Instructions on how to add a number to the RollResult via the RollResultBuilder.

    Attributes:
    ===========
    value: int
        The number to add.

    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct methods to add a value to the RollResult.
    """

    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to add a value to the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_add_modifier(self.value)


class SubtractOperator(Operator):
    """
    Instructions on how to subtract a number to the RollResult via the RollResultBuilder.

    Attributes:
    ===========
    value: int
        The number to subtract.

    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct methods to subtract
        a value to the RollResult.
    """

    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to subtract a value
        to the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_subtract_modifier(self.value)


class MultiplyOperator(Operator):
    """Instructions on how to multiply a number to the RollResult via the RollResultBuilder.

    Attributes:
    ===========
    value: int
        The number to multiply by.

    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct methods to multiply by a value
        to the RollResult.
    """

    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to multiply by a value
        to the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_multiply_modifier(self.value)


class DivideOperator(Operator):
    """
    Instructions on how to divide by a number to the RollResult via the RollResultBuilder.

    Attributes:
    ===========
    value: int
        The number to divide by.
    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct methods to divide by a value
        to the RollResult.
    """

    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to divide by a value
        to the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_divide_modifier(self.value)


class ExplodingOperator(Operator):
    """
    Instructions on how to explode die equal to the value to the RollResult via the
    RollResultBuilder.

    Attributes:
    ===========
    value: int
        The number to which triggers dice to explode.

    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct methods to explode dice based on
        a value to the RollResult.
    """

    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to explode dice based on
         a value to the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_exploding_modifier(self.value)


class EqualToOperator(Operator):
    """
    Instructions on how to check if a number is equal to a value to the RollResult
    via the RollResultBuilder.

    Attributes:
    ===========
    value: int
        The number to check it is equal to.
    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct methods to check if a result is equal to
        a value to the RollResult.
    """

    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to check if a result is equal to
        a value to the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_count_values_equal_to(self.value)


class NotEqualToOperator(Operator):
    """
        Instructions on how to check if a number is not equal to a value to the RollResult
        via the RollResultBuilder.

        Attributes:
        ===========
        value: int
            The number to check it is not equal to.
        Methods:
        ========
        add(builder: RollResultBuilder) -> RollResultBuilder
            This method calls the builder with the correct methods to check if a
            result is not equal to a value to the RollResult.
        """
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to check if a result is not equal
        to a value to the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_not_equals_to(self.value)


class GreaterThanOperator(Operator):
    """
        Instructions on how to check if a number is greater than a value to the RollResult
        via the RollResultBuilder.

        Attributes:
        ===========
        value: int
            The number to check it is greater than.
        Methods:
        ========
        add(builder: RollResultBuilder) -> RollResultBuilder
            This method calls the builder with the correct methods to check if a result is
            greater than a value to the RollResult.
        """
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to check if a result is
        greater than a value to the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_count_values_greater_than(self.value)


class GreaterThanEqualToOperator(Operator):
    """
    Instructions on how to check if a number is greater than or equal to a value to
    the RollResult via the RollResultBuilder.

    Attributes:
    ===========
    value: int
        The number to check it is greater than or equal to.

    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct methods to check if a result is
        greater than orequal to a value to the RollResult.
    """
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to check if a result is
        greater than or equal to a value to the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_count_values_greater_than_equal_to(self.value)


class LessThanOperator(Operator):
    """
    Instructions on how to check if a number is less than a value to the RollResult
    via the RollResultBuilder.

    Attributes:
    ===========
    value: int
        The number to check it is less than.

    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct methods to check if a result is less than
        a value to the RollResult.
    """
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to check if a result is less than
        a value to the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_count_values_less_than(self.value)


class LessThanEqualToOperator(Operator):
    """
    Instructions on how to check if a number is less than or equal to a value to the RollResult
    via the RollResultBuilder.

    Attributes:
    ===========
    value: int
        The number to check it is less than or equal to.

    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct methods to check if a result is
        less than or equal to a value to the RollResult.
    """
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to check if a result is
        less than or equal to a value to the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_count_values_less_than_equal_to(self.value)


class DropHighestOperator(Operator):
    """
    Instructions on how to drop the highest x dice from the RollResult
    via the RollResultBuilder.

    Attributes:
    ===========
    value: int
        The number of dice to drop.

    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct methods to drop the highest x dice
        from the RollResult.
    """
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to drop the highest x dice
        from the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_drop_highest(self.value)


class DropLowestOperator(Operator):
    """
    Instructions on how to drop the lowest x dice from the RollResult
    via the RollResultBuilder.

    Attributes:
    ===========
    value: int
        The number of dice to drop.

    Methods:
    ========
    add(builder: RollResultBuilder) -> RollResultBuilder
        This method calls the builder with the correct methods to drop the lowest x dice
        from the RollResult.
    """
    def add(self, builder: RollResultBuilder) -> RollResultBuilder:
        """
        This method calls the builder with the correct methods to drop the lowest x dice
        from the RollResult.
        :param builder: The builder to add the operation to.
        :return: The updated builder.
        """
        return builder.with_drop_lowest(self.value)


ACCEPTED_OPERATORS: dict[str, type] = {
    "+": AddOperator,
    "-": SubtractOperator,
    "*": MultiplyOperator,
    "x": MultiplyOperator,
    "/": DivideOperator,
    "=": EqualToOperator,
    "!=": NotEqualToOperator,
    "=/=": NotEqualToOperator,
    ">": GreaterThanOperator,
    ">=": GreaterThanEqualToOperator,
    "<": LessThanOperator,
    "<=": LessThanEqualToOperator,
    "e": ExplodingOperator,
    "dh": DropHighestOperator,
    "dl": DropLowestOperator
}


def get_operator(operator: str, value: int) -> Operator | None:
    """
    Checks if the operator exists.  If it will return an intialised Operator.
    :param operator: The dice string representation of an Operator.
    :param value:  The value for the Operator.
    :return: If the operator doesn't exist, None.  Otherwise the correct Operator for the
    dice string initialised with the value.
    """
    if operator.lower() not in ACCEPTED_OPERATORS:
        return None

    return ACCEPTED_OPERATORS[operator.lower()](value)


def get_storyteller_operators() -> list[Operator]:
    """
    Returns a list of Operators initialised for the StoryTeller System.
    :return: A list of operators, specifically [EqualToOperator(10), GreaterThanEqualToOperator(7)]'
    """
    return [EqualToOperator(10), GreaterThanEqualToOperator(7)]
