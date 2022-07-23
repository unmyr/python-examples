"""Example of decimal."""
import decimal
import time


def calc_add_float(count: int) -> float:
    """Calc add using float."""
    ret = 0.0

    t_0 = time.time()
    for _ in range(1, count + 1):
        ret += 1
    t_1 = time.time()

    return t_1 - t_0


def calc_add_decimal(count: int) -> float:
    """Calc add using decimal."""
    ret = decimal.Decimal(0)

    t_0 = time.time()
    for _ in range(1, count + 1):
        ret += decimal.Decimal("1")
    t_1 = time.time()

    return t_1 - t_0


def calc_mul_float(count: int) -> float:
    """Calc multiplication using float."""
    ret = 2**63 - 1

    t_0 = time.time()
    for _ in range(1, count + 1):
        ret *= 0.000001
    t_1 = time.time()

    return t_1 - t_0


def calc_mul_decimal(count: int) -> float:
    """Calc multiplication using decimal."""
    ret = decimal.Decimal(2**63 - 1)

    t_0 = time.time()
    for _ in range(1, count + 1):
        ret *= decimal.Decimal("0.000001")
    t_1 = time.time()

    return t_1 - t_0


def calc_div_float(count: int) -> float:
    """Calc division using float."""
    ret = 2**63 - 1

    t_0 = time.time()
    for _ in range(1, count + 1):
        ret /= 0.000001
    t_1 = time.time()

    return t_1 - t_0


def calc_div_decimal(count: int) -> float:
    """Calc division using decimal."""
    ret = decimal.Decimal(2**63 - 1)

    t_0 = time.time()
    for _ in range(1, count + 1):
        ret /= decimal.Decimal("0.000001")
    t_1 = time.time()

    return t_1 - t_0


def main() -> None:
    """Run main."""
    count = 100000
    elapsed_time_float_add = calc_add_float(count)
    elapsed_time_decimal_add = calc_add_decimal(count)
    print(
        "plus: float={:.4f}, decimal={:.4f}, rate={:.3f}".format(
            elapsed_time_float_add, elapsed_time_decimal_add,
            elapsed_time_decimal_add / elapsed_time_float_add
        )
    )

    elapsed_time_float_mul = calc_div_float(count)
    elapsed_time_decimal_mul = calc_div_decimal(count)
    print(
        " mul: float={:.4f}, decimal={:.4f}, rate={:.3f}".format(
            elapsed_time_float_mul, elapsed_time_decimal_mul,
            elapsed_time_decimal_mul / elapsed_time_float_mul
        )
    )

    elapsed_time_float_div = calc_div_float(count)
    elapsed_time_decimal_div = calc_div_decimal(count)
    print(
        " div: float={:.4f}, decimal={:.4f}, rate={:.3f}".format(
            elapsed_time_float_div, elapsed_time_decimal_div,
            elapsed_time_decimal_div / elapsed_time_float_div
        )
    )


if __name__ == '__main__':
    main()

# EOF
