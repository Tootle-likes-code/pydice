import unittest
from unittest.mock import Mock

from roll_result import DivideByRollResultDecorator


class DivideByRollResultDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
            self.test_die = Mock()
            self.test_die.result = Mock(return_value=4)


class ResultsTests(DivideByRollResultDecoratorTests):
    def test_result_is_divided_correctly(self):
        # Arrange
        expected_result = 2
        test_roll_result = DivideByRollResultDecorator(self.test_die, 2)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_remainder_result_is_rounded_up_correctly(self):
        # Arrange
        expected_result = 1
        test_roll_result = DivideByRollResultDecorator(self.test_die, 5)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)

    def test_remainder_result_is_rounded_down_correctly(self):
        # Arrange
        expected_result = 1
        test_roll_result = DivideByRollResultDecorator(self.test_die, 3)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
