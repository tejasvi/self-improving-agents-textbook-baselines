from math import gcd
import itertools

MOD = 998244353

def prime_factorization(n):
    """Return prime factorization as a dictionary {prime: exponent}"""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def get_coprime_factorizations(n):
    """
    Get all ways to factor n as P * Q where gcd(P, Q) = 1.
    Returns list of tuples (P, Q) sorted by P.
    """
    if n == 1:
        return [(1, 1)]
    
    # Get prime factorization
    factors = prime_factorization(n)
    
    # Generate all subsets of prime factors
    primes = list(factors.keys())
    factorizations = []
    
    # Iterate through all 2^k subsets
    for mask in range(1 << len(primes)):
        p = 1
        q = 1
        for i, prime in enumerate(primes):
            exp = factors[prime]
            if mask & (1 << i):
                p *= prime ** exp
            else:
                q *= prime ** exp
        factorizations.append((p, q))
    
    return sorted(factorizations)

def lcm(a, b):
    """Compute least common multiple"""
    return a * b // gcd(a, b)

def results_from_factorizations(facs, n):
    """
    Given factorizations [(P_0, Q_0), (P_1, Q_1), ..., (P_{n-2}, Q_{n-2})],
    where S_i / S_{i+1} = P_i / Q_i,
    compute the sequence and return its score if gcd=1, else 0.
    """
    # Build the sequence structure as ratios relative to S_1
    ratios = [(1, 1)]  # S_1 / S_1
    
    for pi, qi in facs:
        prev_num, prev_den = ratios[-1]
        new_num = prev_num * qi
        new_den = prev_den * pi
        g = gcd(new_num, new_den)
        ratios.append((new_num // g, new_den // g))
    
    # Compute LCM of all denominators to make all elements integers
    denominators = [r[1] for r in ratios]
    lcm_val = denominators[0]
    for d in denominators[1:]:
        lcm_val = lcm(lcm_val, d)
    
    # Compute the sequence
    sequence = []
    for num, den in ratios:
        sequence.append(num * (lcm_val // den))
    
    # Check if gcd of all elements is 1
    overall_gcd = sequence[0]
    for s in sequence[1:]:
        overall_gcd = gcd(overall_gcd, s)
    
    if overall_gcd > 1:
        return 0
    
    # Compute score: product of all elements
    score = 1
    for s in sequence:
        score = (score * s) % MOD
    
    return score

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # For each A_i, get all coprime factorizations
    all_factorizations = []
    for ai in a:
        all_factorizations.append(get_coprime_factorizations(ai))
    
    # Iterate through all combinations of factorizations
    result = 0
    for facs_combo in itertools.product(*all_factorizations):
        score = results_from_factorizations(facs_combo, n)
        result = (result + score) % MOD
    
    print(result)

solve()
