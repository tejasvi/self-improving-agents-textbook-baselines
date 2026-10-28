import math

def get_divisors(n):
    """Get all divisors of n up to sqrt(n)"""
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
        i += 1
    return divisors

def isqrt(n):
    """Integer square root"""
    if n < 0:
        return -1
    if n == 0:
        return 0
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def solve(N):
    """Find x, y such that x^3 - y^3 = N"""
    # x^3 - y^3 = (x-y)(x^2 + xy + y^2)
    # Let a = x - y, b = x^2 + xy + y^2
    # Then N = a * b
    # From x = y + a, substituting into x^2 + xy + y^2:
    # (y+a)^2 + (y+a)y + y^2 = b
    # y^2 + 2ay + a^2 + y^2 + ay + y^2 = b
    # 3y^2 + 3ay + a^2 = b
    # 3y^2 + 3ay + (a^2 - b) = 0
    # y = (-3a ± sqrt(9a^2 - 12(a^2 - b))) / 6
    # y = (-3a ± sqrt(12b - 3a^2)) / 6
    # y = (-3a ± sqrt(3(4b - a^2))) / 6
    
    divisors = get_divisors(N)
    
    for a in divisors:
        b = N // a
        
        # Check if 3(4b - a^2) is a perfect square
        discriminant = 3 * (4 * b - a * a)
        
        if discriminant < 0:
            continue
        
        sqrt_disc = isqrt(discriminant)
        if sqrt_disc * sqrt_disc != discriminant:
            continue
        
        # y = (-3a + sqrt_disc) / 6 (taking positive root)
        if (-3 * a + sqrt_disc) % 6 != 0:
            continue
        
        y = (-3 * a + sqrt_disc) // 6
        
        if y <= 0:
            continue
        
        x = y + a
        
        if x <= 0:
            continue
        
        # Verify the solution
        if x * x * x - y * y * y == N:
            return x, y
    
    return None

N = int(input())
result = solve(N)

if result is None:
    print(-1)
else:
    x, y = result
    print(x, y)
