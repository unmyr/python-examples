import sympy
from sympy import sqrt


def main() -> None:
    """Run main."""
    # Definition: Variables and functions
    x, y, z, w = sympy.symbols("x y z w")
    y_x = 2 * x / (1 - x**2)
    z_y = sympy.simplify(2 * y / (1 - y**2))
    w_z = sympy.simplify(2 * z / (1 - z**2))
    x_w = sympy.simplify(2 * w / (1 - w**2))

    # Define the list of initial values
    initial_values = [
        sympy.Number(0),
        -sympy.I,
        sympy.I,
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
        y_out = y_x.subs(x, complex(x_in))
        z_out = z_y.subs(y, complex(y_out))
        w_out = w_z.subs(z, complex(z_out))
        x_out = x_w.subs(w, complex(w_out))

        # Calculate the error
        error = abs(x_out - x_in)

        print(
            f"x={complex(x_in):+2.3f}: "
            + ",".join(
                [
                    f"f^1={complex(y_out):+.3f}",
                    f"f^2={complex(z_out):+.3f}",
                    f"f^3={complex(w_out):+.3f}",
                    f"f^4={complex(x_out):+.3f}",
                    f"error={error:.3f}",
                ]
            )
            + f": x={x_in}"
        )


if __name__ == "__main__":
    main()

# EOF
