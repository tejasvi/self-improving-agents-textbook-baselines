import math

def find_cubes(N):
    """
    Find positive integers (x, y) such that x^3 - y^3 = N
    Using the identity: x^3 - y^3 = (x - y)(x^2 + xy + y^2)
    """
    
    # Try all divisors of N
    # Since a = x - y and b = x^2 + xy + y^2, we have a * b = N
    # We need a >= 1 and b >= 1
    # Also, a < b for positive x, y (since x > y, we have x - y >= 1)
    
    divisors = []
    
    # Find all divisors up to sqrt(N)
    i = 1
    while i * i <= N:
        if N % i == 0:
            divisors.append(i)
            if i != N // i:
                divisors.append(N // i)
        i += 1
    
    for a in divisors:
        b = N // a
        
        # From x - y = a and x^2 + xy + y^2 = b
        # We get: 3y^2 + 3ay + (a^2 - b) = 0
        # Discriminant: 9a^2 - 12(a^2 - b) = 12b - 3a^2 = 3(4b - a^2)
        
        discriminant = 3 * (4 * b - a * a)
        
        if discriminant < 0:
            continue
        
        # Check if discriminant is a perfect square
        sqrt_disc = math.isqrt(discriminant)
        if sqrt_disc * sqrt_disc != discriminant:
            continue
        
        # y = (-3a ± sqrt_disc) / 6
        # We need y > 0
        
        y1_num = -3 * a + sqrt_disc
        y2_num = -3 * a - sqrt_disc
        
        for y_num in [y1_num, y2_num]:
            if y_num > 0 and y_num % 6 == 0:
                y = y_num // 6
                x = y + a
                
                # Verify
                if x > 0 and y > 0 and x**3 - y**3 == N:
                    return (x, y)
    
    return None

# Read input
N = int(input())

result = find_cubes(N)

if result is None:
    print(-1)
else:
    print(result[0], result[1])
