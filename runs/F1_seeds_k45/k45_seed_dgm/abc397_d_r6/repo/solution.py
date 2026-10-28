import math

def find_divisors(n):
    """Find all divisors of n up to a reasonable limit"""
    divisors = []
    # We only need to check divisors up to n
    # But since x^3 - y^3 = (x-y)(x^2+xy+y^2), and x^2+xy+y^2 >= 3y^2
    # If x-y is large, then x^2+xy+y^2 would be small
    # For practical purposes, check divisors up to n
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return sorted(divisors)

def solve(n):
    """Find (x, y) such that x^3 - y^3 = n"""
    divisors = find_divisors(n)
    
    for d in divisors:
        # d = x - y
        # x^2 + xy + y^2 = n / d
        quotient = n // d
        
        # x = y + d
        # (y + d)^2 + (y + d)y + y^2 = quotient
        # y^2 + 2dy + d^2 + y^2 + dy + y^2 = quotient
        # 3y^2 + 3dy + d^2 = quotient
        # 3y^2 + 3dy + (d^2 - quotient) = 0
        
        # Using quadratic formula: y = (-3d ± sqrt(9d^2 - 12(d^2 - quotient))) / 6
        # y = (-3d ± sqrt(9d^2 - 12d^2 + 12*quotient)) / 6
        # y = (-3d ± sqrt(-3d^2 + 12*quotient)) / 6
        # y = (-3d ± sqrt(12*quotient - 3d^2)) / 6
        
        discriminant = 12 * quotient - 3 * d * d
        
        if discriminant < 0:
            continue
        
        sqrt_disc = math.isqrt(discriminant)
        if sqrt_disc * sqrt_disc != discriminant:
            continue
        
        # y = (-3d + sqrt_disc) / 6 or y = (-3d - sqrt_disc) / 6
        if (-3 * d + sqrt_disc) % 6 == 0:
            y = (-3 * d + sqrt_disc) // 6
            if y > 0:
                x = y + d
                if x > 0 and x ** 3 - y ** 3 == n:
                    return (x, y)
        
        if (-3 * d - sqrt_disc) % 6 == 0:
            y = (-3 * d - sqrt_disc) // 6
            if y > 0:
                x = y + d
                if x > 0 and x ** 3 - y ** 3 == n:
                    return (x, y)
    
    return None

n = int(input())
result = solve(n)

if result is None:
    print(-1)
else:
    print(result[0], result[1])
