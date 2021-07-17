"""Example of dataclass."""
import dataclasses
import typing


@dataclasses.dataclass
class ListDataClass:
    """Example of dataclass."""
    list_field: typing.List[int] = dataclasses.field(default_factory=list)

    def add(self, element: int):
        """Add element."""
        self.list_field.append(element)


if __name__ == '__main__':
    o1 = ListDataClass()
    o2 = ListDataClass()
    o1.add(1)
    o1.add(2)
    o2.add(3)
    print(f"o1={o1.list_field} o2={o2.list_field}")
    assert o1.list_field == [1, 2]
    assert o2.list_field == [3]

    my_list = [3, 4]
    o3 = ListDataClass(my_list)
    o4 = ListDataClass(my_list)
    o3.add(5)
    o4.add(6)
    print(f"o3={o3.list_field} o4={o4.list_field}")
    assert o3.list_field == [3, 4, 5, 6]
    assert o4.list_field == [3, 4, 5, 6]
    assert o3.list_field == o4.list_field
