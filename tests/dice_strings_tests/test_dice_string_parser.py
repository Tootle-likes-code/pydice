import unittest
from unittest.mock import call, patch

from pydice.dice_string import dice_string_parser
from tests.dice_strings_tests.test_parsed_dice_string import ParsedDiceStringTests


class DiceStringParserTests(unittest.TestCase):
    def setUp(self) -> None:
        pass


@patch("pydice.dice_string.dice_string_parser.DiceStringParserFactory.create_parsed_dice_string")
class ParseTests(ParsedDiceStringTests):
    def test_calls_dice_string_parser_factory(self, mock_factory):
        # Arrange
        expected_calls = [call("1d20")]

        # Act
        dice_string_parser.parse("1d20")

        # Assert
        mock_factory.assert_called_once()
        mock_factory.assert_has_calls(expected_calls)


if __name__ == '__main__':
    unittest.main()
