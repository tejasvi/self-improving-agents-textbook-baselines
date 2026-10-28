import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    s = data[2]

    # State: LCS DP row f[0..n] of T-prefix vs S[:j]; reachable states <= 2^n.
    init = tuple([0] * (n + 1))
    ids = {init: 0}
    rows = [init]
    trans = []  # trans[id] = list of 26 next ids
    i = 0
    while i < len(rows):
        f = rows[i]
        nxt = []
        for c in range(26):
            ch = chr(97 + c)
            g = [0] * (n + 1)
            for j in range(1, n + 1):
                v = g[j - 1]
                if f[j] > v:
                    v = f[j]
                t = f[j - 1] + (1 if s[j - 1] == ch else 0)
                if t > v:
                    v = t
                g[j] = v
            g = tuple(g)
            if g not in ids:
                ids[g] = len(rows)
                rows.append(g)
            nxt.append(ids[g])
        trans.append(nxt)
        i += 1

    num = len(rows)
    dp = [0] * num
    dp[0] = 1
    for _ in range(m):
        nd = [0] * num
        for st in range(num):
            v = dp[st]
            if v:
                for nx in trans[st]:
                    nd[nx] += v
        dp = [x % MOD for x in nd]

    ans = [0] * (n + 1)
    for st in range(num):
        if dp[st]:
            ans[rows[st][n]] = (ans[rows[st][n]] + dp[st]) % MOD
    print(" ".join(map(str, ans)))


main()
