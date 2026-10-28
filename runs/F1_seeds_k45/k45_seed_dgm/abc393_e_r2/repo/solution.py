import math

def get_divisors(n):
    """Get all divisors of n"""
    divisors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sorted(divisors, reverse=True)

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    results = []
    
    # For each element that must be included
    for i in range(n):
        current_element = a[i]
        
        # Get all divisors of current_element, sorted in descending order
        divisors = get_divisors(current_element)
        
        max_gcd = 1
        
        # Try each divisor as potential GCD
        for d in divisors:
            # Count how many elements in A are divisible by d
            # We need K elements total, and current_element is already one of them
            count = 0
            for j in range(n):
                if a[j] % d == 0:
                    count += 1
            
            # If we can form a subset of size K with GCD d
            if count >= k:
                max_gcd = d
                break
        
        results.append(max_gcd)
    
    for r in results:
        print(r)

solve()
