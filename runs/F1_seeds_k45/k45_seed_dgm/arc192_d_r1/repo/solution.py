from math import gcd
from functools import lru_cache

MOD = 998244353

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
    return sorted(divisors)

def get_fraction_pairs(a):
    """Get all pairs (P, Q) where gcd(P, Q) = 1 and P * Q = a"""
    pairs = []
    divisors = get_divisors(a)
    for d in divisors:
        p = d
        q = a // d
        if gcd(p, q) == 1:
            pairs.append((p, q))
    return pairs

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # For each position, get all possible (P, Q) pairs where P/Q in lowest terms and P*Q = A_i
    fraction_pairs = [get_fraction_pairs(a_i) for a_i in a]
    
    result = 0
    
    # DFS to enumerate all valid sequences
    def dfs_helper(frac_idx, relative_seq):
        """
        frac_idx: index of fraction we just processed (0 to n-2)
        relative_seq: sequence of elements representing the structure
                     where consecutive elements have ratio from fractions
        """
        nonlocal result
        
        if frac_idx == n - 2:
            # All fractions used, sequence is complete
            # relative_seq should have n elements
            # Check if gcd of all elements is 1
            overall_gcd = relative_seq[0]
            for s in relative_seq[1:]:
                overall_gcd = gcd(overall_gcd, s)
            
            if overall_gcd == 1:
                # Calculate product (score)
                product = 1
                for s in relative_seq:
                    product = (product * s) % MOD
                result = (result + product) % MOD
            return
        
        # Continue building sequence with next fraction
        last_elem = relative_seq[-1]
        p_next, q_next = fraction_pairs[frac_idx + 1]
        
        # We need last_elem / next = p_next / q_next
        # So next = last_elem * q_next / p_next
        # For next to be an integer, p_next must divide last_elem
        
        if last_elem % p_next == 0:
            next_elem = (last_elem // p_next) * q_next
            dfs_helper(frac_idx + 1, relative_seq + [next_elem])
    
    # Start DFS with each possible first fraction pair
    for p0, q0 in fraction_pairs[0]:
        # First two elements: S_0 / S_1 = p0 / q0
        # We can set S_0 = p0, S_1 = q0 as a base
        dfs_helper(0, [p0, q0])
    
    print(result)

solve()
