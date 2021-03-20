class Hoge:
    def _private_method(self):
        return "hoge"

    def public_method(self):
        return self._private_method()


if __name__ == '__main__':
    print(Hoge()._private_method())

# EOF
