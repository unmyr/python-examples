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
    y_of_x = (2 * x) / (1 - x**2)  # Polynomial: (2x)/(1 - x²)

    try:
        # calculate y(x)
        eq_x = sympy.factor(y_of_x - sympy.conjugate(sympy.I * x))
        print_adoc_latexmath_content(
            "Simplified result: f^1^=ix", f"0 = z(x) = {sympy.latex(eq_x)}"
        )

        # Solve the equation using solve
        solution_solve = sympy.solve(eq_x, x, domain=sympy.S.Complexes)
        print_adoc_latexmath_content("Solution using solve", format_latex_array(solution_solve))

    except Exception as e:
        print(f"ERROR: An error occurred while simplifying the polynomial: {e}")


if __name__ == "__main__":
    main()

# EOF
