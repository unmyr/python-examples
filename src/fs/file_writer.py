# -*- coding: utf-8 -*-
"""Writing to file in Python."""
import sys


def main():
    """Run main."""
    with open(sys.argv[1], "w") as file_handle:
        file_handle.write("Pythonでファイルに書き込みました！")


if __name__ == "__main__":
    main()

# EOF
