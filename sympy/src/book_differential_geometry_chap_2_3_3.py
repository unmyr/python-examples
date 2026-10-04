import sympy
from sympy import symbols, expand

# Calculate the differential form ω in polar coordinates (r, θ) from the given Cartesian coordinates (x, y)
# \omega = -(-2x + 3y) dx + (x - 3y)dy

# Define symbols
x, y, r, theta = symbols('x y r theta')

# Coordinate transformation: Cartesian -> Polar
x_expr = r * sympy.cos(theta)
y_expr = r * sympy.sin(theta)

# Example 1-form in (x, y)
# You can replace P and Q with any expressions in x, y
omega_r2_x = -(-2*x + 3*y)
omega_r2_y = x - 3*y

# Differentiate x and y with respect to r and theta
dx_dr = sympy.diff(x_expr, r)
dx_dtheta = sympy.diff(x_expr, theta)
dy_dr = sympy.diff(y_expr, r)
dy_dtheta = sympy.diff(y_expr, theta)

# Apply chain rule: dx = (∂x/∂r) dr + (∂x/∂θ) dθ
# Similarly for dy
# In SymPy, we just keep them symbolic as dr, dtheta
dr, dtheta = sympy.symbols('dr dtheta')

dx = dx_dr * dr + dx_dtheta * dtheta
dy = dy_dr * dr + dy_dtheta * dtheta

# Substitute x(r,θ), y(r,θ) into omega_x and omega_y
omega_x_rt = omega_r2_x.subs({x: x_expr, y: y_expr})
omega_y_rt = omega_r2_y.subs({x: x_expr, y: y_expr})

# Transform the 1-form: ω = omega_x dx + omega_y dy
omega_rt = sympy.expand(omega_x_rt * dx + omega_y_rt * dy)

# Display result
print("Original 1-form in (x, y):")
print(f"ω = ({omega_r2_x}) dx + ({omega_r2_y}) dy\n")

print("Transformed 1-form in (r, θ):")
print(sympy.factor(omega_rt))
omega_rt_coeff_dr = sympy.factor(omega_rt.coeff(dr))
# Print the expanded result
print("ωr:", omega_rt_coeff_dr)
omega_rt_coeff_dtheta = sympy.factor(omega_rt.coeff(dtheta))
# Print the expanded result
print("ωθ:", omega_rt_coeff_dtheta)

# Factor the result
print(f"Factored ω(r,θ): ({omega_rt_coeff_dr}) dr + ({omega_rt_coeff_dtheta}) dθ")
