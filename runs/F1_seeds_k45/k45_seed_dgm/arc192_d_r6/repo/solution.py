from math import gcd
from functools import lru_cache
from collections import defaultdict
from fractions import Fraction

MOD = 998244353

def get_prime_factors(n):
    """Get prime factorization as a dictionary"""
    factors = defaultdict(int)
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] += 1
            n //= d
        d += 1
    if n > 1:
        factors[n] += 1
    return factors

def get_coprime_factorizations(n):
    """Get all ways to factorize n into coprime pairs (p, q) where p*q = n"""
    if n == 1:
        return [(1, 1)]
    
    prime_factors = get_prime_factors(n)
    primes = list(prime_factors.keys())
    
    # For each prime factor, we decide whether it goes to p or q
    factorizations = []
    
    # Generate all 2^k subsets of primes
    k = len(primes)
    for mask in range(1 << k):
        p = 1
        q = 1
        for i, prime in enumerate(primes):
            power = prime_factors[prime]
            if mask & (1 << i):
                p *= prime ** power
            else:
                q *= prime ** power
        factorizations.append((p, q))
    
    return factorizations

def fraction_to_components(frac):
    """Convert a Fraction to its numerator and denominator"""
    return frac.numerator, frac.denominator

def get_lcm(a, b):
    return a * b // gcd(a, b)

def gcd_multiple(nums):
    """Get gcd of multiple numbers"""
    result = nums[0]
    for num in nums[1:]:
        result = gcd(result, num)
    return result

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # For each A_i, get all coprime factorizations
    factorizations = []
    for a in A:
        factorizations.append(get_coprime_factorizations(a))
    
    results = []
    
    def backtrack(pos, ratios):
        # pos is position in A (0 to N-2)
        # ratios is a list of Fractions, where ratios[i] = S_{i+1} / S_1
        
        if pos == N - 1:
            # We have ratios[0..N-2] representing S_2/S_1, S_3/S_1, ..., S_N/S_1
            # We need to find S_1 such that all S_i are positive integers
            
            # S_i = S_1 * ratios[i-1] for i >= 2
            # We need S_1 * ratios[i-1] to be an integer for all i
            
            # Find LCM of all denominators
            lcm_denom = 1
            for r in ratios:
                lcm_denom = get_lcm(lcm_denom, r.denominator)
            
            # Try different values of S_1
            # S_1 must be a multiple of lcm_denom
            # Also need to check gcd condition
            
            # For a minimal solution, S_1 = lcm_denom
            s1 = lcm_denom
            
            # Compute all S_i
            sequence = [s1]
            for r in ratios:
                si = s1 * r.numerator // r.denominator
                sequence.append(si)
            
            # Check gcd condition
            g = gcd_multiple(sequence)
            if g == 1:
                # Calculate score
                score = 1
                for s in sequence:
                    score *= s
                    score %= MOD
                results.append(score)
            
            # Try multiples of lcm_denom that still satisfy gcd = 1
            # Actually, we need to be more careful here
            # If we scale S_1 by k, all S_i get scaled by k (if they were integers)
            # So gcd gets multiplied by k, meaning gcd = 1 is only possible if k divides into it
            
            # Actually, we only need gcd(scaled sequence) = 1
            # If gcd of (unscaled) sequence is g, then for any k, gcd(k*sequence) = k*g
            # So g must be 1 for any scaling to work
            
            return
        
        # Try all factorizations of A[pos]
        for p, q in factorizations[pos]:
            # S_{pos} / S_{pos+1} = p / q
            # So S_{pos+1} / S_{pos} = q / p
            # So S_{pos+1} / S_1 = (S_{pos+1} / S_{pos}) * (S_{pos} / S_1)
            #                     = (q/p) * ratios[pos-1]
            
            if pos == 0:
                # S_1 / S_2 = p / q
                # S_2 / S_1 = q / p
                new_ratio = Fraction(q, p)
                new_ratios = [new_ratio]
            else:
                new_ratio = Fraction(q, p) * ratios[-1]
                new_ratios = ratios + [new_ratio]
            
            backtrack(pos + 1, new_ratios)
    
    backtrack(0, [])
    
    # Sum all results
    total = sum(results) % MOD
    print(total)

solve()
