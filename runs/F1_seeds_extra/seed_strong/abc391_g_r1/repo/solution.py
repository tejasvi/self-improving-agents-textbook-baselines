import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    s = data[2]

    start = tuple([0] * (n + 1))
    idx = {start: 0}
    states = [start]
    edges = {}  # (from, to) -> multiplicity
    q = 0
    while q < len(states):
        f = states[q]
        q += 1
        for c in range(26):
            ch = chr(97 + c)
            g = [0] * (n + 1)
            for j in range(1, n + 1):
                v = g[j - 1]
                if f[j] > v:
                    v = f[j]
                if s[j - 1] == ch and f[j - 1] + 1 > v:
                    v = f[j - 1] + 1
                g[j] = v
            g = tuple(g)
            if g not in idx:
                idx[g] = len(states)
                states.append(g)
            t = idx[g]
            fs = idx[f]
            edges[(fs, t)] = edges.get((fs, t), 0) + 1

    # index of states: f is states[fs]; fs is its id
    E = [(a, b, w) for (a, b), w in edges.items()]
    S_cnt = len(states)
    cnt = [0] * S_cnt
    cnt[0] = 1
    for _ in range(m):
        nxt = [0] * S_cnt
        for a, b, w in E:
            ca = cnt[a]
            if ca:
                nxt[b] += ca * w
        cnt = [x % MOD for x in nxt]

    ans = [0] * (n + 1)
    for i, st in enumerate(states):
        ans[st[n]] = (ans[st[n]] + cnt[i]) % MOD
    print(" ".join(map(str, ans)))


main()
