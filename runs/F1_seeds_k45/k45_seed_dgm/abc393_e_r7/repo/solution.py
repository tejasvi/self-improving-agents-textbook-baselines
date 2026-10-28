# Write your solution here. Read from stdin, write to stdout.

def get_divisors(n):
    """Get all divisors of n in descending order"""
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
    line1 = input().split()
    N, K = int(line1[0]), int(line1[1])
    
    A = list(map(int, input().split()))
    
    results = []
    
    for i in range(N):
        # For element A[i], find the maximum GCD of K elements including A[i]
        current_element = A[i]
        
        # Get all divisors of A[i] in descending order
        divisors = get_divisors(current_element)
        
        max_gcd = 1
        
        # Try each divisor from largest to smallest
        for divisor in divisors:
            # Count how many elements in A (excluding A[i]) are divisible by divisor
            count = 0
            for j in range(N):
                if j != i and A[j] % divisor == 0:
                    count += 1
            
            # If we have at least K-1 elements divisible by divisor (plus A[i]),
            # then we can achieve GCD of divisor
            if count >= K - 1:
                max_gcd = divisor
                break
        
        results.append(max_gcd)
    
    for result in results:
        print(result)

solve()
