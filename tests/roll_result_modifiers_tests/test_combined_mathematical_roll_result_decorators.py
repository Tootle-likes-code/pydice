import unittest
from unittest.mock import Mock, PropertyMock

from pydice.roll_result_operators.roll_result_decorators import AddToRollResultDecorator, \
    SubtractFromRollResultDecorator, \
    MultiplyRollResultDecorator, DivideByRollResultDecorator


class CombinedMathematicalRollResultDecoratorsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_die_result = Mock()
        type(self.test_die_result).result = PropertyMock(return_value=3)
        type(self.test_die_result).die_rolls = PropertyMock(return_value=[4, 3, 5, 6, 1])

        self.add_decorator = AddToRollResultDecorator(self.test_die_result, 2)
        self.subtract_decorator = SubtractFromRollResultDecorator(self.add_decorator, 4)
        self.multiply_decorator = MultiplyRollResultDecorator(self.subtract_decorator, 3)
        self.final_roller = DivideByRollResultDecorator(self.multiply_decorator, 2)


class DieRollTests(CombinedMathematicalRollResultDecoratorsTests):
    def test_die_rolls_represent_base_rolls(self):
        # Arrange
        expected_result = [4, 3, 5, 6, 1]

        # Act
        result = self.final_roller.die_rolls

        # Assert
        self.assertEqual(expected_result, result)


class ResultsTests(CombinedMathematicalRollResultDecoratorsTests):
    def test_result_correctly_applies_all_decorators_to_give_correct_result(self):
        # Arrange
        expected_result = 2

        # Act
        result = self.final_roller.result

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
