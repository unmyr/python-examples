"""Generate passwords."""
import argparse
import re
import secrets
import string
import typing


def gen_password(pass_len: int) -> str:
    """Generate password."""
    # https://learn.microsoft.com/ja-jp/microsoft-365/admin/misc/password-policy-recommendations?view=o365-worldwide
    # https://docs.oracle.com/cd/E11223_01/doc.910/e11197/app_special_char.htm#MCMAD416
    symbols_ignore: str = "&*,;<=>`|"
    symbols: str = re.sub("[" + symbols_ignore + "]", "", string.punctuation)

    alphabet: str = string.ascii_letters + string.digits + symbols
    password: str = ""
    secrets.randbelow(pass_len)
    password += secrets.choice(string.ascii_lowercase)
    password += secrets.choice(string.ascii_uppercase)
    password += secrets.choice(string.digits)
    password += secrets.choice(symbols)
    password += "".join(secrets.choice(alphabet) for _ in range(pass_len - len(password)))
    password_chars: typing.List = list(password)
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars[0:pass_len])


def main():
    """main."""
    parser = argparse.ArgumentParser(description="Generate passwords.")
    parser.add_argument(
        "password_len",
        type=int,
        nargs="?",
        default=12,
        metavar="L",
        help="password length",
    )
    parser.add_argument(
        "count", type=int, nargs="?", default=6, metavar="N", help="number of passwords"
    )
    args = parser.parse_args()
    for v in sorted([gen_password(args.password_len) for _ in range(args.count)]):
        print(v)


if __name__ == "__main__":
    main()

# EOF
