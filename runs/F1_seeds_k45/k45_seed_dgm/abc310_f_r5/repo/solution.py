MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # For each possible outcome (dice values), we need to check if 
    # any subset sums to 10
    
    # We'll iterate through all possible outcomes and count favorable ones
    # Total outcomes = product of all A_i
    
    total_outcomes = 1
    for a in A:
        total_outcomes *= a
    
    # We need to count outcomes where a subset sums to 10
    # Let's use recursion with memoization to enumerate outcomes
    # and check the subset sum condition
    
    favorable = 0
    
    def has_subset_sum_10(values):
        """Check if any subset of values sums to exactly 10"""
        # Use DP: dp[s] = True if sum s is achievable
        possible = {0}  # We can always achieve sum 0 by choosing nothing
        
        for v in values:
            new_possible = set(possible)
            for s in possible:
                new_sum = s + v
                if new_sum <= 10:
                    new_possible.add(new_sum)
            possible = new_possible
        
        return 10 in possible
    
    def enumerate_outcomes(index, current_values):
        nonlocal favorable
        
        if index == N:
            # We have a complete outcome
            if has_subset_sum_10(current_values):
                favorable += 1
            return
        
        # Try all values for die at index
        for value in range(1, A[index] + 1):
            enumerate_outcomes(index + 1, current_values + [value])
    
    enumerate_outcomes(0, [])
    
    # favorable / total_outcomes mod MOD
    result = (favorable * modinv(total_outcomes)) % MOD
    print(result)

solve()
