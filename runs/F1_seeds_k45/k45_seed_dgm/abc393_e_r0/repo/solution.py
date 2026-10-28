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
    return sorted(divisors, reverse=True)


def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    # For each position i
    for i in range(n):
        target = a[i]
        # Get all divisors of a[i] in descending order
        divisors = get_divisors(target)
        
        max_gcd = 1
        
        # Try each divisor as a potential GCD
        for divisor in divisors:
            # Count how many elements are divisible by this divisor
            count = sum(1 for x in a if x % divisor == 0)
            
            # If we can choose K elements that are all divisible by divisor
            # and a[i] is one of them, then divisor is valid
            if count >= k:
                max_gcd = divisor
                break  # Since divisors are in descending order, first match is max
        
        print(max_gcd)


solve()
