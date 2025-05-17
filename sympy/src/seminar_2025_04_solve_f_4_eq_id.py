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
    y = (2 * x) / (1 - x**2)  # Polynomial: (2x₀)/(1 - x₀²)
    z = (2 * y) / (1 - y**2)  # Polynomial: (2y)/(1 - y²)
    w = (2 * z) / (1 - z**2)  # Polynomial: (2z)/(1 - z²)
    x_1 = (2 * w) / (1 - w**2)  # Polynomial: (2w)/(1 - w²)

    try:
        # Simplify z
        simplified_z = sympy.simplify(z)
        print_adoc_latexmath_content(
            "Simplified result: f^2^=e", f"z = {sympy.latex(simplified_z)}"
        )

        # Simplify the equation
        simplified_eq = sympy.simplify(x - x_1)

        # Factor x - x_1
        factored_eq = sympy.factor(simplified_eq, deep=True, extension=sympy.sqrt(5))
        print_adoc_latexmath_content("Factored result: f^4^=e", f"0 = {sympy.latex(factored_eq)}")

        # Solve the equation using solve
        solution_solve = sympy.solve(factored_eq, x, domain=sympy.S.Complexes)
        print_adoc_latexmath_content("Solution using solve", format_latex_array(solution_solve))

        # Solve the equation using solveset
        solution_solveset = sympy.solveset(simplified_eq, x, domain=sympy.S.Complexes)
        print_adoc_latexmath_content(
            "Solution using solveset", format_latex_array(solution_solveset)
        )

    except Exception as e:
        print(f"ERROR: An error occurred while simplifying the polynomial: {e}")


if __name__ == "__main__":
    main()

# EOF
