import unittest

from pydice.operators import OperatorFactory, AddOperator, SubtractOperator, MultiplyOperator, DivideOperator, \
    EqualToOperator, GreaterThanEqualToOperator, ExplodingOperator, GreaterThanOperator, LessThanOperator, \
    LessThanEqualToOperator, NotEqualToOperator


class OperatorFactoryTests(unittest.TestCase):
    pass


class GetOperatorTests(OperatorFactoryTests):
    def test_get_operator_is_invalid_returns_none(self):
        # Act
        result = OperatorFactory.get_operator("kajhdfklah", 100)

        # Assert
        self.assertIsNone(result)

    def test_get_operator_is_add_returns_AddOperator(self):
        # Act
        result = OperatorFactory.get_operator("+", 5)

        # Assert
        self.assertIsInstance(result, AddOperator)

    def test_get_operator_is_add_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("+", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_subtract_returns_SubtractOperator(self):
        # Act
        result = OperatorFactory.get_operator("-", 5)

        # Assert
        self.assertIsInstance(result, SubtractOperator)

    def test_get_operator_is_subtract_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("-", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_multiply_returns_MultiplyOperator(self):
        # Act
        result = OperatorFactory.get_operator("*", 5)

        # Assert
        self.assertIsInstance(result, MultiplyOperator)

    def test_get_operator_is_multiply_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("*", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_multiply_x_returns_MultiplyOperator(self):
        # Act
        result = OperatorFactory.get_operator("x", 5)

        # Assert
        self.assertIsInstance(result, MultiplyOperator)

    def test_get_operator_is_multiply_x_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("x", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_multiply_x_is_case_insensitive(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("X", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_divide_returns_DivideOperator(self):
        # Act
        result = OperatorFactory.get_operator("/", 5)

        # Assert
        self.assertIsInstance(result, DivideOperator)

    def test_get_operator_is_divide_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("/", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_exploding_returns_ExplodingOperator(self):
        # Act
        result = OperatorFactory.get_operator("e", 5)

        # Assert
        self.assertIsInstance(result, ExplodingOperator)

    def test_get_operator_is_exploding_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("e", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_equal_to_returns_EqualToOperator(self):
        # Act
        result = OperatorFactory.get_operator("=", 5)

        # Assert
        self.assertIsInstance(result, EqualToOperator)

    def test_get_operator_is_equal_to_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("=", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_not_equal_to_returns_NotEqualToOperator(self):
        # Act
        result = OperatorFactory.get_operator("!=", 5)

        # Assert
        self.assertIsInstance(result, NotEqualToOperator)

    def test_get_operator_is_not_equal_to_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("!=", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_not_equal_to_alt_returns_NotEqualToOperator(self):
        # Act
        result = OperatorFactory.get_operator("=/=", 5)

        # Assert
        self.assertIsInstance(result, NotEqualToOperator)

    def test_get_operator_is_not_equal_to_alt_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("=/=", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_greater_than_returns_GreaterThanOperator(self):
        # Act
        result = OperatorFactory.get_operator(">", 5)

        # Assert
        self.assertIsInstance(result, GreaterThanOperator)

    def test_get_operator_is_greater_than_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator(">", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_greater_than_equal_to_returns_GreaterThanEqualToOperator(self):
        # Act
        result = OperatorFactory.get_operator(">=", 5)

        # Assert
        self.assertIsInstance(result, GreaterThanEqualToOperator)

    def test_get_operator_is_greater_than_equal_to_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator(">=", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_less_than_returns_LessThanOperator(self):
        # Act
        result = OperatorFactory.get_operator("<", 5)

        # Assert
        self.assertIsInstance(result, LessThanOperator)

    def test_get_operator_is_less_than_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("<", 5)

        # Assert
        self.assertEqual(expected_result, result.value)

    def test_get_operator_is_less_than_equal_to_returns_LessThanEqualToOperator(self):
        # Act
        result = OperatorFactory.get_operator("<=", 5)

        # Assert
        self.assertIsInstance(result, LessThanEqualToOperator)

    def test_get_operator_is_less_than_equal_to_provides_correct_value(self):
        # Arrange
        expected_result = 5

        # Act
        result = OperatorFactory.get_operator("<=", 5)

        # Assert
        self.assertEqual(expected_result, result.value)


if __name__ == '__main__':
    unittest.main()
