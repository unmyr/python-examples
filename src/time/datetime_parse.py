"""Calculate the date delta."""
import datetime


def main():
    """Run main."""
    dt_str = '2008-09-03T20:56:35.450686Z'
    for time_fmt in ['%Y-%m-%dT%H:%M:%S.Z', '%Y-%m-%dT%H:%M:%S.%fZ']:
        try:
            dt_obj = datetime.datetime.strptime(dt_str, time_fmt)
            break
        except ValueError:
            pass

    assert dt_obj == datetime.datetime(2008, 9, 3, 20, 56, 35, 450686)


if __name__ == "__main__":
    main()
