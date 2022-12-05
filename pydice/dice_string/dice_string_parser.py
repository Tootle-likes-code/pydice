import re
from re import Pattern, Match

from pydice.dice_string.operators import OperatorFactory
from pydice.dice_string.parsed_dice_string import ParsedDiceString
from pydice.dice_string.parsed_dice_string_builder import ParsedDiceStringBuilder
from pydice.die import Dice, Die


def parse(dice_string: str) -> ParsedDiceString:
    dice_string_parser = DiceStringParser(dice_string)
    dice_string_parser.parse()

    return dice_string_parser.parsed_dice_string


_fate_regex = re.compile(r"df", re.IGNORECASE)
_storyteller_regex = re.compile(r"(?P<number_of_dice>\d+)st", re.IGNORECASE)
_base_dice_regex = re.compile(r"(?:\d*d\d.)|(?:\d+st)|(?:df)", re.IGNORECASE)
_extract_dice_regex = re.compile(r"(?P<number_of_dice>\d*)d(?P<dice_size>\d+)", re.IGNORECASE)


class DiceStringParser:
    def __init__(self, dice_string):
        self._parsed_dice_string = None
        self._dice_string = dice_string
        self._builder = ParsedDiceStringBuilder.create_parsed_dice_string(dice_string)

    def parse(self) -> None:
        self._extract_dice()
        self._extract_operators()
        self._parsed_dice_string = self._builder.build()

    def _extract_dice(self):
        extracted_special_dice = self._extract_reserved_dice()
        if extracted_special_dice:
            return

        self._extract_generic_dice()

    def _extract_reserved_dice(self) -> bool:
        if self._check_string_for_dice(_fate_regex):
            self._builder.with_fate_dice()
            return True

        storyteller_match = self._check_string_for_dice(_storyteller_regex)
        if storyteller_match:
            self._create_storyteller_dice(storyteller_match)
            return True

        return False

    def _check_string_for_dice(self, dice_regex: Pattern) -> Match:
        match = re.match(dice_regex, self._dice_string)

        return match

    def _create_storyteller_dice(self, storyteller_match: Match) -> None:
        number_of_dice = int(storyteller_match.group("number_of_dice"))
        self._builder.with_storyteller_dice(number_of_dice)
        self._builder.with_operators(OperatorFactory.get_storyteller_operators())

    def _extract_generic_dice(self):
        dice_match = re.match(_extract_dice_regex, self._dice_string)
        if not dice_match:
            self._builder.with_dice_failure()
            return

        number_of_dice = int(dice_match.group("number_of_dice")) if \
            "number_of_dice" in dice_match.groupdict().keys() \
            and dice_match.group("number_of_dice") != '' \
            else 1
        dice_size = int(dice_match.group("dice_size"))

        self._builder.with_dice(Dice(Die(dice_size), number_of_dice))

    def _extract_operators(self) -> None:
        operator_string = self._get_operator_string()
        if not operator_string:
            return
        self._builder.with_operators(OperatorFactory.get_operators(operator_string))

    def _get_operator_string(self):
        modifiers = re.split(_base_dice_regex, self._dice_string)
        return modifiers[1] if len(modifiers) > 1 else None

    @property
    def parsed_dice_string(self) -> ParsedDiceString | None:
        return self._parsed_dice_string
