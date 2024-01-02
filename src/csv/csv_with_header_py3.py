"""Example of csv"""
import csv
import datetime
import typing


def write_to_csv(csv_path: str) -> None:
    """Write to csv."""
    with open(csv_path, "w") as file_writer:
        header = ["timestamp", "code", "message", "val1", "val2", "val3"]
        csv_writer = csv.writer(file_writer)
        csv_writer.writerow(header)
        dt_0 = datetime.datetime(2021, 11, 10, 11, 12, 13)
        dt_1 = datetime.datetime(2021, 11, 11, 23, 59, 59)

        row = [dt_0, 10, "Hello", *[1, 2, 3]]
        csv_writer.writerow(row)
        row = [dt_1, 11, "こんにちは", *[4, 5, 6]]
        csv_writer.writerow(row)


def read_from_csv(csv_path: str) -> None:
    """Read from csv."""
    with open(csv_path, "r") as file_reader:
        reader = csv.reader(file_reader)
        row: typing.List[str]
        for row in reader:
            print(",".join(row))


def main() -> None:
    """Run main."""
    write_to_csv("sample.csv")
    read_from_csv("sample.csv")


if __name__ == "__main__":
    main()

# EOF
