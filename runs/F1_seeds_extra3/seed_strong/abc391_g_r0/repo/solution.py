import sys
from collections import Counter

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353

    init = tuple([0] * (N + 1))
    ids = {init: 0}
    rows = [init]
    trans = []  # trans[id] = Counter of target ids
    i = 0
    while i < len(rows):
        old = rows[i]
        cnt = Counter()
        for ci in range(26):
            c = chr(97 + ci)
            new = [0] * (N + 1)
            for j in range(1, N + 1):
                v = new[j - 1]
                if old[j] > v:
                    v = old[j]
                w = old[j - 1] + (1 if S[j - 1] == c else 0)
                if w > v:
                    v = w
                new[j] = v
            t = tuple(new)
            if t not in ids:
                ids[t] = len(rows)
                rows.append(t)
            cnt[ids[t]] += 1
        trans.append(list(cnt.items()))
        i += 1

    K = len(rows)
    dp = [0] * K
    dp[0] = 1
    for _ in range(M):
        nd = [0] * K
        for s in range(K):
            v = dp[s]
            if v:
                for t, m in trans[s]:
                    nd[t] = (nd[t] + v * m) % MOD
        dp = nd

    ans = [0] * (N + 1)
    for s in range(K):
        ans[rows[s][N]] = (ans[rows[s][N]] + dp[s]) % MOD
    print(" ".join(map(str, ans)))

main()
