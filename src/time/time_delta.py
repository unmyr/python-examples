"""Calculate the time delta."""
import datetime
import time


def sleep_with_time(sec: float) -> float:
    """Example of time.time()"""
    t_0: float
    t_1: float

    t_0 = time.time()
    time.sleep(sec)
    t_1 = time.time()

    time_delta: float
    time_delta = t_1 - t_0

    return time_delta


def sleep_with_datetime(sec: float) -> float:
    """Example of datetime.datetime.now()"""
    t_0: "datetime.datetime"
    t_1: "datetime.datetime"

    t_0 = datetime.datetime.now()
    time.sleep(sec)
    t_1 = datetime.datetime.now()

    time_delta: datetime.timedelta
    time_delta = t_1 - t_0

    assert isinstance(t_0, datetime.datetime)
    assert isinstance(t_1, datetime.datetime)
    assert isinstance(time_delta, datetime.timedelta)

    return time_delta.total_seconds()


def main() -> None:
    """Run main."""
    print("dt = %f" % (sleep_with_time(0.8)))
    print("dt = %f" % (sleep_with_datetime(0.8)))


if __name__ == "__main__":
    main()
