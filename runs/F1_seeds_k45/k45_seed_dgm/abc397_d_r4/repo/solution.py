import math

def is_perfect_square(n):
    """Check if n is a perfect square and return its square root if it is."""
    if n < 0:
        return False, 0
    root = int(math.sqrt(n))
    # Check root and nearby values due to floating point errors
    for r in [root - 1, root, root + 1]:
        if r >= 0 and r * r == n:
            return True, r
    return False, 0

def solve(N):
    """Find (x, y) such that x^3 - y^3 = N."""
    # x^3 - y^3 = (x-y)(x^2 + xy + y^2) = N
    # Let d = x - y, then x = y + d
    # d * ((y+d)^2 + (y+d)*y + y^2) = N
    # d * (3y^2 + 3dy + d^2) = N
    # So: 3y^2 + 3dy + (d^2 - N/d) = 0
    
    # For d to be valid, N must be divisible by d
    # d must satisfy d^3 <= N roughly (since x > y)
    # More precisely, for y >= 1: d(3 + 3d + d^2) <= N, so d is limited
    
    # We'll iterate through potential values of d
    # d ranges from 1 to roughly N^(1/3)
    max_d = int(N**(1/3)) + 100
    
    for d in range(1, max_d + 1):
        if N % d != 0:
            continue
        
        quotient = N // d
        # We need: 3y^2 + 3dy + d^2 = quotient
        # Rearranging: 3y^2 + 3dy + (d^2 - quotient) = 0
        # Discriminant: 9d^2 - 12(d^2 - quotient) = -3d^2 + 12*quotient
        
        discriminant = 12 * quotient - 3 * d * d
        
        if discriminant < 0:
            continue
        
        is_square, sqrt_disc = is_perfect_square(discriminant)
        if not is_square:
            continue
        
        # y = (-3d ± sqrt_disc) / 6
        
        # Try both roots
        for sign in [1, -1]:
            numerator = -3 * d + sign * sqrt_disc
            if numerator % 6 == 0:
                y = numerator // 6
                if y > 0:
                    x = y + d
                    # Verify the solution
                    if x > 0 and x * x * x - y * y * y == N:
                        return x, y
    
    return None

N = int(input())
result = solve(N)
if result:
    x, y = result
    print(x, y)
else:
    print(-1)
