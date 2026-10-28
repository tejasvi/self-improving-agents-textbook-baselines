import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); m = int(data[1]); s = data[2]
    MOD = 998244353

    def step(dp, c):
        new = [0] * (n + 1)
        for j in range(1, n + 1):
            v = new[j - 1]
            if dp[j] > v:
                v = dp[j]
            if s[j - 1] == c and dp[j - 1] + 1 > v:
                v = dp[j - 1] + 1
            new[j] = v
        return tuple(new)

    start = tuple([0] * (n + 1))
    index = {start: 0}
    states = [start]
    trans = []  # trans[i] = dict target_index -> multiplicity
    q = 0
    while q < len(states):
        dp = states[q]
        cnt = {}
        for ci in range(26):
            c = chr(97 + ci)
            nd = step(dp, c)
            if nd not in index:
                index[nd] = len(states)
                states.append(nd)
            t = index[nd]
            cnt[t] = cnt.get(t, 0) + 1
        trans.append(list(cnt.items()))
        q += 1

    K = len(states)
    f = [0] * K
    f[0] = 1
    for _ in range(m):
        g = [0] * K
        for i in range(K):
            v = f[i]
            if v:
                for t, mult in trans[i]:
                    g[t] = (g[t] + v * mult) % MOD
        f = g

    ans = [0] * (n + 1)
    for i in range(K):
        if f[i]:
            k = states[i][n]
            ans[k] = (ans[k] + f[i]) % MOD
    print(" ".join(map(str, ans)))

main()
