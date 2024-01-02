"""Share global variables across modules."""
from sub import get_my_dict
from sub import MY_DICT  # pylint: disable=unused-import
from sub import MY_LIST
import sub


def main():
    """Run main."""
    MY_LIST.append("d")
    print(f"MY_LIST={MY_LIST}")
    assert id(MY_DICT) == id(sub.MY_DICT)
    assert sub.get_my_list() == ["a", "b", "c", "d"]
    # MY_LIST = ['a', 'b', 'c', 'd', 'e']  # NG
    print()

    # OK
    assert isinstance(sub.MY_DICT, dict)
    assert len(sub.MY_DICT) == 0
    sub.MY_DICT = {"message": "Hello world"}
    print(f"sub.MY_DICT=(id:{id(sub.MY_DICT)}) {sub.MY_DICT}")
    print(f"    MY_DICT=(id:{id(MY_DICT)}) {MY_DICT}")
    assert id(MY_DICT) != id(sub.MY_DICT)
    assert get_my_dict().get("message") == "Hello world"
    print()

    # NG: Redefining name 'MY_DICT' from outer scope (line 3)
    # MY_DICT = {'message': 'Hello world'}
    # print(f"MY_DICT={MY_DICT}")
    # print(get_my_dict())  # -> None

    sub.init_tuple(("Hello", "world"))
    print(f"sub.MY_TUPLE={sub.MY_TUPLE}")
    from sub import MY_TUPLE  # pylint: disable=import-outside-toplevel

    print(f"    MY_TUPLE={MY_TUPLE}")
    assert id(MY_TUPLE) == id(sub.MY_TUPLE)
    print()


if __name__ == "__main__":
    main()

# EOF
