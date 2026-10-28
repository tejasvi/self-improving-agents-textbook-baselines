import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353
    # state: tuple f where f[j] = LCS(T, S[:j]); transitions on appending char c
    def step(f, c):
        g = [0] * (N + 1)
        for j in range(1, N + 1):
            v = g[j - 1]
            if f[j] > v:
                v = f[j]
            if S[j - 1] == c and f[j - 1] + 1 > v:
                v = f[j - 1] + 1
            g[j] = v
        return tuple(g)

    start = tuple([0] * (N + 1))
    index = {start: 0}
    states = [start]
    trans = []  # trans[i] = list of (target, multiplicity)
    i = 0
    while i < len(states):
        f = states[i]
        cnt = {}
        for c in map(chr, range(97, 123)):
            g = step(f, c)
            if g not in index:
                index[g] = len(states)
                states.append(g)
            t = index[g]
            cnt[t] = cnt.get(t, 0) + 1
        trans.append(list(cnt.items()))
        i += 1

    K = len(states)
    dp = [0] * K
    dp[0] = 1
    for _ in range(M):
        nd = [0] * K
        for s in range(K):
            v = dp[s]
            if v:
                for t, m in trans[s]:
                    nd[t] += v * m
        dp = [x % MOD for x in nd]

    ans = [0] * (N + 1)
    for s in range(K):
        ans[states[s][N]] = (ans[states[s][N]] + dp[s]) % MOD
    print(" ".join(map(str, ans)))

main()
