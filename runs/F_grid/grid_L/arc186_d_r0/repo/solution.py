import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]

    N = n
    MAXF = 2 * N + 5
    fact = [1] * (MAXF + 1)
    for i in range(1, MAXF + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv = [1] * (MAXF + 1)
    inv[MAXF] = pow(fact[MAXF], MOD - 2, MOD)
    for i in range(MAXF, 0, -1):
        inv[i - 1] = inv[i] * i % MOD

    def C(a, b):
        if b < 0 or a < 0 or b > a:
            return 0
        return fact[a] * inv[b] % MOD * inv[a - b] % MOD

    # sum_{k=a}^{b} G(L,k) for 1 <= a <= b <= L, L >= 1
    # G(L,k) = 2*C(n, L-1) - C(n+1, L), n = 2L-k-1
    def rangesum(L, a, b):
        if a > b:
            return 0
        # n in [lo, hi]
        lo = 2 * L - 1 - b
        hi = 2 * L - 1 - a
        s1 = (C(hi + 1, L) - C(lo, L)) % MOD  # sum C(n, L-1)
        # m = n+1 in [lo+1, hi+1]; sum C(m, L) = C(hi+2, L+1) - C(lo+1, L+1)
        s2 = (C(hi + 2, L + 1) - C(lo + 1, L + 1)) % MOD
        return (2 * s1 - s2) % MOD

    ans = 0
    c = 1  # pending subtrees before position i (1-indexed)
    valid = True
    for i in range(1, N + 1):  # i is 1-indexed
        a_i = A[i - 1]
        L = N - i
        if L == 0:
            # need after = c-1+v must be 0 with v < a_i
            if c == 1 and a_i > 0:
                ans += 1
        else:
            if a_i > 0:
                lo_k = max(1, c - 1)
                hi_k = min(L, c - 1 + a_i - 1)
                ans += rangesum(L, lo_k, hi_k)
        # follow A
        c = c - 1 + a_i
        if c == 0:
            if i == N:
                ans += 1  # A itself is Polish
            valid = False
            break
        if c < 0:
            valid = False
            break
    else:
        # loop finished without break: c must be 0 at end for A Polish
        pass
    ans %= MOD
    print(ans)


main()
