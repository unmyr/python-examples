"""Example of typing."""
import datetime
import typing


def increment(num: int) -> int:
    """Increment value."""
    num += 1
    return num


def to_lower(in_str: str) -> str:
    """Make it lowercase."""
    return str.lower(in_str)


def get_dict(name: str, age: int) -> typing.Dict:
    """Get string."""
    return {'name': name, 'age': age}


def get_now() -> 'datetime.datetime':
    """Get current datetime."""
    return datetime.datetime.now()


def append_int(
    in_list: typing.List[int], val: int
) -> typing.List[int]:
    """Get string."""
    in_list.append(val)
    return in_list


def get_multiple_returns(
    ret_kind: int
) -> typing.Tuple[str, typing.Union[typing.List, typing.Dict, bytes, str, int, float]]:
    """Example of multiple returns."""
    if ret_kind == 0:
        return "Hello", 3.14
    else:
        return "Hello", True


class User:
    """User"""
    def __init__(self, name: str, age: int) -> None:
        self.name: str = name
        self.age: int = age

    def get_name(self) -> str:
        """Get name."""
        return self.name

    def get_age(self) -> int:
        """Get age."""
        return self.age


def get_timestamps() -> typing.Tuple[User, typing.List]:
    """Get current datetime."""
    perf_list = []
    t_0 = datetime.datetime.now()
    t_1 = datetime.datetime.now()
    t_2 = datetime.datetime.now()
    perf_list.append(round((t_1 - t_0).total_seconds(), 3))
    perf_list.append(round((t_2 - t_1).total_seconds(), 3))
    perf_list.insert(0, round((t_2 - t_0).total_seconds(), 3))
    perf_list.append([1, 2])
    return User('Bob', 28), perf_list


def main() -> None:
    """Run main."""
    user: User
    user = User('Alice', 19)
    print(increment(user.get_age()))

    message: str = to_lower('Hello world.')
    print(message)
    dt_value: 'datetime.datetime' = get_now()
    print(dt_value)

    str_val: str
    float_val: float
    bool_val: bool

    str_val, float_val = typing.cast(
        typing.Tuple[str, float],
        get_multiple_returns(0)
    )
    print(f"{str_val}, {float_val} = get_multiple_returns(0)")

    str_val, bool_val = typing.cast(
        typing.Tuple[str, bool],
        get_multiple_returns(1)
    )
    print(f"{str_val}, {bool_val} = get_multiple_returns(1)")

    number_List: typing.Iterable = append_int([1, 2, 3], 4)
    for elem in number_List:
        print(elem)

    result: typing.List
    user, result = get_timestamps()
    print(f"{user} {result}")


if __name__ == '__main__':
    main()

# EOF
