"""Convert yaml to json."""
import json
import datetime
import sys
import typing

import yaml


def json_dumper(obj: typing.Any) -> typing.Any:
    """Dump json."""
    if isinstance(obj, datetime.date):
        # date and datetime
        return obj.isoformat()
    else:
        return obj


def yaml_to_json(yamlFileName: str) -> str:
    """Convert yaml to json"""
    with open(yamlFileName, "rb") as f:
        d = yaml.safe_load(f)
        s = json.dumps(d, default=json_dumper, indent=4)
        return s


if __name__ == "__main__":
    print(yaml_to_json(sys.argv[1]))

# EOF
