import unittest
from unittest.mock import MagicMock, patch, call

from pydice.dice_string import operators
from pydice.dice_string.dice_string_parser import DiceStringParser
from pydice.dice_string.parsed_dice_string_builder import ParsedDiceStringBuilder
from pydice.dice_string.operators import AddOperator
from pydice.die import Dice, Die
from tests import helpers


class DiceStringParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_builder = MagicMock(spec=ParsedDiceStringBuilder)
        self.mock_builder.build.return_value = "ParsedDiceString"


@patch("pydice.dice_string.dice_string_parser.ParsedDiceStringBuilder.create_parsed_dice_string")
class ParseTests(DiceStringParserTests):
    def test_given_valid_dice_string_calls_builder_with_dice(self, mock_create_builder):
        # Arrange
        expected_calls = [call(Dice(Die(20), 1))]
        mock_create_builder.return_value = self.mock_builder

        # Act
        DiceStringParser("1d20").parse()

        # Assert
        self.mock_builder.with_dice.assert_called_once()
        self.mock_builder.with_dice.assert_has_calls(expected_calls)

    def test_invalid_dice_adds_calls_builder_failure(self, mock_create_builder):
        # Arrange
        mock_create_builder.return_value = self.mock_builder

        # Act
        DiceStringParser("1d").parse()

        # Assert
        self.mock_builder.with_dice_failure.assert_called_once()

    def test_fate_dice_calls_builder_add_fate_dice(self, mock_create_builder):
        # Arrange
        mock_create_builder.return_value = self.mock_builder

        # Act
        DiceStringParser("df").parse()

        # Assert
        self.mock_builder.with_fate_dice.assert_called_once()

    def test_storyteller_dice_calls_builder_add_storyteller_dice(self, mock_create_builder):
        # Arrange
        expected_calls = [call(5)]
        mock_create_builder.return_value = self.mock_builder

        # Act
        DiceStringParser("5st").parse()

        # Assert
        self.mock_builder.with_storyteller_dice.assert_called_once()
        self.mock_builder.with_storyteller_dice.assert_has_calls(expected_calls)

    def test_valid_dice_with_operators_calls_builder_add_operator(self, mock_create_builder):
        # Arrange
        expected_calls = [call([AddOperator(4)])]
        mock_create_builder.return_value = self.mock_builder

        # Act
        DiceStringParser("1d20+4").parse()

        # Assert
        self.mock_builder.with_operators.assert_called_once()
        self.mock_builder.with_operators.assert_has_calls(expected_calls)

    def test_no_modifiers_adds_no_modifiers(self, mock_create_builder):
        # Arrange
        mock_create_builder.return_value = self.mock_builder

        # Act
        DiceStringParser("1d20").parse()

        # Assert
        self.mock_builder.with_operators.assert_not_called()

    def test_storyteller_dice_calls_builder_add_storyteller_operators(self, mock_create_builder):
        # Arrange
        expected_calls = [call(operators.get_storyteller_operators())]
        mock_create_builder.return_value = self.mock_builder

        # Act
        DiceStringParser("5st").parse()

        # Assert
        self.mock_builder.with_operators.assert_called_once()
        self.mock_builder.with_operators.assert_has_calls(expected_calls)

    def test_storyteller_dice_with_modifier_builder_adds_correct_operators(self, mock_create_builder):
        # Arrange
        expected_calls = [call(operators.get_storyteller_operators()), call([AddOperator(4)])]
        mock_create_builder.return_value = self.mock_builder

        # Act
        DiceStringParser("5st+4").parse()

        # Assert
        helpers.assert_is_calls(self.mock_builder.with_operators, expected_calls)


@patch("pydice.dice_string.dice_string_parser.ParsedDiceStringBuilder.create_parsed_dice_string")
class ParsedDiceStringTests(DiceStringParserTests):
    def test_no_parse_called_returns_None(self, _):
        # Arrange
        dice_string_parser = DiceStringParser("1d20+4")

        # Act
        result = dice_string_parser.parsed_dice_string

        # Assert
        self.assertIsNone(result)

    def test_valid_parse_sets_expected_ParsedDiceString(self, mock_create_builder):
        # Arrange
        expected_result = "ParsedDiceString"
        mock_create_builder.return_value = self.mock_builder
        dice_string_parser = DiceStringParser("1d20+4")

        # Act
        dice_string_parser.parse()
        result = dice_string_parser.parsed_dice_string

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
