import sympy as sym
sym.init_printing()

a, b, x, y, z = sym.symbols('a b x y z')

f = sym.cos(x * y) + sym.sin(z * x)
