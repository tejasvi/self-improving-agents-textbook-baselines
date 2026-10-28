import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    S = data[2]

    # Row L[j] = LCS(T, S[:j]) for j = 0..N; represented by its tuple.
    def step(row, c):
        new = [0] * (N + 1)
        for j in range(1, N + 1):
            best = new[j - 1]
            if row[j] > best:
                best = row[j]
            if S[j - 1] == c and row[j - 1] + 1 > best:
                best = row[j - 1] + 1
            new[j] = best
        return tuple(new)

    start = tuple([0] * (N + 1))
    index = {start: 0}
    rows = [start]
    trans = []
    i = 0
    while i < len(rows):
        row = rows[i]
        t = [0] * 26
        for ci in range(26):
            c = chr(ord('a') + ci)
            nr = step(row, c)
            if nr not in index:
                index[nr] = len(rows)
                rows.append(nr)
            t[ci] = index[nr]
        trans.append(t)
        i += 1

    K = len(rows)
    dp = [0] * K
    dp[0] = 1
    for _ in range(M):
        nd = [0] * K
        for s in range(K):
            v = dp[s]
            if v:
                ts = trans[s]
                for ns in ts:
                    nd[ns] += v
        dp = [x % MOD for x in nd]

    ans = [0] * (N + 1)
    for s in range(K):
        if dp[s]:
            ans[rows[s][N]] = (ans[rows[s][N]] + dp[s]) % MOD
    print(' '.join(map(str, ans)))


main()
