import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    s = data[2]

    # LCS row: f[j] = LCS(prefix of T, S[:j]); state is the row tuple.
    init = tuple([0] * (n + 1))
    idx = {init: 0}
    states = [init]
    trans = []  # trans[id][c] = id of next state
    i = 0
    while i < len(states):
        f = states[i]
        row = []
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
            row.append(idx[g])
        trans.append(row)
        i += 1

    num = len(states)
    cnt = [0] * num
    cnt[0] = 1
    for _ in range(m):
        nxt = [0] * num
        for st in range(num):
            v = cnt[st]
            if v:
                for nst in trans[st]:
                    nxt[nst] += v
        cnt = [x % MOD for x in nxt]

    ans = [0] * (n + 1)
    for st in range(num):
        ans[states[st][n]] = (ans[states[st][n]] + cnt[st]) % MOD
    print(" ".join(map(str, ans)))


main()
