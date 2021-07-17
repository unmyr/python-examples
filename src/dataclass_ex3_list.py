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
