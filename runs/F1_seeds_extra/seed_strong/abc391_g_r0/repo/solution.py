import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353

    def decode(mask):
        f = [0] * (N + 1)
        for j in range(1, N + 1):
            f[j] = f[j - 1] + ((mask >> (j - 1)) & 1)
        return f

    def encode(f):
        m = 0
        for j in range(1, N + 1):
            if f[j] - f[j - 1]:
                m |= 1 << (j - 1)
        return m

    # transitions over reachable states
    start = 0
    index = {start: 0}
    states = [start]
    trans = []  # trans[i][c] = next state index
    i = 0
    while i < len(states):
        f = decode(states[i])
        row = []
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
            nm = encode(g)
            if nm not in index:
                index[nm] = len(states)
                states.append(nm)
            row.append(index[nm])
        trans.append(row)
        i += 1

    K = len(states)
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
        ans[bin(states[s]).count("1")] = (ans[bin(states[s]).count("1")] + dp[s]) % MOD
    print(" ".join(map(str, ans)))

main()
