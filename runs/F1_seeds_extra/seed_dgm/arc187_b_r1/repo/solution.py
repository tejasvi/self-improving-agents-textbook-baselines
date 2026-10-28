import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    b = [int(x) for x in data[2:2 + n]]
    q = sum(1 for x in b if x == -1)
    ans = pow(m, q, MOD)

    # Cut after position k (1 <= k <= n-1) happens iff
    # min(prefix) > max(suffix). Sum over prefix-min value v:
    #   (#prefix with min exactly v) * (#suffix with max < v)
    # E(v)[k] = prod_{i<k} #{choices of b_i >= v}
    # L(u)[k] = prod_{i>=k} #{choices of b_i <= u}
    def build_E(v):
        E = [1] * (n + 1)
        for k in range(n):
            x = b[k]
            if x == -1:
                c = m - v + 1 if v <= m else 0
            else:
                c = 1 if x >= v else 0
            E[k + 1] = E[k] * c % MOD
        return E

    def build_L(u):
        L = [1] * (n + 1)
        for i in range(n - 1, -1, -1):
            x = b[i]
            if x == -1:
                c = u if u > 0 else 0
            else:
                c = 1 if x <= u else 0
            L[i] = L[i + 1] * c % MOD
        return L

    total = 0
    E_next = build_E(m + 1)
    for v in range(m, 0, -1):
        E_cur = build_E(v)
        L = build_L(v - 1)
        s = 0
        for k in range(1, n):
            ex = E_cur[k] - E_next[k]
            if ex:
                s += ex * L[k]
        total = (total + s) % MOD
        E_next = E_cur
    ans = (ans + total) % MOD
    print(ans)


main()
