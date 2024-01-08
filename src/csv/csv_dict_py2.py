# -*- coding: utf-8 -*-
"""Example of csv"""
import codecs
import csv
import datetime
import os


def write_to_csv(csv_path):
    """Write to csv."""
    with open(csv_path, "w") as file_writer:
        header = ["timestamp", "code", "message", "val1", "val2", "val3"]
        csv_writer = csv.DictWriter(file_writer, fieldnames=header)
        csv_writer.writeheader()
        csv_writer.writerow(
            {
                "timestamp": datetime.datetime(2021, 11, 10, 11, 12, 13),
                "code": 10,
                "message": "Hello",
                "val1": [1, 2, 3][0],
                "val2": [1, 2, 3][1],
                "val3": [1, 2, 3][2],
            }
        )
        csv_writer.writerow(
            {
                "timestamp": datetime.datetime(2021, 11, 11, 23, 59, 59),
                "code": 11,
                "message": u"こんにちは".encode("utf-8"),
                "val1": [4, 5, 6][0],
                "val2": [4, 5, 6][1],
                "val3": [4, 5, 6][2],
            }
        )


def read_from_csv(csv_path):
    """Read from csv."""
    with codecs.open(csv_path, "r") as file_reader:
        reader = csv.DictReader(file_reader)
        for row in reader:
            print(
                ",".join(
                    [
                        row.get("timestamp"),
                        row.get("code"),
                        row.get("message"),
                        row.get("val1"),
                        row.get("val2"),
                        row.get("val3"),
                    ]
                )
            )


def main():
    """Run main."""
    csv_file = "sample.csv"
    write_to_csv(csv_file)
    read_from_csv(csv_file)
    os.remove(csv_file)


if __name__ == "__main__":
    main()

# EOF
