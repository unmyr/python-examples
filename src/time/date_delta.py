"""Calculate the date delta."""
import datetime


def main() -> None:
    """Run main."""
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    delta_date: datetime.timedelta
    delta_date = datetime.date.today() - yesterday
    print(f"days = {delta_date.days}")


if __name__ == "__main__":
    main()
