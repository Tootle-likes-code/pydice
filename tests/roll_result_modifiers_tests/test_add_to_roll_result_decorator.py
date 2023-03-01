import unittest
from unittest.mock import Mock, PropertyMock

from pydice.die import Die, Dice
from pydice.roll_result import DiceRollResult
from pydice.roll_result_operators.roll_result_decorators import AddToRollResultDecorator


class AddToRollResultDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.die_rolls = [4, 5]
        self.test_die_result = Mock()
        self.test_die_result.result = 3
        self.test_die_result.die_rolls = self.die_rolls

        self.test_roll_result = AddToRollResultDecorator(self.test_die_result, 2)


class ConstructorTests(AddToRollResultDecoratorTests):
    def setUp(self) -> None:
        self.test_die_result = Mock()
        self.test_die_result_result = PropertyMock(return_value=3)
        type(self.test_die_result).result = self.test_die_result_result

    def test_constructor_calls_decorated_results(self):
        # Act
        AddToRollResultDecorator(self.test_die_result, 3)

        # Assert
        self.test_die_result_result.assert_called_once()


class DieRollsTests(AddToRollResultDecoratorTests):
    def test_rolled_values_are_returned(self):
        # Arrange
        expected_result = [4, 5]

        # Act
        result = self.test_roll_result.die_rolls

        # Assert
        self.assertEqual(expected_result, result)


class ResultTests(AddToRollResultDecoratorTests):
    def test_results_has_modifier_added_to_it(self):
        # Arrange
        expected_result = 12
        roll_result = DiceRollResult(Dice(Die(6), 2), self.die_rolls)
        test_decorator = AddToRollResultDecorator(roll_result, 3)

        # Act
        result = test_decorator.result

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
