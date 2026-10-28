import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]
    q = b.count(-1)
    ans = pow(m, q, MOD)  # the "+1" component of every sequence

    # prefix info: c = number of -1 in prefix, L = min fixed value in prefix (m if none)
    # suffix info: R = max fixed value in suffix (0 if none)
    sufR = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        sufR[i] = max(sufR[i + 1], b[i] if b[i] != -1 else 0)

    # A[v] = (m-v+1)^c for v in 0..m+1 ; Pge(v) = A[v] if v <= L else 0
    # B[w] = w^(q-c) for w in 0..m ; Ple(w) = B[w] if w >= R else 0
    A = [1] * (m + 2)
    base = [m - v + 1 for v in range(m + 2)]
    B = [pow(w, q, MOD) for w in range(m + 1)]
    invw = [0] + [pow(w, MOD - 2, MOD) for w in range(1, m + 1)]
    B0_is_one = (q == 0)  # 0^(q-c) at w=0

    c = 0
    L = m
    for k in range(1, n):  # prefix = positions 0..k-1 (0-indexed), suffix = k..n-1
        x = b[k - 1]
        if x == -1:
            c += 1
            A = [a * t % MOD for a, t in zip(A, base)]
            B[1:] = [bw * iw % MOD for bw, iw in zip(B[1:], invw[1:])]
            B0_is_one = False
        else:
            if x < L:
                L = x
        R = sufR[k]
        # Ple(0) = [0>=R] * B[0]
        B[0] = 1 if B0_is_one else 0
        # sum over w in [lo, hi] of (Ple(w)-Ple(w-1)) * Pge(w+1)
        lo = max(R, 1)
        hi = min(L - 1, m)
        if lo > hi:
            continue
        s1 = sum(map(int.__mul__, B[lo:hi + 1], A[lo + 1:hi + 2]))
        lo2 = max(R + 1, 1)
        s2 = 0
        if lo2 <= hi:
            s2 = sum(map(int.__mul__, B[lo2 - 1:hi], A[lo2 + 1:hi + 2]))
        ans = (ans + s1 - s2) % MOD
    print(ans % MOD)

main()
