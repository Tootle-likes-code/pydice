"""
Contains the custom Exceptions for parsing dice.

Classes
=======

DiceParseError An error to be raised for dice string parsing exceptions.
"""


class DiceParseError(Exception):
    """
    An error that is to be called when an attempt to parse a dice string fails, that provides
    a custom message.
    """

    def __init__(self, dice_string: str):
        """
        Constructor.
        :param dice_string: The dice string that caused the failure.
        """
        message = f"Was given {dice_string}, which is an invalid dice string.  Must either use a " \
                  f"predefined die or have <Optional:number_of_dice>d<size_of_dice>."
        super().__init__(message)
        self._erroneous_dice_string: str = dice_string
