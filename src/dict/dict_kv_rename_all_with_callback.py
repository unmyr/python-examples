# -*- coding: utf-8 -*-
"""Example of dict."""
import typing


def recursive(
    data: typing.Any,
    depth: int = -1,
    *,
    dict_func: typing.Callable = lambda x: x,
    iter_func: typing.Callable = lambda x: x,
    value_func: typing.Callable = lambda x: x,
    exclude_iter: typing.List[type] = [str, bytes, bytearray, memoryview],
) -> typing.Any:
    """Example."""
    if depth == 0:
        return data

    if isinstance(data, dict):
        return {
            key: recursive(
                value,
                depth - 1,
                dict_func=dict_func,
                iter_func=iter_func,
                value_func=value_func,
                exclude_iter=exclude_iter,
            )
            for key, value in dict_func(data).items()
        }
    elif isinstance(data, (type(None), bool, int, float, complex, *exclude_iter)):
        # str などの対象外 iterable オブジェクトか否かを判定する
        return value_func(data)
    elif hasattr(data, "__iter__"):
        return [
            recursive(
                i,
                depth - 1,
                dict_func=dict_func,
                iter_func=iter_func,
                value_func=value_func,
                exclude_iter=exclude_iter,
            )
            for i in iter_func(data)
        ]
    else:
        value_func(data)


def main():
    """Run main."""
    org_dict1 = {"Outer": {"Inner": "Value"}}
    new_dict1 = recursive(
        org_dict1, dict_func=lambda x: {key.lower(): value for key, value in x.items()}
    )
    print(f" in={org_dict1}\nout:{new_dict1}\n")

    org_list1 = ["Item1", "Item2", "Item3"]
    new_list1 = recursive(org_list1, iter_func=lambda x: x + [len(x)])
    print(f" in={org_list1}\nout:{new_list1}\n")

    org_list2 = [{"None": "None"}, {"bool": "False"}, {"int": "0"}, {"str": ""}]
    new_list2 = recursive(org_list2, value_func=str)
    print(f" in={org_list2}\nout:{new_list2}\n")


if __name__ == "__main__":
    main()

# EOF
