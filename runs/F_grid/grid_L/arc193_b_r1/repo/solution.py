import sys

MOD = 998244353


def build():
    NONE = 3

    def step(state, c):
        f, l = state
        if c == 1:
            return state
        if l != NONE and l == c:
            return None
        return (f if f != NONE else c, c)

    def compat(d, si):
        # cycle in-degree c in {0,1,2} compatible with d_i (given s_i)
        if si == 0:
            return [c for c in (0, 1, 2) if d == c]
        return [c for c in (0, 1, 2) if d - c in (0, 1)]

    init = frozenset([(NONE, NONE)])
    idx = {init: 0}
    subs = [init]
    q = [init]
    trans = {0: [], 1: []}  # si -> list of (a, b) with multiplicity
    i = 0
    while i < len(q):
        sub = q[i]
        i += 1
        for si in (0, 1):
            for d in range(4):
                out = set()
                for st in sub:
                    for c in compat(d, si):
                        ns = step(st, c)
                        if ns is not None:
                            out.add(ns)
                if not out:
                    continue
                t = frozenset(out)
                if t not in idx:
                    idx[t] = len(subs)
                    subs.append(t)
                    q.append(t)
                trans[si].append((idx[sub], idx[t]))

    accept = []
    for sub in subs:
        acc = any(f == NONE or f != l for (f, l) in sub)
        accept.append(acc)
    return len(subs), trans, accept


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    s = data[1].strip()
    S, trans, accept = build()
    # per-letter adjacency: for each source a, list of targets b (with multiplicity)
    adj = {}
    for si in (0, 1):
        lst = [[] for _ in range(S)]
        for a, b in trans[si]:
            lst[a].append(b)
        adj[si] = lst
    v = [0] * S
    v[0] = 1
    adj0, adj1 = adj[0], adj[1]
    for ch in s[:N]:
        lst = adj1 if ch == '1' else adj0
        w = [0] * S
        for a in range(S):
            x = v[a]
            if x:
                for b in lst[a]:
                    w[b] += x
        v = [x % MOD for x in w]
    ans = 0
    for i in range(S):
        if accept[i]:
            ans += v[i]
    print(ans % MOD)


main()
