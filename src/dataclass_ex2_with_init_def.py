"""Example of dataclass."""
from dataclasses import dataclass
import typing


@dataclass
class User:
    """Example of dataclass."""
    name: str
    age: int = 0

    # pylint: disable=unused-argument
    def __init__(self, name: str, age: int = -1):
        """Over write."""
        self.name = 'John Doe'

    def aging(self) -> typing.NoReturn:
        """Aging."""
        self.age += 1


if __name__ == '__main__':
    user1 = User('Ken', 99)
    assert user1.name == 'John Doe'
    assert user1.age == 0
    user1.aging()
    assert user1.age == 1

    user2 = User('Mary')
    assert user2.name == 'John Doe'
    assert user2.age == 0
    user2.name = 'Mary'
    assert user2.name == 'Mary'
