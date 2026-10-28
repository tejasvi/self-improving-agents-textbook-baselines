import sys

MOD = 998244353


def main():
    S = sys.stdin.readline().strip()
    n = len(S)

    # w_up[i]: ways position i is uppercase; w_low[i]: ways it is lowercase
    w_up = [0] * n
    w_low = [0] * n
    for i, c in enumerate(S):
        if c == '?':
            w_up[i] = 26
            w_low[i] = 26
        elif c.isupper():
            w_up[i] = 1
        else:
            w_low[i] = 1

    q = [0] * (n + 1)   # number of '?' in prefix of length L
    h = [0] * (n + 1)   # number of fixed uppercase in prefix
    dup = [False] * (n + 1)  # prefix contains repeated fixed uppercase
    seen = [False] * 26
    d = False
    for i, c in enumerate(S):
        q[i + 1] = q[i] + (c == '?')
        h[i + 1] = h[i] + (1 if c.isupper() else 0)
        if c.isupper():
            idx = ord(c) - 65
            if seen[idx]:
                d = True
            seen[idx] = True
        dup[i + 1] = d

    # Pre[L] = #fillings of prefix length L with pairwise distinct uppercase letters
    # f_m(q) recurrence: f(0)=1, f(1)=26+m, f(q+1)=(26+m-q) f(q) + 26 q f(q-1)
    # where m = 26 - (fixed uppercase count). Cache per m.
    cache = {}

    def seq_for(m):
        if m in cache:
            return cache[m]
        arr = [0] * (n + 1)
        arr[0] = 1
        if n >= 1:
            arr[1] = (26 + m) % MOD
        base = 26 + m
        for k in range(1, n):
            arr[k + 1] = ((base - k) * arr[k] + 26 * k * arr[k - 1]) % MOD
        cache[m] = arr
        return arr

    def pre(L):
        if dup[L]:
            return 0
        m = 26 - h[L]
        if m < 0:
            return 0
        return seq_for(m)[q[L]]

    # Bsuf[i] = prod_{j>=i} w_low[j]
    Bsuf = [1] * (n + 1)
    for i in range(n - 1, -1, -1):
        Bsuf[i] = Bsuf[i + 1] * w_low[i] % MOD

    def Bof(U):
        return Bsuf[U + 1]

    # Tsh[K+1] = sum_{U>K} (prod_{i=K+1..U} w_up[i]) * B(U)
    # use shifted array: Tsh[K+1] = T[K]
    Tsh = [0] * (n + 2)
    for K in range(n - 2, -2, -1):
        nxt = K + 1  # position K+1 in [0,n-1]
        Tsh[K + 1] = w_up[nxt] * ((Bof(nxt) + Tsh[nxt + 1]) % MOD) % MOD

    ans = 0
    for K in range(-1, n):
        if K == -1:
            pv = 1
            wl = 1
        else:
            wl = w_low[K]
            if wl == 0:
                continue
            pv = pre(K)
        if pv == 0:
            continue
        ans = (ans + pv * wl % MOD * Tsh[K + 1]) % MOD

    if h[n] == 0:
        ans = (ans + pow(26, q[n], MOD)) % MOD
    print(ans % MOD)


main()
