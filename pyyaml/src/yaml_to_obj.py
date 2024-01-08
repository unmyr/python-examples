"""Load yaml."""
import pprint
import sys
import typing

import yaml


def yaml_to_obj(
    file_handler_or_str: typing.Union[str, typing.IO],
) -> typing.Union[dict, list, None]:
    """Convert yaml to json"""
    return yaml.safe_load(file_handler_or_str)


def main(yaml_filename: str) -> None:
    """Run main."""
    pp = pprint.PrettyPrinter(indent=2)
    with open(yaml_filename, "rb") as f:
        pp.pprint(yaml_to_obj(f))


if __name__ == "__main__":
    main(sys.argv[1])

# EOF
