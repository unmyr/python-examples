"""Test datetime.date with unittest."""
import unittest
import datetime


class TestDate(unittest.TestCase):
    """Test datetime.date module."""
    def test_date_fix_timedelta(self) -> None:
        """Test timedelta."""
        d1 = datetime.date(2021, 12, 1)
        d2 = d1 + datetime.timedelta(days=31)

        self.assertEqual(d2, datetime.date(2022, 1, 1))

    def test_date_delta(self) -> None:
        """Test timedelta."""
        today: datetime.date
        yesterday: datetime.date

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        self.assertEqual((today - yesterday).days, 1)

    def test_string_dt_native_fromisoformat(self) -> None:
        """Test fromisoformat()."""
        # Python 3.7 or later
        date_obj = datetime.date(2021, 11, 13)
        assert datetime.date.fromisoformat('2021-11-13') == date_obj
