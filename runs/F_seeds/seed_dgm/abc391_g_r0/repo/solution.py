import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353
    NS = 1 << N
    # trans[s] : dict target -> count of chars leading s -> target
    trans = []
    for s in range(NS):
        f = [0] * (N + 1)
        for j in range(1, N + 1):
            f[j] = f[j - 1] + ((s >> (j - 1)) & 1)
        d = {}
        for c in range(26):
            ch = chr(97 + c)
            g = [0] * (N + 1)
            for j in range(1, N + 1):
                v = g[j - 1]
                if f[j] > v:
                    v = f[j]
                if S[j - 1] == ch and f[j - 1] + 1 > v:
                    v = f[j - 1] + 1
                g[j] = v
            t = 0
            for j in range(1, N + 1):
                if g[j] - g[j - 1]:
                    t |= 1 << (j - 1)
            d[t] = d.get(t, 0) + 1
        trans.append(list(d.items()))
    dp = [0] * NS
    dp[0] = 1
    for _ in range(M):
        nd = [0] * NS
        for s in range(NS):
            v = dp[s]
            if v:
                for t, c in trans[s]:
                    nd[t] = (nd[t] + v * c) % MOD
        dp = nd
    ans = [0] * (N + 1)
    for s in range(NS):
        if dp[s]:
            k = bin(s).count("1")
            ans[k] = (ans[k] + dp[s]) % MOD
    print(" ".join(map(str, ans)))

main()
