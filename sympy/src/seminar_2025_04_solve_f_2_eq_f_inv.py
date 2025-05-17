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
    x = sympy.symbols("x")
    sympy.init_printing(use_unicode=True)

    # Define polynomials
    y_of_x = (2 * x) / (1 - x**2)  # Polynomial: (2x₀)/(1 - x²)
    z_of_y = (2 * y_of_x) / (1 - y_of_x**2)  # Polynomial: (2y)/(1 - y²)

    try:
        # calculate z(x)
        simplified_z_of_x = sympy.simplify(z_of_y.subs(y_of_x, y_of_x))
        print_adoc_latexmath_content(
            "Simplified result: f^2^", f"0 = z(x) = {sympy.latex(simplified_z_of_x)}"
        )

        # solve the equation
        simplified_eq = sympy.factor(x + simplified_z_of_x, deep=True, extension=sympy.sqrt(5))
        print_adoc_latexmath_content(
            "Simplified result: f^2^=f^-1^", f"0 = x + z(x) = {sympy.latex(simplified_eq)}"
        )

    except Exception as e:
        print(f"ERROR: An error occurred while simplifying the polynomial: {e}")


if __name__ == "__main__":
    main()

# EOF
