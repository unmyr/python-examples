"""Convert all keys of a dictionary into lowercase."""


def main():
    """Run main."""
    my_dict1 = {
        'A': 1, 'B': 2,
        'C': {'D': 3, 'E': 4},
        True: False,
        4098: 'F',
        ('T0', 'T1'): 'TV'
    }

    str_lowered = repr(my_dict1).lower().replace(
        ' true:', ' True:'
    ).replace(
        ' false,', ' False,'
    )
    # pylint: disable=eval-used
    d_1 = eval(str_lowered)
    print(d_1)


if __name__ == '__main__':
    main()

# EOF
