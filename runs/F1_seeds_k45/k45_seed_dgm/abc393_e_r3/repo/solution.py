# Write your solution here. Read from stdin, write to stdout.

def get_divisors(n):
    """Get all divisors of n in descending order."""
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
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    
    results = []
    
    for i in range(N):
        # For element A[i], find the maximum GCD when choosing K elements including A[i]
        target = A[i]
        divisors = get_divisors(target)
        
        # Try divisors from largest to smallest
        answer = 1
        for d in divisors:
            # Count how many elements in A are divisible by d
            count = sum(1 for x in A if x % d == 0)
            
            # If we can select K elements divisible by d (including A[i] which is divisible by d)
            if count >= K:
                answer = d
                break
        
        results.append(answer)
    
    for r in results:
        print(r)

solve()
