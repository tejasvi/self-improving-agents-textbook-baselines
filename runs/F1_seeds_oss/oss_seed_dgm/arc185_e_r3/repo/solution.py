# Write your solution here. Read from stdin, write to stdout.

import sys

MOD = 998244353
INV2 = (MOD + 1) // 2  # modular inverse of 2 under MOD (since MOD is prime)

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    A = [int(next(it)) for _ in range(n)]
    max_a = max(A)

    # compute phi up to max_a using linear sieve
    phi = list(range(max_a + 1))
    primes = []
    is_comp = [False] * (max_a + 1)
    for i in range(2, max_a + 1):
        if not is_comp[i]:
            primes.append(i)
            phi[i] = i - 1
        for p in primes:
            if i * p > max_a:
                break
            is_comp[i * p] = True
            if i % p == 0:
                phi[i * p] = phi[i] * p
                break
            else:
                phi[i * p] = phi[i] * (p - 1)
    # precompute divisors for each number up to max_a (O(max_a log max_a))
    divisors = [[] for _ in range(max_a + 1)]
    for d in range(1, max_a + 1):
        for mult in range(d, max_a + 1, d):
            divisors[mult].append(d)

    # precompute powers of 2 and inverse powers of 2 up to n
    pow2 = [1] * (n + 1)
    invpow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD
        invpow2[i] = (invpow2[i - 1] * INV2) % MOD

    # cur[d] = sum_{i (processed)} invpow2[i] for which d divides A_i
    cur = [0] * (max_a + 1)
    total = 0
    out = []
    for m in range(1, n + 1):
        a = A[m - 1]
        # contribution from pairs (i, m) where i < m
        contrib = 0
        for d in divisors[a]:
            contrib = (contrib + phi[d] * cur[d]) % MOD
        contrib = (contrib * pow2[m - 1]) % MOD
        total = (total + contrib) % MOD
        out.append(str(total))
        # update cur for future positions
        w = invpow2[m]
        for d in divisors[a]:
            cur[d] = (cur[d] + w) % MOD
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
