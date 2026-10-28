import sys

MOD = 998244353


def factorize(x):
    res = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            res[d] = res.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        res[x] = res.get(x, 0) + 1
    return res


def solve_prime(p, a, N):
    # Positions 1..N. a[j-1] = a_j = |e_{j+1} - e_j| for j=1..N-1.
    # e_k >= 0, min over k is 0, weight prod p^{e_k}. Sum over all such sequences.
    # Split at first position t with e_t = 0.
    #   L_t = sum over e_1..e_{t-1} >=1, e_{t-1}=a_{t-1}, of prod p^{e_k}   (F_{t-1}[a_{t-1}])
    #   R_t = sum over e_{t+1}..e_N >=0, e_{t+1}=a_t, of prod_{k>t} p^{e_k}  (B_{t+1}[a_t])
    # Bounds: valid sequences have e_j <= c_j = max(pre_j, suf_j); truncation is exact.
    pre = [0] * (N + 2)  # pre[j] = a_1+..+a_{j-1}
    for j in range(2, N + 1):
        pre[j] = pre[j - 1] + a[j - 2]
    suf = [0] * (N + 2)  # suf[j] = a_j + ... + a_{N-1}
    for j in range(N - 1, 0, -1):
        suf[j] = suf[j + 1] + a[j - 1]
    c = [max(pre[j], suf[j]) for j in range(N + 2)]
    H = max(c[1:N + 1])

    pw = [1] * (H + 1)
    for h in range(1, H + 1):
        pw[h] = pw[h - 1] * p % MOD

    # Forward: F_j[h], 0 <= h <= c_j, h>=1 ; F_1[h] = p^h
    L = [0] * (N + 2)
    L[1] = 1
    F = [0] + pw[1:c[1] + 1]
    for j in range(1, N):
        aj = a[j - 1]
        L[j + 1] = F[aj] if aj < len(F) else 0
        if j == N - 1:
            break
        nl = c[j + 1] + 1
        # newF[h] = pw[h] * (F[h-aj] + F[h+aj]) for h in [0,nl); F[0]=0, out-of-range=0
        X = ([0] * aj + F)[:nl]
        X += [0] * (nl - len(X))
        if aj:
            Y = F[aj:aj + nl]
            Y += [0] * (nl - len(Y))
        else:
            Y = [0] * nl
        F = [(x + y) * w % MOD for x, y, w in zip(X, Y, pw)]
        F[0] = 0

    # Backward: B_j[h], 0 <= h <= c_j ; B_N[h] = p^h (includes p^{e_N})
    R = [0] * (N + 2)
    R[N] = 1
    B = pw[:c[N] + 1]
    for t in range(N - 1, 0, -1):
        at = a[t - 1]
        R[t] = B[at] if at < len(B) else 0  # B = B_{t+1}
        if t == 1:
            break
        nl = c[t] + 1
        # newB[h] = pw[h] * (B[h-at] + B[h+at]), out-of-range = 0
        X = ([0] * at + B)[:nl]
        X += [0] * (nl - len(X))
        if at:
            Y = B[at:at + nl]
            Y += [0] * (nl - len(Y))
        else:
            Y = [0] * nl
        B = [(x + y) * w % MOD for x, y, w in zip(X, Y, pw)]

    G = 0
    for t in range(1, N + 1):
        G = (G + L[t] * R[t]) % MOD
    return G


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    A = [int(x) for x in data[1:N]]
    primes = {}
    facs = []
    for x in A:
        f = factorize(x)
        facs.append(f)
        for p in f:
            primes[p] = True
    ans = 1
    for p in primes:
        a = [f.get(p, 0) for f in facs]
        ans = ans * solve_prime(p, a, N) % MOD
    print(ans)


main()
