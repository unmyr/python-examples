"""Example of class."""


class Hoge:
    """Example of class."""

    def _private_method(self):
        """Private method."""
        return "hoge"

    def public_method(self):
        """Public method."""
        return self._private_method()


if __name__ == "__main__":
    print(Hoge()._private_method())

# EOF
