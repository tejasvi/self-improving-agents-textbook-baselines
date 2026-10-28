import math

def get_divisors(n):
    """Get all divisors of n efficiently"""
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return divisors

def is_perfect_square(n):
    """Check if n is a perfect square"""
    if n < 0:
        return False
    root = int(math.isqrt(n))
    return root * root == n

def solve(n):
    """Find x, y such that x^3 - y^3 = n"""
    # x^3 - y^3 = (x - y)(x^2 + xy + y^2) = n
    # Let a = x - y, then x = y + a
    # x^2 + xy + y^2 = (y+a)^2 + (y+a)y + y^2 = 3y^2 + 3ay + a^2
    # So n = a * (3y^2 + 3ay + a^2)
    # For each divisor a of n, we have b = n/a = 3y^2 + 3ay + a^2
    # Solving: 3y^2 + 3ay + (a^2 - b) = 0
    # y = (-3a ± sqrt(9a^2 - 12(a^2 - b))) / 6
    # y = (-3a ± sqrt(12b - 3a^2)) / 6
    
    divisors = get_divisors(n)
    
    for a in divisors:
        b = n // a
        discriminant = 12 * b - 3 * a * a
        
        if discriminant < 0:
            continue
        
        if not is_perfect_square(discriminant):
            continue
        
        sqrt_disc = int(math.isqrt(discriminant))
        
        # y = (-3a + sqrt_disc) / 6  (we need positive y)
        if (-3 * a + sqrt_disc) % 6 == 0:
            y = (-3 * a + sqrt_disc) // 6
            if y > 0:
                x = y + a
                if x > 0 and x * x * x - y * y * y == n:
                    return x, y
        
        # Also try with negative sign
        if (-3 * a - sqrt_disc) % 6 == 0:
            y = (-3 * a - sqrt_disc) // 6
            if y > 0:
                x = y + a
                if x > 0 and x * x * x - y * y * y == n:
                    return x, y
    
    return None

# Read input
n = int(input())
result = solve(n)

if result is None:
    print(-1)
else:
    x, y = result
    print(x, y)
