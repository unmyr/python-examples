"""Python for Loop explained with examples."""


def main() -> None:
    """Run main."""
    makers = ['Toyota', 'Nissan', 'Honda']
    for maker_name in makers:
        print(maker_name)

    for i, maker_name in enumerate(makers):
        print(f'{i}: {maker_name}')

    ary = []
    for i in range(5):
        ary.append(i)
    assert ary == [0, 1, 2, 3, 4]

    ary.clear()
    for i in range(5):
        if i == 3:
            continue
        ary.append(i)
    assert ary == [0, 1, 2, 4]


if __name__ == '__main__':
    main()

# EOF
