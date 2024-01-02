import math

for n in range(1, 8):
    print(
        "{:02d} {:19d} {:.1f} KiB".format(
            n, math.factorial(n), math.factorial(n) * n * 4 / 1024
        )
    )

for n in range(8, 12):
    print(
        "{:02d} {:19d} {:.0f} MiB".format(
            n, math.factorial(n), math.factorial(n) * n * 4 / (1024 * 1024)
        )
    )

for n in range(12, 14):
    print(
        "{:02d} {:19d} {:.0f} GiB".format(
            n, math.factorial(n), math.factorial(n) * n * 4 / (1024 * 1024 * 1024)
        )
    )

for n in range(14, 17):
    print(
        "{:02d} {:19d} {:.0f} TiB".format(
            n,
            math.factorial(n),
            math.factorial(n) * n * 4 / (1024 * 1024 * 1024 * 1024),
        )
    )

for n in range(17, 19):
    print(
        "{:02d} {:19d} {:.0f} PiB".format(
            n,
            math.factorial(n),
            math.factorial(n) * n * 4 / (1024 * 1024 * 1024 * 1024 * 1024),
        )
    )

for n in range(19, 21):
    print(
        "{:02d} {:19d} {:.0f} EiB".format(
            n,
            math.factorial(n),
            math.factorial(n) * n * 4 / (1024 * 1024 * 1024 * 1024 * 1024 * 1024),
        )
    )
