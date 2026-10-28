import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353

    def step(r, c):
        # r[j] = LCS(current prefix, S[:j]); returns new row for appended char c
        nr = [0] * (N + 1)
        for j in range(1, N + 1):
            v = nr[j - 1]
            if r[j] > v:
                v = r[j]
            t = r[j - 1] + (1 if S[j - 1] == c else 0)
            if t > v:
                v = t
            nr[j] = v
        return tuple(nr)

    start = tuple([0] * (N + 1))
    idx = {start: 0}
    states = [start]
    trans = []
    q = 0
    while q < len(states):
        r = states[q]
        row = []
        for ci in range(26):
            c = chr(97 + ci)
            nr = step(r, c)
            if nr not in idx:
                idx[nr] = len(states)
                states.append(nr)
            row.append(idx[nr])
        trans.append(row)
        q += 1

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
        ans[states[s][N]] = (ans[states[s][N]] + dp[s]) % MOD
    print(" ".join(map(str, ans)))

main()
