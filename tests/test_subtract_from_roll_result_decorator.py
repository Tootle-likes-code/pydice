import unittest
from unittest.mock import Mock

from roll_result import SubtractFromRollResultDecorator


class SubtractFromRollResultDecoratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_die = Mock()
        self.test_die.result = Mock(return_value=3)


class ResultTests(SubtractFromRollResultDecoratorTests):
    def test_results_has_modifier_added_to_it(self):
        # Arrange
        expected_result = 1
        test_roll_result = SubtractFromRollResultDecorator(self.test_die, 2)

        # Act
        result = test_roll_result.result()

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
