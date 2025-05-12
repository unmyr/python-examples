import sympy
from sympy import symbols, expand

# Define symbolic variables
x = symbols("x")

# Define polynomials
poly1 = x**2 - 5 - 2 * sympy.sqrt(5)  # Polynomial: x² - 5 - 2√5
poly2 = x**2 - 5 + 2 * sympy.sqrt(5)  # Polynomial: x² - 5 + 2√5

# Compute the product and expand
result = expand(poly1 * poly2)  # Result: (x² - 5 - 2√5)(x² - 5 + 2√5) = x⁴ - 10x² + 5
# Print the expanded result
print("Expanded polynomial:", result)

# Factor the result
fact = sympy.factor(
    result, extension=sympy.sqrt(5)
)  # Factor the result => (x² - 5 - 2√5)(x² - 5 + 2√5)
print("Factored polynomial:", fact)  # Print the factored result
