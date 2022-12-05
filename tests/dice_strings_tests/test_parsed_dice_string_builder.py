import unittest
from unittest.mock import MagicMock, patch

from pydice.dice_string.parsed_dice_string_builder import ParsedDiceStringBuilder
from pydice.die import Dice, Die


class ParsedDiceStringBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.d20 = Dice(Die(20), 1)
        self.mock_builder = MagicMock()
        self.mock_builder.build.return_value = "Roll Result"


class WithOperatorsTests(ParsedDiceStringBuilderTests):
    def test_adding_second_operators_adds_operators_again(self):
        # Arrange
        mock_1 = MagicMock(return_value=1)
        mock_2 = MagicMock(return_value=2)
        mock_3 = MagicMock(return_value=3)
        expected_result = [mock_1, mock_2, mock_3]
        builder = ParsedDiceStringBuilder("1d20").with_operators([mock_1, mock_2])

        # Act
        builder.with_operators([mock_3])

        # Assert
        self.assertEqual(expected_result, builder._operators)


@patch("pydice.dice_string.parsed_dice_string_builder.RollResultBuilder.create_roll_result_builder")
class BuildTests(ParsedDiceStringBuilderTests):
    def test_dice_is_present_no_failures_adds_roll_result(self, created_builder):
        # Arrange
        expected_result = "Roll Result"
        builder = ParsedDiceStringBuilder("1d20").with_dice(self.d20)
        created_builder.return_value = self.mock_builder

        # Act
        result = builder.build()

        # Assert
        self.assertEqual(expected_result, result.roll_result)

    def test_dice_is_not_present_does_not_add_roll_result(self, created_builder):
        # Arrange
        builder = ParsedDiceStringBuilder("1d20").with_dice(self.d20)
        created_builder.return_value = self.mock_builder
        self.mock_builder.build.return_value = None

        # Act
        result = builder.build()

        # Assert
        self.assertIsNone(result.roll_result)

    def test_roll_result_builder_is_created(self, created_builder):
        # Arrange
        builder = ParsedDiceStringBuilder("1d20").with_dice(self.d20)
        created_builder.return_value = self.mock_builder

        # Act
        builder.build()

        # Assert
        created_builder.assert_called_once()

    def test_roll_result_builder_build_is_called(self, created_builder):
        # Arrange
        builder = ParsedDiceStringBuilder("1d20").with_dice(self.d20)
        created_builder.return_value = self.mock_builder

        # Act
        builder.build()

        # Assert
        self.mock_builder.build.assert_called_once()
