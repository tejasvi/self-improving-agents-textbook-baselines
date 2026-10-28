# Fine Triplets solution using Number Theoretic Transform (NTT)
# Counts the number of triples (A, B, C) from a set S such that A < B < C and B-A = C-B.
# The algorithm works in O(M log M) where M is the maximum element (≤ 1e6).
# It uses an NTT with modulus 998244353 (primitive root 3).

import sys

MOD = 998244353
ROOT = 3  # primitive root for MOD

def ntt(a, invert):
    n = len(a)
    # bit-reversal permutation
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = pow(ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v + MOD) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    N = data[0]
    vals = data[1:1 + N]
    if N == 0:
        print(0)
        return
    max_v = max(vals)
    size = 1
    while size <= 2 * max_v:
        size <<= 1
    # indicator array
    a = [0] * size
    for v in vals:
        a[v] = 1
    # NTT forward
    ntt(a, False)
    # pointwise square (convolution with itself)
    for i in range(size):
        a[i] = a[i] * a[i] % MOD
    # inverse NTT
    ntt(a, True)
    ans = 0
    for b in vals:
        s = 2 * b
        total = a[s]
        total -= 1  # remove the (b,b) pair
        ans += total // 2
    print(ans)

if __name__ == "__main__":
    main()
