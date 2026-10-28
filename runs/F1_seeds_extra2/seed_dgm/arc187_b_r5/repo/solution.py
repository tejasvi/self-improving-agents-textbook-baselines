import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]

    # pref_free[k] = number of -1 among positions 1..k (1-based)
    pref_free = [0] * (n + 1)
    for i in range(1, n + 1):
        pref_free[i] = pref_free[i - 1] + (1 if b[i - 1] == -1 else 0)
    q = pref_free[n]

    # last_idx_val[v]: last position with fixed value v (0 if none)
    # first_idx_val[v]: first position with fixed value v (n+1 if none)
    last_idx_val = [0] * (m + 2)
    first_idx_val = [n + 1] * (m + 2)
    for i in range(1, n + 1):
        x = b[i - 1]
        if x != -1:
            last_idx_val[x] = i
            if first_idx_val[x] == n + 1:
                first_idx_val[x] = i

    # lastgt[w] = max position of a fixed value > w (0 if none)
    lastgt = [0] * (m + 1)
    cur = 0
    for w in range(m, -1, -1):
        lastgt[w] = cur
        if w >= 1:
            cur = max(cur, last_idx_val[w])
    # firstle[w] = min position of a fixed value <= w (n+1 if none)
    firstle = [n + 1] * (m + 1)
    cur = n + 1
    for w in range(0, m + 1):
        if w >= 1:
            cur = min(cur, first_idx_val[w])
        firstle[w] = cur

    # Cut after position k (1 <= k <= n-1) is present iff min(prefix) > max(suffix).
    # Count such (prefix, suffix) completions: group by w = max(suffix) >= 1.
    #   prefix all > w, suffix max exactly w.
    # Contribution: P_w(k) * (S_le_w(k) - S_le_{w-1}(k)).
    cut_total = 0
    for w in range(1, m + 1):
        base_p = m - w          # free prefix cells must be in (w, m]
        fl = firstle[w]         # prefix positions 1..k need all fixed > w: k < fl
        lg_w = lastgt[w]        # suffix all <= w: lg_w <= k
        lg_wm1 = lastgt[w - 1]  # suffix all <= w-1: lg_wm1 <= k
        lo = max(1, lg_w)
        hi = min(n - 1, fl - 1)
        if lo > hi:
            continue
        for k in range(lo, hi + 1):
            pf = pref_free[k]
            sf = q - pf
            s_w = pow(w, sf, MOD)
            s_wm1 = pow(w - 1, sf, MOD) if lg_wm1 <= k else 0
            cut_total += pow(base_p, pf, MOD) * (s_w - s_wm1)
        cut_total %= MOD

    ans = (pow(m, q, MOD) + cut_total) % MOD
    print(ans)


main()
