import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353

    start = tuple([0] * (N + 1))
    idx = {start: 0}
    states = [start]
    trans = []  # trans[i] = list of 26 target indices
    q = 0
    while q < len(states):
        f = states[q]
        row = []
        for c in range(26):
            ch = chr(97 + c)
            g = [0] * (N + 1)
            for j in range(1, N + 1):
                if S[j - 1] == ch:
                    g[j] = f[j - 1] + 1
                else:
                    g[j] = max(g[j - 1], f[j])
            g = tuple(g)
            if g not in idx:
                idx[g] = len(states)
                states.append(g)
            row.append(idx[g])
        trans.append(row)
        q += 1

    K = len(states)
    dp = [0] * K
    dp[0] = 1
    for _ in range(M):
        nd = [0] * K
        for i in range(K):
            v = dp[i]
            if v:
                for t in trans[i]:
                    nd[t] += v
        dp = [x % MOD for x in nd]

    ans = [0] * (N + 1)
    for i in range(K):
        ans[states[i][N]] = (ans[states[i][N]] + dp[i]) % MOD
    print(" ".join(map(str, ans)))

main()
