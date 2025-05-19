import sympy


def format_latex_array(solutions):
    """
    Format a list of solutions into a LaTeX array for display.
    """
    latex_solutions = [sympy.latex(sol) for sol in solutions]
    return (
        "\\begin{align*}\n"
        "x = \\left[\n"
        "  \\begin{array}{c}\n" + " \\\\\n".join(latex_solutions) + "\n  \\end{array}\n"
        "\\right]\n"
        "\\end{align*}"
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


def main() -> None:
    """Run main."""
    # Define symbolic variables
    x, y = sympy.symbols("x y")
    sympy.init_printing(use_unicode=True)

    # Define polynomials
    y_of_x = (2 * x) / (1 - x**2)  # Polynomial: (2x)/(1 - x²)
    z_of_y = (2 * y) / (1 - y**2)  # Polynomial: (2y)/(1 - y²)

    try:
        z_of_x = sympy.simplify(z_of_y.subs(y, y_of_x))

        # Factor the polynomial: z = (2y)/(1 - y²), y = (2x)/(1 - x²), z=x
        z_eq_plus_x_eq = sympy.factor(x - z_of_x)
        z_eq_plus_x_solved = sympy.solveset(z_eq_plus_x_eq, x, domain=sympy.S.Complexes)
        print_adoc_latexmath_content(
            "Factored result: f{nbsp}^2^=e",
            "\n".join(
                [
                    "\\begin{align*}",
                    "z\\left.\\right|_{z=x} &= " + f"{sympy.latex(sympy.factor(z_of_x))}" + " \\\\",
                    f"0 &= {sympy.latex(z_eq_plus_x_eq)} \\\\",
                    f"x &= {sympy.latex(z_eq_plus_x_solved)} \\\\",
                    "\\end{align*}",
                ]
            ),
        )

        # Factor the polynomial: z = (2y)/(1 - y²), y = (2x)/(1 - x²), z=-x
        z_eq_minus_x_eq = sympy.factor(x + z_of_x)
        z_eq_minus_x_solved = sympy.solveset(z_eq_minus_x_eq, x, domain=sympy.S.Complexes)
        print_adoc_latexmath_content(
            "Factored result: f{nbsp}^2^=f{nbsp}^-1^",
            "\n".join(
                [
                    "\\begin{align*}",
                    "z\\left.\\right|_{z=-x} &= "
                    + f"{sympy.latex(sympy.factor(z_of_y.subs(y, y_of_x)))}"
                    + " \\\\",
                    f"0 &= {sympy.latex(z_eq_minus_x_eq)} \\\\",
                    f"x &= {sympy.latex(z_eq_minus_x_solved)} \\\\",
                    "\\end{align*}",
                ]
            ),
        )

    except Exception as e:
        print(f"ERROR: An error occurred while simplifying the polynomial: {e}")


if __name__ == "__main__":
    main()

# EOF
