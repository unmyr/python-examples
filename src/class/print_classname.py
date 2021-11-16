"""Example of class."""


class Hoge:
    """Example of class."""
    def public_method(self) -> str:
        """Public method."""
        return "Hello world"


def print_class(class_):
    """Print classname."""
    print(class_.__name__)


if __name__ == '__main__':
    print_class(Hoge)

# EOF
