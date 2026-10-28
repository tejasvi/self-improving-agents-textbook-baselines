import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    B = [int(x) for x in data[2:2 + n]]
    q = sum(1 for x in B if x == -1)

    # For cut k (1 <= k <= n-1): prefix = B[:k] (positions 1..k), suffix = B[k:].
    # Cut is valid iff min(prefix) > max(suffix).
    # Sum over w: #prefix fills with min exactly w  * #suffix fills with max <= w-1.
    #  G_k(w) = #prefix fills with all >= w = [w <= L_k] * (m-w+1)^{c_k}
    #  H_k(v) = #suffix fills with all <= v = [v >= R_k] * v^{d_k}
    R = [0] * (n + 1)   # max fixed value in B[k:]
    d = [0] * (n + 1)   # count of -1 in B[k:]
    for i in range(n - 1, -1, -1):
        if B[i] == -1:
            R[i] = R[i + 1]
            d[i] = d[i + 1] + 1
        else:
            R[i] = max(R[i + 1], B[i])
            d[i] = d[i + 1]

    L = [m + 1] * (n + 1)  # min fixed value in B[:k]
    c = [0] * (n + 1)      # count of -1 in B[:k]
    for i in range(n):
        if B[i] == -1:
            L[i + 1] = L[i]
            c[i + 1] = c[i] + 1
        else:
            L[i + 1] = min(L[i], B[i])
            c[i + 1] = c[i]

    total = pow(m, q, MOD)
    inv = [0] * (m + 2)
    for v in range(1, m + 2):
        inv[v] = pow(v, MOD - 2, MOD)

    # pc[w] = (m-w+1)^{c} for w in 1..m, index 0 and m+1 unused (0)
    base = [0] + [m - w + 1 for w in range(1, m + 1)] + [0]
    pc = [0] + [pow(base[w], c[1], MOD) for w in range(1, m + 1)] + [0]
    cur_c = c[1]
    # ph[v] = v^{d} for v in 0..m
    ph = [pow(v, d[1], MOD) for v in range(0, m + 1)] + [0]
    cur_d = d[1]
    # Process k ascending: c nondecreasing, d nonincreasing.
    for k in range(1, n):
        ck = c[k]
        while cur_c < ck:
            pc = [0] + [pc[w] * base[w] % MOD for w in range(1, m + 1)] + [0]
            cur_c += 1
        dk = d[k]
        while cur_d > dk:
            # divide by v: v^{d-1} = v^d * inv(v) for v >= 1; 0^{d-1} is 0 when d-1>0, else 1
            ph = [0] + [ph[v] * inv[v] % MOD for v in range(1, m + 1)] + [0]
            cur_d -= 1
            if cur_d == 0:
                ph[0] = 1
            else:
                ph[0] = 0
        Lk = min(L[k], m)
        lo = max(1, R[k] + 1)
        cnt = 0
        for w in range(lo, Lk + 1):
            nxt = pc[w + 1] if w + 1 <= Lk else 0
            ep = pc[w] - nxt
            if ep:
                cnt += ep * ph[w - 1]
        total = (total + cnt) % MOD
    print(total % MOD)

main()
