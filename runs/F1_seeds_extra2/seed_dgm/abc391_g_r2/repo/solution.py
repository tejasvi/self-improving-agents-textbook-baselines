import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353

    def step(row, c):
        new = [0] * (N + 1)
        for j in range(1, N + 1):
            if S[j - 1] == c:
                v = row[j - 1] + 1
            else:
                v = row[j]
            if new[j - 1] > v:
                v = new[j - 1]
            if row[j] > v:
                v = row[j]
            new[j] = v
        return tuple(new)

    init = tuple([0] * (N + 1))
    idx = {init: 0}
    rows = [init]
    trans = []  # trans[s] = list of 26 target indices
    q = 0
    letters = [chr(ord('a') + i) for i in range(26)]
    while q < len(rows):
        r = rows[q]
        t = []
        for c in letters:
            nr = step(r, c)
            if nr not in idx:
                idx[nr] = len(rows)
                rows.append(nr)
            t.append(idx[nr])
        trans.append(t)
        q += 1

    K = len(rows)
    dp = [0] * K
    dp[0] = 1
    for _ in range(M):
        nd = [0] * K
        for s in range(K):
            v = dp[s]
            if v:
                for ti in trans[s]:
                    nd[ti] += v
        dp = [x % MOD for x in nd]

    ans = [0] * (N + 1)
    for s in range(K):
        ans[rows[s][N]] = (ans[rows[s][N]] + dp[s]) % MOD
    print(' '.join(map(str, ans)))

main()
