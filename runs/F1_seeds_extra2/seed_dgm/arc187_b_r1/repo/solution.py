import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]

    q = sum(1 for x in b if x == -1)
    # Each B' contributes 1 (its base component) plus one per cut.
    ans = pow(m, q, MOD)

    # Cut after prefix [0,k), suffix [k,n), k = 1..n-1.
    # Count of (B') with cut k: sum over t of
    #   #(suffix with max exactly t) * #(prefix with min > t)
    # #(suffix with max <= t) = suf_k(t) = prod_{i>=k} le_i(t)
    # le_i(t) = t if B_i = -1 else [B_i <= t]
    # gt_i(t) = (m - t) if B_i = -1 else [B_i > t]
    # Maintain suf_k(t) for all k across t incrementally via recomputation.
    def le_arr(t):
        return [(t if x == -1 else (1 if x <= t else 0)) for x in b]

    prev_suf = None  # suf_k(t-1) for k = 0..n
    for t in range(0, m + 1):
        le = le_arr(t)
        suf = [0] * (n + 1)
        suf[n] = 1
        for i in range(n - 1, -1, -1):
            suf[i] = suf[i + 1] * le[i] % MOD
        if t >= 1:
            # exact-max counts for suffix
            ex = [(suf[k] - prev_suf[k]) % MOD for k in range(n + 1)]
            # prefix min > t counts: pre_k = prod_{i<k} gt_i(t)
            pre = 1
            s = 0
            for k in range(1, n):
                i = k - 1
                x = b[i]
                g = (m - t) if x == -1 else (1 if x > t else 0)
                pre = pre * g % MOD
                if pre:
                    s += pre * ex[k]
            ans = (ans + s) % MOD
        prev_suf = suf

    print(ans % MOD)


main()
