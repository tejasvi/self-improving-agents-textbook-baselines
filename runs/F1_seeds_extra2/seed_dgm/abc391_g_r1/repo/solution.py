import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353

    start = tuple([0] * (N + 1))
    ids = {start: 0}
    rows = [start]
    trans = []  # trans[id] = list of 26 target ids
    i = 0
    while i < len(rows):
        f = rows[i]
        tr = []
        for c in range(26):
            ch = chr(97 + c)
            g = [0] * (N + 1)
            for j in range(1, N + 1):
                v = g[j - 1]
                if f[j] > v:
                    v = f[j]
                w = f[j - 1] + (1 if S[j - 1] == ch else 0)
                if w > v:
                    v = w
                g[j] = v
            g = tuple(g)
            if g not in ids:
                ids[g] = len(rows)
                rows.append(g)
            tr.append(ids[g])
        trans.append(tr)
        i += 1

    K = len(rows)
    dp = [0] * K
    dp[0] = 1
    for _ in range(M):
        nd = [0] * K
        for s in range(K):
            v = dp[s]
            if v:
                for t in trans[s]:
                    nd[t] += v
        dp = [x % MOD for x in nd]

    ans = [0] * (N + 1)
    for s in range(K):
        ans[rows[s][N]] = (ans[rows[s][N]] + dp[s]) % MOD
    print(" ".join(map(str, ans)))

main()
