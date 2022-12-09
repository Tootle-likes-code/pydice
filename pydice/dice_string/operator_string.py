"""
A module for containing strings of pydice.dice_string.operators.

=======
Classes
=======
OperatorString - A class to represent an Operator String.
"""

from pydice.dice_string import operators as operator_functions
from pydice.dice_string.operators import Operator


class OperatorString:
    """
    Represents a string of pydice.dice_string.operators and contains basic
    processing to extract operators.

    =======
    Methods
    =======
    :operators: Returns the operators contained in the given Operator String.
    :unfinished_operators:
        Returns the end of the string that was unable to converted to an Operator.
    :is_valid: Returns if this operator was valid.
    """
    def __init__(self, operator_string: str | None):
        self.operator_string = operator_string
        self._operators: list[Operator] = []
        self._unfinished_operators: str | None = None
        self._process_operator_string()

    def _process_operator_string(self):
        if not self.operator_string:
            return

        operator = ""
        value = ""

        for index, character in enumerate(self.operator_string):
            if not character.isnumeric():
                operator += character

                if index == len(self.operator_string) - 1:
                    self._unfinished_operators = operator
                continue

            next_character = self.operator_string[index + 1:index + 2]
            if index != len(self.operator_string) and next_character.isnumeric():
                value = character
                continue
            value += character
            built_operator = operator_functions.get_operator(operator, int(value))
            if built_operator is not None:
                self._operators.append(built_operator)
            operator = ""
            value = ""

    @property
    def operators(self) -> list[Operator]:
        """
        Returns the parsed operators.
        """
        return self._operators

    @property
    def unfinished_operators(self) -> str | None:
        """
        Returns the unparsed operators.
        """
        return self._unfinished_operators

    @property
    def is_valid(self) -> bool:
        """
        Returns if this Operator String was valid.
        """
        return self._unfinished_operators is None
