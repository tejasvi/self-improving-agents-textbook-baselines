import sys

MOD = 998244353


def factorize(n):
    res = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            res[d] = res.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        res[n] = res.get(n, 0) + 1
    return res


def step(X, ek, M):
    # Y[v] = X[v+ek] + X[v-ek] (for ek>0), Y = X for ek == 0; values in [0, M)
    if ek == 0:
        return X
    Xa = X[ek:] + [0] * ek               # Xa[v] = X[v+ek]
    Xb = [0] * ek + X[:len(X) - ek]      # Xb[v] = X[v-ek] (v >= ek)
    return [(a + b) % MOD for a, b in zip(Xa, Xb)]


def solve_prime(p, e, n):
    # e[i-1] = v_p(A_i), i = 1..n-1 ; x_1..x_n exponents of p in S_1..S_n
    B = sum(e)
    M = B + 1
    pw = [1] * (M + 1)
    for k in range(1, M + 1):
        pw[k] = pw[k - 1] * p % MOD

    # Backward: H_k(v) = sum over x_{k+1..n} valid given x_k = v, weights p^{x_m}, m > k
    Hz = [0] * (n + 1)
    H = [1] * M
    Hz[n] = 1
    for k in range(n - 1, 0, -1):
        ek = e[k - 1]
        W = [h * pw[u] % MOD for u, h in enumerate(H)]
        H = step(W, ek, M)
        Hz[k] = H[0]

    # Forward: G_j(u) = F_j(u) * p^u, F_j(u) = sum over x_1..x_{j-1} all > 0, x_j = u
    G = [0] + [pw[v] for v in range(1, M)]
    total = Hz[1]  # x_1 = 0 : left part is empty
    for j in range(2, n + 1):
        ek = e[j - 2]
        left = G[ek] if ek > 0 else 0   # x_{j-1} = ek > 0, x_j = 0
        if left:
            total = (total + left * Hz[j]) % MOD
        if j == n:
            break
        S = step(G, ek, M)
        G = [0] + [S[v] * pw[v] % MOD for v in range(1, M)]
    return total % MOD


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:n]]
    fac = [factorize(a) for a in A]
    primes = set()
    for f in fac:
        primes.update(f.keys())

    ans = 1
    for p in sorted(primes):
        e = [f.get(p, 0) for f in fac]
        ans = ans * solve_prime(p, e, n) % MOD
    print(ans % MOD)


main()
