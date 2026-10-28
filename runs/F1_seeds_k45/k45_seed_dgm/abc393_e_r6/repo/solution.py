import math

def get_divisors(n):
    """Get all divisors of n"""
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return divisors

def solve():
    # Read input
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    # For each position i
    for i in range(n):
        current = a[i]
        
        # Get all divisors of current element
        divisors = get_divisors(current)
        
        # Sort divisors in descending order to find maximum first
        divisors.sort(reverse=True)
        
        max_gcd = 1
        
        # Check each divisor as a potential GCD
        for d in divisors:
            # Count how many elements are divisible by d
            count = 0
            for j in range(n):
                if a[j] % d == 0:
                    count += 1
            
            # If we can choose K elements divisible by d (including a[i])
            if count >= k:
                max_gcd = d
                break
        
        print(max_gcd)

solve()
