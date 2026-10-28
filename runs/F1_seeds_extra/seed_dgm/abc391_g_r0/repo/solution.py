import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353

    def step(dp, c):
        new = [0] * (N + 1)
        for j in range(1, N + 1):
            v = new[j - 1]
            if dp[j] > v:
                v = dp[j]
            t = dp[j - 1] + (1 if S[j - 1] == c else 0)
            if t > v:
                v = t
            new[j] = v
        return tuple(new)

    letters = 'abcdefghijklmnopqrstuvwxyz'
    start = tuple([0] * (N + 1))
    index = {start: 0}
    states = [start]
    trans = []
    q = 0
    while q < len(states):
        st = states[q]
        row = []
        for c in letters:
            ns = step(st, c)
            if ns not in index:
                index[ns] = len(states)
                states.append(ns)
            row.append(index[ns])
        trans.append(row)
        q += 1

    # count transitions per (state, target) with multiplicity
    S_cnt = len(states)
    edges = []
    for s in range(S_cnt):
        cnt = {}
        for t in trans[s]:
            cnt[t] = cnt.get(t, 0) + 1
        edges.append(list(cnt.items()))

    dist = [0] * S_cnt
    dist[0] = 1
    for _ in range(M):
        nd = [0] * S_cnt
        for s in range(S_cnt):
            v = dist[s]
            if v:
                for t, m in edges[s]:
                    nd[t] = (nd[t] + v * m) % MOD
        dist = nd

    ans = [0] * (N + 1)
    for s in range(S_cnt):
        k = states[s][N]
        ans[k] = (ans[k] + dist[s]) % MOD
    print(' '.join(map(str, ans)))

main()
