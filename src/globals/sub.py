"""Example of a global variable."""
import typing

MY_LIST: typing.List = ['a', 'b', 'c']
MY_DICT: typing.Dict = {}
MY_TUPLE: typing.Tuple


def get_my_list() -> typing.List:
    """Dump dict."""
    return MY_LIST


def get_my_dict() -> typing.Dict:
    """Dump dict."""
    return MY_DICT


def init_tuple(data: typing.Tuple) -> None:
    """Set tuple."""
    global MY_TUPLE  # pylint: disable=global-statement
    MY_TUPLE = data


# EOF
