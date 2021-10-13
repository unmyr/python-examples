"""Test datetime with unittest."""
import unittest
import datetime


class TestDateTime(unittest.TestCase):
    """Test datetime module."""

    def test_date_fix_timedelta(self):
        """Test timedelta."""
        d1 = datetime.date(2021, 12, 1)
        d2 = d1 + datetime.timedelta(days=31)

        self.assertEqual(
            d2,
            datetime.date(2022, 1, 1)
        )
