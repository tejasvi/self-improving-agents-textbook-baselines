MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # dp[reachable_set] = count of dice configurations where this set of sums is reachable
    # reachable_set is represented as a frozenset of integers
    
    # Start: no dice assigned, only sum 0 is reachable (empty subset)
    dp = {frozenset([0]): 1}
    
    for i in range(N):
        new_dp = {}
        
        # For each current state
        for reachable_set, count in dp.items():
            # For each possible outcome of die i (value from 1 to A[i])
            for value in range(1, A[i] + 1):
                # Compute new reachable sums when we add this die
                new_reachable = set(reachable_set)
                
                # We can either include or exclude this die from subsets
                # Including: add 'value' to each previously reachable sum
                for s in reachable_set:
                    new_sum = s + value
                    # Only track sums up to 10 (we only care if we can make 10)
                    if new_sum <= 10:
                        new_reachable.add(new_sum)
                
                new_reachable = frozenset(new_reachable)
                new_dp[new_reachable] = (new_dp.get(new_reachable, 0) + count) % MOD
        
        dp = new_dp
    
    # Count configurations where sum 10 is reachable
    favorable = 0
    for reachable_set, count in dp.items():
        if 10 in reachable_set:
            favorable = (favorable + count) % MOD
    
    # Total number of outcomes
    total = 1
    for a in A:
        total = (total * a) % MOD
    
    # Probability = favorable / total
    result = (favorable * modinv(total)) % MOD
    print(result)

solve()
