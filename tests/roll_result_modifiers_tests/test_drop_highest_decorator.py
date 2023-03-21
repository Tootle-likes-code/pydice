import unittest
from unittest.mock import MagicMock

from parameterized import parameterized

from pydice.die import Dice, Die
from pydice.roll_result import RollResult, DiceRollResult
from pydice.roll_result_operators.drop_dice_roll_result_decorators import DropHighestDecorator


class DropHighestDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.die_rolls = [9, 10, 3]
        self.mock_roll_results = MagicMock(spec=RollResult)
        type(self.mock_roll_results).die_rolls = self.die_rolls


class Constructor(DropHighestDecoratorTests):
    def test_number_to_drop_less_than_1_raises_value_error(self):
        # Assert
        with self.assertRaises(ValueError) as ex:
            # Act
            DropHighestDecorator(self.mock_roll_results, 0)


class DieRollsTests(DropHighestDecoratorTests):
    def test_one_dropped_returns_correct_result(self):
        # Arrange
        expected_results = [3, 9]
        test_decorator = DropHighestDecorator(self.mock_roll_results)

        # Act
        results = test_decorator.die_rolls

        # Assert
        self.assertListEqual(expected_results, results)

    def test_two_dropped_returns_correct_result(self):
        # Arrange
        expected_results = [3]
        test_decorator = DropHighestDecorator(self.mock_roll_results, 2)

        # Act
        results = test_decorator.die_rolls

        # Assert
        self.assertListEqual(expected_results, results)

    def test_more_than_length_to_drop_returns_empty_list(self):
        # Arrange
        expected_results = []
        test_roll = DropHighestDecorator(self.mock_roll_results, 5)

        # Act
        results = test_roll.die_rolls

        # Assert
        self.assertListEqual(expected_results, results)

class ResultsTests(DropHighestDecoratorTests):
    def setUp(self) -> None:
        super().setUp()
        self.mock_dice = MagicMock(Dice)

    def test_result_value_is_updated_correctly(self):
        # Arrange
        expected_result = 12
        roll_result = DiceRollResult(self.mock_dice, self.die_rolls)
        test_decorator = DropHighestDecorator(roll_result)

        # Act
        result = test_decorator.result

        # Assert
        self.assertEqual(expected_result, result)

class ExampleTests(DropHighestDecoratorTests):
    @parameterized.expand([
        ("Example 1: 2d20dh1 [17, 6] -> [6]", [17, 6], 1, [6]),
        ("Example 2: 12d6dh4 [2, 4, 5, 6, 2, 6, 6, 5, 4, 1, 6, 6] -> [1, 2, 2, 4, 4, 5, 5, 6]",
         [2, 4, 5, 6, 2, 6, 6, 5, 4, 1, 6, 6], 4, [1, 2, 2, 4, 4, 5, 5, 6])
    ])
    def test_examples_work(self, _, test_die_rolls, number_to_drop, expected_results):
        # Arrange
        type(self.mock_roll_results).die_rolls = test_die_rolls
        test_decorator = DropHighestDecorator(self.mock_roll_results, number_to_drop)

        # Act
        results = test_decorator.die_rolls

        # Assert
        self.assertListEqual(expected_results, results)


if __name__ == '__main__':
    unittest.main()
