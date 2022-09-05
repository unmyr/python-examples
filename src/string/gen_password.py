"""Generate passwords."""
import secrets
import string
import typing


def gen_passwords() -> typing.List:
    """Generate password."""
    alphabet = string.ascii_letters + string.digits + '%^*(-_=+)'
    return sorted([''.join(secrets.choice(alphabet) for i in range(12)) for j in range(10)])


if __name__ == '__main__':
    _ = [print(p) for p in gen_passwords()]

# EOF
