"""Example of typing."""
import typing


def get_my_list() -> (
    typing.List[typing.Union[float, typing.List[int], typing.Tuple[float, int, str]]]
):
    """Get current datetime."""
    my_list: typing.List[
        typing.Union[float, typing.List[int], typing.Tuple[float, int, str]]
    ]
    my_list = []
    my_list.append(3.14)
    my_list.append([1, 2])
    my_list.append((3.14, 4, "Hello"))
    return my_list


def append_int(in_list: typing.List[int], val: int) -> typing.List[int]:
    """Get string."""
    in_list.append(val)
    return in_list


def main() -> None:
    """Run main."""
    my_list: typing.Iterable
    my_list = get_my_list()
    for item in my_list:
        print(item)

    number_List: typing.Iterable = append_int([1, 2, 3], 4)
    print(list(map(lambda x: x * x, number_List)))


if __name__ == "__main__":
    main()

# EOF
