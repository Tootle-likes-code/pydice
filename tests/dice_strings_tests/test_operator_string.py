import unittest

from pydice.dice_string.operator_string import OperatorString


class OperatorStringTests(unittest.TestCase):
    pass


class ConstructorTests(OperatorStringTests):
    def test_empty_string_operator_string_gives_base_operators(self):
        # Arrange
        expected_results = []

        # Act
        results = OperatorString("").operators

        # Assert
        self.assertListEqual(expected_results, results)

    def test_empty_string_operator_gives_none_unfinished_operators(self):
        # Act
        result = OperatorString("").unfinished_operators

        # Assert
        self.assertIsNone(result)

    def test_none_string_operator_string_gives_base_operators(self):
        # Arrange
        expected_results = []

        # Act
        results = OperatorString(None).operators

        # Assert
        self.assertListEqual(expected_results, results)

    def test_none_string_operator_gives_none_unfinished_operators(self):
        # Act
        result = OperatorString(None).unfinished_operators

        # Assert
        self.assertIsNone(result)

    def test_unfinished_operator_sets_unfinished_operators(self):
        # Arrange
        expected_result = "fe"

        # Act
        result = OperatorString("fe").unfinished_operators

        # Assert
        self.assertEqual(expected_result, result)
