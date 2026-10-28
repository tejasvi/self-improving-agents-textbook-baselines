import math

def solve():
    N = int(input())
    
    # We need to find positive integers (x, y) such that x^3 - y^3 = N
    # x^3 - y^3 = (x - y)(x^2 + xy + y^2) = N
    # Let a = x - y, b = x^2 + xy + y^2
    # Then a * b = N
    # From x = y + a, we get:
    # (y + a)^2 + (y + a)y + y^2 = b
    # y^2 + 2ay + a^2 + y^2 + ay + y^2 = b
    # 3y^2 + 3ay + a^2 = b
    # 3y^2 + 3ay + (a^2 - b) = 0
    # y = (-3a ± sqrt(9a^2 - 12(a^2 - b))) / 6
    # y = (-3a ± sqrt(12b - 3a^2)) / 6
    # y = (-3a ± sqrt(3(4b - a^2))) / 6
    
    # Limit search to a reasonable bound
    # Maximum value of a = x - y is approximately N^(1/3)
    # For N = 10^18, this is 10^6
    # We use 10^7 as a safe upper bound
    limit = min(10**7, int(N**(1/3)) + 2)
    
    # Collect all divisors up to the limit
    divisors = set()
    i = 1
    while i <= limit and i * i <= N:
        if N % i == 0:
            divisors.add(i)
            if i != N // i:
                divisors.add(N // i)
        i += 1
    
    # Also check divisors that might be > sqrt(N) but <= limit
    # by checking the range where i > sqrt(N) and i <= limit
    if limit > int(N**0.5):
        i = int(N**0.5) + 1
        while i <= limit:
            if N % i == 0:
                divisors.add(i)
            i += 1
    
    for a in divisors:
        if a > limit:
            continue
            
        b = N // a
        
        # Discriminant: 3(4b - a^2)
        discriminant = 3 * (4 * b - a * a)
        
        if discriminant < 0:
            continue
        
        # Check if discriminant is a perfect square
        sqrt_disc_float = math.sqrt(discriminant)
        sqrt_disc = int(sqrt_disc_float + 0.5)
        
        if sqrt_disc * sqrt_disc != discriminant:
            continue
        
        # y = (-3a ± sqrt_disc) / 6
        # We need the positive root
        
        # Try both signs
        for sign in [1, -1]:
            numerator = -3 * a + sign * sqrt_disc
            
            if numerator % 6 != 0:
                continue
            
            y = numerator // 6
            
            if y <= 0:
                continue
            
            x = y + a
            
            if x <= 0:
                continue
            
            # Verify the solution
            if x * x * x - y * y * y == N:
                print(x, y)
                return
    
    print(-1)

solve()
