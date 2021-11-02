"""Convert yaml to json."""
import json
import sys

import yaml


class NoDatesSafeLoader(yaml.SafeLoader):
    """Disable SafeLoader.
    https://stackoverflow.com/questions/34667108/ignore-dates-and-times-while-parsing-yaml
    """
    @classmethod
    def remove_implicit_resolver(cls, tag_to_remove: str) -> None:
        """
        Remove implicit resolvers for a particular tag

        Takes care not to modify resolvers in super classes.

        We want to load datetimes as strings, not dates, because we
        go on to serialize as json which doesn't have the advanced types
        of yaml, and leads to incompatibilities down the track.
        """
        if 'yaml_implicit_resolvers' not in cls.__dict__:
            cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()

        for first_letter, mappings in cls.yaml_implicit_resolvers.items():
            cls.yaml_implicit_resolvers[first_letter] = [
                (tag, regexp) for tag, regexp in mappings if tag != tag_to_remove
            ]


def yaml_to_json(yamlFileName: str) -> str:
    """Convert yaml to json"""
    NoDatesSafeLoader.remove_implicit_resolver('tag:yaml.org,2002:timestamp')

    with open(yamlFileName, 'rb') as f:
        d = yaml.load(f, Loader=NoDatesSafeLoader)
        return json.dumps(d, indent=4)


if __name__ == '__main__':
    print(yaml_to_json(sys.argv[1]))

# EOF
