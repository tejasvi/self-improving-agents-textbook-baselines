import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    s = data[2]
    MOD = 998244353

    # DP row over S prefixes: row[j] = LCS(S[:j], T) for current T.
    def step(row, c):
        new = [0] * (n + 1)
        for j in range(1, n + 1):
            v = new[j - 1]
            if row[j] > v:
                v = row[j]
            t = row[j - 1] + (1 if s[j - 1] == c else 0)
            if t > v:
                v = t
            new[j] = v
        return tuple(new)

    letters = [chr(ord('a') + i) for i in range(26)]
    init = tuple([0] * (n + 1))
    ids = {init: 0}
    rows = [init]
    trans = []
    i = 0
    while i < len(rows):
        r = rows[i]
        tr = []
        for c in letters:
            nr = step(r, c)
            if nr not in ids:
                ids[nr] = len(rows)
                rows.append(nr)
            tr.append(ids[nr])
        trans.append(tr)
        i += 1

    S = len(rows)
    cnt = [0] * S
    cnt[0] = 1
    for _ in range(m):
        nc = [0] * S
        for st in range(S):
            v = cnt[st]
            if v:
                for nx in trans[st]:
                    nc[nx] += v
        cnt = [x % MOD for x in nc]

    ans = [0] * (n + 1)
    for st in range(S):
        ans[rows[st][n]] = (ans[rows[st][n]] + cnt[st]) % MOD
    print(' '.join(map(str, ans)))


main()
