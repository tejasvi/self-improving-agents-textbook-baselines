from collections import defaultdict

MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    n = int(input())
    A = list(map(int, input().split()))
    
    # Total number of outcomes
    total = 1
    for a in A:
        total = (total * a) % MOD
    
    # We only care about sums 0 to 10
    # dp[mask] = count of outcomes resulting in this achievable mask
    # mask bit i is set if sum i is achievable from some subset
    dp = defaultdict(int)
    dp[0] = 1  # Initially, no sums achievable (we haven't added any dice yet)
    
    for i in range(n):
        new_dp = defaultdict(int)
        for mask, count in dp.items():
            # Die i can show values 1 to A[i]
            for value in range(1, A[i] + 1):
                new_mask = mask
                # Add value alone to form a new subset (if value <= 10)
                if value <= 10:
                    new_mask = new_mask | (1 << value)
                # Extend each previously achievable sum by adding value
                for s in range(11):
                    if mask & (1 << s):
                        new_sum = s + value
                        if new_sum <= 10:
                            new_mask = new_mask | (1 << new_sum)
                
                new_dp[new_mask] = (new_dp[new_mask] + count) % MOD
        dp = new_dp
    
    # Count outcomes where bit 10 is set (sum 10 is achievable)
    favorable = 0
    for mask, count in dp.items():
        if mask & (1 << 10):
            favorable = (favorable + count) % MOD
    
    # Probability = favorable / total
    result = (favorable * modinv(total)) % MOD
    print(result)

solve()
