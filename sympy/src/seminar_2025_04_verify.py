import sympy
from sympy import sqrt


def main() -> None:
    """Run main."""
    # Definition: Variables and functions
    x = sympy.symbols("x")
    f_1 = 2 * x / (1 - x**2)
    # f_2 = sympy.simplify(2 * f_1 / (1 - f_1**2))
    # f_3 = sympy.simplify(2 * f_2 / (1 - f_2**2))
    # f_4 = sympy.simplify(2 * f_3 / (1 - f_3**2))

    # Define the list of initial values
    initial_values = [
        sympy.Number(0),
        sympy.conjugate(-sympy.I),
        sympy.conjugate(sympy.I),
        -sqrt(3),
        sqrt(3),
        -sqrt(5 - 2 * sqrt(5)),
        sqrt(5 - 2 * sqrt(5)),
        -sqrt(5 + 2 * sqrt(5)),
        sqrt(5 + 2 * sqrt(5)),
        -sqrt(23 + 2 * 5 * sqrt(5) + 2 * sqrt(3 * 5 * 17 + 2 * 3 * 19 * sqrt(5))),
        sqrt(23 + 2 * 5 * sqrt(5) + 2 * sqrt(3 * 5 * 17 + 2 * 3 * 19 * sqrt(5))),
        -sqrt(23 - 2 * 5 * sqrt(5) + 2 * sqrt(3 * 5 * 17 - 2 * 3 * 19 * sqrt(5))),
        sqrt(23 - 2 * 5 * sqrt(5) + 2 * sqrt(3 * 5 * 17 - 2 * 3 * 19 * sqrt(5))),
        -sqrt(23 + 2 * 5 * sqrt(5) - 2 * sqrt(3 * 5 * 17 + 2 * 3 * 19 * sqrt(5))),
        sqrt(23 + 2 * 5 * sqrt(5) - 2 * sqrt(3 * 5 * 17 + 2 * 3 * 19 * sqrt(5))),
        -sqrt(23 - 2 * 5 * sqrt(5) - 2 * sqrt(3 * 5 * 17 - 2 * 3 * 19 * sqrt(5))),
        sqrt(23 - 2 * 5 * sqrt(5) - 2 * sqrt(3 * 5 * 17 - 2 * 3 * 19 * sqrt(5))),
        sympy.Number(-1.111),
        sympy.Number(-0.445),
        sympy.Number(-0.213),
    ]

    # Apply the function f to the initial values and output the results
    for x_in in initial_values:
        # Apply the function f four times
        y = complex(f_1.subs(x, x_in))
        z = complex(f_1.subs(x, y))
        w = complex(f_1.subs(x, z))
        x_out = complex(f_1.subs(x, w))
        # y = sympy.simplify(f_1.subs(x, x_in))
        # z = sympy.simplify(f_2.subs(x, x_in))
        # w = sympy.simplify(f_3.subs(x, x_in))
        # x_out = sympy.simplify(f_4.subs(x, x_in))
        error = abs(x_out - x_in)

        print(
            f"x={complex(x_in):+2.3f}: "
            + ",".join(
                [
                    f"f^1={complex(y):+.3f}",
                    f"f^2={complex(z):+.3f}",
                    f"f^3={complex(w):+.3f}",
                    f"f^4={complex(x_out):+.3f}",
                    f"error={error:.3f}",
                ]
            )
            + f": x={x_in}"
        )


if __name__ == "__main__":
    main()

# EOF
