"""Test datetime with unittest."""
import unittest
import datetime
import typing


def parse_naive_datetime(dt_iso8601_str: str) -> typing.Optional[datetime.datetime]:
    """Parse naive datetime."""
    for time_fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f']:
        try:
            return datetime.datetime.strptime(dt_iso8601_str, time_fmt)
        except ValueError:
            pass

    return None


class TestDateTime(unittest.TestCase):
    """Test datetime module."""
    def test_string_dt_naive_fromisoformat(self):
        """Test fromisoformat()."""
        # Python 3.7 or later
        dt_obj_with_us = datetime.datetime(2021, 11, 13, 11, 49, 20, 673681)
        assert datetime.datetime.fromisoformat('2021-11-13 11:49:20.673681') == dt_obj_with_us
        assert datetime.datetime.fromisoformat('2021-11-13T11:49:20.673681') == dt_obj_with_us

        dt_obj_with_ms = datetime.datetime(2021, 11, 13, 11, 49, 20, 673000)
        assert datetime.datetime.fromisoformat('2021-11-13 11:49:20.673') == dt_obj_with_ms
        assert datetime.datetime.fromisoformat('2021-11-13T11:49:20.673') == dt_obj_with_ms

        dt_obj_with_sec = datetime.datetime(2021, 11, 13, 11, 49, 20)
        assert datetime.datetime.fromisoformat('2021-11-13 11:49:20') == dt_obj_with_sec
        assert datetime.datetime.fromisoformat('2021-11-13 11:49:20.000') == dt_obj_with_sec
        assert datetime.datetime.fromisoformat('2021-11-13 11:49:20.000000') == dt_obj_with_sec

        dt_obj_with_min = datetime.datetime(2021, 11, 13, 11, 49)
        assert datetime.datetime.fromisoformat('2021-11-13 11:49') == dt_obj_with_min
        assert datetime.datetime.fromisoformat('2021-11-13T11:49') == dt_obj_with_min
        assert datetime.datetime.fromisoformat('2021-11-13T11:49:00') == dt_obj_with_min

        dt_obj_with_hour = datetime.datetime(2021, 11, 13, 11, 0)
        assert datetime.datetime.fromisoformat('2021-11-13 11') == dt_obj_with_hour
        assert datetime.datetime.fromisoformat('2021-11-13T11') == dt_obj_with_hour

        dt_obj_with_date = datetime.datetime(2021, 11, 13, 0, 0)
        assert datetime.datetime.fromisoformat('2021-11-13') == dt_obj_with_date

    def test_string_dt_naive_isoformat(self):
        """Test isoformat(): +09:00 format. (Python 3.6 or later)"""
        dt_obj_with_microseconds = datetime.datetime(2021, 11, 13, 11, 49, 20, 673681)
        dt_obj_with_ms = datetime.datetime(2021, 11, 13, 11, 49, 20, 673000)
        dt_obj_no_ms = datetime.datetime(2021, 11, 13, 11, 49, 20, 0)

        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='auto')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673681'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(sep=' ', timespec='auto')
        assert dt_iso8601_str == '2021-11-13 11:49:20.673681'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='microseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673681'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='milliseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='seconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='minutes')
        assert dt_iso8601_str == '2021-11-13T11:49'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='hours')
        assert dt_iso8601_str == '2021-11-13T11'

        dt_iso8601_str = dt_obj_with_ms.isoformat(timespec='auto')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673000', (
            f"isoformat(timespec='auto')={dt_iso8601_str}"
        )
        dt_iso8601_str = dt_obj_with_ms.isoformat(timespec='microseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673000'
        dt_iso8601_str = dt_obj_with_ms.isoformat(timespec='milliseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673'

        # isoformat function drops microseconds part if its value is 000000
        dt_iso8601_str = dt_obj_no_ms.isoformat(timespec='auto')
        assert dt_iso8601_str == '2021-11-13T11:49:20'
        dt_iso8601_str = dt_obj_no_ms.isoformat(timespec='microseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.000000'
        dt_iso8601_str = dt_obj_no_ms.isoformat(timespec='milliseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.000'

    def test_parse_dt_naive_isoformat(self):
        """Test strptime"""
        dt_iso8601_str = datetime.datetime(2021, 11, 13, 11, 49, 20, 673681).isoformat()
        assert dt_iso8601_str == '2021-11-13T11:49:20.673681'

        dt_obj = parse_naive_datetime(dt_iso8601_str)

        assert dt_obj == datetime.datetime(2021, 11, 13, 11, 49, 20, 673681)

    def test_timezone_naive_jst_to_aware_jst_combine(self):
        """Test convert the timezone from UTC to JST."""
        datetime_naive_jst = datetime.datetime.strptime(
            '2021-11-13T11:49:20.673681', '%Y-%m-%dT%H:%M:%S.%f'
        )
        datetime_aware_jst = datetime.datetime.combine(
            datetime_naive_jst.date(), datetime_naive_jst.time(),
            tzinfo=datetime.timezone(datetime.timedelta(hours=9))
        )
        assert datetime_aware_jst == datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681, tzinfo=datetime.timezone(datetime.timedelta(hours=9))
        )

    def test_timezone_naive_jst_to_aware_jst_replace(self):
        """Test convert the timezone from UTC to JST."""
        datetime_naive_jst = datetime.datetime.strptime(
            '2021-11-13T11:49:20.673681', '%Y-%m-%dT%H:%M:%S.%f'
        )
        datetime_aware_jst = datetime_naive_jst.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
        assert datetime_aware_jst == datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681, tzinfo=datetime.timezone(datetime.timedelta(hours=9))
        )
