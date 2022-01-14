"""Test datetime with unittest."""
import unittest
import datetime
import typing


def parse_native_datetime(dt_iso8601_str: str) -> typing.Optional[datetime.datetime]:
    """Parse native datetime."""
    for time_fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f']:
        try:
            return datetime.datetime.strptime(dt_iso8601_str, time_fmt)
        except ValueError:
            pass

    return None


def parse_aware_datetime(dt_iso8601_str: str) -> typing.Optional[datetime.datetime]:
    """Parse aware datetime."""
    for time_fmt in ['%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%f%z']:
        try:
            return datetime.datetime.strptime(dt_iso8601_str, time_fmt)
        except ValueError:
            pass

    return None


class TestDateTime(unittest.TestCase):
    """Test datetime module."""
    def test_string_dt_native_fromisoformat(self):
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

    def test_string_dt_aware_utc_fromisoformat(self):
        """Test fromisoformat()."""
        # Python 3.7 or later
        dt_obj_with_us = datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681, tzinfo=datetime.timezone.utc
        )
        dt_iso8601_str = '2021-11-13 11:49:20.673681+00:00'
        assert datetime.datetime.fromisoformat(dt_iso8601_str) == dt_obj_with_us
        dt_iso8601_str = '2021-11-13 11:49:20.673681+0000'
        with self.assertRaises(ValueError) as context:
            assert datetime.datetime.fromisoformat(dt_iso8601_str) == dt_obj_with_us
        self.assertEqual(f"Invalid isoformat string: '{dt_iso8601_str}'",
                         str(context.exception))

        dt_obj_with_ms = datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673000, tzinfo=datetime.timezone.utc
        )
        dt_iso8601_str = '2021-11-13 11:49:20.673-00:00'
        assert datetime.datetime.fromisoformat(dt_iso8601_str) == dt_obj_with_ms
        dt_iso8601_str = '2021-11-13 11:49:20.673000-00:00'
        assert datetime.datetime.fromisoformat(dt_iso8601_str) == dt_obj_with_ms

        dt_obj_with_sec = datetime.datetime(
            2021, 11, 13, 11, 49, 20, tzinfo=datetime.timezone.utc
        )
        dt_iso8601_str = '2021-11-13 11:49:20+00:00'
        assert datetime.datetime.fromisoformat(dt_iso8601_str) == dt_obj_with_sec
        dt_iso8601_str = '2021-11-13 11:49:20.000000-00:00'
        assert datetime.datetime.fromisoformat(dt_iso8601_str) == dt_obj_with_sec

        dt_obj_with_min = datetime.datetime(
            2021, 11, 13, 11, 49, tzinfo=datetime.timezone.utc
        )
        dt_iso8601_str = '2021-11-13 11:49+00:00'
        assert datetime.datetime.fromisoformat(dt_iso8601_str) == dt_obj_with_min
        dt_iso8601_str = '2021-11-13 11:49:00.000000+00:00'
        assert datetime.datetime.fromisoformat(dt_iso8601_str) == dt_obj_with_min

        dt_obj_with_hour = datetime.datetime(
            2021, 11, 13, 11, 0, tzinfo=datetime.timezone.utc
        )
        dt_iso8601_str = '2021-11-13 11+00:00'
        assert datetime.datetime.fromisoformat(dt_iso8601_str) == dt_obj_with_hour
        dt_iso8601_str = '2021-11-13 11:00:00.000000+00:00'
        assert datetime.datetime.fromisoformat(dt_iso8601_str) == dt_obj_with_hour

    def test_string_dt_aware_jst_fromisoformat(self):
        """Test fromisoformat()."""
        dt_obj_with_us = datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681,
            tzinfo=datetime.timezone(datetime.timedelta(hours=9))
        )
        dt_iso8601_str = '2021-11-13 11:49:20.673681+09:00'
        assert datetime.datetime.fromisoformat(dt_iso8601_str) == dt_obj_with_us

    def test_string_dt_native_isoformat(self):
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

    def test_string_dt_aware_jst_isoformat(self):
        """Test isoformat(): +09:00 format. (Python 3.6 or later)"""
        dt_obj_with_microseconds = datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681,
            datetime.timezone(datetime.timedelta(hours=9))
        )
        dt_obj_with_ms = datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673000,
            datetime.timezone(datetime.timedelta(hours=9))
        )
        dt_obj_no_ms = datetime.datetime(
            2021, 11, 13, 11, 49, 20, 0,
            datetime.timezone(datetime.timedelta(hours=9))
        )

        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='auto')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673681+09:00'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='microseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673681+09:00'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(sep=' ', timespec='auto')
        assert dt_iso8601_str == '2021-11-13 11:49:20.673681+09:00'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='milliseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673+09:00'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='seconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20+09:00'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='minutes')
        assert dt_iso8601_str == '2021-11-13T11:49+09:00'
        dt_iso8601_str = dt_obj_with_microseconds.isoformat(timespec='hours')
        assert dt_iso8601_str == '2021-11-13T11+09:00'

        dt_iso8601_str = dt_obj_with_ms.isoformat(timespec='auto')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673000+09:00', (
            f"isoformat(timespec='auto')={dt_iso8601_str}"
        )
        dt_iso8601_str = dt_obj_with_ms.isoformat(timespec='microseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673000+09:00'
        dt_iso8601_str = dt_obj_with_ms.isoformat(timespec='milliseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673+09:00'

        # isoformat function drops microseconds part if its value is 000000
        dt_iso8601_str = dt_obj_no_ms.isoformat(timespec='auto')
        assert dt_iso8601_str == '2021-11-13T11:49:20+09:00'
        dt_iso8601_str = dt_obj_no_ms.isoformat(timespec='microseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.000000+09:00'
        dt_iso8601_str = dt_obj_no_ms.isoformat(timespec='milliseconds')
        assert dt_iso8601_str == '2021-11-13T11:49:20.000+09:00'

    def test_parse_dt_native_isoformat(self):
        """Test strptime"""
        dt_iso8601_str = datetime.datetime(2021, 11, 13, 11, 49, 20, 673681).isoformat()
        assert dt_iso8601_str == '2021-11-13T11:49:20.673681'

        dt_obj = parse_native_datetime(dt_iso8601_str)

        assert dt_obj == datetime.datetime(2021, 11, 13, 11, 49, 20, 673681)

    def test_parse_dt_aware_isoformat(self):
        """Test isoformat(): +09:00 format."""
        # isoformat function drops microseconds part if its value is 000000
        dt_aware_src_obj = datetime.datetime(
            2021, 11, 13, 11, 49, 20, 0, datetime.timezone(datetime.timedelta(hours=9))
        )

        dt_iso8601_str = dt_aware_src_obj.isoformat(timespec='microseconds')  # Python 3.6 or later
        assert dt_iso8601_str == '2021-11-13T11:49:20.000000+09:00', (
            f"isoformat()={dt_iso8601_str}"
        )
        dt_aware_dst_obj = parse_aware_datetime(dt_iso8601_str)
        assert dt_aware_dst_obj == dt_aware_src_obj

        # with millisecond
        dt_aware_src_obj = datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681, datetime.timezone(datetime.timedelta(hours=9))
        )
        dt_iso8601_str = dt_aware_src_obj.isoformat()
        assert dt_iso8601_str == '2021-11-13T11:49:20.673681+09:00', (
            f"isoformat()={dt_iso8601_str}"
        )
        dt_aware_dst_obj = parse_aware_datetime(dt_iso8601_str)
        assert dt_aware_dst_obj == dt_aware_src_obj

    def test_parse_dt_aware_strftime(self):
        """Test strftime(): +0900 format."""
        dt_aware_src_obj = datetime.datetime(
            2021, 11, 13, 11, 49, 20, 0, datetime.timezone(datetime.timedelta(hours=9))
        )

        dt_iso8601_str = dt_aware_src_obj.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        assert dt_iso8601_str == '2021-11-13T11:49:20.000000+0900', (
            f"strftime('%Y-%m-%dT%H:%M:%S.%f%z')={dt_iso8601_str}"
        )
        dt_aware_dst_obj = parse_aware_datetime(dt_iso8601_str)
        assert dt_aware_dst_obj == dt_aware_src_obj

        # with millisecond
        dt_aware_src_obj = datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681, datetime.timezone(datetime.timedelta(hours=9))
        )

        dt_iso8601_str = dt_aware_src_obj.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        assert dt_iso8601_str == '2021-11-13T11:49:20.673681+0900', (
            f"strftime('%Y-%m-%dT%H:%M:%S.%f%z')={dt_iso8601_str}"
        )
        dt_aware_dst_obj = parse_aware_datetime(dt_iso8601_str)
        assert dt_aware_dst_obj == dt_aware_src_obj

    def test_timezone_utc_to_jst(self):
        """Test convert the timezone from UTC to JST."""
        datetime_utc = datetime.datetime.strptime('2021-11-13T02:49:20.673681+00:00', '%Y-%m-%dT%H:%M:%S.%f%z')
        datetime_jst = datetime_utc.astimezone(datetime.timezone(datetime.timedelta(hours=+9)))
        assert datetime_jst == datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681, tzinfo=datetime.timezone(datetime.timedelta(hours=9))
        )

    def test_timezone_jst_to_utc(self):
        """Test convert the timezone from UTC to JST."""
        datetime_jst = datetime.datetime.strptime('2021-11-13T11:49:20.673681+09:00', '%Y-%m-%dT%H:%M:%S.%f%z')
        datetime_utc = datetime_jst.astimezone(datetime.timezone.utc)
        assert datetime_utc == datetime.datetime(
            2021, 11, 13, 2, 49, 20, 673681, tzinfo=datetime.timezone(datetime.timedelta(hours=0))
        )

    def test_timezone_native_jst_to_aware_jst_combine(self):
        """Test convert the timezone from UTC to JST."""
        datetime_native_jst = datetime.datetime.strptime(
            '2021-11-13T11:49:20.673681', '%Y-%m-%dT%H:%M:%S.%f'
        )
        datetime_aware_jst = datetime.datetime.combine(
            datetime_native_jst.date(), datetime_native_jst.time(),
            tzinfo=datetime.timezone(datetime.timedelta(hours=9))
        )
        assert datetime_aware_jst == datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681, tzinfo=datetime.timezone(datetime.timedelta(hours=9))
        )

    def test_timezone_native_jst_to_aware_jst_replace(self):
        """Test convert the timezone from UTC to JST."""
        datetime_native_jst = datetime.datetime.strptime(
            '2021-11-13T11:49:20.673681', '%Y-%m-%dT%H:%M:%S.%f'
        )
        datetime_aware_jst = datetime_native_jst.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
        assert datetime_aware_jst == datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681, tzinfo=datetime.timezone(datetime.timedelta(hours=9))
        )

    def test_timezone_aware_to_native(self):
        """Test convert datetime from aware to native."""
        datetime_aware_jst = datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681, tzinfo=datetime.timezone(datetime.timedelta(hours=9))
        )
        datetime_native_jst = datetime_aware_jst.replace(tzinfo=None)
        assert datetime_native_jst == datetime.datetime(
            2021, 11, 13, 11, 49, 20, 673681
        )
