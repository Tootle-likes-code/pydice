"""
Contains failures for dice parsing and details about them.

Classes
=======

Severity - An enum containing the severity of the error.
DiceParserFailure - ABC to contain a parser failure reason and severity.
InvalidDice - Called when the dice string is invalid.
InvalidOperator - Called when an operator string is invalid.
UnfinishedOperator - Called when an operator string doesn't complete.
"""

from abc import ABC
from dataclasses import dataclass
from enum import auto, Enum

from pydice.dice_string import operators


class Severity(Enum):
    """
    Contains the Severity values for DiceParserFailures.

    Values
    ______
    WARNING - Represents a failure that does not prevent continuation.
    ERROR - Represents a failure that prevents continuation.
    """
    WARNING = auto()
    ERROR = auto()


@dataclass
class DiceParserFailure(ABC):
    """
    An ABC that contains the details of a Data Parsing failure.


    Attributes
    ----------
    reason: str - The reason message for why this failure occurred.
    severity: Severity - The severity for the failure.


    Methods
    -------
    get_message() - returns the reason for the failure.
    invalidates() - returns if this failure causes the dice string being parsed to no
    longer be viable.


    Sub Classing
    ------------
    Sub Classes are only expected to supply a reason and a severity to the parent.
    """
    reason: str
    severity: Severity

    def get_message(self):
        """
        Returns the for the failure occurring.
        :return: A plain text message for displaying the failure.
        """
        return self.reason

    def invalidates(self):
        """
        Indicates that the failure invalidates the data string.
        :return: True indicates that the dice string is now invalid.
        """
        return self.severity == Severity.ERROR


class InvalidDice(DiceParserFailure):
    """
    Inherits its functionality from its parent, providing the details for an invalid dice.
    """
    def __init__(self, dice_string):
        """
        Constructor
        :param dice_string: The dice string that triggered the failure.
        """
        reason = f"Was given {dice_string}, which is an invalid dice string.  Must either use a " \
                 "predefined die or have <Optional:number_of_dice>d<size_of_dice>."
        super().__init__(reason, Severity.ERROR)


class InvalidOperator(DiceParserFailure):
    """
    Inherits its functionality from its parent, providing the details for an invalid operator.
    """
    def __init__(self, operator_string):
        """
        Constructor
        :param operator_string: The operator string that triggered the failure.
        """
        reason = f"Was given {operator_string}, which is an invalid set of operators.  The " \
                 f"supported operators are {list(operators.ACCEPTED_OPERATORS.keys())}."
        super().__init__(reason, Severity.ERROR)


class UnfinishedOperator(DiceParserFailure):
    """
    Inherits its functionality from its parent, providing the details from an invalid operator.
    """
    def __init__(self, operator_string):
        reason = f"Was given {operator_string}, which is an unfinished operator."
        super().__init__(reason, Severity.WARNING)
