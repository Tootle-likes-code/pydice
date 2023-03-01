import unittest
from unittest.mock import MagicMock

from pydice.roll_result import RollResult
from pydice.roll_result_operators.roll_result_decorators import DropLowestDecorator


class DropLowestDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.die_rolls = [15, 7, 19]
        self.mocked_roll_result = MagicMock(spec=RollResult)
        type(self.mocked_roll_result).die_rolls = self.die_rolls


class ConstructorTests(DropLowestDecoratorTests):
    def test_target_number_is_less_than_1_raises_value_error(self):
        # Assert
        with self.assertRaises(ValueError):
            # Act
            DropLowestDecorator(self.mocked_roll_result,0)


class DieRollsTests(DropLowestDecoratorTests):
    def test_default_die_roll_is_changed_to_correct_values(self):
        # Arrange
        expected_results = [15, 19]
        test_roll = DropLowestDecorator(self.mocked_roll_result)

        # Act
        results = test_roll.die_rolls

        # Assert
        self.assertListEqual(expected_results, results)
        
    def test_given_larger_numbers_die_roll_is_changed_to_correct_values(self):
        # Arrange
        expected_results = [19]
        test_roll = DropLowestDecorator(self.mocked_roll_result, 2)

        # Act
        results = test_roll.die_rolls

        # Assert
        self.assertListEqual(expected_results, results)


if __name__ == '__main__':
    unittest.main()
