"""
This module facilitates the creation of complex parsed dice strings.

Classes
=======
ParsedDiceStringBuilder - A builder pattern for creating ParsedDiceStrings.
"""

from typing import Optional

from pydice.dice_string.dice_parser_failures import DiceParserFailure, InvalidDice, \
    UnfinishedOperator
from pydice.dice_string.operators import Operator
from pydice.dice_string.parsed_dice_string import ParsedDiceString
from pydice.die import Dice, Die, FateDie
from pydice.roll_result import RollResult
from pydice.roll_result_operators.roll_result_builder import RollResultBuilder

fate_dice = Dice(FateDie(), 4)
d10 = Die(10)


class ParsedDiceStringBuilder:
    """
    Creates ParsedDiceString objects with many different configurations.

    Class Methods:
    ==============
    create_parsed_dice_string(dice_string) - A factory method to create a new
        ParsedDiceStringBuilder.

    Methods:
    ========
    with_dice(Dice) -> ParsedDiceStringBuilder:
        Sets the dice of the ParsedDiceString to the given value.
    with_fate_dice() -> ParsedDiceStringBuilder:
        Sets the dice of the ParsedDiceString to be FateDice.
    with_storyteller_dice(int) -> ParsedDiceStringBuilder:
        Sets the dice of the ParsedDiceString to be StorytellerDice
    with_operators(list[operator]) -> ParsedDiceStringBuilder:
        Sets the operators of the ParsedDiceString.
    with_failures(failure) -> ParsedDiceStringBuilder:
        Adds a failure to the ParsedDiceString.
    with_dice_failure() -> ParsedDiceStringBuilder:
        Add an InvalidDice failure to the ParsedDiceString.
    with_unfinished_operator(str) -> ParsedDiceStringBuilder:
        Adds unfinished operators as an UnfinishedOperatorFailure.
    build() -> ParsedDiceString:
        Creates the ParsedDiceString.
    """
    @staticmethod
    def create_parsed_dice_string(dice_string: str):
        """
        A factory method for creating the Builder.
        :param dice_string: The base dice string that is used to create this builder.
        :return: A ParsedDiceStringBuilder configured with that dice string.
        """
        return ParsedDiceStringBuilder(dice_string)

    def __init__(self, dice_string: str):
        self._dice_string = dice_string
        self._dice: Dice | None = None
        self._operators: list[Operator] = []
        self._roll_result: Optional[RollResult] = None
        self._failures: list[DiceParserFailure] = []

    def with_dice(self, dice: Dice) -> 'ParsedDiceStringBuilder':
        """
        Sets the dice to be used when building ParsedDiceString.
        :param dice: The dice to be set.
        :return: This ParsedDiceStringBuilder.
        """
        self._dice = dice
        return self

    def with_fate_dice(self) -> 'ParsedDiceStringBuilder':
        """
        Sets the dice to be used when building ParsedDiceString to be FATEDice.
        :return: This ParsedDiceStringBuilder.
        """
        self._dice = fate_dice
        return self

    def with_storyteller_dice(self, number_of_dice: int) -> 'ParsedDiceStringBuilder':
        """
        Sets the dice to be used when building ParsedDiceString to be Storyteller Dice.
        :param number_of_dice: The number of dice to add.
        :return: This ParsedDiceStringBuilder.
        """
        self._dice = Dice(d10, number_of_dice)
        return self

    def with_operators(self, operators: list[Operator]) -> 'ParsedDiceStringBuilder':
        """
        Adds the operators to the operators for the ParsedDiceString.
        :param operators: The operators to add.
        :return: This ParsedDiceStringBuilder.
        """
        self._operators.extend(operators)
        return self

    def with_failure(self, failure: DiceParserFailure) -> 'ParsedDiceStringBuilder':
        """
        Adds a failure to the ParseDiceString.
        :param failure: The Failure to add.
        :return: This ParsedDiceStringBuilder.
        """
        self._failures.append(failure)
        return self

    def with_dice_failure(self) -> 'ParsedDiceStringBuilder':
        """
        Adds a InvalidDice failure to the ParsedDiceString.
        :return: This ParsedDiceStringBuilder.
        """
        failure = InvalidDice(self._dice_string)
        return self.with_failure(failure)

    def with_unfinished_operator(self, unfinished_operator: str) -> 'ParsedDiceStringBuilder':
        """
        Adds an UnfinishedOperator failure to the ParsedDiceString.
        :param unfinished_operator: The operator that wasn't completed.
        :return: This ParsedDiceStringBuilder.
        """
        failure = UnfinishedOperator(unfinished_operator)
        return self.with_failure(failure)

    def build(self) -> ParsedDiceString:
        """
        Creates the ParsedDiceString based on the configuration of the builder.
        :return:
        """
        self._build_roll_result()
        return ParsedDiceString(self._dice_string, self._failures, self._roll_result)

    def _build_roll_result(self):
        if not self._can_build_result():
            return
        builder = RollResultBuilder.create_roll_result_builder(self._dice)
        for operator in self._operators:
            if operator is None:
                continue
            builder = operator.add(builder)

        self._roll_result = builder.build()

    def _can_build_result(self) -> bool:
        return self._dice is not None and (failure.invalidates for failure in self._failures)
