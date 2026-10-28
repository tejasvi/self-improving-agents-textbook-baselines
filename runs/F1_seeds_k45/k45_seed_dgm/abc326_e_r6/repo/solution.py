MOD = 998244353

def modinv(a, m=MOD):
    """Calculate modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # E[i] = expected salary starting from state i
    # E[n] = 0 (can't roll higher than n)
    # E[i] = (1/n) * sum(A[j] + E[j] for j in range(i+1, n))
    
    inv_n = modinv(n)
    
    # Build system of equations - work backwards
    E = [0] * (n + 1)
    E[n] = 0  # Base case: can't win anything from state n
    
    # Working backwards from i = n-1 to i = 0
    for i in range(n - 1, -1, -1):
        # E[i] = (1/n) * sum(A[j] + E[j] for j in range(i+1, n))
        # Note: a is 0-indexed, so a[j] is the j-th element (1-indexed die shows j)
        total = 0
        for j in range(i + 1, n):
            total = (total + a[j] + E[j]) % MOD
        
        E[i] = (total * inv_n) % MOD
    
    print(E[0])

solve()
