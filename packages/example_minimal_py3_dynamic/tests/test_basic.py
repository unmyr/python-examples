"""Test a package."""
import unittest

from example_package import calc


class Test(unittest.TestCase):
    """Test `example_package` module."""

    def test_add_one(self):
        """Test `add_one` method."""
        self.assertEqual(
            calc.add_one(2), 3
        )
