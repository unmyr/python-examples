import sympy


def format_latex_array(solutions):
    """
    Format a list of solutions into a LaTeX array for display.
    """
    latex_solutions = ["    " + sympy.latex(sol) for sol in solutions]
    return (
        "x = \\left\\{\n"
        "  \\begin{array}{c}\n" + ", \\\\\n".join(latex_solutions) + "\n  \\end{array}\n"
        "\\right\\}"
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
    x, y, z, w = sympy.symbols("x y z w")
    sympy.init_printing(use_unicode=True)

    # Define polynomials
    y_x = (2 * x) / (1 - x**2)  # Polynomial: (2x)/(1 - x²)
    z_y = (2 * y) / (1 - y**2)  # Polynomial: (2y)/(1 - y²)
    w_z = (2 * z) / (1 - z**2)  # Polynomial: (2z)/(1 - z²)
    x_w = (2 * w) / (1 - w**2)  # Polynomial: (2w)/(1 - w²)

    try:
        # Factor all the polynomials
        x_out = sympy.factor(x - x_w.subs(w, w_z).subs(z, z_y).subs(y, y_x))
        print_adoc_latexmath_content("Factored result: f^4^=e", f"0 = {sympy.latex(x_out)}")

        # Solve the equation using solve
        solution_solve = sympy.solve(x_out, x, domain=sympy.S.Complexes)
        print_adoc_latexmath_content("Solution using solve", format_latex_array(solution_solve))

        # Solve the equation using solveset
        solution_solveset = sympy.solveset(x_out, x, domain=sympy.S.Complexes)
        print_adoc_latexmath_content(
            "Solution using solveset", format_latex_array(solution_solveset)
        )

    except Exception as e:
        print(f"ERROR: An error occurred while simplifying the polynomial: {e}")


if __name__ == "__main__":
    main()

# EOF
