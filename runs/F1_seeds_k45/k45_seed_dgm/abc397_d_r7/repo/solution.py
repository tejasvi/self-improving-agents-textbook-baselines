import math
from math import isqrt

def get_divisors(n):
    """Get all divisors of n"""
    divisors = []
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sorted(divisors)

def solve(N):
    """
    Find positive integers (x, y) such that x^3 - y^3 = N
    
    Using: x^3 - y^3 = (x - y)(x^2 + xy + y^2)
    Let d = x - y, then: d(x^2 + xy + y^2) = N
    
    Since x = y + d:
    d((y+d)^2 + (y+d)y + y^2) = N
    d(y^2 + 2dy + d^2 + y^2 + dy + y^2) = N
    d(3y^2 + 3dy + d^2) = N
    
    So: 3y^2 + 3dy + d^2 = N/d
    Which gives quadratic: 3y^2 + 3dy + (d^2 - N/d) = 0
    
    Using quadratic formula:
    y = (-3d ± sqrt(9d^2 - 12(d^2 - N/d))) / 6
    y = (-3d ± sqrt(12N/d - 3d^2)) / 6
    """
    
    divisors = get_divisors(N)
    
    for d in divisors:
        quotient = N // d
        
        # Calculate discriminant: 12N/d - 3d^2
        discriminant = 12 * quotient - 3 * d * d
        
        if discriminant < 0:
            continue
        
        sqrt_disc = isqrt(discriminant)
        
        # Check if discriminant is a perfect square
        if sqrt_disc * sqrt_disc != discriminant:
            continue
        
        # y = (-3d + sqrt_disc) / 6  (we want positive y)
        numerator = -3 * d + sqrt_disc
        
        if numerator <= 0 or numerator % 6 != 0:
            continue
        
        y = numerator // 6
        x = y + d
        
        # Verify the solution
        if x > 0 and y > 0 and x * x * x - y * y * y == N:
            return (x, y)
    
    return None

# Read input
N = int(input())

# Solve
result = solve(N)

# Output
if result is None:
    print(-1)
else:
    print(result[0], result[1])
