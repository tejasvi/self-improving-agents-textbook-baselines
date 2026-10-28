import sys

def main():
    data = sys.stdin.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    SZ = 2 * n + 10
    fact = [1] * SZ
    for i in range(1, SZ):
        fact[i] = fact[i - 1] * i % MOD
    inv = [1] * SZ
    inv[SZ - 1] = pow(fact[SZ - 1], MOD - 2, MOD)
    for i in range(SZ - 1, 0, -1):
        inv[i - 1] = inv[i] * i % MOD

    def C(a, b):
        if b < 0 or a < 0 or b > a:
            return 0
        return fact[a] * inv[b] % MOD * inv[a - b] % MOD

    # H(M,k) = sum_{m=0}^{M} C(m,k) = C(M+1,k+1)
    def H(M, k):
        if M < 0:
            return 0
        return C(M + 1, k + 1)

    def S(L, x):
        # sum_{c=1}^{x} f(L,c), f(L,c) = C(2L-c-1,L-1) - C(2L-c-1,L), L>=1
        x = min(x, 2 * L - 1)
        if x <= 0:
            return 0
        a = 2 * L - 1 - x
        b = 2 * L - 2
        return ((H(b, L - 1) - H(a - 1, L - 1)) - (H(b, L) - H(a - 1, L))) % MOD

    ans = 0
    c = 1  # counter before position i (1-indexed)
    valid_full = True
    for i in range(1, n + 1):
        ai = A[i - 1]
        if i < n:
            L = n - i
            lo = max(1, c - 1)
            hi = c + ai - 2
            if hi >= lo:
                ans = (ans + S(L, hi) - S(L, lo - 1)) % MOD
        else:
            if c == 1 and ai >= 1:
                ans = (ans + 1) % MOD
        c = c - 1 + ai
        if c == 0:
            if i < n:
                valid_full = False
                break
        elif c < 0:
            valid_full = False
            break
        # c>=1 here (or finished)
    if valid_full and c == 0:
        ans = (ans + 1) % MOD
    else:
        # if loop broke early, A not Polish
        pass
    print(ans % MOD)

main()
