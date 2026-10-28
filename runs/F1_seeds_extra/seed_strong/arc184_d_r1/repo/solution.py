import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    Yx = [0] * (n + 2)  # Yx[x] = y of the point with X = x (1-based)
    for i in range(n):
        x = int(data[1 + 2 * i])
        y = int(data[2 + 2 * i])
        Yx[x] = y

    def valid(a, b, c, d):
        # points with x in (a,b) and y in (c,d) must each have a
        # same-direction partner inside the rectangle (no isolated point)
        if b - a <= 1 or d - c <= 1:
            return True
        sel = [Yx[x] for x in range(a + 1, b) if c < Yx[x] < d]
        m = len(sel)
        if m <= 1:
            return m == 0
        pre = [0] * m
        cur = sel[0] + 1
        for i in range(m):
            if sel[i] < cur:
                cur = sel[i]
            pre[i] = cur
        suf_max = -1
        for i in range(m - 1, -1, -1):
            v = sel[i]
            # v is a prefix-min and suffix-max -> no comparable partner
            if pre[i] == v and suf_max < v:
                # verify it's a prefix minimum and suffix maximum
                return False
            if v > suf_max:
                suf_max = v
        return True

    total_valid = valid(0, n + 1, 0, n + 1)
    Lv = [0] * (n + 1)
    Rv = [0] * (n + 1)
    for j in range(1, n + 1):
        Lv[j] = 1 if valid(0, j, Yx[j], n + 1) else 0
        Rv[j] = 1 if valid(j, n + 1, 0, Yx[j]) else 0

    f = [0] * (n + 1)
    for k in range(1, n + 1):
        acc = Lv[k]
        yk = Yx[k]
        for j in range(1, k):
            if f[j] and Yx[j] > yk:
                if valid(j, k, yk, Yx[j]):
                    acc += f[j]
        f[k] = acc % MOD

    ans = total_valid
    for j in range(1, n + 1):
        if Rv[j]:
            ans += f[j]
    print(ans % MOD)


main()
