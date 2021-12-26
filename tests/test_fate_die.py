import unittest

from die import FateDie


class FateDieTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_die = FateDie()


class MinTest(FateDieTests):
    def test_min_is_negative_one(self):
        # Arrange
        expected_result = -1

        # Assert
        self.assertEqual(expected_result, self.test_die.min)


class MaxTest(FateDieTests):
    def test_max_is_one(self):
        # Arrange
        expected_result = 1

        # Assert
        self.assertEqual(expected_result, self.test_die.max)


class StrTests(FateDieTests):
    def test_result_is_expected_string(self):
        # Arrange
        expected_result = "Df"

        # Act
        result = str(self.test_die)

        # Assert
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
