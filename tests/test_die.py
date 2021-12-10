import unittest

from die import Die


class DieTests(unittest.TestCase):
    def setUp(self) -> None:
        pass


class MinTests(DieTests):
    def test_min_returns_min_value(self):
        # Arrange
        expected_result = 1
        test_die = Die(6, 1)

        # Act
        result = test_die.min

        # Assert
        self.assertEqual(expected_result, result)

    def test_negative_min_returns_negative_min_value(self):
        # Arrange
        expected_result = -10
        test_die = Die(6, -10)

        # Act
        result = test_die.min

        # Assert
        self.assertEqual(expected_result, result)
        

class MaxTests(DieTests):
    def test_max_returns_expected_value(self):
        # Arrange
        expected_result = 6
        test_die = Die(6)
        
        # Act
        result = test_die.max
        
        # Assert
        self.assertEqual(expected_result, result)

    def test_max_is_incremental_of_negative_min(self):
        # Arrange
        expected_result = 3
        test_die = Die(6, -2)

        # Act
        result = test_die.max

        # Assert
        self.assertEqual(expected_result, result)

    def test_max_is_incremental_of_min_greater_than_zero(self):
        # Arrange
        expected_result = 7
        test_die = Die(6, 2)

        # Act
        result = test_die.max

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
