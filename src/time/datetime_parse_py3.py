"""Calculate the date delta."""
import datetime
import typing


def parse_native_datetime(dt_iso8601_str: str) -> typing.Optional[datetime.datetime]:
    """Parse native datetime."""
    for time_fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f']:
        try:
            dt_obj = datetime.datetime.strptime(dt_iso8601_str, time_fmt)
            return dt_obj
        except ValueError:
            pass

    return None


def main() -> None:
    """Run main."""
    dt_str = '2008-09-03T20:56:35.450686'
    dt_obj = parse_native_datetime(dt_str)

    assert dt_obj == datetime.datetime(2008, 9, 3, 20, 56, 35, 450686), (
        f"dt_obj={dt_obj}"
    )

    dt_str = '2008-09-03T20:56:35'
    dt_obj = parse_native_datetime(dt_str)

    assert dt_obj == datetime.datetime(2008, 9, 3, 20, 56, 35, 0), (
        f"dt_obj={dt_obj}"
    )


if __name__ == "__main__":
    main()
