import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353

    def step(f, c):
        g = [0] * (N + 1)
        for j in range(1, N + 1):
            if S[j - 1] == c:
                g[j] = f[j - 1] + 1
            else:
                g[j] = max(f[j], g[j - 1])
        return tuple(g)

    start = tuple([0] * (N + 1))
    idx = {start: 0}
    rows = [start]
    trans = []
    i = 0
    while i < len(rows):
        f = rows[i]
        tr = []
        for c in "abcdefghijklmnopqrstuvwxyz":
            g = step(f, c)
            if g not in idx:
                idx[g] = len(rows)
                rows.append(g)
            tr.append(idx[g])
        trans.append(tr)
        i += 1

    K = len(rows)
    # count transitions per (src, dst) to compress
    cnt = [0] * K
    cnt[0] = 1
    for _ in range(M):
        nc = [0] * K
        for s in range(K):
            v = cnt[s]
            if v:
                for d in trans[s]:
                    nc[d] += v
        cnt = [x % MOD for x in nc]

    ans = [0] * (N + 1)
    for s in range(K):
        ans[rows[s][N]] = (ans[rows[s][N]] + cnt[s]) % MOD
    print(" ".join(map(str, ans)))

main()
