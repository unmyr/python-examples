"""Convert all keys of a dictionary into lowercase."""
from collections.abc import Iterable
import typing


def rename_dict_keys_all(obj: typing.Any) -> typing.Any:
    """Rename dict keys all."""
    if isinstance(obj, str):
        # Value of string
        return obj.upper()

    elif isinstance(obj, dict):
        # Dict
        # return {
        #     k.lower() if isinstance(k, str) else k: rename_dict_keys_all(v) for k, v in obj.items()
        # }
        new_dict = {}
        for k, v in obj.items():
            new_key = None
            if isinstance(k, str):
                new_key = k.lower()
            else:
                new_key = k

            new_dict[new_key] = rename_dict_keys_all(v)

        return new_dict

    elif isinstance(obj, tuple):
        # tuple
        # new_list = []
        # for item in obj:
        #     new_list.append(rename_dict_keys_all(item))
        # return tuple(new_list)
        return tuple(map(rename_dict_keys_all, obj))

    elif isinstance(obj, Iterable):
        # list (or the like)
        # new_list = []
        # for item in obj:
        #     new_list.append(rename_dict_keys_all(item))
        # return new_list
        return list(map(rename_dict_keys_all, obj))

    else:
        # anything else
        return obj


def main():
    """Run main."""
    org_dict1 = {
        "Str-Key": "Val:Str",
        "Baz": {"BazA": "Val1", "BazB": 4},
        4098: "Val:number",
        3.14: "Val:float",
        True: "True",
        ("T0", "T1"): "TV",
        "ArrayKey": ["a1", "a2"],
        "Tuple-Key": ("t1", "t2", {"FOO": "bar"}),
        "Num-Key": 1234,
        "Float-Key": 3.14,
    }
    new_dict = rename_dict_keys_all(org_dict1)
    print(new_dict)

    org_list1 = ["foo", True, False, None, float("inf"), ("foo", "bar")]
    new_list1 = rename_dict_keys_all(org_list1)
    print(new_list1)


if __name__ == "__main__":
    main()

# EOF
