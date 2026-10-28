import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    out = [[] for _ in range(n + 1)]  # out[a] = list of (b, c)
    idx = 2
    for _ in range(m):
        a = int(data[idx]); b = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        out[a].append((b, c))

    # Constraint: for villager A, t_B XOR C_B must be the same for all out-edges.
    # Equivalent: t_{B_first} ^ t_{B_j} = C_first ^ C_j.
    adj = [[] for _ in range(n + 1)]
    for a in range(1, n + 1):
        if len(out[a]) >= 2:
            b0, c0 = out[a][0]
            for b, c in out[a][1:]:
                w = c0 ^ c
                adj[b0].append((b, w))
                adj[b].append((b0, w))

    t = [-1] * (n + 1)
    for s in range(1, n + 1):
        if t[s] != -1:
            continue
        t[s] = 0
        dq = deque([s])
        while dq:
            u = dq.popleft()
            tu = t[u]
            for v, w in adj[u]:
                want = tu ^ w
                if t[v] == -1:
                    t[v] = want
                    dq.append(v)
                elif t[v] != want:
                    print(-1)
                    return

    res = []
    for a in range(1, n + 1):
        if out[a]:
            b0, c0 = out[a][0]
            u = t[b0] ^ c0
            res.append('1' if (t[a] ^ u) else '0')
        else:
            res.append('0')
    print(''.join(res))


main()
