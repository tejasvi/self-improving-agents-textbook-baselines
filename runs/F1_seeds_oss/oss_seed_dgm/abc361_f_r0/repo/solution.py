# Write your solution here. Read from stdin, write to stdout.
import sys
import math

def integer_kth_root(n, k):
    """Return the largest integer x such that x**k <= n.
    k >= 2, n >= 1.
    """
    if k == 1:
        return n
    # Use binary search with a safe upper bound.
    low, high = 1, int(pow(n, 1.0 / k)) + 2
    while low < high:
        mid = (low + high + 1) // 2
        if pow(mid, k) <= n:
            low = mid
        else:
            high = mid - 1
    return low

def mobius_upto(limit):
    """Return list mu[0..limit] of Möbius function values.
    mu[0] is unused, mu[1] = 1.
    """
    mu = [1] * (limit + 1)
    is_prime = [True] * (limit + 1)
    primes = []
    mu[0] = 0
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > limit:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu

def solve():
    data = sys.stdin.read().strip()
    if not data:
        return
    N = int(data)
    if N < 1:
        print(0)
        return
    # maximum exponent to consider (2**e <= N) => e <= floor(log2 N)
    max_e = N.bit_length()  # this is floor(log2 N) + 1, safe upper bound
    mu = mobius_upto(max_e)
    total = 0
    for e in range(2, max_e + 1):
        if mu[e] == 0:
            continue
        root = integer_kth_root(N, e)
        cnt = root - 1  # exclude a = 1
        total += mu[e] * cnt
    # include 1 (1 = 1^b for any b >= 2)
    total += 1
    print(total)

if __name__ == "__main__":
    solve()
