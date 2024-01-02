"""Convert all keys of a dictionary into lowercase."""
import typing


def rename_dict_keys_toplevel(d: dict, convert_keys: typing.Callable):
    """Rename dict keys."""
    print(type(convert_keys))
    return {convert_keys(k): v for k, v in d.items()}


def main():
    """Run main."""
    my_dict1 = {
        "A": 1,
        "B": 2,
        "C": {"D": 3, "E": 4},
        4098: "F",
        True: "True",
        ("T0", "T1"): "TV",
    }
    d_1 = rename_dict_keys_toplevel(
        my_dict1, lambda k: k.lower() if isinstance(k, str) else k
    )
    print(d_1)


if __name__ == "__main__":
    main()

# EOF
