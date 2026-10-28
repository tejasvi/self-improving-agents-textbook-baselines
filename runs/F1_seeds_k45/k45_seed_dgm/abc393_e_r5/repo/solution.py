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
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    
    # Precompute count of elements divisible by each divisor
    divisor_count = {}
    
    # For each element, add its divisors to the count
    for num in A:
        # Get divisors and track count
        for i in range(1, int(num**0.5) + 1):
            if num % i == 0:
                divisor_count[i] = divisor_count.get(i, 0) + 1
                if i != num // i:
                    divisor_count[num // i] = divisor_count.get(num // i, 0) + 1
    
    # For each position
    for i in range(N):
        current_elem = A[i]
        
        # Get all divisors of A[i] in descending order
        divisors = []
        j = 1
        while j * j <= current_elem:
            if current_elem % j == 0:
                divisors.append(j)
                if j != current_elem // j:
                    divisors.append(current_elem // j)
            j += 1
        
        divisors.sort(reverse=True)
        
        max_gcd = 1
        
        # Try each divisor as a potential GCD
        for d in divisors:
            # Check if we can select K elements divisible by d
            if divisor_count.get(d, 0) >= K:
                max_gcd = d
                break
        
        print(max_gcd)


solve()
