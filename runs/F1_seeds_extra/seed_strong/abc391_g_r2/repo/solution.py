import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353
    NS = 1 << N

    def step(state, c):
        # decode LCS row f[0..N] from difference bits
        f = [0] * (N + 1)
        for j in range(1, N + 1):
            f[j] = f[j - 1] + ((state >> (j - 1)) & 1)
        g = [0] * (N + 1)
        for j in range(1, N + 1):
            v = g[j - 1]
            if f[j] > v:
                v = f[j]
            if S[j - 1] == c and f[j - 1] + 1 > v:
                v = f[j - 1] + 1
            g[j] = v
        ns = 0
        for j in range(1, N + 1):
            if g[j] - g[j - 1]:
                ns |= 1 << (j - 1)
        return ns

    # trans[s] = list of (t, multiplicity)
    trans = []
    for s in range(NS):
        cnt = {}
        for ci in range(26):
            t = step(s, chr(97 + ci))
            cnt[t] = cnt.get(t, 0) + 1
        trans.append(list(cnt.items()))

    dp = [0] * NS
    dp[0] = 1
    for _ in range(M):
        nd = [0] * NS
        for s in range(NS):
            v = dp[s]
            if v:
                for t, m in trans[s]:
                    nd[t] += v * m
        dp = [x % MOD for x in nd]

    ans = [0] * (N + 1)
    for s in range(NS):
        ans[bin(s).count("1")] = (ans[bin(s).count("1")] + dp[s]) % MOD
    print(" ".join(map(str, ans)))

main()
