import sympy


def format_latex_array(solutions):
    """
    Format a list of solutions into a LaTeX array for display.
    """
    latex_solutions = ["    & " + sympy.latex(sol) for sol in solutions]
    return (
        "\\begin{array}{ll}\n"
        "(x, y, z, w) = \\{ & \\\\\n"
        "  \\begin{array}{l}\n" + ", \\\\\n".join(latex_solutions) + "\\\\ \n  \\end{array} \\\\ \n"
        "\\} & \\\\\n"
        "\\end{array}"
    )


def print_adoc_latexmath_content(title, content):
    """
    Print a AsciiDoc latexmath section with a title.
    """
    print("[latexmath]")
    print(f".{title}")
    print("++++")
    print(content)
    print("++++")
    print("")


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


def main() -> None:
    """Run main."""
    # Initialize sympy printing
    sympy.init_printing(use_unicode=True)

    # Define symbolic variables
    x, y, z, w = sympy.symbols("x y z w")

    # Defile roots
    roots_x4 = sympy.all_roots(x**4 - 10 * x**2 + 5)
    roots_x8 = sympy.all_roots(x**8 - 92 * x**6 + 134 * x**4 - 28 * x**2 + 1)
    roots = roots_x4 + roots_x8

    try:
        # Solve the equation using solve
        solution_solve = sympy.solve(
            [
                y - (2 * x) / (1 - x**2),
                z - (2 * y) / (1 - y**2),
                w - (2 * z) / (1 - z**2),
                x - (2 * w) / (1 - w**2),
            ],
            [x, y, z, w],
            domain=sympy.S.Complexes,
        )
        print_adoc_latexmath_content("Solution using solve", format_latex_array(solution_solve))

        # Solve the equation using solveset
        solution_solveset_of_x = sympy.solveset(
            sympy.simplify(
                (x - (2 * w) / (1 - w**2))
                .subs(w, (2 * z) / (1 - z**2))
                .subs(z, (2 * y) / (1 - y**2))
                .subs(y, (2 * x) / (1 - x**2))
            ),
            x,
            domain=sympy.S.Complexes,
        )

        results = []
        for x_in in solution_solveset_of_x:
            y_out = replace_with_CRootOf_if_close(((2 * x) / (1 - x**2)).subs(x, x_in), roots)
            z_out = replace_with_CRootOf_if_close(((2 * y) / (1 - y**2)).subs(y, y_out), roots)
            w_out = replace_with_CRootOf_if_close(((2 * z) / (1 - z**2)).subs(z, z_out), roots)
            results.append(
                (
                    x_in,
                    y_out,
                    z_out,
                    w_out,
                )
            )
        print_adoc_latexmath_content("Solution using solveset", format_latex_array(results))

    except Exception as e:
        print(f"ERROR: An error occurred while simplifying the polynomial: {e}")


if __name__ == "__main__":
    main()

# EOF
