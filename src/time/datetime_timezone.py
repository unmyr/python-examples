"""Example of datetime."""
import datetime


def main() -> None:
    """Run main."""
    dt_aware_obj = datetime.datetime.now(
        datetime.timezone.utc
    ).astimezone()

    print(f"dt_aware_obj = {dt_aware_obj.isoformat()}")


if __name__ == "__main__":
    main()
