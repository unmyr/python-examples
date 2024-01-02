"""Dynamically overwrite setters/getters."""


class PropertyExample(object):
    """Add property to a class dynamically."""

    def __init__(self, initial_value):
        attr_name = "my_int_attr"
        field_name = f"__{attr_name}"
        setattr(self, field_name, initial_value)

        getter = lambda obj: getattr(obj, field_name) * -1
        setter = lambda obj, value: setattr(obj, field_name, value + 1)
        setattr(self.__class__, attr_name, property(getter, setter))


def main() -> None:
    """Run main."""
    obj = PropertyExample(0)
    print(obj.my_int_attr)
    obj.my_int_attr = 2  # pylint: disable=attribute-defined-outside-init
    print(obj.my_int_attr)

    PropertyExample.next_one = property(lambda self: self.my_int_attr + 1)
    print(obj.next_one)


if __name__ == "__main__":
    main()

# EOF
