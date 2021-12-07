"""Statically overwrite setters/getters."""


class Positive(object):
    """Example."""
    @property
    def my_attr(self):
        """Get my_attr."""
        return self._my_attr

    @my_attr.setter
    def my_attr(self, value: int) -> None:
        """Set my_attr."""
        self._my_attr = abs(value)


def main() -> None:
    """Run main."""
    my_obj = Positive()
    my_obj.my_attr = -3
    print(my_obj.my_attr)


if __name__ == '__main__':
    main()

# EOF
