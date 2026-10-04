import sympy
from sympy import symbols
import sympy.diffgeom

# Calculate the differential form ω in polar coordinates
# (r, θ) from the given Cartesian coordinates (x, y)
# \omega = -(-2x + 3y) dx + (x - 3y) dy

# Define a 2D manifold and coordinate system
m = sympy.diffgeom.Manifold("M", 2)
patch = sympy.diffgeom.Patch("P", m)
xy_coords = sympy.diffgeom.CoordSystem("xy", patch, symbols("x y", real=True))
xy_oneforms = xy_coords.base_oneforms()
dx: sympy.Expr = xy_oneforms[0]
dy: sympy.Expr = xy_oneforms[1]
polar_coords = sympy.diffgeom.CoordSystem("polar", patch, symbols("r θ", real=True))
polar_oneforms = polar_coords.base_oneforms()
dr: sympy.Expr = polar_oneforms[0]
dtheta: sympy.Expr = polar_oneforms[1]

# Define symbols
x, y, r, theta = symbols("x y r theta")

# 1-form in (x, y)
omega_xy = (-(-2 * x + 3 * y)) * dx + (x - 3 * y) * dy

# Coordinate transformation: Cartesian -> Polar
x_r_theta = r * sympy.cos(theta)
y_r_theta = r * sympy.sin(theta)

# Transform the 1-form ω from Cartesian coordinates (x, y) to polar coordinates (r, θ)
omega_rt = sympy.simplify(
    sympy.expand(
        omega_xy.subs(
            {
                x: x_r_theta,
                y: y_r_theta,
                dx: sympy.diff(x_r_theta, r) * dr + sympy.diff(x_r_theta, theta) * dtheta,  # type: ignore
                dy: sympy.diff(y_r_theta, r) * dr + sympy.diff(y_r_theta, theta) * dtheta,  # type: ignore
            }
        )
    ),
    deep=False,
)  # type: ignore

# Print the results
print(f"Original 1-form ω in (x, y): ω = ({omega_xy.coeff(dx)}) dx + ({omega_xy.coeff(dy)}) dy")
print(
    f"Transformed 1-form ω in (r, θ): ω=({omega_rt.coeff(dr)}) dr + ({omega_rt.coeff(dtheta)}) dθ"
)
