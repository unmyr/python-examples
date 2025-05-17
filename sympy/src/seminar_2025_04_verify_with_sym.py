import sympy


def replace_with_CRootOf_if_close(val, roots, tol=1e-8):
    """
    If val is numerically close to any CRootOf in roots, return that CRootOf, else return val.
    """
    val_num = complex(sympy.N(val))
    for root in roots:
        root_num = complex(root.evalf())
        if abs(val_num - root_num) < tol:
            return root
    return val


def process_and_replace(val, roots_x4, roots_x8):
    """
    Replace val with a matching CRootOf from roots_x4 or roots_x8 if close.
    """
    val = replace_with_CRootOf_if_close(val, roots_x4)
    val = replace_with_CRootOf_if_close(val, roots_x8)
    return val


def main() -> None:
    """Run main."""
    # Definition: Variables and functions
    x, y, z, w = sympy.symbols("x y z w")
    roots_x4 = sympy.all_roots(x**4 - 10 * x**2 + 5)
    roots_x8 = sympy.all_roots(x**8 - 92 * x**6 + 134 * x**4 - 28 * x**2 + 1)
    y_x = 2 * x / (1 - x**2)
    z_y = sympy.simplify(2 * y / (1 - y**2))
    w_z = sympy.simplify(2 * z / (1 - z**2))
    x_w = sympy.simplify(2 * w / (1 - w**2))

    # Define the list of initial values
    initial_values = (
        [
            sympy.Number(0),
        ]
        + sympy.all_roots(x**2 + 1)
        + sympy.real_roots((x**2 - 3), x)
        + roots_x4
        + roots_x8
    )

    # Print Asciidoc table header
    print('[options="header, autowidth"]')
    print("|===")
    print("|x:in |y |z |w |x:out |error")

    # Apply the function f to the initial values and output the results
    for x_in in initial_values:
        # Apply the function f four times, replacing with CRootOf if close
        y_out = sympy.simplify(y_x.subs(x, x_in))
        y_out = process_and_replace(y_out, roots_x4, roots_x8)
        z_out = sympy.simplify(z_y.subs(y, y_out))
        z_out = process_and_replace(z_out, roots_x4, roots_x8)
        w_out = sympy.simplify(w_z.subs(z, z_out))
        w_out = process_and_replace(w_out, roots_x4, roots_x8)
        x_out = sympy.simplify(x_w.subs(w, w_out))
        x_out = process_and_replace(x_out, roots_x4, roots_x8)
        error = sympy.N(x_out - x_in)

        print(
            "| "
            + "| ".join(
                [
                    " latexmath:[" + sympy.latex(val) + "] "
                    for val in [x_in, y_out, z_out, w_out, x_out]
                ]
            )
            + f"|{sympy.latex(error)}"
        )

    print("|===")


if __name__ == "__main__":
    main()

# EOF
