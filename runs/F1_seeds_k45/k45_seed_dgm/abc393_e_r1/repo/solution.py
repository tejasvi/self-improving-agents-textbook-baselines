import math

def get_divisors(n):
    """Get all divisors of n, sorted in descending order"""
    divisors = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
        i += 1
    return sorted(divisors, reverse=True)

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    # Precompute divisor counts for all elements
    # divisor_count[d] = count of indices where a[i] % d == 0
    divisor_count = {}
    
    for i in range(n):
        divisors = get_divisors(a[i])
        for d in divisors:
            divisor_count[d] = divisor_count.get(d, 0) + 1
    
    # For each position i, find the maximum GCD
    results = []
    
    for i in range(n):
        current_val = a[i]
        divisors = get_divisors(current_val)
        
        max_gcd = 1
        
        # For each divisor of A[i], in descending order
        for d in divisors:
            # Count how many elements (excluding current) are divisible by d
            count = divisor_count[d]
            if current_val % d == 0:  # current element is divisible by d
                count -= 1
            
            # If we can pick K-1 other elements, then d is a valid GCD
            if count >= k - 1:
                max_gcd = d
                break  # Since divisors are sorted descending, first match is best
        
        results.append(max_gcd)
    
    for res in results:
        print(res)

solve()
