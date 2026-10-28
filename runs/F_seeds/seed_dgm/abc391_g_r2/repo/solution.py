import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353

    # State: row f[0..N] where f[i] = LCS(S[:i], T_prefix).
    start = tuple([0] * (N + 1))
    index = {start: 0}
    states = [start]
    trans = []  # trans[s] = list of 26 next-state indices
    q = 0
    while q < len(states):
        f = states[q]
        row = []
        for c in range(26):
            ch = chr(97 + c)
            g = [0] * (N + 1)
            for i in range(1, N + 1):
                v = g[i - 1]
                if f[i] > v:
                    v = f[i]
                w = f[i - 1] + (1 if S[i - 1] == ch else 0)
                if w > v:
                    v = w
                g[i] = v
            g = tuple(g)
            if g not in index:
                index[g] = len(states)
                states.append(g)
            row.append(index[g])
        trans.append(row)
        q += 1

    K = len(states)
    score = [st[N] for st in states]
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
        ans[score[s]] = (ans[score[s]] + dp[s]) % MOD
    print(" ".join(map(str, ans)))

main()
