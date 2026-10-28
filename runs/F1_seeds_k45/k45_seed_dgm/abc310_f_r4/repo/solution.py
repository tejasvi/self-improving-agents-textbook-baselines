MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # DP approach:
    # dp[possible_sums_as_frozenset] = count of die outcomes where exactly these sums are achievable
    # 
    # Transition: when processing die i:
    #   For each previous state with sums S and count c:
    #     For each value v that die i can show:
    #       New state: S' = S ∪ {s + v : s in S}
    #       Add c to dp[S']
    
    # Start with empty set of dice: the only achievable sum is 0
    dp = {frozenset({0}): 1}
    
    for i in range(N):
        new_dp = {}
        for sums, count in dp.items():
            # Die i shows some value in [1, A[i]]
            for v in range(1, A[i] + 1):
                # When die i shows value v, the new achievable sums are:
                # old sums + {s + v : s in old_sums}
                # This represents choosing subsets from all dice, where we either
                # include or exclude die i
                new_sums = frozenset(sums | frozenset(s + v for s in sums))
                
                # Limit to sums <= 10 to save memory (we only care about sum 10)
                new_sums = frozenset(s for s in new_sums if s <= 10)
                
                key = new_sums
                new_dp[key] = (new_dp.get(key, 0) + count) % MOD
        
        dp = new_dp
    
    # Count favorable outcomes (where 10 is achievable)
    favorable = 0
    for sums, count in dp.items():
        if 10 in sums:
            favorable = (favorable + count) % MOD
    
    # Total outcomes
    total = 1
    for a in A:
        total = (total * a) % MOD
    
    # Result: favorable / total mod MOD
    answer = (favorable * modinv(total)) % MOD
    
    print(answer)

solve()
