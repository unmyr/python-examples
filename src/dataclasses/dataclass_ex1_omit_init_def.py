"""Example of dataclass."""
import dataclasses
import typing


@dataclasses.dataclass
class User:
    """Example of dataclass."""
    name: str
    age: int = 0

    def aging(self) -> typing.NoReturn:
        """Aging."""
        self.age += 1


if __name__ == '__main__':
    user1 = User('John', 99)
    assert user1.name == 'John'
    assert user1.age == 99
    user1.aging()
    assert user1.age == 100

    user2 = User('Mary')
    assert user2.name == 'Mary'
    assert user2.age == 0
    user2.age = 10
    assert user2.age == 10

    print(f'user1={user1}, user2={user2}')
