"""
Contains the custom Exceptions for parsing dice.
"""


class DiceParseError(Exception):
    """
    An error that is to be called when an attempt to parse a dice string fails.
    """

    def __init__(self, dice_string: str):
        message = f"Was given {dice_string}, which is an invalid dice string.  Must either use a " \
                  f"predefined die or have <Optional:number_of_dice>d<size_of_dice>."
        super().__init__(message)
        self._erroneous_dice_string: str = dice_string
