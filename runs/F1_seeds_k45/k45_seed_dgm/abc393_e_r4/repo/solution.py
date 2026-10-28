# Write your solution here. Read from stdin, write to stdout.

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
    # Read input
    line1 = input().split()
    N, K = int(line1[0]), int(line1[1])
    
    A = list(map(int, input().split()))
    
    results = []
    
    # For each element A_i
    for i in range(N):
        ai = A[i]
        
        # Get all divisors of A_i in descending order
        divisors = get_divisors(ai)
        
        # For each divisor, check if we can form a set of K elements with that GCD
        max_gcd = 1
        for d in divisors:
            # Count how many elements are divisible by d
            count = sum(1 for x in A if x % d == 0)
            
            # If we have at least K elements divisible by d, and one of them is A_i
            if count >= K:
                max_gcd = d
                break  # Since divisors are in descending order, first match is maximum
        
        results.append(max_gcd)
    
    # Print results
    for r in results:
        print(r)

solve()
