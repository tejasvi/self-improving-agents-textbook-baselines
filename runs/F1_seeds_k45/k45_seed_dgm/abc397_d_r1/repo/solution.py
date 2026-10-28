# Write your solution here. Read from stdin, write to stdout.
import math

def solve(N):
    # We need to find positive integers (x, y) such that x^3 - y^3 = N
    # x^3 - y^3 = (x - y)(x^2 + xy + y^2) = N
    # 
    # For each divisor d of N:
    # x - y = d
    # x^2 + xy + y^2 = N/d
    # 
    # Substituting x = y + d into the second equation:
    # (y + d)^2 + (y + d)y + y^2 = N/d
    # 3y^2 + 3dy + d^2 = N/d
    # 3y^2 + 3dy + (d^2 - N/d) = 0
    # 
    # y = (-3d ± √(9d^2 - 12(d^2 - N/d))) / 6
    # y = (-3d ± √(12N/d - 3d^2)) / 6
    
    # We need d to divide N and d^3 <= 4N (for discriminant to be non-negative)
    max_d = int((4 * N) ** (1/3)) + 2  # Add small buffer for floating point errors
    
    # Find divisors of N up to max_d
    divisors = []
    
    # Check all potential divisors up to max_d
    i = 1
    while i * i <= N and i <= max_d:
        if N % i == 0:
            divisors.append(i)
            if i != N // i and N // i <= max_d:
                divisors.append(N // i)
        i += 1
    
    for d in divisors:
        if N % d != 0:
            continue
        
        quotient = N // d
        
        # Calculate discriminant: 12N/d - 3d^2 = 3(4N/d - d^2)
        discriminant = 12 * quotient - 3 * d * d
        
        if discriminant < 0:
            continue
        
        # Check if discriminant is a perfect square
        sqrt_disc = int(math.sqrt(discriminant))
        
        # Try both sqrt_disc and sqrt_disc + 1 due to floating point errors
        for sd in [sqrt_disc, sqrt_disc + 1]:
            if sd * sd != discriminant:
                continue
            
            # y = (-3d + sqrt_discriminant) / 6 (we want positive y)
            if (-3 * d + sd) % 6 == 0:
                y = (-3 * d + sd) // 6
                if y > 0:
                    x = y + d
                    # Verify the solution
                    if x > 0 and y > 0 and x * x * x - y * y * y == N:
                        return (x, y)
    
    return None

N = int(input())
result = solve(N)

if result is None:
    print(-1)
else:
    x, y = result
    print(x, y)
